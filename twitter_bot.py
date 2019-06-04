import tweepy
import sys
import re
import jsonpickle

#In order to have access to Twitter data it is necessary to create an app that interacts with the Twitter API.
#Info at: http://apps.twitter.com
#You will receive a consumer key and a consumer secret. 
#From the configuration page of your app, you can also require an access token and an access token secret.
#They provide the application access to Twitter on behalf of your account.

consumer_key = 'Insert the consumer_key'
consumer_secret = 'Insert the consumer_secret'
access_token = 'Insert the access_token'
access_secret = 'Insert the access_secret'

bad_word_list = ["word1", "word2"]
target_words_list1 = ["word3", "word4"]
target_words_list2 = ["word5", "word6"]
target_words_list3 = ["word7", "word8"]
target_words_list4 = ["target word"]


answer_phrase = "mind your language!"

phrase1 = "This video is for you, click on the link..."
phrase2 = "It is just a matter of freedom, it is not your choise!"
phrase3 = "Does it bother you?"
phrase4 = "I chatch you!"

def content_analyser(text, target_list): #This function is used to look for words of interest in a given string list
    count = 0
    tokens = text.split()

    for target in target_list:
        keyword = re.compile(target, re.IGNORECASE)
        
        for index in range( len(tokens) ):
            if keyword.match( tokens[index] ):
                count+=1
    return count
		   		   
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

this_user = api.me()
print("The replying tweets on the", this_user.screen_name, "'s timeline are going to be checked...")
print(" ")

path = "log.dat"
replied_id_file = open(path, "r")

#print("id tweets it has been already answered to")
check = replied_id_file.read().split()

#check the time line
public_tweets = api.user_timeline(this_user.screen_name)

for tweet in public_tweets:
	if tweet.id_str in check:
		print("This tweet has been already answered to")
		pass
	
	elif tweet.in_reply_to_screen_name == this_user.screen_name: #check whether the Tweet is a reply to this account or not
		print("New tweet on the timeline!!!!!!!!!")
		b = content_analyser(tweet.text, bad_word_list)
		if b >= 1:
			print("\n", "***** Bad language! *****", "\n", "Id code: ", tweet.user.id, "\n", "User name: ", tweet.user.screen_name, "\n", "text: ", tweet.text, "\n")
			api.update_status("@" + tweet.user.screen_name + " " + answer_phrase, in_reply_to_status_id = tweet.id)
			print("Replied with " + answer_phrase)
			replied_id_tweets = open(path,"a")
			replied_id_tweets.write(tweet.id_str + "\n")
	else:
		#print(tweet.text + "\n")
		continue

print("no more replies to be checked")
print(" ")
print("*** Phase number 2 ***") ###################################################################################
print(" ")
print("Tweets on the following hashtags are going to be checked: ")
print(" ")

list_of_hashtags = {
				0:"#Python",
				1:"#MachineLearing"
				}

for key, value in list_of_hashtags.items():
	print(value)
print(" ")

hashtag_count = 0
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1
tweetCount = 0
TotTweetCount = 0

print("Downloading max {0} tweets".format(maxTweets))
print(" ")

while hashtag_count < len(list_of_hashtags):
	searchQuery = list_of_hashtags[hashtag_count] # this is what we're searching for
	print("Downloading tweets on {0}".format(searchQuery))
	# We'll store the tweets in a text file.
	fName = searchQuery + '.txt' 
	with open(fName, 'w') as f:
		while tweetCount < maxTweets:
			try:
				if (max_id <= 0):
					if (not sinceId):
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended')
					else:
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended', 
											since_id=sinceId) #Returns results with an ID greater than (that is, more recent than) the specified ID.
				else:
					if (not sinceId):
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended',
                                            max_id=str(max_id - 1)) #Returns results with an ID less than (that is, older than) or equal to the specified ID.
					else:
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended',
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
				if not new_tweets:
					print(" ")
					print("No more tweets found on this hashtag")
					break
						
				for tweet in new_tweets:
					if tweet.id_str in check:
						print("è nella lista!")
						pass
					elif 'RT' in tweet.full_text:
						pass
					else:				
						b = content_analyser(tweet.full_text, bad_word_list)
						s = content_analyser(tweet.full_text, target_words_list1)
						r = content_analyser(tweet.full_text, target_words_list2)
						h = content_analyser(tweet.full_text, target_words_list3)
						t = content_analyser(tweet.full_text, target_words_list4)

						score = 0
						score_s = 0
						score_r = 0
						score_h = 0
						score_t = 0
					
						if s >= 1 and b >= 1:
							print("\n", "***** Sexist language! *****", "\n", "Id code: ", tweet.user.id,
							"\n", "Username: ", tweet.user.screen_name, "\n", "text: ", tweet.full_text, "\n")
							api.update_status("@" + tweet.user.screen_name + " " + phrase1, in_reply_to_status_id = tweet.id) 
							print("Replied with " + phrase_s)
							score_s = 1
							
						elif r >= 1 and b >= 1:
							print("\n", "***** Racist language! *****", "\n", "Id code: ", tweet.user.id, 
								"\n", "Username: ", tweet.user.screen_name, "\n", "text: ", tweet.full_text, "\n")
							api.update_status("@" + tweet.user.screen_name + " " + phrase2, in_reply_to_status_id = tweet.id)
							print("Replied with " + phrase_r)
							score_r = 1
							
						elif h >= 1 and b >= 1:
							print("\n", "***** Homophobic language! *****", "\n", "Id code: ", tweet.user.id, "\n",
									"Username: ", tweet.user.screen_name, "\n", "text: ", tweet.full_text, "\n")
							api.update_status("@" + tweet.user.screen_name + " " + phrase3, in_reply_to_status_id = tweet.id)
							print("Replied with " + phrase_h)
							score_h = 1
							
						elif t >= 1 and b >= 1:
							print("\n", "***** Hate speach! *****", "\n", "Id code: ", tweet.user.id, "\n", 
									"Username: ", tweet.user.screen_name, "\n", "text: ", tweet.full_text, "\n")
							api.update_status("@" + tweet.user.screen_name + " " + phrase4, in_reply_to_status_id = tweet.id)
							print("Replied with " + phrase_t)
							score_t = 1
							
						elif b >= 1:
							print("\n", "***** Rough language! *****", "\n", "Id code: ", tweet.user.id, "\n", 
							"Username: ", tweet.user.screen_name, "\n", "text: ", tweet.full_text, "\n")
						else:
							continue
							
						score = score_s + score_r + score_h + score_t
						if score >= 1:
							replied_id_tweets = open(path,"a")
							replied_id_tweets.write(tweet.id_str + "\n")
							f.write(jsonpickle.encode(tweet._json, unpicklable=False)+ "\n")
						
				tweetCount += len(new_tweets)
				print("Checked {0} tweets".format(tweetCount))
				max_id = new_tweets[-1].id
			except tweepy.TweepError as e:
            # Just exit if any error
				print("some error : " + str(e))
				break
	print("Checked {0} tweets, replied/target tweets saved to {1}".format(tweetCount, fName))
	print(" ")
	TotTweetCount += tweetCount
	tweetCount = 0
	max_id = -1
	hashtag_count+=1
print("Downloaded {0} tweets in total".format(TotTweetCount))

