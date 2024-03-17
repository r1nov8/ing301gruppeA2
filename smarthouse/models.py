from typing import List, Optional, Union
from pydantic import BaseModel, Field

class RoomModel(BaseModel):
    room_size: float
    room_name: str

class FloorModel(BaseModel):
    level: int
    rooms: List[RoomModel]

class DeviceModel(BaseModel):
    id: str
    kind: str = Field(..., description="The type of the device, such as sensor or actuator")
    supplier: str = Field(..., description="The supplier of the device")
    product: str = Field(..., description="The product name or model of the device")

class SensorModel(DeviceModel):
    unit: str = Field(..., description="The unit of measurement for the sensor")

class ActuatorModel(DeviceModel):
    state: Union[float, bool] = Field(..., description="The current state of the actuator, could be a boolean or a float value")