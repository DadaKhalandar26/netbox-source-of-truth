from urllib import response

import pynetbox, os, requests, json
from utils.logger import Setup_logging
from docs.netbox_docs.API_DETAILS import API_LIST, SUB_API_LIST
# below imports and variables are added for testing purpose, they will be removed once the client is ready to use in other modules
# from dotenv import load_dotenv
# from rich import print as r_print

# load_dotenv()

# base_url = os.getenv('NETBOX_URL')
# v1_token_RO = os.getenv('NETBOX_V1_TOKEN_RO')
# v1_token_Rw = os.getenv('NETBOX_V1_TOKEN_RW')
# v2_token_RO = os.getenv('NETBOX_V2_TOKEN_RO')
# v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

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
    def __init__(self, netbox_base_url:str,netbox_auth_token:str):
        """
        Initialize the NetBoxClient.

        Args:
            netbox_base_url (str): Base URL for the NetBox API.
            netbox_auth_token (str): Bearer token used for NetBox authentication.
        """
        # Base URL for all NetBox API requests
        self.netbox_base_url = netbox_base_url
        # Authentication token used for NetBox API access
        self.netbox_auth_token = netbox_auth_token
        

    def get_requests(self, url) -> dict:
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
                'Authorization': f"Bearer {self.netbox_auth_token}"
                    }
        # Execute the GET request and handle pagination if needed
        try:
            logger.info(f'Connecting to Netbox to get inventory details from: {self.netbox_base_url+url}')
            response = requests.request('GET', url=self.netbox_base_url+url, headers=header, timeout=15)
            
            response.raise_for_status() # Raise exception automatically if HTTP status code is 4xx/5xx

            get_result = response.json()
            # Follow pagination links until NetBox has returned all pages
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


    def get_pynetbox(self, api='', sub_api = None, **kwargs) -> list:
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

        # Initialize the pynetbox client using the configured base URL and auth token
        nb = pynetbox.api(url=self.netbox_base_url, token=self.netbox_auth_token)
        result = []
        try:
            if api.lower() in API_LIST:
                if sub_api and sub_api.lower() in SUB_API_LIST:
                    api_path = getattr(nb, api.lower())
                    path = getattr(api_path, sub_api.lower())
                    if not kwargs:
                        # Return all objects when no filters were provided
                        result = list(path.all())
                    else:
                        # Apply keyword filters to the NetBox endpoint
                        result = list(path.filter(**kwargs))
            elif api.lower() == 'status':
                result = list(nb.status())
            else:
                logger.error('Passed wrong api/sub_api in get_pynetbox function correct it')
        except Exception as e:
            logger.error(f'Encountered exception while fetching NetBox data: {e}')
                
        return result

    
    def post_requests(self, url, payload) -> dict:
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

        logger.debug(f'Sending POST request to NetBox endpoint: {self.netbox_base_url+url}')

        header = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.netbox_auth_token}",
                    }
        # Prepare result container for the API response
        get_result = {}
        try:
            logger.info(f'Connecting to Netbox to add new record in inventory for: {self.netbox_base_url+url}')
            if not payload:
                logger.error('Payload is empty')
                return {}
            response = requests.request('POST', url=self.netbox_base_url+url, headers=header, timeout=15, json=payload)
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
    
    def post_pynetbox(self, api='', sub_api ='', **kwargs):
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

        # Use pynetbox SDK to create a new object on the configured NetBox instance
        nb = pynetbox.api(url=self.netbox_base_url, token=self.netbox_auth_token)
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
    
    def patch_requests(self, url:str, payload:dict) -> dict:

        """
        Sends a PATCH request to a NetBox API endpoint using the requests library.
        """
        
        logger.debug(f'Sending PATCH request to NetBox endpoint: {self.netbox_base_url+url}')

        header = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.netbox_auth_token}",
                    }
        # Prepare response container for patch results
        patch_result = {}
        try:
            logger.info(f'Sending PATCH request to NetBox endpoint: {self.netbox_base_url+url}')
            if not payload:
                logger.error('Payload is empty')
                return {}
            response = requests.request('PATCH', url=self.netbox_base_url+url, headers=header, timeout=15, json=payload)
            response.raise_for_status()
            logger.debug(f'NetBox returned status code: {response.status_code}')
            patch_result = response.json()

            logger.info(f'Successfully Updated NetBox object using endpoint: {url}')

        except requests.exceptions.JSONDecodeError as J:
            logger.error(f'There is issue with pasring header/Token/url/payload error message:{J}')
        except requests.exceptions.HTTPError as e:
            logger.error(f'HTTP error occurred: {e}')
        except Exception as e:
            logger.error(f'Encountered Error: {e}')

        return patch_result
    
    def patch_pynetbox(self, api='', sub_api='', obj_id:int=None, **kwargs):

        """
        Updates a NetBox object using the pynetbox library via dynamic attribute lookup.
        """
        
        logger.debug(f'Sending PATCH request to NetBox endpoint: {api, sub_api}')

        # Use pynetbox SDK to look up the object and apply updates
        nb = pynetbox.api(url=self.netbox_base_url, token=self.netbox_auth_token)
        result = None
        try:
            if api.lower() in API_LIST:
                if sub_api and sub_api.lower() in SUB_API_LIST:
                    api_path = getattr(nb, api.lower())
                    sub_api_path = getattr(api_path, sub_api.lower())
                    path = sub_api_path.get(obj_id)
                    if not path:
                        logger.error(f'Object with ID {obj_id} not found')
                        return None
                    if kwargs:
                        result = path.update(kwargs)
                        if result:
                            logger.info(f'Successfully updated NetBox object ID {obj_id}')
                            result = path
                    else:
                        logger.error('Payload has not passed.')
            elif api.lower() == 'status':
                result = list(nb.status())
            else:
                logger.error('Passed wrong api/sub_api in get_pynetbox function correct it')
        except Exception as e:
            logger.error(f'Encountered exception while fetching NetBox data: {e}')
                
        return result
    
    def delete_requests(self, url_with_id:str, obj_id:int) -> bool:

        """
        Sends a DELETE request to a NetBox API endpoint using the requests library.

        Args:
            url_with_id (str): NetBox API endpoint path including object identifier.
            obj_id (int): Identifier of the object to delete.

        Returns:
            bool: True if deletion succeeded, False otherwise.
        """
        
        logger.debug(f'Sending DELETE request to NetBox endpoint: {self.netbox_base_url+url_with_id}')

        header = {
                'Authorization': f"Bearer {self.netbox_auth_token}",
                }
        
        # Some NetBox delete operations may include a payload; include the object ID for clarity
        payload = {'id': obj_id}

        try:
            logger.info(f'Sending DELETE request to NetBox endpoint: {self.netbox_base_url+url_with_id} for object ID: {obj_id}')
            response = requests.request('DELETE', url=self.netbox_base_url+url_with_id, headers=header, timeout=15, json=payload)
            response.raise_for_status()
            logger.debug(f'NetBox returned status code: {response.status_code}')

            logger.info(f'Successfully deleted NetBox object using endpoint: {url_with_id}')

            return True

        except requests.exceptions.JSONDecodeError as J:
            logger.error(f'There is issue with pasring header/Token/url/payload error message:{J}')
            return False
        except requests.exceptions.HTTPError as e:
            logger.error(f'HTTP error occurred: {e}')
            return False
        except Exception as e:
            logger.error(f'Encountered Error: {e}')
            return False


    def delete_pynetbox(self, api='', sub_api='', obj_id:int=None) -> bool:

        """
        Deletes a NetBox object using the pynetbox library via dynamic attribute lookup.

        Args:
            api (str): NetBox application name.
            sub_api (str): NetBox endpoint inside application.
            obj_id (int): Identifier of the object to delete.

        Returns:
            bool: True if deletion succeeded, False otherwise.
        """
        
        logger.debug(f'Sending DELETE request to NetBox endpoint: {api, sub_api}')

        # Use pynetbox SDK to look up the object and apply deletion
        nb = pynetbox.api(url=self.netbox_base_url, token=self.netbox_auth_token)
        try:
            if api.lower() in API_LIST:
                if sub_api and sub_api.lower() in SUB_API_LIST:
                    api_path = getattr(nb, api.lower())
                    sub_api_path = getattr(api_path, sub_api.lower())
                    path = sub_api_path.get(obj_id)
                    if not path:
                        logger.error(f'Object with ID {obj_id} not found')
                        return False
                    result = path.delete()
                    if result:
                        logger.info(f'Successfully deleted NetBox object ID {obj_id}')
                        return True
                    else:
                        logger.error(f'Failed to delete NetBox object ID {obj_id}')
                        return False
            elif api.lower() == 'status':
                logger.error('Status API does not support deletion')
                return False
            else:
                logger.error('Passed wrong api/sub_api in delete_pynetbox function correct it')
                return False
        except Exception as e:
            logger.error(f'Encountered exception while deleting NetBox data: {e}')
            return False       
        




