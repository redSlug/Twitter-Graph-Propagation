Download Twitter Data
=====================

This command line tool downloads twitter data including tweets, friends, followers for your twitter network.
Starting with a 'seed' id, this tool can download data from thousands of people in your network (or more if you're patient).
The rate of saving data is one user per minute (every 15 minutes) in accordance with the Twitter api limits, so you may need to leave this
tool running for a long time depending on how much data you want. Data for each user is saved in a separate json file. 
A user_ids file is used to keep track of the next set of users you want to gather information for

- If you plan to grab data for more than just a few users, make sure to prevent your machine from sleeping in your energy settings,
or find another way to keep the network connection alive.

- Make sure you have tweepy installed

- Before you run this tool, make sure to create/populate a file named 'secret' in the root directory with your authentication keys from twitter (one per line): 
CONSUMER_KEY
CONSUMER_SECRET
ACCESS_KEY
ACCESS_SECRET 

Once you've completed these steps, run python main.py

positive words: http://positivewordsresearch.com/list-of-positive-words/
http://boostblogtraffic.com/power-words/
http://www.slate.com/blogs/lexicon_valley/2013/09/11/top_swear_words_most_popular_curse_words_on_facebook.html

negative words:
https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/negative-words.txt
; If you use this list, please cite one of the following two papers:
;
;   Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
;       Proceedings of the ACM SIGKDD International Conference on Knowledge 
;       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
;       Washington, USA, 
;   Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
;       and Comparing Opinions on the Web." Proceedings of the 14th 
;       International World Wide Web conference (WWW-2005), May 10-14, 
;       2005, Chiba, Japan.
