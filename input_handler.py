import pygame
import time
from commons import ALL_TO_MORSE as ALL_CHARS_TO_MORSE

# TODO: should be modifiable?
THRESHOLD = 0.2  # Time threshold for dot vs dash

class InputHandler:
    def __init__(self, state_manager, display_manager, sound_manager):
        self.state_manager = state_manager
        self.display_manager = display_manager
        self.sound_manager = sound_manager
        
    def handle_event(self, event, current_time_ms):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.KEYUP:
            self.handle_keyup(event)
    
    def handle_keydown(self, event):
        """Handle key press events."""
        # Global Keys
        if event.key == pygame.K_ESCAPE:
            self._handle_escape()
            return
            
        if event.key == pygame.K_BACKSPACE:
            self._handle_backspace()
            return
            
        # State-specific handlers
        method_name = f"_handle_keydown_{self.state_manager.state}"
        if hasattr(self, method_name):
            handler = getattr(self, method_name)
            handler(event)
    
    def handle_keyup(self, event):
        """Handle key release events."""
        # Handle specific key releases for states
        if self.state_manager.state == "transmit_game" and event.key == pygame.K_SPACE:
            self._handle_keyup_transmit_game()
        elif self.state_manager.state == "practice_morse_to_char" and event.key == pygame.K_SPACE:
            self._handle_keyup_practice_morse_to_char(event)
    
    # --- Global key handlers ---
    # FIXME: final_score should probably be displayed only if there is a result
    def _handle_escape(self):
        """Handle escape key globally."""
        if self.state_manager.state in ["transmit_game", "receive_game"]:
            self.state_manager.exiting_to = "quit"
            self.state_manager.state = "final_score"
            self.state_manager.result_display_time = pygame.time.get_ticks()
        else:
            self.state_manager.state = "quit"
    
    def _handle_backspace(self):
        """Handle backspace key globally."""
        if self.state_manager.state in ["transmit_game", "receive_game", "result", "receive_result"]:
            self.state_manager.exiting_to = "menu"
            self.state_manager.state = "final_score"
            self.state_manager.result_display_time = pygame.time.get_ticks()
        elif self.state_manager.state in ["play_menu", "practice_sub_menu", "settings"]:
            self.state_manager.state = "menu"
            # Reset selections
            self.state_manager.play_menu_selection = 0
            self.state_manager.practice_menu_selection = 0
        elif self.state_manager.state in ["practice_char_to_morse", "practice_morse_to_char"]:
            self.state_manager.state = "practice_sub_menu"
        elif self.state_manager.state == "countdown":
            self.state_manager.state = "menu"
    
    # --- State-specific key handlers ---
    def _handle_keydown_menu(self, event):
        """Handle key presses in main menu."""
        if event.key == pygame.K_UP:
            self.state_manager.menu_selection = (self.state_manager.menu_selection - 1) % 3
        elif event.key == pygame.K_DOWN:
            self.state_manager.menu_selection = (self.state_manager.menu_selection + 1) % 3
        elif event.key == pygame.K_RETURN:
            if self.state_manager.menu_selection == 0:
                self.state_manager.state = "play_menu"
            elif self.state_manager.menu_selection == 1:
                self.state_manager.state = "practice_sub_menu"
            elif self.state_manager.menu_selection == 2:
                self.state_manager.state = "settings"
    
    def _handle_keydown_play_menu(self, event):
        """Handle key presses in play menu."""
        if event.key == pygame.K_UP:
            self.state_manager.play_menu_selection = (self.state_manager.play_menu_selection - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.state_manager.play_menu_selection = (self.state_manager.play_menu_selection + 1) % 2
        elif event.key == pygame.K_RETURN:
            self.state_manager.state = "countdown"
            self.state_manager.countdown_start_time = time.time()
            if self.state_manager.play_menu_selection == 0:  # Receive
                self.state_manager.next_state_after_countdown = "receive_game"
            else:
                self.state_manager.next_state_after_countdown = "transmit_game"
    
    def _handle_keydown_practice_sub_menu(self, event):
        """Handle key presses in practice submenu."""
        if event.key == pygame.K_UP:
            self.state_manager.practice_menu_selection = (self.state_manager.practice_menu_selection - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.state_manager.practice_menu_selection = (self.state_manager.practice_menu_selection + 1) % 2
        elif event.key == pygame.K_RETURN:
            if self.state_manager.practice_menu_selection == 0:  # Char -> Morse
                self.state_manager.state = "practice_char_to_morse"
                self.state_manager.practice_input_char = "?"
            elif self.state_manager.practice_menu_selection == 1:  # Morse -> Char
                self.state_manager.state = "practice_morse_to_char"
                self.state_manager.initialize_practice_morse_to_char()
    
    def _handle_keydown_transmit_game(self, event):
        """Handle key presses in transmit game."""
        if event.key == pygame.K_SPACE and not self.sound_manager.sound_playing:
            self.state_manager.transmit_start_time = time.time()
            self.sound_manager.start_tone()
            self.state_manager.transmit_last_input_time = 0

    def _handle_keyup_transmit_game(self):
        """Handle space key release in transmit game."""
        if self.sound_manager.sound_playing:
            self.sound_manager.stop_tone()
            time_pressed = time.time() - self.state_manager.transmit_start_time
            self.state_manager.transmit_input_chars.append("-" if time_pressed > THRESHOLD else ".")
            self.state_manager.transmit_last_input_time = pygame.time.get_ticks()

    def _handle_keydown_receive_game(self, event):
        """Handle key presses in receive game."""
        if not self.sound_manager.is_sound_thread_active():
            if event.unicode.upper() in ALL_CHARS_TO_MORSE:
                self.state_manager.receive_input_char = event.unicode.upper()
            self.state_manager.result_display_time = pygame.time.get_ticks()

    def _handle_keyup_practice_morse_to_char(self, event):
        """Handle space key release in morse->char practice."""
        if self.sound_manager.sound_playing:
            self.sound_manager.stop_tone()
            time_pressed = time.time() - self.state_manager.practice_start_time
            self.state_manager.practice_morse_input.append("-" if time_pressed > THRESHOLD else ".")
            self.state_manager.practice_last_input_time = pygame.time.get_ticks()

    def _handle_keydown_practice_morse_to_char(self, event):
        """Handle key presses in morse->char practice."""
        if event.key == pygame.K_SPACE and not self.sound_manager.sound_playing:
            self.state_manager.practice_start_time = time.time()
            self.sound_manager.start_tone()
            self.state_manager.practice_last_input_time = 0

    def _handle_keydown_practice_char_to_morse(self, event):
        """Handle key presses in char->morse practice."""
        char = event.unicode.upper()
        if char in ALL_CHARS_TO_MORSE:
            self.state_manager.practice_input_char = char
            self.sound_manager.play_morse_character(char)
    