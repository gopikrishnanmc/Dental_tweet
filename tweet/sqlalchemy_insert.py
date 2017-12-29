from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tweet.database import WikiDentist, Base, DentistsCareer, EnglandDentalClinics, engine
from tweet.sparql_wrap import wiki_dent, dental_career
from mapping.read_csv import CSV2Dict
from mapping.lat_lon_converter import LatLonGenerator
import time
import gc
import csv

# Create an engine that stores data in the local directory's dentists.db file
engine = engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class DBInsert:

    def __init__(self):
        self.dentist_results = None
        self.row = None
        self.dental_clinics = None

    def insert_dentist_data(self):
        self.dentist_results = wiki_dent.results()
        for result in self.dentist_results["results"]["bindings"]:
            self.row = WikiDentist(
                dentist_wiki_id=result['Dentists']['value'],
                dentist_date_of_birth=result['DateOfBirth']['value'],
                dentist_wiki_site_link=result['sitelink']['value'],
                dentist_name=result['DentistsLabel']['value'],
                dentist_image=result['image']['value'],
                dentist_sex=result['SexGenderLabel']['value'],
                dentist_country_citizen=result['CitizenCountryLabel']['value']
            )
            session.add(self.row)
        den = session.query(WikiDentist).filter_by(dentist_sex='intersex').one()
        session.delete(den)
        session.commit()

    def insert_dentist_careers(self):
        self.dentist_results = dental_career.results()
        for result in self.dentist_results["results"]["bindings"]:
            self.row = DentistsCareer(
                dentist_wiki_id=result['Dentists']['value'],
                dentist_name=result['DentistsLabel']['value'],
                dentist_date_of_birth=result['DateOfBirth']['value'],
                dentist_alt_career=result['OccupationLabel']['value'],
                dentist_wiki_site_link=result['sitelink']['value']
            )
            session.add(self.row)
        session.commit()

    @staticmethod
    def print_results(data_text):
        print(wiki_dent.print_results(data_text))


class MappingDBInsert(DBInsert):

    def __init__(self):
        super().__init__()

    def insert_dental_clinics(self, csv_file):
        csv_dict = CSV2Dict(csv_file)
        self.dental_clinics = csv_dict.get_dict_clinics()
        try:
            for result in self.dental_clinics:
                self.row = EnglandDentalClinics(
                    dc_file_id=result['dc_file_id'],
                    dc_name=result['dc_name'],
                    dc_address_line_1=result['dc_address_line_1'],
                    dc_address_line_2=result['dc_address_line_2'],
                    dc_address_line_3=result['dc_address_line_3'],
                    dc_address_line_4=result['dc_address_line_4'],
                    dc_address_line_5=result['dc_address_line_5'],
                    dc_postcode=result['dc_postcode'],
                    dc_status_code=result['dc_status_code'],
                    dc_practice_type=result['dc_practice_type']
                )
                session.add(self.row)
            session.commit()
        except Exception as e:
            print(str(e))
            session.rollback()

    @staticmethod
    def insert_full_address():
        dental_c = session.query(EnglandDentalClinics).all()
        for clinic in dental_c:
            if clinic.dc_address_line_2 == '':
                add_line_2 = ''
            else:
                add_line_2 = clinic.dc_address_line_2 + ', '

            if clinic.dc_address_line_3 == '':
                add_line_3 = ''
            else:
                add_line_3 = clinic.dc_address_line_3 + ', '

            if clinic.dc_address_line_4 == '':
                add_line_4 = ''
            else:
                add_line_4 = clinic.dc_address_line_4 + ', '

            if clinic.dc_address_line_5 == '':
                add_line_5 = ''
            else:
                add_line_5 = clinic.dc_address_line_5 + ', '

            clinic.dc_address_line_full = clinic.dc_address_line_1 + ', ' + add_line_2 + \
                                          add_line_3 + \
                                          add_line_4 + \
                                          add_line_5 + \
                                          clinic.dc_postcode

        session.commit()


def insert_lat_long():
    start = time.time()
    dental_lat_lon = session.query(EnglandDentalClinics).filter(EnglandDentalClinics.dc_latitude == None,
                                                                EnglandDentalClinics.dc_status_code == 'A').limit(100).all()
    count = 0
    for clinic in dental_lat_lon:
        lat_lon = LatLonGenerator(clinic.dc_address_line_full, clinic.dc_postcode)
        clinic.dc_latitude = float(lat_lon.get_lat_lon()['lat'])
        clinic.dc_longitude = float(lat_lon.get_lat_lon()['lon'])
        count += 1
        print(count)
        time.sleep(1)

    session.commit()
    end = time.time()
    elapsed = end - start
    print(elapsed)
    gc.collect()


def insert_lat_long_to_CSV():
    dental_lat_lon = session.query(EnglandDentalClinics).filter(EnglandDentalClinics.dc_longitude  == 0.0,
                                                                EnglandDentalClinics.dc_status_code == 'A').limit(2).all()
    for clinic in dental_lat_lon:
        lat_lon = LatLonGenerator(clinic.dc_address_line_full, clinic.dc_postcode)
        my_data = [clinic.dc_id, clinic.dc_file_id, clinic.dc_postcode,
                   lat_lon.get_lat_lon()['geometry']['location']['lat'],
                   lat_lon.get_lat_lon()['geometry']['location']['lng']
                   ]
        time.sleep(0.5)
        with open('clinic_latitude_longitude.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(my_data)
    gc.collect()

def insert_lat_lon_CSV_to_DB():
    with open('clinic_latitude_longitude.csv') as f:
        read_CSV = csv.reader(f, delimiter=',')
        for row in read_CSV:
            clinic = session.query(EnglandDentalClinics).filter_by(dc_id=row[0]).first()
            clinic.dc_latitude = float(row[3])
            clinic.dc_longitude = float(row[4])
        session.commit()

# db.insert_dentist_data()
# db.insert_dentist_careers()
# db.insert_dental_clinics(csv_file='mapping/clinic_data/egdpprac.csv')
# db.insert_full_address()
# db.insert_lat_long()
# db = MappingDBInsert()

# insert_lat_long_to_CSV()
#
# insert_lat_lon_CSV_to_DB()
