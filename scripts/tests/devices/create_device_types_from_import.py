import os, yaml, dotenv, pynetbox
from rich import print as r_print

dotenv.load_dotenv()
base_url = os.getenv('NETBOX_URL')
v2_token_RW = os.getenv('NETBOX_V2_TOKEN_RW')
mapping = {
    'interfaces': 'interface_templates',
    'module-bays': 'module_bay_templates',
    'console-ports': 'console_port_templates',
    'power-ports': 'power_port_templates',
    'power-outlets': 'power_outlet_templates' 
}

nb = pynetbox.api(url=base_url,token=v2_token_RW)

IMPORT_DEVICE_FILE_PATH = "static_inventory/devices/device_types_imported/"
IMPORT_MODULE_FILE_PATH = "static_inventory/module_type_imported/"

list_of_vendors_devie_types = os.listdir(IMPORT_DEVICE_FILE_PATH)
list_of_vendors_module_types = os.listdir(IMPORT_MODULE_FILE_PATH)


# for vendors in list_of_vendors_devie_types:
#     # ⚠️ FIX: Removed the trailing slash so os.listdir doesn't crash
#     device_file_path = f"{IMPORT_DEVICE_FILE_PATH}{vendors}/"
#     list_of_device_types = os.listdir(device_file_path)
    
#     if list_of_device_types:
#         for device_type in list_of_device_types:
#             device_type_file_path = f"{device_file_path}{device_type}"
            
#             with open(device_type_file_path, 'r') as f:
#                 data = yaml.safe_load(f.read())
            
#             # --- STEP 1: CLEAN UP THE DATA ---
#             data.pop("front_image", None)
#             data.pop("rear_image", None)
            
#             # Replace manufacturer string with the actual integer ID
#             mfg_obj = nb.dcim.manufacturers.get(name=data.get("manufacturer"))
#             if mfg_obj:
#                 data["manufacturer"] = mfg_obj.id
#             else:
#                 r_print(f"❌ Manufacturer '{data.get('manufacturer')}' not found. Skipping.")
#                 continue

#             # --- STEP 2: SPLIT BASE DATA FROM COMPONENTS ---
#             # We pop the components out of 'data' and store them safely.
#             # Now, 'data' only contains safe base attributes (model, slug, u_height, etc.)
#             components_to_create = {}
#             for yaml_key in mapping.keys():
#                 if yaml_key in data:
#                     components_to_create[yaml_key] = data.pop(yaml_key)

#             # --- STEP 3: CREATE OR GET THE BASE DEVICE TYPE ---
#             device_type_obj = nb.dcim.device_types.get(slug=data.get("slug"))
#             if not device_type_obj:
#                 try:
#                     # Create the base hardware model
#                     device_type_obj = nb.dcim.device_types.create(**data)
#                     r_print(f"✅ Created base Device Type: {device_type_obj.model}")
#                 except Exception as e:
#                     r_print(f"❌ Failed to create Device Type {data.get('model')}: {e}")
#                     continue
#             else:
#                 r_print(f"⚠️ Device Type already exists: {device_type_obj.model}. Appending components...")

#             dt_id = device_type_obj.id

#             # --- STEP 4: DYNAMICALLY CREATE ALL COMPONENTS ---
#             # Loop through the components we found in the YAML
#             for yaml_key, component_list in components_to_create.items():
                
#                 endpoint_name = mapping[yaml_key]
                
#                 # ⚠️ SPECIAL FIX: Pre-fetch Power Ports for this specific Device Type
#                 # We do this OUTSIDE the inner loop so we only make 1 API call, not 48!
#                 pp_cache = {}
#                 if yaml_key == 'power-outlets':
#                     # Grab only the power ports belonging to THIS device type ID
#                     device_ports = nb.dcim.power_port_templates.filter(device_type_id=dt_id)
#                     # Create a quick local dictionary: {"Power Port 1": 1502}
#                     pp_cache = {pp.name: pp.id for pp in device_ports}

#                 # Inject the ID and handle relationships
#                 for item in component_list:
#                     item["device_type"] = dt_id
                    
#                     # Safely map the string name to the exact integer ID
#                     if yaml_key == 'power-outlets' and 'power_port' in item:
#                         port_name = item["power_port"]
#                         exact_port_id = pp_cache.get(port_name)
                        
