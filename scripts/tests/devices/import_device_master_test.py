import pynetbox, os, dotenv, csv
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

nb = pynetbox.api(url=base_url,token=v2_token_RW)

list_of_device_manufacturers = []
with open('static_inventory/devices/device_manufacturer.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_device_manufacturers.append(row)

list_of_device_roles = []
with open('static_inventory/devices/device_roles.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_device_roles.append(row)

list_of_device_platforms = []
with open('static_inventory/devices/device_platforms.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_device_platforms.append(row)

for manufacturers in list_of_device_manufacturers:

    verify_manufacturer_exists = nb.dcim.manufacturers.get(name=manufacturers.get("name"))
    if verify_manufacturer_exists:
        r_print(f"🚫 manufacturer already exists: {manufacturers['name']}, Skipping creation.")
        continue
    nb.dcim.manufacturers.create(
        name=manufacturers.get("name"),
        slug=manufacturers.get("slug"),
        description=manufacturers.get("description"),
    )
    r_print(f"✅ Created Device manufacturer {manufacturers['name']} successfully")

print(f'{"#"*75}\n Done with creating Device Manufaturers\n{"#"*75}\n')

for device_role in list_of_device_roles:

    verify_device_role_exists = nb.dcim.device_roles.get(name=device_role.get("name"), colour=device_role.get("colour"))
    if verify_device_role_exists:
        r_print(f"🚫 Device role already exists: {device_role['name']}, Skipping creation.")
        continue

    nb.dcim.device_roles.create(
        name=device_role.get("name"),
        slug=device_role.get("slug"),
        color=device_role.get("color"),
        description=device_role.get("description"),
    )
    r_print(f"✅ Created Device role {device_role['name']} successfully")

print(f'{"#"*75}\n Done with creating Device Manufaturers\n{"#"*75}\n')

for device_platform in list_of_device_platforms:

    verify_device_platform_exists = nb.dcim.platforms.get(name=device_platform.get("name"))
    if verify_device_platform_exists:
        r_print(f"🚫 Device Platform already exists: {device_platform['name']}, Skipping creation.")
        continue
    nb.dcim.platforms.create(
        name=device_platform.get("name"),
        slug=device_platform.get("slug"),
        manufacturer={"name":device_platform.get("manufacturer")},
        description=device_platform.get("description"),
    )
    r_print(f"✅ Created Device Platform {device_platform['name']} successfully")
