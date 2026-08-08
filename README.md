# EasyHomeMG

A home server management platform with a clean Docker-based development environment.

## Project Structure

- `frontend/`: Next.js + Tailwind frontend
- `backend/`: Python FastAPI backend
- `backend/node/`: Node.js backend for real-time or auxiliary API services
- `docker-compose.yaml`: local development stack with PostgreSQL
- `setup.sh`: initialize the environment and install dependencies
- `.env.example`: environment variable template
- `LANGUAGE_USAGE.md`: architecture and technology guidance

## What is included

- Node 26 environment for frontend and Node.js backend
- Python 3.14 environment for the FastAPI backend
- PostgreSQL database for app config and installed app metadata
- Docker Compose setup for easy local startup
- Example app install workflow for Nextcloud

## Setup

1. Make the script executable:
   ```bash
   chmod +x setup.sh
   ```
2. Run setup:
   ```bash
   ./setup.sh
   ```
3. Start the whole stack:
   ```bash
   docker compose up --build
   ```

> If `npm` is not installed locally, the project can still run inside Docker. The setup script will skip local npm installs in that case.

4. Open the frontend at:
   - `http://localhost:3000`
5. Open the Python API at:
   - `http://localhost:8000`
6. Open the Node API at:
   - `http://localhost:8001`

## Development Notes

- Edit the frontend in `frontend/`
- Edit the main backend in `backend/app/`
- Edit the Node API in `backend/node/src/`
- Use PostgreSQL on `localhost:5432`

## Database and App Installation

- `LANGUAGE_USAGE.md` contains the app installation model and Nextcloud example.
- Use PostgreSQL tables like `available_apps`, `installed_apps`, and `app_install_history`.

## Recommended Commands

- Rebuild after changes:
  ```bash
  docker compose up --build
  ```
- Remove stopped containers and volumes:
  ```bash
  docker compose down -v
  ```
- Check logs:
  ```bash
  docker compose logs -f
  ```
