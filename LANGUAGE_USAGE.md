# EasyHomeMG Technology Guidance

This document summarizes which programming languages and technologies are best suited for each part of your home server management platform.

## Python
- Best for backend services, APIs, automation, and system orchestration.
- Strong fit for server management functions, data processing, scripting, and integrations.
- Recommended use cases:
  - FastAPI or Flask web APIs
  - system monitoring and management tasks
  - scripting database migrations or automation jobs
  - handling PostgreSQL logic and backend workflows
  - storing and reading application configuration from the database
  - managing installed apps and software packages

## Node.js
- Great for building JavaScript-based backend services and real-time applications.
- Useful when you want a single language across frontend and backend.
- Recommended use cases:
  - Express or Fastify REST APIs
  - lightweight backend services for device management
  - WebSocket or real-time status dashboards
  - integration with frontend code and JSON-based APIs
  - managing app installation workflows or remote commands

## Go
- Strong choice for portable command-line tools, networking utilities, and server-side tooling.
- Go can be a good fit if you need a compiled, efficient service that is easy to deploy.
- Recommended use cases:
  - CLI tools for server management
  - small services or background workers
  - network probes and monitoring agents
  - utilities where concurrency and binary distribution matter
  - app installers, package scanning, or system audit tools

## React / Next.js
- Best for the user interface and management dashboard.
- Use Next.js for modern React apps, server-side rendering, and fast page transitions.
- Recommended use cases:
  - home server administration frontend
  - dashboard for logs, alerts, and system status
  - interactive controls and configuration pages
  - installing, enabling, and disabling apps from the UI

## Tailwind CSS
- Great for styling the frontend quickly with utility-first CSS.
- Recommended use cases:
  - fast UI design and responsive layouts
  - consistent visual styling across dashboard components
  - building maintainable and modern admin interfaces

## PostgreSQL
- Use PostgreSQL as the primary relational database for structured data.
- Recommended use cases:
  - storing users, device information, configuration profiles, and logs
  - relational data management and queries
  - transactions, data integrity, and reporting
  - storing installed apps, app metadata, and installation history
  - saving system configuration and permissions for services

## Docker
- Use Docker to isolate services and manage deployment consistently.
- Recommended use cases:
  - running Node, Python, and PostgreSQL together
  - local development environment for the full stack
  - simplifying service dependencies and startup
  - building and deploying app installer or management services

## Database and App Installation Concepts
- Store app definitions in PostgreSQL: name, version, install command, status, and description.
- Save system settings and feature flags in the database so the UI reads and writes them centrally.
- Track installed apps with a table such as `installed_apps` and a history table like `app_install_history`.
- Use Python or Node.js backend endpoints to:
  - list available apps
  - install an app
  - remove or update an app
  - check install progress and current state
- Keep app installation commands, package URLs, and system prerequisites safe in the database so the backend can run them dynamically.

## Example: Nextcloud Installation
- Add a Nextcloud entry to your app catalog in PostgreSQL.
- Example database record for Nextcloud:
  - `app_id`: `nextcloud`
  - `name`: `Nextcloud`
  - `description`: `Self-hosted file sync and collaboration platform`
  - `category`: `storage`
  - `version`: `28.0.0`
  - `status`: `available`
  - `install_command`: `docker run -d --name nextcloud -p 8080:80 nextcloud`
  - `uninstall_command`: `docker rm -f nextcloud`
  - `check_command`: `docker ps --filter name=nextcloud --format '{{.Names}}'`

- Recommended tables for app management:
  - `available_apps(id, app_id, name, description, category, version, install_command, uninstall_command, check_command, created_at)`
  - `installed_apps(id, app_id, status, installed_at, updated_at, config_json)`
  - `app_install_history(id, app_id, operation, status, result_message, created_at)`

- Nextcloud install workflow:
  1. The frontend requests `/api/apps` and displays available apps.
  2. The user clicks `Install Nextcloud`.
  3. The backend logs the install request in `app_install_history`.
  4. The backend executes the `install_command` stored in the database.
  5. On success, the backend inserts or updates `installed_apps` with `status='installed'`.
  6. The frontend polls `/api/apps/nextcloud/status` or receives a WebSocket event.

- Backend responsibilities for this flow:
  - read app metadata from PostgreSQL
  - validate system prerequisites (Docker installed, port available, disk space)
  - execute install and uninstall commands safely
  - update the app state and history tables
  - expose `/api/apps/:id/install`, `/api/apps/:id/status`, `/api/apps/:id/remove`

- Optional Node.js/real-time responsibilities:
  - stream install progress to the dashboard
  - notify the UI when the Nextcloud container is running
  - run periodic health checks for the `nextcloud` container

## Suggested Architecture
- Frontend: React / Next.js + Tailwind for the dashboard.
- Backend API: Python for the main application logic and configuration management.
- Node.js: secondary backend or real-time service for WebSocket status and app installation events.
- Go: optional CLI or utility tool for portable installers and audits.
- Database: PostgreSQL for all structured backend, configuration, and installed app data.
- Docker: containerize each service and PostgreSQL for consistent development.

## Notes
- Use each language for its strengths rather than forcing one language for everything.
- Python and Node.js are best for backend logic; C++ is best for system-level tasks; Go is best for portable utilities.
- Keep the frontend separated and use Docker Compose to connect services cleanly.
- Save app and system state in PostgreSQL so the dashboard can control installations and configuration reliably.
