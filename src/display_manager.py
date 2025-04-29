import pygame
import time
from src.commons import COMMON_TO_MORSE as ALL_CHARS_TO_MORSE

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
FONT_SIZE = 24
LARGE_FONT_SIZE = 48
SMALL_FONT_SIZE = 18

GAME_COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "ORANGE": (255, 165, 0),
    "GREY": (200, 200, 200),
}

class DisplayManager:
    def __init__(self, screen):
        """Initialize the display manager."""
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        self.instructions_font = pygame.font.Font(None, SMALL_FONT_SIZE)
        
        # Track if the static parts of the game screen have been drawn
        self.displayed_game_state = False
        
    def display_text(self, text, pos, font, color=GAME_COLORS["WHITE"], center=False):
        """Helper function to render and blit text."""
        lines = text.split("\n")
        y_offset = 0
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            if center:
                text_rect.center = (pos[0], pos[1] + y_offset)
            else:
                text_rect.topleft = (pos[0], pos[1] + y_offset)
            self.screen.blit(text_surface, text_rect)
            y_offset += font.get_linesize()
    
    def display_common_elements(self, state):
        """Displays elements common to most screens (like exit instructions)."""
        esc_message = "ESC to exit"
        back_message = "BACKSPACE for menu"
        full_message = f"{esc_message} | {back_message}" if state not in ["menu", "final_score"] else esc_message
        self.display_text(full_message, (20, SCREEN_HEIGHT - 30), self.instructions_font, GAME_COLORS["GREY"])
    
    def display_current_state(self, state_manager):
        """Display the current game state."""
        if not state_manager.state == "quit":
            method_name = f"display_{state_manager.state}"
            display_method = getattr(self, method_name, self.display_not_implemented)
            display_method(state_manager)
    
    def display_menu(self, state_manager):
        """Display the main menu."""
        self.display_menu_common("MORSE CODE GAME", 
                           ["Play", "Practice", "Settings"], 
                           state_manager.menu_selection,
                           state_manager.state)
    
    def display_play_menu(self, state_manager):
        """Display the play submenu."""
        self.display_menu_common("PLAY MODE",
                           ["Receive", "Transmit"],
                           state_manager.play_menu_selection,
                           state_manager.state)
    
    def display_practice_sub_menu(self, state_manager):
        """Display the practice submenu."""
        self.display_menu_common("PRACTICE MODE",
                           ["Practice Receiving", "Practice Transmitting"],
                           state_manager.practice_menu_selection,
                           state_manager.state)
    
    def display_menu_common(self, title, options, selection, current_state, y_start=120):
        """Generic function to display a menu."""
        self.screen.fill(GAME_COLORS["BLACK"])
        self.display_text(title, (SCREEN_WIDTH // 2, 50), self.font, GAME_COLORS["WHITE"], center=True)

        for i, option in enumerate(options):
            color = GAME_COLORS["YELLOW"] if i == selection else GAME_COLORS["WHITE"]
            self.display_text(option, (SCREEN_WIDTH // 2, y_start + i * 40), self.font, color, center=True)

        instructions = "UP/DOWN arrows to select\nENTER to confirm"
        self.display_text(instructions, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70), self.instructions_font, GAME_COLORS["GREY"], center=True)
        self.display_common_elements(current_state)
        pygame.display.flip()
    
    def display_not_implemented(self, state_manager):
        """Display a message if a state does not exist."""
        self.screen.fill(GAME_COLORS["BLACK"])
        mode_name = state_manager.state.upper().replace("_", " ")
        self.display_text(mode_name, 
                     (SCREEN_WIDTH // 2, 80), self.font, GAME_COLORS["WHITE"], center=True)
        self.display_text("To be implemented soon!", 
                     (SCREEN_WIDTH // 2, 150), self.font, GAME_COLORS["WHITE"], center=True)
        self.display_common_elements(state_manager.state)
        pygame.display.flip()
        
    def display_countdown(self, state_manager):
        """Display the countdown before starting a game."""
        self.screen.fill(GAME_COLORS["BLACK"])
        current_time = time.time()
        elapsed = current_time - state_manager.countdown_start_time

        if elapsed < 1: display_text = "3"
        elif elapsed < 2: display_text = "2"
        elif elapsed < 3: display_text = "1"
        else: display_text = "GO!"

        self.display_text(display_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                     pygame.font.Font(None, 72), GAME_COLORS["YELLOW"], center=True)
        pygame.display.flip()
        
    def display_transmit_game(self, state_manager):
        """Displays the main transmit game screen."""
        
        # FIXME: draw only once per round
        self.screen.fill(GAME_COLORS["BLACK"])
        self.display_text(f"Transmit: {state_manager.char_to_be_guessed}", (20, 50), self.font)
        self.display_text("Your input:", (20, 100), self.font)
        self.display_text(f"Score: {state_manager.score}", (SCREEN_WIDTH - 100, 20), self.font, GAME_COLORS["YELLOW"])
        self.display_common_elements(state_manager.state)

        # Clear previous dynamic input area
        input_rect = pygame.Rect(20, 130, SCREEN_WIDTH - 40, FONT_SIZE * 2)
        self.screen.fill(GAME_COLORS["BLACK"], input_rect)
        # Draw current input
        self.display_text("".join(state_manager.transmit_input_chars), (20, 130), self.font)
        # Clear previous status area
        status_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 130, FONT_SIZE)
        self.screen.fill(GAME_COLORS["BLACK"], status_rect)

        pygame.display.flip()

    def display_receive_game(self, state_manager):
        self.screen.fill(GAME_COLORS["BLACK"])
        self.display_text(f"Listen and type the character", (20, 50), self.font)
        self.display_text(f"Score: {state_manager.score}", (SCREEN_WIDTH - 100, 20), self.font, GAME_COLORS["YELLOW"])
        self.display_common_elements(state_manager.state)
        pygame.display.flip()

    def display_result(self, state_manager):
        """Displays result after a transmit round."""
        correct_char = ALL_CHARS_TO_MORSE.get(state_manager.char_to_be_guessed, "???")
        correct_text = f"Answer: {correct_char} ({state_manager.char_to_be_guessed})"
        user_text = f"You sent: {''.join(state_manager.transmit_input_chars)}"
        self.display_result_common(state_manager.result_message, GAME_COLORS[state_manager.result_color], state_manager.score, correct_text, user_text)

    def display_receive_result(self, state_manager):
        user_text = f"You guessed: {state_manager.receive_input_char} ({ALL_CHARS_TO_MORSE.get(state_manager.receive_input_char, '?')})"
        correct_text = f"Answer: {state_manager.char_to_receive} ({ALL_CHARS_TO_MORSE.get(state_manager.char_to_receive, '?')})"
        self.display_result_common(state_manager.result_message, GAME_COLORS[state_manager.result_color], state_manager.score, correct_text, user_text)

    def display_result_common(self, result_msg, result_clr, score, correct_ans_text, user_guess_text=""):
        """Common display logic for result screens."""
        self.screen.fill(GAME_COLORS["BLACK"])

        # Display result message (CORRECT/WRONG/INVALID)
        self.display_text(result_msg, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40), self.large_font, result_clr, center=True)

        # Display correct answer
        self.display_text(correct_ans_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20), self.font, GAME_COLORS["WHITE"], center=True)

        # Display user's guess if provided
        if user_guess_text:
             self.display_text(user_guess_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), self.font, GAME_COLORS["GREY"], center=True)

        # Display current score
        score_text = f"Score: {score}"
        self.display_text(score_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50), self.font, GAME_COLORS["YELLOW"], center=True)

        pygame.display.flip()    
    
    def display_final_score(self, state_manager):
        """Display the final score before exiting or returning to menu."""
        self.screen.fill(GAME_COLORS["BLACK"])
        message = f"Final score: {state_manager.score}"
        self.display_text(message, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), self.large_font, GAME_COLORS["YELLOW"], center=True)
        pygame.display.flip()


