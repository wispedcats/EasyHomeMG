# EasyHomeMG

A home server management platform with.
<!-- lines_of_code_start -->
![Lines of Code](https://img.shields.io/badge/Lines_of_Code-7553-blue)
<!-- lines_of_code_end -->


## Project Structure

- `frontend/`: Next.js + Tailwind frontend
- `backend/`: Python FastAPI backend
- `backend/node/`: Node.js backend for real-time or auxiliary API services
- `docker-compose.yaml`: local development stack with PostgreSQL
- `setup.sh`: initialize the environment and install dependencies
- `.env.example`: environment variable template
- `LANGUAGE_USAGE.md`: architecture and technology guidance

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
