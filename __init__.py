from tweet.TweetFacts import FemaleDentists, DentistOfTheDay, DentistAltCareers
import time

if __name__ == '__main__':
    fd = FemaleDentists()
    dod = DentistOfTheDay()
    dac = DentistAltCareers()

    # Daily Tweets
    fd.tweet_fact()  # #WomenInDentistry
    time.sleep(10)
    dod.tweet_fact()  # #DentistOfTheDay
    time.sleep(10)
    dac.tweet_fact()  # #AlternateCareers
