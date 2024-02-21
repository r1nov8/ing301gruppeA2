import csv
import random
from datetime import datetime


class Measurement:
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit


class Room:
    def __init__(self, room_name, area):
        self.room_name = room_name
        self.area = area
        self.devices = []


class Device:
    def __init__(self, id, device_type, supplier, model_name):
        self.id = id
        self.device_type = device_type
        self.supplier = supplier
        self.model_name = model_name
        self.room = None

    def is_sensor(self):
        return isinstance(self, Sensor)

    def is_actuator(self):
        return isinstance(self, Actuator)


class Sensor(Device):
    def last_measurement(self):
        # Returner en Measurement-instans i stedet for en ordbok
        value = random.uniform(20.0, 30.0)
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, '°C')


class Actuator(Device):
    def __init__(self, id, device_type, supplier, model_name):
        super().__init__(id, device_type, supplier, model_name)
        self.active = False
        self.extra_info = None

    def turn_on(self, extra_info=None):
        self.active = True
        self.extra_info = extra_info

    def turn_off(self):
        self.active = False
        self.extra_info = None

    def is_active(self):
        return self.active


class SmartHouse:
    def __init__(self):
        self.rooms = []

    def register_room(self, room_name, area):
        room = Room(room_name, area)
        self.rooms.append(room)

    def get_rooms(self):
        return self.rooms

    def get_area(self):
        return sum(room.area for room in self.rooms)

    def get_devices(self):
        return [device for room in self.rooms for device in room.devices]

    def get_device_by_id(self, id):
        for room in self.rooms:
            for device in room.devices:
                if device.id == id:
                    return device
        return None

    def register_device(self, room, device):
        # Fjern enheten fra det gamle rommet hvis den allerede er registrert et sted
        if device.room:
            device.room.devices.remove(device)
        # Legg til enheten i det nye rommet
        room.devices.append(device)
        # Oppdater enhetens romreferanse
        device.room = room

    def move_device_to_room(self, device_id, new_room_name):
        device = self.get_device_by_id(device_id)
        if device:
            # Fjern enheten fra det gamle rommet
            if device.room:
                device.room.devices.remove(device)
            # Finn det nye rommet
            new_room = next((room for room in self.rooms if room.room_name == new_room_name), None)
            if new_room:
                # Legg enheten til i det nye rommet og oppdater enhetens romreferanse
                new_room.devices.append(device)
                device.room = new_room
#5
    def load_devices_from_csv(self, csv_file_path):
        print("Attempting to load devices from CSV...")
        try:
            with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
                print("CSV file opened successfully.")
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    device_id = row['Identifikator']
                    device_type = row['Enhet']
                    supplier = row['Produsent']
                    model_name = row['Modellnavn']
                    room_name = row['Room']
                    device_category = row['DeviceCategory']

                    # Finn rommet basert på navnet
                    room = next((r for r in self.rooms if r.room_name == room_name), None)
                    if not room:
                        print(f"Room '{room_name}' not found for device '{device_id}'. Skipping...")
                        continue

                    # Opprett enheten basert på DeviceCategory
                    if device_category == 'Sensor':
                        device = Sensor(device_id, device_type, supplier, model_name)
                    elif device_category == 'Actuator':
                        device = Actuator(device_id, device_type, supplier, model_name)
                    else:
                        print(f"Unknown device category '{device_category}' for device '{device_id}'. Skipping...")
                        continue

                    # Legg enheten til i det tilsvarende rommet
                    room.devices.append(device)
                    device.room = room  # Sett enhetens romreferanse
                    print(f"Added {device_type} ({device_category}) to {room_name}")
        except FileNotFoundError:
            print(f"Error: File '{csv_file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
