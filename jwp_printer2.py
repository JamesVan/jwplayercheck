# Steps:
# Set Date Range
import datetime
import jwplatform
import logging
import time
import os
import sys
import moment
import json
from keys import JWPLAYER_FC_KEY, JWPLAYER_FC_SECRET

days_ago = 8

# offset = time.time() - mktime()
# dt = datetime.date.today() - datetime.timedelta(days=days_ago)
# start_date = int(time.mktime(dt.timetuple(,tzinfo = dateime.timezone.utc)))

start_date = 1539993600


# Set Key params to look for and defualts
defualt_parms = {
    'category':'misc',
    'series' : 'video'
}
paramsToCheck = [ 'category', 'series']

# Establish Client Connection
jwplatform_client = jwplatform.Client( JWPLAYER_FC_KEY, JWPLAYER_FC_SECRET)

# Request all videos published within date Range
def list_videos_missing_params(result_limit=1000):
    timeout_in_seconds = 2
    max_retries = 3
    retries = 0
    offset = 0
    videos = list()

    logging.info("Querying for video list.")
    while True:
        try:
            response = jwplatform_client.videos.list(result_limit=result_limit,
                                                        result_offset=offset)
        except jwplatform.errors.JWPlatformRateLimitExceededError:
            logging.error("Encountered rate limiting error. Backing off on request time.")
            if retries == max_retries:
                raise jwplatform.errors.JWPlatformRateLimitExceededError()
            timeout_in_seconds *= timeout_in_seconds  # Exponential back off for timeout in seconds. 2->4->8->etc.etc.
            retries += 1
            time.sleep(timeout_in_seconds)
            continue
        except jwplatform.errors.JWPlatformError as e:
            logging.error("Encountered an error querying for videos list.\n{}".format(e))
            raise e
        
        # Reset retry flow-control variables upon a non successful query (AKA not rate limited)
        retries = 0
        timeout_in_seconds = 2

        # Add all fetched video objects to our videos list.
        next_videos = response.get('videos', [])
        last_query_total = response.get('total', 0)
        videos.extend(next_videos)
        offset += len(next_videos)
        logging.info("Accumulated {} videos.".format(offset))
        if offset >= last_query_total:  # Condition which defines you've reached the end of the library
            break
        return(videos)
    # desired_fields = ['key', 'title', 'description', 'tags', 'date', 'link', 'custom']


tester = list_videos_missing_params()

def print_video_ids_missing_keys(result_limit=1000):
    video_list = list_videos_missing_params(result_limit=result_limit)
    for each in video_list:
        if each['custom']['series'] is None and each['custom']['category'] is None:
            print(f"Video {each['title']} (key = {each['key']}) is missing both category and series")
            ### Add click to apply function
        elif each['custom']['series'] is None:
            print(f"Video {each['title']} (key = {each['key']}) is missing SERIES custom parameter")
            ### Add click to apply functionif  
        elif each['custom']['category'] is None:
            print(f"Video {each['title']} (key = {each['key']}) is missing the CATEGORY custom parameter")
            ### Add click to apply function


print_video_ids_missing_keys(5)
# Check each video in date range for key params, 
# add where missing