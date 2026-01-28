# 🔥 A-lex Artist Hub

A fully automated artist hub that displays what's hot right now and the latest releases from your roster. Zero maintenance after setup.

## ✨ Features

- **🏆 Top Songs Ranking** - Automatically ranked by Spotify popularity + YouTube views
- **👨‍🎤 Artist Grid** - Beautiful grid with hover/tap to see latest releases
- **🔄 Auto-Updates** - Updates every 12 hours via GitHub Actions
- **🎵 Multi-Platform** - Links to Spotify, YouTube, Apple Music, Audiomack
- **📱 Responsive** - Perfect on mobile and desktop
- **⚡ Fast** - Static site hosted free on GitHub Pages
- **🎨 Distinctive Design** - Bold, modern UI with fire theme

## 🚀 Quick Setup (30 minutes)

### 1. Fork or Clone This Repo

```bash
git clone https://github.com/YOUR_USERNAME/artist-hub.git
cd artist-hub
```

### 2. Get API Keys (All Free)

#### Spotify API
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
   - App name: "A-lex Artist Hub"
   - Redirect URI: `http://localhost` (not used but required)
4. Copy your **Client ID** and **Client Secret**

#### YouTube API (Optional but recommended)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Copy your API key

### 3. Add API Keys to GitHub Secrets

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret" and add:
   - `SPOTIFY_CLIENT_ID`: Your Spotify Client ID
   - `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret
   - `YOUTUBE_API_KEY`: Your YouTube API key (optional)

### 4. Add Your Artists

Edit `artists.json`:

```json
{
  "artists": [
    {
      "name": "BNick",
      "spotify": "https://open.spotify.com/artist/YOUR_ARTIST_ID",
      "youtube": "https://youtube.com/@bnick",
      "appleMusic": "https://music.apple.com/artist/YOUR_ARTIST_ID",
      "audiomack": "https://audiomack.com/bnick"
    },
    {
      "name": "Another Artist",
      "spotify": "https://open.spotify.com/artist/ANOTHER_ID",
      "youtube": "https://youtube.com/@another",
      "appleMusic": "https://music.apple.com/artist/ANOTHER_ID",
      "audiomack": "https://audiomack.com/another"
    }
  ],
  "config": {
    "updateFrequencyHours": 12,
    "topSongsCount": 3,
    "latestReleasesPerArtist": 5,
    "spotifyWeight": 0.7,
    "youtubeWeight": 0.3
  }
}
```

**To find Spotify Artist ID:**
1. Open artist page on Spotify
2. Click Share → Copy link to artist
3. URL format: `https://open.spotify.com/artist/ARTIST_ID`

### 5. Enable GitHub Pages

1. Go to repo Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` or `master`
4. Folder: `/ (root)`
5. Click Save

Your site will be live at: `https://YOUR_USERNAME.github.io/artist-hub/`

### 6. Trigger First Update

1. Go to Actions tab in your repo
2. Click "Update Artist Data" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait ~1-2 minutes
5. Check the "data/cache.json" file is created

## 🎯 How It Works

### Architecture

```
┌─────────────────┐
│  artists.json   │ ← You manage this (artist URLs only)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Actions  │ ← Runs every 12 hours automatically
│  update_data.py │
└────────┬────────┘
         │ Fetches from:
         ├─ Spotify API
         ├─ YouTube API
         └─ Generates rankings
         │
         ▼
┌─────────────────┐
│ data/cache.json │ ← Auto-generated, committed to repo
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GitHub Pages   │ ← Website loads cache.json
│  index.html     │
└─────────────────┘
```

### Ranking Algorithm

**Top Songs Score:**
```
score = (Spotify Popularity × 0.7) + (Normalized YouTube Views × 0.3)
```

- Spotify popularity: 0-100 scale
- YouTube views: Normalized to 0-100 (1M views = 100 points)
- Top 3 songs displayed on homepage

**Latest Releases:**
- Sorted by release date (newest first)
- 5 most recent per artist shown in modal

## 📁 Project Structure

```
artist-hub/
├── index.html              # Main homepage
├── styles.css             # Styling (fire theme)
├── app.js                 # Frontend logic
├── artists.json           # YOUR ARTISTS CONFIG
├── update_data.py         # Automation script
├── requirements.txt       # Python dependencies
├── data/
│   └── cache.json        # Auto-generated cache
└── .github/
    └── workflows/
        └── update-data.yml # Automation workflow
```

## 🎨 Customization

### Change Update Frequency

Edit `.github/workflows/update-data.yml`:

```yaml
on:
  schedule:
    # Every 6 hours: '0 */6 * * *'
    # Every 24 hours: '0 0 * * *'
    - cron: '0 */12 * * *'
```

### Change Colors/Theme

Edit `styles.css` variables:

```css
:root {
    --primary: #FF4500;        /* Main accent color */
    --accent: #FFD700;         /* Secondary accent */
    --bg-main: #0A0A0A;        /* Background */
    /* ... */
}
```

### Adjust Ranking Weights

Edit `artists.json`:

```json
"config": {
  "spotifyWeight": 0.7,  // Higher = Spotify matters more
  "youtubeWeight": 0.3,  // Higher = YouTube matters more
  "topSongsCount": 3     // How many top songs to show
}
```

## 🔧 Troubleshooting

### Automation not running?
1. Check Actions tab → ensure workflow is enabled
2. Verify API keys are added as secrets (not in code)
3. Check workflow logs for errors

### No data showing?
1. Run workflow manually first time
2. Check `data/cache.json` exists
3. Open browser console (F12) for errors
4. Ensure artists.json has valid Spotify URLs

### Wrong songs showing?
1. Check Spotify URLs are correct artist pages
2. Verify API keys are valid
3. Re-run workflow to refresh data

### YouTube not working?
- YouTube API is optional
- Without it, ranking uses Spotify only
- Get free API key for full functionality

## 💰 Cost Breakdown

| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| GitHub Pages | ✅ Unlimited public repos | Hosting | **$0** |
| GitHub Actions | ✅ 2,000 min/month | ~2 min per update | **$0** |
| Spotify API | ✅ Unlimited | Artist/track data | **$0** |
| YouTube API | ✅ 10,000 quota/day | ~50 quota per update | **$0** |
| **Total** | | | **$0/month** |

## 🚀 Going Live

### Option 1: GitHub Pages (Free)
Your site: `https://username.github.io/artist-hub/`

### Option 2: Custom Domain (Optional)
1. Buy domain ($10-15/year)
2. In repo settings → Pages → Custom domain
3. Add CNAME record in DNS

## 📊 What Gets Updated Automatically

✅ **Every 12 hours:**
- Artist images
- Latest releases
- Top songs ranking
- Spotify popularity scores
- YouTube view counts
- Platform links

❌ **You never touch:**
- HTML/CSS/JS files
- cache.json
- Rankings
- Song metadata

✅ **You only manage:**
- `artists.json` (when adding/removing artists)

## 🎯 Next Steps

### Phase 2 Features (Optional)
- [ ] Individual artist pages (`/artist/artist-name`)
- [ ] Analytics dashboard
- [ ] AI-powered insights
- [ ] Playlist generation
- [ ] Fan engagement metrics

### Need Help?
- Check workflow logs in Actions tab
- Verify all API keys are set correctly
- Ensure artists.json has valid URLs
- Check browser console for frontend errors

## 📝 License

MIT License - Use freely for your artist hub!

---

**Built with 🔥 for artists by A-lex**

*Auto-updates, zero maintenance, completely free.*
