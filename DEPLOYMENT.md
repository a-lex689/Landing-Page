# 🚀 Deployment Guide

Complete step-by-step guide to deploy your A-lex Artist Hub.

## Prerequisites

- GitHub account (free)
- Spotify account (free)
- 30 minutes

## Step-by-Step Deployment

### Step 1: Create Your Repository

#### Option A: Use This Template
1. Click "Use this template" button on GitHub
2. Name your repo: `artist-hub` (or anything you want)
3. Set to Public (required for free GitHub Pages)
4. Click "Create repository"

#### Option B: Fork
1. Click "Fork" button
2. Your fork will be created

#### Option C: Manual Clone
```bash
git clone https://github.com/YOUR_USERNAME/artist-hub.git
cd artist-hub
git remote set-url origin https://github.com/YOUR_NEW_USERNAME/YOUR_NEW_REPO.git
git push -u origin main
```

---

### Step 2: Get Spotify API Credentials

1. **Go to Spotify Developer Dashboard**
   - URL: https://developer.spotify.com/dashboard
   - Log in with your Spotify account

2. **Create an App**
   - Click "Create App"
   - Fill in:
     - App name: `A-lex Artist Hub`
     - App description: `Artist hub automation`
     - Redirect URI: `http://localhost`
     - Check "Web API"
   - Click "Save"

3. **Get Your Credentials**
   - Click on your new app
   - Click "Settings"
   - Copy these values:
     - **Client ID** (looks like: `abc123def456...`)
     - **Client Secret** (click "View client secret")

⚠️ **Keep these secret!** Never commit them to your code.

---

### Step 3: Get YouTube API Key (Optional)

YouTube integration adds view counts to ranking. It's optional but recommended.

1. **Go to Google Cloud Console**
   - URL: https://console.cloud.google.com/

2. **Create a Project**
   - Click project dropdown → "New Project"
   - Name: `Artist Hub`
   - Click "Create"

3. **Enable YouTube Data API**
   - In the search bar, type "YouTube Data API v3"
   - Click on it → Click "Enable"

4. **Create API Key**
   - Go to "Credentials" in left sidebar
   - Click "Create Credentials" → "API Key"
   - Copy the API key
   - Click "Restrict Key" (recommended)
     - API restrictions: "YouTube Data API v3"
     - Save

---

### Step 4: Add Secrets to GitHub

1. **Go to Your Repository Settings**
   - Click "Settings" tab (top right)
   - Click "Secrets and variables" → "Actions" (left sidebar)

2. **Add Repository Secrets**
   Click "New repository secret" for each:

   **Secret 1:**
   - Name: `SPOTIFY_CLIENT_ID`
   - Value: *paste your Spotify Client ID*
   - Click "Add secret"

   **Secret 2:**
   - Name: `SPOTIFY_CLIENT_SECRET`
   - Value: *paste your Spotify Client Secret*
   - Click "Add secret"

   **Secret 3 (optional):**
   - Name: `YOUTUBE_API_KEY`
   - Value: *paste your YouTube API key*
   - Click "Add secret"

✅ Your secrets are now secure and encrypted.

---

### Step 5: Configure Your Artists

1. **Find Your Artists' Spotify URLs**

   For each artist:
   - Open Spotify (web or app)
   - Search for the artist
   - Click on their profile
   - Click "Share" → "Copy link to artist"
   - URL will look like: `https://open.spotify.com/artist/4dpARuHxo51G3z768sgnrY`

