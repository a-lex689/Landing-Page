# ⚡ Quick Start - 15 Minutes to Live

Get your A-lex Artist Hub running in 4 simple steps.

## Prerequisites
- GitHub account (free)
- Spotify account (free)

---

## Step 1: Create Repository (2 min)

1. Create new repo on GitHub
2. Upload all these files to it
3. Commit to `main` branch

**Or via command line:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/artist-hub.git
git push -u origin main
```

---

## Step 2: Get Spotify API Keys (5 min)

1. Go to: https://developer.spotify.com/dashboard
2. Log in with Spotify
3. Click "Create App"
   - Name: `Artist Hub`
   - Redirect: `http://localhost`
4. Copy **Client ID** and **Client Secret**

---

## Step 3: Add Secrets to GitHub (3 min)

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** twice:

   **First secret:**
   - Name: `SPOTIFY_CLIENT_ID`
   - Value: [paste your Client ID]

   **Second secret:**
   - Name: `SPOTIFY_CLIENT_SECRET`
   - Value: [paste your Client Secret]

---

## Step 4: Configure & Deploy (5 min)

### A. Add Your Artists

Edit `artists.json`:
```json
{
  "artists": [
    {
      "name": "Your Artist Name",
      "spotify": "https://open.spotify.com/artist/ARTIST_ID",
      "youtube": "https://youtube.com/@channel",
      "appleMusic": "",
      "audiomack": ""
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

**To get Spotify URL:**
- Open Spotify → Search artist → Click artist → Share → Copy link

### B. Enable GitHub Pages

1. Repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main**
4. Folder: **/ (root)**
5. Click **Save**

### C. Run First Update

1. Go to **Actions** tab
2. Click **Update Artist Data** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait 1-2 minutes

---

## ✅ Done!

Your site is live at:
```
https://YOUR_USERNAME.github.io/artist-hub/
```

**Auto-updates every 12 hours** with latest:
- Top songs
- Artist releases
- YouTube views
- Platform links

---

## What You Just Built

✅ Fully automated artist hub  
✅ Multi-platform integration  
✅ Auto-ranking by popularity  
✅ Zero maintenance needed  
✅ Completely free hosting  
✅ Professional responsive design  

---

## Next Steps (Optional)

- Add YouTube API for view counts (see DEPLOYMENT.md)
- Customize colors in `styles.css`
- Add custom domain
- Check out API.md for advanced features

---

## Need Help?

**Check these in order:**
1. Actions tab → Click latest workflow → Check for errors
2. `data/cache.json` → Should have your artist data
3. Browser console (F12) → Check for JavaScript errors
4. DEPLOYMENT.md → Full troubleshooting guide

**Common Issues:**
- Demo data showing? → Run workflow manually
- Workflow failed? → Check API keys in Secrets
- Site not loading? → Wait 5 min after enabling Pages

---

**🔥 Enjoy your automated artist hub!**
