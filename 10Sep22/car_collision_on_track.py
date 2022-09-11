# config file adapted from https://github.com/CodeReclaimers/neat-python/blob/master/examples/xor/config-feedforward

import pygame
import math
import neat

screen_width, screen_height = 700, 700
generation = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("car neural network")
clock = pygame.time.Clock()
track = pygame.image.load("track.png")

class Car:
    def __init__(self):
        self.x, self.y, self.width, self.height, self.rotation, self.speed, self.rot_speed, self.distance = 300, 650, 22, 50, -90, 5, 3, 0
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
        self.x += move * math.cos(math.radians(self.rotation + 90)) * self.speed
        self.y -= move * math.sin(math.radians(self.rotation + 90)) * self.speed

        self.distance += self.speed

    def collision_check(self, track): # return True -> dead
        points = [ (self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height) ]
        for i in range(len(points)):
            check_point = int(points[i][0] - self.width/2), int(points[i][1] - self.height/2)
            origin = (self.x, self.y)
            
            rot_x = origin[0] + math.sin(math.radians(self.rotation + 90)) * (check_point[0] - origin[0]) - math.cos(math.radians(self.rotation + 90)) * (check_point[1] - origin[1])
            rot_y = origin[1] + math.cos(math.radians(self.rotation + 90)) * (check_point[0] - origin[0]) + math.sin(math.radians(self.rotation + 90)) * (check_point[1] - origin[1])

            check_point = (int(rot_x), int(rot_y))

            # pygame.draw.circle(screen, (255, 255, 0), check_point, 5, 5) # corner collision visual markers

            if(check_point[0] > 0 and check_point[0] < screen_width and check_point[1] > 0 and check_point[1] < screen_height):
                if(track.get_at(check_point) == (0, 0, 0, 255)):
                    return True
            else:
                return True # kill if leave arena
        return False

    def draw_proximity_lines(self, track):
        dist_arr = []
        for i in range(8):
            angle = i * 45
            calculated_line = self.dist_to_collision(track, angle)
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), calculated_line, 3)

            dist = math.sqrt((abs(calculated_line[0] - self.x) ** 2 + abs(calculated_line[1] - self.y) ** 2))
            dist_arr.append(dist)
        return dist_arr

    def dist_to_collision(self, track, angle):
        accuracy = 1 # less is more
        for i in range(int(screen_width/accuracy)): # assumes screen_width is at least as large as screen_height
            x_val = self.x + i * math.sin(math.radians(self.rotation + angle + 90)) * accuracy
            y_val = self.y + i * math.cos(math.radians(self.rotation + angle + 90)) * accuracy
            point = (int(x_val), int(y_val))
            if(x_val > 0 and x_val < screen_width and y_val > 0 and y_val < screen_height):
                if(track.get_at(point) == (0, 0, 0, 255)):
                    return point
            else:
                return point

    def proximity_report(self, track):
        arr = self.draw_proximity_lines(track)
        return arr

    def draw(self):
        screen.blit(self.car, self.rect)


def run(genomes, config):
    global screen
    nets = []
    cars = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    pygame.init()
    font = pygame.font.SysFont("Arial", 30)

    global generation
    generation += 1
    frame = 0
    while True:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for index, car in enumerate(cars):
            output = nets[index].activate(car.proximity_report(track)) # neural network control options
            i = output.index(max(output))
            if i == 0:
                car.move(True)
            elif i == 1:
                car.rotate(True)
            elif i == 2:
                car.rotate(False)

        for i, car in enumerate(cars):
            genomes[i][1].fitness += car.distance
            car.draw()

        screen.blit(track, (0, 0))
        for car in cars:
            if (car.collision_check(track) or car.distance/frame < 1): # remove cars from simulation if collision or too slow
                del cars[cars.index(car)]
            else:
                car.draw()

        text = font.render(f"Generation: {generation} - Remaining: {len(cars)}", True, (255, 255, 255))
        screen.blit(text, (0, 0, 0, 0))

        if len(cars) == 0:
            break

        pygame.display.flip()
        clock.tick(0)

if __name__ == "__main__":
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.run(run, 1000)