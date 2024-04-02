import json
import datetime


class SensorMeasurement:

    def __init__(self, init_value):
        self.timestamp = str(datetime.datetime.now().isoformat())
        self.value = init_value
        self.unit = "°C"

    def set_temperature(self, new_value):
        self.timestamp = str(datetime.datetime.now().isoformat())
        self.value = new_value

    def get_temperature(self):
        return self.value

    def to_json(self):
        sensor_measurement_encoded = json.dumps(self.__dict__)
        return sensor_measurement_encoded

    @staticmethod
    def json_decoder(json_sensor_measurement_dict):
        return SensorMeasurement(json_sensor_measurement_dict['value'])

    @staticmethod
    def from_json(json_sensor_measurement_str: str):

        json_sensor_measurement_dict = json.loads(json_sensor_measurement_str)
        actuator_state = SensorMeasurement.json_decoder(json_sensor_measurement_dict)

        return actuator_state


class ActuatorState:

    def __init__(self, init_state):
        self.state = init_state

    def to_json(self):
        actuator_state_encoded = json.dumps(self.__dict__)
        return actuator_state_encoded

    @staticmethod
    def json_decoder(json_actuator_state_dict):
        return ActuatorState(json_actuator_state_dict['state'])

    @staticmethod
    def from_json(json_actuator_state_str: str):

        json_actuator_state_dict = json.loads(json_actuator_state_str)
        actuator_state = ActuatorState.json_decoder(json_actuator_state_dict)

        return actuator_state
