import pygame
import numpy as np
import threading
from src.commons import ALL_TO_MORSE as ALL_CHARS_TO_MORSE

class SoundManager:
    def __init__(self):
        """Initialize the sound manager."""
        self.sound_playing = False
        self.tone = self.generate_tone()
        self.receive_sound_thread = None
    
    def generate_tone(self):
        """Generate the 800 Hz sine wave tone for morse code."""
        sample_rate = 44100
        duration = 1.0  # Buffer length in seconds
        frequency = 800  # Standard Morse frequency
        t = np.arange(0, duration, 1/sample_rate)
        sine_wave = np.sin(2 * np.pi * frequency * t)
        sine_wave = (sine_wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((sine_wave, sine_wave))
        return pygame.sndarray.make_sound(stereo_wave)
    
    def start_tone(self):
        """Start playing the tone."""
        self.tone.play(-1)
        self.sound_playing = True
    
    def stop_tone(self):
        """Stop playing the tone."""
        self.tone.stop()
        self.sound_playing = False
    
    def play_morse_character(self, character):
        """Plays the Morse code sound for a given character without blocking."""
        # Stop any existing sound thread
        if self.receive_sound_thread and self.receive_sound_thread.is_alive():
            self.receive_sound_thread.join()
        
        # Create and start new sound thread
        self.receive_sound_thread = threading.Thread(
            target=self._play_morse_character_thread, 
            args=(character,)
        )
        self.receive_sound_thread.start()
    
    def _play_morse_character_thread(self, character):
        """Thread function to play morse character."""
        if character not in ALL_CHARS_TO_MORSE:
            print(f"Warning: Character '{character}' not found in Morse dictionary.")
            return
        
        char_in_morse = ALL_CHARS_TO_MORSE[character]
        # --- Timing (WPM approx 12-15 based on 100ms dot) ---
        dot_duration = 100  # ms
        dash_duration = 3 * dot_duration  # ms
        symbol_gap = dot_duration  # ms
        letter_gap = 3 * dot_duration  # ms
        # ---
        
        try:
            for i, symbol in enumerate(char_in_morse):
                if symbol == '.':
                    self.tone.play(-1)
                    pygame.time.delay(dot_duration)
                    self.tone.stop()
                elif symbol == '-':
                    self.tone.play(-1)
                    pygame.time.delay(dash_duration)
                    self.tone.stop()
                
                # Gap between symbols within the same character
                if i < len(char_in_morse) - 1:
                    pygame.time.delay(symbol_gap)
            
            # Gap after the character (important for sequences later)
            pygame.time.delay(letter_gap)
        
        except Exception as e:
            print(f"Error playing sound: {e}")
        finally:
            self.tone.stop()  # Ensure tone is stopped
    
    def is_sound_thread_active(self):
        """Check if sound thread is currently active."""
        return self.receive_sound_thread and self.receive_sound_thread.is_alive()
    
    def cleanup(self):
        """Clean up sound resources."""
        if self.sound_playing:
            self.tone.stop()
        
        if self.receive_sound_thread and self.receive_sound_thread.is_alive():
            print("Waiting for sound thread to finish...")
            self.tone.stop()