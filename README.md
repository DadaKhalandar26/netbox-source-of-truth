# NetBox Source of Truth

## Enterprise Network Automation Platform

A comprehensive, production-ready NetBox Source of Truth (SoT) implementation designed to manage a globally distributed enterprise infrastructure footprint. This repository provides enterprise-style structured inventory data, automation-ready configuration, and integration tools for network automation teams.

**Purpose:** Establish a scalable, intent-driven Network Source of Truth that enables automated inventory pull, push, and data sterilization workflows while maintaining consistency across a 12-region, 59-site, 650+ device global infrastructure.

**Target Audience:** Network Engineers, DevOps Teams, Automation Engineers, Network Operations Centers (NOCs)

---

## 🌍 Global Infrastructure at a Glance

| Metric | Value |
|--------|-------|
| **Regions** | 12 (AMER, EMEA, APAC, ME/Africa) |
| **Sites** | 59 (18 Data Centers, 16 HQs, 25 Branch Offices) |
| **Physical Locations** | 250+ (DC halls, MDFs, IDFs, floors) |
| **Racks** | 264 |
| **Physical Devices** | 350+ (switches, routers, firewalls, WAPs) |
| **Virtual Machines** | 60 (across 6 vSphere clusters) |
| **VLANs** | 362 (per-site standard VIDs) |
| **IP Subnets** | 362 (per-site /24 allocations) |
| **WAN Circuits** | 73 (DIA, MPLS, Cloud Connect) |
| **Wireless SSIDs** | 159 |

---

## 📁 Project Structure

```
netbox-source-of-truth/
├── README.md                          # This file (project overview)
│
├── netbox_enterprise/                 # Static inventory & config
│   ├── README.md                      # Detailed inventory documentation
│   │
│   ├── Organisational/
│   │   ├── regions_new.csv            # 135 geographic regions
│   │   ├── 03_sites_new.csv           # 59 sites (DC/HQ/Branch)
│   │   ├── manufacturers_new.csv      # 4 manufacturers
│   │   ├── device_roles_new.csv       # 12 device roles
│   │   └── device_platforms_new.csv   # 6 OS platforms
│   │
│   ├── Physical_Infrastructure/
│   │   ├── 04_locations_new.csv       # 252 physical locations
│   │   ├── racks_new.csv              # 264 racks
│   │   ├── devices_with_rack_new.csv  # 351 network devices
│   │   └── devices_with_rack_position_new.csv  # 18 ESXi hosts
│   │
│   ├── Power_Distribution/
│   │   ├── power_panels_new.csv       # 12 power panels
│   │   ├── power_feeds_new.csv        # 48 power feeds
│   │   └── pdus_new.csv               # 24 rack PDUs
│   │
│   ├── Connectivity_Topology/
│   │   ├── cables_new.csv             # 48 fiber/copper cables
│   │   ├── portchannel_new.csv        # 72 LAG definitions
│   │   ├── providers_new.csv          # 20 ISP/carrier providers
│   │   ├── provider_accounts_new.csv  # 20 provider accounts
│   │   ├── provider_networks_new.csv  # 17 provider networks
│   │   └── circuits_new.csv           # 73 WAN circuits
│   │
│   ├── IPAM_VLAN/
│   │   ├── vlan_groups_new.csv        # 59 VLAN groups (per-site)
│   │   ├── vlans_new.csv              # 362 VLANs
│   │   ├── prefix_scoped_new.csv      # 24 regional /16 supernets
│   │   └── prefixes_with_vlan_new.csv # 362 per-site /24 prefixes
│   │
│   ├── Wireless/
│   │   ├── wlan_groups_new.csv        # 9 WLAN groups
│   │   └── wireless_lans_new.csv      # 159 SSIDs
│   │
│   ├── Virtualization/
│   │   ├── 02_clusters_new.csv        # 6 vSphere clusters
│   │   ├── 03_device_mapping_new.csv  # 18 ESXi→cluster mappings
│   │   ├── 04_virtual_machines_new.csv # 60 VMs
│   │   └── 05_vm_ip_assignment_new.csv # 60 VM IP assignments
│   │
│   ├── Config_Contexts/
│   │   ├── 02_config_context_AMER-CONFIG.json
│   │   ├── 02_config_context_EMEA-CONFIG.json
│   │   ├── 02_config_context_APAC-CONFIG.json
│   │   └── 02_config_context_ME-AFRICA-CONFIG.json
│   │
│   ├── Contacts/
│   │   └── contact_assignments_new.csv # 136 contact assignments
│   │
│   └── device_types_import_vars_new.yml # Device model definitions
│
├── integrations/                      # NetBox API integration
│   └── netbox/
│       ├── README.md                  # NetBox client documentation
│       └── client.py                  # Reusable NetBox API client
│
├── scripts/                           # Automation & utility scripts
│   └── (Planned: import, export, validation scripts)
│
├── docs/                              # Additional documentation
│   └── (Planned: NetBox API details, architecture diagrams)
│
└── LICENSE                            # Apache 2.0
```

