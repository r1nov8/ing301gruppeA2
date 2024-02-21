import random
from datetime import datetime

class Measurement:
    """This class represents a measurement taken from a sensor."""
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

class SmartHouse:
    def __init__(self):
        self.floors = {}
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    It provides functionality to register rooms and floors (i.e., changing the house's physical layout)
    as well as register and modify smart devices and their state.
    """
    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        if level not in self.floors:
            self.floors[level] = Floor(level)
        return self.floors[level]

    def register_room(self, floor_level, room_size, room_name=None):
        """
        This method registers a new room with the given room area size
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        if floor_level not in self.floors:
            raise ValueError(f"Floor {floor_level} not registered.")
        floor = self.floors[floor_level]
        return floor.add_room(Room(room_size, room_name))

    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g., if the house has
        registered a basement (level=0), a ground floor (level=1) and a first floor (level=2),
        then the resulting list contains these floors in the above order.
        """
        return [floor for level, floor in sorted(self.floors.items())]

    def get_rooms(self):
        """
        This method returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        return [room for floor in self.floors.values() for room in floor.get_rooms()]

    def get_area(self):
        """
        This method returns the total area size of the house, i.e., the sum of the area sizes of each room in the house.
        """
        return sum(room.room_size for room in self.get_rooms())

    def register_device(self, room_name, device):
        """
        This method registers a given device in a given room.
        """
        for floor in self.floors.values():
            for room in floor.get_rooms():
                if room.room_name == room_name:
                    room.add_device(device)
                    return
        raise ValueError(f"Room {room_name} not found.")

    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        for room in self.get_rooms():
            device = room.get_device(device_id)
            if device:
                return device
        return None

class Floor:
    def __init__(self, level):
        self.level = level
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)
        return room

    def get_rooms(self):
        return self.rooms

class Room:
    def __init__(self, room_size, room_name=None):
        self.room_size = room_size
        self.room_name = room_name
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def get_device(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None

class Device:
    def __init__(self, device_id, supplier, model_name):
        self.device_id = device_id
        self.supplier = supplier
        self.model_name = model_name

    def is_actuator(self):
        return hasattr(self, 'perform_action')

    def is_sensor(self):
        return hasattr(self, 'read_data')

    def get_device_type(self):
        return self.__class__.__name__

class Sensor(Device):
    def read_data(self):
        return Measurement(datetime.now().isoformat(), random.random(), self.unit)

    def last_measurement(self):
        return self.read_data()

class Actuator(Device):
    def __init__(self, device_id, supplier, model_name, target_value=None):
        super().__init__(device_id, supplier, model_name)
        self.target_value = target_value
        self.active = False

    def turn_on(self):
        self.active = True

    def turn_off(self):
        self.active = False

    def is_active(self):
        return self.active

    def set_target_value(self, value):
        self.target_value = value
