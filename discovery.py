# REQUIRES:
	# spotipy module
	# web app configured on https://developer.spotify.com/ (with Spotify credentials)
	# OS environment variables set (in cmd):
		# Windows:
			# set SPOTIPY_CLIENT_ID='your-spotify-client-id'
			# set SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
		# Mac: 
			# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
			# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pprint import pprint
import random
from time import sleep

os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8000"

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(), auth_manager=SpotifyOAuth(scope=scope))

allchars = 'qwertyuiopasdfghjklzxcvbnm'
market = "CA" # start with a canadian market (this will change later)

while True:
	char = random.choice(allchars)
	n = 10000
	offset = random.randint(0,n-1) # random spot on the list
	try:
		results = sp.search(q=char+'%', type='track', offset=offset, market=market) # start with the letter and fill in the rest of the query ordered by popularity
	except: # most queries don't return n results
		continue
	result = results['tracks']['items'][0] # select the "first" song (offset by up to n)
	album_id = result['album']['id']
	album_ = sp.album(album_id)
	markets = album_['available_markets']
	market = random.choice(markets) # choose new market
	# track_duration = result['duration_ms']
	if result['explicit']: # skip explicit
		continue
	sp.start_playback(uris=['spotify:track:'+result['id']]) # play track
	sleep(0.5) # wait for track to start
	# nesting infinite loops in place of event listeners (hopefully temporarily)
	while True: # start next track when current one finishes
		while True:
			if sp.current_playback()['progress_ms']: # playback started
				break
		while True:
			if not sp.current_playback()['progress_ms']: # playback stopped
				# Triggers at end of track (a simple method for which I didn't find)
				# Doesn't trigger if paused as long as progress is nonzero
				# In theory, can trigger if track is set back to start while playing (progress = 0), but unlikely since the intepreter only checks this condition every 100 milliseconds or so, while the track begins to play much more quickly than that (making nonzero progress)
				# DOES trigger if track is set back to zero while paused
				break
		break

