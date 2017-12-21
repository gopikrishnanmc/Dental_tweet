from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import WikiDentist, Base, DentistsCareer
from sparql_wrap import wiki_dent, dental_career

# Create an engine that stores data in the local directory's dentists.db file
engine = create_engine('sqlite:///dentists.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class DBInsert:

    def __init__(self):
        self.dentist_results = None
        self.row = None

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


db = DBInsert()
# db.insert_dentist_data()
# db.insert_dentist_careers()
