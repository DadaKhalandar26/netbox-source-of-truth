# NetBox Enterprise Static Inventory

## Overview

This directory contains enterprise-grade static inventory data designed to bootstrap and maintain a production-ready NetBox Source of Truth (SoT) implementation. The dataset simulates a real-world, globally distributed infrastructure spanning 59 sites across 12 regions, 250+ locations, 350+ physical devices, and 60 virtual machines.

**Purpose:** Establish a scalable, automation-ready inventory foundation that enables network automation teams to pull, push, and sterilize data while maintaining intent-driven infrastructure configuration across the enterprise.

**Target Audience:** Network Engineers, DevOps Teams, Automation Engineers, Network Operations Centers

---

## Features

- **Enterprise-Scale Inventory:** 59 globally distributed sites (Data Centers, HQs, Branch Offices)
- **Hierarchical Geography:** Continental → Country → State → City region structure
- **Standardized Naming Conventions:** IATA-based site codes with consistent device and interface naming
- **Multi-Tenant Architecture:** Tenant-scoped inventory with role-based access controls
- **Comprehensive IPAM:** 12-region IP scheme with per-site /24 allocation strategy
- **Power & Cabling:** Complete physical topology with PDU and cable mappings
- **Virtualization Support:** vSphere cluster definitions with 60 VM templates across 6 DCs
- **Wireless Infrastructure:** Regional WLAN groups with 159 SSID configurations
- **Circuit Inventory:** 73 provider circuits (DIA, MPLS, Cloud Connect) with provider networks
- **Configuration Contexts:** Regional DNS, NTP, SNMP, and Syslog settings for automated device configuration
- **Automation-Ready:** All data structured for scripted imports, updates, and exports

---

## Global Site Structure

The enterprise footprint is organized across **12 regions** with **59 new sites** distributed as follows:

### Regional Distribution

| Region | Site Count | Type Distribution | Subnet Range |
|--------|:----------:|---|---|
| **North America (US)** | 12 | 3 DC / 3 HQ / 6 Branch | 10.1.0.0/16 |
| **North America (CA/MX)** | 6 | 1 DC / 1 HQ / 4 Branch | 10.2.0.0/16 |
| **South America** | 4 | 1 DC / 1 HQ / 2 Branch | 10.3.0.0/16 |
| **Western Europe** | 8 | 2 DC / 2 HQ / 4 Branch | 10.4.0.0/16 |
| **N/E Europe** | 6 | 1 DC / 1 HQ / 4 Branch | 10.5.0.0/16 |
| **Middle East** | 4 | 1 DC / 1 HQ / 2 Branch | 10.6.0.0/16 |
| **Africa** | 3 | 1 DC / 1 HQ / 1 Branch | 10.7.0.0/16 |
| **East Asia** | 4 | 1 DC / 1 HQ / 2 Branch | 10.8.0.0/16 |
| **SE Asia** | 5 | 1 DC / 1 HQ / 3 Branch | 10.9.0.0/16 |
| **Japan/Korea** | 2 | 1 DC / 1 Branch | 10.11.0.0/16 |
| **South Asia** | 3 | 1 DC / 1 HQ / 1 Branch | 10.12.0.0/16 |
| **Oceania** | 2 | 1 DC / 1 Branch | 10.13.0.0/16 |
| **TOTAL** | **59** | 18 DC / 16 HQ / 25 Branch | – |

### Site Type Characteristics

**Data Centers (18 sites):**
- 8 racks per DC (multi-tiered spine-leaf fabric)
- Redundant power feeds and PDU pairs
- ESXi hypervisor clusters (vSphere)
- Core routing and security appliances

**Headquarters (16 sites):**
- 6 racks per HQ (access layer + distributed services)
- Single power feed (non-redundant)
- Regional connectivity hub
- Desktop/branch office access switches

**Branch Offices (25 sites):**
- 4 racks per branch (compact footprint)
- Single uplink to HQ/DC
- Local access switches and wireless APs
- Minimal redundancy

---

## File Manifest

### Organisational Structure

