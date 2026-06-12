import os, yaml, dotenv, requests, pynetbox
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')

nb = pynetbox.api(url=base_url,token=v2_token_RW)

BASE_REPO_URL = "https://raw.githubusercontent.com/netbox-community/devicetype-library/refs/heads/master/"
IMPORT_DEVICE_FILE_PATH = "static_inventory/devices/device_types_imported/"
IMPORT_MODULE_FILE_PATH = "static_inventory/module_type_imported/"

def creat_dir(dir_path):
    if os.path.exists(dir_path):
        r_print(f"{dir_path} path exists ⏭️  skipping creation")
    else:
        os.mkdir(dir_path)
        if os.path.exists(dir_path):
            r_print(f'{dir_path} Created file ✅')

with open("static_inventory/devices/device_types.yaml", "r") as f:
    device_type_raw_data = yaml.safe_load(f.read())
    device_type_data = device_type_raw_data.get("device_types")
    module_type_data = device_type_raw_data.get("module_types")


for manufactures,device_type in device_type_data.items():
    MANUFACTURER_REPO_URL = f"{BASE_REPO_URL}device-types/{manufactures}/"
    vendor_dir_path = f"{IMPORT_DEVICE_FILE_PATH}{manufactures}"
    creat_dir(vendor_dir_path)
    for device in device_type:
        DEVICE_TYPE_REPO_URL=f"{MANUFACTURER_REPO_URL}{device}."
        for ext in ["yaml", "yml"]:
            FINAL_URL = f"{DEVICE_TYPE_REPO_URL}{ext}"
            imported_device_file_path = f"{vendor_dir_path}/{device}.yaml"
            get_git_data = requests.get(url=FINAL_URL)
            if get_git_data.status_code == 404:
                print(f"⚠️ 404 Error:{device} File not found for extenction {ext}. Skipping...")
                continue
            elif get_git_data.status_code == 200:
                imported_device_file_path = f"{vendor_dir_path}/{device}.yaml"
                with open(imported_device_file_path, "w") as f:
                    f.write(get_git_data.text)
                    r_print(f"✅ added date to file {imported_device_file_path}")
                with open(imported_device_file_path, "r") as f:
                    data = yaml.safe_load(f.read())

                device_type_exists = nb.dcim.device_types.get(slug=data.get("slug"))
                if device_type_exists:
                    r_print(f"🚫 manufacturer already exists: {data['model']}, Skipping creation.")
                    continue
                
                nb.dcim.device_types.create(**data)
                r_print(f"✅ Created Device manufacturer {data['model']} successfully")


for manufactures,module_type in module_type_data.items():
    MANUFACTURER_REPO_URL = f"{BASE_REPO_URL}module-types/{manufactures}/"
    vendor_dir_path = f"{IMPORT_MODULE_FILE_PATH}{manufactures}"
    creat_dir(vendor_dir_path)
    for module in module_type:
        DEVICE_TYPE_REPO_URL=f"{MANUFACTURER_REPO_URL}{module}."
        for ext in ["yaml", "yml"]:
            FINAL_URL = f"{DEVICE_TYPE_REPO_URL}{ext}"
            imported_moule_file_path = f"{vendor_dir_path}/{module}.yaml"
            get_git_data = requests.get(url=FINAL_URL)
            if get_git_data.status_code == 404:
                print(f"⚠️ 404 Error:module{module} File not found for extenction {ext}. Skipping...")
                continue
            elif get_git_data.status_code == 200:
                imported_device_file_path = f"{vendor_dir_path}/{module}.yaml"
                with open(imported_device_file_path, "w") as f:
                    f.write(get_git_data.text)
                    r_print(f"✅ added date to file {imported_device_file_path}")


                
                