2. **Edit `artists.json`**

   In your GitHub repo:
   - Click on `artists.json` file
   - Click the pencil icon (Edit)
   - Replace the example with your artists:

   ```json
   {
     "artists": [
       {
         "name": "Drake",
         "spotify": "https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4",
         "youtube": "https://youtube.com/@Drake",
         "appleMusic": "https://music.apple.com/us/artist/drake/271256",
         "audiomack": "https://audiomack.com/drake"
       },
       {
         "name": "The Weeknd",
         "spotify": "https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ",
         "youtube": "https://youtube.com/@theweeknd",
         "appleMusic": "https://music.apple.com/us/artist/the-weeknd/479756766",
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

   - **Required:** `name`, `spotify`
   - **Optional:** `youtube`, `appleMusic`, `audiomack` (leave as empty string `""` if not available)

3. **Commit Changes**
   - Scroll down
   - Click "Commit changes"
   - Add commit message: "Add my artists"
   - Click "Commit changes"

---

### Step 6: Enable GitHub Pages

1. **Go to Repository Settings**
   - Click "Settings" tab
   - Scroll down to "Pages" (left sidebar)

2. **Configure Source**
   - Source: "Deploy from a branch"
   - Branch: `main` (or `master`)
   - Folder: `/ (root)`
   - Click "Save"

3. **Wait for Deployment**
   - Go to "Actions" tab
   - You'll see a "pages build and deployment" workflow running
   - Wait 1-2 minutes for it to complete

4. **Get Your URL**
   - Go back to Settings → Pages
   - Your site URL will show at top:
     ```
     Your site is live at https://YOUR_USERNAME.github.io/artist-hub/
     ```

🎉 **Your site is now live!** (But it's showing demo data)

---

### Step 7: Run First Data Update

1. **Go to Actions Tab**
   - Click "Actions" at top of repo

2. **Find the Workflow**
   - Click "Update Artist Data" in left sidebar

3. **Run Manually**
   - Click "Run workflow" (blue button, top right)
   - Branch: `main`
   - Click "Run workflow"

4. **Wait for Completion**
   - Watch the workflow run (takes 1-2 minutes)
   - It will show ✅ when complete

5. **Verify the Update**
   - Click on the completed workflow run
   - Check for errors (should all be green ✅)
   - Go to your repo, navigate to `data/cache.json`
   - You should see real data for your artists!

6. **Refresh Your Website**
   - Open your GitHub Pages URL
   - Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
   - You should now see your real artists and songs! 🔥

---

## Post-Deployment

### ✅ What's Automated Now

From this point forward:

- **Every 12 hours:** Data auto-updates
  - Runs at 00:00 UTC and 12:00 UTC
  - Fetches latest Spotify data
  - Fetches YouTube views
  - Ranks songs
  - Commits new cache.json
  - GitHub Pages auto-deploys

- **Whenever you edit `artists.json`:**
  - Workflow runs automatically
  - Updates within 2-3 minutes

### 🎯 Your Only Maintenance

- **Add/remove artists:** Edit `artists.json`
- That's it! ✨

---

## Verification Checklist

After deployment, verify:

- [ ] Site is live at GitHub Pages URL
- [ ] Top songs section shows real data
- [ ] Artist grid shows your artists
- [ ] Clicking an artist opens modal with releases
- [ ] Platform links work (Spotify, YouTube, etc.)
- [ ] "Last updated" shows recent timestamp
- [ ] Workflow runs successfully in Actions tab

---

## Troubleshooting

### Site shows demo data after workflow runs

**Solution:**
1. Check Actions tab → Click on latest workflow run
2. Look for errors in logs
3. Verify API keys are correct in Secrets
4. Make sure `artists.json` has valid Spotify URLs
5. Wait 2-3 minutes after workflow completes
6. Hard refresh browser (Ctrl+Shift+R)

### Workflow fails with "401 Unauthorized"

**Solution:**
- Spotify credentials are wrong
- Double-check Client ID and Secret in GitHub Secrets
- Make sure you copied the full values (no spaces)

### Workflow runs but cache.json doesn't update

**Solution:**
1. Check workflow logs for Python errors
2. Verify Spotify URLs in `artists.json` are valid artist URLs
3. Try running workflow manually again

### Artist shows but no releases

**Possible reasons:**
- Artist has no releases on Spotify
- Artist ID is wrong (check URL)
- Recent releases not yet on Spotify

### YouTube views not showing

**Reasons:**
- YouTube API key not set (it's optional)
- API key has no quota left (10k requests/day free)
- YouTube video not found for that track

### Site not accessible

**Solution:**
1. Settings → Pages → Verify it's enabled
2. Check branch is correct (`main` or `master`)
3. Wait 5 minutes after enabling
4. Try incognito/private browsing

---

## Next Steps

### Add Custom Domain (Optional)

1. **Buy a domain** (Namecheap, Google Domains, etc.)

2. **Add to GitHub Pages**
   - Settings → Pages
   - Custom domain: `yourdomain.com`
   - Click Save

3. **Configure DNS**
   Add these records at your domain provider:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: A
   Name: @
   Value: 185.199.110.153
   
   Type: A
   Name: @
   Value: 185.199.111.153
   
   Type: CNAME
   Name: www
   Value: YOUR_USERNAME.github.io
   ```

4. **Wait for DNS** (can take 24-48 hours)

5. **Enable HTTPS** (in GitHub Pages settings)

---

## Support

**Common Resources:**
- [Spotify API Docs](https://developer.spotify.com/documentation/web-api)
- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

**Check These First:**
1. GitHub Actions logs (Actions tab → Click workflow run)
2. Browser console (F12) for frontend errors
3. `data/cache.json` for data structure

---

**🔥 Congratulations!** Your artist hub is now fully automated and running! 🎉
