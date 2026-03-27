# StudyGuard 🎯

A smart YouTube learning assistant that automates video search, skips ads, and enforces focus breaks to help students maintain productive study sessions.

## Features

- **Automated Video Search**: Search and play YouTube videos directly from the app
- **Ad Skipping**: Automatically detects and skips YouTube ads during playback
- **Focus Timer**: Enforces 1-minute breaks after 60-second focus sessions
- **Daily Watch Plan**: Curated content suggestions across Learning, Career, and Entertainment categories
- **Beautiful UI**: Ocean Gold themed interface with intuitive controls

## Requirements

- Python 3.8+
- Chrome browser (for Selenium WebDriver)
- ChromeDriver (compatible with your Chrome version)

## Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd studyguard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**
   - Download from [ChromeDriver](https://chromedriver.chromium.org/)
   - Ensure it matches your Chrome browser version
   - Add to PATH or place in project directory

4. **Optional: Add YouTube icon**
   - Place `youtube_icon.png` in the project root for the UI icon

## Usage

Run the application:
```bash
python main.py
```

### How to Use

1. **Search Videos**: Enter a topic in the search box and click "🔍 Search Video"
   - The app will open Chrome, search YouTube, and play the first result
   - Ads will be automatically skipped
   - A focus timer will start (default: 60 seconds)

2. **View Daily Plan**: Click "📅 Daily Watch Plan" to see suggested content categories

3. **Focus Break**: After the timer completes, a popup will remind you to take a break

## Project Structure

```
studyguard/
├── main.py           # Application entry point
├── gui.py            # GUI interface and user interactions
├── bot.py            # Selenium bot for YouTube automation
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Code Quality Improvements

This version includes:

- **Type Hints**: Full type annotations for better code clarity and IDE support
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Proper exception handling with specific error types
- **Constants**: Centralized configuration values
- **Documentation**: Docstrings for all functions and classes
- **Input Validation**: Validation of user inputs and parameters
- **Code Organization**: Better structure with helper functions

## Configuration

### Focus Duration

Modify the focus timer duration in `bot.py`:
```python
DEFAULT_FOCUS_DURATION = 60  # Change to desired seconds
```

### Theme Colors

Customize the UI theme in `gui.py`:
```python
THEME = {
    "bg": "#0B3D91",        # Background color
    "panel": "#FCEBB6",     # Panel color
    "accent": "#FFB400",    # Button/accent color
    "text": "#FFFFFF"       # Text color
}
```

## Troubleshooting

### ChromeDriver Issues
- Ensure ChromeDriver version matches your Chrome browser version
- Add ChromeDriver to system PATH or place in project directory
- On Windows, ensure `chromedriver.exe` is executable

### YouTube Element Not Found
- YouTube's HTML structure may change; update selectors in `bot.py` if needed
- Check browser console for element IDs/classes

### Icon Not Loading
- Ensure `youtube_icon.png` is in the project root
- The app will work without the icon (graceful fallback)

## Logging

Logs are printed to console with timestamps and severity levels:
```
2024-03-27 10:30:45,123 - bot - INFO - Chrome WebDriver started successfully
2024-03-27 10:30:50,456 - bot - INFO - Successfully found and clicked video: Python Tutorial
```

## Dependencies

- `selenium>=4.0.0` - Web automation
- `Pillow>=9.0.0` - Image processing for UI icons

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to submit issues and enhancement requests!

## Future Enhancements

- [ ] Configurable focus duration via UI
- [ ] Video history tracking
- [ ] Custom daily plan creation
- [ ] Statistics dashboard
- [ ] Multi-language support
- [ ] Keyboard shortcuts
