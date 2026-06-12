import pynetbox, os, dotenv, csv
from rich import print as r_print
from threading import Thread

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

nb = pynetbox.api(url=base_url,token=v2_token_RW)

def create_rack(**kwargs):
    nb.dcim.racks.create(**payload)

# list_of_rack_types = []
# with open('static_inventory/racks/rack_type.csv', 'r') as csvfile:
#     csv_reader = csv.DictReader(csvfile)
#     for row in csv_reader:
#         list_of_rack_types.append(row)

list_of_racks = []
with open('static_inventory/racks/racks.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        list_of_racks.append(row)


# for rack_type in list_of_rack_types:

#     verify_rack_type_exists = nb.dcim.rack_types.get(model=rack_type.get("model"))
#     if verify_rack_type_exists:
#         r_print(f"🚫 rack already exists: {rack_type['model']}, Skipping creation.")
#         continue
#     nb.dcim.rack_types.create(
#         manufacturer={"name":rack_type.get("manufacturer")},
#         model=rack_type.get("model"),
#         slug=rack_type.get("slug"),
#         width=rack_type.get("width"),
#         u_height=rack_type.get("u_height"),
#         form_factor=rack_type.get("form_factor"),
#         description=rack_type.get("description"),
#     )
#     r_print(f"✅ Created Rack type {rack_type['model']} successfully")

# print(f'{"#"*75}\nDone with creating Rack Types\n{"#"*75}\n')

threads = []
final_payload = []
for rack in list_of_racks:
    rack_name = rack.get("name").strip()
    site_name = rack.get("site").strip()
    location_name = rack.get("location").strip()

    verify_rack_exists = nb.dcim.racks.get(name=rack.get("name"))
    if verify_rack_exists:
        r_print(f"🚫 manufacturer already exists: {rack['name']}, Skipping creation.")
        continue

    # 2. Get the exact Site ID
    site_obj = nb.dcim.sites.get(name=site_name)
    if not site_obj:
        r_print(f"❌ Site '{site_name}' not found. Skipping.")
        continue

    # 3. Get the exact Location ID (Filtered by the Site!)
    location_obj = nb.dcim.locations.get(site_id=site_obj.id, name=location_name)
    if not location_obj:
        r_print(f"❌ Location '{location_name}' not found in Site '{site_name}'. Skipping.")
        continue


    # 5. Build the Payload using STRICT INTEGER IDs
    payload = {
        "name": rack_name,
        "site": site_obj.id,          # Pass integer ID
        "location": location_obj.id,  # Pass integer ID
        "status": rack.get("status"),
        "tenant": {"name":rack.get("tenant")},
        "role": {"name": rack.get("role")},
        "rack_type": {"model":rack.get("rack_type")},
    }

    final_payload.append(payload)

print("Collected payload starting the threding")

for data in payload:
    create_threads = Thread(target=create_rack, kwargs=data)
    threads.append(create_threads)

for t in threads:
    t.start()

for t in threads:
    t.join()