| File | Rows | Description |
|------|:----:|---|
| `regions_new.csv` | 135 | Geographic hierarchy: continents, countries, states, cities |
| `03_sites_new.csv` | 59 | Site definitions (DC/HQ/Branch) with region, group, tenant assignments |
| `manufacturers_new.csv` | 4 | Equipment manufacturers: Cisco, APC, Juniper, Palo Alto |
| `device_roles_new.csv` | 12 | Device roles: Spine, Leaf, Access, Firewall, WAP, Router, etc. |
| `device_platforms_new.csv` | 6 | OS platforms: Cisco IOS-XE, NX-OS, FTD, WLC, AP CAPWAP, SD-WAN |

### Physical Infrastructure

| File | Rows | Description |
|------|:----:|---|
| `04_locations_new.csv` | 252 | Physical locations: DC halls, MDFs, IDFs, floors scoped to sites |
| `racks_new.csv` | 264 | Rack inventory: 8/DC, 6/HQ, 4/Branch with role assignments |
| `devices_with_rack_new.csv` | 351 | Network devices (switches, routers, WAPs) with rack/position |
| `devices_with_rack_position_new.csv` | 18 | HPE ESXi hosts with U-position in DC racks |
| `device_types_import_vars_new.yml` | – | Device model definitions (Cisco/HPE/APC) for NetBox import |

### Power Distribution

| File | Rows | Description |
|------|:----:|---|
| `power_panels_new.csv` | 12 | Main power distribution panels (2 per DC × 6 DCs) |
| `power_feeds_new.csv` | 48 | Primary + redundant feeds scoped to core racks |
| `pdus_new.csv` | 24 | Rack-mounted PDUs (APC AP9572) with outlet mappings |

### Connectivity & Cabling

| File | Rows | Description |
|------|:----:|---|
| `cables_new.csv` | 48 | SMF OS2 fiber cables (leaf-to-server interconnects) |
| `portchannel_new.csv` | 72 | LAG/port-channel definitions and member interfaces |
| `providers_new.csv` | 20 | Regional ISPs and telecom carriers |
| `provider_accounts_new.csv` | 20 | Provider account IDs and reference numbers |
| `provider_networks_new.csv` | 17 | Provider backbone networks (MPLS, backbone, Cloud Connect) |
| `circuits_new.csv` | 73 | WAN circuits: DIA, MPLS, Cloud Connect with commit rates |

### IP Address Management (IPAM)

| File | Rows | Description |
|------|:----:|---|
| `vlan_groups_new.csv` | 59 | Per-site VLAN groups (ensures VID uniqueness across regions) |
| `vlans_new.csv` | 362 | VLAN definitions: Mgmt, Servers, Users, Voice, WiFi, IoT, Guest |
| `prefix_scoped_new.csv` | 24 | Regional /16 supernets (CORP-VRF, GUEST-VRF) |
| `prefixes_with_vlan_new.csv` | 362 | Per-site /24 prefixes with VLAN mappings |

### Wireless Infrastructure

| File | Rows | Description |
|------|:----:|---|
| `wlan_groups_new.csv` | 9 | WLAN groups: Regional (AMER/EMEA/APAC) × Function (Corp/Guest/IoT) |
| `wireless_lans_new.csv` | 159 | SSID configurations with authentication and VLAN bindings |

### Virtualization

| File | Rows | Description |
|------|:----:|---|
| `02_clusters_new.csv` | 6 | vSphere clusters (1 per DC): production hosts and specifications |
| `03_device_mapping_new.csv` | 18 | ESXi host-to-cluster mappings |
| `04_virtual_machines_new.csv` | 60 | VM definitions: AD, WEB, APP, DB, MGMT, LOG (10 per DC) |
| `05_vm_ip_assignment_new.csv` | 60 | Primary interface (eth0) IP assignments for all VMs |

### Configuration Contexts

| File | Description |
|------|---|
| `02_config_context_AMER-CONFIG.json` | Americas: DNS, NTP, SNMP, Syslog servers |
| `02_config_context_EMEA-CONFIG.json` | Europe/ME/Africa: Regional service endpoints |
| `02_config_context_APAC-CONFIG.json` | Asia Pacific: Regional service endpoints |
| `02_config_context_ME-AFRICA-CONFIG.json` | Middle East & Africa: Regional service endpoints |

### Contacts & Assignments

| File | Rows | Description |
|------|:----:|---|
| `contact_assignments_new.csv` | 136 | Contact assignments: Technical Lead, NOC, Facilities per site |

