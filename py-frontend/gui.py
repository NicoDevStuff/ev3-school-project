import pygame

SIZE = (54, 30)

class Switch:
    def __init__(self, pos, enabled, label="", fsize=11):
        self.pos = pos
        self.enabled = enabled
        self.rect = pygame.rect.Rect(pos.x, pos.y, SIZE[0], SIZE[1])
        self.lastpressed = False
        self.label = label
        self.fsize = fsize
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.fsize)

    def show(self, screen, event):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        if self.enabled:
            # green boi
            pygame.draw.rect(screen, (0, 255, 0), pygame.rect.Rect(self.pos.x + SIZE[0] / 2, self.pos.y, SIZE[0] / 2, SIZE[1]))
        else:
            # red boi
            pygame.draw.rect(screen, (255, 0, 0), pygame.rect.Rect(self.pos.x, self.pos.y, SIZE[0] / 2, SIZE[1]))
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            mbts = pygame.mouse.get_pressed()
            if mbts[0]:
                if not self.lastpressed: 
                    self.enabled = not(self.enabled)
                    if self.enabled:
                        event()
                self.lastpressed = True

            else:
                self.lastpressed = False

        textsurf = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(textsurf, (self.pos.x, self.pos.y - SIZE[1] + self.fsize))

class Button:
    def __init__(self, pos, enabled, label="", fsize=11):
        self.pos = pos
        self.enabled = enabled
        self.rect = pygame.rect.Rect(pos.x, pos.y, SIZE[0], SIZE[1])
        self.lastpressed = False
        self.label = label
        self.fsize = fsize
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.fsize)

    def show(self, screen, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (90, 90, 90), pygame.rect.Rect(self.pos.x, self.pos.y, SIZE[0], SIZE[1]))
            mbts = pygame.mouse.get_pressed()
            if mbts[0]:
                pygame.draw.rect(screen, (120, 120, 120), pygame.rect.Rect(self.pos.x, self.pos.y, SIZE[0], SIZE[1]))
                if not self.lastpressed: 
                    self.enabled = not(self.enabled)
                    event()
                self.lastpressed = True

            else:
                self.lastpressed = False
        else:
            pygame.draw.rect(screen, (70, 70, 70), pygame.rect.Rect(self.pos.x, self.pos.y, SIZE[0], SIZE[1]))

        textsurf = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(textsurf, (self.pos.x, self.pos.y - SIZE[1] + self.fsize))

class Label:
    def __init__(self, pos, text, fsize=13):
        self.pos = pos
        self.text = text
        self.fsize = fsize
        self.font = pygame.font.Font(pygame.font.get_default_font(), fsize)

    def show(self, screen):
        textsurf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(textsurf, (self.pos.x, self.pos.y))
