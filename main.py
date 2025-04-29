#!/usr/bin/env python3
import pygame
from src.morse_game import MorseGame

def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2)
    
    game = MorseGame()
    game.run_game_loop()
    
if __name__ == "__main__":
    main()