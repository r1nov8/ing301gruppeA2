import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Actuator, Sensor, Room

# Definerer en klasse som håndterer lagring oglasting
# av SmartHouse-objektet i SQLlite-db.
class SmartHouseRepository:
    """
    Provides the functionality to persist and load a SmartHouse object in a SQLite database.
    """
    # Initialiserer klassen med filbanen til SQlite-DB.
    def __init__(self, file: str) -> None:
        self.file = file # Lagrer filbanen
        self.conn = sqlite3.connect(file) # Oppretter en forbindelse til db.
        self.setup_database() # Kaller en metode for oppretting av tabell i db

    def get_conn(self):
        return sqlite3.connect(self.file)
    
    # Setter opp db ved å oprette tabeller om den ikke eksisterer.
    def setup_database(self):
        cursor = self.conn.cursor() # Oppretter en databasepeker
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actuator_states (
                device TEXT NOT NULL,
                state TEXT NOT NULL,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(device),
                FOREIGN KEY(device) REFERENCES devices(id)
            );
        """)
        self.conn.commit() # Lagrer endringene i databasen

    # Lukker db-tilkoblingen når objektet blir slettet.
    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    # Lukker og åpner db-tilkoblingen på nytt for å sikre at vi har en frisk forbindelse.
    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)
    

    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        smarthouse = SmartHouse()
        cursor = self.conn.cursor()

        # Henter informasjon om alle rom og registrerer dem i SmartHouse-objektet
        cursor.execute("SELECT id, floor, area, name FROM rooms")
        for room_id, floor_level, area, name in cursor.fetchall():
            # Nå vil denne linjen sjekke for duplisering internt
            floor = smarthouse.register_floor(floor_level)
            room = smarthouse.register_room(floor, area, name)

        # Henter informasjon om alle enheter og registrerer dem i tilsvarende rom i SmartHouse-objektet
        cursor.execute("SELECT id, room, kind, category, supplier, product FROM devices")
        for device_id, room_id, kind, category, supplier, product in cursor.fetchall():
            room = smarthouse.get_rooms()[int(room_id)-1]  # Assuming room_id starts at 1
            if category == "actuator":
                device = Actuator(device_id, product, supplier, kind)
            elif category == "sensor":
                device = Sensor(device_id, product, supplier, kind)
            smarthouse.register_device(room, device)

        # Henter og oppdaterer tilstanden for alle aktuatorer basert på lagrede tilstander i db.
        cursor.execute("SELECT device, state FROM actuator_states")
        for device_id, state in cursor.fetchall():
            device = smarthouse.get_device_by_id(device_id)
            if device and isinstance(device, Actuator):
                if state == 'True':
                    device.turn_on()
                else:
                    device.turn_off()

        return smarthouse
    

    # Henter den siste målingen for en gitt sensor, hvis tilgjengelig.
    def get_latest_reading(self, sensor: str) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        sensor_id = sensor if isinstance(sensor, str) else sensor.id
        # Utfører en spørring for å finne den siste målingen for den gitte sensoren
        with self.get_conn() as conn:    
            cursor = conn.cursor()
            cursor.execute("SELECT ts, value, unit FROM measurements WHERE device = ? ORDER BY ts DESC LIMIT 1", (sensor_id,))
            row = cursor.fetchone()
            if row:
                return Measurement(row[0], row[1], row[2]) 
            return None
        
    # Oppdaterer tilstanden for en gitt aktuator i db.
    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        state_value = 'True' if actuator.is_active() else 'False' # Konverterer aktuator-tilstanden til en streng
        cursor = self.conn.cursor()
        # Oppdaterer eller setter inn aktuator-tilstanden i databasen
        cursor.execute("""
            INSERT INTO actuator_states (device, state) VALUES (?, ?)
            ON CONFLICT(device) DO UPDATE SET state=excluded.state, ts=CURRENT_TIMESTAMP
        """, (actuator.id, state_value))
        self.conn.commit() # Lagrer endringene
        

    def get_sensor_by_id(self, sensor_id: str) -> Optional[Sensor]:
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT kind FROM devices WHERE id = ?", (sensor_id,))
            kind = cursor.fetchone()
            if kind:
                # Assuming that 'kind' corresponds to device_type in Sensor class
                return Sensor(id=sensor_id, model_name='', supplier='', device_type=kind[0], unit='')
            return None
        
    def add_measurement(self, sensor_id: str, ts: str, value: float, unit: str):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO measurements (device, ts, value, unit) VALUES (?, ?, ?, ?)
            """, (sensor_id, ts, value, unit))
            conn.commit()
            cursor.close()
    
    def get_latest_sensor_measurements(self, sensor_id: str, limit: Optional[int] = None) -> list:
        with self.get_conn() as conn:
            cursor = conn.cursor()
            if limit is not None:
                cursor.execute("SELECT device, ts, value, unit FROM measurements WHERE device = ? ORDER BY ts DESC LIMIT ?", (sensor_id, limit))
            else:
                cursor.execute("SELECT device, ts, value, unit FROM measurements WHERE device = ? ORDER BY ts DESC", (sensor_id,))
            measurements = cursor.fetchall()
        # Convert the raw data into Measurement instances or a suitable format for the endpoint
        return [Measurement(timestamp=m[1], value=m[2], unit=m[3]) for m in measurements]
     
                           
    # statistics
    
    # Beregner gjennomsnittstemperaturen i et gitt rom for en gitt tidsperiode.
        
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        cursor = self.conn.cursor()
        
        # Bygger SQL-spørringen dynamisk basert på inngitte parametere
        query = """
        SELECT DATE(m.ts) as date, AVG(m.value) as avg_temp
        FROM measurements m
        INNER JOIN devices d ON m.device = d.id
        INNER JOIN rooms r ON d.room = r.id
        WHERE r.name = ? AND m.unit = '°C' 
        """ 
        # Add conditions for the date range if specified
        parameters = [room.room_name] # Initialiserer parameterlisten med romnavnet
        # Legger til datoområdebegrensninger i spørringen hvis spesifisert
        if from_date and until_date:
            query += "AND DATE(m.ts) >= ? AND DATE(m.ts) <= ? "
            parameters.extend([from_date, until_date])
        elif from_date:
            query += "AND DATE(m.ts) >= ? "
            parameters.append(from_date)
        elif until_date:
            query += "AND DATE(m.ts) <= ? "
            parameters.append(until_date)
        
        query += "GROUP BY DATE(m.ts)" # Grupperer resultatene etter
        
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        cursor.close()
        
        # Transform the results into the desired dictionary format
        avg_temperatures = {result[0]: result[1] for result in results}
        
        return avg_temperatures
    
    def calc_hours_with_humidity_above(self, room: Room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        cursor = self.conn.cursor()

        query = f"""
        WITH AverageHumidity AS ( 
            SELECT m.device, AVG(m.value) as avg_humidity
            FROM measurements m
            INNER JOIN devices d ON m.device = d.id
            INNER JOIN rooms r ON d.room = r.id
            WHERE r.name LIKE '{room.room_name}%' AND DATE(m.ts) = ?
            AND m.unit = '%'
            GROUP BY m.device
        )
        SELECT 
            CAST(strftime('%H', m.ts) AS INTEGER) as hour
        FROM measurements m
        INNER JOIN AverageHumidity ah ON m.device = ah.device
        WHERE DATE(m.ts) = ? AND m.unit = '%' 
        AND m.value > ah.avg_humidity
        GROUP BY hour
        HAVING COUNT(*) > 3
        """

        cursor.execute(query, (date, date))
        results = cursor.fetchall()
        cursor.close()

        # Return a list of hours where the count of measurements above the average is greater than three
        return [hour[0] for hour in results]
