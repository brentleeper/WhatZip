connection_parameters = {
        'host': 'localhost',
        'database': 'postgis',
        'user': 'brent',
        'password': ''
    }

zip_zipcode_query = """
select zcta5ce10 as zipcode, ST_AsGeoJSON(ST_Transform(geom,4326)) as geo_json, state_name, county_name
from public.zipcodes_2015, public.state_map_2017, public.county_map_2017
where 
    zcta5ce10 = %(zipcode)s
    and
    ST_Intersects(
        ST_SetSRID(state_geom, 4326),
        ST_SetSRID(ST_Centroid(geom), 4326)
    )
    and
    ST_Intersects(
        ST_SetSRID(county_geom, 4326),
        ST_SetSRID(ST_Centroid(geom), 4326)
    );
"""

zip_coordinate_query = """
select zcta5ce10 as zipcode, ST_AsGeoJSON(ST_Transform(geom,4326)) as geo_json, state_name, county_name
from public.zipcodes_2015, public.state_map_2017, public.county_map_2017
where 
    ST_Intersects(
        ST_SetSRID(geom, 4326),
        ST_SetSRID(ST_MakePoint(%(lon)s, %(lat)s), 4326)
    )
    and 
    ST_Intersects(  
        ST_SetSRID(state_geom, 4326),
        ST_SetSRID(ST_Centroid(geom), 4326)
    )
    and
    ST_Intersects(
        ST_SetSRID(county_geom, 4326),
        ST_SetSRID(ST_Centroid(geom), 4326)
    );
"""

zip_radius_query = """
select zcta5ce10 as zipcode, ST_AsGeoJSON(ST_Transform(geom,4326)) as geo_json, state_name, county_name
from public.zipcodes_2015, public.state_map_2017, public.county_map_2017
where 
    ST_DWithin(
        geography(ST_SetSRID(geom, 4326)),
        geography(ST_SetSRID(ST_MakePoint(%(lon)s, %(lat)s), 4326)),
        1609 * %(radius_miles)s
    )
    and
    ST_Intersects(
        ST_SetSRID(state_geom, 4326),
        ST_SetSRID(ST_Centroid(geom), 4326)
    )
    and
    ST_Intersects(
        ST_SetSRID(county_geom, 4326),
        ST_SetSRID(ST_Centroid(geom), 4326)
    );
"""