---

## Naming Conventions

All inventory data follows enterprise-grade standardized naming to ensure consistency and automation readiness.

### Site Naming

Format: `{IATA}-{LOCATION}-{TYPE}{SEQUENCE}`

**Examples:**
- `US-NYC-HQ` — New York Corporate HQ (IATA: NYC)
- `US-SFO-BO1` — San Francisco Branch Office 1
- `EU-AMS-DC1` — Amsterdam Data Center 1
- `AU-MEL-HQ` — Melbourne Headquarters
- `IN-MUM-DC1` — Mumbai Data Center 1

| Component | Values | Notes |
|-----------|--------|-------|
| IATA | 2-letter country code + 1-letter city ID | ISO 3166-1 alpha-2 |
| LOCATION | 3-letter IATA airport code | or custom city abbreviation |
| TYPE | `DC` / `HQ` / `BO` | Data Center, Headquarters, Branch Office |
| SEQUENCE | Numeric (1, 2, 3…) | Multiple sites in same location |

### Device Naming

Format: `{SITE}-{ROLE}-{SEQUENCE}`

**Examples:**
- `US-NYC-HQ-SPINE-01` — Spine switch
- `US-NYC-HQ-LEAF-03` — Leaf switch
- `US-NYC-HQ-FW-01` — Firewall
- `US-NYC-HQ-WAP-12` — Wireless access point
- `AU-MEL-DC1-ESX-01` — ESXi hypervisor

### Interface Naming

Standard interface naming per platform:

- **Cisco IOS-XE / NX-OS:** `Ethernet 1/1`, `GigabitEthernet 0/0/0`
- **Port-Channel / LAG:** `Port-channel 1`, `LAG members: Ethernet 1/1-4`

### Virtual Machine Naming

Format: `{SITE}-{FUNCTION}-{SEQUENCE}`

**Examples:**
- `US-NYC-DC1-AD-01` — Active Directory VM
- `US-NYC-DC1-WEB-02` — Web server
- `US-NYC-DC1-APP-05` — Application server
- `US-NYC-DC1-DB-01` — Database server
- `US-NYC-DC1-LOG-01` — Logging/syslog VM

---

## IP Addressing Scheme

### Regional Allocation

Enterprise uses a hierarchical addressing model with per-region /16 supernets subdivided into per-site /24 prefixes.

| Region Code | Region Name | Corporate /16 | Guest /16 | VRF |
|:---:|---|:---:|:---:|---|
| 1 | North America (US) | 10.1.0.0/16 | 172.17.0.0/16 | CORP-VRF |
| 2 | North America (CA/MX) | 10.2.0.0/16 | 172.18.0.0/16 | CORP-VRF |
| 3 | South America | 10.3.0.0/16 | 172.19.0.0/16 | CORP-VRF |
| 4 | Western Europe | 10.4.0.0/16 | 172.20.0.0/16 | CORP-VRF |
| 5 | N/E Europe | 10.5.0.0/16 | 172.21.0.0/16 | CORP-VRF |
| 6 | Middle East | 10.6.0.0/16 | 172.22.0.0/16 | CORP-VRF |
| 7 | Africa | 10.7.0.0/16 | 172.23.0.0/16 | CORP-VRF |
| 8 | East Asia | 10.8.0.0/16 | 172.24.0.0/16 | CORP-VRF |
| 9 | SE Asia | 10.9.0.0/16 | 172.25.0.0/16 | CORP-VRF |
| 11 | Japan/Korea | 10.11.0.0/16 | 172.27.0.0/16 | CORP-VRF |
| 12 | South Asia | 10.12.0.0/16 | 172.28.0.0/16 | CORP-VRF |
| 13 | Oceania | 10.13.0.0/16 | 172.29.0.0/16 | CORP-VRF |

### Per-Site Prefix Allocation

Each site is allocated per-function /24 prefixes based on `region_code` (rc) and `site_index` (si):

