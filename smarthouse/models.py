from pydantic import BaseModel
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
    measurements: Optional[List[MeasurementModel]] = None

class RoomModel(BaseModel):
    id: int
    floor: int
    area: float
    name: str
    devices: Optional[List[DeviceModel]] = None

class FloorModel(BaseModel):
    level: int
    rooms: Optional[List[RoomModel]] = None

class ActuatorStateModel(BaseModel):
    device: str
    state: bool
    ts: datetime