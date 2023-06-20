import pygame

def num_mapping(input, a, b, c, d):
    result = ((d-c)/(b-a))*(input-a)+c

    return(result)

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
pygame.init()

speed = 0
accel = 0
gear = 0.0
car_break = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            print(event)
            speed = pygame.joystick.Joystick(0).get_axis(0)*10
            accel = pygame.joystick.Joystick(0).get_axis(1)
            car_break = pygame.joystick.Joystick(0).get_axis(2)

            car_break = num_mapping(car_break, -1, 1, 1, 0)
            accel = num_mapping(accel, -1, 1, 1, 0)

        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(13):
                gear += 1.0

                if gear > 7:
                    gear = 7.0

            if pygame.joystick.Joystick(0).get_button(12):
                gear -= 1.0

                if gear < 0:
                    gear = 0.0

    print(accel)