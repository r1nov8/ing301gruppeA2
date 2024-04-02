import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common


def lightbulb_cmd(state, did):
    new_state = state.get()
    logging.info(f"Dashboard: {new_state}")

    # Convert the state to a boolean True/False
    state_bool = new_state == "On"

    # Create an instance of ActuatorState with the new state
    actuator_state = ActuatorState(state_bool)

    # Convert the ActuatorState instance to a JSON string
    payload = actuator_state.to_json()

    # Corrected URL for PUT request (no '/current')
    put_url = f"{common.BASE_URL}actuator/{did}"

    # Send the PUT request with the new state to the cloud service
    try:
        response = requests.put(put_url,
                                data=payload,
                                headers={'Content-Type': 'application/json'})
        response.raise_for_status()

        # Log the successful state update
        logging.info(f"Successfully updated lightbulb {did} to {new_state}")
    except requests.RequestException as e:
        # Log any errors during the state update attempt
        logging.error(f"Error updating lightbulb {did}: {e}")


# TODO: END


def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