if __name__ == "__main__":

    # paylaod = ({"status": "planned", "description": "Adding the Description for Test", "region": {"slug": "hyderabad"}, "group": {"slug": "lab-environment"}, "tenant": {"slug": "internal"}})

    # # header = {
    # #             'Content-Type': 'application/json',
    # #             'Authorization': f"Token {self.netbox_auth_token}",
    # #                 }
    # # response = requests.request('PATCH', url=base_url+'/api/dcim/sites/31/', headers=header, timeout=15, json=paylaod)

    # # result  = NetBoxClient.patch_requests(url='/api/dcim/sites/33/', payload=paylaod)
    # # print(result)

    # # result = NetBoxClient.patch_pynetbox(api='dcim', sub_api='sites', obj_id=37, **paylaod)
    # # r_print(list(result))

    # # header = {
    # #             'Authorization': f"Bearer {v2_token_RW}",
    # #             }
        
    # # payload = {'id': 38}

    # # response = requests.request('DELETE', url='http://34.131.182.113/api/dcim/sites/38/', headers=header, timeout=15, json=payload)

    # nb = NetBoxClient(netbox_base_url=base_url, netbox_auth_token=v2_token_RW)
    # result = nb.delete_requests(url_with_id=f'/api/dcim/sites/40/', obj_id=40)
    # print(result)

    # # nb = pynetbox.api(url=self.netbox_base_url, token=self.netbox_auth_token)

    # # site = nb.dcim.sites
    # # next_get = site.get(34)
    # # print(next_get)
    # # # response = site.update({"status": "planned", "description": "Adding the Description for Test", "region": {"slug": "hyderabad"}, "group": {"slug": "lab-environment"}, "tenant": {"slug": "internal"}})

    # # # print(response)
    pass