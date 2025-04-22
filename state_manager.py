import pygame
import time
import random
from commons import MORSE_COMMON as ALL_MORSE_CHARACTERS, COMMON_TO_MORSE as ALL_CHARS_TO_MORSE


class StateManager:
    def __init__(self, sound_manager, config_manager):
        """Initialize the game state manager."""
        self.sound_manager = sound_manager
        self.config_manager = config_manager

        # Main state
        self.state = "menu"
        
        # Game state variables
        self.score = 0
        self.exiting_to = None
        
        # Menu selections
        self.menu_selection = 0
        self.play_menu_selection = 0
        self.practice_menu_selection = 0
        
        # Transmit game variables
        self.transmit_input_chars = []
        self.char_to_be_guessed = None
        self.transmit_start_time = None
        self.transmit_last_input_time = 0
        self.transmit_input_complete = False
        
        # Countdown variables
        self.countdown_value = 3
        self.countdown_start_time = 0
        self.next_state_after_countdown = "play"
        
        # Result display variables
        self.result_display_time = 0
        self.result_message = ""
        self.result_color = (255, 255, 255)  # WHITE

        # Receive game variables
        self.char_to_receive = None
        self.receive_input_char = ""
        
        # Practice mode variables
        self.practice_input_char = ""
        self.practice_morse_input = []
        self.practice_morse_result = ""
        self.practice_start_time = None
        self.practice_last_input_time = 0
        self.practice_input_complete = False

        # Game configurations
        self.input_timeout_ms = self.config_manager.get_input_timeout()

    def update(self, current_time_ms):
        """Update game state based on timers and input state."""
        # TODO: Should be possible to skip countdown
        if self.state == "countdown":
            current_time = time.time()
            elapsed = current_time - self.countdown_start_time
            
            if elapsed >= 4:  # After 3,2,1,GO (1s each)
                self.state = self.next_state_after_countdown
                self.score = 0  # Reset score for new game session
                if self.next_state_after_countdown == "play":
                    self.initialize_transmit_game()
                elif self.next_state_after_countdown == "receive_game":
                    self.initialize_receive_game()
        
        # Results state check
        elif self.state in ["result", "receive_result"]:
            if current_time_ms - self.result_display_time >= 2000:  # Show result for 2 seconds
                if self.exiting_to == "menu":
                    self.state = "menu"
                    self.exiting_to = None
                elif self.exiting_to == "quit":
                    self.state = "final_score"
                else:
                    # Transition to next round
                    if self.state == "result":
                        self.state = "play"
                        self.initialize_transmit_game()
                    elif self.state == "receive_result":
                        self.state = "receive_game"
                        self.initialize_receive_game()
        
        # Final score display check
        elif self.state == "final_score":
            if current_time_ms - self.result_display_time >= 2000:
                if self.exiting_to == "quit":
                    # handled by the main game loop
                    self.state = "quit"
                else:
                    self.state = "menu"
                    self.exiting_to = None
        
        # Transmit game input timeout check
        elif self.state == "play" and not self.transmit_input_complete:
            if (self.transmit_last_input_time > 0 and
                current_time_ms - self.transmit_last_input_time > self.input_timeout_ms and
                len(self.transmit_input_chars) > 0):
                self.transmit_input_complete = True
                self.parse_transmit_input()
        
        elif self.state == "receive_game" and self.receive_input_char:
            self.validate_receive_input()

        # Practice morse->char input timeout check
        elif self.state == "practice_morse_to_char" and not self.practice_input_complete:
            if (self.practice_last_input_time > 0 and
                current_time_ms - self.practice_last_input_time > self.input_timeout_ms and
                len(self.practice_morse_input) > 0):
                self.practice_input_complete = True
                self.parse_practice_morse_input()
    
    # State initialization methods
    def initialize_transmit_game(self):
        """Reinitialize the transmit game state for a new round."""
        self.transmit_input_chars = []
        valid_chars = list(ALL_MORSE_CHARACTERS.values())
        self.char_to_be_guessed = random.choice(valid_chars)
        self.transmit_start_time = None
        self.transmit_last_input_time = 0
        self.transmit_input_complete = False
    
    def initialize_receive_game(self):
        """Initialize the receive game state for a new round."""
        self.receive_input_char = ""
        valid_receive_chars = list(ALL_MORSE_CHARACTERS.values())
        self.char_to_receive = random.choice(valid_receive_chars)
        self.sound_manager.play_morse_character(self.char_to_receive)

    # FIXME: finalize practice, rename for clarity
    def initialize_practice_morse_to_char(self):
        """Reset state for morse -> character practice."""
        self.practice_morse_input = []
        self.practice_morse_result = "?"
        self.practice_start_time = None
        self.practice_last_input_time = 0
        self.practice_input_complete = False
    
    # Input parsing methods
    def parse_transmit_input(self):
        """Parse the user's transmit input and check if it matches."""
        user_transmit_input = "".join(self.transmit_input_chars)
    
        target_morse_char = ALL_CHARS_TO_MORSE.get(self.char_to_be_guessed, None)

        if user_transmit_input == target_morse_char:
            self.result_message = "CORRECT!"
            self.result_color = "GREEN"
            self.score += 1

        else:
            # Check if the input is at least a valid morse sequence
            if user_transmit_input in ALL_MORSE_CHARACTERS:
                self.result_message = "WRONG!"
                self.result_color = "RED"
            else:
                self.result_message = "INVALID MORSE!"
                self.result_color = "ORANGE"
        
        self.state = "result"
        self.result_display_time = pygame.time.get_ticks()
        self.transmit_input_complete = False

    def validate_receive_input(self):
        if self.receive_input_char == self.char_to_receive:
            self.result_message = "CORRECT!"
            self.result_color = "GREEN"
            self.score += 1
        else:
            if self.receive_input_char in ALL_CHARS_TO_MORSE:
                self.result_message = "WRONG!"
                self.result_color = "RED"
            else:
                self.result_message = "INVALID MORSE!"
                self.result_color = "ORANGE"
        time.sleep(0.2)
        self.state = "receive_result"
        self.result_display_time = pygame.time.get_ticks()

    # TODO: finalize
    def parse_practice_morse_input(self):
        """Parse the morse input in practice mode."""
        cleaned_input = "".join(self.practice_morse_input)
        try:
            guessed_char = ALL_MORSE_CHARACTERS[cleaned_input]
            self.practice_morse_result = guessed_char
        except KeyError:
            self.practice_morse_result = "INVALID"
        
        # Reset for next input sequence
        self.practice_morse_input = []
        self.practice_input_complete = False