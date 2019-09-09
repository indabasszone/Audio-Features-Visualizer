#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import plotly.graph_objs as go
import chart_studio.plotly as py

from ipywidgets import widgets
from IPython.display import display, clear_output, Image
from chart_studio.widgets import GraphWidget

import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials


# In[2]:


#Setting up everything we need to make calls to the Spotify API
#Done globally so that it can be shared easily by all methods
id = "f40e1f7f67db4e7d858aacdc03749ef9"
secret = "c3617937da9043c6b91e8717bdbaa49e"
client_credentials_manager = SpotifyClientCredentials(client_id=id, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Enter your own album URI here (or check out this one, I think it's pretty cool)
album_uri = "spotify:album:0WBKzTwWxcjFhFNEoOYY5A"


# In[3]:


def get_album_info(album_uri):
    #Gets all tracks from the album, adds their names and URIs to the tracks dict
    album_tracks = sp.album_tracks(album_uri)
    tracks = {}
    for item in album_tracks["items"]:
        tracks.update({item["name"]: item["uri"]})

    album_audio_features = {"Name": [], "Danceability": [], "Energy": [], "Acousticness": [],
                            "Instrumentalness": [], "Valence": []}

    #Gets the audio features for each track and adds them to the dict
    for track in tracks:
        uri = tracks[track]
        audio_features = sp.audio_features(uri)

        album_audio_features['Name'].append(track)
        album_audio_features['Danceability'].append(audio_features[0]["danceability"])
        album_audio_features['Energy'].append(audio_features[0]["energy"])
        album_audio_features['Acousticness'].append(audio_features[0]["acousticness"])
        album_audio_features['Instrumentalness'].append(audio_features[0]["instrumentalness"])
        album_audio_features['Valence'].append(audio_features[0]["valence"])

    #Adds the data for the whole album to the dict then returns it
    add_album_features(album_audio_features)
    
    return pd.DataFrame(album_audio_features)


# In[7]:


def add_album_features(feat_dict):
    #Adds data for the album as a whole (just averages the values for all tracks)
    total = len(feat_dict['Name'])

    feat_dict['Name'].insert(0, "Whole Album")
    feat_dict['Danceability'].insert(0, sum(feat_dict['Danceability'])/total)
    feat_dict['Energy'].insert(0, sum(feat_dict['Energy'])/total)
    feat_dict['Acousticness'].insert(0, sum(feat_dict['Acousticness'])/total)
    feat_dict['Instrumentalness'].insert(0, sum(feat_dict['Instrumentalness'])/total)
    feat_dict['Valence'].insert(0, sum(feat_dict['Valence'])/total)


# In[5]:


def track_changed(change):
    #Follows same process as above to get the new y-values and colors for the bar graph
    new_track_name = track_selection.value
    new_y_values = album_audio_features.loc[[new_track_name], ['Danceability', 'Energy', 'Acousticness', 'Instrumentalness', 'Valence']].values
    new_y_values = new_y_values[0]
    
    new_color = []
    for i in range (0, len(new_y_values)):
        val = new_y_values[i]
        r_val = str(val * 200)
        g_val = str(10)
        b_val = str(200)
        new_color.append('rgb(' + r_val + ',' + g_val + ',' + b_val + ')')
    
    #Updates the graph with the new y values and colors
    with fig_widget.batch_update():
        fig_widget.data[0].r = new_y_values
        fig_widget.data[0].marker=dict(color=new_color)


# In[8]:


#Gets each song's audio features analysis in a pandas dataframe
album_audio_features = get_album_info(album_uri)
album_audio_features.set_index('Name', inplace=True)

#Dropdown menu to select track to view data for (defaults to whole album)
track_selection = widgets.Dropdown(options=list(album_audio_features.index.values),value='Whole Album',description='View for:     ',)

#When the dropdown menu is changed, it executes the track_changed method
track_selection.observe(track_changed, names="value")

#Gets the current track name from the dropdown menu (only default value will be used here)
track_name = track_selection.value

#Uses the column categories in the dataframe as the x-values in the bar graph
x_values = list(album_audio_features)

#Gets the values for each column category for the selected track
y_values = album_audio_features.loc[[track_name], ['Danceability', 'Energy', 'Acousticness', 'Instrumentalness', 'Valence']].values

#For some reason it stores all the values as a list inside another list,
#So this line just gets the real list of y values
y_values = y_values[0]

#Calculates each bar's RGB color
color = []
for i in range (0, len(y_values)):
    val = y_values[i]
    r_val = str(val * 200)
    g_val = str(10)
    b_val = str(200)
    color.append('rgb(' + r_val + ',' + g_val + ',' + b_val + ')')

#Creates the polar bar graph with the x values, y values, and colors from above
trace = go.Figure([go.Barpolar(opacity=0.75, theta=x_values, r=y_values, marker=dict(color=color))])

#Displays the dropdown menu
display(track_selection)

#Turns the polar bar graph into a FigureWidget so it will live update then displays it
fig_widget = go.FigureWidget(data=trace)
fig_widget


# In[ ]:




