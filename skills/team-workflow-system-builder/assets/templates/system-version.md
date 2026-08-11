# Workflow System Version

- System version: `0.2.0`
- Template version: `0.2.0`
- Contract/schema version: `0.5.0`
- Status: `active`
- Effective date:

## Changes

- Separate approval requirement from approval result, add safe runtime configuration, and tighten validation.

## Compatibility

- Projects record the system and template versions they were generated from.
- Template upgrades require a migration record and must not overwrite project facts silently.
