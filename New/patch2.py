import re

file_path = "c:\\Users\\hh\\Downloads\\SOFTWEAR\\DUA AND DARUD PLAYER\\New\\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_load = """          // 2. Try LocalStorage if Supabase failed or not configured
          if (!videoSections) {
              try {
                  const stored = localStorage.getItem("duaDarudVideoSections");
                  if (stored) {
                      const parsed = JSON.parse(stored);
                      if (Array.isArray(parsed) && parsed.length > 0) {
                          videoSections = mergeMissingDefaultSections(parsed);
                      }
                  }
              } catch (e) {}
          }"""

new_load = """          // 2. Fallback removed - we purely rely on Supabase or defaults now
"""

content = content.replace(old_load, new_load)


old_sync = """      function setupLocalStorageSync() {
          window.addEventListener('storage', (e) => {
              if (e.key !== 'duaDarudVideoSections') return;
              try {
                  const parsed = JSON.parse(e.newValue || '[]');
                  if (!Array.isArray(parsed)) return;
                  videoSections = mergeMissingDefaultSections(parsed);
                  renderPlaylist();
              } catch (err) {
                  console.error('LocalStorage sync failed', err);
              }
          });
      }"""

new_sync = """      function setupLocalStorageSync() {
          // Intentionally left empty. Data is now solely managed via Supabase realtime.
      }"""
content = content.replace(old_sync, new_sync)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("index.html Replacement complete")
