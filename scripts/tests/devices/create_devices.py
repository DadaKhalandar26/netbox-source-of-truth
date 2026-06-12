import os, dotenv, pynetbox, csv
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

nb = pynetbox.api(url=base_url,token=v2_token_RW)

LIST_OF_DEVICES = []
with open('static_inventory/devices/devices.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        LIST_OF_DEVICES.append(row)

for device in LIST_OF_DEVICES:
    check_group_exists = nb.dcim.devices.get(name=device.get('name'))
    if check_group_exists:
        print(f"🚫 contact group already exists: {device['name']}, Skipping creation.")
        continue

    site_name = device.get("site")
    location_name = device.get("location") 

    site_obj = nb.dcim.sites.get(name=site_name)
    if not site_obj:
        r_print(f"❌ Site '{site_name}' not found. Skipping.")
        continue

    location_obj = nb.dcim.locations.get(site_id=site_obj.id, name=location_name)
    if not location_obj:
        r_print(f"❌ Location '{location_name}' not found in Site '{site_name}'. Skipping.")
        continue

    nb.dcim.devices.create(
        name=device.get('name'),
        role={"name": device.get('role')},
        description=device.get('description'),
        device_type= {"part_number": device.get('device_type')},
        manufacturer=device.get('manufacturer'),
        site=site_obj.id,
        location=location_obj.id,
        rack={"name": device.get('rack')},
        status=device.get('status'),
        platform={"name": device.get('platform')},
        tenant={"name": device.get('tenant')},
        position=device.get('position'),
        face=device.get('face'),
    )
    print(f"✅ Created contact group: {device['name']}")
    
