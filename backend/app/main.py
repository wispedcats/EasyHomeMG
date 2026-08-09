import os
import secrets

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.util.pam import authenticate_user


app = FastAPI(title="EasyHomeMG BACKEND")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


sessions = {}


class HealthResponse(BaseModel):
    status: str
    service: str


class LoginData(BaseModel):
    username: str
    password: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        service="python-api"
    )


@app.get("/temperature")
async def temperature():
    with open(
        "/sys/class/thermal/thermal_zone0/temp",
        "r"
    ) as file:
        temp = int(file.read()) / 1000

    with open(
        "/sys/class/thermal/cooling_device0/cur_state",
        "r"
    ) as file:
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


@app.post("/auth")
async def authSystemUser(
    data: LoginData,
    response: Response
):
    if not authenticate_user(
        data.username,
        data.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )

    session_id = secrets.token_urlsafe(32)

    sessions[session_id] = data.username

    response.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {
        "username": data.username,
        "authenticated": True
    }