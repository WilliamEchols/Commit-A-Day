import pygame
from math import sin, cos, radians
pygame.init()

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("pygame car collision on track")

class Car:
    def __init__(self):
        self.x, self.y, self.width, self.height, self.rotation, self.speed, self.rot_speed = 300, 650, 44, 100, -90, 5, 3
        self.car = pygame.image.load("car.png")
        self.car = pygame.transform.scale(self.car, (self.width, self.height))
        self.ref_car = self.car
        self.rect = self.car.get_rect(center = (round(self.x), round(self.y)))

    def rotate(self, angle):
        self.rotation += angle * self.rot_speed
        self.rotation %= 360
        self.car = pygame.transform.rotate(self.ref_car, self.rotation)
        self.rect = self.car.get_rect(center = (round(self.x), round(self.y)))
        
    def move(self, move):
        self.x += move * cos(radians(self.rotation + 90)) * self.speed
        self.y -= move * sin(radians(self.rotation + 90)) * self.speed

    def collision_check(self, track): # return True -> dead
        points = [ (self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height) ]
        for i in range(len(points)):
            check_point = int(points[i][0] - self.width/2), int(points[i][1] - self.height/2)
            origin = (self.x, self.y)
            
            rot_x = origin[0] + sin(radians(self.rotation + 90)) * (check_point[0] - origin[0]) - cos(radians(self.rotation + 90)) * (check_point[1] - origin[1])
            rot_y = origin[1] + cos(radians(self.rotation + 90)) * (check_point[0] - origin[0]) + sin(radians(self.rotation + 90)) * (check_point[1] - origin[1])

            check_point = (int(rot_x), int(rot_y))

            # pygame.draw.circle(screen, (255, 255, 0), check_point, 5, 5) # corner collision visual markers

            if(check_point[0] > 0 and check_point[0] < 700 and check_point[1] > 0 and check_point[1] < 700):
                if(track.get_at(check_point) == (0, 0, 0, 255)):
                    return True
            else:
                return True # kill if leave arena
        return False


    def draw(self):
        screen.blit(self.car, self.rect)

def main():
    car = Car()
    clock = pygame.time.Clock()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # input
        keys = pygame.key.get_pressed()
        rotate = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        move = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        car.move(-move)
        car.rotate(-rotate)

        # display
        track = pygame.image.load("track.png")
        screen.blit(track, (0, 0))

        # car running logic
        car.draw()
        if(car.collision_check(track)):
            car = Car()

        # updates
        pygame.display.update()
        clock.tick(60)


main()