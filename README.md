Automated Marketing Collateral Migration (Box → Google Drive)

Overview

This repository provides a production-ready, automated pipeline to migrate large volumes of marketing collateral (images, videos, brochures, PDFs, etc.) from Box.com to Google Drive while preserving folder hierarchy and granular access controls. It also adds automatic visual and textual tagging using Google Cloud Vision and Video Intelligence, a continuous real-time tagging microservice for new uploads, an advanced search API/UI for creatives, and scheduled audit scripts for ongoing health checks.

Key Capabilities

- End-to-end migration from Box to Google Drive
- Exact hierarchy mirroring and permission mapping (users and groups)
- Resumable, parallelized large file transfer with retry/recovery
- Auto-tagging via GCP Vision (images, PDFs) and Video Intelligence (videos)
- Continuous tagging microservice for new uploads to Drive
- Search API and minimal UI layered on Drive metadata and custom tags
- Scheduled audits for tagging completeness and pipeline health
- Dockerized services with a clear, configurable deployment

High-Level Workflow

1) Migrate: Traverse Box enterprise folders recursively, create mirrored Drive folders, copy files using resumable uploads, and map permissions based on a configurable identity map.
2) Tag: For each migrated asset, run Vision/Video Intelligence to extract labels, logos, text (OCR), people/activity cues, and campaign keywords (configurable). Store tags in Drive `appProperties` and descriptions.
3) Continuously Tag: A microservice monitors Drive changes for new files and auto-tags them in real-time.
4) Search: A FastAPI service exposes human-friendly search over tags, visual elements, and campaign metadata, with a minimal web UI for creative teams.
5) Audit: A scheduled job validates tagging completeness, permission health, and service liveness, notifying admins if anything degrades.

Architecture (text diagram)

Box SDK → Migration Orchestrator → Google Drive API (folders/files/permissions)
                                     ↘
                                      Tagging Engine → Vision API / Video Intelligence API
                                                        ↘
                                                         Drive file appProperties + description

Drive Changes API → Tagging Microservice → Tagging Engine (idempotent)

Search API/UI → Google Drive API (query by appProperties/mime/owners/labels)

Audit Scripts → Google Drive API + service health checks → notifications

Prerequisites

- Box JWT App credentials (enterprise app) or OAuth2 app with sufficient scopes
- Google Cloud project with enabled APIs: Drive API, Vision API, Video Intelligence API
- Service Account with domain-wide delegation to your Google Workspace (for Drive)
- A mapping file for Box identities (users/groups) to Google identities
- Docker and docker-compose (recommended)

Configuration

Copy `.env.example` to `.env` and update values. Edit `app/config/mappings.yaml` to define identity mappings and campaign keywords. See inline comments.

Services

- Migrator (one-off): Runs the Box → Drive migration preserving structure and permissions
- Tagging Microservice (long-running): Listens for new Drive files and tags them
- Search API/UI (service): Exposes REST and minimal UI for discovery
- Audit (cron or ad-hoc): Validates completeness and health

Quick Start (Docker)

1. Fill in `.env` and `app/config/mappings.yaml`.
2. Build images: `docker-compose build`
3. Run search and tagging services: `docker-compose up -d search tagging`
4. Run the migrator (one-time): `docker-compose run --rm migrator python -m app.migration.migrate`
5. Run audits on demand: `docker-compose run --rm audit python -m app.audits.audit_tagging`

Local Development

- Python 3.11+
- `pip install -r requirements.txt`
- Export environment variables from `.env`
- Run: `python -m app.migration.migrate` (migration), `uvicorn app.search.api:app --reload` (search), `uvicorn app.tagging.microservice:app --reload` (tagging)

Search Usage Examples

- GET `/search?q=logo:Nike AND campaign:BackToSchool`
- GET `/search?labels=people,product&mime=image/&text=summer catalog`

Operational Notes

- Resumable uploads and exponential backoff are implemented for robustness.
- Idempotency keys ensure tagging and permission operations are safe to re-run.
- Permissions are mapped via `mappings.yaml`; unmapped identities can be defaulted or skipped per config.
- AppProperties are used for tags and campaign metadata to enable efficient Drive queries.

Security

- Secrets are read from environment variables and not stored in the repo.
- Service Account keys should be mounted via secret stores or Docker secrets in production.

License

Proprietary. Company-internal use only unless otherwise specified.


