import uvicorn
from fastapi import FastAPI, HTTPException, Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
from typing import List, Any, Dict


def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    print(db_file.absolute())
    return SmartHouseRepository(db_file.absolute())

app = FastAPI()

repo = setup_database()
router = APIRouter()

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
    floors_data = smarthouse.get_floors()
    return [
        FloorModel(
            level=floor.level,
            rooms=[
                RoomModel(
                    room_size=room.room_size, 
                    room_name=room.room_name
                ) for room in floor.rooms
            ]
        ) for floor in floors_data
    ]


@app.get("/smarthouse/floor/{fid}", response_model=FloorModel)
def get_floor_info(fid: int):
    floor = next((fl for fl in smarthouse.get_floors() if fl.level == fid), None)
    if floor is None:
        raise HTTPException(status_code=404, detail=f"Floor with id {fid} not found")
    return FloorModel(
        level=floor.level,
        rooms=[
            RoomModel(
                room_size=room.room_size, 
                room_name=room.room_name
            ) for room in floor.rooms
        ]
    )

@app.get("/smarthouse/floor/{fid}/room", response_model=List[RoomModel])
def get_rooms_on_floor(fid: int):
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    
    rooms_response = [RoomModel(room_size=room.room_size, room_name=room.room_name) for room in floor.rooms]
    return rooms_response

@app.get("/smarthouse/floor/{fid}/room/{rid}", response_model=RoomModel)
def get_specific_room(fid: int, rid: str):
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    
    room = next((r for r in floor.rooms if r.room_name == rid), None)
    if room is None:
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

    device = smarthouse.get_device_by_id(uuid)  # Retrieve the device by its ID
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Return the device information in the appropriate model
    if isinstance(device, Sensor):
        # Get the unit for the sensor kind from the SENSOR_UNITS dictionary
        unit = SENSOR_UNITS.get(device.get_device_type(), "")
        return SensorModel(
            id=device.id,
            kind=device.get_device_type(),
            supplier=device.supplier,
            product=device.model_name,
            unit=unit  # Set the unit based on the sensor kind
        )
    elif isinstance(device, Actuator):
        return ActuatorModel(
            id=device.id,
            kind=device.get_device_type(),
            supplier=device.supplier,
            product=device.model_name,
            state=device.state  # The state might be True/False or a specific float value
        )
    else:
        # If the device is neither a sensor nor an actuator, raise a 404 error
        raise HTTPException(status_code=404, detail="Device type not supported")

@app.get("/smarthouse/sensor/{uuid}/current")
def get_current_sensor_measurement(uuid: str):
    measurement = repo.get_latest_reading(uuid)
    if measurement:
        return measurement
    else:
        raise HTTPException(status_code=404, detail="Measurement not found")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)