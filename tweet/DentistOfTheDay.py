from sqlalchemy.orm import sessionmaker
from tweet.TweetFacts import TweetFacts
from tweet.database import Base, WikiDentist, engine

# Create an engine that stores data in the local directory's dentists.db file
engine = engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class DentistOfTheDay(TweetFacts):
    def __init__(self):
        super().__init__()
        self.hashtag_main = '#Dentists from #Wikipedia.' + ' '

    def query_and_tweet_build(self):
        self.dentist = session.query(WikiDentist).order_by(WikiDentist.number_of_tweets).first()
        if self.dentist.dentist_image == 'unknown' and self.dentist.dentist_country_citizen == 'unknown':
            tweet_text = '{}, born: {}, sex/gender-{}, Wiki-{},'. \
                format(self.dentist.dentist_name,
                       self.dentist.dentist_date_of_birth.split('T')[0],
                       self.dentist.dentist_sex,
                       self.dentist.dentist_wiki_site_link
                       )
        elif self.dentist.dentist_country_citizen == 'unknown':
            tweet_text = '{}, born: {}, sex/gender-{}, Wiki-{}, Image-{},'. \
                format(self.dentist.dentist_name,
                       self.dentist.dentist_date_of_birth.split('T')[0],
                       self.dentist.dentist_sex,
                       self.dentist.dentist_wiki_site_link,
                       self.dentist.dentist_image
                       )
        elif self.dentist.dentist_image == 'unknown':
            tweet_text = '{}, born: {}, sex/gender-{}, Wiki-{}, Citizen of-{},'. \
                format(self.dentist.dentist_name,
                       self.dentist.dentist_date_of_birth.split('T')[0],
                       self.dentist.dentist_sex,
                       self.dentist.dentist_wiki_site_link,
                       self.dentist.dentist_country_citizen
                       )
        else:
            tweet_text = '{}, born: {}, sex/gender-{}, Wiki-{}, Image-{}, Citizen of-{},'. \
                format(self.dentist.dentist_name,
                       self.dentist.dentist_date_of_birth.split('T')[0],
                       self.dentist.dentist_sex,
                       self.dentist.dentist_wiki_site_link,
                       self.dentist.dentist_image,
                       self.dentist.dentist_country_citizen
                       )
        tweet_text = self.hashtag_main + tweet_text + self.hashtag_other
        return tweet_text, self.dentist.dentist_id

