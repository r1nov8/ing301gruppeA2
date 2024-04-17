import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")

        # TODO: START
        # send temperature to the cloud service with regular intervals
        while True:
            payload = self.measurement.to_json()

            try:
                response = requests.post(f"{common.BASE_URL}sensor/{self.did}/current",
                                         json=payload,  # Ensure payload is the raw JSON string if needed
                                         headers={'Content-Type': 'application/json'})
                response.raise_for_status()
                logging.info(f"Successfully sent temperature for sensor {self.did}: {payload}")
            except requests.RequestException as e:
                logging.error(f"Error sending temperature data for sensor {self.did}: {e}")

            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)


        # TODO: END

    def run(self):
        # TODO: START
        simulator_thread = threading.Thread(target=self.simulator)
        client_thread = threading.Thread(target=self.client)
        # create and start thread simulating physical temperature sensor
        simulator_thread.start()
        client_thread.start()

        # create and start thread sending temperature to the cloud service
        # simulator_thread.join()
        # client_thread.join()
        # TODO: END

