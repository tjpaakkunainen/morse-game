import pygame
import sys
from src.display_manager import DisplayManager
from src.state_manager import StateManager
from src.input_handler import InputHandler
from src.sound_manager import SoundManager
from src.config_manager import ConfigManager

class MorseGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Morse Code Game")
        
        self.config_manager = ConfigManager()
        self.sound_manager = SoundManager()
        self.display_manager = DisplayManager(self.screen)
        self.state_manager = StateManager(self.sound_manager, self.config_manager)
        self.input_handler = InputHandler(self.state_manager, self.display_manager, self.sound_manager)

        self.running = True

    def run_game_loop(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        
        while self.running:
            current_time_ms = pygame.time.get_ticks()
            
            # Update state logic
            self.state_manager.update(current_time_ms)
            
            # Display current state
            self.display_manager.display_current_state(self.state_manager)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                else:
                    self.input_handler.handle_event(event)
            
            # FIXME: needless duplication with event handling?
            if self.state_manager.state == "quit":
                self.quit_game()

            clock.tick(60)  # Limit FPS
    
    def quit_game(self):
        self.sound_manager.cleanup()
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()