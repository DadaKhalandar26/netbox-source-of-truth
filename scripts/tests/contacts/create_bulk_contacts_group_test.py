import pynetbox, os, dotenv, csv
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

list_of_contacts_groups = []
with open('static_inventory/organization/contacts/contact_groups.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_contacts_groups.append(row)


nb = pynetbox.Api(url=base_url, token=v2_token_RW)

for contact in list_of_contacts_groups:
    check_group_exists = nb.tenancy.contact_groups.get(name=contact.get('name'))
    if check_group_exists:
        print(f"🚫 contact group already exists: {contact['name']}, Skipping creation.")
        continue
    nb.tenancy.contact_groups.create(
        name=contact.get('name'),
        slug=contact.get('slug'),
        description=contact.get('description'),
    )
    print(f"✅ Created contact group: {contact['name']}")
