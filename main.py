import pygame as pg
import math 
import datetime 

""" Clock.py

    This program is an analog clock that grabs the current time from the user's
    system and through a Pygame UI renders the analog clock. 
    
    In the future this widget will contain settings for themes and different formats like 
    digital with 12 and 24 hour formats, world clock options, and eventually custom themes.

    Written by: Noah Chaney
"""

pg.init()

# window setup 
WIDTH = 500
HEIGHT = 500
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Analog Clock")

# grabbing window center for placing elements
CENTER = pg.Vector2(screen.get_width()/2, screen.get_height()/2)

# UI values
RADIUS = 225
BUFFER = 20

tick_length = 10

# math constants for hands and numbers
num_theta = math.radians(30)
hour_theta = num_theta/60
second_theta = math.radians(6)
minute_theta = math.radians(6/60)
degree = math.radians(1)

# function to grab coordinates for a tick or number to display on the clock
def coords(theta, len=0):
    a = (RADIUS - BUFFER - len)*math.cos(theta)
    o_p = a * math.tan(theta)
    return pg.Vector2(CENTER.x + a, CENTER.y + o_p)

# clock initialization
clock = pg.time.Clock()

# text settings
font = pg.font.SysFont("Aldrich", 50)
nums = [str(x) for x in range(1,13)]

# hand settings
hour_width = 5
hour_length = (RADIUS-BUFFER) / 2
minute_width = 3
minute_length = (RADIUS-BUFFER) / 1.2
second_width = 2
second_length = RADIUS - BUFFER

# main loop
exit = False
while not exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True

    # grabbing the current time from the system in a hour, minute, and second format
    now = datetime.datetime.now()

    minute = now.minute
    second = now.second
    hour = now.hour

    screen.fill(pg.Color("black"))

    # main body
    base = pg.draw.circle(screen, pg.Color("white"), CENTER, RADIUS)

    # render clock ticks and numbers
    current_theta = math.radians(-90) # start at the 12 on the clock
    for i in range(1, 61): # range is 1 - 61 to avoid divide by 0 error
        current_theta = current_theta + second_theta # add a tick amount in radians to current angle
        coord = coords(current_theta) # grab current coordinates
        if i % 5 == 0: # test for if a number or tick should render
            txt = font.render(str(nums[(i//5)-1]), True, (0, 0, 0)) 
            screen.blit(txt, (coord.x - txt.get_rect().width/2, coord.y - txt.get_rect().height/2)) 
            #print(nums[(i//5)-1])
        else: # if not a number then draw a tick line
            pg.draw.line(screen, pg.Color("black"), coords(current_theta, tick_length), coord)

    seconds_theta = math.radians(-90) + (second_theta * second)
    minutes_theta = math.radians(-90) + (second_theta * minute) + (minute_theta * second)
    hours_theta = math.radians(-90) + (num_theta * hour) + (hour_theta * minute)

    # drawing the hour, minute, and second hands
    pg.draw.line(screen, pg.Color("black"), start_pos=CENTER, end_pos=coords(hours_theta, RADIUS-hour_length), width=hour_width)
    pg.draw.line(screen, pg.Color("black"), start_pos=CENTER, end_pos=coords(minutes_theta, RADIUS-minute_length), width=minute_width)
    pg.draw.line(screen, pg.Color("red"), start_pos=CENTER, end_pos=coords(seconds_theta, RADIUS-second_length), width=second_width)

    pg.display.flip()

    pg.display.update()
    clock.tick(60)