# Enterprise NetBox Inventory Dataset
## 59 New Globally Distributed Sites

### Overview
This dataset extends an existing 21-site deployment to an 80-site enterprise
footprint across 6 global regions, ~250 locations, and ~650 devices.

---

### File Manifest

#### Organisational
| File | Rows | Description |
|------|------|-------------|
| regions_new.csv | 135 | New geographic hierarchy (continent → country → state → city) |
| 03_sites_new.csv | 59 | New sites (DC / HQ / Branch) |
| manufacturers_new.csv | 4 | Cisco, APC, Juniper, Palo Alto |
| device_roles_new.csv | 12 | All network device roles (spine, leaf, firewall, WAP …) |
| device_platforms_new.csv | 6 | Cisco IOS-XE, NX-OS, FTD, WLC, AP CAPWAP, SD-WAN |

#### Physical Infrastructure
| File | Rows | Description |
|------|------|-------------|
| 04_locations_new.csv | 252 | DC halls, MDFs, IDFs, floors – all new sites |
| racks_new.csv | 264 | Racks per site (8 DC / 6 HQ / 4 Branch) |
| devices_with_rack_new.csv | 351 | Network devices + WAPs (all new sites) |
| devices_with_rack_position_new.csv | 18 | HPE ESXi hosts (DC sites only) |
| device_types_import_vars_new.yml | – | Cisco / HPE / APC device model definitions |

#### Power
| File | Rows | Description |
|------|------|-------------|
| power_panels_new.csv | 12 | 2 power panels per DC (6 DCs) |
| power_feeds_new.csv | 48 | Primary + redundant feeds for core racks |
| pdus_new.csv | 24 | APC AP9572 rack PDUs (2 per core rack) |

#### Connectivity & Cabling
| File | Rows | Description |
|------|------|-------------|
| cables_new.csv | 48 | SMF OS2 leaf→server cables (DC sites) |
| portchannel_new.csv | 72 | LAG + member interfaces on DC leaf switches |
| providers_new.csv | 20 | Regional ISPs and carriers |
| provider_accounts_new.csv | 20 | Provider account references |
| provider_networks_new.csv | 17 | Provider backbone / MPLS networks |
| circuits_new.csv | 73 | DIA + MPLS + Cloud Connect circuits |

#### IPAM / VLAN
| File | Rows | Description |
|------|------|-------------|
| vlan_groups_new.csv | 59 | Per-site VLAN groups (ensures VID uniqueness) |
| vlans_new.csv | 362 | Mgmt, Servers, Users, Voice, WiFi, IoT, Guest |
| prefix_scoped_new.csv | 24 | Regional /16 supernets (CORP-VRF + GUEST-VRF) |
| prefixes_with_vlan_new.csv | 362 | Per-site /24 prefixes mapped to VLANs |

#### Wireless
| File | Rows | Description |
|------|------|-------------|
| wlan_groups_new.csv | 9 | Regional AMER/EMEA/APAC × Corp/Guest/IoT groups |
| wireless_lans_new.csv | 159 | CORP / GUEST / IOT SSIDs (HQ + branch sites) |

#### Virtualisation
| File | Rows | Description |
|------|------|-------------|
| 02_clusters_new.csv | 6 | vSphere clusters (one per DC) |
| 03_device_mapping_new.csv | 18 | ESXi host → cluster mappings |
| 04_virtual_machines_new.csv | 60 | AD, WEB, APP, DB, MGMT, LOG (10 per DC) |
| 05_vm_ip_assignment_new.csv | 60 | eth0 IP assignments for all VMs |

#### Config Contexts
| File | Description |
|------|-------------|
| 02_config_context_AMER-CONFIG.json | DNS/NTP/SNMP/Syslog for Americas |
| 02_config_context_EMEA-CONFIG.json | DNS/NTP/SNMP/Syslog for Europe/ME/Africa |
| 02_config_context_APAC-CONFIG.json | DNS/NTP/SNMP/Syslog for Asia Pacific |
| 02_config_context_ME-AFRICA-CONFIG.json | DNS/NTP/SNMP/Syslog for ME & Africa |

#### Contacts
| File | Rows | Description |
|------|------|-------------|
| contact_assignments_new.csv | 136 | Technical Lead + NOC + Facilities per site |

---

### IP Addressing Scheme

| Region | Sites | Corporate /16 | Guest /16 |
|--------|-------|--------------|-----------|
| North America US | rc=1 | 10.1.0.0/16 | 172.17.0.0/16 |
| North America CA/MX | rc=2 | 10.2.0.0/16 | 172.18.0.0/16 |
| South America | rc=3 | 10.3.0.0/16 | 172.19.0.0/16 |
| Western Europe | rc=4 | 10.4.0.0/16 | 172.20.0.0/16 |
| N/E Europe | rc=5 | 10.5.0.0/16 | 172.21.0.0/16 |
| Middle East | rc=6 | 10.6.0.0/16 | 172.22.0.0/16 |
| Africa | rc=7 | 10.7.0.0/16 | 172.23.0.0/16 |
| East Asia | rc=8 | 10.8.0.0/16 | 172.24.0.0/16 |
| SE Asia | rc=9 | 10.9.0.0/16 | 172.25.0.0/16 |
| Japan/Korea | rc=11 | 10.11.0.0/16 | 172.27.0.0/16 |
| South Asia | rc=12 | 10.12.0.0/16 | 172.28.0.0/16 |
| Oceania | rc=13 | 10.13.0.0/16 | 172.29.0.0/16 |

Per-site /24 allocations (site_index = si):
- Device Mgmt (VLAN 10): 10.rc.si.0/24
- VM Servers (VLAN 20): 10.rc.(si+50).0/24  [DCs and HQs only]
- Users (VLAN 100): 10.rc.(si+100).0/24
- VoIP (VLAN 110): 10.rc.(si+150).0/24
- WiFi Users (VLAN 120): 10.rc.(si+170).0/24
- IoT (VLAN 200): 10.rc.(si+200).0/24
- Guest (VLAN 1000): 172.(16+rc).si.0/24

### Import Order
Import files into NetBox in this dependency order:
1. regions → manufacturers → device_roles → device_platforms
2. sites → vlan_groups → locations → racks
3. providers → provider_accounts → provider_networks → circuits
4. vlans → prefix_scoped → prefixes_with_vlan
5. devices (with_rack, with_rack_position) → pdus → power_panels → power_feeds
6. portchannel → cables
7. cluster_types → clusters → device_mapping → virtual_machines → vm_ip_assignment
8. wlan_groups → wireless_lans
9. contact_assignments
10. config contexts (import via API or UI)

### Notes
- `scope_id` in prefix files is intentionally blank. After importing sites,
  query the NetBox API for site IDs and update these fields.
- VLAN group is scoped per site (e.g. US-CHI-DC1-VLANS) – standard VIDs
  (10, 100, etc.) repeat safely across groups.
- All new data uses tenant = 'IT Operations'. Update as required per your
  tenant structure.
