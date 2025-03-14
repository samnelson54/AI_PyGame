import pygame  
import math  
import random  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the game window  
screen_width = 800  
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("Cube Survival Game")  
  
# Define colors  
white = (255, 255, 255)  
black = (0, 0, 0)  
red = (255, 0, 0)  
green = (0, 255, 0)  
yellow = (255, 255, 0)  
  
# Define the player cube  
cube_size = 50  
cube_speed = 5  
  
# Create a player cube image  
cube_image = pygame.Surface((cube_size, cube_size), pygame.SRCALPHA)  
cube_image.fill(red)  
  
# Initialize font for text  
font = pygame.font.SysFont(None, 36)  
  
# Game states  
MAIN_MENU = 0  
GAME_PLAY = 1  
DEATH_MENU = 2  
WIN_MENU = 3  
game_state = MAIN_MENU  
  
# Score  
score = 0  
  
# Enemy speed  
enemy_speed = 2  
  
# Function to draw text  
def draw_text(text, font, color, surface, x, y):  
    text_obj = font.render(text, True, color)  
    text_rect = text_obj.get_rect()  
    text_rect.center = (x, y)  
    surface.blit(text_obj, text_rect)  
  
# Main loop  
running = True  
clock = pygame.time.Clock()  
while running:  
    clock.tick(60)  
  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
  
        # Ensure the shooting mechanic is correctly implemented  
        if game_state == GAME_PLAY:  
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_x, mouse_y = pygame.mouse.get_pos()  
                rel_x, rel_y = mouse_x - (cube_x + cube_size // 2), mouse_y - (cube_y + cube_size // 2)  
                angle = math.atan2(rel_y, rel_x)  
                projectiles.append({  
                    "x": cube_x + cube_size // 2,  
                    "y": cube_y + cube_size // 2,  
                    "angle": angle,  
                    "speed": 10  
                })  
  
    if game_state == MAIN_MENU:  
        screen.fill(black)  
        draw_text('Cube Survival Game', font, white, screen, screen_width // 2, screen_height // 2 - 100)  
        draw_text('Play', font, green, screen, screen_width // 2, screen_height // 2)  
  
        mouse_x, mouse_y = pygame.mouse.get_pos()  
        if pygame.mouse.get_pressed()[0]:  
            if screen_width // 2 - 50 < mouse_x < screen_width // 2 + 50 and screen_height // 2 - 25 < mouse_y < screen_height // 2 + 25:  
                # Start game  
                game_state = GAME_PLAY  
                score = 0  
                cube_x = screen_width // 2  
                cube_y = screen_height // 2  
                projectiles = []  
                enemies = []  
  
    elif game_state == GAME_PLAY:  
        # Spawn enemies  
        if random.randint(1, 30) == 1:  
            side = random.choice(['top', 'bottom', 'left', 'right'])  
            if side == 'top':  
                x = random.randint(0, screen_width)  
                y = 0  
            elif side == 'bottom':  
                x = random.randint(0, screen_width)  
                y = screen_height  
            elif side == 'left':  
                x = 0  
                y = random.randint(0, screen_height)  
            else:  # 'right'  
                x = screen_width  
                y = random.randint(0, screen_height)  
  
            enemies.append({"x": x, "y": y})  
  
        # Get key states  
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_a]:  
            cube_x -= cube_speed  
        if keys[pygame.K_d]:  
            cube_x += cube_speed  
        if keys[pygame.K_w]:  
            cube_y -= cube_speed  
        if keys[pygame.K_s]:  
            cube_y += cube_speed  
  
        # Update projectiles  
        for projectile in projectiles:  
            projectile['x'] += projectile['speed'] * math.cos(projectile['angle'])  
            projectile['y'] += projectile['speed'] * math.sin(projectile['angle'])  
  
        # Remove off-screen projectiles  
        projectiles = [p for p in projectiles if 0 <= p['x'] <= screen_width and 0 <= p['y'] <= screen_height]  
  
        # Update enemies  
        for enemy in enemies:  
            dx, dy = cube_x - enemy['x'], cube_y - enemy['y']  
            dist = math.hypot(dx, dy)  
            dx, dy = dx / dist, dy / dist  # Normalize  
            enemy['x'] += dx * enemy_speed  
            enemy['y'] += dy * enemy_speed  
  
        # Check for collisions  
        for enemy in enemies[:]:  
            if pygame.Rect(enemy['x'], enemy['y'], cube_size, cube_size).colliderect(cube_x, cube_y, cube_size, cube_size):  
                game_state = DEATH_MENU  
  
            for projectile in projectiles[:]:  
                if pygame.Rect(enemy['x'], enemy['y'], cube_size, cube_size).collidepoint(projectile['x'], projectile['y']):  
                    enemies.remove(enemy)  
                    projectiles.remove(projectile)  
                    score += 1  
                    if score >= 100:  
                        game_state = WIN_MENU  
                    break  
  
        # Get mouse position for cube rotation  
        mouse_x, mouse_y = pygame.mouse.get_pos()  
        rel_x, rel_y = mouse_x - (cube_x + cube_size // 2), mouse_y - (cube_y + cube_size // 2)  
        angle = math.degrees(math.atan2(rel_y, rel_x))  
  
        # Rotate cube image  
        rotated_image = pygame.transform.rotate(cube_image, -angle)  
        rect = rotated_image.get_rect(center=(cube_x + cube_size // 2, cube_y + cube_size // 2))  
  
        # Fill the screen and draw everything  
        screen.fill(black)  
        screen.blit(rotated_image, rect.topleft)  
        for projectile in projectiles:  
            pygame.draw.circle(screen, yellow, (int(projectile['x']), int(projectile['y'])), 5)  
        for enemy in enemies:  
            pygame.draw.rect(screen, green, (enemy['x'], enemy['y'], cube_size, cube_size))  
  
        # Draw the score on the screen  
        score_text = font.render(f'Score: {score}', True, white)  
        screen.blit(score_text, (10, 10))  
  
    elif game_state == DEATH_MENU:  
        screen.fill(black)  
        draw_text('You Died!', font, red, screen, screen_width // 2, screen_height // 2 - 100)  
        draw_text(f'Score: {score}', font, white, screen, screen_width // 2, screen_height // 2)  
        draw_text('Play Again', font, green, screen, screen_width // 2, screen_height // 2 + 100)  
  
        mouse_x, mouse_y = pygame.mouse.get_pos()  
        if pygame.mouse.get_pressed()[0]:  
            if screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100 and screen_height // 2 + 75 < mouse_y < screen_height // 2 + 125:  
                game_state = GAME_PLAY  
                score = 0  
                cube_x = screen_width // 2  
                cube_y = screen_height // 2  
                projectiles = []  
                enemies = []  
  
    elif game_state == WIN_MENU:  
        screen.fill(black)  
        draw_text('You Win!', font, green, screen, screen_width // 2, screen_height // 2 - 100)  
        draw_text(f'Final Score: {score}', font, white, screen, screen_width // 2, screen_height // 2)  
        draw_text('Play Again', font, green, screen, screen_width // 2, screen_height // 2 + 100)  
  
        mouse_x, mouse_y = pygame.mouse.get_pos()  
        if pygame.mouse.get_pressed()[0]:  
            if screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100 and screen_height // 2 + 75 < mouse_y < screen_height // 2 + 125:  
                game_state = GAME_PLAY  
                score = 0  
                cube_x = screen_width // 2  
                cube_y = screen_height // 2  
                projectiles = []  
                enemies = []  
  
    pygame.display.flip()  
  
pygame.quit()  
