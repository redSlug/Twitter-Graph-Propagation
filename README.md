Twitter Trust Propogation
=========================

Makes predictions of trustworthiness of people in your network based on who their connections are.
Downloads timelines and connections, and saves each user's data to a separate json file. 
Assigns a score to each user based on vocabulary, re-tweets, and favorited tweets. Predicts score 
based on 'friends_ids' with a 70 percent accuracy using my network.

### Setup:

- If you plan to grab data for more than just a few users, make sure to prevent your machine from sleeping in your energy settings,
or find another way to keep the network connection alive.
- Make sure you have tweepy installed
- Before you run this tool, make sure to create/populate a file named 'secret' in the root directory with your authentication keys from twitter: 
    - CONSUMER_KEY
    - CONSUMER_SECRET
    - ACCESS_KEY
    - ACCESS_SECRET 

### Execution:

1. `python download_data.py` (leave this running until you have downloaded enough data)
2. `python generate_user_scores_dict` (check out the histogram of user scores)
3. `python predict_scores.py` (check out how the predicted scores compare to the actual)

### Sources:

##### positive words: 
- http://positivewordsresearch.com/list-of-positive-words/
- http://boostblogtraffic.com/power-words/
- Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing and Comparing Opinions on the Web."

#####negative words:
- https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/negative-words.txt
- http://www.slate.com/blogs/lexicon_valley/2013/09/11/top_swear_words_most_popular_curse_words_on_facebook.html

