import pygame
import math
import particle
import time
import random

WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()

class Screen:
    
    DRAG_SPEED = 0.1
    
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.particles = []
        self.running = False
        self.paused = True
        self.background_colour = WHITE
        self.selected_particle = None
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.FPS = 200
        self.average_FPS = self.FPS
        self.clock_fps = self.FPS
        
    def collide(self, particle1, particle2):
        pass
        
    def particle_loop(self, dt):
        for index, particle_ in enumerate(self.particles):
            if not self.paused:
                particle_.apply_vector(1.5 * math.pi, -9.81 * dt / self.clock_fps)
                particle_.move(dt)
                particle_.bounce(self.width, self.height)
                
                if particle.Particle.COLLISIONS:
                    for particle2 in self.particles[index + 1:]:
                        if particle.collide_particle(particle2):
                            self.collide(particle, particle2)
                    
            particle_.draw(self.screen)
                    
    def get_particle_at(self, x, y):
        for particle in self.particles:
            if particle.collide_point(x, y):
                return particle
                    
    def draw_ui(self):
        fps_text = self.font.render(f"FPS: {round(self.clock_fps, 2)}", True, (0, 0, 0))
        average_fps_text = self.font.render(f"Average FPS: {round(self.average_FPS, 2)}", True, (0, 0, 0))
        paused_text = self.font.render(f"Paused: {self.paused}", True, (0, 0, 0))
        
        self.screen.blit(fps_text, (0, 0))
        self.screen.blit(average_fps_text, (0, 25))
        self.screen.blit(paused_text, (0, 50))
        
    def mainloop(self):
        self.running = True
        start_time = time.time()
        start_frame_time = time.time()
        last_time = 0
        total_frames = 0
        while self.running:
            
            game_time = time.time() - start_time
            dt = (game_time - last_time) * self.clock_fps
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        break
                    
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.selected_particle = self.get_particle_at(event.pos[0], event.pos[1])
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.selected_particle = None
                    
            if self.selected_particle:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.selected_particle.x
                dy = mouse_y - self.selected_particle.y
                self.selected_particle.direction = math.atan2(dy, dx)
                self.selected_particle.speed = math.hypot(dy, dx) * Screen.DRAG_SPEED
            
            self.screen.fill(self.background_colour)
            self.particle_loop(dt)
            self.draw_ui()
            pygame.display.flip()
            
            last_time = game_time
            
            self.clock.tick(self.FPS)
            
            total_frames += 1
            self.average_FPS = total_frames / (time.time() - start_frame_time)
            if time.time() - start_frame_time >= 10:
                start_frame_time = time.time()
                self.average_FPS = self.clock_fps
                total_frames = 0
                
            self.clock_fps = self.clock.get_fps()
                    
        pygame.quit()
        
    def generate_random_particles(self, number: int, radius_range: tuple[float, float], speed_range: tuple[float, float], mass_range: tuple[float, float]):
        for i in range(number):
            radius = random.uniform(radius_range[0], radius_range[1])
            x = random.uniform(0 + radius, self.width - radius)
            y = random.uniform(0 + radius, self.height - radius)
            colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            speed = random.uniform(speed_range[0], speed_range[1])
            direction = random.uniform(0, 2*math.pi)
            mass = random.uniform(mass_range[0], mass_range[1])
            new_particle = particle.Particle(radius, x, y, colour, speed, direction, mass)
            self.particles.append(new_particle)

if __name__ == "__main__":
    particle.Particle.DEBUG = True
    particle.Particle.COLLISIONS = False
    screen = Screen()
    screen.generate_random_particles(100, (5, 10), (1, 5), (1, 5))
    screen.mainloop()