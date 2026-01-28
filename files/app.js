// A-lex Artist Hub - Main Application Logic

class ArtistHub {
    constructor() {
        this.data = null;
        this.artists = [];
        this.topSongs = [];
        this.init();
    }

    async init() {
        await this.loadData();
        this.renderTopSongs();
        this.renderArtists();
        this.setupEventListeners();
        this.updateLastUpdateTime();
    }

    async loadData() {
        try {
            // In production, this will fetch from /data/cache.json
            // For now, we'll use mock data
            const response = await fetch('data/cache.json').catch(() => null);
            
            if (response && response.ok) {
                this.data = await response.json();
            } else {
                // Use mock data for development
                this.data = this.getMockData();
            }

            this.processData();
        } catch (error) {
            console.error('Error loading data:', error);
            this.data = this.getMockData();
            this.processData();
        }
    }

    processData() {
        // Extract artists
        this.artists = this.data.artists || [];
        
        // Extract and rank top songs
        this.topSongs = this.calculateTopSongs();
    }

    calculateTopSongs() {
        const allSongs = [];

        // Collect all songs from all artists
        this.artists.forEach(artist => {
            if (artist.tracks && artist.tracks.length > 0) {
                artist.tracks.forEach(track => {
                    allSongs.push({
                        ...track,
                        artistName: artist.name,
                        artistImage: artist.image
                    });
                });
            }
        });

        // Calculate composite score and sort
        allSongs.forEach(song => {
            const spotifyScore = (song.popularity || 0) * 0.7;
            const youtubeScore = this.normalizeYoutubeViews(song.youtubeViews || 0) * 0.3;
            song.compositeScore = spotifyScore + youtubeScore;
        });

        // Sort by composite score and return top 3
        return allSongs
            .sort((a, b) => b.compositeScore - a.compositeScore)
            .slice(0, 3);
    }

    normalizeYoutubeViews(views) {
        // Normalize YouTube views to 0-100 scale
        // Assumes 10M views = 100 score
        const maxViews = 10000000;
        return Math.min((views / maxViews) * 100, 100);
    }

