fetch("releases.json")
  .then(res => res.json())
  .then(data => {
    const wall = document.getElementById("music-wall");

    data.forEach(song => {
      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <img src="${song.cover}" />
        <h3>${song.title}</h3>
        <p>${song.artist}</p>
        <div class="links">
          <a href="${song.links.spotify}" target="_blank">Spotify</a>
          <a href="${song.links.audiomack}" target="_blank">Audiomack</a>
          <a href="${song.links.youtube}" target="_blank">YouTube</a>
        </div>
      `;

      wall.appendChild(card);
    });
  });