---

## ✨ Key Features

### 1. **Enterprise-Scale Inventory**
- 59 globally distributed sites (18 DCs, 16 HQs, 25 branches)
- Hierarchical geographic structure (continent → country → state → city)
- Multi-tenant architecture with role-based scoping

### 2. **Complete Physical Topology**
- 264 racks with detailed location hierarchy
- 350+ network devices with rack positions
- Power distribution (panels, feeds, PDUs) for redundancy mapping
- 48 fiber/copper cables with end-to-end connectivity

### 3. **Standardized Naming Conventions**
- Site: `{IATA}-{LOCATION}-{TYPE}{SEQ}` (e.g., `US-NYC-HQ`)
- Device: `{SITE}-{ROLE}-{SEQ}` (e.g., `US-NYC-HQ-SPINE-01`)
- VM: `{SITE}-{FUNCTION}-{SEQ}` (e.g., `US-NYC-DC1-WEB-02`)

### 4. **Comprehensive IPAM**
- 12-region IP addressing (10.x.0.0/16 corporate, 172.x.0.0/16 guest)
- Per-site /24 allocation per function (mgmt, servers, users, voice, WiFi, IoT, guest)
- 362 VLANs with per-site VLAN groups for ID uniqueness

### 5. **Multi-Region Wireless**
- 9 WLAN groups (AMER/EMEA/APAC × Corp/Guest/IoT)
- 159 SSID configurations across HQ and branch sites
- Per-region authentication and VLAN bindings

### 6. **Virtualization Modeling**
- 6 vSphere clusters (1 per data center)
- 60 VM templates (AD, WEB, APP, DB, MGMT, LOG)
- IP assignment tracking per VM interface

### 7. **WAN Connectivity**
- 73 provider circuits (DIA, MPLS, Cloud Connect)
- 20 ISP/carrier providers with account tracking
- 17 provider networks (backbones, MPLS, cloud connectivity)

### 8. **Automation-Ready**
- CSV-based inventory imports (no manual data entry)
- Dependency-ordered import sequence
- Config contexts for regional device configuration
- Integration client for API-driven pull/push workflows

---

## 🚀 Quick Start

### Prerequisites

- NetBox 3.5+ instance with REST API enabled
- Python 3.8+ with `requests` and `pynetbox` libraries
- Git access to this repository
- NetBox API token (read/write permissions)

### 1. Clone Repository

```bash
git clone https://github.com/DadaKhalandar26/netbox-source-of-truth.git
cd netbox-source-of-truth
```

### 2. Review Directory Structure

All inventory data is located in the `netbox_enterprise/` directory. For detailed documentation:

```bash
cat netbox_enterprise/README.md
```

### 3. Understand Import Dependencies

Before importing data into NetBox, review the dependency order:

```bash
grep -A 10 "Import Order" netbox_enterprise/README.md
```

Key principle: **Parent objects must exist before child objects can reference them.**

### 4. Configure NetBox Connection

Create `.env` file in project root:

```env
NETBOX_URL=https://your-netbox-instance.com
NETBOX_API_TOKEN=your-read-write-token
NETBOX_TIMEOUT=30
```

### 5. Validate Data Integrity

```bash
# Check file structure
cd netbox_enterprise
for file in *.csv; do
  lines=$(wc -l < "$file")
  echo "$file: $lines rows"
done
```

### 6. Import into NetBox

Use NetBox UI bulk import or integration client (see `integrations/netbox/README.md`):

**Via UI:**
1. Navigate to Admin → Fixtures → Import
2. Select object type and CSV file
3. Review and confirm

**Via API (Python):**
```python
from integrations.netbox.client import NetBoxClient

# Example: Import regions
regions = NetBoxClient.get_pynetbox(api='dcim', sub_api='regions')
```

---

## 📊 Global Site Structure

### Regional Distribution

