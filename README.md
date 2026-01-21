# Funding Service Operational Data Layer Prototype
This repository contains the source code for the Funding Service ODL (Operational Data Layer) prototype, including infra, backend code, and a UI prototype.

## Using the prototype

Refer to [prototype/README.md](./prototype/README.md) for guidance on using the prototype.

## Still to do...

- [ ] Set up local set up script that: runs docker compose; extracts data from database/seed/seed-data.zip; runs seed data on database

## Questions

- Do we need to support Cosmos/NoSQL DBs, or just relational DBs?
- What does the permission model look up?
- Should the current data be stored alongside the to-be data as part of the changeset?
- What's the max field size to be changed as part of this process? bytes, kbs, mbs? Or bigger?
- How many people need to approve a changeset?
- Does approval and deployment need to be separate steps? Or does it need to be separate to give the changeset owner the power to deploy?
- What do we do if a user tries to change a column that was removed in the meantime/before merged?

## Ideas
- show warning banner if more than one open changeset changes the same column (thanks Tom!)