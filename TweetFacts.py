from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import WikiDentist, Base, DentistsCareer
from tweet_dental import Tweet
import os.path

# Create an engine that stores data in the local directory's dentists.db file
engine = create_engine('sqlite:///dentists.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class TweetFacts:
    def __init__(self):
        self.dentist = None
        self.hashtag_main = None
        self.hashtag_dental_informatics = '#DentalInformatics'
        self.hashtag_SPARQL = '#SPARQL'
        self.hashtag_linked_data = '#LinkedData'
        self.hashtag_SemanticWeb = '#SemanticWeb'
        self.wikidata = '-Data from @wikidata'
        self.dataviz = '#dataviz'

    def query_and_tweet_build(self):
        self.dentist = session.query(WikiDentist).filter_by(dentist_sex='female').order_by(WikiDentist.number_of_tweets).first()
        tweet_text = '{} {}, born: {}, Wiki-{}, Image-{}, Citizen of-{}, {} {} {} {}'. \
            format(self.hashtag_main,
                   self.dentist.dentist_name,
                   self.dentist.dentist_date_of_birth.split('T')[0],
                   self.dentist.dentist_wiki_site_link,
                   self.dentist.dentist_image,
                   self.dentist.dentist_country_citizen,
                   self.hashtag_dental_informatics, self.hashtag_SPARQL, self.hashtag_linked_data, self.hashtag_SemanticWeb
                   )
        return tweet_text, self.dentist.dentist_id

    def update_tweet_counter(self):
        dentistid = self.query_and_tweet_build()[1]
        den = session.query(WikiDentist).filter_by(dentist_id=dentistid).first()
        den.number_of_tweets += 1
        session.commit()

    def tweet_fact(self):
        tweet_text = self.query_and_tweet_build()[0]
        tweettweet = Tweet(tweet_text)
        tweettweet.do_tweet()
        self.update_tweet_counter()
        print(tweet_text)
        print('Done tweeting https://twitter.com/WikiDentalFacts ')


class FemaleDentists(TweetFacts):

    def __init__(self):
        super().__init__()
        self.hashtag_main = '#WomenInDentistry'

    def query_and_tweet_build(self):
        self.dentist = session.query(WikiDentist).filter_by(dentist_sex='female').order_by(WikiDentist.number_of_tweets).first()
        tweet_text = '{} {}, born: {}, Wiki-{}, Image-{}, Citizen of-{}, {} {} {} {} {}'. \
            format(self.hashtag_main,
                   self.dentist.dentist_name,
                   self.dentist.dentist_date_of_birth.split('T')[0],
                   self.dentist.dentist_wiki_site_link,
                   self.dentist.dentist_image,
                   self.dentist.dentist_country_citizen,
                   self.hashtag_dental_informatics, self.hashtag_SPARQL,
                   self.hashtag_linked_data, self.hashtag_SemanticWeb, self.wikidata
                   )

        return tweet_text, self.dentist.dentist_id


class DentistOfTheDay(TweetFacts):
    def __init__(self):
        super().__init__()
        self.hashtag_main = '#DentistOfTheDay'

    def query_and_tweet_build(self):
        self.dentist = session.query(WikiDentist).order_by(WikiDentist.number_of_tweets).first()
        tweet_text = '{} {}, born: {}, sex/gender-{}, Wiki-{}, Image-{}, Citizen of-{}, {} {} {} {} {}'. \
            format(self.hashtag_main,
                   self.dentist.dentist_name,
                   self.dentist.dentist_date_of_birth.split('T')[0],
                   self.dentist.dentist_sex,
                   self.dentist.dentist_wiki_site_link,
                   self.dentist.dentist_image,
                   self.dentist.dentist_country_citizen,
                   self.hashtag_dental_informatics, self.hashtag_SPARQL,
                   self.hashtag_linked_data, self.hashtag_SemanticWeb, self.wikidata
                   )
        return tweet_text, self.dentist.dentist_id


class DentistAltCareers(TweetFacts):
    def __init__(self):
        super().__init__()
        self.hashtag_main = '#AlternateCareers'

    def query_and_tweet_build(self):
        self.dentist = session.query(DentistsCareer).order_by(DentistsCareer.number_of_tweets).first()
        dentist_career = str(self.dentist.dentist_alt_career).title()
        tweet_text = '{} #Dentists with alternate careers, {}, Dentist & {}, born: {}, Wiki-{}, {} {} {} {} {}'. \
            format(self.hashtag_main,
                   self.dentist.dentist_name,
                   dentist_career,
                   self.dentist.dentist_date_of_birth.split('T')[0],
                   self.dentist.dentist_wiki_site_link,
                   self.hashtag_dental_informatics, self.hashtag_SPARQL,
                   self.hashtag_linked_data, self.hashtag_SemanticWeb, self.wikidata
                   )
        return tweet_text, self.dentist.dentist_id

    def update_tweet_counter(self):
        dentistid = self.query_and_tweet_build()[1]
        den = session.query(DentistsCareer).filter_by(dentist_id=dentistid).first()
        den.number_of_tweets += 1
        session.commit()


class TweetDentalGraphs(TweetFacts):
    def __init__(self):
        super().__init__()
        self.hashtag_main = '#AlternateCareers'

    def query_and_tweet_build(self):
        tweet_text = '{} #Dentists with alternate careers. Most famous dentists in #Wikidata are also politicians!! {} {} {} {} {} {}'. \
            format(self.hashtag_main, self.hashtag_dental_informatics, self.hashtag_SPARQL,
                   self.hashtag_linked_data, self.hashtag_SemanticWeb, self.dataviz, self.wikidata
                   )
        return tweet_text

    def tweet_image(self, file):
        tweet_text = self.query_and_tweet_build()
        # print(tweet_text)
        tg = Tweet(tweet_text)
        if os.path.isfile(file):
            tg.tweet_image(file)
            print('Done tweeting https://twitter.com/WikiDentalFacts')
        else:
            print('File not found')


# tdg = TweetDentalGraphs()
# tdg.tweet_image('images/dentists/dentist_careers.png')
