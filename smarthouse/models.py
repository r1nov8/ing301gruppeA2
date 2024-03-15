from typing import Any, List, Type
from pydantic import BaseModel
from datetime import datetime

class MeasurementModel(BaseModel):
    ts: datetime
    value: float
    unit: str

    class Config:
        from_attributes = True

class DeviceModel(BaseModel):
    id: str
    room: int
    kind: str
    category: str
    supplier: str
    product: str
    measurements: List[MeasurementModel] = []

    class Config:
        from_attributes = True

class RoomModel(BaseModel):
    level: int
    rooms: List[DeviceModel] = []

    class Config:
        from_attributes = True

class FloorModel(BaseModel):
    level: int
    rooms: List[RoomModel] = []

    class Config:
        from_attributes = True

class SmartHouseModel(BaseModel):
    floors: List[FloorModel] = []

    class Config:
        from_attributes = True

    