#                         if exact_port_id:
#                             item["power_port"] = exact_port_id
#                         else:
#                             r_print(f"[yellow]⚠️ Warning: Power Port '{port_name}' not found for this device. Leaving blank.[/yellow]")
#                             item.pop("power_port") # Remove it so the API doesn't crash

#                 # Dynamically fetch the pynetbox endpoint
#                 api_endpoint = getattr(nb.dcim, endpoint_name)
                
#                 try:
#                     # Bulk create!
#                     api_endpoint.create(component_list)
#                     r_print(f"[green]✅ Created {len(component_list)} {yaml_key} for {device_type_obj.model}[/green]")
#                 except Exception as e:
#                     r_print(f"[bold red]❌ Error creating {yaml_key}:[/bold red] {e}")

# Iterating Module types
for vendor in list_of_vendors_module_types:
    module_dir_path = f"{IMPORT_MODULE_FILE_PATH}{vendor}/"
    list_of_module_types = os.listdir(module_dir_path)
    
    if list_of_module_types:
        for module_file in list_of_module_types:
            module_type_file_path = f"{module_dir_path}{module_file}"
            
            with open(module_type_file_path, 'r') as f:
                data = yaml.safe_load(f.read())
            
            # --- STEP 1: CLEAN UP THE DATA ---
            data.pop("front_image", None)
            data.pop("rear_image", None)
            
            # Module Types do not use slugs in NetBox! Pop it if it exists in the YAML
            data.pop("slug", None) 
            
            # Replace manufacturer string with the actual integer ID
            mfg_obj = nb.dcim.manufacturers.get(name=data.get("manufacturer"))
            if mfg_obj:
                data["manufacturer"] = mfg_obj.id
            else:
                r_print(f"❌ Manufacturer '{data.get('manufacturer')}' not found. Skipping.")
                continue

            # --- STEP 2: SPLIT BASE DATA FROM COMPONENTS ---
            components_to_create = {}
            for yaml_key in mapping.keys():
                if yaml_key in data:
                    components_to_create[yaml_key] = data.pop(yaml_key)

            # --- STEP 3: CREATE OR GET THE BASE MODULE TYPE ---
            # ⚠️ FIX: Query by 'model' instead of 'slug', as Module Types don't have slugs
            module_type_obj = nb.dcim.module_types.get(model=data.get("model"))
            
            if not module_type_obj:
                try:
                    module_type_obj = nb.dcim.module_types.create(**data)
                    r_print(f"✅ Created base Module Type: {module_type_obj.model}")
                except Exception as e:
                    r_print(f"❌ Failed to create Module Type {data.get('model')}: {e}")
                    continue
            else:
                r_print(f"⚠️ Module Type already exists: {module_type_obj.model}. Appending components...")

            mt_id = module_type_obj.id

            # --- STEP 4: DYNAMICALLY CREATE ALL COMPONENTS ---
            for yaml_key, component_list in components_to_create.items():
                
                endpoint_name = mapping[yaml_key]
                
                # Pre-fetch Power Ports for this specific MODULE Type
                pp_cache = {}
                if yaml_key == 'power-outlets':
                    # ⚠️ FIX: Filter by module_type_id, not device_type_id
                    module_ports = nb.dcim.power_port_templates.filter(module_type_id=mt_id)
                    pp_cache = {pp.name: pp.id for pp in module_ports}

                # Inject the ID and handle relationships
                for item in component_list:
                    # ⚠️ FIX: The API key for modules is 'module_type', not 'device_type'
                    item["module_type"] = mt_id
                    
                    # Safely map the string name to the exact integer ID
                    if yaml_key == 'power-outlets' and 'power_port' in item:
                        port_name = item["power_port"]
                        exact_port_id = pp_cache.get(port_name)
                        
                        if exact_port_id:
                            item["power_port"] = exact_port_id
                        else:
                            r_print(f"[yellow]⚠️ Warning: Power Port '{port_name}' not found for this module. Leaving blank.[/yellow]")
                            item.pop("power_port") 

                # Dynamically fetch the pynetbox endpoint
                api_endpoint = getattr(nb.dcim, endpoint_name)
                
                try:
                    # Bulk create!
                    api_endpoint.create(component_list)
                    r_print(f"[green]✅ Created {len(component_list)} {yaml_key} for {module_type_obj.model}[/green]")
                except Exception as e:
                    r_print(f"[bold red]❌ Error creating {yaml_key}:[/bold red] {e}")