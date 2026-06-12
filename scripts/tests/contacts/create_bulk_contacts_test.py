import pynetbox, os, dotenv, csv
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

list_of_contacts = []
with open('static_inventory/organization/contacts/contacts.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_contacts.append(row)


nb = pynetbox.Api(url=base_url, token=v2_token_RW)

for contact in list_of_contacts:
    check_contact_exists = nb.tenancy.contacts.get(name=contact.get('name'))
    if check_contact_exists:
        print(f"🚫 contact already exists: {contact['name']}, Skipping creation.")
        continue
    nb.tenancy.contacts.create(
        name=contact.get('name'),
        contact_groups=contact.get('groups'),
        title=contact.get('title'),
        email=contact.get('email'),
        phone=contact.get('phone'),
    )
    print(f"✅ Created contact for: {contact['name']}")
