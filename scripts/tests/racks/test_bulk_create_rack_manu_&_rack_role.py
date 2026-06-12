import pynetbox, os, dotenv, csv
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

nb = pynetbox.api(url=base_url,token=v2_token_RW)

list_of_rack_manufacturers = []
with open('static_inventory/racks/rack_manufacturer.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_rack_manufacturers.append(row)

list_of_rack_roles = []
with open('static_inventory/racks/rack_role.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_rack_roles.append(row)

for manufacturers in list_of_rack_manufacturers:

    verify_manufacturer_exists = nb.dcim.manufacturers.get(name=manufacturers.get("name"))
    if verify_manufacturer_exists:
        r_print(f"🚫 manufacturer already exists: {manufacturers['name']}, Skipping creation.")
        continue
    nb.dcim.manufacturers.create(
        name=manufacturers.get("name"),
        slug=manufacturers.get("slug"),
        description=manufacturers.get("description"),
    )
    r_print(f"✅ Created manufacturer {manufacturers['name']} successfully")

print(f'{"#"*75}\n Done with creating Manufaturers\n{"#"*75}\n')

for rack_role in list_of_rack_roles:

    verify_rack_role_exists = nb.dcim.rack_roles.get(name=rack_role.get("name"))
    if verify_rack_role_exists:
        r_print(f"🚫 rack role already exists: {rack_role['name']}, Skipping creation.")
        continue
    nb.dcim.rack_roles.create(
        name=rack_role.get("name"),
        slug=rack_role.get("slug"),
        color=rack_role.get("color"),
        description=rack_role.get("description"),
    )
    r_print(f"✅ Created rack role {rack_role['name']} successfully")


