from smarthouse.domain import SmartHouse, Sensor, Actuator
import csv

# Initialiser SmartHouse
DEMO_HOUSE = SmartHouse()

# Registrer etasjer og rom
DEMO_HOUSE.register_floor(1)
DEMO_HOUSE.register_room(1, 13.5, "Entrance")
DEMO_HOUSE.register_room(1, 39.75, "Living room / Kitchen")
DEMO_HOUSE.register_room(1, 6.3, "Bathroom 1")
DEMO_HOUSE.register_room(1, 8, "Guest room 1")
DEMO_HOUSE.register_room(1, 19, "Garage")

DEMO_HOUSE.register_floor(2)
DEMO_HOUSE.register_room(2, 11.75, "Office")
DEMO_HOUSE.register_room(2, 9.25, "Bathroom 2")
DEMO_HOUSE.register_room(2, 10, "Hallway")
DEMO_HOUSE.register_room(2, 8, "Guest Room 2")
DEMO_HOUSE.register_room(2, 10, "Guest Room 3")
DEMO_HOUSE.register_room(2, 4, "Dressing Room")
DEMO_HOUSE.register_room(2, 17, "Master Bedroom")