| Function | VLAN ID | Corporate Prefix | Guest Prefix | Purpose |
|:---|:---:|---|---|---|
| **Device Management** | 10 | 10.rc.si.0/24 | – | Network device mgmt interfaces |
| **VM Servers** | 20 | 10.rc.(si+50).0/24 | – | Hypervisor and VM servers (DCs/HQs) |
| **Users** | 100 | 10.rc.(si+100).0/24 | – | Workstations, desktops, laptops |
| **VoIP** | 110 | 10.rc.(si+150).0/24 | – | Telephony and voice systems |
| **WiFi Users** | 120 | 10.rc.(si+170).0/24 | – | Wireless LAN (corporate SSID) |
| **IoT** | 200 | 10.rc.(si+200).0/24 | – | IoT and embedded devices |
| **Guest** | 1000 | – | 172.(16+rc).si.0/24 | Temporary/contractor access |

### Allocation Example

**Site:** US-NYC-HQ (Region Code: 1, Site Index: 1)

- Device Mgmt (VLAN 10): **10.1.1.0/24**
- VM Servers (VLAN 20): **10.1.51.0/24**
- Users (VLAN 100): **10.1.101.0/24**
- VoIP (VLAN 110): **10.1.151.0/24**
- WiFi Users (VLAN 120): **10.1.171.0/24**
- IoT (VLAN 200): **10.1.201.0/24**
- Guest (VLAN 1000): **172.17.1.0/24**

---

## Import Dependencies & Order

CSV files must be imported into NetBox in strict dependency order. Parent objects must exist before child objects can reference them.

### Import Sequence

**Stage 1: Foundation Objects** (no dependencies)
1. `regions_new.csv` → Regions
2. `manufacturers_new.csv` → Manufacturers
3. `device_roles_new.csv` → Device Roles
4. `device_platforms_new.csv` → Platforms

**Stage 2: Hierarchy Objects** (depends on Stage 1)
5. `03_sites_new.csv` → Sites
6. `vlan_groups_new.csv` → VLAN Groups (scoped to sites)
7. `04_locations_new.csv` → Locations (scoped to sites)
8. `racks_new.csv` → Racks (scoped to locations)

**Stage 3: Connectivity Objects** (depends on providers)
9. `providers_new.csv` → Providers
10. `provider_accounts_new.csv` → Provider Accounts
11. `provider_networks_new.csv` → Provider Networks
12. `circuits_new.csv` → Circuits

**Stage 4: IPAM Objects** (depends on VLAN Groups)
13. `vlans_new.csv` → VLANs (scoped to VLAN groups)
14. `prefix_scoped_new.csv` → Scoped Prefixes (regional /16s)
15. `prefixes_with_vlan_new.csv` → Site Prefixes (scoped /24s with VLAN mappings)

**Stage 5: Physical Devices & Power** (depends on Racks)
16. `devices_with_rack_new.csv` → Devices (with rack positions)
17. `devices_with_rack_position_new.csv` → ESXi Hosts (U-position specifics)
18. `power_panels_new.csv` → Power Panels
19. `power_feeds_new.csv` → Power Feeds
20. `pdus_new.csv` → PDUs

**Stage 6: Topology Objects** (depends on Devices)
21. `portchannel_new.csv` → Port-channels
22. `cables_new.csv` → Cables

**Stage 7: Virtualization** (depends on Devices)
23. `02_clusters_new.csv` → Clusters
24. `03_device_mapping_new.csv` → Device Mappings
25. `04_virtual_machines_new.csv` → Virtual Machines
26. `05_vm_ip_assignment_new.csv` → VM IP Assignments

**Stage 8: Wireless & Config** (depends on VLANs)
27. `wlan_groups_new.csv` → WLAN Groups
28. `wireless_lans_new.csv` → Wireless LANs (scoped to VLAN)
29. `02_config_context_*-CONFIG.json` → Config Contexts (API import)

**Stage 9: Contacts** (depends on Sites)
30. `contact_assignments_new.csv` → Contact Assignments

---

## Setup & Import Instructions

### Prerequisites

- NetBox 3.5+ instance (with API enabled)
- Python 3.8+ with `requests` and `pynetbox` libraries
- Valid NetBox API token with read/write permissions
- Git access to this repository

### Step 1: Clone Repository

```bash
git clone https://github.com/DadaKhalandar26/netbox-source-of-truth.git
cd netbox-source-of-truth/netbox_enterprise
```

### Step 2: Verify Data Integrity

Before importing, validate CSV structure and content:

