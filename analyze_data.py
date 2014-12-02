__author__ = 'brandy'
import json, os, sys


def generate_score_based_on_tweets(user_id, word_dict):
    tweet_arr = []

    with open(user_id + '.json') as json_file:
        user_data = json.loads(json_file.readline())
        if 'user_timeline' in user_data:
            tweets = user_data['user_timeline']
            for tweet in tweets:
                tweet_arr.append(tweet['text'])

    tweet_count = 1 # to avoid division by zero
    special_word_count = 0
    for tweet in tweet_arr:
        tweet_count += 1
        for special_word in word_dict:
            try:
                if " " + special_word + " " in tweet.lower():
                    special_word_count += 1
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
        #else:
            #print ".",


def generate_user_score_dict(array_of_user_dicts_and_weights):



def main(argv):

    # base scores on amount of followers, favorites, and words in tweets.


    negative_word_dict = generate_special_word_dict_from_file("negative_words")
    user_negativity_score_dict = process_all_json_files(negative_word_dict)
    print_user_ids_with_score_greater_than_n_to_screen(user_negativity_score_dict, 10)


    positive_word_dict = generate_special_word_dict_from_file("positive_words2")
    user_positivity_score_dict = process_all_json_files(positive_word_dict)
    print_user_ids_with_score_greater_than_n_to_screen(user_positivity_score_dict, 100)



    swear_word_dict = generate_special_word_dict_from_file("swear_words")
    user_profanity_score_dict = process_all_json_files(swear_word_dict)
    print_user_ids_with_score_greater_than_n_to_screen(user_profanity_score_dict)

    score_dict = generate_user_score_dict([(negative_word_dict, -1), (positive_word_dict, 3), (swear_word_dict, -5)])



if __name__ == "__main__":
    main(sys.argv)
