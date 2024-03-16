from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MeasurementModel(BaseModel):
    device: str
    ts: datetime
    value: float
    unit: str

class DeviceModel(BaseModel):
    id: str
    room: int
    kind: str
    category: str
    supplier: str
    product: str
    measurements: List[MeasurementModel] = []

class SensorModel(DeviceModel):
    unit: str

    # Assuming last_measurement() method exists in Sensor and returns a Measurement object.
    # If not, we'll need to create a method or logic to fetch the last measurement for the sensor.
    def last_measurement(self) -> MeasurementModel:
        # This method should be implemented in the domain layer (business logic)
        pass

class ActuatorModel(DeviceModel):
    state: bool

    # Assuming methods like turn_on(), turn_off() and is_active() exist in Actuator.
    # We can also add a method to return the current state of the actuator.

class ActuatorWithSensorModel(SensorModel, ActuatorModel):
    pass  # This class inherits from both SensorModel and ActuatorModel

class RoomModel(BaseModel):
    id: int
    floor: int
    area: float
    name: Optional[str] = None
    devices: List[DeviceModel] = []

class FloorModel(BaseModel):
    level: int
    rooms: List[RoomModel] = []

class SmartHouseModel(BaseModel):
    floors: List[FloorModel] = []
    # Optionally, you can add other fields like total area etc. if needed.