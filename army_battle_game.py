import pygame
import random
import math
import sys

# PyGame initialization
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("सेना युद्ध - Army Battle Game")

# Colors
RED = (220, 20, 60)  # Red army
BLUE = (30, 144, 255)  # Blue army
GREEN = (50, 205, 50)  # Health bar
DARK_GREEN = (0, 100, 0)  # Background
BLACK = (0, 0, 0)  # Borders
WHITE = (255, 255, 255)  # Text
GOLD = (255, 215, 0)  # Special units

# Fonts
title_font = pygame.font.SysFont("devanagari", 48, bold=True)
font = pygame.font.SysFont("devanagari", 28)
small_font = pygame.font.SysFont("devanagari", 20)

# Soldier class
class Soldier:
    def __init__(self, x, y, color, team, is_hero=False):
        self.x = x
        self.y = y
        self.color = color
        self.team = team
        self.radius = 12 if is_hero else 8
        self.speed = random.uniform(0.7, 1.3) * (1.5 if is_hero else 1.0)
        self.health = 150 if is_hero else 100
        self.max_health = self.health
        self.attack_power = random.randint(8, 18) * (2 if is_hero else 1)
        self.attack_range = 120 if is_hero else 90
        self.target = None
        self.is_hero = is_hero
        
    def draw(self):
        # Draw soldier
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw team indicator
        if self.is_hero:
            pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.radius + 4, 2)
        else:
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius + 2, 1)
        
        # Health bar background
        pygame.draw.rect(screen, BLACK, (self.x - 15, self.y - 25, 30, 5))
        # Health bar
        health_width = 30 * (self.health / self.max_health)
        pygame.draw.rect(screen, GREEN, (self.x - 15, self.y - 25, health_width, 5))
        
    def move(self, enemy_team):
        if self.target is None or self.target.health <= 0 or \
           math.hypot(self.x - self.target.x, self.y - self.target.y) > self.attack_range * 1.5:
            # Find new target
            alive_enemies = [e for e in enemy_team if e.health > 0]
            if alive_enemies:
                self.target = min(alive_enemies, 
                                 key=lambda e: math.hypot(self.x - e.x, self.y - e.y))
        
        if self.target and self.target.health > 0:
            # Move toward target
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = max(0.1, math.hypot(dx, dy))
            
            if dist <= self.attack_range:
                # Attack
                self.target.health -= self.attack_power / 20  # Slower damage for visual effect
            else:
                # Move toward target
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
        else:
            # Random movement if no target
            self.x += random.uniform(-1, 1) * self.speed
            self.y += random.uniform(-1, 1) * self.speed
            
            # Boundary check
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Create armies
def create_armies(red_count, blue_count):
    red_army = []
    blue_army = []
    
    # Add hero units
    red_army.append(Soldier(random.randint(100, 300), random.randint(100, HEIGHT-100), RED, "red", True))
    blue_army.append(Soldier(random.randint(WIDTH-300, WIDTH-100), random.randint(100, HEIGHT-100), BLUE, "blue", True))
    
    # Add regular soldiers
    for _ in range(red_count - 1):
        red_army.append(Soldier(random.randint(50, 400), random.randint(50, HEIGHT-50), RED, "red"))
    
    for _ in range(blue_count - 1):
        blue_army.append(Soldier(random.randint(WIDTH-400, WIDTH-50), random.randint(50, HEIGHT-50), BLUE, "blue"))
    
    return red_army, blue_army

