project/
│
├── main.py
├── requirements.txt
├── README.md
├── .env
│
├── configs/
│   ├── app_config.yml
│   ├── logging.yml
│   └── standards.yml
│
├── integrations/
│   │
│   ├── netbox/
│   │   ├── client.py
│   │   ├── devices.py
│   │   ├── sites.py
│   │   ├── locations.py
│   │   ├── racks.py
│   │   ├── interfaces.py
│   │   ├── ipam.py
│   │   ├── prefixes.py
│   │   ├── vlans.py
│   │   ├── tenants.py
│   │   ├── tags.py
│   │   ├── cables.py
│   │   └── custom_fields.py
│   │
│   ├── csv/
│   │   ├── csv_reader.py
│   │   └── csv_writer.py
│   │
│   ├── excel/
│   │   ├── excel_reader.py
│   │   └── excel_writer.py
│   │
│   ├── yaml/
│   │   ├── yaml_reader.py
│   │   └── yaml_writer.py
│   │
│   └── exporters/
│       ├── json_exporter.py
│       ├── csv_exporter.py
│       └── excel_exporter.py
│
├── services/
│   │
│   ├── inventory/
│   │   ├── device_inventory.py
│   │   ├── ip_inventory.py
│   │   ├── vlan_inventory.py
│   │   └── rack_inventory.py
│   │
│   ├── onboarding/
│   │   ├── device_onboarding.py
│   │   ├── site_onboarding.py
│   │   ├── vlan_onboarding.py
│   │   └── rack_onboarding.py
│   │
│   ├── validation/
│   │   ├── naming_validation.py
│   │   ├── ip_validation.py
│   │   ├── vlan_validation.py
│   │   ├── duplicate_validation.py
│   │   └── standards_validation.py
│   │
│   ├── synchronization/
│   │   ├── inventory_sync.py
│   │   ├── drift_detection.py
│   │   └── reconciliation.py
│   │
│   ├── transformations/
│   │   ├── normalize_devices.py
│   │   ├── normalize_sites.py
│   │   └── normalize_ips.py
│   │
│   ├── reporting/
│   │   ├── audit_reports.py
│   │   ├── compliance_reports.py
│   │   ├── utilization_reports.py
│   │   └── inventory_reports.py
│   │
│   ├── compliance/
│   │   ├── compliance_engine.py
│   │   └── standards_checker.py
│   │
│   └── cleanup/
│       ├── stale_objects.py
│       ├── orphan_cleanup.py
│       └── duplicate_cleanup.py
│
├── schemas/
│   ├── device_schema.py
│   ├── site_schema.py
│   ├── vlan_schema.py
│   ├── prefix_schema.py
│   └── interface_schema.py
│
├── models/
│   ├── device_model.py
│   ├── site_model.py
│   └── vlan_model.py
│
├── templates/
│   ├── reports/
│   └── onboarding/
│
├── exports/
│
├── logs/
│
└── tests/
    ├── test_integrations/
    ├── test_services/
    └── test_validations/