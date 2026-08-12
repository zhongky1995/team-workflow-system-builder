# Workflow System Version

- System version: `0.3.0`
- Template version: `0.2.0`
- Contract/schema version: `0.6.0`
- Status: `active`
- Effective date:

## Changes

- Separate build-time specialist routing from target runtime dispatch; add complete work-item accounting, capability-state evidence, fallback, and reintegration validation.

## Compatibility

- Projects record the system and template versions they were generated from.
- Template upgrades require a migration record and must not overwrite project facts silently.
