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


class TweetDentalGraphs(TweetFacts):
    """
    Tweet text and images from pandas visualisations or map images.

    """

    def __init__(self):
        super().__init__()
        self.hashtag_main = '#DentalPractices #Dentists'
        self.hashtag_other = self.hashtag_dental_informatics + '' + self.dataviz

    def query_and_tweet_build(self):
        """
        :return: Text for tweeting
        """

        tweet_text = '{} '.format(self.hashtag_main)
        tweet_text = tweet_text + ' ' + self.hashtag_other  # Adds the main tweet text to other hashtags
        return tweet_text

    def tweet_image(self, file):
        """
        This method takes the path to the image as an argument. It also takes the tweet text returned from query_and_tweet_build() method and
        tweet the text alongside the image.

        :param file:
        """

        tweet_text = self.query_and_tweet_build()
        tg = Tweet(tweet_text)  # Tweet text

        try:
            os.path.isfile(file)  # If image file is present
        except FileNotFoundError as w:
            print('File not found' + str(w))
        else:
            tg.tweet_image(file)  # Tweet image
            print('Done tweeting https://twitter.com/WikiDentalFacts')

# tg = TweetDentalGraphs()
# tg.tweet_image('../images/dentists/sample.jpg')
