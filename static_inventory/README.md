# Static Inventory

This directory contains CSV-based static inventory data used for the initial population and bootstrap of the NetBox Source of Truth environment.

## Purpose

The CSV files in this directory are used to:

- Populate NetBox objects
- Establish enterprise inventory hierarchy
- Maintain standardized naming conventions
- Simulate production-style infrastructure data
- Support automation-ready inventory modeling

## Inventory Domains

### Tenancy
- Tenant Groups
- Tenants

### Regions
- Continents
- Countries
- States
- Cities

### Devices
- Manufacturers
- Platforms
- Device Roles
- Device Types

### IPAM
- VRFs
- VLANs
- Prefixes
- IP Addresses

### Topology
- Racks
- Interfaces
- Cables

## Notes

- All inventory data follows strict naming conventions.
- Slugs are lowercase and hyphen-separated.
- CSV files are intended for bootstrap/import workflows.
- Inventory structure is designed for scalability and automation readiness.