# Section Lock Feature - 3-Hour Playback Lock

## Overview
This feature automatically locks a playlist section for **3 hours** after it has been fully played. This encourages spacing out your sessions and prevents repetitive playback of the same section immediately.

## How It Works

### Automatic Locking 🔒
- **Trigger**: When the last video of a section finishes playing.
- **Duration**: 3 hours.
- **Visual**: The section becomes greyed out and a lock icon (🔒) appears.

### Enforcement 🛡️
- **Clicking**: If you try to open or play a locked section, a warning message appears:
  > "⚠️ Section locked for 2h 45m"
- **Drag & Drop**: Locked sections cannot be dragged or reordered.
- **Auto-Play**: If "Play All" is active, locked sections are automatically skipped.

## Usage Guide

1.  **Play a Section**: Start playing any section as usual.
2.  **Finish**: Once the last video ends, the section will lock.
3.  **Wait**: The lock remains active for 3 hours.
4.  **Unlock**: After time expires, the section automatically unlocks and becomes playable again.

## Technical Details

-   **Storage**: Lock timestamps are saved in your browser's local storage (`duaSectionLocks`).
-   **Persistence**: Locks remain active even if you close or refresh the browser.
-   **Reset**: The feature checks for expired locks every minute and updates the UI automatically.

## Comparison with Previous Behavior
-   **Before**: You could play any section repeatedly at any time.
-   **Now**: Sections require a 3-hour cool-down period after completion.

---
*Note: This feature is designed to help structure your learning or listening schedule.*
