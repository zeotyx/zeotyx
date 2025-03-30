import pyautogui
import time
import subprocess
import psutil
import pygetwindow as gw

# Function to check if Spotify is running
def is_spotify_running():
    for process in psutil.process_iter(['name']):
        if 'Spotify.exe' in process.info['name']:
            return True
    return False

# Function to open Spotify if not running
def open_spotify():
    if not is_spotify_running():
        try:
            subprocess.Popen("C:\\Users\\lolik\\AppData\\Roaming\\Spotify\\Spotify.exe")  # Update path if necessary
            time.sleep(5)  # Wait for Spotify to launch
            print("Spotify was not running, so it has been opened.")
        except Exception as e:
            print(f"Error opening Spotify: {e}")
            return False
    else:
        print("Spotify is already running.")
    return True

# Function to bring Spotify to the front
def bring_spotify_to_front():
    try:
        windows = gw.getWindowsWithTitle("Spotify")
        if windows:
            spotify_window = windows[0]
            spotify_window.activate()  # Brings the Spotify window to the front
            print("Spotify is now in front.")
        else:
            print("Spotify window not found.")
    except Exception as e:
        print(f"Error bringing Spotify to the front: {e}")

# Function to play a specific playlist from your saved collection
def play_saved_playlist(playlist_name):
    # Open Spotify and bring it to the front first
    if open_spotify():
        bring_spotify_to_front()

        # Assuming Spotify is now focused, simulate 'Ctrl + L' to open the search bar and type the playlist name
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.typewrite(playlist_name)  # Type the name of the saved playlist
        pyautogui.press('enter')  # Hit enter to search
        time.sleep(3)  # Wait for the results to load (increased wait time)

        # Navigate through the search results to find the correct playlist
        # This ensures that we don't select a song from the dropdown
        pyautogui.press('down')  # Move down to the first result
        time.sleep(1)  # Wait for a second to ensure the result is focused
        pyautogui.press('down')  # Move down again to avoid selecting a song

        # After two downs, it should be on the playlist, then select it
        pyautogui.press('enter')  # Select the playlist

        # Wait for the playlist to load and start playing
        time.sleep(2)

        # Simulate play/pause (spacebar) to start the playlist
        pyautogui.press('space')  # Start playing
        print(f"Playing saved playlist: {playlist_name}")

# Now call the function to play your saved playlist
play_saved_playlist('Therian Playlist')  # Replace with the actual name of your saved playlist
