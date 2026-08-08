-- EasyHomeMG database schema

CREATE TABLE IF NOT EXISTS available_apps (
  id SERIAL PRIMARY KEY,
  app_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  category TEXT NOT NULL,
  version TEXT NOT NULL,
  install_command TEXT NOT NULL,
  uninstall_command TEXT NOT NULL,
  check_command TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS installed_apps (
  id SERIAL PRIMARY KEY,
  app_id TEXT NOT NULL,
  status TEXT NOT NULL,
  installed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  config_json JSONB DEFAULT '{}'::jsonb,
  FOREIGN KEY (app_id) REFERENCES available_apps(app_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS app_install_history (
  id SERIAL PRIMARY KEY,
  app_id TEXT NOT NULL,
  operation TEXT NOT NULL,
  status TEXT NOT NULL,
  result_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  FOREIGN KEY (app_id) REFERENCES available_apps(app_id) ON DELETE CASCADE
);
