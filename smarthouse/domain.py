import csv

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
        return "sensor" in self.device_type.lower()

    def is_actuator(self):
        return hasattr(self, 'active')

class Sensor(Device):
    pass

class Actuator(Device):
    def init(self, device_id, supplier, model_name, target_value=None):
        super().init(device_id, supplier, model_name)
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

    def get_device_type(self):
        return "Generic Actuator"  # Endre dette til en mer spesifikk enhetstype etter behov

    def is_sensor(self):
        return False

    def is_actuator(self):
        return True

class SmartHouse:
    def __init__(self):
        self.rooms = []

    def register_room(self, room_name, area):
        self.rooms.append(Room(room_name, area))

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
        room.devices.append(device)

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

                    room = next((r for r in self.rooms if r.room_name == room_name), None)
                    if not room:
                        print(f"Room '{room_name}' not found for device '{device_id}'. Skipping...")
                        continue

                    if 'Sensor' in device_type:
                        device = Sensor(device_id, device_type, supplier, model_name)
                    elif 'Actuator' in device_type:
                        device = Actuator(device_id, device_type, supplier, model_name)
                    else:
                        device = Device(device_id, device_type, supplier, model_name)

                    self.register_device(room, device)
                    print(f"Added {device_type} to {room_name}")
        except FileNotFoundError:
            print(f"Error: File '{csv_file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
