# Codem Music Player & Converter

🎵 **A Powerful Desktop Application for Downloading, Playing, and Converting Media Files with API Control**

---

## 🚀 Features

### 🎵 **Music Player**
- Play MP3, WAV, M4A audio files
- Create and manage playlists
- Volume control, loop modes (off/track/playlist)
- Track seeking and playback controls
- Album art display

### 📥 **YouTube Downloader**
- Download videos as MP4 (720p, 1080p, 4K)
- Extract audio as MP3 (128k, 192k, 320k), M4A, WAV, WebM
- Custom filename patterns
- Progress tracking and status updates

### 🔄 **File Converter**
- Convert between image formats (PNG ↔ JPG, WebP, ICO)
- Convert PDF to multiple JPG images
- Combine JPG images into PDF
- Batch conversion support

### 🌐 **API Control**
- Control the player remotely from other Python scripts
- Programmatic control of all features
- Real-time status monitoring

---

## 📦 Installation

### Option 1: Quick Start (Windows)
1. Download the latest `CodemMusicPlayerV4.exe` from the releases page
2. Run the executable - no installation required!
3. For API control, download `Music_Player_Client.py` to your project folder

### Option 2: Manual Installation
1. Ensure you have [FFmpeg](https://ffmpeg.org/download.html) installed (for YouTube downloads)
2. Run the executable
3. In Settings tab, configure FFmpeg path if not auto-detected

---

## 🎮 Basic Usage

### Starting the Application
1. Double-click `CodemMusicPlayerV4.exe`
2. The application will start with a futuristic dark interface
3. The API server automatically starts (default port: 65432)

### Downloading YouTube Content
1. **Enter URL**: Paste a YouTube link in the URL field
2. **Select Format**: Choose Audio (MP3, M4A, etc.) or Video (MP4) tab
3. **Configure Options**: 
   - Set quality preferences
   - Choose download folder
   - Customize filename
4. **Click**: `⚡ DOWNLOAD NOW ⚡`

### Playing Music
1. **Load Files**: Click `📁` in Music Player tab or use API
2. **Controls**:
   - ▶ Play / ⏸ Pause / ⏹ Stop
   - ⏮ Previous / ⏭ Next track
   - 🔁 Toggle loop modes
   - 🔊 Volume slider
   - ⏺️ Progress seek bar

### Converting Files
1. **Select Mode**: Choose conversion type from dropdown
2. **Select Files**: Click `📁 Select File(s)`
3. **Convert**: Click `⚡ Convert ⚡`

---

## 🖥️ API Usage (Remote Control)

### Setup
1. Ensure the main application (`CodemMusicPlayerV4.exe`) is running
2. Copy `Music_Player_Client.py` to your project folder
3. Import and use in your Python scripts:

```python
from Music_Player_Client import MusicPlayerClient

# Create connection to running player
client = MusicPlayerClient()  # Default: localhost:65432

# Now control the player remotely!
```

### API Examples

#### Basic Playback Control
```python
client.play()      # Start/resume playback
client.pause()     # Pause playback
client.stop()      # Stop playback
client.next_track() # Next song
client.prev_track() # Previous song
client.set_volume(75)  # Set volume to 75%
```

#### YouTube Downloads
```python
# Download a song/video
client.download("https://www.youtube.com/watch?v=EXAMPLE")

# Download and immediately play
client.play_url("https://www.youtube.com/watch?v=EXAMPLE")
```

#### Playlist Management
```python
# Load specific audio files
client.load_playlist(["song1.mp3", "song2.mp3"])

# Open file dialog to select files
client.load_playlist()  # No parameters = open dialog

# Get current playlist
playlist = client.get_playlist()
```

#### File Conversion
```python
# Convert images
client.convert_files(["photo1.png", "photo2.jpg"], mode="PNG to JPG")

# Convert PDF to images
client.convert_files(["document.pdf"], mode="PDF to JPGs")
```

#### Status Monitoring
```python
# Get current player status
status = client.get_status()
print(f"Playing: {status['data']['current_track']}")
print(f"Volume: {status['data']['volume']}%")
print(f"Progress: {status['data']['position']:.1f}/{status['data']['duration']:.1f}s")
```

#### Advanced Controls
```python
# Seek to specific position
client.set_position(30)       # 30 seconds in
client.set_position("50%")    # 50% through track

# Toggle loop mode
client.toggle_loop()

# Check connection
if client.is_connected():
    print("Connected to music player!")
```

---

## ⚙️ Settings Configuration

### API Server Settings
- **Port**: Default 65432 (change in Settings tab if needed)
- **Auto-start**: API server starts automatically with application
- **Restart**: Use "Restart API" button after port changes

### FFmpeg Configuration
1. **Auto-detection**: App tries to find FFmpeg automatically
2. **Manual setup**: Click "📁" to browse to ffmpeg.exe
3. **Download**: Click link to get FFmpeg if not installed

### Download Settings
- **Output folder**: Where downloads are saved
- **Filename template**: Custom naming patterns
- **Quality presets**: Balance between size and quality

---

## 🔧 Troubleshooting

### ❌ "Cannot connect to API"
- Ensure main application is running
- Check firewall isn't blocking port 65432
- Verify API server status in sidebar (should show "✅ Running")

### ❌ "FFmpeg not found"
- Download FFmpeg from https://ffmpeg.org/download.html
- Point to ffmpeg.exe in Settings tab
- Or place ffmpeg.exe in same folder as application

### ❌ "Download failed"
- Check internet connection
- Verify YouTube URL is correct
- Ensure FFmpeg is properly configured

### ❌ "File not playing"
- Check file exists and is valid audio format
- Try different audio files
- Restart application if needed

---

## 📁 File Structure

```
Your_Computer/
├── CodemMusicPlayerV4.exe      # Main application
├── Music_Player_Client.py      # Python API client
├── Downloads/                  # Default download folder
│   ├── audio_files/
│   └── video_files/
└── AppData/Roaming/CodemMusicPlayer/  # Settings and cache
```

---

## 🎯 Advanced API Examples

### Automation Script
```python
from Music_Player_Client import MusicPlayerClient
import time

class MusicAutomation:
    def __init__(self):
        self.client = MusicPlayerClient()
        
    def morning_playlist(self):
        """Start morning playlist routine"""
        # Load relaxing playlist
        self.client.load_playlist(["morning1.mp3", "morning2.mp3"])
        
        # Start playback
        self.client.play()
        self.client.set_volume(40)
        
        # Gradually increase volume
        for vol in range(40, 80, 10):
            time.sleep(30)
            self.client.set_volume(vol)
    
    def download_playlist(self, urls):
        """Download multiple YouTube videos"""
        for url in urls:
            print(f"Downloading: {url}")
            self.client.download(url)
            time.sleep(2)  # Brief pause between downloads
    
    def party_mode(self):
        """Enable party mode settings"""
        self.client.set_volume(85)
        # Could add visual effects or other automation here

# Usage
automator = MusicAutomation()
automator.morning_playlist()
```

### Integration with Other Apps
```python
# Integrate with Discord bot
import discord
from Music_Player_Client import MusicPlayerClient

class MusicBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.music_client = MusicPlayerClient()
    
    async def on_message(self, message):
        if message.content.startswith("!play"):
            url = message.content.split(" ")[1]
            self.music_client.play_url(url)
            await message.channel.send(f"🎵 Now playing: {url}")
        
        if message.content.startswith("!pause"):
            self.music_client.pause()
            await message.channel.send("⏸️ Playback paused")
```

---

## ⚠️ Important Notes

### Requirements
- **Windows** (primary platform, may work on Mac/Linux with Wine)
- **FFmpeg** for YouTube downloads (auto-download available)
- **Python 3.6+** for API client usage only

### Limitations
- YouTube downloads subject to YouTube's terms of service
- Conversion features limited to supported formats
- API requires main application to be running

### Legal
- Only download content you have rights to
- Respect copyright laws
- Personal use only

---

## 📞 Support

- **Website**: [Your Website URL]
- **Issues**: Report on GitHub issues page
- **Feature Requests**: Submit via website contact form

---

## 🔄 Updates

Check for updates regularly for:
- New features
- Bug fixes
- Performance improvements
- Security updates

---

## 🎉 Enjoy Your Music!

Codem Music Player combines powerful media handling with flexible API control, perfect for both casual users and developers wanting to integrate music functionality into their projects.

**Happy listening!** 🎧

---

*Last Updated: [Current Date]*  
*Version: 4.0*  
*Developed Codem*
