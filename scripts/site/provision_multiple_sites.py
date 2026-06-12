import os, dotenv
from utils import csv_handler, logger
from integrations.netbox.client import NetBoxClient
from integrations.netbox.sites import DeviceManager

dotenv.load_dotenv()

logger = logger.setup_logging('logs/integrations/netbox.log')

base_url = os.getenv('NETBOX_URL')
v1_token_RO = os.getenv('NETBOX_V1_TOKEN_RO')
v1_token_Rw = os.getenv('NETBOX_V1_TOKEN_RW')
v2_token_RO = os.getenv('NETBOX_V2_TOKEN_RO')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')


def main(file_path:str):
    netbox_client = NetBoxClient(netbox_base_url=base_url, netbox_auth_token=v2_token_RW)
    device_manager = DeviceManager(api_clinet=netbox_client)
    if not os.path.isfile(file_path):
        logger.error(f"File not found: {file_path}")
        return
    get_sites_payload = csv_handler.csv_to_payloads(file_path)
    try:
        if not get_sites_payload:
            logger.warning(f"No data found in the CSV file {file_path}. Please check the file path and contents.")
        else:
            for site in get_sites_payload:
                post_response = device_manager.provision_site_request(
                    name=site.get('name'),
                    slug=site.get('slug'),
                    status= site.get('status'),
                    description=site.get('description'),
                    region={"name": site.get('region')},
                    group={"name": site.get('group')},
                    tenant={"name": site.get('tenant')},
                )
                if post_response and 'id' in post_response:
                    logger.info(f"✅ Site provisioned successfully with Site id - {post_response.get('id')}, name - {post_response.get('name')}")
                elif post_response:
                    logger.error(f"❌ Failed to provision site. Response: {post_response.get('name')}")
        
    except Exception as e:
        logger.exception(f"An error occurred while provisioning sites: {e}")


if __name__ == '__main__':
    main(file_path='static_inventory/sites/test/test.csv')


    