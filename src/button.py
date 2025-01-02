import pygame


class Button:
    #button setting
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path) #Uploading images
        self.image = pygame.transform.scale(self.image, (width, height)) #Resize the image to the desired size
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)#Uploading images  with cursor
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

            #Follows the mouse and checks the actions
        self.rect = self.image.get_rect(topleft=(x, y)) 
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path) #Sound
        self.is_hovered = False


    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image #Determine which button to use (hovered or not)
        screen.blit(current_image, self.rect.topleft)#Image

    #Cursor operation
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    #Cursor operation with sound and actions
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self)) 
            #To open buttons and actions for the main menu


    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
