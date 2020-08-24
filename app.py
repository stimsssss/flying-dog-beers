#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 13:37:10 2020

@author: pi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 17:00:06 2020

@author: pi
"""

"""
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.server.run(port=8000, host='127.0.0.1')

# -*- coding: utf-8 -*-
    """
"""
Created on Sun Jul 12 12:27:33 2020

@author: e142133
"""
#!pip install chart_studio

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from pandas import DataFrame, read_excel
from pandas import ExcelWriter
import requests
import time
from bs4 import BeautifulSoup
import base64
import json
#from secrets import *
#import json
import ast
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.renderers.default='browser'
import datetime
import re
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import chart_studio
import chart_studio.plotly as py
import numpy as np

"""
ADD TIMESTAMP TO GEOGRAPHIC LISTENERS AND APPEND ALL
add change over time sliders
set to run at a certain time
set map bubbles to a certain color depending on amount of listeners increase in period
"""

timestamp = datetime.datetime.now()
weekday = (datetime.datetime.today().weekday()) #4 = Friday
print(timestamp)

from datetime import datetime

#-------FILES FILES FILES -----------------------------------------------------
#os.path.join(base_dir, filename)

base_dir = '/home/pi/Desktop/Python Scripts/Spotify'
all_geo_file = os.path.join(base_dir, 'All Geographic Listeners.xlsx')
all_stats_file = os.path.join(base_dir, 'All General Stats.xlsx')
all_youtube_file = os.path.join(base_dir, 'All Youtube.xlsx')
current_youtube_file = os.path.join(base_dir,'Current Youtube.xlsx')
world_cities_file = os.path.join(base_dir,'worldcities.xlsx')

#--------SPOTIFY API FOR TRACK FEATURES THROUGH SPOTIPY ("SP")---------------------------------
cid = '38a89765637f43dbb7c6cce35637daff'
secret = '9b263812668740268d60c728a3727347'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)

johnny = '00OF0nwYaoBSO3AnPVq3vE'
johnny_uri = 'spotify:artist:00OF0nwYaoBSO3AnPVq3vE'
print("Accessing Spotify...")

#-------Get Track List from Complete Playlist

def getPlaylistTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

ids = getPlaylistTrackIDs('johnny stimson', '1Teioad4fKoVjuSwGQW3P9?si=2zvXvzURTeKRHjAw4t2_zg') # Johnny Complete
ct_songs = len(ids)

#------Get Track Features
#https://unboxed-analytics.com/data-technology/analyzing-drakes-catalog-using-spotifys-api/
print("Getting track features...")

def getTrackFeatures(id):
  meta = sp.track(id)
  features = sp.audio_features(id)
 
  # Meta
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']

  # Features
  acousticness = features[0]['acousticness']
  danceability = features[0]['danceability']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']

  track = [name, album, artist, release_date, length, popularity, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
  return track
 
tracks = []
for i in range(0, ct_songs):
    time.sleep(.5)
    track = getTrackFeatures(ids[i])
    tracks.append(track)
   
johnny_songs = pd.DataFrame(data=tracks,
                          index=None,
                          columns=['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo','time_signature'],
                          dtype=None,
                          copy=False)

print("Visualizing track features...")

johnny_songs_radar = johnny_songs.drop(columns=['name','album','artist','release_date','tempo','time_signature','instrumentalness'])

johnny_songs_radar['length'] = johnny_songs['length']/max(johnny_songs['length'])
johnny_songs_radar['loudness'] = johnny_songs['loudness']/min(johnny_songs['loudness'])
johnny_songs_radar['popularity'] = johnny_songs['popularity']/max(johnny_songs['popularity'])
#johnny_songs = johnny_songs.set_index(['name','album','artist','release_date'])
    #(columns=['tempo','time_signature','instrumentalness'])

johnny_songs_radar.head(5)

categories = ['length', 'popularity', 'acousticness', 'danceability', 'energy', 'liveness', 'loudness', 'speechiness']


radar = go.Figure()

for i in range(ct_songs):
    radar.add_trace(
                go.Scatterpolar(          
                    r=johnny_songs_radar.loc[i].values,
                                #theta=johnny_songs.columns,
                                theta=categories,
                                fill='toself',
                                name=johnny_songs['name'].loc[i],
                                #name="Johnny-%s"%wine.target_names[i],
                                showlegend=True
                                )
                )

radar.update_layout(
    polar=dict(
        radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
            ),
    title="Tracks by Features",
    margin=dict(l=20, r=20, t=40, b=20)
)

#radar.show()

##ADD FILTER AND/OR SLIDER
   
#----------GET ARTIST USING SPOTIFY API-----------------------------------------------
#--Spotify SDK Access Token Using My Client/Secret IDs

print("Getting Spotify artist...")
# Step 1 - Authorization
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"38a89765637f43dbb7c6cce35637daff:9b263812668740268d60c728a3727347"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

# Step 2 - Use Access Token to call ARTIST endpoint

artistUrl = f"https://api.spotify.com/v1/artists/00OF0nwYaoBSO3AnPVq3vE"
headers = {
    "Authorization": "Bearer " + token
}

res = requests.get(url=artistUrl, headers=headers)

artist = json.dumps(res.json(), indent=2) #json
artist = json.loads(artist) #parse
johnny_popularity = (artist['popularity'])
johnny_followers = (artist['followers'])
johnny_followers = johnny_followers['total']


#----------SCRAPE MONTHLY SPOTIFY LISTENERS-----------------------------------------------
print("Scraping monthly listeners...")
user_agent_desktop = 'Chrome/80.0.3987.149 '
headers = { 'User-Agent': user_agent_desktop}
page = requests.get("https://open.spotify.com/artist/00OF0nwYaoBSO3AnPVq3vE", headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())
text2 = soup.get_text()
search_key = "u00B7"
length = len(search_key)
position_of_first_letter_key = text2.find(search_key) #29125
position_of_last_letter_key = position_of_first_letter_key + length
next_comma = position_of_last_letter_key + text2[position_of_last_letter_key:position_of_last_letter_key+50].find("K")
monthly_listeners = text2[position_of_last_letter_key:next_comma] 
monthly_listeners = int(float(monthly_listeners) * 1000)


print("Scraping geographic listeners") #Using a weirdly different process from monthly listeners, bc they're somehow different
page = requests.get("https://open.spotify.com/artist/00OF0nwYaoBSO3AnPVq3vE")
soup = BeautifulSoup(page.content, 'html.parser')


#print(soup.prettify())
text1 = soup.get_text()
"""
search_key = "monthly_listeners"
length = len(search_key)
position_of_first_letter_key = text1.find(search_key) #29125
position_of_last_letter_key = position_of_first_letter_key + length
next_comma = position_of_last_letter_key + text1[position_of_last_letter_key:position_of_last_letter_key+50].find(",")
monthly_listeners = text1[position_of_last_letter_key + 2:next_comma] #+2 for ": in "monthy_listeners": 792854...
"""

#Geographic Spotify listeners
search_key = "cities"
last_separator = "};"
length = len(search_key)
position_of_first_letter_key = text1.find(search_key)
position_of_last_letter_key = position_of_first_letter_key + length
position_of_last_separator = position_of_last_letter_key + text1[position_of_last_letter_key:position_of_last_letter_key+5000].find(last_separator)
geographic_listeners = text1[position_of_last_letter_key + 2:position_of_last_separator-1] #+2 for ": in "monthy_listeners": 792854...
#geographic_listeners = ast.literal_eval(geographic_listeners)
geographic_listeners = json.loads(geographic_listeners)
#geographic_listeners = eval(geographic_listeners)
geographic_listeners = pd.DataFrame(geographic_listeners)
geographic_listeners['country_code'] = geographic_listeners['country']
geographic_listeners['timestamp'] = timestamp

#import WorldCities and merge with geographic listeners
worldCities = pd.read_excel(world_cities_file)
worldCities['country_code'] = worldCities['iso2']
worldCities.head(10)

keys = [
                 "country_code",
                 "city"]
geographic_listeners_lat_long = geographic_listeners.merge(worldCities, on= keys, how='left')
geographic_listeners_lat_long['text'] = geographic_listeners_lat_long['listeners'].astype(str) + (" listeners \n") +  geographic_listeners_lat_long['city'] + ", " + geographic_listeners_lat_long['country_code']

#Combine with historic geographic listeners info
all_geographic_listeners_lat_long = pd.read_excel(all_geo_file)  
all_geographic_listeners_lat_long = all_geographic_listeners_lat_long.append(geographic_listeners_lat_long)

#Drop unnamed columns
drop_cols = [col for col in all_geographic_listeners_lat_long.columns if 'Unnamed' in col]
all_geographic_listeners_lat_long.drop(columns=drop_cols, inplace=True)  
all_geographic_listeners_lat_long.to_excel(all_geo_file)

#starter groupby for later, so you can show emerging change/time bubbles
#pivot2 = all_geographic_listeners_lat_long.groupby(by=["city","timestamp"], dropna=False).sum()
 

#Build Geogarphic map
print("Visualizing geographic audience...")

geographic_map = go.Figure(data=go.Scattergeo(
        lon = geographic_listeners_lat_long['lng'],
        lat = geographic_listeners_lat_long['lat'],
        text = geographic_listeners_lat_long['text'],
        mode = 'markers',
        marker=dict(
            color = 'LightSkyBlue',
            size = geographic_listeners_lat_long['listeners']/500)
            #opacity=0.5)
        #marker_color = df['cnt'],
        ))
#geographic_map.show()
        
geographic_map.update_layout(title="Global Spotify Listeners", margin=dict(l=20, r=20, t=40, b=20))
   
#----------INSTAGRAM-----------------------------------------------------------
#ADD "liked" etc. which is all searchable in the text
print("Scraping Instagram followers...")
page = requests.get("https://www.instagram.com/johnnystimson/")
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)
text = soup.get_text()
length = len(text)

#get followers
foll = "edge_followed_by"
followers_index = int(text.find(foll))  
followers = text[followers_index:followers_index + 100]
followers = followers.split("count\":")
followers = followers[1]
followers = followers.split("}")
followers = followers[0]

#----------YOUTUBE-------------------------------------------------------------
print("Scraping YouTube...")
page = requests.get("https://www.youtube.com/c/johnnystimson/videos")
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)
text = soup.get_text()
text = text.replace(u'—\xa0', u'- ')
length = len(text)

#get subscribers
subsc = "subscribers"
subscribers_index = int(text.find(subsc))  
subscribers = text[subscribers_index - 100:subscribers_index]
subscribers = subscribers.split("\"")
subscribers = subscribers[len(subscribers) - 1]
subscribers = subscribers[:-2]
subscribers = int(float(subscribers)*1000)

#GET VIDEO FEATURES
start_search = "Johnny Stimson -"
end_search = "views"
 
# using re.finditer()
# All occurrences of first substring in string - Johnny
start_key = [i.start() for i in re.finditer(start_search, text)]  
start_key = [int(i) for i in start_key]

#Find ALL occurences of second substring in string (VIEWS)
end_key = [i.start() for i in re.finditer(end_search, text)]
end_key = [int(i) for i in end_key]

#Find NEXT occurence of second substring in string
next_key = []
drop_starts = [] #iterations of "Johnny" for which no "views" follows
for i,val in enumerate(start_key):
    filtered_numbers = [x for x in end_key if x > val]
    while True:
        try:
            next = min(filtered_numbers)
            next_key.append(next)
            break
        except ValueError:
            next_key.append(length)
            break
       
     
#DataFrame that ish
youtube = pd.DataFrame({'Start':start_key,'Next':next_key})
youtube['Start'] = pd.to_numeric(youtube['Start'])
youtube['Next'] = pd.to_numeric(youtube['Next'])
youtube['String'] = ""

string = []
for index, row in youtube.iterrows():
    s = row['Start']
    e = row['Next']
    ranger = slice(s,e)
    string.append(text[ranger])

youtube['String'] = string

youtube = youtube[~youtube.String.str.contains("}]")]

youtube['String'] = youtube['String'].str.split(" ")
youtube['String'].replace('—\xa0Pink','- Pink')
youtube['Song'] = ""
youtube['Days Ago'] = ""
youtube['Weeks Ago'] = ""
youtube['Months Ago'] = ""
youtube['Years Ago'] = ""
years = []
months = []
weeks = []
days = []
songs = []
views = []

for index, row in youtube.iterrows():
    string = row['String']
    string = string[3:]
    #print(string)
    by = string.index('by')
    lenStr = len(string)
    song = ' '.join(string[:by])
    view = string[lenStr - 2]
    try:
        year_past = string[string.index('year') - 1]
    except ValueError:
        try:
           year_past = string[string.index('years') - 1]
        except ValueError:
               year_past = 0
    try:
        month_past = string[string.index('month') - 1]
    except ValueError:
        try:
            month_past = string[string.index('months') - 1]
        except ValueError:
            month_past = 0
    try:
        week_past = string[string.index('week') - 1]
    except ValueError:
        try:
            week_past = string[string.index('weeks') - 1]
        except ValueError:
            week_past = 0
    try:
        day_past = string[string.index('day') - 1]
    except ValueError:
        try:
            day_past = string[string.index('day') - 1]
        except ValueError:
            day_past = 0
    views.append(view)
    years.append(year_past)
    months.append(month_past)
    weeks.append(week_past)
    days.append(day_past)
    songs.append(song)
   

youtube['Years Ago'] = years
youtube['Months Ago'] = months
youtube['Weeks Ago'] = weeks
youtube['Days Ago'] = days
youtube['Song'] = songs
youtube['Views'] = views
youtube['timestamp'] = timestamp

#SAVE to Excel and Import Youtube History
print("Saving YouTube details to Excel...")
AllYoutube = pd.read_excel(all_youtube_file)
AllYoutube = AllYoutube.append(youtube)
#Drop unnamed columns
drop_cols = [col for col in AllYoutube.columns if 'Unnamed' in col]
AllYoutube.drop(columns=drop_cols, inplace=True)    
#to_excel
AllYoutube.to_excel(all_youtube_file)

#------------------------------------------------------------------------------
#-----------CURRENT STATS DATAFRAME-----------------------------------------------------------------
print("Storing statistics...")
johnny_current_stats = pd.DataFrame()
johnny_current_stats['timestamp'] = [timestamp]
johnny_current_stats['spotify popularity'] = [johnny_popularity]
johnny_current_stats['spotify followers'] = [johnny_followers]
johnny_current_stats['spotify monthly_listeners'] = [monthly_listeners]
johnny_current_stats['youtube subscribers'] = [subscribers]
johnny_current_stats['instagram followers'] = [followers]

johnny_all_stats = pd.read_excel(all_stats_file)
johnny_all_stats = johnny_all_stats.append(johnny_current_stats)
#Drop unnamed columns
drop_cols = [col for col in johnny_all_stats.columns if 'Unnamed' in col]
johnny_all_stats.drop(columns=drop_cols, inplace=True)  
johnny_all_stats2 = johnny_all_stats.set_index('timestamp')
johnny_all_stats2.index = pd.to_datetime(johnny_all_stats2.index)
johnny_all_stats2 = johnny_all_stats2.dropna().astype(int)
#to_excel
johnny_all_stats.to_excel(all_stats_file)

#-----------ALL STATS GRAPH---------------------------------------------------------
print("Visualizing general stats...")


#--Prepping Line of Best Fit Data
goal = 1000000
goal_formatted = "{:,}".format(goal)

johnny_all_stats2['numeric_date'] = johnny_all_stats2.index.to_julian_date()

X = johnny_all_stats2['numeric_date']
Y = johnny_all_stats2['spotify monthly_listeners']
m, b = np.polyfit(X,Y,1)
johnny_all_stats2['monthly_listeners_best_fit'] = johnny_all_stats2['numeric_date']*m + b

goal_x = ((goal - b ) / m)
goal_date = pd.to_datetime(goal_x, unit='D', origin = 'julian')
goal_date = goal_date.strftime("%b %-d, %Y at %-I:%M %p")
yay = "Johnny is set to reach %s monthly listeners on %s!!" % (goal_formatted, goal_date)
print(yay)

#Visualizing Line Charts

line = make_subplots(rows = 2, cols=1, shared_xaxes=True,vertical_spacing=0.02)

line.add_trace(
    go.Scatter(x=johnny_all_stats2.index, y=johnny_all_stats2['spotify monthly_listeners'], mode="lines+markers", name="Spotify Monthly Listeners"),
    row=1,col=1)

line.add_trace(
    go.Scatter(x=johnny_all_stats2.index, y=johnny_all_stats2['monthly_listeners_best_fit'], mode='lines',name="Prediction of Spotify Monthly Listeners", 
               line=dict(color='silver', width=2,
                              dash='dash')),
    row=1,col=1)

line.add_trace(
    go.Scatter(x=johnny_all_stats2.index, y=johnny_all_stats2['spotify followers'], mode="lines+markers", name="Spotify Followers"),
    row=2,col=1)

line.add_trace(
    go.Scatter(x=johnny_all_stats2.index, y=johnny_all_stats2['youtube subscribers'], mode="lines+markers", name="YouTube Subscribers"),
    row=2,col=1)

line.add_trace(
    go.Scatter(x=johnny_all_stats2.index, y=johnny_all_stats2['instagram followers'], mode="lines+markers", name="Instagram Followers"),
    row=2,col=1)


# Set x-axis title
line.update_layout(title_text="Social Media Hype", margin=dict(l=20, r=20, t=40, b=20))

line.show()




##-----------PLOTLY CHART STUDIO----------------------------------------------------------------
"""
username = 'marystimson' # your username
api_key = 'NA0Aj5kRqGk4SHLraxp9' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

