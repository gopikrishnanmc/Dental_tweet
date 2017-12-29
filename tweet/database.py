from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class WikiDentist(Base):
    __tablename__ = 'wikidentists'

    dentist_id = Column(Integer(), primary_key=True)
    dentist_wiki_id = Column(String(200))
    dentist_date_of_birth = Column(String(50))
    dentist_image = Column(String(255), nullable=True)
    dentist_wiki_site_link = Column(String(255))
    dentist_name = Column(String(100))
    dentist_sex = Column(String(20), nullable=True)
    dentist_country_citizen = Column(String(80), nullable=True)
    number_of_tweets = Column(Integer(), default=0)

    def __repr__(self):
        return "{self.dentist_name}, " \
               "{self.dentist_wiki_site_link}".format(self=self)


class DentistsCareer(Base):
    __tablename__ = 'dentistcareers'

    dentist_id = Column(Integer(), primary_key=True)
    dentist_name = Column(String(100))
    dentist_wiki_id = Column(String(200))
    dentist_date_of_birth = Column(String(50))
    dentist_alt_career = Column(String(100))
    dentist_wiki_site_link = Column(String(255))
    number_of_tweets = Column(Integer(), default=0)

    def __repr__(self):
        return "{self.dentist_name}, {self.dentist_alt_career}"


class EnglandDentalClinics(Base):
    __tablename__ = 'englanddentalclinics'

    dc_id = Column(Integer(), primary_key=True)
    dc_file_id = Column(String(30))
    dc_name = Column(String(100))
    dc_address_line_1 = Column(String(50))
    dc_address_line_2 = Column(String(20), nullable=True)
    dc_address_line_3 = Column(String(20), nullable=True)
    dc_address_line_4 = Column(String(20), nullable=True)
    dc_address_line_5 = Column(String(20), nullable=True)
    dc_address_line_full = Column(String(255), nullable=True)
    dc_postcode = Column(String(20))
    dc_latitude = Column(Float(), nullable=True)
    dc_longitude = Column(Float(), nullable=True)
    dc_status_code = Column(String(5))
    dc_practice_type = Column(String(5))




# Create an engine that stores data in the local directory's dentists.db file
engine = create_engine('sqlite:///sqlite_db/dentists.db')
Base.metadata.create_all(engine)
