#Imports
import idsecrets
import xml.etree.ElementTree as ET
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
import asyncio
import time

def gen_title():
    #Import XML File
    tree = ET.parse(r"C:\Users\waffl\AppData\Roaming\StardewValley\Saves\Clickbait_366212092\SaveGameInfo")
    root = tree.getroot()

    #Setup XML Attribute Names
    day = 'dayOfMonthForSaveGame'
    season = 'seasonForSaveGame'
    year = 'yearForSaveGame'

    #Vars
    current_day_val = None
    current_season_val = None
    current_year_val = None

    #Season Dictionary
    seasons = {
        '0' : 'Spring',
        '1' : 'Summer',
        '2' : 'Fall',
        '3' : 'Winter'
    }

    #Search Element Tree for Data
    for child in root:
        if child.tag == day:
            current_day_val = child.text
        elif child.tag == season:
            current_season_val = child.text
        elif child.tag == year:
            current_year_val = child.text

    if current_day_val == '29':
        current_day_val = '1'
        if current_season_val == '3':
            current_season_val = '0'
            current_year_val = str(int(current_year_val) + 1) 
        else:
            current_season_val = str(int(current_season_val) + 1)

    TITLE_STRING = f'{seasons[current_season_val]} {current_day_val} - Year {current_year_val} | Stardew Valley Expanded Mod | !sdv'
    #print(TITLE_STRING)

    return TITLE_STRING


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

#Auth with Twitch
print('Authing...')
twitch = asyncio.run(auth())
print(f'Auth Complete...')
#Main Loop
while True:
    now = time.time()

    unixid = 'id-' + str(now)[-5:]

    if int(now) % 60 == 0:
        print(f'Getting Title String')
        title = gen_title()
        titleid = f'{title} | {unixid}'
        print(f'Title = {titleid}')
        asyncio.run(set_title(twitch, titleid)) 
        print(f'Title Set Complete')
    time.sleep(1)
