import uvicorn
from fastapi import FastAPI, HTTPException, Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
from typing import List
from smarthouse.models import FloorModel, RoomModel, DeviceModel


def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    print(db_file.absolute())
    return SmartHouseRepository(db_file.absolute())

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

# http://localhost:8000/welcome/index.html
app.mount("/static", StaticFiles(directory="static"), name="static")


# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")


# Health Check / Hello World
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


# Starting point ...
@app.get("/hello")
def hello(name: str = "world") -> dict[str, str]:
    return {"hello": name}

@app.get("/smarthouse")
def get_smarthouse_info() -> dict[str, int | float]:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return {
        "no_rooms": len(smarthouse.get_rooms()),
        "no_floors": len(smarthouse.get_floors()),
        "registered_devices": len(smarthouse.get_devices()),
        "area": smarthouse.get_area()
    }

# TODO: implement the remaining HTTP endpoints as requested in
# https://github.com/selabhvl/ing301-projectpartC-startcode?tab=readme-ov-file#oppgavebeskrivelse
# here ...

@app.get("/smarthouse/floor")
def get_all_floors():
    floors = smarthouse.get_floors()
    return [{"level": floor.level, "rooms": [
        {"room_size": room.room_size, "room_name": room.room_name} for room in floor.rooms
    ]} for floor in floors]

@app.get("/smarthouse/floor/{fid}")
def get_floor_info(fid: int):
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    return {"level": floor.level, "rooms": [
        {"room_size": room.room_size, "room_name": room.room_name} for room in floor.rooms
    ]}

@app.get("/smarthouse/floor/{fid}/room")
def get_rooms_on_floor(fid: int):
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    return [{"room_size": room.room_size, "room_name": room.room_name} for room in floor.rooms]

@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_specific_room(fid: int, rid: str):
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    room = next((r for r in floor.rooms if r.room_name == rid), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found on this floor")

    # Include device information in the response
    devices = [{"id": device.id, "model_name": device.model_name, "supplier": device.supplier, "device_type": device.device_type} for device in room.devices]
    
    room_size_with_unit = f"{room.room_size} kvm"

    return {
        "room_size": room_size_with_unit, 
        "room_name": room.room_name,
        "devices": devices  # Add devices list to the response
    }

@app.get("/smarthouse/device")
def get_all_devices():
    """
    This endpoint returns information on all devices.
    """
    devices = smarthouse.get_devices()
    # Antar at 'devices' er en liste av Device objekter
    return [{"id": device.id, "model_name": device.model_name, "supplier": device.supplier, "device_type": device.device_type} for device in devices]

@app.get("/smarthouse/device/{uuid}")
def get_device_by_uuid(uuid: str):
    device = smarthouse.get_device_by_id(uuid)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"id": device.id, "model_name": device.model_name, "supplier": device.supplier, "device_type": device.device_type}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
