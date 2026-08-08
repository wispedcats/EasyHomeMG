from databases import Database
from sqlalchemy import MetaData, Table, Column, Integer, String, Text, JSON, TIMESTAMP, func

metadata = MetaData()

available_apps = Table(
    'available_apps',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('app_id', String, unique=True, nullable=False),
    Column('name', String, nullable=False),
    Column('description', Text, nullable=False),
    Column('category', String, nullable=False),
    Column('version', String, nullable=False),
    Column('install_command', Text, nullable=False),
    Column('uninstall_command', Text, nullable=False),
    Column('check_command', Text, nullable=False),
    Column('created_at', TIMESTAMP(timezone=True), server_default=func.now()),
)

installed_apps = Table(
    'installed_apps',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('app_id', String, nullable=False),
    Column('status', String, nullable=False),
    Column('installed_at', TIMESTAMP(timezone=True), server_default=func.now()),
    Column('updated_at', TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()),
    Column('config_json', JSON, nullable=False, default='{}'),
)

app_install_history = Table(
    'app_install_history',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('app_id', String, nullable=False),
    Column('operation', String, nullable=False),
    Column('status', String, nullable=False),
    Column('result_message', Text),
    Column('created_at', TIMESTAMP(timezone=True), server_default=func.now()),
)
