import uvicorn
from fastapi import FastAPI, HTTPException, Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
from typing import List
from models import FloorModel, RoomModel, DeviceModel


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

@app.get("/smarthouse/floor", response_model=List[FloorModel])
def get_all_floors():
    return smarthouse.get_floors()

@app.get("/smarthouse/floor/{fid}", response_model=FloorModel)
def get_floor_info(fid: int):
    floor = smarthouse.get_floor_by_id(fid)  # Anta at denne metoden returnerer et Floor-objekt eller None
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@app.get("/smarthouse/floor/{fid}/room", response_model=List[RoomModel])
def get_rooms_on_floor(fid: int):
    floor = smarthouse.get_floor_by_id(fid)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor.rooms

@app.get("/smarthouse/floor/{fid}/room/{rid}", response_model=RoomModel)
def get_specific_room(fid: int, rid: str):
    floor = smarthouse.get_floor_by_id(fid)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    
    room = next((room for room in floor.rooms if room.room_name == rid), None)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found on this floor")
    return room

@app.get("/smarthouse/device/", response_model=List[DeviceModel])
def get_all_device():
    devices = smarthouse.get_devices()
    return devices

@app.get("/smarthouse/device/{uuid}", response_model=DeviceModel)
def get_device_by_uuid(uuid: str):
    # Finn enheten basert på UUID (dette er en forenklet eksempel)
    device = smarthouse.get_device_by_id(uuid)  # Du må implementere denne funksjonen
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
