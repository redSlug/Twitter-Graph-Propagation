__author__ = 'brandy'


import json, os


def predict_score(user_id, predict_based_on):
    with open('json/' + str(user_id) + '.json') as json_file:
        this_user_dict = json.loads(json_file.readline())

    with open('user_id_score_vector_dict.json') as json_file:
        all_users_scores_dict = json.loads(json_file.readline())
    if user_id not in all_users_scores_dict:
        return 50, 50, 0
    actual_score = all_users_scores_dict[str(user_id)][-1]

    scores_sum = 0
    if not predict_based_on in this_user_dict:
        return 50, actual_score, 0          # data was not public. can make no assessment based on this criteria

    friend_count = len(this_user_dict[predict_based_on])
    count = 0
    for friend in this_user_dict[predict_based_on]:
        if str(friend) in all_users_scores_dict:
            count += 1
            scores_sum += all_users_scores_dict[str(friend)][-1]
    if count == 0:
        return 50, actual_score, 0

    predicted_score = scores_sum / float(count)
    return predicted_score, actual_score, count / float(friend_count)


def predict_all_scores(predict_based_on):
    correctCount = 0
    predictedCount = 0
    for file_name in os.listdir('json'):  # grabbing all ids from json files from current directory
        if file_name.endswith(".json"):
            predicted_score, actual_score, confidence = predict_score(file_name[:-5], predict_based_on)
        if confidence > .9 and actual_score != 50 and predicted_score != 50:
            #print "predicted: %f\t\tactual: %d\t\tconfidence: %f" % (predicted_score, actual_score, confidence)
            if (predicted_score < 50 and actual_score < 50) or (predicted_score > 50 and actual_score > 50):
                correctCount += 1
            predictedCount += 1
    prediction_accuracy = correctCount / float(predictedCount)
    return prediction_accuracy


#predict_score(26589987)
print predict_all_scores("friends_ids")
print predict_all_scores("followers_ids")