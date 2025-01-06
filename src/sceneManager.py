# SceneManager.py

import pygame
import sys

class SceneManager:
    def __init__(self, screen):
# Initialize the SceneManager with a screen and set up storage for scenes
        self.screen = screen
        self.scenes = {}  # Dictionary to store scenes by name
        self.current_scene = None  # Keep track of the active scene

    def add_scene(self, scene_name, scene):
# Add a new scene to the manager
        self.scenes[scene_name] = scene

    def switch_scene(self, scene_name):
# Switch to a new scene by name
        if self.current_scene:
            self.current_scene.cleanup()  # Cleanup the current scene if it exists

        self.current_scene = self.scenes.get(scene_name)  # Get the new scene by name

        if self.current_scene:
            self.current_scene.setup()  # Set up the new scene if it exists

    def run_current_scene(self):
# Run the logic of the current scene
        if self.current_scene:
# Handle events from Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit if the quit event is detected
                    pygame.quit()
                    sys.exit()
                self.current_scene.handle_event(event)  # Pass events to the current scene

            self.current_scene.update()  # Update the current scene
            self.current_scene.render()  # Render the current scene to the screen
