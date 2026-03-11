// Runtime configuration for the static HTML app.
// Supabase credentials are intentionally not hard-coded in HTML.
// Configure from Admin (Supabase Settings) or manually via localStorage keys:
// - SUPABASE_URL
// - SUPABASE_ANON_KEY
(function () {
  try {
    const url = (localStorage.getItem('SUPABASE_URL') || '').trim();
    const anonKey = (localStorage.getItem('SUPABASE_ANON_KEY') || '').trim();
    window.DUA_SUPABASE = { url, anonKey };
  } catch (e) {
    window.DUA_SUPABASE = { url: '', anonKey: '' };
  }
})();
