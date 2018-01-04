from sqlalchemy.orm import sessionmaker
from tweet.TweetFacts import TweetFacts
from tweet.database import Base, engine, DentistsCareer

# Create an engine that stores data in the local directory's dentists.db file
engine = engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class DentistAltCareers(TweetFacts):
    def __init__(self):
        super().__init__()
        self.hashtag_main = '#AlternateCareers' + ' ' + '#Dentists with alternate careers.' + ' '

    def query_and_tweet_build(self):
        self.dentist = session.query(DentistsCareer).order_by(DentistsCareer.number_of_tweets).first()
        dentist_career = str(self.dentist.dentist_alt_career).title()
        tweet_text = '{}, Dentist & {}, born: {}, Wiki-{},'. \
            format(self.dentist.dentist_name,
                   dentist_career,
                   self.dentist.dentist_date_of_birth.split('T')[0],
                   self.dentist.dentist_wiki_site_link
                   )
        tweet_text = self.hashtag_main + tweet_text + self.hashtag_other
        return tweet_text, self.dentist.dentist_id

    def update_tweet_counter(self):
        dentistid = self.query_and_tweet_build()[1]
        den = session.query(DentistsCareer).filter_by(dentist_id=dentistid).first()
        den.number_of_tweets += 1
        session.commit()

