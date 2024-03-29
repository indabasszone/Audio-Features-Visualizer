# Audio-Features-Visualizer

This is a short Jupyter notebook script that visualizes the audio features for an album, as described by Spotify. While they provide many data points in their audio features analysis, the five I chose to highlight are danceability, energy, acousticness, instrumentalness, and valence (described her: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/). The data is collected using the Spotify Web API (in this case accessed through the Spotipy wrapper), stored/cleaned in Pandas, then displayed using Plotly & ipywidgets.

The code can be easily previewed here in the .py script, but to actually run the program, you must open the .ipynb file in a Jupyter notebook. All you have to do is paste the Spotify URI for the album you want to analyze (which you can find using the Spotify desktop app) into the corresponding field then run the script (be sure to shift+enter the code blocks sequentially). You can view data for the whole album or for the individual tracks using the dropdown menu, which will live update the graph. To see data for another album just change the album URI field and rerun the script.
![](aafv.gif)
