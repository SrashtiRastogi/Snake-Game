import pygame
import time
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Load sounds
pygame.mixer.music.load("snake bg music2.mp3")  # Replace with your file name
pygame.mixer.music.play(-1)  # -1 makes it loop infinitely
pygame.mixer.music.set_volume(0.6)  # Set volume (0.0 to 1.0)

eat_sound = pygame.mixer.Sound("pow-90398.mp3")
game_over_sound = pygame.mixer.Sound("game over.mp3")

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
brown = (101, 67, 33)
red = (213, 50, 80)

# Set display dimensions
dis_width = 800
dis_height = 600
        
# Create display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Load background image
background = pygame.image.load('snake game bg.jpg')
background = pygame.transform.scale(background, (dis_width, dis_height))

# Set clock and snake speed
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 8

# Define fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_score(score):
    value = score_font.render(f"Score: {score}", True, yellow)
    dis.blit(value, [10, 10])

snake_texture = pygame.image.load("snake texture.png")
snake_texture = pygame.transform.scale(snake_texture, (snake_block, snake_block))

def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Head of the snake
            pygame.draw.circle(dis, (80, 50, 20), (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 2 + 2)
            pygame.draw.circle(dis, (255, 255, 255), (x[0] + 3, x[1] + 3), 2)  # Left eye
            pygame.draw.circle(dis, (255, 255, 255), (x[0] + snake_block - 3, x[1] + 3), 2)  # Right eye
        else:
            pygame.draw.circle(dis, (101, 67, 33), (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 2)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False
    paused = False
    
    x1 = dis_width / 2
    y1 = dis_height / 2
    
    x1_change = 0
    y1_change = 0
    
    snake_List = []
    Length_of_snake = 1
    
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    
    score = 0  # Initialize score

    while not game_over:
        while game_close:
            dis.blit(background, (0, 0))
            message("You Lost! Press Q-Quit or C-Play Again", white)
            game_over_sound.play()  # Play game over sound
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused  # Toggle pause state
                if not paused:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0
        
        if paused:
            continue

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.blit(background, (0, 0))
        
        food_radius = 5
        pygame.draw.circle(dis, red, (foodx + food_radius, foody + food_radius), food_radius)
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        
        our_snake(snake_block, snake_List)
        show_score(score)  # Display score on screen
        pygame.display.update()
        
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 10  # Increase score when food is eaten
            eat_sound.play()
        
        clock.tick(snake_speed)
    
    pygame.quit()
    quit()

gameLoop()
