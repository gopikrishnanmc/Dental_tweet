from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tweet.database import WikiDentist, Base, DentistsCareer
from tweet.tweet_dental import Tweet
import os.path

# Create an engine that stores data in the local directory's dentists.db file
engine = create_engine('sqlite:///sqlite_db/dentists.db')
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
        self.hashtag_other = ' ' + \
                             self.hashtag_dental_informatics + ' ' + \
                             self.hashtag_SPARQL + ' ' + \
                             self.hashtag_linked_data + ' ' + \
                             self.hashtag_SemanticWeb + ' ' + \
                             self.wikidata
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





class DentistOfTheDay(TweetFacts):
    def __init__(self):
        super().__init__()
        self.hashtag_main = '#DentistOfTheDay' + ' '

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


class TweetDentalGraphs(TweetFacts):
    """
    Tweet text and images from pandas visualisations or map images.

    """

    def __init__(self):
        """

        """

        super().__init__()
        self.hashtag_main = '#AlternateCareers'
        self.hashtag_other = ' ' + \
                             self.hashtag_dental_informatics + ' ' + \
                             self.hashtag_SPARQL + ' ' + \
                             self.hashtag_linked_data + ' ' + \
                             self.hashtag_SemanticWeb + ' ' + \
                             self.dataviz

    def query_and_tweet_build(self):
        """

        :return:
        """

        tweet_text = '{} #Dentists with alternate careers. Most famous dentists in #Wikidata are also politicians!!'. \
            format(self.hashtag_main)
        tweet_text = tweet_text + ' ' + self.hashtag_other  # Adds the main tweet text to other hashtags
        return tweet_text

    def tweet_image(self, file):
        """
        This method takes the path to the image as a argument. However if the image file is not present in the path
        it will print 'File not found'. It also takes the tweet text returned from query_and_tweet_build() method and
        tweet the text alongside the image.

        :param file:
        :return:
        """

        tweet_text = self.query_and_tweet_build()
        tg = Tweet(tweet_text)  # Tweet text
        if os.path.isfile(file):  # If image file is present
            tg.tweet_image(file)  # Tweet image
            print('Done tweeting https://twitter.com/WikiDentalFacts')
        else:
            print('File not found')
