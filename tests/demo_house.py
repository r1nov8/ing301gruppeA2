# In demo_house.py

from smarthouse.domain import SmartHouse

# Initialiser SmartHouse
DEMO_HOUSE = SmartHouse()

## Registrer rom
DEMO_HOUSE.register_room("Entrance", 13.5)
DEMO_HOUSE.register_room("Living room / Kitchen", 39.75)
DEMO_HOUSE.register_room("Bathroom 1", 6.3)
DEMO_HOUSE.register_room("Guest room 1", 8)
DEMO_HOUSE.register_room("Garage", 19)

DEMO_HOUSE.register_room("Office", 11.75)
DEMO_HOUSE.register_room("Bathroom 2", 9.25)
DEMO_HOUSE.register_room("Hallway", 10)
DEMO_HOUSE.register_room("Guest Room 2", 8)
DEMO_HOUSE.register_room("Guest Room 3", 10)
DEMO_HOUSE.register_room("Dressing Room", 4)
DEMO_HOUSE.register_room("Master Bedroom", 17)


# Last inn enheter fra CSV
DEMO_HOUSE.load_devices_from_csv('C:\\Python\\ing301gruppeA2\\tests\\Bookofmormons.csv')
