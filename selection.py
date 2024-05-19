
class SelectNumber:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_width = 60
        self.btn_height = 60
        self.num_font = font
        self.selected_number = 0
        
        self.color_selected = (0, 255, 0)
        self.color_normal = (200, 200, 200)
        
        self.btn_positions = [ (780, 40), (860, 40),
                               (780, 120), (860, 120),
                               (780, 200), (860, 200),
                               (780, 280), (860, 280),
                               (860, 360) ]
      
      
    def draw(self, pygame, surface):
        for index, pos in enumerate(self.btn_positions):
            x, y = pos
            pygame.draw.rect(surface, self.color_normal, [x, y, self.btn_width, self.btn_height], width=3, border_radius=10)

            # check for mouse hover
            if self.button_hover(pos):
                pygame.draw.rect(surface, self.color_selected, [x, y, self.btn_width, self.btn_height], width=3, border_radius=10)
                text_surface = self.num_font.render(str(index + 1), False, self.color_selected)
            else:
                text_surface = self.num_font.render(str(index + 1), False, self.color_normal)
            
            # check if a number is selected, then draw it green
            if self.selected_number > 0:
                if self.selected_number == index + 1:
                    pygame.draw.rect(surface, self.color_selected, [x, y, self.btn_width, self.btn_height], width=3, border_radius=10)
                    text_surface = self.num_font.render(str(index + 1), False, self.color_selected)
            
            surface.blit(text_surface, (x + 18, y))
            

    def button_clicked(self, mouse_x: int, mouse_y: int) -> None:
        """ Check for mouse hover over a button. """
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_number = index + 1


    def button_hover(self, pos: tuple) -> bool|None:
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True
        

    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool|None:
        x, y = pos
        return (x < mouse_x < x + self.btn_width) and (y < mouse_y < y + self.btn_height)
