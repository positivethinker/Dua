import re

file_path = "c:\\Users\\hh\\Downloads\\SOFTWEAR\\DUA AND DARUD PLAYER\\New\\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add global user settings state and sync function
global_state = """      // --- USER SETTINGS SYNC ---
      let userSettings = {
          theme: null, bg: null, favorites: [], history: [], streak: 0, lastVisit: null, notes: {}, checklist: [], checklistLastReset: null, sectionLocks: {}
      };

      async function fetchUserSettings() {
          if (!_supabase || SUPABASE_URL === 'YOUR_SUPABASE_URL') return;
          try {
              const { data, error } = await _supabase.from('user_settings').select('*').eq('id', 1).single();
              if (data && !error) {
                  userSettings.theme = data.theme;
                  userSettings.bg = data.bg;
                  userSettings.favorites = data.favorites || [];
                  userSettings.history = data.history || [];
                  userSettings.streak = data.streak || 0;
                  userSettings.lastVisit = data.last_visit;
                  userSettings.notes = data.notes || {};
                  userSettings.checklist = data.checklist || [];
                  userSettings.checklistLastReset = data.checklist_last_reset;
                  userSettings.sectionLocks = data.section_locks || {};
                  
                  // Apply loaded settings
                  favorites = userSettings.favorites;
                  playHistory = userSettings.history;
                  checklistItems = userSettings.checklist;
                  checklistLastReset = parseInt(userSettings.checklistLastReset || Date.now());
                  
                  if (userSettings.theme) setTheme(userSettings.theme, false);
                  if (userSettings.bg) setBg(userSettings.bg, false);
                  updateHabitStreak(false); // don't sync back immediately
                  renderChecklist();
              }
          } catch(e) { console.error("Failed to fetch user settings", e); }
      }

      async function syncUserSetting(key, value) {
          if (!_supabase || SUPABASE_URL === 'YOUR_SUPABASE_URL') return;
          try {
              const payload = {};
              payload[key] = value;
              await _supabase.from('user_settings').update(payload).eq('id', 1);
          } catch(e) { console.error("Failed to sync setting", key, e); }
      }
"""

# Insert just before // Drag and Drop handlers or a suitable place early on, let's inject after setupRealtime
content = content.replace("      function setupLocalStorageSync() {", global_state + "\n      function setupLocalStorageSync() {")


# 2. Add fetchUserSettings to initializeData
content = content.replace("renderPlaylist();\n      }", "fetchUserSettings();\n          renderPlaylist();\n      }")

# 3. Replace Section Locks
content = content.replace("""      function getSectionLocks() {
          try {
              return JSON.parse(localStorage.getItem('duaSectionLocks') || '{}');
          } catch (e) { return {}; }
      }

      function saveSectionLocks(locks) {
          localStorage.setItem('duaSectionLocks', JSON.stringify(locks));
      }""", """      function getSectionLocks() {
          return userSettings.sectionLocks || {};
      }

      function saveSectionLocks(locks) {
          userSettings.sectionLocks = locks;
          syncUserSetting('section_locks', locks);
      }""")

# 4. Replace History
content = content.replace("""      let playHistory = JSON.parse(localStorage.getItem('duaHistory') || '[]');

      function addToHistory(videoId, label) {
          // Remove if exists to push to top
          playHistory = playHistory.filter(h => h.id !== videoId);
          playHistory.unshift({ id: videoId, label: label, date: Date.now() });
          if(playHistory.length > 20) playHistory.pop(); // Keep last 20
          localStorage.setItem('duaHistory', JSON.stringify(playHistory));""", """      let playHistory = [];

      function addToHistory(videoId, label) {
          // Remove if exists to push to top
          playHistory = playHistory.filter(h => h.id !== videoId);
          playHistory.unshift({ id: videoId, label: label, date: Date.now() });
          if(playHistory.length > 20) playHistory.pop(); // Keep last 20
          syncUserSetting('history', playHistory);""")

