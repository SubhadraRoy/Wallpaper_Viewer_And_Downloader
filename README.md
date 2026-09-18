# LuminaWall — Super Advanced Wallpaper Studio & Downloader

✨ **Live Demo**: [https://subhadraroy.github.io/website/](https://subhadraroy.github.io/website/)

LuminaWall is a next-generation static web application for browsing, previewing, and downloading high-resolution wallpapers tailored for **Mobile Phones**, **Desktop Displays**, and **Universal Screens**.

---

## 🚀 Key Features

- **📱 Smart Device Categorization**: Automatically indexes wallpaper dimensions into **Phone** (179 portrait), **Desktop** (42 landscape), and **Universal** categories.
- **👁️ Interactive Live Device Preview Studio**:
  - **Phone Mockup**: Realistic iPhone frame simulation with live lockscreen clock, battery/status bar, and wallpaper scaling.
  - **Desktop Mockup**: Monitor frame simulation with macOS/Windows dock, app windows, and desktop scaling.
- **⚡ Single & Batch Downloader**:
  - Direct 1-click high-resolution download with clean filename handling.
  - Floating multi-select tray with **Batch ZIP Archiver** powered by JSZip.
- **🔍 Advanced Search & Tag Filtering**: Instant search across titles, dimensions, tags (`#krishna`, `#radheradhe`, `#pink`, `#pinterest`, `#4k`), and categories.
- **🎨 Modern Cyber-Glassmorphism UI**: Built with Tailwind CSS, Lucide Icons, GSAP animations, and an interactive WebGL/Canvas ambient particle backdrop.
- **🔍 Full-Screen Lightbox**: Keyboard-controlled slide navigation (`←`, `→`, `Esc`) with detailed EXIF data swatches.
- **❤️ Local Favorites System**: Bookmark favorite wallpapers persisted in browser `localStorage`.

---

## 📂 Repository Structure

```
Wallpaper_Viewer_And_Downloader/
├── index.html           # Main LuminaWall Web Application
├── wallpapers.json      # Auto-indexed wallpaper metadata database
├── generate_index.py    # Python metadata indexing script
├── Pictures/            # Directory containing 221 high-definition wallpapers
└── README.md            # Documentation
```

---

## ⚙️ Updating the Wallpaper Index

If you add new images to the `Pictures/` folder, regenerate `wallpapers.json` by running:

```bash
python generate_index.py
```
