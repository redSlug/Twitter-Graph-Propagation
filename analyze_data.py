__author__ = 'brandy'
import json, os, sys

class User_Score_Vector:        # this is not json serializable!!!
    def __init__(self, retweets=0, favorites=0, followers=0, negativity=0, positivity=0, swearing=0):
        self.retweets = retweets
        self.favorites = favorites
        self.followers = followers
        self.negativity = negativity
        self.positivity = positivity
        self.swearing = swearing
        self.score = self.calculateScore()

    def calculateScore(self):
        baseScore = 50

        if self.retweets >= 2:
            baseScore += 1
        elif self.retweets >= 10:
            baseScore += 2
        elif self.retweets >= 20:
            baseScore += 3

        if self.followers >= 25:
            baseScore += 1
        elif self.followers >= 250:
            baseScore += 2
        elif self.followers >= 2500:
            baseScore += 3

        if self.positivity >= 5:
            baseScore += 1
        elif self.positivity >= 50:
            baseScore += 2
        elif self.positivity >= 80:
            baseScore += 3

        if self.negativity >= 5:
            baseScore -= 3
        elif self.negativity >= 50:
            baseScore -= 5
        elif self.negativity >= 80:
            baseScore -= 10

        if self.swearing >= 1:
            baseScore -= 10
        elif self.swearing >= 5:
            baseScore -= 20
        elif self.swearing >= 10:
            baseScore -= 40
        return baseScore


def generate_score_based_on_tweets(user_id, word_dict):
    tweet_arr = []

    with open(user_id + '.json') as json_file:
        user_data = json.loads(json_file.readline())
        if 'user_timeline' in user_data:
            tweets = user_data['user_timeline']
            for tweet in tweets:
                tweet_arr.append(tweet['text'])

    tweet_count = 1     # to avoid division by zero
    special_word_count = 0
    for tweet in tweet_arr:
        tweet_count += 1
        for special_word in word_dict:
            try:
                if " " + special_word + " " in tweet.lower():
                    special_word_count += 1
                    break   # just looking for one word in the tweet, keeps it normalized between 0 and 100%
            except:
                print "problem with word:", special_word

    #print user_id, special_word_count, int((special_word_count/float(tweet_count))*100)
    return int(user_id), int((special_word_count/float(tweet_count))*100)


def generate_special_word_dict_from_file(file_name):
    """
    :param file_name: words separated by line
    :return: a dictionary of words
    """
    special_word_dict = {}
    with open(file_name) as f:
        content = f.readlines()
        for line in content:
            word_or_phrase = line.strip()
            if word_or_phrase not in special_word_dict:
                special_word_dict[word_or_phrase] = True
    return special_word_dict


def process_all_json_files(word_dict):
    os.chdir('json')
    id_to_score_dict = {}
    for file_name in os.listdir('.'):  # grabbing all ids from json files from current directory
        if file_name.endswith(".json"):
            id, score = generate_score_based_on_tweets(file_name[:-5], word_dict)
            id_to_score_dict[id] = score
    os.chdir('../')  # setting state back to how it started
    return id_to_score_dict


def print_user_ids_with_score_greater_than_n_to_screen(dict, n):
    for key in dict:
        if dict[key] > n:
            print key, dict[key]


def save_user_id_to_score_vector_to_file():
    # base scores on amount of followers, favorites, and words in tweets.

    negative_word_dict = generate_special_word_dict_from_file("negative_words")
    user_negativity_score_dict = process_all_json_files(negative_word_dict)

    positive_word_dict = generate_special_word_dict_from_file("positive_words2")
    user_positivity_score_dict = process_all_json_files(positive_word_dict)

    swear_word_dict = generate_special_word_dict_from_file("swear_words")
    user_profanity_score_dict = process_all_json_files(swear_word_dict)

    #user_negativity_score_dict = user_positivity_score_dict = user_profanity_score_dict = {}

    os.chdir('json')
    id_to_score_dict = {}
    for file_name in os.listdir('.'):  # grabbing all ids from json files from current directory
        if file_name.endswith(".json"):
            with open(file_name) as json_file:
                user_id = int(file_name[:-5])
                user_data = json.loads(json_file.readline())
                tweetsToExamine = 10
                retweetCount = 0
                favoriteCount = 0
                if not 'user_timeline' in user_data:
                    continue
                for tweet in user_data['user_timeline']:
                    if tweetsToExamine == 0:
                        break
                    tweetsToExamine -= 1
                    retweetCount += tweet['retweet_count']
                    favoriteCount += tweet['favorite_count']

                followerCount = user_data['followers_ids'].__len__()   #    5000 is the limit of num followeres saved
                negativity = positivity = swearing = 0
                if user_id in user_negativity_score_dict:
                    negativity = user_negativity_score_dict[user_id]
                if user_id in user_positivity_score_dict:
                    positivity = user_positivity_score_dict[user_id]
                if user_id in user_profanity_score_dict:
                    swearing = user_profanity_score_dict[user_id]


                usv = User_Score_Vector(retweetCount, favoriteCount, followerCount, negativity, positivity, swearing)
                id_to_score_dict[user_id] = [retweetCount, favoriteCount, followerCount, negativity, positivity, swearing, usv.score]

    os.chdir('../')  # setting state back to how it started

    json_encoded = json.dumps(id_to_score_dict)
    f = open(str("user_id_score_vector_dict") + '.json', 'w')
    f.write(json_encoded)
    f.close()

def main(argv):
    save_user_id_to_score_vector_to_file()

    file_name = "user_id_score_vector_dict.json"
    score_histogram = {}
    with open(file_name) as json_file:
        id_score_dict = json.loads(json_file.readline())
        for user_id in id_score_dict:
            if id_score_dict[user_id][-1] not in score_histogram:   # last one refers to score
                score_histogram[id_score_dict[user_id][-1]] = []
            score_histogram[id_score_dict[user_id][-1]].append(user_id)
        print









if __name__ == "__main__":
    print
    main(sys.argv)
