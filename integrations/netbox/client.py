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
    NetBox API Client

    Supports:
    - Raw REST API requests using requests library
    - Pynetbox SDK operations
    - Generic reusable GET methods
    - Filtering support
    - Pagination handling

    Tokens and URL are loaded from environment variables.
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
            response.raise_for_status()
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



if __name__ == "__main__":
    result = NetBoxClient.get_requests(url='/api/dcim/locations')
    
    with open('tests/test_outputs_file/netbox_client.txt', 'w') as test:
        json.dump(result, test, indent=4, ensure_ascii=False)

    # result = NetBoxClient.get_pynetbox('sites')
    # r_print(result)
    # get_details = NetBoxClient.get_pynetbox(api='status')
    # print(get_details)



        #    dcim = ['cable-terminations', 'cables', 'connected-device', 'console-port-templates', 'console-ports', 'console-server-port-templates', 'console-server-ports', 'device-bay-templates', 'device-bays', 'device-roles', 'device-types', 'devices', 'front-port-templates', 'front-ports', 'interface-templates', 'interfaces', 'inventory-item-roles', 'inventory-item-templates', 'inventory-items', 'locations', 'mac-addresses', 'manufacturers', 'module-bay-templates', 'module-bays', 'module-type-profiles', 'module-types', 'modules', 'platforms', 'power-feeds', 'power-outlet-templates', 'power-outlets', 'power-panels', 'power-port-templates', 'power-ports', 'rack-reservations', 'rack-roles', 'rack-types', 'racks', 'rear-port-templates', 'rear-ports', 'regions', 'site-groups', 'sites', 'virtual-chassis', 'virtual-device-contexts']