import tkinter as tk
from tkinter import ttk

import logging
import requests

from messaging import SensorMeasurement
import common


def refresh_btn_cmd(temp_widget, did):

    logging.info("Temperature refresh")

    try:
        # Make the API call to fetch the current temperature
        r = requests.get(f"{common.BASE_URL}sensor/{did}/current")
        r.raise_for_status()  # Check for HTTP errors
        data = r.json()

        # Directly use 'value' from the response to update the sensor measurement
        # Assuming 'data' is a dictionary that contains a 'value' key with the temperature
        sensor_measurement = SensorMeasurement(init_value=str(data['value']))

        # Update the GUI with the new temperature
        temp_widget['state'] = 'normal'
        temp_widget.delete(1.0, tk.END)
        temp_widget.insert(tk.END, f"{sensor_measurement.value} °C")
        temp_widget['state'] = 'disabled'

    except requests.RequestException as e:
        logging.error(f"Error refreshing temperature: {e}")


def init_temperature_sensor(container, did):

    ts_lf = ttk.LabelFrame(container, text=f'Temperature sensor [{did}]')

    ts_lf.grid(column=0, row=1, padx=20, pady=20, sticky=tk.W)

    temp = tk.Text(ts_lf, height=1, width=10)
    temp.insert(1.0, 'None')
    temp['state'] = 'disabled'

    temp.grid(column=0, row=0, padx=20, pady=20)

    refresh_button = ttk.Button(ts_lf, text='Refresh',
                                command=lambda: refresh_btn_cmd(temp, did))

    refresh_button.grid(column=1, row=0, padx=20, pady=20)