py.plot(geographic_map, filename = 'geographic_map', auto_open=True)
py.plot(radar, filename = 'radar', auto_open=True)
"""
#------------DASH---------------------------------------------------------------\


app = dash.Dash()

app.layout = html.Div([
       html.Div([
            html.H3("The Official Johnny Stimson Fan Club Mega Tracking Dashboard 1.0"),
            html.P(yay),
            dcc.Graph(id='line', figure=line, config={'displayModeBar': False}),
        ], className="six columns"),
            
    html.Div(children=[
        dcc.Graph(id="graph1", figure=geographic_map, config={'displayModeBar': False}, style={'display': 'inline-block'}),
        dcc.Graph(id="graph2", figure=radar, config={'displayModeBar': False}, style={'display': 'inline-block'})
    ])
])
            
            
if __name__ == '__main__':
    app.run_server(debug=False)  #debug=False makes it run a lot smoother but may throw a file descriptor error!
#Look into hot reloading.
    
print("Success!")

#####TEST TEST TEST



"""
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div(dcc.Graph(
        id='map',
        figure=geographic_map
    ),
    html.Div(dcc.Graph(
    id='radar',
    figure=radar
    ))) 
#])

if __name__ == '__main__':
    app.run_server(debug=True)
#------------------------------------------------------------------------------------

<after first html.Div(>
style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

#Geographic listeners over time slider
#Youtube
#size of stadium of listeners on spotify
#Google trends see pytrends
#Scrape number of listens per song on Spotify
#append/track number of listeners on Spotify
#Add/append number of Instagram likes per pic, etc.
#The first option for calculating your Instagram engagement rate is to divide your total number of likes and comments by your follower count, and then multiply by 100 to give you a percentage.
#Add/append Youtube views and #/subscribers /comments per pink lemonade

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------TONS OF ARTISTS

artist_name = []
track_name = []
popularity = []
track_id = []
for i in range(0,10000,50):
    track_results = sp.search(q='year:2020', type='track', limit=50,offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
       
import pandas as pd
track_dataframe = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_id, 'popularity' : popularity})
print(track_dataframe.shape)
track_dataframe.head()
"""
#########