| Region | DC Count | HQ Count | Branch Count | Total | Subnet |
|--------|:--------:|:--------:|:------------:|:-----:|--------|
| **North America (US)** | 3 | 3 | 6 | 12 | 10.1.0.0/16 |
| **North America (CA/MX)** | 1 | 1 | 4 | 6 | 10.2.0.0/16 |
| **South America** | 1 | 1 | 2 | 4 | 10.3.0.0/16 |
| **Western Europe** | 2 | 2 | 4 | 8 | 10.4.0.0/16 |
| **N/E Europe** | 1 | 1 | 4 | 6 | 10.5.0.0/16 |
| **Middle East** | 1 | 1 | 2 | 4 | 10.6.0.0/16 |
| **Africa** | 1 | 1 | 1 | 3 | 10.7.0.0/16 |
| **East Asia** | 1 | 1 | 2 | 4 | 10.8.0.0/16 |
| **SE Asia** | 1 | 1 | 3 | 5 | 10.9.0.0/16 |
| **Japan/Korea** | 1 | 0 | 1 | 2 | 10.11.0.0/16 |
| **South Asia** | 1 | 1 | 1 | 3 | 10.12.0.0/16 |
| **Oceania** | 1 | 0 | 1 | 2 | 10.13.0.0/16 |
| **TOTAL** | **18** | **16** | **25** | **59** | – |

### Site Type Specifications

**Data Centers (18):**
- 8 racks per DC
- Spine-leaf fabric topology
- Redundant power distribution
- vSphere cluster (3+ ESXi hosts)
- Security (firewalls) and core routing

**Headquarters (16):**
- 6 racks per HQ
- Access layer with redundancy
- Regional hub for branch connectivity
- Desktop and server support

**Branch Offices (25):**
- 4 racks per branch
- Single uplink to HQ/DC
- Local access and wireless
- Minimal redundancy

---

## 📖 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [netbox_enterprise/README.md](netbox_enterprise/README.md) | Detailed inventory documentation, import procedures, naming conventions | Network Engineers, Automation Teams |
| [integrations/netbox/README.md](integrations/netbox/README.md) | NetBox API client usage, integration examples | DevOps, Automation Engineers |
| This file | Project overview, quick start, structure | Everyone |

---

## 🔄 Automation Workflows

### Data Pull (Read from NetBox)

Extract current inventory state for reporting, backup, or validation:

```python
from integrations.netbox.client import NetBoxClient

# Get all sites
sites = NetBoxClient.get_pynetbox(api='dcim', sub_api='sites')

# Get devices by site
devices = NetBoxClient.get_pynetbox(
    api='dcim',
    sub_api='devices',
    site='US-NYC-HQ'
)
```

### Data Push (Write to NetBox)

Update NetBox with configuration changes or bulk imports:

```python
# Update device attribute
device = nb.dcim.devices.get(name='US-NYC-HQ-SPINE-01')
device.comments = 'Updated configuration'
device.save()
```

### Data Sterilization

Validate and transform inventory data to maintain SoT intent:

```bash
# Validate CSV structure
python scripts/validate_inventory.py --source netbox_enterprise/

# Export current state
python scripts/export_inventory.py --target exports/
```

---

## 🏗️ IP Addressing Scheme

### Regional Allocation

Each region is assigned a /16 supernet for corporate traffic and a separate /16 for guest traffic:

```
Corporate VRF:  10.{rc}.0.0/16
Guest VRF:      172.{16+rc}.0.0/16
```

Where `rc` = Region Code (1-13)

### Per-Site Allocation

Within each /16, per-site /24 prefixes are allocated by function:

```
Device Mgmt (VLAN 10):    10.rc.si.0/24
VM Servers (VLAN 20):     10.rc.(si+50).0/24  [DCs/HQs only]
Users (VLAN 100):         10.rc.(si+100).0/24
VoIP (VLAN 110):          10.rc.(si+150).0/24
WiFi (VLAN 120):          10.rc.(si+170).0/24
IoT (VLAN 200):           10.rc.(si+200).0/24
Guest (VLAN 1000):        172.(16+rc).si.0/24
```

Where `si` = Site Index (0-254)

### Example: US-NYC-HQ (rc=1, si=1)

| Function | VLAN | Prefix | Purpose |
|----------|:----:|--------|---------|
| Mgmt | 10 | 10.1.1.0/24 | Device management |
| Servers | 20 | 10.1.51.0/24 | VM servers |
| Users | 100 | 10.1.101.0/24 | Workstations |
| VoIP | 110 | 10.1.151.0/24 | Telephony |
| WiFi | 120 | 10.1.171.0/24 | Wireless users |
| IoT | 200 | 10.1.201.0/24 | IoT devices |
| Guest | 1000 | 172.17.1.0/24 | Visitors |

