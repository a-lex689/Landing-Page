#!/usr/bin/env python3
"""
A-lex Artist Hub - Data Automation Script
Fetches artist data from Spotify, YouTube and generates cache.json
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
import base64
import re

class ArtistHubAutomation:
    def __init__(self):
        self.config = self.load_config()
        self.spotify_token = None
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY', '')
        
    def load_config(self) -> Dict:
        """Load artists configuration"""
        with open('artists.json', 'r') as f:
            return json.load(f)
    
    def get_spotify_token(self) -> str:
        """Get Spotify API access token"""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            print("⚠️  Spotify credentials not found in environment variables")
            return None
        
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            self.spotify_token = response.json()['access_token']
            return self.spotify_token
        
        print(f"❌ Failed to get Spotify token: {response.status_code}")
        return None
    
    def extract_spotify_id(self, url: str) -> Optional[str]:
        """Extract artist ID from Spotify URL"""
        match = re.search(r'artist/([a-zA-Z0-9]+)', url)
        return match.group(1) if match else None
    
    def fetch_spotify_artist(self, artist_id: str) -> Optional[Dict]:
        """Fetch artist data from Spotify"""
        if not self.spotify_token:
            return None
        
        headers = {'Authorization': f'Bearer {self.spotify_token}'}
        
        # Get artist info
        artist_response = requests.get(
            f'https://api.spotify.com/v1/artists/{artist_id}',
            headers=headers
        )
        
        if artist_response.status_code != 200:
            print(f"❌ Failed to fetch artist {artist_id}")
            return None
        
        artist_data = artist_response.json()
        
        # Get artist's albums (latest releases)
        albums_response = requests.get(
            f'https://api.spotify.com/v1/artists/{artist_id}/albums',
            headers=headers,
            params={
                'include_groups': 'single,album',
                'limit': 20,
                'market': 'US'
            }
        )
        
        albums = albums_response.json().get('items', []) if albums_response.status_code == 200 else []
        
        # Get top tracks
        top_tracks_response = requests.get(
            f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks',
            headers=headers,
            params={'market': 'US'}
        )
        
        top_tracks = top_tracks_response.json().get('tracks', []) if top_tracks_response.status_code == 200 else []
        
        return {
            'id': artist_id,
            'name': artist_data['name'],
            'imageUrl': artist_data['images'][0]['url'] if artist_data['images'] else None,
            'albums': albums,
            'topTracks': top_tracks
        }
    
    def fetch_youtube_data(self, track_name: str, artist_name: str) -> Optional[Dict]:
        """Fetch YouTube video data for a track"""
        if not self.youtube_api_key:
            return None
        
        search_query = f"{artist_name} {track_name} official"
        
        params = {
            'part': 'snippet',
            'q': search_query,
            'type': 'video',
            'maxResults': 1,
            'key': self.youtube_api_key
        }
        
        try:
            response = requests.get(
                'https://www.googleapis.com/youtube/v3/search',
                params=params
            )
            
            if response.status_code == 200:
                items = response.json().get('items', [])
                if items:
                    video_id = items[0]['id']['videoId']
                    
                    # Get video statistics
                    stats_response = requests.get(
                        'https://www.googleapis.com/youtube/v3/videos',
                        params={
                            'part': 'statistics',
                            'id': video_id,
                            'key': self.youtube_api_key
                        }
                    )
                    
                    if stats_response.status_code == 200:
                        stats = stats_response.json()['items'][0]['statistics']
                        return {
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'views': int(stats.get('viewCount', 0))
                        }
        except Exception as e:
            print(f"⚠️  YouTube API error: {e}")
        
        return None
    
    def generate_apple_music_url(self, artist_name: str, track_name: str) -> str:
        """Generate Apple Music search URL"""
        query = f"{artist_name} {track_name}".replace(' ', '+')
        return f"https://music.apple.com/us/search?term={query}"
    
    def process_artists(self) -> Dict:
        """Process all artists and generate cache data"""
        print("🎵 Starting A-lex Artist Hub automation...")
        
        if not self.get_spotify_token():
            print("❌ Cannot proceed without Spotify token")
            return self.generate_empty_cache()
        
        print("✅ Spotify token obtained")
        
        all_artists = []
        all_tracks = []
        
        for artist_config in self.config['artists']:
            print(f"\n🎤 Processing: {artist_config['name']}")
            
            spotify_id = self.extract_spotify_id(artist_config.get('spotify', ''))
            if not spotify_id:
                print(f"  ⚠️  No valid Spotify URL, skipping")
                continue
            
            # Fetch Spotify data
            artist_data = self.fetch_spotify_artist(spotify_id)
            if not artist_data:
                continue
            
            print(f"  ✅ Fetched Spotify data")
            
            # Process latest releases
            latest_releases = []
            for album in artist_data['albums'][:self.config['config']['latestReleasesPerArtist']]:
                release = {
                    'title': album['name'],
                    'releaseDate': album['release_date'],
                    'spotifyUrl': album['external_urls']['spotify']
                }
                
                # Try to find YouTube video
                youtube_data = self.fetch_youtube_data(album['name'], artist_data['name'])
                
                if youtube_data:
                    release['youtubeUrl'] = youtube_data['url']
                
                release['appleMusicUrl'] = self.generate_apple_music_url(
                    artist_data['name'], 
                    album['name']
                )
                
                if artist_config.get('audiomack'):
                    release['audiomackUrl'] = artist_config['audiomack']
                
                latest_releases.append(release)
            
            # Process top tracks for global ranking
            for track in artist_data['topTracks']:
                track_data = {
                    'id': track['id'],
                    'title': track['name'],
                    'artist': artist_data['name'],
                    'coverUrl': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'popularity': track['popularity'],
                    'spotifyUrl': track['external_urls']['spotify'],
                    'score': 0
                }
                
                # Fetch YouTube data
                youtube_data = self.fetch_youtube_data(track['name'], artist_data['name'])
                
                if youtube_data:
                    track_data['youtubeUrl'] = youtube_data['url']
                    track_data['youtubeViews'] = youtube_data['views']
                    
                    # Calculate combined score
                    spotify_score = track['popularity'] * self.config['config']['spotifyWeight']
                    youtube_score = min(100, youtube_data['views'] / 100000) * self.config['config']['youtubeWeight']
                    track_data['score'] = spotify_score + youtube_score
                else:
                    track_data['score'] = track['popularity'] * self.config['config']['spotifyWeight']
                
                track_data['appleMusicUrl'] = self.generate_apple_music_url(
                    artist_data['name'],
                    track['name']
                )
                
                if artist_config.get('audiomack'):
                    track_data['audiomackUrl'] = artist_config['audiomack']
                
                all_tracks.append(track_data)
            
            # Add to artists list
            all_artists.append({
                'id': artist_data['id'],
                'name': artist_data['name'],
                'imageUrl': artist_data['imageUrl'],
                'latestReleases': latest_releases
            })
            
            print(f"  ✅ Processed {len(latest_releases)} releases")
        
        # Sort tracks by score and get top N
        all_tracks.sort(key=lambda x: x['score'], reverse=True)
        top_songs = all_tracks[:self.config['config']['topSongsCount']]
        
        # Generate cache
        cache = {
            'lastUpdated': datetime.utcnow().isoformat() + 'Z',
            'topSongs': top_songs,
            'artists': all_artists
        }
        
        print(f"\n✅ Generated cache with {len(top_songs)} top songs and {len(all_artists)} artists")
        
        return cache
    
    def generate_empty_cache(self) -> Dict:
        """Generate empty cache structure"""
        return {
            'lastUpdated': datetime.utcnow().isoformat() + 'Z',
            'topSongs': [],
            'artists': []
        }
    
    def save_cache(self, cache: Dict):
        """Save cache to file"""
        os.makedirs('data', exist_ok=True)
        
        with open('data/cache.json', 'w') as f:
            json.dump(cache, f, indent=2)
        
        print(f"💾 Cache saved to data/cache.json")
    
    def run(self):
        """Main execution"""
        cache = self.process_artists()
        self.save_cache(cache)
        print("\n🔥 Automation complete!")

if __name__ == '__main__':
    automation = ArtistHubAutomation()
    automation.run()
