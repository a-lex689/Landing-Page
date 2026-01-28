# 📚 API Documentation

Technical documentation for developers who want to extend or customize the A-lex Artist Hub.

## Table of Contents

1. [Data Structure](#data-structure)
2. [Configuration Options](#configuration-options)
3. [Python Automation Script](#python-automation-script)
4. [Frontend JavaScript API](#frontend-javascript-api)
5. [Customization Guide](#customization-guide)
6. [Adding New Platforms](#adding-new-platforms)

---

## Data Structure

### `cache.json` Schema

The auto-generated cache file that powers the frontend.

```typescript
interface Cache {
  lastUpdated: string;        // ISO 8601 timestamp
  topSongs: Song[];          // Top N songs (default: 3)
  artists: Artist[];         // All configured artists
}

interface Song {
  id: string;                // Spotify track ID
  title: string;             // Track name
  artist: string;            // Artist name
  coverUrl: string | null;   // Album cover image URL
  popularity: number;        // Spotify popularity (0-100)
  spotifyUrl: string;        // Spotify track URL
  youtubeUrl?: string;       // YouTube video URL (optional)
  youtubeViews?: number;     // View count (optional)
  appleMusicUrl?: string;    // Apple Music URL (optional)
  audiomackUrl?: string;     // Audiomack URL (optional)
  score: number;             // Calculated ranking score
}

interface Artist {
  id: string;                // Spotify artist ID
  name: string;              // Artist name
  imageUrl: string | null;   // Artist image URL
  latestReleases: Release[]; // Latest N releases (default: 5)
}

interface Release {
  title: string;             // Release name
  releaseDate: string;       // YYYY-MM-DD format
  spotifyUrl: string;        // Spotify album/single URL
  youtubeUrl?: string;       // YouTube video URL (optional)
  appleMusicUrl?: string;    // Apple Music URL (optional)
  audiomackUrl?: string;     // Audiomack URL (optional)
}
```

### Example `cache.json`

```json
{
  "lastUpdated": "2026-01-28T12:00:00Z",
  "topSongs": [
    {
      "id": "4cOdK2wGLETKBW3PvgPWqT",
      "title": "example track",
      "artist": "Example Artist",
      "coverUrl": "https://i.scdn.co/image/...",
      "popularity": 87,
      "spotifyUrl": "https://open.spotify.com/track/...",
      "youtubeUrl": "https://youtube.com/watch?v=...",
      "youtubeViews": 1500000,
      "appleMusicUrl": "https://music.apple.com/...",
      "audiomackUrl": "https://audiomack.com/...",
      "score": 91.5
    }
  ],
  "artists": [
    {
      "id": "3TVXtAsR1Inumwj472S9r4",
      "name": "Example Artist",
      "imageUrl": "https://i.scdn.co/image/...",
      "latestReleases": [
        {
          "title": "Latest Single",
          "releaseDate": "2026-01-15",
          "spotifyUrl": "https://open.spotify.com/album/...",
          "youtubeUrl": "https://youtube.com/watch?v=...",
          "appleMusicUrl": "https://music.apple.com/..."
        }
      ]
    }
  ]
}
```

---

## Configuration Options

### `artists.json` Schema

```typescript
interface Config {
  artists: ArtistConfig[];
  config: GlobalConfig;
}

interface ArtistConfig {
  name: string;              // Display name
  spotify: string;           // Spotify artist URL (required)
  youtube?: string;          // YouTube channel URL
  appleMusic?: string;       // Apple Music artist URL
  audiomack?: string;        // Audiomack profile URL
}

interface GlobalConfig {
  updateFrequencyHours: number;         // Default: 12
  topSongsCount: number;                // Default: 3
  latestReleasesPerArtist: number;      // Default: 5
  spotifyWeight: number;                // Default: 0.7 (0-1)
  youtubeWeight: number;                // Default: 0.3 (0-1)
}
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `updateFrequencyHours` | number | 12 | Hours between auto-updates |
| `topSongsCount` | number | 3 | Number of top songs to display |
| `latestReleasesPerArtist` | number | 5 | Latest releases per artist |
| `spotifyWeight` | number | 0.7 | Weight for Spotify popularity (0-1) |
| `youtubeWeight` | number | 0.3 | Weight for YouTube views (0-1) |

**Note:** `spotifyWeight + youtubeWeight` should equal 1.0

---

## Python Automation Script

### Class: `ArtistHubAutomation`

Main automation class that fetches and processes artist data.

#### Methods

##### `__init__()`
Initialize the automation script.

```python
automation = ArtistHubAutomation()
```

##### `get_spotify_token() -> str`
Fetch Spotify API access token using client credentials flow.

**Returns:** Access token string or None

**Environment Variables:**
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`

##### `fetch_spotify_artist(artist_id: str) -> Optional[Dict]`
Fetch complete artist data from Spotify.

**Parameters:**
- `artist_id`: Spotify artist ID

**Returns:** Dictionary containing:
```python
{
    'id': str,
    'name': str,
    'imageUrl': str,
    'albums': List[Dict],
    'topTracks': List[Dict]
}
```

##### `fetch_youtube_data(channel: str, track_name: str, artist_name: str) -> Optional[Dict]`
Search YouTube for track and get statistics.

**Parameters:**
- `channel`: YouTube channel ID or handle
- `track_name`: Track title to search
- `artist_name`: Artist name for search

**Returns:**
```python
{
    'url': str,
    'views': int
}
```

##### `process_artists() -> Dict`
Main processing function that generates complete cache data.

**Returns:** Cache dictionary (see Data Structure)

##### `save_cache(cache: Dict)`
Save cache to `data/cache.json`.

##### `run()`
Main execution method. Run with:

```python
automation = ArtistHubAutomation()
automation.run()
```

---

## Frontend JavaScript API

### Class: `ArtistHub`

Main frontend application class.

#### Properties

```javascript
this.data = null;           // Loaded cache data
this.modal = HTMLElement;   // Modal element reference
```

#### Methods

##### `async init()`
Initialize the application. Loads data and renders UI.

##### `async loadData()`
Fetch `data/cache.json` from server.

**Fallback:** If fetch fails, uses demo data.

##### `render()`
Render all UI components:
- Top songs
- Artist grid
- Last update timestamp

##### `renderTopSongs()`
Render top songs cards from `data.topSongs`.

##### `renderArtists()`
Render artist grid from `data.artists`.

##### `showArtistModal(artistId: string)`
Display modal with artist's latest releases.

**Parameters:**
- `artistId`: Spotify artist ID

##### `closeModal()`
Close the artist modal.

#### Utility Methods

##### `escapeHtml(text: string) -> string`
Escape HTML to prevent XSS.

##### `formatNumber(num: number) -> string`
Format large numbers (1.5M, 50.2K).

##### `formatDate(dateString: string) -> string`
Format ISO date to readable format.

---

## Customization Guide

### Change Ranking Algorithm

Edit `update_data.py`:

```python
def calculate_score(spotify_pop, youtube_views):
    """Custom ranking algorithm"""
    # Example: Prioritize YouTube
    spotify_score = spotify_pop * 0.4
    youtube_score = min(100, youtube_views / 50000) * 0.6
    return spotify_score + youtube_score
```

Then update in `process_artists()`:

```python
# Replace this line:
track_data['score'] = spotify_score + youtube_score

# With:
track_data['score'] = calculate_score(
    track['popularity'],
    youtube_data['views']
)
```

### Add New Data Fields

1. **Update `update_data.py`:**

```python
# In fetch_spotify_artist or process_artists
track_data['genres'] = track.get('genres', [])
track_data['explicit'] = track.get('explicit', False)
```

2. **Update `app.js` rendering:**

```javascript
${song.genres ? `<div class="genres">${song.genres.join(', ')}</div>` : ''}
${song.explicit ? '<span class="explicit">🅴</span>' : ''}
```

3. **Add styling in `styles.css`:**

```css
.genres {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.explicit {
    background: var(--primary);
    padding: 2px 6px;
    border-radius: 4px;
}
```

### Filter By Genre

Add genre filtering to the frontend:

```javascript
// In app.js, add filter method
filterByGenre(genre) {
    const filtered = this.data.topSongs.filter(song => 
        song.genres && song.genres.includes(genre)
    );
    this.renderTopSongs(filtered);
}

// Add genre buttons in HTML
<div class="genre-filters">
    <button onclick="hub.filterByGenre('hip hop')">Hip Hop</button>
    <button onclick="hub.filterByGenre('pop')">Pop</button>
    <button onclick="hub.filterByGenre(null)">All</button>
</div>
```

---

## Adding New Platforms

### 1. Add to Configuration

Update `artists.json` schema:

```json
{
  "artists": [
    {
      "name": "Artist",
      "spotify": "...",
      "tidal": "https://tidal.com/artist/..." // NEW
    }
  ]
}
```

### 2. Update Python Script

Add fetching logic in `update_data.py`:

```python
def fetch_tidal_data(self, artist_url: str) -> Optional[Dict]:
    """Fetch data from Tidal (example)"""
    # Implement Tidal API or scraping
    artist_id = self.extract_tidal_id(artist_url)
    
    # Make API call
    response = requests.get(
        f'https://api.tidal.com/v1/artists/{artist_id}'
    )
    
    if response.status_code == 200:
        data = response.json()
        return {
            'url': artist_url,
            'followers': data.get('followers', 0)
        }
    
    return None

def process_artists(self):
    # ... existing code ...
    
    # Add Tidal to track data
    if artist_config.get('tidal'):
        tidal_data = self.fetch_tidal_data(artist_config['tidal'])
        if tidal_data:
            track_data['tidalUrl'] = tidal_data['url']
```

### 3. Update Frontend

Add platform button in `app.js`:

```javascript
// In renderTopSongs()
${song.tidalUrl ? `
    <a href="${song.tidalUrl}" 
       target="_blank" 
       rel="noopener" 
       class="platform-btn">
        🌊 Tidal
    </a>
` : ''}
```

### 4. Style the Button

Add to `styles.css`:

```css
.platform-btn[href*="tidal"] {
    background: linear-gradient(135deg, #000, #333);
}

.platform-btn[href*="tidal"]:hover {
    background: linear-gradient(135deg, #111, #444);
}
```

---

## Advanced Customizations

### Add Search Functionality

```javascript
// Add to app.js
class ArtistHub {
    // ... existing code ...
    
    setupSearch() {
        const searchInput = document.getElementById('search');
        searchInput.addEventListener('input', (e) => {
            this.search(e.target.value);
        });
    }
    
    search(query) {
        const filtered = {
            topSongs: this.data.topSongs.filter(song =>
                song.title.toLowerCase().includes(query.toLowerCase()) ||
                song.artist.toLowerCase().includes(query.toLowerCase())
            ),
            artists: this.data.artists.filter(artist =>
                artist.name.toLowerCase().includes(query.toLowerCase())
            )
        };
        
        this.renderTopSongs(filtered.topSongs);
        this.renderArtists(filtered.artists);
    }
}
```

### Add Analytics Tracking

```javascript
// Track platform clicks
document.addEventListener('click', (e) => {
    const btn = e.target.closest('.platform-btn');
    if (btn) {
        const platform = btn.textContent.trim();
        const song = btn.closest('.song-card')
            .querySelector('.song-title').textContent;
        
        // Send to analytics
        gtag('event', 'platform_click', {
            'platform': platform,
            'song': song
        });
    }
});
```

### Add Dark/Light Mode Toggle

```javascript
// Add theme toggle
function toggleTheme() {
    const root = document.documentElement;
    const isDark = root.style.getPropertyValue('--bg-main') === '#0A0A0A';
    
    if (isDark) {
        root.style.setProperty('--bg-main', '#FFFFFF');
        root.style.setProperty('--text-primary', '#000000');
        // ... other colors
    } else {
        // Reset to dark
        root.style.setProperty('--bg-main', '#0A0A0A');
        root.style.setProperty('--text-primary', '#FFFFFF');
    }
    
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}
```

---

## Performance Optimization

### Cache Frontend Assets

Add service worker for offline support:

```javascript
// sw.js
self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open('artist-hub-v1').then((cache) => {
            return cache.addAll([
                '/',
                '/styles.css',
                '/app.js',
                '/data/cache.json'
            ]);
        })
    );
});
```

### Lazy Load Images

```javascript
// Add to app.js
renderTopSongs() {
    // ... existing code ...
    
    // Add loading="lazy" to images
    img.setAttribute('loading', 'lazy');
}
```

### Reduce API Calls

Implement caching in Python script:

```python
import pickle
from datetime import datetime, timedelta

class ArtistHubAutomation:
    def __init__(self):
        self.cache_file = '.api_cache.pkl'
        self.cache = self.load_cache()
    
    def load_cache(self):
        try:
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    
    def save_api_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def fetch_spotify_artist(self, artist_id):
        cache_key = f'spotify_{artist_id}'
        
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < timedelta(hours=6):
                return cached_data
        
        # Fetch fresh data
        data = # ... API call
        
        self.cache[cache_key] = (data, datetime.now())
        self.save_api_cache()
        
        return data
```

---

## Testing

### Test Automation Locally

```bash
# Set environment variables
export SPOTIFY_CLIENT_ID="your_id"
export SPOTIFY_CLIENT_SECRET="your_secret"
export YOUTUBE_API_KEY="your_key"

# Run script
python update_data.py

# Check output
cat data/cache.json
```

### Test Frontend Locally

```bash
# Serve locally (Python 3)
python -m http.server 8000

# Open browser
open http://localhost:8000
```

### Mock Data for Testing

Create `data/cache.mock.json` for testing without APIs:

```javascript
// In app.js, update loadData()
async loadData() {
    try {
        const url = window.location.hostname === 'localhost' 
            ? 'data/cache.mock.json'
            : 'data/cache.json';
        
        const response = await fetch(url);
        this.data = await response.json();
    } catch (error) {
        this.data = this.getDemoData();
    }
}
```

---

## API Rate Limits

### Spotify API
- **Rate Limit:** None specified, but use respectfully
- **Daily Limit:** Unlimited for public data
- **Best Practice:** Cache for 6-12 hours

### YouTube API
- **Daily Quota:** 10,000 units
- **Search:** 100 units per request
- **Video stats:** 1 unit per request
- **Estimated:** ~50-100 requests per update = 5000 units
- **Safe:** 2 updates per day

### Recommendations
- Run updates every 12 hours (well within limits)
- Implement caching for repeated lookups
- Handle rate limit errors gracefully

---

## Security Best Practices

1. **Never commit API keys** to repository
2. **Use GitHub Secrets** for credentials
3. **Validate user input** in frontend
4. **Escape HTML** to prevent XSS
5. **Use HTTPS** for production
6. **Keep dependencies updated**

```bash
# Update dependencies
pip install --upgrade requests
```

---

This API documentation should help you extend and customize the A-lex Artist Hub to fit your specific needs!
