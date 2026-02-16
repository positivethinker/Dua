
import os

new_header = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dua Player Pro</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0f172a;
            --bg-sec: #1e293b;
            --text-main: #f8fafc;
            --text-sec: #94a3b8;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.2);
            --border: #334155;
        }
        * { box-sizing: border-box; }
        body { margin: 0; font-family: 'Inter', sans-serif; background: var(--bg-main); color: var(--text-main); height: 100vh; overflow: hidden; display: flex; }
        .sidebar { width: 320px; background: var(--bg-sec); border-right: 1px solid var(--border); display: flex; flex-direction: column; height: 100%; transition: transform 0.3s; }
        .logo { padding: 20px; border-bottom: 1px solid var(--border); }
        .logo h1 { font-family: 'Playfair Display', serif; margin: 0; font-size: 1.5rem; background: linear-gradient(45deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .playlist { flex: 1; overflow-y: auto; padding: 10px; }
        .section-item { margin-bottom: 8px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: #182235; }
        .section-header { padding: 12px 16px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.03); transition: background 0.2s; font-weight: 500; font-size: 0.95rem; }
        .section-header:hover { background: rgba(255,255,255,0.05); }
        .section-header.active { background: var(--border); }
        .video-list { list-style: none; margin: 0; padding: 0; display: none; }
        .video-list.open { display: block; }
        .video-item { padding: 10px 16px; border-top: 1px solid var(--border); font-size: 0.9rem; color: var(--text-sec); cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }
        .video-item:hover { background: rgba(56, 189, 248, 0.1); color: var(--accent); }
        .video-item.active { background: var(--accent-glow); color: var(--accent); border-left: 3px solid var(--accent); }
        .video-loop-badge { font-size: 0.75rem; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; margin-left: auto; color: var(--accent); }
        .main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; padding: 20px; gap: 20px; align-items: center; }
        .player-card { width: 100%; max-width: 900px; aspect-ratio: 16/9; background: #000; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid var(--border); }
        #player { width: 100%; height: 100%; }
        .controls-card { width: 100%; max-width: 900px; background: var(--bg-sec); border-radius: 12px; padding: 20px; border: 1px solid var(--border); display: flex; flex-direction: column; gap: 16px; }
        .info-row { text-align: center; }
        .video-title { font-size: 1.25rem; font-weight: 600; margin: 0 0 8px 0; color: var(--text-main); }
        .tooltip { font-size: 0.95rem; color: var(--text-sec); font-style: italic; min-height: 1.4rem; }
        .stats-row { display: flex; justify-content: center; gap: 30px; margin-top: 10px; flex-wrap: wrap; }
        .stat-badge { background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 8px; font-size: 0.9rem; display: flex; align-items: center; gap: 8px; border: 1px solid var(--border); }
        .stat-value { font-weight: 700; color: var(--accent); font-size: 1.1rem; }
        .actions-row { display: flex; justify-content: center; gap: 16px; margin-top: 10px; }
        .btn { padding: 10px 24px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; transition: transform 0.1s, opacity 0.2s; display: flex; align-items: center; gap: 8px; }
        .btn:active { transform: scale(0.98); }
        .btn-primary { background: var(--accent); color: #0f172a; }
        .btn-primary:hover { opacity: 0.9; }
        .btn-secondary { background: transparent; border: 1px solid var(--border); color: var(--text-main); }
        .btn-secondary:hover { background: rgba(255,255,255,0.05); }
        .mobile-toggle { display: none; position: fixed; bottom: 20px; right: 20px; z-index: 100; padding: 12px; border-radius: 50%; width: 50px; height: 50px; justify-content: center; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); background: var(--accent); color: #000; font-size: 1.5rem; border: none;}
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
        @media (max-width: 900px) {
            .sidebar { position: fixed; left: -320px; top: 0; bottom: 0; z-index: 50; box-shadow: 10px 0 30px rgba(0,0,0,0.5); }
            .sidebar.active { transform: translateX(320px); left: 0; }
            .mobile-toggle { display: flex; }
            .main-content { padding: 10px; }
            .player-card { border-radius: 0; width: 100vw; max-width: 100vw; margin: -10px -10px 20px -10px; }
        }
    </style>
</head>
<body>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
    <aside class="sidebar" id="sidebar">
        <div class="logo">
            <h1>Dua Player</h1>
            <div style="font-size: 0.8rem; color: #64748b; margin-top:4px;">Modern Edition</div>
        </div>
        <div class="playlist" id="playlist"></div>
        <div style="padding: 16px; border-top: 1px solid var(--border); text-align: center;">
             <a href="admin.html" style="color: var(--text-sec); text-decoration: none; font-size: 0.8rem; margin-right: 15px;">🛠️ Admin</a>
             <button onclick="copyDataForAdmin()" style="background: none; border: none; color: var(--accent); cursor: pointer; font-size: 0.8rem;">📋 Copy Data</button>
        </div>
    </aside>
    <main class="main-content">
        <div class="player-card">
            <div id="player"></div>
        </div>
        <div class="controls-card">
            <div class="info-row">
                <h2 class="video-title" id="videoTitle">Ready to Play</h2>
                <div class="tooltip" id="tooltip">Select a section from the playlist to begin</div>
            </div>
            <div class="stats-row">
                <div class="stat-badge">
                    <span>Repeat</span>
                    <span class="stat-value"><span id="currentLoop">0</span>/<span id="maxLoop">-</span></span>
                </div>
                <div class="stat-badge">
                    <span>Remaining</span>
                    <span class="stat-value" id="remainingTime">--:--</span>
                </div>
                <div class="stat-badge" id="allTimerBadge" style="display:none;">
                    <span>Total</span>
                    <span class="stat-value" id="allTimer">--:--</span>
                </div>
            </div>
            <div class="actions-row">
                 <button class="btn btn-secondary" onclick="playAllSections()">▶ Play All</button>
                 <button class="btn btn-primary" onclick="skipVideo()">Skip ⏭</button>
            </div>
        </div>
    </main>
    <script src="https://www.youtube.com/iframe_api"></script>
    <script>
"""

new_footer = r"""
      let videoSections;
      try {
        const stored = localStorage.getItem("duaDarudVideoSections");
        if (stored) {
          const parsed = JSON.parse(stored);
          if (Array.isArray(parsed) && parsed.length > 0) videoSections = parsed;
        }
      } catch (e) {}
      if (!videoSections) videoSections = defaultVideoSections;

      let player, playerReady = false;
      let currentState = { sectionIndex: -1, videoIndex: -1, loopCount: 0, maxLoops: 0, isPlaying: false, isAllMode: false, allSectionIndex: 0 };
      let timers = { section: null, all: null, loopCheck: null };

      function onYouTubeIframeAPIReady() {
          player = new YT.Player("player", {
              height: "100%", width: "100%", videoId: "",
              playerVars: { modestbranding: 1, rel: 0, autoplay: 0, playsinline: 1 },
              events: { onReady: () => { playerReady = true; renderPlaylist(); }, onStateChange: onPlayerStateChange }
          });
      }

      function renderPlaylist() {
          const container = document.getElementById("playlist");
          container.innerHTML = "";
          videoSections.forEach((section, sIdx) => {
              const div = document.createElement("div");
              div.className = "section-item";
              const header = document.createElement("div");
              header.className = "section-header";
              header.innerHTML = `<span>${section.name}</span> <span style="font-size:0.8em">▼</span>`;
              header.onclick = () => toggleSection(sIdx);
              const ul = document.createElement("ul");
              ul.className = "video-list";
              ul.id = `list-${sIdx}`;
              section.videos.forEach((vid, vIdx) => {
                  const li = document.createElement("li");
                  li.className = "video-item";
                  li.id = `vid-${sIdx}-${vIdx}`;
                  if (vid.isSubcategory) {
                      li.style.fontWeight = "bold"; li.style.color = "#94a3b8"; li.style.borderTop = "1px solid #334155"; li.style.background = "#0f172a"; li.style.cursor = "default"; li.textContent = vid.label;
                  } else {
                      li.onclick = () => playSingleSection(sIdx, vIdx);
                      li.innerHTML = `<span>${vid.label}</span>${vid.loop > 1 ? `<span class="video-loop-badge">x${vid.loop}</span>` : ''}`;
                  }
                  ul.appendChild(li);
              });
              div.appendChild(header); div.appendChild(ul); container.appendChild(div);
          });
      }

      function toggleSection(idx) {
          const list = document.getElementById(`list-${idx}`);
          const wasOpen = list.classList.contains("open");
          document.querySelectorAll(".video-list").forEach(el => el.classList.remove("open"));
          document.querySelectorAll(".section-header").forEach(el => el.classList.remove("active"));
          if (!wasOpen) { list.classList.add("open"); list.previousElementSibling.classList.add("active"); }
      }

      function toggleSidebar() { document.getElementById("sidebar").classList.toggle("active"); }

      function playSingleSection(sIdx, vIdx = 0) {
          currentState.isAllMode = false; currentState.sectionIndex = sIdx;
          let validIdx = vIdx;
          while(validIdx < videoSections[sIdx].videos.length && videoSections[sIdx].videos[validIdx].isSubcategory) validIdx++;
          if(validIdx >= videoSections[sIdx].videos.length) return;
          startVideo(sIdx, validIdx);
          toggleSection(sIdx);
          if (window.innerWidth <= 900) toggleSidebar(); 
      }

      function playAllSections() {
          currentState.isAllMode = true; currentState.allSectionIndex = 0;
          playSingleSection(0, 0);
          document.getElementById("allTimerBadge").style.display = "flex";
      }

      function startVideo(sIdx, vIdx) {
          const video = videoSections[sIdx].videos[vIdx];
          currentState.sectionIndex = sIdx; currentState.videoIndex = vIdx;
          currentState.loopCount = 0; currentState.maxLoops = video.loop || 1;
          document.querySelectorAll(".video-item").forEach(el => el.classList.remove("active"));
          const el = document.getElementById(`vid-${sIdx}-${vIdx}`);
          if(el) el.classList.add("active");
          document.getElementById("videoTitle").textContent = video.label;
          document.getElementById("tooltip").textContent = video.tooltip || "";
          updateStats();
          if(player && player.loadVideoById) { player.loadVideoById({ videoId: video.id, startSeconds: video.start }); }
      }
      
      function onPlayerStateChange(event) {
          if (event.data === YT.PlayerState.PLAYING) startLoopCheck();
          else clearInterval(timers.loopCheck);
          if (event.data === YT.PlayerState.ENDED) handleVideoEnd();
      }

      function startLoopCheck() {
          clearInterval(timers.loopCheck);
          timers.loopCheck = setInterval(() => {
              if(!player || !player.getCurrentTime) return;
              const cur = player.getCurrentTime();
              const v = videoSections[currentState.sectionIndex].videos[currentState.videoIndex];
              if (cur >= v.end) handleVideoEnd();
              const remaining = Math.max(0, v.end - cur);
              document.getElementById("remainingTime").textContent = formatTime(remaining);
          }, 500);
      }

      function handleVideoEnd() {
          currentState.loopCount++; updateStats();
          const v = videoSections[currentState.sectionIndex].videos[currentState.videoIndex];
          if (currentState.loopCount < currentState.maxLoops) { player.seekTo(v.start); player.playVideo(); }
          else nextVideo();
      }

      function nextVideo() {
          let sIdx = currentState.sectionIndex; let vIdx = currentState.videoIndex + 1;
          const section = videoSections[sIdx];
          while(vIdx < section.videos.length && section.videos[vIdx].isSubcategory) vIdx++;
          if(vIdx < section.videos.length) startVideo(sIdx, vIdx);
          else {
              if (currentState.isAllMode) {
                  const nextSec = sIdx + 1;
                  if (nextSec < videoSections.length) playSingleSection(nextSec, 0);
                  else stop();
              } else stop();
          }
      }

      function skipVideo() { nextVideo(); }
      function stop() { player.stopVideo(); document.getElementById("videoTitle").textContent = "Completed"; clearInterval(timers.loopCheck); }
      function updateStats() { document.getElementById("currentLoop").textContent = currentState.loopCount + 1; document.getElementById("maxLoop").textContent = currentState.maxLoops; }
      function formatTime(s) { const m = Math.floor(s / 60); const sec = Math.floor(s % 60); return `${m}:${sec < 10 ? '0'+sec : sec}`; }
      function copyDataForAdmin() { navigator.clipboard.writeText(JSON.stringify(videoSections, null, 2)); alert("Data copied!"); }
    </script>
</body>
</html>
"""

def migrate():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_idx = -1
        end_idx = -1
        
        # Locate the data block
        for i, line in enumerate(lines):
            if "const defaultVideoSections = [" in line:
                start_idx = i
            if "let videoSections;" in line:
                # The array ends before this
                end_idx = i
                break
        
        if start_idx == -1 or end_idx == -1:
            print("Error: Could not find data block")
            return

        # Extract data lines (inclusive of start, exclusive of end_idx where 'let' is)
        # Note: 'let videoSections' is at end_idx. The previous line should be '];'.
        # We want to keep lines from start_idx up to end_idx (exclusive of let line)
        data_block = "".join(lines[start_idx:end_idx])
        
        full_content = new_header + data_block + new_footer
        
        with open('modern_player.html', 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        print("Success: modern_player.html created")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    migrate()
