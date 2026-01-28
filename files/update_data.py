#!/usr/bin/env python3
"""
A-lex Artist Hub - Data Update Script
Fetches data from Spotify and YouTube APIs and generates cache.json
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class ArtistDataUpdater:
    def __init__(self):
        # Initialize Spotify client
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')
            )
        )
        
        # YouTube API key
        self.youtube_api_key = os.environ.get('YOUTUBE_API_KEY')
        
        # Load artist configuration
        with open('data/artists.json', 'r') as f:
            self.config = json.load(f)
    
    def extract_spotify_id(self, url: str) -> Optional[str]:
        """Extract Spotify artist ID from URL"""
        if '/artist/' in url:
            return url.split('/artist/')[-1].split('?')[0]
        return None
    
    def extract_youtube_channel_id(self, url: str) -> Optional[str]:
        """Extract YouTube channel ID from URL"""
        # This is a simplified version - you may need to use YouTube API
        # to resolve @username to channel ID
        if '@' in url:
            username = url.split('@')[-1].strip('/')
            return self.resolve_youtube_username(username)
        elif '/channel/' in url:
            return url.split('/channel/')[-1].split('?')[0]
        return None
    
    def resolve_youtube_username(self, username: str) -> Optional[str]:
        """Resolve YouTube username to channel ID using API"""
        if not self.youtube_api_key:
            return None
            
        try:
            url = f'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': username,
                'type': 'channel',
                'maxResults': 1,
                'key': self.youtube_api_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['snippet']['channelId']
        except Exception as e:
            print(f"Error resolving YouTube username: {e}")
        
        return None
    
    def get_artist_data(self, spotify_url: str) -> Optional[Dict]:
        """Fetch artist data from Spotify"""
        artist_id = self.extract_spotify_id(spotify_url)
        if not artist_id:
            return None
        
        try:
            artist = self.spotify.artist(artist_id)
            return {
                'id': artist_id,
                'name': artist['name'],
                'image': artist['images'][0]['url'] if artist['images'] else None,
                'followers': artist['followers']['total'],
                'genres': artist['genres']
            }
        except Exception as e:
            print(f"Error fetching artist data: {e}")
            return None
    
    def get_artist_tracks(self, artist_id: str, limit: int = 10) -> List[Dict]:
        """Fetch artist's latest tracks from Spotify"""
        try:
            # Get artist's albums
            albums = self.spotify.artist_albums(
                artist_id,
                album_type='album,single',
                limit=10
            )
            
            tracks = []
            seen_track_names = set()
            
            for album in albums['items']:
                album_tracks = self.spotify.album_tracks(album['id'])
                
                for track in album_tracks['items']:
                    # Avoid duplicates
                    if track['name'] in seen_track_names:
                        continue
                    
                    seen_track_names.add(track['name'])
                    
                    # Get full track details for popularity
                    full_track = self.spotify.track(track['id'])
                    
                    tracks.append({
                        'id': track['id'],
                        'title': track['name'],
                        'coverArt': album['images'][0]['url'] if album['images'] else None,
                        'releaseDate': album['release_date'],
                        'popularity': full_track['popularity'],
                        'spotifyUrl': full_track['external_urls']['spotify']
                    })
                    
                    if len(tracks) >= limit:
                        break
                
                if len(tracks) >= limit:
                    break
            
            # Sort by release date (newest first)
            tracks.sort(key=lambda x: x['releaseDate'], reverse=True)
            return tracks[:limit]
            
        except Exception as e:
            print(f"Error fetching tracks: {e}")
            return []
    
    def search_youtube_video(self, track_name: str, artist_name: str) -> Optional[Dict]:
        """Search for track on YouTube"""
        if not self.youtube_api_key:
            return None
        
        try:
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': f'{artist_name} {track_name} official',
                'type': 'video',
                'maxResults': 1,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                video = data['items'][0]
                video_id = video['id']['videoId']
                
                # Get video statistics
                stats_url = 'https://www.googleapis.com/youtube/v3/videos'
                stats_params = {
                    'part': 'statistics',
                    'id': video_id,
                    'key': self.youtube_api_key
                }
                
                stats_response = requests.get(stats_url, params=stats_params)
                stats_data = stats_response.json()
                
                if 'items' in stats_data and len(stats_data['items']) > 0:
                    stats = stats_data['items'][0]['statistics']
                    return {
                        'url': f'https://youtube.com/watch?v={video_id}',
                        'views': int(stats.get('viewCount', 0))
                    }
        except Exception as e:
            print(f"Error searching YouTube: {e}")
        
        return None
    
    def search_apple_music(self, track_name: str, artist_name: str) -> Optional[str]:
        """Search for track on Apple Music"""
        try:
            # Apple Music API requires authentication
            # For now, we'll construct a search URL
            # In production, you'd use the Apple Music API
            search_query = f"{artist_name} {track_name}".replace(' ', '+')
            return f"https://music.apple.com/search?term={search_query}"
        except Exception as e:
            print(f"Error searching Apple Music: {e}")
            return None
    
    def update_all_artists(self):
        """Update data for all configured artists"""
        artists_data = []
        
        for artist_config in self.config['artists']:
            print(f"\n📀 Processing {artist_config['artist']}...")
            
            # Get artist info from Spotify
            artist_data = self.get_artist_data(artist_config['spotify'])
            if not artist_data:
                print(f"❌ Could not fetch data for {artist_config['artist']}")
                continue
            
            # Get tracks
            tracks = self.get_artist_tracks(artist_data['id'])
            
            # Enrich tracks with YouTube and Apple Music data
            for track in tracks:
                print(f"  🎵 Processing: {track['title']}")
                
                # YouTube
                youtube_data = self.search_youtube_video(
                    track['title'],
                    artist_data['name']
                )
                if youtube_data:
                    track['youtubeUrl'] = youtube_data['url']
                    track['youtubeViews'] = youtube_data['views']
                else:
                    track['youtubeUrl'] = None
                    track['youtubeViews'] = 0
                
                # Apple Music
                apple_url = self.search_apple_music(
                    track['title'],
                    artist_data['name']
                )
                track['appleMusicUrl'] = apple_url
                
                # Audiomack (use artist's base URL + track slug)
                if 'audiomack' in artist_config:
                    track_slug = track['title'].lower().replace(' ', '-')
                    track['audiomackUrl'] = f"{artist_config['audiomack']}/song/{track_slug}"
                else:
                    track['audiomackUrl'] = None
            
            artists_data.append({
                'id': artist_data['id'],
                'name': artist_data['name'],
                'image': artist_data['image'],
                'spotify': artist_config['spotify'],
                'youtube': artist_config.get('youtube'),
                'appleMusic': artist_config.get('appleMusic'),
                'audiomack': artist_config.get('audiomack'),
                'tracks': tracks
            })
            
            print(f"✅ Processed {len(tracks)} tracks for {artist_data['name']}")
        
        # Generate cache file
        cache_data = {
            'lastUpdated': datetime.utcnow().isoformat() + 'Z',
            'artists': artists_data
        }
        
        # Save to cache.json
        os.makedirs('data', exist_ok=True)
        with open('data/cache.json', 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"\n✨ Successfully updated data for {len(artists_data)} artists")
        print(f"📝 Cache saved to data/cache.json")

def main():
    """Main execution function"""
    updater = ArtistDataUpdater()
    updater.update_all_artists()

if __name__ == '__main__':
    main()
