import tkinter as tk # https://www.pythontutorial.net/tkinter/

import logging

from dashboard_lightbulb import init_lightbulb
from dashboard_temperaturesensor import init_temperature_sensor

import common

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

root = tk.Tk()
root.geometry('450x300')
root.title('ING301 SmartHouse Dashboard')

init_lightbulb(root, common.LIGHTBULB_DID)
init_temperature_sensor(root, common.TEMPERATURE_SENSOR_DID)

root.mainloop()
