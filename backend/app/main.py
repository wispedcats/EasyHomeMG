import os
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='EasyHomeMG BACKEND')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel
from databases import Database

from .apps import available_apps, installed_apps, app_install_history


DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/easyhomemg')

database = Database(DATABASE_URL)

class HealthResponse(BaseModel):
    status: str
    service: str
    database_url: str

class AppInfo(BaseModel):
    app_id: str
    name: str
    description: str
    category: str
    version: str
    status: str
    install_command: str
    uninstall_command: str
    check_command: str

class AppStatus(BaseModel):
    app_id: str
    status: str
    installed_at: Optional[str]
    updated_at: Optional[str]
    config_json: dict

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.get('/health', response_model=HealthResponse)
async def health():
    return HealthResponse(status='ok', service='python-api', database_url=DATABASE_URL)

@app.get("/temperature")
async def temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        temp = int(file.read()) / 1000

    with open("/sys/class/thermal/cooling_device0/cur_state", "r") as file:
        fan_state = int(file.read().strip())

    if fan_state > 0:
        fan = "on"
    else:
        fan = "off"

    return {
        "temperature": temp,
        "fan_state": fan_state,
        "fan": fan
    }
@app.get('/apps', response_model=List[AppInfo])
async def list_apps():
    query = available_apps.select()
    rows = await database.fetch_all(query)
    return [AppInfo(**row) for row in rows]

@app.get('/apps/{app_id}/status', response_model=AppStatus)
async def app_status(app_id: str):
    query = installed_apps.select().where(installed_apps.c.app_id == app_id)
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(status_code=404, detail='App not installed')
    return AppStatus(**row)

@app.post('/apps/{app_id}/install')
async def install_app(app_id: str):
    app_query = available_apps.select().where(available_apps.c.app_id == app_id)
    app_data = await database.fetch_one(app_query)
    if not app_data:
        raise HTTPException(status_code=404, detail='App not found')

    await database.execute(
        app_install_history.insert().values(
            app_id=app_id,
            operation='install',
            status='pending',
            result_message='Installation started',
        )
    )

    await database.execute(
        installed_apps.insert().values(
            app_id=app_id,
            status='installing',
            config_json={},
        )
    )

    # Installation execution can be added here using subprocess or task queue.

    await database.execute(
        installed_apps.update()
        .where(installed_apps.c.app_id == app_id)
        .values(status='installed')
    )

    await database.execute(
        app_install_history.insert().values(
            app_id=app_id,
            operation='install',
            status='success',
            result_message='Installation recorded',
        )
    )

    return {'status': 'install started', 'app_id': app_id}

@app.post('/apps/{app_id}/remove')
async def remove_app(app_id: str):
    app_query = available_apps.select().where(available_apps.c.app_id == app_id)
    app_data = await database.fetch_one(app_query)
    if not app_data:
        raise HTTPException(status_code=404, detail='App not found')

    await database.execute(
        app_install_history.insert().values(
            app_id=app_id,
            operation='remove',
            status='pending',
            result_message='Removal started',
        )
    )

    await database.execute(
        installed_apps.delete().where(installed_apps.c.app_id == app_id)
    )

    await database.execute(
        app_install_history.insert().values(
            app_id=app_id,
            operation='remove',
            status='success',
            result_message='Removal recorded',
        )
    )

    return {'status': 'remove started', 'app_id': app_id}
