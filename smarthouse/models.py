from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone
from uuid import UUID

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
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="The timestamp of the measurement")

class ActuatorStateUpdateRequest(BaseModel):
    state: Union[bool, float]
    
class MeasurementModel(BaseModel):
    device: UUID = Field(..., description="The device UUID")
    value: float = Field(..., description="The measured value")
    unit: str = Field(..., description="The unit of measurement")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="The timestamp of the measurement")

    @validator('timestamp', pre=True, allow_reuse=True)
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            try:
                # Handles ISO format with 'Z' as UTC
                if v.endswith('Z'):
                    return datetime.fromisoformat(v.replace('Z', '+00:00'))
                else:
                    return datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError(f"Timestamp '{v}' is not in the expected format.")
        return v

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v.tzinfo else v.isoformat()
        }
