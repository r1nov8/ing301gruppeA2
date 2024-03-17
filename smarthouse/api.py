import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
from typing import List, Optional
from smarthouse.models import FloorModel, RoomModel, DeviceModel, SensorModel, ActuatorModel
from smarthouse.domain import Sensor, Actuator

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

    return RoomModel(room_size=room.room_size, room_name=room.room_name)

@router.get("/smarthouse/device", response_model=List[DeviceModel])
def get_all_devices():
    devices = smarthouse.get_devices()  # Assuming this retrieves all devices correctly
    response = []
    for device in devices:
        # Now build your response based on the type of device
        if isinstance(device, Sensor):
            response.append(SensorModel(
                id=device.id,
                kind=device.device_type,  # Assuming direct access to attribute
                supplier=device.supplier,
                product=device.model_name,
                unit=device.unit
            ))
        elif isinstance(device, Actuator):
            response.append(ActuatorModel(
                id=device.id,
                kind=device.device_type,
                supplier=device.supplier,
                product=device.model_name,
                state=device.state
            ))
        else:
            response.append(DeviceModel(
                id=device.id,
                kind=device.device_type,
                supplier=device.supplier,
                product=device.model_name
            ))
    return response
'''
@app.get("/smarthouse/device/{uuid}")
def get_device_by_uuid(uuid: str):
    device = smarthouse.get_device_by_id(uuid)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"id": device.id, "model_name": device.model_name, "supplier": device.supplier, "device_type": device.device_type}

@app.get("/smarthouse/device/{uuid}", response_model=DeviceModel)
def get_device_by_uuid(uuid: str):
    device = smarthouse.get_device_by_id(uuid)  # Assuming this method is correctly implemented
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return DeviceModel(
        id=device.id,
        device_type=device.device_type,  # Adjusted to device_type
        supplier=device.supplier
    )

@app.get("/smarthouse/sensor/{uuid}/current", response_model=MeasurementModel)
def get_current_sensor_measurement(uuid: str):
    # Fetch the latest sensor measurement using the provided UUID
    measurement = repo.get_latest_reading(sensor=uuid)
    if not measurement:
        raise HTTPException(status_code=404, detail="No measurement found for this sensor")

    # Note: Adjusted to match the actual attributes of the Measurement class
    return MeasurementModel(
        device=uuid,  # Assuming you want to return the sensor UUID as the device identifier
        ts=measurement.timestamp,  # Corrected attribute name
        value=measurement.value,
        unit=measurement.unit
    )

@app.post("/smarthouse/sensor/{uuid}/current")
def add_measurement_for_sensor(uuid: UUID, measurement: MeasurementModel):
    try:
        repo.add_measurement(sensor_id=str(uuid), value=measurement.value, unit=measurement.unit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Measurement added successfully."}

@app.get("/smarthouse/sensor/{uuid}/values", response_model=List[MeasurementModel])
def get_latest_measurements_for_sensor(uuid: UUID, limit: Optional[int] = None):
    try:
        measurements = repo.get_latest_measurements(sensor_id=str(uuid), limit=limit)
        return measurements
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/smarthouse/sensor/{uuid}/oldest")
def delete_oldest_measurement_for_sensor(uuid: UUID):
    try:
        repo.delete_oldest_measurement(sensor_id=str(uuid))
        return {"message": "Oldest measurement deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/smarthouse/actuator/{uuid}/current")
def get_current_state_for_actuator(uuid: UUID):
    state = repo.get_current_state(actuator_id=str(uuid))
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")
    return {"state": state}

@app.put("/smarthouse/device/{uuid}")
def update_current_state_for_actuator(uuid: UUID, state: bool):
    try:
        repo.update_actuator_state(actuator_id=str(uuid), state=state)
        return {"message": "Actuator state updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)