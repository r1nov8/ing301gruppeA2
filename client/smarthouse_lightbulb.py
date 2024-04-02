import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")
        while True:
            try:
                r = requests.get(f"{common.BASE_URL}actuator/{self.did}/current")
                r.raise_for_status()
                data = r.json()

                if 'state' in data:
                    # Convert 1/0 to True/False
                    received_state = bool(data['state'])
                    # Update the ActuatorState instance
                    self.state.state = str(received_state).lower()
                    logging.info(f"Updated actuator {self.did} state to: {'On' if received_state else 'Off'}")

            except requests.RequestException as e:
                logging.error(f"Error fetching state for Actuator {self.did}: {e}")

            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)
        # TODO: END

    def run(self):

        # TODO: START

        # start thread simulating physical light bulb
        client_thread = threading.Thread(target=self.client)
        simulator_thread = threading.Thread(target=self.simulator)

        client_thread.start()
        simulator_thread.start()
        # start thread receiving state from the cloud

        # TODO: END


