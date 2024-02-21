import csv
import random
from datetime import datetime

csv_file_path = '/Users/kingston/Desktop/ING301/ing301public/ing301gruppeA2/tests/Bookofmormons (1).csv'

class Measurement:
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

class Device:
    def __init__(self, device_id, supplier, model_name):
        self.device_id = device_id
        self.supplier = supplier
        self.model_name = model_name

    def is_sensor(self):
        return isinstance(self, Sensor)

    def is_actuator(self):
        return isinstance(self, Actuator)

class Sensor(Device):
    def last_measurement(self):
        return Measurement(datetime.now().isoformat(), random.uniform(20.0, 30.0), "°C")

class Actuator(Device):
    def __init__(self, device_id, supplier, model_name, target_value=None):
        super().__init__(device_id, supplier, model_name)
        self.target_value = target_value
        self.active = False

    def turn_on(self, target_value=None):
        self.active = True
        if target_value is not None:
            self.target_value = target_value

    def turn_off(self):
        self.active = False

    def is_active(self):
        return self.active

class Room:
    def __init__(self, room_size, room_name=None):
        self.room_size = room_size
        self.room_name = room_name
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)
        device.room = self

    def get_device(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None

class Floor:
    def __init__(self, level):
        self.level = level
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)
    def get_rooms(self):
        return self.rooms

class SmartHouse:
    def __init__(self):
        self.floors = {}

    def register_floor(self, level):
        floor = Floor(level)
        self.floors[level] = floor
        return floor

    def register_room(self, floor_level, room_size, room_name=None):
        if floor_level not in self.floors:
            raise ValueError(f"Floor {floor_level} not registered.")
        room = Room(room_size, room_name)
        self.floors[floor_level].add_room(room)
        return room

    def get_rooms(self):
        rooms = []
        for floor in self.floors.values():
            rooms.extend(floor.get_rooms())
        return rooms

    def get_area(self):
        return sum(room.room_size for room in self.get_rooms())

    def get_device(self, device_id):
        for room in self.get_rooms():
            device = room.get_device(device_id)
            if device:
                return device

    def get_devices(self):
        devices = []
        for room in self.get_rooms():
            devices.extend(room.devices)
        return devices
    
    def get_device_by_id(self, device_id):
        for device in self.get_devices():
            if device.device_id == device_id:
                return device
        return None  # If the device isn't found, return None   

class SmartHouse:
    def __init__(self):
        self.floors = {}

    def register_floor(self, level):
        floor = Floor(level)
        self.floors[level] = floor
        return floor

    def register_room(self, floor_level, room_size, room_name=None):
        if floor_level not in self.floors:
            raise ValueError(f"Floor {floor_level} not registered.")
        room = Room(room_size, room_name)
        self.floors[floor_level].add_room(room)
        return room

    def get_rooms(self):
        rooms = []
        for floor in self.floors.values():
            rooms.extend(floor.get_rooms())
        return rooms

    def get_area(self):
        return sum(room.room_size for room in self.get_rooms())

    def get_device(self, device_id):
        for room in self.get_rooms():
            device = room.get_device(device_id)
            if device:
                return device

    def get_devices(self):
        devices = []
        for room in self.get_rooms():
            devices.extend(room.devices)
        return devices
    
    def get_device_by_id(self, device_id):
        for floor in self.floors.values():
            for room in floor.get_rooms():
                for device in room.devices:
                    if device.device_id == device_id:
                        return device
        return None  # If the device isn't found, return None

    def load_devices_from_csv(self, csv_file_path):
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            # Assuming delimiter is semicolon based on the provided CSV format
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                device_id = row['Identifikator']
                device_type = row['Enhet']
                supplier = row['Produsent']
                model_name = row['Modellnavn']
                room_name = row['Room']

                room = next((r for r in self.get_rooms() if r.room_name == room_name), None)
                if not room:
                    print(f"Room '{room_name}' not found for device '{device_id}'. Skipping...")
                    continue

                if 'Sensor' in device_type:
                    device = Sensor(device_id, supplier, model_name)
                elif 'Actuator' in device_type:
                    device = Actuator(device_id, supplier, model_name)
                else:
                    print(f"Unknown device type '{device_type}' for device '{device_id}'. Skipping...")
                    continue

                room.add_device(device)
                print(f"Added {device_type} to {room_name}")
# Create a SmartHouse instance
DEMO_HOUSE = SmartHouse()

# Assuming you have already registered floors and rooms...

# Load devices from CSV
  # Replace with the actual path to your CSV file
DEMO_HOUSE.load_devices_from_csv(csv_file_path)

# For testing purposes, print the total number of devices
print(f"Total number of devices registered: {len(DEMO_HOUSE.get_devices())}")

if __name__ == "__main__":
    # Run some tests if necessary
    pass