import requests,urllib,re,pylab
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from wordcloud import WordCloud,STOPWORDS
from token_key import APP_ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'
##############instabot 1.0###############
#function to get ur info(username,followers,following etc..
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'
#####################################################

#to get the id of user from the username
def get_user_id(insta_username):
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s" % (insta_username, APP_ACCESS_TOKEN))
    print"Get Request Url : %s"%(request_url)
    user_info=requests.get(request_url).json()
    if user_info["meta"]["code"]==200:
        if len(user_info["data"]):
            #to return the first search user.
            return user_info["data"][0]["id"]
        else:
            return None
    else:
        print"Status other than 200 received !!!!!"
#to get details of a user
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User does not exist!"
        exit()
    request_url = (BASE_URL + "users/%s?access_token=%s") % (user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "Username: %s" % (user_info['data']['username'])
            print "No. of followers: %s" % (user_info['data']['counts']['followed_by'])
            print "No. of people you are following: %s" % (user_info['data']['counts']['follows'])
            print "No. of posts: %s" % (user_info['data']['counts']['media'])
        else:
            print "There is no data for this user!"
    else:
        print "Status code other than 200 received!"
####################################################
        #to get your own recent post
def get_own_post():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    own_media = requests.get(request_url).json()
    if own_media["meta"]["code"] == 200:
        if len(own_media["data"]):
            image_name = own_media["data"][0]["id"] + ".jpeg"
            print "image id : %s"%(own_media["data"][0]["id"])
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received!"
###############################################################3
#to get one's recent post
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            print "POST ID : %s" + (user_media['data'][0]['id'])
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
        ##################################################3
#function to get post id of recent post of user
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()
        ##################################################3
#to post a like on recent post of a user
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

#########################################################
#function to get post id of own recent post
def get_own_post_id():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            return own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
#######################################################

#function to post a comment on recent post of a user
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    if len(comment_text) <= 300 and comment_text.isupper()==False and comment_text.count("#")<=4:
        c = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',comment_text)
        if len(c) <= 1:
            payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print "Successfully added a new comment!"
            else:
                print "Unable to add comment. Try again!"

        else:
            print "Comment cannot be posted as it is not appropriate"

    else:
        print "Comment cannot be posted as it is not appropriate"

        ######################################################

#to post comments info on friends recent post
def comment_info(insta_username):
    get_user_id(insta_username)
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info1 = requests.get(request_url).json()
    if comment_info1['meta']['code'] == 200:
        if len(comment_info1):
            a=0
            for a in range(0, len(comment_info1["data"])):
                print "%s commented : %s"%(comment_info1["data"][a]["from"]["username"],comment_info1["data"][a]["text"])
                a=a+1
        else:
            print "no data"
    else:
        print"code not 200"
        #######################################################
#get comments of own recent post
def own_comment_info():
    media_id = get_own_post_id()
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info1 = requests.get(request_url).json()
    if comment_info1['meta']['code'] == 200:
        if len(comment_info1):
            a = 0
            for a in range(0,len(comment_info1["data"])):
                print "%s commented : %s" % (comment_info1["data"][a]["from"]["username"], comment_info1["data"][a]["text"])
                a = a + 1
        else:
            print "no data"
    else:
        print"code not 200"

#to delete negative comments on post
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'
        
#################################################################

#to compare the comments on own recent post & plot a pie chart of same
def compare_comments():
    media_id = get_own_post_id()
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    negative = 0
    positive = 0

    if comment_info['meta']['code'] == 200 and len(comment_info['data']):
    # Plot
        for x in range(0, len(comment_info['data'])):
            comment_id = comment_info['data'][x]['id']
            comment_text = comment_info['data'][x]['text']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                print "Negative comment : %s by %s\n" % (comment_text,comment_info["data"][x]["from"]["username"])
                negative=negative+1
            else:
                print "Positive comment : %s by %s\n" % (comment_text,comment_info["data"][x]["from"]["username"])
                positive=positive+1
        print"GOOD comments :) : %s"%(positive)
        print"BAD comments :( : %s"%(negative)
        labels = "Positive Comments", "Negative Comments"
        numbers = [positive, negative]
        colors = ['blue', 'red']
        explode = (0.1, 0) 
        plt.pie(numbers, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.show()
        ##################################################################
#objective 1:
#To target a particular tag & comment an appropriate comment of your choice to the meadia of that tag
def post_a_targetted_comment(media_id):
    comment_text =raw_input("Enter the comment you want to post? \n")
    if len(comment_text) <= 300 and comment_text.isupper()==False and comment_text.count("#")<=4:
        c = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',comment_text)
        if len(c) <= 1:
            payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print "Successfully added a new comment!"
            else:
                print "Unable to add comment. Try again!"

        else:
            print "Comment cannot be posted as it is not appropriate"

    else:
        print "Comment cannot be posted as it is not appropriate"

def get_media_of_tag(tag):
    request_url=BASE_URL+ 'tags/%s/media/recent?access_token=%s'%(tag,APP_ACCESS_TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for x in range(0,len(user_media['data'])):
                post_a_targetted_comment(user_media['data'][x]['id'])
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
        
#################################################################

#function to show recently liked media
def recent_media_liked():
    request_url = BASE_URL + "users/self/media/liked?access_token=%s" % (APP_ACCESS_TOKEN)
    recently_liked_media=requests.get(request_url).json()
    if recently_liked_media["meta"]["code"] == 200:
        if len(recently_liked_media["data"]):
            image_name = recently_liked_media["data"][0]["id"] + ".jpeg"
            image_url = recently_liked_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "User does not exist!"
    else:
        print "Status code other than 200 received!"
        #########################################################################
#function to download the posts of user or self
def download_recent_posts():
    a=True
    while a==True:
        print "\n"
        print "a.Download own  posts"
        print "b. Download other user's post"
        choice = raw_input("enter the choice:")

        if choice=="a":
            request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
            print 'GET request url : %s' % (request_url)
            own_media = requests.get(request_url).json()

            if own_media['meta']['code'] == 200:
                if len(own_media['data']):
                    x=0
                    for x in range(0,len(own_media["data"])):
                        image_name = own_media['data'][x]['id'] + '.jpeg'
                        image_url = own_media['data'][x]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                    print 'Your images have been downloaded!'
                else:
                    print 'Post does not exist!'
            else:
                print 'Status code other than 200 received!'
            a=False


        elif choice=="b":
            insta_username=raw_input("Enter the username :")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in Instagram !!"
            else:
                user_id = get_user_id(insta_username)
                if user_id == None:
                    print 'User does not exist!'
                    exit()
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()

                if user_media['meta']['code'] == 200:
                    if len(user_media['data']):
                        x = 0
                        for x in range(0, len(user_media["data"])):
                            image_name = user_media['data'][x]['id'] + '.jpeg'
                            image_url = user_media['data'][x]['images']['standard_resolution']['url']
                            urllib.urlretrieve(image_url, image_name)
                        print 'Your images have been downloaded!'
                    else:
                        print 'Post does not exist!'
                else:
                    print 'Status code other than 200 received!'
            a=False
        else:
            print "Wrong Choice"
            a = False
###############################################################################
#function to find subtrends of a post
def find_subtrends(tag):
    request_url=BASE_URL+ "tags/%s/media/recent?access_token=%s"%(tag,APP_ACCESS_TOKEN)

    hash_items = {}
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for x in range(0, len(user_media['data'])):
                for y in range(0, len(user_media['data'][x]['tags'])):

                    if user_media['data'][x]['tags'][y] in hash_items:
                        hash_items[user_media['data'][x]['tags'][y]] += 1
                    else:
                        hash_items[user_media['data'][x]['tags'][y]] = 1
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    hash_items.pop(tag)
    print hash_items
    pylab.figure()

    x = range(len(hash_items))
    pylab.xticks(x, hash_items.keys())
    pylab.plot(x, hash_items.values(), "g")
    pylab.show()
    wordcloud = WordCloud(font_path=r"C:\Windows\Fonts\FREESCPT.TTF",
                      stopwords=STOPWORDS,
                      background_color="white",
                      width=1200,
                      height=1000,
                      ).generate_from_frequencies(hash_items)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
############################end of objective :>##################################
#Function to cleck climate and return if any natural disaster#
def climate_check(latitude, longitude):
    url = (BASE_URL + "locations/search?lat=%s&lng=%s&access_token=%s") % (latitude, longitude, ACCESS_TOKEN)
    location_info = requests.get(url).json()
    if location_info['meta']['code'] == 200:

        location_id = [location_info["data"][x]["id"] for x in range(0, len(location_info["data"]))]

        media_list = []

        for i in range(0, len(location_id)):
            request_url = (BASE_URL + "locations/%s/media/recent?access_token=%s") % (location_id[i], ACCESS_TOKEN)
            media_request = requests.get(request_url).json()
            if media_request["meta"]["code"] == 200:
                media_list.append(media_request["data"])
            else:
                print "Code other than 200"
                exit()

        media_info = [media_list[y] for y in range(0, len(media_list))]

        caption = [media_info[j][e]["caption"]["text"] for j in range(0, len(media_info)) if len(media_info[j]) > 0 for
                   e in range(0, len(media_info[j]))]
        for m in range(0, len(caption)):
            print ">> %s " % caption[m]
        if len(caption):
            print "***Images with these captions found!***"
        else:
            print "***Woops!No images in this area***"

        calamities = ["Avalanche", "Cloudburst", "cloudburst", "Earthquake", "earthquake","avalanche", "Landslide", "Landslide", "Hailstorm", "hailstorm", "Heatwave",
                      "heatwave",  "Flood", "flood", "Cyclone","cyclone", "Tsunami", "tsunami", "Drought", "drought", "Thunderstorm", "thunderstorm", "Blizzard",
                      "blizzard", "Volcano", "volcano"]
        check = False

        for k in range(0, len(caption)):
            for l in range(0, len(calamities)):
                if calamities[l] in caption[k]:
                    check = True
                    break
            if check:
                print "This caption :%s ->  denotes the calamity : %s" % (caption[k], calamities[l])
            else:
                print "This caption :%s ->  denotes no calamity" % (caption[k])
    else:
        print "Something went wrong!"

        ###########################################################################

def start_bot():
    while True:
        print "\n"
        print "Hey! Welcome to instaBot!"
        print "Choose from following  options:"
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.get your recent pic downloaded \n"
        print "d.get recent pic of a username\n"
        print "e. like recent media of a username \n"
        print "f. comment on recent media of user\n"
        print "g. view comments on own recent post \n"
        print "h. view comments on user's recent post \n"
        print "i. delete bad comments on the picture \n"
        print "j. compare the comments on own recent post an creat a pie chart of the same\n"
        print "k. Target a particular tag and comment a appropriate comment of ur wish to the media of that tag\n"
        print "l. Download the recent media you just liked \n"
        print "m. Download the recent media of anyone \n"
        print "n. to find and plot subtrends of a trend \n"
        print "o. Calamity analysis between any latitudes \n"
        print "p.Exit"

        choice=raw_input("Enter you choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in instagram!!!"
            else:
                get_user_info(insta_username)
        elif choice=="c":
            get_own_post()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in instagram!!!"
            else:
                get_user_post(insta_username)
        elif choice=="e":
            insta_username=raw_input("enter username of the user :")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in instagram!!!"
            else:
                like_a_post(insta_username)
        elif choice=="f":
            insta_username=raw_input("enter the username of the user")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in instagram!!!"
            else:
                post_a_comment(insta_username)
        elif choice == "g":
            own_comment_info()
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in instagram!!!"
            else:
                comment_info(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in instagram!!!"
            else:
                delete_negative_comment(insta_username)
        elif choice=="j":
            compare_comments()
        elif choice=="k":
            tag_name=raw_input("enter the tag you want to search? \n")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Username not valid in instagram!!!"
            else:
                get_media_of_tag(tag_name)
        elif choice=="l":
            recent_media_liked()
        elif choice=="m":
            download_recent_posts()
        elif choice=="n":
            trend = raw_input("Enter trend to be searched : ")
            find_subtrends(trend)
        elif choice == 'o':
            latitude = raw_input("enter the georgraphical latitude coordinate in decimal:")
            longitude = raw_input("enter the georgraphical longitude coordinate in decimal:")
            climate_check(latitude, longitude)
        elif choice=="p":
            exit()

        else:
            print "wrong choice"

start_bot()
########End of instabot########
