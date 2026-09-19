# LuminaWall — Wallpaper Studio & Downloader

✨ **Live Demo**: [https://subhadraroy.github.io/website/](https://subhadraroy.github.io/website/)

LuminaWall is a high-performance, responsive web application for browsing, pairing, previewing, and downloading high-resolution wallpapers for **Mobile Phones**, **Desktop Displays**, and **Matching Phone + PC Combos**.

---

## 🚀 Key Features

- **📱 Smart Screen Categorization**: Automatically indexes wallpaper dimensions into **Phone**, **Desktop**, and **Universal** categories.
- **📱💻 Matching Phone & PC Combos Tab**: Pair and view matching Mobile and Desktop wallpapers side-by-side with instant 1-click dual downloads.
- **🔗 Manual Combo Matcher Studio**: Click **"🔗 Link Pair"** on any wallpaper card to select its matching counterpart and save your custom pairs.
- **👁️ Interactive Live Device Preview Studio**:
  - **Phone Mockup**: Realistic iPhone frame simulation with live lockscreen clock, status bar, and customizable filters.
  - **Desktop Mockup**: Ultra-wide monitor frame simulation with scaling controls.
- **🎛️ Real Image Filter Studio**: Live sliders for **Brightness**, **Contrast**, **Saturation**, **Hue Rotation**, and **Blur** with direct **Download Custom Edited HD** export.
- **⚡ Single & Batch Downloader**: Direct 1-click downloads plus a floating multi-select **Batch ZIP Archiver** powered by JSZip.
- **❤️ Local Favorites & Combos Persistence**: Bookmarks and manual combo pairings saved automatically in browser `localStorage`.

---

## 📂 Repository Structure

```
Wallpaper_Viewer_And_Downloader/
├── index.html           # Main LuminaWall Web Application
├── wallpapers.js        # Embedded JavaScript wallpapers database (Zero-CORS)
├── wallpapers.json      # JSON metadata database
├── sanitize_and_tag.py  # Python metadata indexing & auto-tagging script
├── Pictures/            # Directory containing high-definition wallpapers
└── README.md            # Documentation
```

---

## ⚙️ Updating the Wallpaper Index

Whenever you add new wallpapers to the `Pictures/` folder, run:

```bash
python sanitize_and_tag.py
```
This automatically cleans filenames, extracts color palettes, assigns tags, and updates `wallpapers.json` and `wallpapers.js`.
