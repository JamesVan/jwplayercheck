import datetime
import jwplatform
import logging
import time
import os
import sys
import pprint
from keys import JWPLAYER_FC_KEY, JWPLAYER_FC_SECRET

# ### Input of date range to today
# user_input = input("How many days ago do you want to pull data for? Please enter a number: ")
# days_ago = int(user_input)

# ### For EasternTimeZone
# tzoffset = -14400
# dt = datetime.date.today() - datetime.timedelta(days=days_ago)
# start_date = int(time.mktime(dt.timetuple())) + tzoffset

### Setting up FC JWplayer client
jwplatform_client = jwplatform.Client(JWPLAYER_FC_KEY, JWPLAYER_FC_SECRET)


### Function for querying Video List, 
def video_lister(result_limit=1000,start_date=1539129600):
    timeout_in_seconds = 2
    max_retries = 3
    retries = 0
    offset = 0
    videos = list()

    logging.info("Querying for video list.")
    while True:
        try:
            response = jwplatform_client.videos.list(result_limit=result_limit,
                                                        result_offset=offset,
                                                        order_by="date:desc")
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
        # except Exception as inst:
        #     print(type(inst))
        #     print(inst.args)
        #     print(inst)
        
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
# json_obj = video_lister(1)
# pp = pprint.PrettyPrinter(width=41, compact= True)
# pp.pprint(json_obj)
def print_video_ids_missing_keys(result_limit=1000):
    video_list = video_lister(result_limit=result_limit)
    missing_series = []
    missing_category = []
    for video in video_list:
        if 'custom' in video:
            if 'series' not in video['custom'] and 'category' not in video['custom']: 
                print(f"Video key = {video['key']} is missing both category and series")
                missing_series.append(video['key'])
                missing_category.append(video['key'])
                ### Add click to apply function
            elif 'series' not in video['custom']:
                print(f"Video key = {video['key']} is missing SERIES custom parameter")
                missing_series.append(video['key'])
                ### Add click to apply functionif  
            elif 'category' not in video['custom']:
                print(f"Video key = {video['key']} is missing the CATEGORY custom parameter")
                missing_category.append(video['key'])
            # else:
            #     print(f"Video ID = {video['key']} made {video['date']}is CATEGORY: {video['custom']['category']} and SERIES: {video['custom']['series']}")
            #     ### Add click to apply function
    return missing_category, missing_series

print_video_ids_missing_keys(result_limit=100)