    renderTopSongs() {
        const grid = document.getElementById('top-songs-grid');
        
        if (this.topSongs.length === 0) {
            grid.innerHTML = '<div class="loading-state"><p>No tracks available yet</p></div>';
            return;
        }

        grid.innerHTML = this.topSongs.map((song, index) => `
            <div class="song-card">
                <div class="song-rank">#${index + 1}</div>
                <img src="${song.coverArt || 'https://via.placeholder.com/400'}" 
                     alt="${song.title}" 
                     class="song-cover">
                <div class="song-info">
                    <h3 class="song-title">${this.escapeHtml(song.title)}</h3>
                    <p class="song-artist">${this.escapeHtml(song.artistName)}</p>
                    <div class="song-platforms">
                        ${song.spotifyUrl ? `
                            <a href="${song.spotifyUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn spotify">
                                <span>♫</span> Spotify
                            </a>
                        ` : ''}
                        ${song.youtubeUrl ? `
                            <a href="${song.youtubeUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn youtube">
                                <span>▶</span> YouTube
                            </a>
                        ` : ''}
                        ${song.appleMusicUrl ? `
                            <a href="${song.appleMusicUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn apple">
                                <span>🍎</span> Apple
                            </a>
                        ` : ''}
                        ${song.audiomackUrl ? `
                            <a href="${song.audiomackUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn audiomack">
                                <span>🎵</span> Audiomack
                            </a>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderArtists() {
        const grid = document.getElementById('artists-grid');
        
        if (this.artists.length === 0) {
            grid.innerHTML = '<div class="loading-state"><p>No artists available yet</p></div>';
            return;
        }

        grid.innerHTML = this.artists.map(artist => `
            <div class="artist-card" data-artist-id="${artist.id}">
                <div class="artist-image-wrapper">
                    <img src="${artist.image || 'https://via.placeholder.com/400'}" 
                         alt="${artist.name}" 
                         class="artist-image">
                    <div class="artist-overlay">
                        <h3 class="artist-name">${this.escapeHtml(artist.name)}</h3>
                    </div>
                </div>
            </div>
        `).join('');
    }

    setupEventListeners() {
        // Artist card clicks
        document.getElementById('artists-grid').addEventListener('click', (e) => {
            const card = e.target.closest('.artist-card');
            if (card) {
                const artistId = card.dataset.artistId;
                this.showArtistModal(artistId);
            }
        });

        // Modal close
        document.getElementById('modal-close').addEventListener('click', () => {
            this.closeArtistModal();
        });

        document.getElementById('modal-backdrop').addEventListener('click', () => {
            this.closeArtistModal();
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeArtistModal();
            }
        });
    }

    showArtistModal(artistId) {
        const artist = this.artists.find(a => a.id === artistId);
        if (!artist) return;

        const modal = document.getElementById('artist-modal');
        const modalImage = document.getElementById('modal-artist-image');
        const modalName = document.getElementById('modal-artist-name');
        const modalTracks = document.getElementById('modal-tracks');

        modalImage.src = artist.image || 'https://via.placeholder.com/400';
        modalName.textContent = artist.name;

        const latestTracks = (artist.tracks || []).slice(0, 5);
        
        if (latestTracks.length === 0) {
            modalTracks.innerHTML = '<p style="color: var(--text-muted);">No releases yet</p>';
        } else {
            modalTracks.innerHTML = latestTracks.map(track => `
                <div class="modal-track">
                    <h4 class="modal-track-title">${this.escapeHtml(track.title)}</h4>
                    <div class="modal-track-platforms">
                        ${track.spotifyUrl ? `
                            <a href="${track.spotifyUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn spotify">
                                <span>♫</span> Spotify
                            </a>
                        ` : ''}
                        ${track.youtubeUrl ? `
                            <a href="${track.youtubeUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn youtube">
                                <span>▶</span> YouTube
                            </a>
                        ` : ''}
                        ${track.appleMusicUrl ? `
                            <a href="${track.appleMusicUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn apple">
                                <span>🍎</span> Apple
                            </a>
                        ` : ''}
                        ${track.audiomackUrl ? `
                            <a href="${track.audiomackUrl}" 
                               target="_blank" 
                               rel="noopener noreferrer" 
                               class="platform-btn audiomack">
                                <span>🎵</span> Audiomack
                            </a>
                        ` : ''}
                    </div>
                </div>
            `).join('');
        }

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    closeArtistModal() {
        const modal = document.getElementById('artist-modal');
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    updateLastUpdateTime() {
        const updateElement = document.getElementById('last-update');
        if (this.data && this.data.lastUpdated) {
            const lastUpdate = new Date(this.data.lastUpdated);
            const now = new Date();
            const diffMinutes = Math.floor((now - lastUpdate) / 1000 / 60);
            
            if (diffMinutes < 60) {
                updateElement.textContent = `Updated ${diffMinutes} minutes ago`;
            } else if (diffMinutes < 1440) {
                const hours = Math.floor(diffMinutes / 60);
                updateElement.textContent = `Updated ${hours} hour${hours > 1 ? 's' : ''} ago`;
            } else {
                updateElement.textContent = `Updated ${lastUpdate.toLocaleDateString()}`;
            }
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    getMockData() {
        // Mock data for development and demonstration
        return {
            lastUpdated: new Date().toISOString(),
            artists: [
                {
                    id: 'bnick',
                    name: 'BNick',
                    image: 'https://i.scdn.co/image/ab6761610000e5eb8c1e066b5c1d3f6b2b3c8e1a',
                    spotify: 'https://open.spotify.com/artist/example',
                    youtube: 'https://youtube.com/@bnick',
                    appleMusic: 'https://music.apple.com/artist/example',
                    audiomack: 'https://audiomack.com/bnick',
                    tracks: [
                        {
                            id: 'track1',
                            title: 'Summer Nights',
                            coverArt: 'https://i.scdn.co/image/ab67616d0000b273a1b5c3d7e8f9a2b4c5d6e7f8',
                            releaseDate: '2026-01-15',
                            popularity: 85,
                            youtubeViews: 2500000,
                            spotifyUrl: 'https://open.spotify.com/track/example1',
                            youtubeUrl: 'https://youtube.com/watch?v=example1',
                            appleMusicUrl: 'https://music.apple.com/song/example1',
                            audiomackUrl: 'https://audiomack.com/song/example1'
                        },
                        {
                            id: 'track2',
                            title: 'Midnight Drive',
                            coverArt: 'https://i.scdn.co/image/ab67616d0000b273b2c3d4e5f6a7b8c9d0e1f2a3',
                            releaseDate: '2025-12-20',
                            popularity: 78,
                            youtubeViews: 1800000,
                            spotifyUrl: 'https://open.spotify.com/track/example2',
                            youtubeUrl: 'https://youtube.com/watch?v=example2',
                            appleMusicUrl: 'https://music.apple.com/song/example2'
                        }
                    ]
                },
                {
                    id: 'artist2',
                    name: 'Luna Wave',
                    image: 'https://i.scdn.co/image/ab6761610000e5ebc4d5e6f7a8b9c0d1e2f3a4b5',
                    spotify: 'https://open.spotify.com/artist/example2',
                    tracks: [
                        {
                            id: 'track3',
                            title: 'Ocean Dreams',
                            coverArt: 'https://i.scdn.co/image/ab67616d0000b273c5d6e7f8a9b0c1d2e3f4a5b6',
                            releaseDate: '2026-01-10',
                            popularity: 92,
                            youtubeViews: 5000000,
                            spotifyUrl: 'https://open.spotify.com/track/example3',
                            youtubeUrl: 'https://youtube.com/watch?v=example3'
                        }
                    ]
                },
                {
                    id: 'artist3',
                    name: 'Echo Rivera',
                    image: 'https://i.scdn.co/image/ab6761610000e5ebd6e7f8a9b0c1d2e3f4a5b6c7',
                    spotify: 'https://open.spotify.com/artist/example3',
                    tracks: [
                        {
                            id: 'track4',
                            title: 'City Lights',
                            coverArt: 'https://i.scdn.co/image/ab67616d0000b273d7e8f9a0b1c2d3e4f5a6b7c8',
                            releaseDate: '2026-01-05',
                            popularity: 88,
                            youtubeViews: 3200000,
                            spotifyUrl: 'https://open.spotify.com/track/example4'
                        }
                    ]
                }
            ]
        };
    }
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ArtistHub();
    });
} else {
    new ArtistHub();
}
