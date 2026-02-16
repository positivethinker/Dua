# Index.html - Problems Found & Fixes

## Problems Identified

### 1. **Monolithic Structure (2247 lines)**
- All HTML, CSS, JavaScript, and data in a single file
- Hard to maintain, debug, and extend
- **Fix:** Extracted styles to `styles.css`, created modular `index-new.html`

### 2. **Font Not Loaded**
- `font-family: Chivo, sans-serif` was used but Chivo was never loaded
- Page fell back to generic sans-serif
- **Fix:** `styles.css` now uses Google Fonts: Amiri (for headings) + Source Sans 3 (body)

### 3. **No Separation of Concerns**
- 1500+ lines of video data embedded in script
- Inline styles mixed with structure
- **Fix:** Styles moved to external `styles.css`

### 4. **Generic Blue Theme**
- Used default Bootstrap-like blue (#007bff)
- **Fix:** New interface uses green theme (--color-primary: #0d5c3d) suited for Dua/Darud spiritual content

### 5. **Minor Code Quality**
- Some objects use `{ isSubcategory: true, label: "..." }` with inconsistent formatting
- One object at ~line 1099 had leading space in label: `" স্বয়ং নবীজি"` 
- **Fix:** New styles improve visual hierarchy; data unchanged for compatibility

### 6. **Accessibility**
- Limited ARIA labels, semantic structure
- **Fix:** Added `:focus` styles for section-select, improved contrast

## New Interface (index-new.html)

- Uses external `styles.css` for all styling
- Amiri + Source Sans 3 fonts via Google Fonts
- Green/teal color scheme for spiritual aesthetic
- Improved hover states and visual feedback
- Custom scrollbar styling
- CSS variables for easy theme customization

## How to Use

1. Open `index-new.html` in a browser
2. Ensure `styles.css` is in the same folder
3. Original `index.html` remains unchanged for reference
