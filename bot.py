
import tweepy, subprocess

time_inverval = 24 # length in hours
upload_threshold = 100.0  # speed in Mbps
download_threshold = 100.0 # speed in Mbps
service_providers_twitter_handle = "@dummyServiceProvider"
tweet_upload_speed = False
tweet_download_speed = False


# enter the corresponding information from your Twitter application:
CONSUMER_KEY = ''  # keep the quotes, replace this with your consumer key
CONSUMER_SECRET = ''  # keep the quotes, replace this with your consumer secret key
ACCESS_KEY = ''  # keep the quotes, replace this with your access token
ACCESS_SECRET = ''  # keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


#run speedtest and return download and upload speed
def runspeedtest():
    # run speed test and get output
    proc = subprocess.Popen('speedtest-cli', stdout=subprocess.PIPE)
    resultinbytes = proc.stdout.read()

    # convert result fromm bytes to string
    result = resultinbytes.decode("utf-8")

    # parse output for upload and download speeds
    dspeed = result[result.index("Download: ") + 10: result.index("Download: ") + 15]
    uspeed = result[result.index("Upload: ") + 8: result.index("Upload: ") + 13]
    return dspeed, uspeed



downloadspeed, uploadspeed = runspeedtest()

print("Download: " + downloadspeed)
print("Upload: " + uploadspeed)

if float(uploadspeed) < upload_threshold:
    tweet_upload_speed = True
    print("\nUpload speed does not meet threshold values of " + str(upload_threshold))

if float(downloadspeed) < download_threshold:
    tweet_download_speed = True
    print("Download speed does not meet threshold values of " + str(download_threshold))




if tweet_upload_speed and tweet_download_speed:
    api.update_status(service_providers_twitter_handle + " I'm paying for a download speed of " + str(download_threshold) + " Mbps and an upload speed of " + str(upload_threshold)
                      + " Mbps but only getting a download speed of " + str(downloadspeed) + " Mbps and an upload speed of " + uploadspeed + " Mbps")

elif tweet_download_speed:
    api.update_status(service_providers_twitter_handle + " Why am I paying for a download speed of " + str(download_threshold) + " Mbps but only getting " + str(downloadspeed) + " Mbps")

elif tweet_upload_speed:
    api.update_status(service_providers_twitter_handle + " Why am I paying for an upload speed of " + str(upload_threshold) + " Mbps but only getting " + str(uploadspeed) + " Mbps")
