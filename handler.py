import spotipy
import datetime
import logging
import time
from spotipy.oauth2 import SpotifyOAuth
from datetime import date

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Spotify_Weekly_Playlists_Handler:
  def __init__(self):
    self.discover_weekly_playlists = None
    self.discover_weekly_tracks = None
    self.sp = None

    self.initialize_spotipy()
    self.run()
  
  def run(self):
    try:
      # Get Tracks
      discover_weekly_tracks = self.get_weekly_playlist_tracks()

      # Construct Playlist Name
      first_track_name = self.get_first_track_name()
      new_playlist_name = self.generate_playlist_name(first_track_name)

      # Create New Playlist
      new_playlist = self.create_new_playlist(name=new_playlist_name)

      # Add Tracks To Playlist
      new_playlist_id = new_playlist.get('id')
      self.add_tracks_to_playlist(playlist_id=new_playlist_id, tracks=discover_weekly_tracks)

      # Print Result
      new_playlist_uri = new_playlist.get('uri')
      print(f"Success! Your Discover Weekly is saved as '{new_playlist_name}' at {new_playlist_uri}")
    except:
      print('Error! Something went wrong')


  def initialize_spotipy(self):
    scopes = ["playlist-modify-private", "playlist-read-private", "user-read-currently-playing", "playlist-modify-private"]
    self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))
  
  def get_weekly_playlist_tracks(self):
    track_uris = list()
    try:
      self.discover_weekly_playlists =  self.sp.playlist('37i9dQZEVXcMu9M1MdIExB')

      self.discover_weekly_tracks = self.discover_weekly_playlists.get('tracks', {}).get('items', [])
      
      for track in self.discover_weekly_tracks:
        current_uri = track['track']['uri']
        track_uris.append(current_uri)

      return track_uris
    except:
      print('no track uris found')

  def get_first_track_name(self):
    first_track_name = None
    try:
      if not self.discover_weekly_playlists or not self.discover_weekly_tracks:
        self.discover_weekly_playlists = self.sp.playlist('37i9dQZEVXcMu9M1MdIExB')
        self.discover_weekly_tracks = self.discover_weekly_playlists.get('tracks', {}).get('items', [])
      first_track_dict = self.discover_weekly_tracks[0]
      first_track_name = first_track_dict['track']['name']
      
      return first_track_name

    except:
      print('no tracks found')

  def print_currently_playing(self):
    current = self.sp.currently_playing()
    print(current)

  def create_new_playlist(self, name):
    print('Creating New Playlist')
    current_user_dict = self.sp.current_user()
    current_user_id = current_user_dict.get('id')
    return self.sp.user_playlist_create(user=current_user_id, name=name, public=False, collaborative=False, description="Code is cool")

  def generate_playlist_name(self, first_track_name='Discover Weekly'):
    today = date.today().strftime("%m/%d/%y")
    title = first_track_name
    if title is not "Discover Weekly":
      if len(title) > 18:
        title = ''
        words = first_track_name.split(' ')
        for word in words:
          if len(title) >= 15:
            break
          if not title:
            title = word
          else:
            title += " " + word

    
    playlist_name = f"{title} {today}"

    return playlist_name

  def find_playlist_by_name(self, name):
    target_playlist = None
    # Get list of playlists
    try:
      current_user_playlists = self.sp.current_user_playlists()
      # find the playlist by name
      playlists = current_user_playlists.get("items", [])
      print(f"Searching for {name} in playlists...")
      for playlist in playlists:
        current_playlist_name_from_list = playlist.get('name', '')
        if current_playlist_name_from_list == name:
          target_playlist = playlist
          break
      # return the URI
      return target_playlist.get('id', '')
    except:
      print(f'Could not find the user playlist {name}')

  def add_tracks_to_playlist(self, playlist_id, tracks):
    self.sp.playlist_add_items(playlist_id=playlist_id, items=tracks, position=0)

def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name

    Spotify_Weekly_Playlists_Handler()

    logger.info("Your cron function " + name + " ran at " + str(current_time))
