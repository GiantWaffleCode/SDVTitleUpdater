#Imports
import idsecrets
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
import asyncio
import time
from datetime import datetime

#?Maybe use Gradio for this aswell

def get_time_delta():
    current_time = datetime.now()
    stream_start_time = datetime.strptime("07/02/24 07:00", "%d/%m/%y %H:%M")

    #print('Current Time:', current_time.time())
    #print('Stream Start Time:', stream_start_time.time())

    delta_time = stream_start_time - current_time
    time_left_seconds = delta_time.total_seconds()

    time_left_minutes = round((time_left_seconds / 60) % 60)

    time_left_hours = round(time_left_seconds / 3600)
    #print(f'Hrs:{time_left_hours} Mins:{time_left_minutes}')

    return time_left_hours, time_left_minutes

def gen_title():
    hrs, mins = get_time_delta()
    if mins != 60:
        TITLE_STRING = f"Live in {hrs} hours and {mins} minutes. Unless I'm late..."
    else:
        TITLE_STRING = f"Live in {hrs} hours. Unless I'm late..."

    #print(TITLE_STRING)

    return TITLE_STRING

#Auth System
async def auth():
    #Import Secrets
    app_id = idsecrets.id
    app_secret = idsecrets.secret
    
    twitch = await Twitch(app_id, app_secret)
    target_scope = [AuthScope.CHANNEL_MANAGE_BROADCAST]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    # this will open your default browser and prompt you with the twitch verification website
    token, refresh_token = await auth.authenticate()
    # add User authentication
    await twitch.set_user_authentication(token, target_scope, refresh_token)
    return twitch


#Function to Set Title
async def set_title(twitch, TITLE_STRING):
    channel_id = idsecrets.channel
    #Set Title
    await twitch.modify_channel_information(channel_id, title=TITLE_STRING)



#Main Loop

#Auth with Twitch
print('Authing...')
twitch = asyncio.run(auth())
print(f'Auth Complete...')

while True:
    now = time.time()
    #Every 60 seconds run this loop
    if int(now) % 60 == 0:
        print(f'Getting Title String')
        title = gen_title()
        print(f'Title = {title}')
        asyncio.run(set_title(twitch, title)) 
        print(f'Title Set Complete')
    time.sleep(1)