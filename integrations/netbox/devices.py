import json, os
from .client import NetBoxClient
from utils.logger import Setup_logging
from dotenv import load_dotenv
from rich import print as r_print

load_dotenv()

logger = Setup_logging('logs/integrations/netbox.log')

base_url = os.getenv('NETBOX_URL')
v1_token_RO = os.getenv('NETBOX_V1_TOKEN_RO')
v1_token_Rw = os.getenv('NETBOX_V1_TOKEN_RW')
v2_token_RO = os.getenv('NETBOX_V2_TOKEN_RO')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

class DeviceManager:
    def __init__(self, api_clinet):
        self.api_client = api_clinet

    def provision_device_request(self, payload:dict):
        """
        Provisions a single device in NetBox using the provided payload.

        Args:
            payload (dict): A dictionary containing the device details to be provisioned.
        """
        try:
            response = self.api_client.post_requests(url='/dcim/devcies/', )
            if response.status_code in [200, 201]:
                logger.info(f"Device provisioned successfully: {response.json()}")
        except Exception as e:
            logger.exception(f"An error occurred while provisioning the device: {e}")




