import folium

dental_map = folium.Map(location=[52.9, -0.92], zoom_start=8)
dental_map.add_child(folium.Marker(location=[51.0133807, -3.1057278],
                                   popup="CRESCENT DENTAL PRACTICE",
                                   icon=folium.Icon(color='green')
                                   ))
dental_map.save('maps/Map1.html')
