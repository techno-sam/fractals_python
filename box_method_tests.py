import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))

class Box:
    def __init__(self, rect: pygame.Rect):
        self.children: list[Box] | None = None
        self.rect: pygame.Rect = rect

    def draw(self, surf: pygame.Surface):
        pygame.draw.line(surf, (255, 255, 255), self.rect.topleft, self.rect.topright)
        pygame.draw.line(surf, (255, 255, 255), self.rect.topright, self.rect.bottomright)
        pygame.draw.line(surf, (255, 255, 255), self.rect.bottomright, self.rect.bottomleft)
        pygame.draw.line(surf, (255, 255, 255), self.rect.bottomleft, self.rect.topleft)
        if self.children is not None:
            for child in self.children:
                child.draw(surf)

    def split_at(self, click_pos: tuple[int, int]):
        if not self.rect.collidepoint(*click_pos):
            return
        if self.children is None:
            self.split()
        else:
            for child in self.children:
                child.split_at(click_pos)

    def split(self):
        if self.children is None:
            x_split = self.rect.centerx
            y_split = self.rect.centery
            """
                                    rect.top
                    |-----------------|-----------------|
                    |                 |                 |
                    |                 |                 |
                    |                 |                 |
                    |                 |     y_split     |
        rect.left   |-----------------|-----------------|   rect.right
                    |                 |                 |
                    |                 |                 |
                    |                 |x_split          |
                    |                 |                 |
                    |-----------------|-----------------|
                                    rect.bottom
    """
            self.children = [
                Box(pygame.Rect(self.rect.left, self.rect.top, x_split-self.rect.left, y_split-self.rect.top)),
                Box(pygame.Rect(x_split, self.rect.top, self.rect.right-x_split, y_split-self.rect.top)),
                Box(pygame.Rect(self.rect.left, y_split, x_split - self.rect.left, self.rect.bottom - y_split)),
                Box(pygame.Rect(x_split, y_split, self.rect.right - x_split, self.rect.bottom - y_split))
            ]
        else:
            for child in self.children:
                child.split()

main = Box(pygame.Rect(0, 0, 800, 800))

kg = True
while kg:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kg = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            main.split()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            main.split_at(mp)

    screen.fill((0, 0, 0))
    main.draw(screen)
    pygame.display.update()

pygame.quit()