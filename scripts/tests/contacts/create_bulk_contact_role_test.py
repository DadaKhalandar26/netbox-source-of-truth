import pynetbox, os, dotenv, csv
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

list_of_contacts_role = []
with open('static_inventory/organization/contacts/contact_roles.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_contacts_role.append(row)


nb = pynetbox.Api(url=base_url, token=v2_token_RW)

for contact in list_of_contacts_role:
    check_role_exists = nb.tenancy.contact_roles.get(name=contact.get('name'))
    if check_role_exists:
        print(f"🚫 contact role already exists: {contact['name']}, Skipping creation.")
        continue
    nb.tenancy.contact_roles.create(
        name=contact.get('name'),
        slug=contact.get('slug'),
        description=contact.get('description'),
    )
    print(f"✅ Created contact role: {contact['name']}")