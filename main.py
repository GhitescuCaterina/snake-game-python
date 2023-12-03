import turtle
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 500))

while True:
    # ecranul
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()

#
# # ecranul de joc
# wn = turtle.Screen()
# wn.title("Snake Game in Python")
# wn.bgcolor("grey")
# wn.setup(width=1000, height=700)
# wn.tracer(0)
#
# wn.mainloop()