# 5. Replace Favorites
content = content.replace("""      let favorites = JSON.parse(localStorage.getItem('duaFavorites') || '[]');
      let isFavFilterActive = false;

      function toggleFav(id, btn) {
          if (favorites.includes(id)) {
              favorites = favorites.filter(fid => fid !== id);
              btn.classList.remove('active');
          } else {
              favorites.push(id);
              btn.classList.add('active');
          }
          localStorage.setItem('duaFavorites', JSON.stringify(favorites));""", """      let favorites = [];
      let isFavFilterActive = false;

      function toggleFav(id, btn) {
          if (favorites.includes(id)) {
              favorites = favorites.filter(fid => fid !== id);
              btn.classList.remove('active');
          } else {
              favorites.push(id);
              btn.classList.add('active');
          }
          syncUserSetting('favorites', favorites);""")

# 6. Replace Theme
content = content.replace("""      function setTheme(color) {
          document.documentElement.style.setProperty('--accent', color);
          document.documentElement.style.setProperty('--accent-glow', color + '33'); // 0.2 alpha approx
          localStorage.setItem('duaTheme', color);
      }
      
      // Load Theme
      const savedTheme = localStorage.getItem('duaTheme');
      if(savedTheme) setTheme(savedTheme);""", """      function setTheme(color, sync = true) {
          document.documentElement.style.setProperty('--accent', color);
          document.documentElement.style.setProperty('--accent-glow', color + '33'); // 0.2 alpha approx
          if (sync) syncUserSetting('theme', color);
      }""")

# 7. Replace Background
content = content.replace("""      function setBg(type) {
          if (type === 'none') {
             document.body.style.background = 'var(--bg-main)';
          } else if (type === 'ocean') {
             document.body.style.background = 'linear-gradient(to bottom, #1e3c72, #2a5298)';
          } else if (type === 'forest') {
             document.body.style.background = 'linear-gradient(to bottom, #11998e, #38ef7d)';
          } else if (type === 'sunset') {
             document.body.style.background = 'linear-gradient(to bottom, #200122, #6f0000)';
          }
          localStorage.setItem('duaBg', type);
      }
      const savedBg = localStorage.getItem('duaBg');
      if(savedBg) setBg(savedBg);""", """      function setBg(type, sync = true) {
          if (type === 'none') {
             document.body.style.background = 'var(--bg-main)';
          } else if (type === 'ocean') {
             document.body.style.background = 'linear-gradient(to bottom, #1e3c72, #2a5298)';
          } else if (type === 'forest') {
             document.body.style.background = 'linear-gradient(to bottom, #11998e, #38ef7d)';
          } else if (type === 'sunset') {
             document.body.style.background = 'linear-gradient(to bottom, #200122, #6f0000)';
          }
          if (sync) syncUserSetting('bg', type);
      }""")

# 8. Replace Notes
content = content.replace("""      function saveNote() {
          const vid = videoSections[currentState.sectionIndex].videos[currentState.videoIndex];
          if(!vid) return;
          const notes = JSON.parse(localStorage.getItem('duaNotes') || '{}');
          const val = document.getElementById('personalNote').value;
          if(val.trim() === "") delete notes[vid.id];
          else notes[vid.id] = val;
          localStorage.setItem('duaNotes', JSON.stringify(notes));
      }
      
      function loadNote(vidId) {
          const notes = JSON.parse(localStorage.getItem('duaNotes') || '{}');""", """      function saveNote() {
          const vid = videoSections[currentState.sectionIndex].videos[currentState.videoIndex];
          if(!vid) return;
          const notes = userSettings.notes || {};
          const val = document.getElementById('personalNote').value;
          if(val.trim() === "") delete notes[vid.id];
          else notes[vid.id] = val;
          userSettings.notes = notes;
          syncUserSetting('notes', notes);
      }
      
      function loadNote(vidId) {
          const notes = userSettings.notes || {};""")

