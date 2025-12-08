# 🛍️ App Store Review Scraper GUI

A clean, modern desktop application for scraping app information and reviews from **Google Play Store** and **Apple App Store**. Built with Python and CustomTkinter for macOS (and other platforms).

![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📸 Screenshot

### Google Play Store - GitHub App

![Google Play Store - App Info](https://github.com/user-attachments/assets/demo-github-info.png)
_Fetching app information from Google Play Store for the GitHub Android app_

![Google Play Store - Reviews](https://github.com/user-attachments/assets/demo-github-reviews.png)
_Successfully fetched 100 reviews with ratings, user info, and timestamps_

### Apple App Store - GitHub App

![App Store - App Info](https://github.com/user-attachments/assets/demo-appstore-info.png)
_Fetching app metadata using iTunes RSS Feed API (App ID: 1477376905)_

![App Store - Reviews](https://github.com/user-attachments/assets/demo-appstore-reviews.png)
_Successfully fetched 49 reviews from iTunes RSS Feed with ratings and review text_

---

## ✨ Features

### Current Features

- ✅ **Dual Platform Support**

  - Google Play Store integration
  - Apple App Store integration
  - Easy platform switching with segmented button

- ✅ **Google Play Store Integration**
  - Fetch detailed app information (title, developer, ratings, installs, etc.)
  - Scrape user reviews with customizable parameters
  - Support for multiple languages and countries
  - ✅ **Fully functional and reliable**
- ⚠️ **Apple App Store Integration** (Currently Limited)

  - **Note**: Apple has changed their API structure, causing the app-store-scraper library to fail
  - Review fetching currently not working due to library compatibility issues
  - Google Play Store recommended for production use
  - Alternative: Use official App Store Connect API for App Store reviews

- ✅ **Clean GUI Interface**

  - Modern dark theme using CustomTkinter
  - Platform switcher (Google Play / App Store)
  - Intuitive input fields for all parameters
  - Live JSON output display
  - Easy-to-use export functionality

- ✅ **Multi-Country Reviews**

  - Fetch reviews from 8 countries simultaneously
  - Automatic duplicate removal
  - Country tracking for each review

- ✅ **Advanced Filtering**

  - Text-only filter to exclude rating-only reviews
  - Get only reviews with written comments/descriptions
  - Improve data quality for sentiment analysis

- ✅ **Data Export**
  - Export results to JSON format
  - Timestamped filenames for easy organization
  - Structured data ready for analysis

### Coming Soon (Future Phases)

- 📊 CSV export for reviews
- 📈 Basic analytics and statistics
- 🔍 Advanced filtering options
- ⚡ Async/background scraping for better performance
- 🔄 Batch processing multiple apps

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **macOS** (tested on macOS, but should work on Windows/Linux)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/app-store-review-scraper-gui.git
cd app-store-review-scraper-gui
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎮 Usage

### Running the Application

```bash
python main.py
```

### Using the GUI

1. **Select Platform**: Choose between "Google Play" or "App Store" using the segmented button

2. **Enter App Identifier**:

   - **Google Play**: Package name (e.g., `com.instagram.android`)
   - **App Store**: App name (e.g., `instagram`, `minecraft`)

3. **Set Parameters**:

   - **Language**: 2-letter language code (Google Play only, default: `en`)
   - **Country**: 2-letter country code (default: `us`)
   - **Review Count**: Number of reviews to fetch (default: `100`)
   - **Sort By**: Choose how to sort reviews (`newest`, `rating`, or `helpfulness`)
   - **Filters**:
     - ☑️ **Only reviews with text/description**: Skip rating-only reviews and fetch only reviews that include written comments

4. **Fetch Data**:

   - Click **"📱 Crawl App Info"** to get app details
   - Click **"⭐ Crawl Reviews"** to fetch user reviews
   - Click **"🌍 Multi-Country Reviews"** to fetch from multiple countries at once

5. **Export Results**:

   - Click **"💾 Export JSON"** to save the current results
   - Files are saved in the `data/` directory by default

6. **Clear Output**:
   - Click **"🗑️ Clear"** to reset the display

### Example Identifiers

**Google Play Store (use Package ID):**

- GitHub: `com.github.android`
- Instagram: `com.instagram.android`
- YouTube: `com.google.android.youtube`
- WhatsApp: `com.whatsapp`
- Spotify: `com.spotify.music`
- TikTok: `com.zhiliaoapp.musically`

**Apple App Store (use Numeric App ID - RECOMMENDED):**

- GitHub: `1477376905`
- Facebook: `284882215`
- Instagram: `389801252`
- WhatsApp: `310633997`
- TikTok: `835599320`
- YouTube: `544007664`

**Note**: For App Store, always use the **numeric App ID** (found in the URL like `id1477376905`). This uses the reliable iTunes RSS Feed API.

- WhatsApp: `whatsapp messenger`
- Spotify: `spotify`
- TikTok: `tiktok`

---

## 📁 Project Structure

```
app-store-review-scraper-gui/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── engine.py             # Google Play Store scraping logic
│   ├── ui_main.py            # CustomTkinter GUI implementation
│   └── models.py             # Data models (optional)
├── data/                     # Output directory for exported files
│   └── .gitignore
├── tests/                    # Unit tests
│   ├── __init__.py
│   └── test_engine.py
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── LICENSE                   # MIT License
```

---

## 🛠️ Development

### Running Tests

```bash
python -m pytest tests/
```

Or run specific tests:

```bash
python -m unittest tests.test_engine
```

### Code Style

This project follows PEP8 guidelines. Format code using:

```bash
black app/ tests/
flake8 app/ tests/
```

### Adding Features

The project is structured for easy extension:

- **New scrapers**: Add new modules in `app/` (e.g., `app_store_engine.py` for iOS)
- **UI improvements**: Modify `app/ui_main.py`
- **Data models**: Define structures in `app/models.py`

---

## 📊 Data Format

### App Information Response

```json
{
  "app_id": "com.instagram.android",
  "title": "Instagram",
  "developer": "Instagram",
  "rating": 4.5,
  "reviews_count": 123456789,
  "installs": "5,000,000,000+",
  "description": "...",
  ...
}
```

### Reviews Response

```json
[
  {
    "review_id": "...",
    "user_name": "John Doe",
    "rating": 5,
    "date": "2024-01-15",
    "text": "Great app!",
    "thumbs_up": 42,
    "reply_text": "Thanks!",
    ...
  },
  ...
]
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'gplay_scraper'`

- **Solution**: Make sure you've installed dependencies: `pip install -r requirements.txt`

**Issue**: GUI doesn't appear on macOS

- **Solution**: Ensure you're using Python 3.8+ and have Tkinter support installed

**Issue**: "No data returned" error

- **Solution**: Verify the App ID is correct and the app exists in the specified country's Play Store

**Issue**: Slow performance when fetching many reviews

- **Solution**: Reduce the review count or wait for async implementation in future versions

---

## 🗺️ Roadmap

- [x] Phase 1: Google Play Store support
- [ ] Phase 2: Apple App Store integration
- [ ] Phase 3: CSV export for reviews
- [ ] Phase 4: Data analytics and visualization
- [ ] Phase 5: Async scraping for better performance
- [ ] Phase 6: Batch processing multiple apps
- [ ] Phase 7: Review sentiment analysis

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [gplay-scraper](https://github.com/JoMingyu/google-play-scraper) - Google Play Store scraping library
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework
- The open-source community

---

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for app developers and data analysts**
