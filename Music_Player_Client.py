"""
Music Player Client API
======================
This client allows you to control the Codem Music Player from other Python scripts.
Make sure the main application (YTm4.exe) is running before using this client.

Usage:
    from Music_Player_Client import MusicPlayerClient
    
    client = MusicPlayerClient()
    client.play()
    client.pause()
    client.download("https://www.youtube.com/watch?v=...")
"""

import socket
import pickle
import time

class MusicPlayerClient:
    """
    Client to control the Codem Music Player via API.
    """
    
    def __init__(self, host='localhost', port=65432, timeout=5):
        """
        Initialize the client.
        
        Args:
            host (str): Hostname where the player is running (default: localhost)
            port (int): API port (default: 65432)
            timeout (int): Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connected = False
        
    def _send_command(self, command, params=None):
        """
        Send a command to the music player server.
        
        Args:
            command (str): Command name
            params (dict): Command parameters
            
        Returns:
            dict: Server response
        """
        if params is None:
            params = {}
            
        request = {
            'command': command,
            'params': params
        }
        
        try:
            # Create socket connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.host, self.port))
                
                # Send request
                sock.send(pickle.dumps(request))
                
                # Receive response
                data = b""
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    
                response = pickle.loads(data)
                self.connected = True
                return response
                
        except (socket.timeout, ConnectionRefusedError, ConnectionError):
            self.connected = False
            raise ConnectionError(f"Could not connect to Music Player at {self.host}:{self.port}. "
                                 f"Make sure the application is running.")
        except Exception as e:
            self.connected = False
            raise RuntimeError(f"Error communicating with Music Player: {e}")
    
    def is_connected(self):
        """Check if client is connected to the server."""
        return self.connected
    
    # Player Control Methods
    
    def play(self):
        """
        Start or resume playback.
        
        Returns:
            dict: Server response
        """
        return self._send_command('play')
    
    def pause(self):
        """
        Pause playback.
        
        Returns:
            dict: Server response
        """
        return self._send_command('pause')
    
    def stop(self):
        """
        Stop playback.
        
        Returns:
            dict: Server response
        """
        return self._send_command('stop')
    
    def next_track(self):
        """
        Play next track in playlist.
        
        Returns:
            dict: Server response
        """
        return self._send_command('next')
    
    def previous_track(self):
        """
        Play previous track in playlist.
        
        Returns:
            dict: Server response
        """
        return self._send_command('prev')
    
    def set_volume(self, volume):
        """
        Set volume level (0-100).
        
        Args:
            volume (int): Volume level from 0 to 100
            
        Returns:
            dict: Server response
        """
        if not 0 <= volume <= 100:
            raise ValueError("Volume must be between 0 and 100")
        return self._send_command('set_volume', {'volume': volume})
    
    def load_playlist(self, files=None):
        """
        Load a playlist.
        
        Args:
            files (list): List of file paths to load. If None, opens file dialog.
            
        Returns:
            dict: Server response
        """
        params = {}
        if files:
            params['files'] = files
        return self._send_command('load_playlist', params)
    
    def download(self, url):
        """
        Download a YouTube video/audio.
        
        Args:
            url (str): YouTube URL to download
            
        Returns:
            dict: Server response
        """
        return self._send_command('download', {'url': url})
    
    def get_status(self):
        """
        Get current player status.
        
        Returns:
            dict: Status information including:
                - is_playing (bool): Whether audio is playing
                - is_paused (bool): Whether playback is paused
                - current_track (str): Current track filename
                - playlist_index (int): Current track index in playlist
                - playlist_length (int): Total tracks in playlist
                - volume (float): Current volume (0-100)
                - position (float): Current playback position in seconds
                - duration (float): Total track duration in seconds
        """
        return self._send_command('get_status')
    
    def get_playlist(self):
        """
        Get current playlist.
        
        Returns:
            dict: Playlist information
        """
        return self._send_command('get_playlist')
    
    def set_position(self, position):
        """
        Set playback position.
        
        Args:
            position (str or float): Position in seconds or as percentage string (e.g., "50%").
                                      If string ends with '%', treated as percentage.
            
        Returns:
            dict: Server response
        """
        return self._send_command('set_position', {'position': position})
    
    def toggle_loop(self):
        """
        Toggle loop mode (none → track → playlist → none).
        
        Returns:
            dict: Server response
        """
        return self._send_command('toggle_loop')
    
    def convert_files(self, files, mode="PNG to JPG"):
        """
        Convert files using the file converter.
        
        Args:
            files (list): List of file paths to convert
            mode (str): Conversion mode (default: "PNG to JPG")
                        Options: "PNG to JPG", "JPG to PNG", "PNG to ICO", 
                                 "Image to WebP", "WebP to PNG", "PDF to JPGs", "JPGs to PDF"
            
        Returns:
            dict: Server response
        """
        return self._send_command('convert_files', {'files': files, 'mode': mode})
    
    # Convenience Methods
    
    def play_url(self, url):
        """
        Download and immediately play a YouTube URL.
        
        Args:
            url (str): YouTube URL
            
        Returns:
            dict: Server response
        """
        # First download
        result = self.download(url)
        if result.get('status') == 'success':
            # Wait a moment for download to start
            time.sleep(1)
            # Then play if not already playing
            status = self.get_status()
            if status.get('status') == 'success':
                if not status.get('data', {}).get('is_playing'):
                    return self.play()
        return result
    
    def add_to_queue(self, url):
        """
        Download a YouTube URL and add to playlist without playing.
        
        Args:
            url (str): YouTube URL
            
        Returns:
            dict: Server response
        """
        return self.download(url)
    
    def get_current_track_info(self):
        """
        Get information about current track.
        
        Returns:
            dict: Current track information or None if error
        """
        status = self.get_status()
        if status.get('status') == 'success':
            return status.get('data')
        return None
    
    def wait_for_download(self, timeout=60):
        """
        Wait for current download to complete.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if download completed, False if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_status()
            if status.get('status') == 'success':
                # Check if we're in download mode
                time.sleep(1)
            else:
                return True
        return False


# Example usage function
def example_usage():
    """Example of how to use the Music Player Client"""
    
    # Create client instance
    client = MusicPlayerClient()
    
    try:
        # Check connection
        print("Testing connection...")
        status = client.get_status()
        print(f"Connected: {client.is_connected()}")
        print(f"Status: {status}")
        
        # Control playback
        print("\nPlaying...")
        result = client.play()
        print(f"Play result: {result}")
        
        time.sleep(2)
        
        print("\nPausing...")
        result = client.pause()
        print(f"Pause result: {result}")
        
        time.sleep(1)
        
        print("\nSetting volume to 80%...")
        result = client.set_volume(80)
        print(f"Volume result: {result}")
        
        # Download a YouTube video
        print("\nDownloading YouTube video...")
        result = client.download("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print(f"Download result: {result}")
        
        # Get playlist
        print("\nGetting playlist...")
        playlist = client.get_playlist()
        print(f"Playlist: {playlist}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Codem Music Player (YTm4.exe) is running!")


if __name__ == "__main__":
    # Run example if script is executed directly
    example_usage()