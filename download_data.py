__author__ = 'brandy'

import tweepy, sys, json, os, time
from time import gmtime, strftime


def sign_in_to_twitter_and_get_api():
    """ :returns api used to make queries to twitter
    This function requires a file named secret in the root directory of the project.
        The file must have the consumer_key, consumer_secret,... all on separate lines.
    """
    with open('secret') as f:  # secret is a file with twitter access keys
        secret = f.readlines()

    CONSUMER_KEY = secret[0].rstrip()
    CONSUMER_SECRET = secret[1].rstrip()
    ACCESS_KEY = secret[2].rstrip()
    ACCESS_SECRET = secret[3].rstrip()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)


def print_expiration_status(api):
    """ prints api call limit status to standard output
    This function is for debugging purposes. Items can be added to desired_info array to see more detailed stats.
        This function reveals how many queries you can still make to the Twitter api at the current time.
    Args:
        api: twitter api signed into using 'secret' credentials
    """
    resource = api.rate_limit_status()['resources']

    # data of interest. this could be passed in as a parameter but I'm lazy
    desired_info = ['application /application/rate_limit_status', 'friends /friends/ids',
                    'friends /friends/list', 'followers /followers/ids', 'followers /followers/list']

    # get limit, remaining, and print it to screen
    for chunk in desired_info:
        cur_resource = resource
        chunk_array = chunk.split()
        length = len(chunk)
        for sub in chunk_array:
            print sub,
            cur_resource = cur_resource[sub]
        print " " * (50 - length),  # makes it print pretty
        print "remaining = %d\t\t limit = %d" % (cur_resource['remaining'], cur_resource['limit'])


def save_user_data_to_file(api, cur_user_id):
    """ :returns string indicating "success" if some user data saved to json or a string with detail about the exception
    This function makes an attempt to save data for one user (follower_ids, user_timeline (tweets), and friends_ids)
        to a json file using the api. friends_ids are not always available based on user privacy settings.
    Args:
        api: twitter api signed into using 'secret' credentials
        cur_user_id: unique id for a given twitter user. can be obtained from http://mytwitterid.com/
    """
    if os.path.isfile(str(cur_user_id) + '.json'):
        print "user already exists"
        return "error"
    try:
        cur_user = {}
        cur_user['followers_ids'] = api.followers_ids(cur_user_id)
        cur_user['user_timeline'] = []
        timeline_data = api.user_timeline(cur_user_id)  # todo get more tweets?
        for tweet in timeline_data:
            cur_user['user_timeline'].append(tweet._json)

        cur_user['friends_ids'] = api.friends_ids(cur_user_id)  # keep last; sometimes not authorized to get this info

    except tweepy.TweepError as e:
        if 'Not authorized' in e.message:
            # usually just means that friends ids is not authorized, but followers and timeline are still retrieved
            print("not authorized for ", cur_user_id)
        elif 'code' in e.message[0] and e.message[0]['code'] == 88:
            # really just likely a bad connection?
            # rate limit exceeded
            """
            when the machine falls asleep, wireless connection goes away. so change energy settings to avoid this
            raise TweepError('Failed to send request: %s' % e)
            tweepy.error.TweepError: Failed to send request: [Errno 8] nodename nor servname provided, or not known
            """
            return "timeout error"
        else:
            print "unrecognized error", e
            return "unrecognized error"

    json_encoded = json.dumps(cur_user)
    f = open(str(cur_user_id) + '.json', 'w')
    f.write(json_encoded)
    f.close()
    return "success"


def add_to_second_list_if_not_in_either_list(user_id, l1, l2):
    # helper method
    if user_id not in l1 and user_id not in l2:
        l2.append(user_id)


def get_array_of_current_degree_ids():
    # helper method
    user_ids = []
    for file_name in os.listdir('.'):
        if file_name.endswith(".json"):
            user_ids.append(int(file_name[:-5]))
    return user_ids


