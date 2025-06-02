let player;
let currentLoopCount = 0;
let currentMaxLoops = 0;
let currentStartTime = 0;
let currentEndTime = 0;
let currentVideoId = '';
let loopInterval = null;

function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '360',
    width: '640',
    videoId: '',
    playerVars: {
      modestbranding: 1,
      rel: 0,
      autoplay: 1
    },
    events: {
      'onReady': () => {},
      'onStateChange': onPlayerStateChange
    }
  });
}

function loadVideoConfig() {
  const select = document.getElementById('videoSelect');
  const config = select.value;
  if (!config) {
    clearTooltip();
    return;
  }

  const [videoId, start, end] = config.split(',');
  const selectedLoopCount = parseInt(document.getElementById('loopCountSelect').value);

  currentVideoId = videoId;
  currentStartTime = parseFloat(start);
  currentEndTime = parseFloat(end);
  currentMaxLoops = selectedLoopCount;
  currentLoopCount = 0;

  updateDisplay();

  player.loadVideoById({
    videoId: currentVideoId,
    startSeconds: currentStartTime,
    endSeconds: currentEndTime
  });

  showTooltip();
}

function updateLoopCount() {
  const selectedLoopCount = parseInt(document.getElementById('loopCountSelect').value);
  currentMaxLoops = selectedLoopCount;
  currentLoopCount = 0;

  updateDisplay();

  if (currentVideoId) {
    player.loadVideoById({
      videoId: currentVideoId,
      startSeconds: currentStartTime,
      endSeconds: currentEndTime
    });
  }
}

function updateDisplay() {
  document.getElementById("currentLoop").textContent = currentLoopCount;
  document.getElementById("remainingLoop").textContent = currentMaxLoops - currentLoopCount;
}

function onPlayerStateChange(event) {
  if (event.data === YT.PlayerState.PLAYING) {
    startLoopCheck();
  }
}

function startLoopCheck() {
  if (loopInterval) clearInterval(loopInterval);

  loopInterval = setInterval(() => {
    const currentTime = player.getCurrentTime();

    if (currentTime >= currentEndTime) {
      currentLoopCount++;
      updateDisplay();

      if (currentLoopCount < currentMaxLoops) {
        player.seekTo(currentStartTime);
      } else {
        player.pauseVideo();
      }

      clearInterval(loopInterval);
      loopInterval = null;
    }
  }, 200);
}

function showTooltip() {
  const select = document.getElementById('videoSelect');
  const tooltipDiv = document.getElementById('tooltipText');
  const selectedOption = select.options[select.selectedIndex];
  const tooltip = selectedOption.getAttribute('data-tooltip') || '';
  tooltipDiv.textContent = tooltip;
}

function clearTooltip() {
  document.getElementById('tooltipText').textContent = '';
}

document.addEventListener('DOMContentLoaded', () => {
  showTooltip();
});
