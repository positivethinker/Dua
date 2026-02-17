# Daily Checklist - 3-Hour Auto-Delete Feature

## Overview
The Daily Checklist now has a **3-hour deadline** that forces you to complete your tasks quickly. All checklist data will be **permanently deleted** after 3 hours, creating urgency and encouraging immediate action.

## How It Works

### Auto-Delete Timer
- **Duration**: 3 hours (180 minutes)
- **Action**: Complete deletion of all checklist items
- **Countdown**: Visible timer shows remaining time (e.g., "Resets in: 2h 45m 30s")

### What Happens on Reset
When the 3-hour timer reaches zero:
1. ✅ All checklist items are **permanently deleted**
2. ✅ Both completed and incomplete tasks are removed
3. ✅ The timer resets to 3 hours
4. ✅ You start with a clean slate

### Previous Behavior (Changed)
- **Before**: 12-hour reset that only unchecked items
- **Now**: 3-hour reset that deletes all data

## Why This Change?

### Creates Urgency ⏰
- Forces you to complete tasks within 3 hours
- Prevents procrastination
- Encourages immediate action

### Fresh Start 🔄
- Clean slate every 3 hours
- No clutter from old tasks
- Focus on what matters now

### Accountability 💪
- If you don't complete tasks in time, they're gone
- Motivates consistent daily practice
- Builds discipline

## Usage Tips

### Best Practices
1. **Add only essential tasks** - Focus on what you can realistically complete in 3 hours
2. **Check the timer regularly** - Don't let tasks expire
3. **Complete tasks quickly** - Don't wait until the last minute
4. **Use for daily spiritual goals** - Morning prayers, Quran reading, dhikr sessions

### Example Workflow
```
9:00 AM - Add tasks for morning routine
        - ✅ Fajr prayer
        - ✅ Read Quran (15 minutes)
        - ✅ Morning dhikr

12:00 PM - All tasks auto-deleted (3 hours passed)
         - Add new tasks for afternoon

3:00 PM - All tasks auto-deleted again
        - Add evening tasks
```

## Technical Details

### Timer Calculation
- Checks every 30 seconds for auto-reset
- Uses `Date.now()` for accurate time tracking
- Stores last reset time in localStorage

### Data Storage
- **Key**: `duaChecklist` - Stores checklist items
- **Key**: `duaChecklistLastReset` - Stores last reset timestamp
- **Behavior**: Complete deletion on reset (not just unchecking)

### Code Location
- File: `index.html`
- Function: `checkAutoReset()` (line ~2662)
- Reset interval: `3 * 60 * 60 * 1000` (3 hours in milliseconds)

## Comparison

| Feature | Old (12 hours) | New (3 hours) |
|---------|---------------|---------------|
| **Duration** | 12 hours | 3 hours |
| **Reset Action** | Uncheck items | Delete all data |
| **Purpose** | Daily reset | Urgent completion |
| **Urgency** | Low | High ⚡ |
| **Use Case** | Daily planning | Immediate action |

---

**Remember**: You have only 3 hours to complete your tasks. Use this feature to build discipline and maintain focus on your spiritual goals! 🎯💪
