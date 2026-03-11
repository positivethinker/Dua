# Dua Player - New Features

## Custom Loop Reset

### Overview
The custom loop input field now automatically resets when you switch to a different video in the playlist.

### How It Works
- When you select a new video from the playlist, any custom loop count you previously entered is automatically cleared
- This prevents the custom loop value from carrying over to videos where you might want to use the default loop count
- Each video starts fresh, allowing you to set a custom loop count specifically for that video if needed

### Usage
1. Select any video from the playlist
2. Enter a custom loop count in the "Set" input field (e.g., "5")
3. The video will loop the custom number of times
4. When you select a different video, the custom loop field automatically clears
5. The new video will use its default loop count unless you enter a new custom value

---


---

## Technical Details

### Custom Loop Reset
- **Implementation**: Added in the `startVideo()` function
- **Location**: `index.html` line ~1892
- **Code**: `document.getElementById('customLoopInput').value = '';`

---

---

## Browser Compatibility
Both features are compatible with:
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)
