import json, os
from .client import NetBoxClient
from utils.logger import setup_logging
from dotenv import load_dotenv
from typing import Literal
from rich import print as r_print

load_dotenv()

logger = setup_logging('logs/integrations/netbox.log')

base_url = os.getenv('NETBOX_URL')
v1_token_RO = os.getenv('NETBOX_V1_TOKEN_RO')
v1_token_Rw = os.getenv('NETBOX_V1_TOKEN_RW')
v2_token_RO = os.getenv('NETBOX_V2_TOKEN_RO')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

class DeviceManager:
    def __init__(self, api_clinet):
        self.api_client = api_clinet

    def provision_site_request(self,  
                                name: str, 
                                slug: str, 
                                status: Literal['planned','staging','active','decommissioning','retired'] | None = None, 
                                description: str | None = None, 
                                region: dict | None = None, 
                                group: dict | None = None, 
                                tenant: dict | None = None
                                ):
        """
        Provisions a single device in NetBox using the provided payload.

        Args:
            payload (dict): A dictionary containing the device details to be provisioned.
        """
        status = status.lower()
        payload = {
            "name": name,
            "slug": slug,
            "status": status,
            "description": description,
            "region": region,
            "group": group,
            "tenant": tenant,
        }

        VALID_STATUSES = ['planned', 'staging', 'active', 'decommissioning', 'retired']
        
        if status not in VALID_STATUSES:
            logger.error(f"Invalid status '{status}' provided. Must be one of: {', '.join(VALID_STATUSES)}")
            return
        response = None
        try:
            response = self.api_client.post_requests(url='/api/dcim/sites/', payload=payload)
            if response and 'id' in response:
                logger.info(f"Site provisioned successfully with Site id - {response.get('id')}, name - {response.get('name')}")
                return response
            else:
                logger.error(f"Failed to provision device. Response: {response.get('name')}")
                return response
        except Exception as e:
            logger.exception(f"An error occurred while provisioning the device: {e}")

        return response

if __name__ == '__main__':
    api_client = NetBoxClient(netbox_base_url=base_url, netbox_auth_token=v2_token_RW)
    device_manager = DeviceManager(api_client)
    device_manager.provision_site_request(
        name="Test-Site-04",
        slug="test-site-04",
        status= "active",
        description="This is Hyderabad region Test Site 4 created via API",
        region={"slug": "hyderabad"},
        group={"slug": "lab-environment"},
        tenant={"slug": "internal"},
    )