# Draw battle statistics
def draw_stats(red_army, blue_army, battle_time):
    red_alive = sum(1 for s in red_army if s.health > 0)
    blue_alive = sum(1 for s in blue_army if s.health > 0)
    
    # Draw side panels
    pygame.draw.rect(screen, (80, 0, 0), (0, 0, 200, HEIGHT))
    pygame.draw.rect(screen, (0, 0, 80), (WIDTH - 200, 0, 200, HEIGHT))
    
    # Draw center panel
    pygame.draw.rect(screen, (20, 20, 20), (200, 0, WIDTH - 400, 60))
    pygame.draw.rect(screen, GOLD, (200, 0, WIDTH - 400, 60), 2)
    
    # Draw titles
    title = title_font.render("सेना युद्ध", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 5))
    
    # Draw stats
    red_text = font.render(f"लाल सेना: {red_alive}", True, RED)
    blue_text = font.render(f"नीली सेना: {blue_alive}", True, BLUE)
    time_text = font.render(f"समय: {int(battle_time)}s", True, WHITE)
    
    screen.blit(red_text, (20, 100))
    screen.blit(blue_text, (WIDTH - 200 + 20, 100))
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 35))
    
    # Draw health bars for armies
    pygame.draw.rect(screen, BLACK, (20, 150, 160, 20))
    pygame.draw.rect(screen, RED, (20, 150, 160 * (red_alive / len(red_army)), 20))
    
    pygame.draw.rect(screen, BLACK, (WIDTH - 180, 150, 160, 20))
    pygame.draw.rect(screen, BLUE, (WIDTH - 180, 150, 160 * (blue_alive / len(blue_army)), 20))
    
    # Draw instructions
    instructions = [
        "R - नया युद्ध शुरू करें",
        "P - युद्ध रोकें/जारी रखें",
        "ESC - गेम से बाहर निकलें"
    ]
    
    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, WHITE)
        screen.blit(text, (20, 200 + i * 30))
        
    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, WHITE)
        screen.blit(text, (WIDTH - 180, 200 + i * 30))

# Draw game over screen
def draw_game_over(winner, red_army, blue_army):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    if winner == "red":
        text = title_font.render("लाल सेना विजयी हुई!", True, RED)
    elif winner == "blue":
        text = title_font.render("नीली सेना विजयी हुई!", True, BLUE)
    else:
        text = title_font.render("दोनों सेनाएं युद्ध में हार गईं!", True, GOLD)
    
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    
    red_text = font.render(f"लाल सेना: {sum(1 for s in red_army if s.health > 0)}/{len(red_army)}", True, RED)
    blue_text = font.render(f"नीली सेना: {sum(1 for s in blue_army if s.health > 0)}/{len(blue_army)}", True, BLUE)
    
    screen.blit(red_text, (WIDTH // 2 - red_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(blue_text, (WIDTH // 2 - blue_text.get_width() // 2, HEIGHT // 2 + 60))
    
    restart_text = font.render("R दबाएं या रीस्टार्ट बटन क्लिक करें", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 120))
    
    return Button(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 50, "नया युद्ध", RED, BLUE)

# Main game function
def main():
    red_army, blue_army = create_armies(30, 30)
    battle_time = 0
    paused = False
    game_over = False
    winner = None
    
    restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 50, "नया युद्ध", RED, (200, 0, 0))
    
    clock = pygame.time.Clock()
    
    # Main game loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    # Reset game
                    red_army, blue_army = create_armies(30, 30)
                    battle_time = 0
                    game_over = False
                    winner = None
                if event.key == pygame.K_p:
                    # Toggle pause
                    paused = not paused
                    
            if game_over:
                if restart_button.is_clicked(mouse_pos, event):
                    red_army, blue_army = create_armies(30, 30)
                    battle_time = 0
                    game_over = False
                    winner = None
        
        if not paused and not game_over:
            # Update battle time
            battle_time += 1/60  # Assuming 60 FPS
            
            # Move soldiers
            for soldier in red_army + blue_army:
                if soldier.health > 0:
                    enemy_team = blue_army if soldier.team == "red" else red_army
                    soldier.move(enemy_team)
            
            # Check win condition
            red_alive = sum(1 for s in red_army if s.health > 0)
            blue_alive = sum(1 for s in blue_army if s.health > 0)
            
            if red_alive == 0 or blue_alive == 0:
                game_over = True
                if red_alive > 0:
                    winner = "red"
                elif blue_alive > 0:
                    winner = "blue"
                else:
                    winner = "draw"
        
        # Draw everything
        screen.fill(DARK_GREEN)
        
        # Draw battle arena
        pygame.draw.rect(screen, (30, 30, 30), (200, 60, WIDTH - 400, HEIGHT - 60))
        pygame.draw.rect(screen, GOLD, (200, 60, WIDTH - 400, HEIGHT - 60), 2)
        
        # Draw soldiers
        for soldier in red_army + blue_army:
            if soldier.health > 0:
                soldier.draw()
        
        # Draw statistics
        draw_stats(red_army, blue_army, battle_time)
        
        # Draw game over screen if game is over
        if game_over:
            restart_button = draw_game_over(winner, red_army, blue_army)
            restart_button.check_hover(mouse_pos)
            restart_button.draw()
        
        # Draw pause indicator
        if paused:
            pause_text = title_font.render("युद्ध रुका हुआ है", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 100))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