def get_explored_and_unexplored_user_ids_from_current_directory():
    """ :returns a list of user_ids for which json files exist, and a list of user_ids for which json files do not exist
    This function generates two lists of user ids, first by iterating through the files names in the current directory
        second by examining the contents of all of the files in the directory and grabbing follower/friend user ids.
        Two separate loops are used to ensure that unexplored_contact_ids are unique and don't overlap with explored.
    """
    explored_contact_ids = get_array_of_current_degree_ids()  # assume explored if json file exists in current directory

    unexplored_contact_ids = []
    for file_name in os.listdir('.'):  # grabbing all ids from json files from current directory
        if file_name.endswith(".json"):
            with open(file_name) as json_file:
                current_user_data = json.loads(json_file.readline())
                if 'followers_ids' in current_user_data:
                    for contact_id in current_user_data['followers_ids']:
                        add_to_second_list_if_not_in_either_list(contact_id, explored_contact_ids, unexplored_contact_ids)
                if 'friends_ids' in current_user_data:
                    for contact_id in current_user_data['friends_ids']:
                        add_to_second_list_if_not_in_either_list(contact_id, explored_contact_ids, unexplored_contact_ids)
    return explored_contact_ids, unexplored_contact_ids


def explore_array_of_users_querrying_api(api, user_ids):
    """
    This function saves each user associated with the user_ids array to new json file if it does not already exist
    Args:
        api: twitter api signed into using 'secret' credentials
        user_ids: list of ids to query the api with and save as json files
    """
    for user_id in user_ids:
        json_file_for_this_user_id_already_exists = os.path.isfile(str(user_id) + '.json')

        if not json_file_for_this_user_id_already_exists:
            result = save_user_data_to_file(api, user_id)
            if "success" in result:
                continue
            elif "timeout" in result:
                print "sleeping 15m ",
                print strftime("%Y-%m-%d %H:%M:%S", gmtime())
                print_expiration_status(api)
                time.sleep(60 * 15)  # Rate limits in version 1.1 of the API are divided into 15 minute intervals
                # retrying with same user. this is kind of hacky. maybe there is a better way to do it
                result = save_user_data_to_file(api, user_id)
                if "error" in result:
                    print "second error after time out"
            else:
                print "skipped: ", user_id  # this should never happen


def save_next_degree_ids_to_file():
    """ generates a list of user_ids to explores, and saves the list to a file
    This function exists because sometimes the program gets stopped mid-way (if you have to shut off your computer)
        Having the next generation user_ids in a file makes it possible to resume the program without mixing the
        generations / degrees of separation.
    """
    explored, unexplored = get_explored_and_unexplored_user_ids_from_current_directory()

    with open("user_ids", "a") as user_ids_file:
        for user_id in unexplored:
            user_ids_file.write(str(user_id) + "\n")    # todo maybe save it as json instead?


def get_json_data_for_user_ids_array(api, nth_degree_array_of_ids):
    """
    This function exists because sometimes something interrupts getting the nth degree.
    # todo possibly save the user_id associated with nth degree somewhere
    Args:
        nth_degree_array_of_ids: can be an array containing just a seed user_id, or data from user_ids file
    """
    user_ids_of_contacts_of_nth_degree = []

    for user_id in nth_degree_array_of_ids:
        current_user_file_name = str(user_id) + '.json'

        with open(current_user_file_name) as current_user_json_file:
            current_user_data = json.loads(current_user_json_file.readline())
            # todo check for duplicates so explore_array_of_users_querrying_api does not have to check
            user_ids_of_contacts_of_nth_degree += current_user_data['followers_ids'] + current_user_data['friends_ids']

    explore_array_of_users_querrying_api(api, user_ids_of_contacts_of_nth_degree)

def process_request(api, choice = "", data=""):
    """
    Must have at least 1 json file / seed before "save_next_gen_ids"
    Must have user_ids list of un-processed users before "process_next_gen"
    :param api: twitter api signed into using 'secret' credentials
    :param choice: what you want to do
    :param data: possible seed id
    :return:
    """
    if 'start_fresh' in choice:
        print "getting first degree"
        save_user_data_to_file(api, int(data))      # save seed to file
    elif 'save_next_gen_ids' in choice:
        save_next_degree_ids_to_file()
    elif 'process_next_gen' in choice:              # can re-run many times
        with open('user_ids', 'r') as user_ids_file:
            content = user_ids_file.readlines()
        ids = []
        for line in content:
            ids.append(int(line.rstrip()))
        explore_array_of_users_querrying_api(api, ids)


def main(argv):
    api = sign_in_to_twitter_and_get_api()
    print_expiration_status(api)

    if not os.path.isdir('json'):
        os.mkdir('json')
    os.chdir('json')

    print "creating seed json file"
    process_request(api, "start_fresh", "15469556")
    print "saving next degree of seperation's ids"
    process_request(api, "save_next_gen_ids")
    print "processing next generation"
    process_request(api, "process_next_gen")

    os.chdir('../')  # setting state back to how it started


if __name__ == "__main__":
    main(sys.argv)



