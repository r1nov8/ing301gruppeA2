from smarthouse.domain import SmartHouse

DEMO_HOUSE = SmartHouse()

ground_floor = DEMO_HOUSE.register_floor(1)
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
living_room_kitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "Living room / Kitchen")
bathroom1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom 1")
guest_room1 = DEMO_HOUSE.register_room(ground_floor, 8, "Guest room 1")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")

second_floor = DEMO_HOUSE.register_floor(2)
office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
bathroom2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")
hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
guest_room2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest Room 2")
guest_room3 = DEMO_HOUSE.register_room(second_floor, 10, "Guest Room 3")
dressing_room = DEMO_HOUSE.register_room(second_floor, 4, "Dressing Room")
master_bedroom = DEMO_HOUSE.register_room(second_floor, 17, "Master Bedroom")