---

## ✅ Import Order (Dependency Sequence)

Files must be imported in this order to satisfy object dependencies:

### Stage 1: Foundation Objects
1. `regions_new.csv` → Regions
2. `manufacturers_new.csv` → Manufacturers
3. `device_roles_new.csv` → Device Roles
4. `device_platforms_new.csv` → Platforms

### Stage 2: Geography & Hierarchy
5. `03_sites_new.csv` → Sites
6. `vlan_groups_new.csv` → VLAN Groups (scoped to sites)
7. `04_locations_new.csv` → Locations
8. `racks_new.csv` → Racks

### Stage 3: Connectivity
9. `providers_new.csv` → Providers
10. `provider_accounts_new.csv` → Provider Accounts
11. `provider_networks_new.csv` → Provider Networks
12. `circuits_new.csv` → Circuits

### Stage 4: IPAM
13. `vlans_new.csv` → VLANs
14. `prefix_scoped_new.csv` → Scoped Prefixes
15. `prefixes_with_vlan_new.csv` → Site Prefixes

### Stage 5: Physical Devices & Power
16. `devices_with_rack_new.csv` → Devices
17. `devices_with_rack_position_new.csv` → ESXi Hosts
18. `power_panels_new.csv` → Power Panels
19. `power_feeds_new.csv` → Power Feeds
20. `pdus_new.csv` → PDUs

### Stage 6: Topology
21. `portchannel_new.csv` → Port-channels
22. `cables_new.csv` → Cables

### Stage 7: Virtualization
23. `02_clusters_new.csv` → Clusters
24. `03_device_mapping_new.csv` → Device Mappings
25. `04_virtual_machines_new.csv` → Virtual Machines
26. `05_vm_ip_assignment_new.csv` → VM IP Assignments

### Stage 8: Wireless & Config
27. `wlan_groups_new.csv` → WLAN Groups
28. `wireless_lans_new.csv` → Wireless LANs
29. Config contexts → Import via NetBox API/UI

### Stage 9: Contacts
30. `contact_assignments_new.csv` → Contact Assignments

---

## 🔧 Integration & Extensibility

This repository is designed to be extended with automation scripts:

### Planned Components

- **Validation Scripts:** Ensure data consistency and compliance
- **Export Utilities:** Extract inventory from NetBox back to CSV
- **CI/CD Integration:** Automated testing and deployment
- **Change Detection:** Track inventory deltas over time
- **Custom Reports:** Generate capacity, utilization, compliance reports

### Contributing

To add new automation capabilities:

1. Create scripts in `scripts/` directory
2. Use `integrations/netbox/client.py` for API access
3. Update documentation in relevant README files
4. Test against NetBox instance before committing

---

## 📋 Important Notes

- **scope_id Field:** Prefix CSV files have intentionally blank `scope_id` values. After importing sites, populate these with actual NetBox site IDs via API query.

- **VLAN Scoping:** VLAN groups are scoped per site (e.g., `US-CHI-DC1-VLANS`). Standard VID ranges (10, 100, 110, etc.) repeat safely across groups.

- **Tenant Assignment:** All inventory defaults to `IT Operations` tenant. Update to match your organizational structure.

- **Custom Fields:** Ensure NetBox custom field definitions exist before importing objects that reference them.

- **Data Freshness:** This is a static dataset for bootstrap and reference. Regular exports and validation against live NetBox ensure SoT integrity.

---

## 📚 External Resources

- **NetBox Documentation:** https://docs.netbox.dev/
- **NetBox API Reference:** https://your-netbox-instance/api/docs/
- **GitHub Repository:** https://github.com/DadaKhalandar26/netbox-source-of-truth
- **Issues & Discussions:** GitHub Issues tab

---

## 📜 License

This project is licensed under the **Apache License 2.0**. See `LICENSE` file for details.

---

## 👥 Team

**Author:** Network Automation Team  
**Project Status:** Production-Ready  
**Last Updated:** 2024

---

## 🤝 Support

For questions or issues:

1. Review relevant README files in subdirectories
2. Check NetBox documentation for API-specific questions
3. Open a GitHub issue for bugs or feature requests
4. Contact the network automation team for enterprise support

---

**Ready to get started?** Begin with the [Quick Start](#-quick-start) section or dive into [netbox_enterprise/README.md](netbox_enterprise/README.md) for detailed inventory documentation.