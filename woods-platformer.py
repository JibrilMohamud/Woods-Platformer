import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Forest Platformer')

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

START_SCREEN = 0
MAIN_GAME = 1
GAME_OVER = 2
game_state = START_SCREEN


BACKGROUND_COLOR = (135, 206, 235)  
BROWN = (139, 69, 19)  
GREEN = (34, 139, 34)  
GRASS_COLOR = (50, 205, 50)  
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  
RED = (255, 0, 0)
BLACK = (0, 0, 0)

def draw_tree(x, y):
    trunk_width, trunk_height = 20, 40
    foliage_radius = 30
    pygame.draw.rect(screen, BROWN, (x, y, trunk_width, trunk_height)) 
    pygame.draw.circle(screen, GREEN, (x + trunk_width // 2, y), foliage_radius)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def update(self, scroll_speed):
        self.x -= scroll_speed
        
    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), 15)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(7, 10)
    def update(self, scroll_speed):
        self.x -= (self.speed + scroll_speed)
    def draw(self):
        pygame.draw.ellipse(screen, BROWN, (self.x, self.y, 40, 20))
        pygame.draw.circle(screen, BROWN, (self.x, self.y + 10), 10)
        pygame.draw.circle(screen, BLACK, (self.x - 5, self.y + 8), 3)
        pygame.draw.polygon(screen, BLACK, [(self.x - 26, self.y + 10), (self.x - 11, self.y + 5), (self.x - 11, self.y + 15)])
        pygame.draw.ellipse(screen, BROWN, (self.x + 15, self.y - 5, 30, 10))
        pygame.draw.ellipse(screen, BROWN, (self.x - 15, self.y - 5, 30, 10))
    
class SmartBird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(5, 10)

    def update(self, player_pos, scroll_speed):
        if self.x > player_pos[0]:
            self.x -= self.speed + scroll_speed
        if self.y > player_pos[1]:
            self.y -= self.speed
        else:
            self.y += self.speed

    def draw(self):
        pygame.draw.ellipse(screen, BROWN, (self.x, self.y, 40, 20))
        pygame.draw.circle(screen, BROWN, (self.x, self.y + 10), 10)
        pygame.draw.circle(screen, BLACK, (self.x - 5, self.y + 8), 3)
        pygame.draw.polygon(screen, BLACK, [(self.x - 26, self.y + 10), (self.x - 11, self.y + 5), (self.x - 11, self.y + 15)])
        pygame.draw.ellipse(screen, BROWN, (self.x + 15, self.y - 5, 30, 10))
        pygame.draw.ellipse(screen, BROWN, (self.x - 15, self.y - 5, 30, 10))


def generate_trees(num_trees, min_spacing=50):
    trees = []
    current_x = SCREEN_WIDTH
    for _ in range(num_trees):
        current_x += min_spacing + random.randint(100, 350)  
        trees.append((current_x, SCREEN_HEIGHT - 140))
    return trees


def generate_coins(num_coins):
    coins = []
    current_x = 0
    i = 0
    for i in range(num_coins):
        coin_x = current_x + random.randint(100, 350) 
        coin_y = random.randint(300, 400)  
        coins.append(Coin(coin_x, coin_y))
        current_x = coin_x  + 250
        i += 1
    return coins

def generate_birds():
    birds = []
    for _ in range(random.randint(1, 5)):  
        bird_x = SCREEN_WIDTH
        bird_y = random.randint(300, 420)
        if random.randint(0, 100) < 1:  
            birds.append(SmartBird(bird_x, bird_y))
        else:
            birds.append(Bird(bird_x, bird_y))
    return birds


def reset_tree_position(trees, min_spacing=50):
    last_tree_x = max(trees, key=lambda t: t[0])[0]
    new_x = last_tree_x + min_spacing + random.randint(100, 350)
    return new_x, SCREEN_HEIGHT - 140

trees = generate_trees(5)
coins = generate_coins(5000)
birds = generate_birds()
coin_count = 0

scroll_speed = 2
player_size = (50, 50)
player_pos = [100, 500]
player_speed = 5
player_vel_y = 0
gravity = 0.5
jump_strength = -10
ground_level = 500 - player_size[1]
jumps = 0

frame1 = pygame.image.load("frame1.png").convert_alpha()
frame2 = pygame.image.load("frame2.png").convert_alpha()
frame1 = pygame.transform.scale(frame1, player_size)
frame2 = pygame.transform.scale(frame2, player_size)
player_frames = [frame1, frame2]
frame_index = 0
animation_speed = 0.1 
animation_delay = 5 
current_delay = 0

def draw_cloud(x, y):
    pygame.draw.ellipse(screen, WHITE, (x, y, 80, 40))
    pygame.draw.ellipse(screen, WHITE, (x - 40, y + 20, 80, 40))
    pygame.draw.ellipse(screen, WHITE, (x + 40, y + 20, 80, 40))
    pygame.draw.ellipse(screen, WHITE, (x, y + 20, 80, 40))

