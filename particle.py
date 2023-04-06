import pygame
import math

class Particle:
    
    VECTOR_SCALAR = 3
    DEBUG = True
    COLLISIONS = True
    DRAG = 0.9999
    ENERGY_LOSS = 0.85
    
    def __init__(self, radius, x, y, colour = (0, 0, 0), speed = 0, direction = 0, mass = 1):
        self.radius = radius #m
        self.x = x
        self.y = y
        self.colour = colour
        self.speed = speed #m/s
        self.direction = direction #radians (0 - RIGHT, pi - LEFT, pi/2 - UP, 3pi/2 - DOWN)
        self.mass = mass #kg
        
    def get_velocity(self):
        vx = math.cos(self.direction) * self.speed
        vy = math.sin(self.direction) * self.speed
        return vy, vx
    
    def collide_point(self, x, y) -> bool:
        dy = self.y - y
        dx = self.x - x
        distance = math.hypot(dy, dx)
        if distance <= self.radius:
            return True
        
        return False
    
    def collide_particle(self, particle) -> bool:
        dy = self.y - particle.y
        dx = self.x - particle.x
        distance = math.hypot(dy, dx)
        if distance <= self.radius + particle.radius:
            return True
        
        return False
    
    def apply_vector(self, direction, speed):
        vy, vx = self.get_velocity()
        new_vx = vx + math.cos(direction) * speed
        new_vy = vy + math.sin(direction) * speed
        new_direction = math.atan2(new_vy, new_vx)
        new_speed = math.hypot(new_vy, new_vx)
        
        self.direction = new_direction
        self.speed = new_speed
        
    def move(self, dt):
        vy, vx = self.get_velocity()
        self.x += vx * dt
        self.y += vy * dt
        self.speed *= Particle.DRAG
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
        if Particle.DEBUG:
            vy, vx = self.get_velocity()
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + vx * Particle.VECTOR_SCALAR, self.y + vy * Particle.VECTOR_SCALAR), 2)
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (self.x, self.y + vy * Particle.VECTOR_SCALAR))
            pygame.draw.line(screen, (0, 0, 255), (self.x, self.y), (self.x + vx * Particle.VECTOR_SCALAR, self.y))
        
    def bounce(self, screen_width, screen_height):
        vy, vx = self.get_velocity()
        
        if self.x < self.radius:
            self.x = self.radius
            self.direction = math.atan2(vy, -vx)
            self.speed *= Particle.ENERGY_LOSS
            
        if self.x > screen_width - self.radius:
            self.x = screen_width - self.radius
            self.direction = math.atan2(vy, -vx)
            self.speed *= Particle.ENERGY_LOSS
            
        if self.y < self.radius:
            self.y = self.radius
            self.direction = math.atan2(-vy, vx)
            self.speed *= Particle.ENERGY_LOSS
            
        if self.y > screen_height - self.radius:
            self.y = screen_height - self.radius
            self.direction = math.atan2(-vy, vx)
            self.speed *= Particle.ENERGY_LOSS
          