# 9. Replace Habit Tracker
content = content.replace("""      function updateHabitStreak() {
          const today = new Date().toDateString();
          const lastVisit = localStorage.getItem('duaLastVisit');
          let streak = parseInt(localStorage.getItem('duaStreak') || '0');
          
          if (lastVisit !== today) {
              const yesterday = new Date();
              yesterday.setDate(yesterday.getDate() - 1);
              if (lastVisit === yesterday.toDateString()) {
                  streak++;
              } else {
                  streak = 1; // Reset or Start
              }
              localStorage.setItem('duaLastVisit', today);
              localStorage.setItem('duaStreak', streak);
          }""", """      function updateHabitStreak(sync = true) {
          const today = new Date().toDateString();
          const lastVisit = userSettings.lastVisit;
          let streak = parseInt(userSettings.streak || '0');
          
          if (lastVisit !== today) {
              const yesterday = new Date();
              yesterday.setDate(yesterday.getDate() - 1);
              if (lastVisit === yesterday.toDateString()) {
                  streak++;
              } else {
                  streak = 1; // Reset or Start
              }
              if (sync) {
                  syncUserSetting('last_visit', today);
                  syncUserSetting('streak', streak);
              }
          }""")

# 10. Replace Checklist
content = content.replace("""      // CHECKLIST FEATURE
      let checklistItems = JSON.parse(localStorage.getItem('duaChecklist') || '[]');
      let checklistLastReset = parseInt(localStorage.getItem('duaChecklistLastReset') || Date.now());""", """      // CHECKLIST FEATURE
      let checklistItems = [];
      let checklistLastReset = Date.now();""")

content = content.replace("""          checklistItems.push({ text: text, completed: false });
          localStorage.setItem('duaChecklist', JSON.stringify(checklistItems));""", """          checklistItems.push({ text: text, completed: false });
          syncUserSetting('checklist', checklistItems);""")

content = content.replace("""      function toggleChecklistItem(index) {
          checklistItems[index].completed = !checklistItems[index].completed;
          localStorage.setItem('duaChecklist', JSON.stringify(checklistItems));""", """      function toggleChecklistItem(index) {
          checklistItems[index].completed = !checklistItems[index].completed;
          syncUserSetting('checklist', checklistItems);""")

content = content.replace("""      function deleteChecklistItem(index) {
          if (confirm('Delete this task?')) {
              checklistItems.splice(index, 1);
              localStorage.setItem('duaChecklist', JSON.stringify(checklistItems));""", """      function deleteChecklistItem(index) {
          if (confirm('Delete this task?')) {
              checklistItems.splice(index, 1);
              syncUserSetting('checklist', checklistItems);""")

content = content.replace("""              checklistItems = [];
              checklistLastReset = now;
              localStorage.setItem('duaChecklist', JSON.stringify(checklistItems));
              localStorage.setItem('duaChecklistLastReset', checklistLastReset.toString());""", """              checklistItems = [];
              checklistLastReset = now;
              syncUserSetting('checklist', checklistItems);
              syncUserSetting('checklist_last_reset', checklistLastReset.toString());""")

# 11. Disable LocalStorage Backup checks
content = content.replace("theme: localStorage.getItem('duaTheme'),", "theme: userSettings.theme,")
content = content.replace("streak: localStorage.getItem('duaStreak'),", "streak: userSettings.streak,")
content = content.replace("lastVisit: localStorage.getItem('duaLastVisit'),", "lastVisit: userSettings.lastVisit,")
content = content.replace("notes: JSON.parse(localStorage.getItem('duaNotes') || '{}')", "notes: userSettings.notes")

# Restore LocalStorage ignores
# Note: we are patching restoreData to be a no-op or just log since everything is in supabase now. Or better, write to supabase instead.
restore_old = """                  if(data.favorites) { favorites = data.favorites; localStorage.setItem('duaFavorites', JSON.stringify(favorites)); }
                  if(data.theme) { setTheme(data.theme); }
                  if(data.videoSections) { localStorage.setItem('duaDarudVideoSections', JSON.stringify(data.videoSections)); } // For Admin changes
                  if(data.streak) { localStorage.setItem('duaStreak', data.streak); }
                  if(data.lastVisit) { localStorage.setItem('duaLastVisit', data.lastVisit); }
                  if(data.notes) { localStorage.setItem('duaNotes', JSON.stringify(data.notes)); }"""

restore_new = """                  if(data.favorites) syncUserSetting('favorites', data.favorites);
                  if(data.theme) syncUserSetting('theme', data.theme);
                  if(data.streak) syncUserSetting('streak', data.streak);
                  if(data.lastVisit) syncUserSetting('last_visit', data.lastVisit);
                  if(data.notes) syncUserSetting('notes', data.notes);"""
                  
content = content.replace(restore_old, restore_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patching complete")
