from tweet.TweetFemaleDentists import FemaleDentists
from tweet.DentistOfTheDay import DentistOfTheDay
from tweet.DentistAltCareers import DentistAltCareers
from tweet.TweetFacts import TweetDentalGraphs
import time

if __name__ == '__main__':
    fd = FemaleDentists()
    dod = DentistOfTheDay()
    dac = DentistAltCareers()

    tg = TweetDentalGraphs

    # Daily Tweets
    fd.tweet_fact()  # #WomenInDentistry
    time.sleep(10)
    dod.tweet_fact()  # #DentistOfTheDay
    time.sleep(10)
    dac.tweet_fact()  # #AlternateCareers
