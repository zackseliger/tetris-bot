import pygame

config = {
    'cell_size': 30,
    'cols': 10,
    'rows': 20,
    'delay': 750,
    'maxfps': 60
}

userEventTypes = {
    'left': pygame.USEREVENT+1,# '25'
    'right': pygame.USEREVENT+2,
    'down': pygame.USEREVENT+3,
    'rotate': pygame.USEREVENT+4
}

userEvents = {
    'left': pygame.event.Event(userEventTypes['left']),
    'right': pygame.event.Event(userEventTypes['right']),
    'down': pygame.event.Event(userEventTypes['down']),
    'rotate': pygame.event.Event(userEventTypes['rotate'])
}