```bash
# Check CSV headers and row counts
for file in *.csv; do
  echo "=== $file ==="
  head -2 "$file" | cut -d, -f1-3
done

# Validate against dependency order
echo "Files ready for import (in order):"
ls -1 regions_new.csv manufacturers_new.csv device_roles_new.csv device_platforms_new.csv
```

### Step 3: Update scope_id References

The `prefix_scoped_new.csv` and `prefixes_with_vlan_new.csv` files have blank `scope_id` values. After importing sites, update these fields with site IDs:

```bash
# Query site IDs from NetBox
curl -H "Authorization: Token YOUR_TOKEN" \
  https://your-netbox-instance/api/dcim/sites/ | jq '.results[] | {name, id}'

# Update scope_id in CSV files (manual or scripted)
# scope_id should match the site's NetBox ID
```

### Step 4: Configure Environment

Create `.env` file in project root:

```env
NETBOX_URL=https://your-netbox-instance.com
NETBOX_API_TOKEN=your-read-write-token-here
NETBOX_TIMEOUT=30
```

### Step 5: Run Import Script

Execute the bulk import utility (available in `integrations/netbox/`):

```python
from integrations.netbox.client import NetBoxClient

# Example: Import regions
with open('regions_new.csv', 'r') as f:
    regions = csv.DictReader(f)
    for region in regions:
        NetBoxClient.create_region(
            name=region['name'],
            slug=region['slug'],
            parent=region['parent'] or None
        )
```

Alternatively, use NetBox UI bulk import tool:
1. Navigate to Admin → Fixtures → Import
2. Select object type (e.g., "Region")
3. Upload corresponding CSV
4. Review and confirm

### Step 6: Verify Imports

After each stage, validate data in NetBox:

```bash
# Check region count
curl -s -H "Authorization: Token TOKEN" \
  https://your-netbox/api/dcim/regions/ | jq '.count'

# Verify site hierarchy
curl -s -H "Authorization: Token TOKEN" \
  https://your-netbox/api/dcim/sites/?region=1 | jq '.results[].name'
```

---

## Data Sterilization & Automation

This inventory supports automated workflows for pulling, updating, and pushing data back to NetBox while maintaining configuration intent.

### Data Pull (Read)

Extract current NetBox state for analysis/backup:

```python
from integrations.netbox.client import NetBoxClient

# Pull all sites
sites = NetBoxClient.get_pynetbox(api='dcim', sub_api='sites')
for site in sites:
    print(f"{site.name}: {site.region.name}")

# Pull devices by site
devices = NetBoxClient.get_pynetbox(
    api='dcim',
    sub_api='devices',
    site='US-NYC-HQ'
)
```

### Data Push (Write)

Update NetBox with configuration changes:

```python
# Update device configuration (example)
device = nb.dcim.devices.get(name='US-NYC-HQ-SPINE-01')
device.custom_fields['backup_status'] = 'completed'
device.save()
```

### Data Validation

Ensure consistency between source files and NetBox:

```bash
# Compare local CSV against NetBox API
python scripts/validate_inventory.py \
  --source netbox_enterprise/03_sites_new.csv \
  --target https://netbox-url/api/dcim/sites/
```

---

## Notes & Caveats

- **Scope IDs:** The `scope_id` field in prefix files is intentionally blank. Populate with actual site IDs after site import.
- **VLAN Groups:** VLANs are scoped per site (e.g., `US-CHI-DC1-VLANS`). Standard VID ranges (10, 100, 110, etc.) repeat safely across groups.
- **Tenant Assignment:** All inventory defaults to `IT Operations` tenant. Update as needed based on your tenancy model.
- **Custom Fields:** Ensure NetBox custom field definitions exist before importing objects that reference them.
- **Automation Ready:** CSV structure is optimized for scripted imports and exports. Maintain column order during updates.

---

## Support & Documentation

For additional resources:

- **NetBox Documentation:** https://docs.netbox.dev/
- **API Reference:** https://your-netbox-instance/api/docs/
- **Project Repository:** https://github.com/DadaKhalandar26/netbox-source-of-truth
- **Integration Client:** See `integrations/netbox/README.md` for SDK usage

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2024 | 1.0 | Initial enterprise dataset with 59 sites, 350+ devices |

---

**Author:** Network Automation Team  
**Status:** Production-Ready  
**Last Updated:** 2024