def check_collision(player_rect, rect):
    return player_rect.colliderect(rect)


bubble_active = False
bubble_duration = 100  
bubble_timer = 0

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_state == START_SCREEN:
                game_state = MAIN_GAME
            elif event.key == pygame.K_RETURN and game_state == GAME_OVER:
                game_state = START_SCREEN
                player_pos = [100, 500]
                player_speed = 5
                scroll_speed = 2
                trees = generate_trees(5)
                coins = generate_coins(5000)  
                birds = generate_birds()
                jumps = 0 
                coin_count = 0  
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                if jumps < 2:  
                    player_vel_y = jump_strength
                    jumps += 1
                    frame_index = 0
            elif event.key == pygame.K_d and not bubble_active:
                if coin_count >= 5:
                    bubble_active = True
                    bubble_timer = bubble_duration
                    coin_count -= 5
                else:
                    print("Not enough coins to activate bubble")  

    if game_state == START_SCREEN:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Press Enter to Start", True, WHITE)
        screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, SCREEN_HEIGHT // 2))
    elif game_state == MAIN_GAME:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
            current_delay += 1
            player_speed += 0.002  

        player_vel_y += gravity
        player_pos[1] += player_vel_y
        if player_pos[1] >= ground_level:
            player_pos[1] = ground_level
            player_vel_y = 0
            jumps = 0

        scroll_speed += 0.002
        player_pos[0] -= scroll_speed
        
        if player_pos[0] < -player_size[0] or player_pos[0] > SCREEN_WIDTH or player_pos[1] < -player_size[1] or player_pos[1] > SCREEN_HEIGHT:
            game_state = GAME_OVER

        for i in range(len(trees)):
            trees[i] = (trees[i][0] - scroll_speed, trees[i][1])
            if trees[i][0] < -60: 
                trees[i] = reset_tree_position(trees)

        for coin in coins:
            coin.update(scroll_speed)

        for bird in birds:
            if isinstance(bird, SmartBird):
                bird.update(player_pos, scroll_speed)
            else:
                bird.update(scroll_speed)
            if bird.x < -50:
                birds.remove(bird)
                new_bird = Bird(SCREEN_WIDTH + random.randint(0, 500), random.randint(100, 300))
                birds.append(new_bird)

        if bubble_active:
            bubble_timer -= 1
            if bubble_timer <= 0:
                bubble_active = False

        screen.fill(BACKGROUND_COLOR)

        pygame.draw.rect(screen, GRASS_COLOR, (0, ground_level + player_size[1] - 5, SCREEN_WIDTH, SCREEN_HEIGHT - (ground_level + player_size[1] - 5)))

        draw_cloud(150, 100)
        draw_cloud(300, 150)
        draw_cloud(450, 50)
        draw_cloud(600, 120)

        for tree in trees:
            draw_tree(tree[0], tree[1])

        for coin in coins:
            coin.draw()

        for bird in birds:
            bird.draw()

        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
        for tree in trees:
            tree_rect = pygame.Rect(tree[0], tree[1], 20, 40)  # Tree trunk size
            if check_collision(player_rect, tree_rect) and not bubble_active:
                game_state = GAME_OVER

        for bird in birds:
            bird_rect = pygame.Rect(bird.x - 30, bird.y - 20, 30, 20)
            if check_collision(player_rect, bird_rect) and not bubble_active:
                game_state = GAME_OVER

        for coin in coins[:]:
            coin_rect = pygame.Rect(coin.x - 15, coin.y - 15, 30, 30)
            if check_collision(player_rect, coin_rect):
                coins.remove(coin)
                coin_count += 1

        if current_delay >= animation_delay:
            frame_index = (frame_index + 1) % 2
            current_delay = 0

        screen.blit(player_frames[frame_index], player_pos)

        if bubble_active:
            pygame.draw.circle(screen, (0, 255, 255), (player_pos[0] + player_size[0] // 2, player_pos[1] + player_size[1] // 2), player_size[0])

        coin_text = small_font.render(f"Coins: {coin_count}", True, WHITE)
        screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))

    elif game_state == GAME_OVER:
        coins = []
        screen.fill(WHITE)
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 50))
        result_text = font.render(f"Score: {coin_count}", True, RED)
        screen.blit(result_text, ((SCREEN_WIDTH - result_text.get_width()) // 2, SCREEN_HEIGHT // 2))
        restart_text = font.render("Press Enter to Restart", True, RED)
        screen.blit(restart_text, ((SCREEN_WIDTH - restart_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 50))
        exit_text = font.render("Press ESC to Exit", True, RED)
        screen.blit(exit_text, ((SCREEN_WIDTH - exit_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 100))

    pygame.display.flip()
    clock.tick(30)
