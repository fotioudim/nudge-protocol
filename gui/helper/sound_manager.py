import pygame
import os
from pathlib import Path

# ==========================================
# Enables sound notifications
# ==========================================
class SoundManager:
    def __init__(self, root, sound_file="funny_alarm.mp3"):
        self.root = root
        self.music_enabled = False
        try:
            pygame.mixer.init()
            
            script_dir = Path(__file__).parent
            sound_path = script_dir / ".." / ".." / "assets" / sound_file
            absolute_sound_path = sound_path.resolve()
            if os.path.exists(absolute_sound_path):
                self.nudge_sound = pygame.mixer.Sound(absolute_sound_path)
                self.music_enabled = True
            else:
                print(f"Warning: {sound_file} not found. Audio disabled.")
        except Exception as e:
            print(f"Failed to initialize audio: {e}")

    def play_nudge(self):
        """Plays the nudge sound if audio is initialized."""
        if self.music_enabled:
            try:
                self.nudge_sound.play()
            except Exception as e:
                print(f"Error playing sound: {e}")
        else:
            self.root.bell()