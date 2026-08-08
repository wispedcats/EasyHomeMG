#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "=== EasyHomeMG Setup ==="

if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
  else
    echo "ERROR: .env.example not found. Create .env manually."
    exit 1
  fi
else
  echo ".env already exists"
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is not installed. Please install Docker first."
  exit 1
fi

if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: Docker Compose is not installed. Please install Docker Compose."
  exit 1
fi

install_node() {
  echo "Installing Node.js and npm using nvm..."

  if ! command -v curl >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
      if [ "$EUID" -ne 0 ] && command -v sudo >/dev/null 2>&1; then
        SUDO=sudo
      elif [ "$EUID" -ne 0 ]; then
        echo "ERROR: Need root privileges to install curl via apt-get. Run setup.sh with sudo or install curl manually."
        return 1
      fi
      $SUDO apt-get update
      $SUDO apt-get install -y curl ca-certificates
    else
      echo "ERROR: curl is required to install nvm and is not available. Please install curl manually."
      return 1
    fi
  fi

  if [ -s "$HOME/.nvm/nvm.sh" ]; then
    # shellcheck source=/dev/null
    source "$HOME/.nvm/nvm.sh"
  else
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.6/install.sh | bash
    if [ -s "$HOME/.nvm/nvm.sh" ]; then
      # shellcheck source=/dev/null
      source "$HOME/.nvm/nvm.sh"
    else
      echo "ERROR: nvm installation failed."
      return 1
    fi
  fi

  nvm install 26
  nvm alias default 26
  nvm use 26
  return $?
}

if ! command -v npm >/dev/null 2>&1; then
  echo "npm not found. Trying to install Node.js and npm via nvm..."
  if install_node; then
    echo "Node.js and npm installed successfully via nvm."
    export NVM_DIR="$HOME/.nvm"
    # shellcheck source=/dev/null
    source "$NVM_DIR/nvm.sh"
    nvm install 26
    nvm alias default 26
    nvm use 26

    if [ -n "${ZSH_VERSION:-}" ]; then
      SHELL_RC="$HOME/.zshrc"
    else
      SHELL_RC="$HOME/.bashrc"
    fi

    if [ ! -f "$SHELL_RC" ]; then
      touch "$SHELL_RC"
    fi

    if ! grep -q 'export NVM_DIR="\$HOME/.nvm"' "$SHELL_RC" 2>/dev/null; then
      cat >> "$SHELL_RC" <<'EOF'
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
EOF
      echo "Added nvm initialization to $SHELL_RC"
    fi
  else
    echo "WARNING: Failed to install Node.js automatically. Skipping local npm install."
    echo "         Docker compose can still build and run the services without local npm."
  fi
fi

if command -v npm >/dev/null 2>&1; then
  echo "Node version: $(node -v)"
  echo "npm version: $(npm -v)"

  if [ ! -d frontend/node_modules ]; then
    echo "Installing frontend dependencies locally..."
    cd frontend
    npm install
    cd "$ROOT_DIR"
  else
    echo "Frontend dependencies already installed locally"
  fi

  if [ ! -d backend/node/node_modules ]; then
    echo "Installing backend node dependencies locally..."
    cd backend/node
    npm install
    cd "$ROOT_DIR"
  else
    echo "Backend Node.js dependencies already installed locally"
  fi
fi

if [ ! -d backend/venv ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv backend/venv
  source backend/venv/bin/activate
  pip install --upgrade pip
  pip install -r backend/requirements.txt
  deactivate
else
  echo "Python virtual environment already exists"
fi

if [ ! -f docker-compose.yaml ]; then
  echo "ERROR: docker-compose.yaml not found."
  exit 1
fi

echo "Setup completed. You can now run: docker compose up --build"
