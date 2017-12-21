from TweetFacts import FemaleDentists, DentistOfTheDay, DentistAltCareers
import time

if __name__ == '__main__':
    fd = FemaleDentists()
    dod = DentistOfTheDay()
    dac = DentistAltCareers()

    fd.tweet_fact()
    time.sleep(10)
    dod.tweet_fact()
    time.sleep(10)
    dac.tweet_fact()
