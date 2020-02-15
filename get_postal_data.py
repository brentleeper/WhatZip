import psycopg2
from db_config import *
from psycopg2.extras import RealDictCursor


class PostalDataDAO:
    def __init__(self, conn=None):
        try:
            if conn:
                self.conn = conn
            else:
                self.conn = psycopg2.connect(**connection_parameters)
        except:
            self.conn = None

    def get_data_from_coordinate(self, lat, lon):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(zip_coordinate_query, {'lat': lat, 'lon': lon})
        return cursor.fetchall()

    def get_data_from_radius(self, lat, lon, radius_miles):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(zip_radius_query, {'lat': lat, 'lon': lon, 'radius_miles': int(round(float(radius_miles)))})
        return cursor.fetchall()

    def get_data_from_zipcode(self, zipcode):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(zip_zipcode_query, {'zipcode': zipcode})
        return cursor.fetchall()

    def validate_coordinates(self, lat, lon):
        return ((-90 <= lat <= 90), (-180 <= lon <= 180))

