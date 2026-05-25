import pynetbox, os, requests, json
from utils.logger import Setup_logging
from docs.netbox_docs.API_DETAILS import API_LIST, SUB_API_LIST
from dotenv import load_dotenv
from rich import print as r_print

load_dotenv()

base_url = os.getenv('NETBOX_URL')
v1_token_RO = os.getenv('NETBOX_V1_TOKEN_RO')
v1_token_Rw = os.getenv('NETBOX_V1_TOKEN_RW')
v2_token_RO = os.getenv('NETBOX_V2_TOKEN_RO')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

logger = Setup_logging('logs/integrations/netbox.log')

class NetBoxClient():
    '''
    Reusable NetBox API client.

    Supports:
    - REST API operations using requests library
    - Pynetbox SDK operations
    - Pagination handling
    - Generic reusable CRUD methods
    - Logging and exception handling

    Designed for inventory and Source of Truth automation.
    '''

    @staticmethod
    def get_requests(url) -> dict:
        '''
        Generic GET method using requests library.

        Args:
            url (str):
                NetBox API endpoint path.
                Example:
                    /api/dcim/sites/

        Returns:
            dict:
                Complete API response including paginated results.

        Features:
            - Handles NetBox pagination
            - Uses Read-Only token
            - Logs all operations

        Raises:
            requests.exceptions.JSONDecodeError:
                If response is not valid JSON.
        '''
            
        logger.debug('Starting NetBox GET request')

        header = {
                'Authorization': f"Bearer {v2_token_RO}"
                    }
        try:
            logger.info(f'Connecting to Netbox to get inventory details from: {base_url+url}')
            response = requests.request('GET', url=base_url+url, headers=header, timeout=15)
            
            response.raise_for_status() # Raise exception automatically if HTTP status code is 4xx/5xx

            get_result = response.json()
            logging_message = 1
            while get_result.get('next'):
                if logging_message == 1:
                    logger.info('Netbox is looping through due to offlimit to get all data')
                    logging_message -= 1
                next_url = get_result.get('next')
                response = requests.request('GET', url=next_url, headers=header, timeout=15)
                response.raise_for_status()
                get_new_result = response.json()
                get_result['next'] = get_new_result['next']
                get_result['previous'] = get_new_result['previous']
                get_result['results'].extend(get_new_result['results'])

        except requests.exceptions.JSONDecodeError as J:
            logger.error(f'There is issue with pasring header/Token/url error message:{J}')
        except requests.exceptions.HTTPError as e:
            logger.error(f'HTTP error occurred: {e}')
        except Exception as e:
            logger.error(f'Encountered Error: {e}')

        return get_result

    @staticmethod
    def get_pynetbox(api='', sub_api = None, **kwargs) -> list:
        '''
        Generic GET method using pynetbox SDK.

        Args:
            api (str):
                NetBox application name.
                Example:
                    dcim
                    ipam
                    tenancy

            sub_api (str):
                NetBox endpoint inside application.
                Example:
                    sites
                    devices
                    locations

            **kwargs:
                Optional filter arguments.
                Example:
                    site='hyd-site-01'
                    status='active'

        Returns:
            list:
                List of NetBox objects.

        Examples:
            Get all sites:
                get_pynetbox(api='dcim', sub_api='sites')

            Filter devices:
                get_pynetbox(
                    api='dcim',
                    sub_api='devices',
                    site='hyd-site-01'
                )

            Get statuses:
                get_pynetbox(api='status')
        '''
    
        logger.debug('Starting NetBox GET request')

        nb = pynetbox.api(url=base_url, token=v1_token_RO)
        result = []
        try:
            if api.lower() in API_LIST:
                if sub_api and sub_api.lower() in SUB_API_LIST:
                    api_path = getattr(nb, api.lower())
                    path = getattr(api_path, sub_api.lower())
                    if not kwargs:
                        result = list(path.all())
                    else:
                        result = list(path.filter(**kwargs))
            elif api.lower() == 'status':
                result = list(nb.status())
            else:
                logger.error('Passed wrong api/sub_api in get_pynetbox function correct it')
        except Exception as e:
            logger.error(f'Encountered exception while fetching NetBox data: {e}')
                
        return result

    @staticmethod
    def post_requests(url, payload) -> dict:
        '''
        Generic POST method using requests library.

        Used to create new objects in NetBox using REST API calls.

        Args:
            url (str):
                NetBox API endpoint path.

                Example:
                    /api/dcim/sites/
                    /api/dcim/locations/

            payload (dict):
                JSON payload containing object details to be created.

        Returns:
            dict:
                API response containing created NetBox object details.

        Features:
            - Uses Read-Write token authentication
            - Supports JSON payloads
            - Handles HTTP error validation
            - Logs API operations
            - Supports reusable generic POST operations

        Raises:
            requests.exceptions.HTTPError:
                Raised when NetBox returns HTTP 4xx/5xx errors.

        Examples:
            Create Site:

                payload = {
                    'name': 'hyd-site-01',
                    'slug': 'hyd-site-01'
                }

                NetBoxClient.post_requests(
                    url='/api/dcim/sites/',
                    payload=payload
                )
        '''

        logger.debug(f'Sending POST request to NetBox endpoint: {base_url+url}')

        header = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {v2_token_RW}",
                    }
        get_result = {}
        try:
            logger.info(f'Connecting to Netbox to add new record in inventory for: {base_url+url}')
            if not payload:
                logger.error('Payload is empty')
                return {}
            response = requests.request('POST', url=base_url+url, headers=header, timeout=15, json=payload)
            response.raise_for_status()
            logger.debug(f'NetBox returned status code: {response.status_code}')
            get_result = response.json()

            logger.info(f'Successfully created NetBox object using endpoint: {url}')

        except requests.exceptions.JSONDecodeError as J:
            logger.error(f'There is issue with pasring header/Token/url/payload error message:{J}')
        except requests.exceptions.HTTPError as e:
            logger.error(f'HTTP error occurred: {e}')
        except Exception as e:
            logger.error(f'Encountered Error: {e}')

        return get_result
    
    @staticmethod
    def post_pynetbox(api='', sub_api ='', **kwargs):
        '''
        Generic POST method using pynetbox SDK.

        Used to create new objects in NetBox using the pynetbox library.

        Args:
            api (str):
                NetBox application name.

                Example:
                    dcim
                    ipam
                    tenancy
                    virtualization

            sub_api (str):
                NetBox endpoint inside application.

                Example:
                    sites
                    devices
                    locations
                    prefixes

            **kwargs:
                Object fields passed dynamically to pynetbox create method.

        Returns:
            object:
                Created NetBox object returned by pynetbox.

        Features:
            - Uses pynetbox SDK
            - Supports dynamic API selection
            - Supports reusable object creation
            - Uses Read-Write token authentication
            - Logs API operations and exceptions

        Examples:
            Create Site:

                NetBoxClient.post_pynetbox(
                    api='dcim',
                    sub_api='sites',
                    name='hyd-site-01',
                    slug='hyd-site-01'
                )

            Create Location:

                NetBoxClient.post_pynetbox(
                    api='dcim',
                    sub_api='locations',
                    name='hyd-location-01',
                    slug='hyd-location-01',
                    site=1
                )
        '''
        
        logger.debug(f'Sending POST request to NetBox endpoint: {api, sub_api}')

        nb = pynetbox.api(url=base_url, token=v1_token_Rw)
        result = None
        try:
            if api.lower() in API_LIST:
                if sub_api and sub_api.lower() in SUB_API_LIST:
                    api_path = getattr(nb, api.lower())
                    path = getattr(api_path, sub_api.lower())
                    if kwargs:
                        result = path.create(**kwargs)
                    else:
                        logger.error('Payload has not passed.')
            elif api.lower() == 'status':
                result = list(nb.status())
            else:
                logger.error('Passed wrong api/sub_api in get_pynetbox function correct it')
        except Exception as e:
            logger.error(f'Encountered exception while fetching NetBox data: {e}')
                
        return result



if __name__ == "__main__":

    paylaod = ({"name": "Test-SITE-08" , "slug":"test-site-08" , "status": "active"})
    result  = NetBoxClient.post_pynetbox(api='dcim', sub_api ='sites', **paylaod)
    print(list(result))

