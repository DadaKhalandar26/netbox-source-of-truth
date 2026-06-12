import pynetbox, os, dotenv, csv
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

list_of_contact_assignments = []
with open('static_inventory/organization/contacts/contact_assignments copy.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_contact_assignments.append(row)


nb = pynetbox.Api(url=base_url, token=v2_token_RW)

# 2. Initialize Local Caches
# These dictionaries will store { "Name": integer_id } to prevent duplicate API calls
cache = {
    "sites": {},
    "contacts": {},
    "roles": {}
}

def get_cached_id(cache_dict, fetch_method, name):
    """Checks local dictionary for ID. If not found, calls NetBox and caches the result."""
    if name not in cache_dict:
        # Fetch from NetBox only if we haven't seen this name yet
        obj = fetch_method(name=name)
        cache_dict[name] = obj.id if obj else None
        
    return cache_dict[name]

for contact_a in list_of_contact_assignments:

    obj_type = contact_a.get('object_type')
    obj_name = contact_a.get('object_name')
    contact_name = contact_a.get('contact')
    role_name = contact_a.get('role')
    priority = contact_a.get('priority')

    # --- CACHED ID LOOKUPS ---
    site_id = get_cached_id(cache["sites"], nb.dcim.sites.get, obj_name)
    if not site_id:
        r_print(f"[red]❌ Object '{obj_name}' not found in NetBox. Skipping.[/red]")
        continue

    contact_id = get_cached_id(cache["contacts"], nb.tenancy.contacts.get, contact_name)
    if not contact_id:
        r_print(f"[red]❌ Contact '{contact_name}' not found in NetBox. Skipping.[/red]")
        continue

    role_id = get_cached_id(cache["roles"], nb.tenancy.contact_roles.get, role_name)
    if not role_id:
        r_print(f"[red]❌ Role '{role_name}' not found in NetBox. Skipping.[/red]")
        continue

    # --- IDEMPOTENCY CHECK ---
    # We still have to check if the assignment exists, but the payload is much faster now.
    existing_assignment = nb.tenancy.contact_assignments.get(
        object_type=obj_type,
        object_id=site_id,
        contact_id=contact_id,
        role_id=role_id
    )

    if existing_assignment is not None:
        r_print(f"[yellow]⚠️ Contact assignment for '{contact_name}' on '{obj_name}' already exists. Skipping.[/yellow]")
        continue

    # --- CREATE ASSIGNMENT ---
    payload = {
        "object_type": obj_type,
        "object_id": site_id,
        "contact": contact_id,
        "role": role_id,
    }
    
    if priority:
        payload["priority"] = priority
    try:
        nb.tenancy.contact_assignments.create(**payload)
        print(f"✅ Contact {contact_a.get('contact')} assigned to {contact_a.get('object_name')}")
    except Exception as e:
        print(e)


