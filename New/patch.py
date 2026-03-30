import re

file_path = "c:\\Users\\hh\\Downloads\\SOFTWEAR\\DUA AND DARUD PLAYER\\New\\admin.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace loadData fallback
old_load = """      // 2. Fallback to LocalStorage
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          data = mergeMissingDefaultSections(JSON.parse(stored));
        } else {
          data = mergeMissingDefaultSections([]);
          saveData();
        }
      } catch (e) {
        data = mergeMissingDefaultSections([]);
        saveData();
      }"""

new_load = """      // 2. Fallback to Empty Array if Supabase fails
      data = mergeMissingDefaultSections([]);"""

content = content.replace(old_load, new_load)

# Replace sync
old_sync = """    function setupLocalStorageSync() {
      window.addEventListener('storage', (e) => {
        if (e.key !== STORAGE_KEY) return;
        if (!isAuthenticated) return;
        const anyModalOpen = document.querySelector('.modal.show');
        if (anyModalOpen) return;
        loadData();
      });
    }"""

new_sync = """    function setupLocalStorageSync() {
      // Intentionally left empty since data is directly managed in Supabase
    }"""

content = content.replace(old_sync, new_sync)

# Replace save
old_save = """    function saveData() {
      if (!requireAuth()) return;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      showToast('Saved to player');
    }"""

new_save = """    function saveData() {
      // Intentionally left empty since data is directly managed in Supabase
    }"""

content = content.replace(old_save, new_save)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement complete")
