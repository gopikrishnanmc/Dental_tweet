import folium
import pprint
from tweet.database import engine, Base, EnglandDentalClinics
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

coordinates_address = []

dental_map = folium.Map(location=[52.9, -0.92], zoom_start=7)
fg = folium.FeatureGroup(name="My Map")

query = session.query(EnglandDentalClinics).filter(EnglandDentalClinics.dc_status_code == 'A').limit(9000).all()
for clinic in query:
    if clinic.dc_practice_type == 'D':
        practice_type = 'NHS and Private Dental Practice'
        marker_color = '#3186cc'
    elif clinic.dc_practice_type == 'P':
        practice_type = 'Private Only Dental Practice'
        marker_color = 'orange'
    else:
        marker_color = 'red'
    coordinates_address.append([clinic.dc_latitude, clinic.dc_longitude,
                                str(clinic.dc_address_line_full).replace("'", ""), practice_type, marker_color])

for coordinates in coordinates_address:
    fg.add_child(folium.CircleMarker(location=[coordinates[0], coordinates[1]],
                                     popup=coordinates[2] + ' || ' + coordinates[3],
                                     radius=5,
                                     fill=True,
                                     fill_color=coordinates[4],
                                     line_color='#3186cc',
                                     fill_opacity=0.7
                                     ))
dental_map.add_child(fg)
dental_map.save('c:/users/gopikrishnan/pycharmprojects/dental_tweet/mapping/maps/Map1.html')

# pprint.pprint(help(folium.Map))
