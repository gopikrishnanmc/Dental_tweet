from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut
import pprint
from mapping.google_map_api import api_key

# geolocator = Nominatim()

geolocator = GoogleV3(api_key=api_key, domain='maps.google.co.uk')

raw_osm = {'geometry': {'location': {'lat': 0.0, 'lng': 0.0},
                        'location_type': 'ROOFTOP',
                        'viewport': {'northeast': {'lat': 52.6247302802915,
                                                   'lng': 1.248281280291502},
                                     'southwest': {'lat': 52.6220323197085,
                                                   'lng': 1.245583319708498}}},
           'place_id': 'ChIJ_5bHoT_h2UcROQ4uonCFP78',
           'types': ['doctor', 'establishment', 'health', 'point_of_interest']}


class LatLonGenerator:
    """
    This class takes the address and postcode (as backup) and returns a dictionary with the latitude and longitude of the dental clinic.


    """

    def __init__(self, address, post_code):
        """

        :param string address: The full dental clinic address from which the latitude and longitude are generated
        :param string post_code: If the API cannot return a latitude and longitude from the full address then the postcode is
        used to obtain the nearest coordinates
        """
        self.address = address
        self.post_code = post_code

    def get_lat_lon(self) -> dict:
        """

        :return : Returns a dict which contains the latitude and the longitude.
        :rtype: dict
        :exception : Raise GeocoderTimedOut when the API request times out.
        """
        try:
            location = geolocator.geocode(self.address, timeout=10)
            if location is None:  # If the geocoding API cannot get the coordinates use the postcode
                print(self.post_code + '-')
                location_postcode = geolocator.geocode(self.post_code, timeout=10)
                return location_postcode.raw
            else:
                print(self.post_code + '+')
                return location.raw
        except Exception as e:
            print("Error:geocode failed on input {} with message {} ".format(self.post_code, str(e)))
            location_postcode = raw_osm
            return location_postcode


# li = LatLonGenerator('UEA HEALTH CENTRE, UNIVERSITY OF EAST ANGLIA, EARLHAM ROAD, NORWICH, NORFOLK, NR4 7TJ', 'NR4 7TJ')

# print(li.get_lat_lon()['geometry']['location']['lat'] + ',' + li.get_lat_lon()['geometry']['location']['lng'])
# #Google V3

# pprint.pprint(li.get_lat_lon())
