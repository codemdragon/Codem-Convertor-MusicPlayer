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

### 📋 **Bulk Playlist Downloader** *(New in V7)*
- Download entire YouTube playlists in one click
- Select specific tracks by index (e.g. `1,3,5` or `2-10`)
- Sequential download queue with live progress
- Optional parallel/concurrent download mode (toggleable)
- Playlist preview before downloading — see all track titles and pick what you want

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
1. Download the latest `CodemMusicPlayerV7.exe` from the releases page
2. Run the executable — no installation required!
3. For API control, download `Music_Player_Client.py` to your project folder

### Option 2: Manual Installation
1. Ensure you have [FFmpeg](https://ffmpeg.org/download.html) installed (for YouTube downloads)
2. Run the executable
3. In Settings tab, configure FFmpeg path if not auto-detected

---

## 🎮 Basic Usage

### Starting the Application
1. Double-click `CodemMusicPlayerV7.exe`
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

### 📋 Bulk Playlist Downloads *(New in V7)*

#### Downloading an Entire Playlist
1. Paste a YouTube **playlist URL** into the URL field
2. Switch to the **Playlist** tab
3. Click `🔍 Load Playlist` to fetch and preview all track titles and their indexes
4. Click `⚡ DOWNLOAD ALL ⚡` to queue every track sequentially

#### Downloading Specific Tracks by Index
After loading a playlist, you can choose exactly which tracks to grab:

| Input Format | What It Does |
|---|---|
| `1,3,5` | Downloads tracks 1, 3, and 5 |
| `2-8` | Downloads tracks 2 through 8 (inclusive) |
| `1,4-7,10` | Downloads 1, then 4 through 7, then 10 |
| *(empty / all)* | Downloads the entire playlist |

1. Load the playlist with `🔍 Load Playlist`
2. Type your index selection into the **Index Filter** field
3. The preview list will highlight your selection
4. Click `⚡ DOWNLOAD SELECTED ⚡`

#### Queue Behaviour
By default, tracks download **one at a time** (sequential mode). Each download finishes before the next begins — reliable and easy on your connection.

Toggle **Parallel Mode** in the Playlist tab or Settings to download multiple tracks simultaneously. Parallel mode is faster on fast connections but uses more bandwidth and CPU.

| Mode | Behaviour | Best For |
|---|---|---|
| 🔁 Sequential *(default)* | One at a time, queued | Stable connections, lower-end PCs |
| ⚡ Parallel | Multiple at once | Fast connections, bulk playlists |

The download queue panel shows:
- ✅ Completed tracks
- ⏳ Currently downloading (with live progress bar)
- 🕐 Queued / waiting
- ❌ Failed (with retry button)

### Playing Music
1. **Load Files**: Click `📁` in the Music Player tab or use the API
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
1. Ensure the main application (`CodemMusicPlayerV7.exe`) is running
2. Copy `Music_Player_Client.py` to your project folder
3. Import and use in your Python scripts:

```python
from Music_Player_Client import MusicPlayerClient

client = MusicPlayerClient()  # Default: localhost:65432
```

### API Examples

#### Basic Playback Control
```python
client.play()
client.pause()
client.stop()
client.next_track()
client.prev_track()
client.set_volume(75)
```

#### Single YouTube Downloads
```python
client.download("https://www.youtube.com/watch?v=EXAMPLE")
client.play_url("https://www.youtube.com/watch?v=EXAMPLE")  # Download + play
```

#### 📋 Playlist & Bulk Downloads *(New in V7)*

```python
# Download an entire playlist (sequential by default)
client.download_playlist("https://www.youtube.com/playlist?list=PLAYLIST_ID")

# Download specific indexes from a playlist
client.download_playlist(
    "https://www.youtube.com/playlist?list=PLAYLIST_ID",
    indexes=[1, 3, 5]           # tracks 1, 3, 5
)

# Download a range of indexes
client.download_playlist(
    "https://www.youtube.com/playlist?list=PLAYLIST_ID",
    indexes=range(2, 11)        # tracks 2 through 10
)

# Mixed ranges and individual indexes
client.download_playlist(
    "https://www.youtube.com/playlist?list=PLAYLIST_ID",
    indexes=[1, *range(4, 8), 10]   # 1, 4-7, 10
)

# Enable parallel (concurrent) downloads
client.download_playlist(
    "https://www.youtube.com/playlist?list=PLAYLIST_ID",
    parallel=True
)
```

#### Inspecting a Playlist Before Downloading
```python
# Fetch playlist metadata without downloading
info = client.get_playlist_info("https://www.youtube.com/playlist?list=PLAYLIST_ID")

for track in info['data']['tracks']:
    print(f"[{track['index']}] {track['title']} ({track['duration']})")
```

Example output:
```
[1] Lo-fi Study Beats Vol.1 (3:42)
[2] Chill Hip Hop Mix (58:21)
[3] Rain Sounds - 1 Hour (1:00:00)
...
```

#### Queue Management
```python
# Check the current download queue
queue = client.get_download_queue()
for item in queue['data']:
    print(f"{item['status']} — {item['title']}")

# Cancel a specific queued item by index
client.cancel_queue_item(3)

# Clear the entire queue (won't cancel active download)
client.clear_queue()
```

#### Playlist Management
```python
client.load_playlist(["song1.mp3", "song2.mp3"])
client.load_playlist()  # Opens file dialog
playlist = client.get_playlist()
```

#### File Conversion
```python
client.convert_files(["photo1.png"], mode="PNG to JPG")
client.convert_files(["document.pdf"], mode="PDF to JPGs")
```

#### Status Monitoring
```python
status = client.get_status()
print(f"Playing: {status['data']['current_track']}")
print(f"Volume:  {status['data']['volume']}%")
print(f"Progress: {status['data']['position']:.1f}/{status['data']['duration']:.1f}s")
```

#### Advanced Controls
```python
client.set_position(30)     # Seek to 30 seconds
client.set_position("50%")  # Seek to 50%
client.toggle_loop()
```

---

## ⚙️ Settings Configuration

### Playlist Download Settings *(New in V7)*
- **Download Mode**: Sequential (default) or Parallel
- **Max Parallel Workers**: 2–5 concurrent downloads in parallel mode (default: 3)
- **Auto-add to Player**: Automatically load completed downloads into the playlist
- **Index Memory**: Remembers your last index filter per playlist URL

### API Server Settings
- **Port**: Default 65432 (change in Settings tab if needed)
- **Auto-start**: API server starts automatically with application
- **Restart**: Use "Restart API" button after port changes

### FFmpeg Configuration
1. **Auto-detection**: App tries to find FFmpeg automatically
2. **Manual setup**: Click "📁" to browse to `ffmpeg.exe`
3. **Download**: Click the link in Settings to get FFmpeg if not installed

### Download Settings
- **Output folder**: Where downloads are saved
- **Filename template**: Custom naming patterns
- **Quality presets**: Balance between size and quality

---

## 🔧 Troubleshooting

### ❌ "Playlist failed to load"
- Make sure the URL is a **playlist** URL (contains `list=` in the link), not a single video
- Some private or age-restricted playlists cannot be fetched
- Ensure FFmpeg is configured correctly

### ❌ "Some tracks skipped in queue"
- Unavailable/deleted/region-locked videos are skipped automatically
- Check the queue panel for ❌ failed items and use the retry button

### ❌ "Cannot connect to API"
- Ensure main application is running
- Check firewall isn't blocking port 65432
- Verify API server status in sidebar (should show "✅ Running")

### ❌ "FFmpeg not found"
- Download FFmpeg from https://ffmpeg.org/download.html
- Point to `ffmpeg.exe` in the Settings tab
- Or place `ffmpeg.exe` in the same folder as the application

### ❌ "Download failed"
- Check your internet connection
- Verify the YouTube URL is correct
- Ensure FFmpeg is properly configured

### ❌ "File not playing"
- Check the file exists and is a valid audio format
- Try different audio files
- Restart the application if needed

---

## 📁 File Structure

```
Your_Computer/
├── CodemMusicPlayerV7.exe      # Main application
├── Music_Player_Client.py      # Python API client
├── Downloads/                  # Default download folder
│   ├── audio_files/
│   └── video_files/
└── AppData/Roaming/CodemMusicPlayer/  # Settings and cache
```

---

## 🎯 Advanced API Examples

### Bulk Playlist Automation
```python
from Music_Player_Client import MusicPlayerClient
import time

client = MusicPlayerClient()

# Preview the playlist first
info = client.get_playlist_info("https://www.youtube.com/playlist?list=YOUR_LIST")
tracks = info['data']['tracks']

print(f"Playlist has {len(tracks)} tracks.\n")
for t in tracks:
    print(f"  [{t['index']}] {t['title']}")

# Pick tracks 1-5 and 10
print("\nQueuing selected tracks...")
client.download_playlist(
    "https://www.youtube.com/playlist?list=YOUR_LIST",
    indexes=[*range(1, 6), 10]
)

# Monitor the queue until done
while True:
    queue = client.get_download_queue()
    pending = [i for i in queue['data'] if i['status'] in ('downloading', 'queued')]
    if not pending:
        break
    print(f"Remaining: {len(pending)} tracks...")
    time.sleep(5)

print("All done! Starting playback.")
client.play()
```

### Morning Playlist Routine
```python
from Music_Player_Client import MusicPlayerClient
import time

class MusicAutomation:
    def __init__(self):
        self.client = MusicPlayerClient()

    def morning_playlist(self):
        self.client.load_playlist(["morning1.mp3", "morning2.mp3"])
        self.client.play()
        self.client.set_volume(40)
        for vol in range(40, 80, 10):
            time.sleep(30)
            self.client.set_volume(vol)

    def download_playlist(self, urls):
        for url in urls:
            print(f"Downloading: {url}")
            self.client.download(url)
            time.sleep(2)

    def party_mode(self):
        self.client.set_volume(85)
```

### Discord Bot Integration
```python
import discord
from Music_Player_Client import MusicPlayerClient

class MusicBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.music = MusicPlayerClient()

    async def on_message(self, message):
        if message.content.startswith("!play"):
            url = message.content.split(" ")[1]
            self.music.play_url(url)
            await message.channel.send(f"🎵 Now playing: {url}")

        if message.content.startswith("!playlist"):
            url = message.content.split(" ")[1]
            self.music.download_playlist(url)
            await message.channel.send(f"📋 Playlist queued!")

        if message.content.startswith("!pause"):
            self.music.pause()
            await message.channel.send("⏸️ Paused")
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
- Parallel mode may be rate-limited by YouTube on large playlists — sequential mode is safer for big batches

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

## 🔄 Changelog

### V7 (Current)
- ✅ Bulk playlist download system
- ✅ Index-based track selection (`1,3,5` or `2-8` or mixed)
- ✅ Sequential download queue with live progress panel
- ✅ Parallel/concurrent download mode (toggleable)
- ✅ `get_playlist_info()` API method for playlist previewing
- ✅ `download_playlist()` API method with index filtering
- ✅ `get_download_queue()`, `cancel_queue_item()`, `clear_queue()` API methods

### V6
- Various bug fixes and performance improvements

### V4–V5
- Initial public release with core player, downloader, converter, and API

---

## 🎉 Enjoy Your Music!

Codem Music Player combines powerful media handling with flexible API control — perfect for both casual users and developers wanting to integrate music functionality into their projects.

**Happy listening!** 🎧

---

*Last Updated: April 2026*
*Version: 7.0*
*Developed by Codem*
