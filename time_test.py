import datetime
import jwplatform
import logging
import time
import os
import sys


user_input = input("How many days ago do you want to pull data for? Please enter a number: ")
days_ago = int(user_input)

tzoffset = -14400
dt = datetime.date.today() - datetime.timedelta(days=days_ago)
start_date = int(time.mktime(dt.timetuple())) + tzoffset


# dt = datetime.date.today() - datetime.timedelta(days=days_ago)
# # start_date = int(time.mktime(dt.timetuple(),tzinfo = datetime.timezone.utc))
# print(dt)
# sdt = str(dt)
# structtime = time.strptime(sdt,"%Y-%m-%d")
# print(structtime)
# final = time.gmtime(structtime)
# print(final)