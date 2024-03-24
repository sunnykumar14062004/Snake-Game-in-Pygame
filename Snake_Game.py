import pygame
import random

pygame.init()
clock = pygame.time.Clock()
screen_width = 600
screen_height = 390
screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.image.load("Background.png")
game_over_image = pygame.image.load("Game Over.png")
icon = pygame.image.load("Logo.png")

pygame.mixer.music.load("Game Music.mp3")
pygame.mixer.music.play(-1)
pygame.display.set_caption("Snake Game")
pygame.display.set_icon(icon)

font_score_play = pygame.font.SysFont("Bell MT", 30)
font_score_over = pygame.font.SysFont("Arial Rounded MT Bold", 70)
font_title = pygame.font.SysFont("Times New Roman", 50)
font_credit = pygame.font.SysFont("Times New Roman", 30)
font_button = pygame.font.SysFont("Comic Sans MS", 40)

def dead(snake_x, snake_y):
    if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
        return True
    if (snake_x, snake_y) in snake_list[:-1]:
        return True
    return False

def check_food(food_x, food_y):
    for x, y in snake_list:
        if food_x == x and food_y == y:
            return False
    return True

def food_coordinate():
    while True:
        food_x = random.randint(15, 570)
        food_y = random.randint(50, 370)
        food_x -= food_x % 15
        food_y -= food_y % 15
        if check_food(food_x, food_y):
            return [food_x, food_y]

def update():
    global movement_count, score_change
    update_point = [5, 15, 30, 50, 75, 105]
    for i in update_point:
        if score_value == i:
            movement_count -= 1
            score_change += 1

white = (255, 255, 255)
blue = (106, 90, 205)
brown = (165, 42, 42)
yellow = (255, 255, 0)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

snake_x = 240
snake_y = 180
snake_size = 15
snake_length = 1
snake_list = [(snake_x, snake_y)]
snake_x_change = 0
snake_y_change = 0

random_coordinate = food_coordinate()
food_x = random_coordinate[0]
food_y = random_coordinate[1]

running = True
state = ""
count = -1
score_value = 0
score_change = 1
movement_count = 8

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            if state == "":
                if 260 < mouse[0] < 335 and 325 < mouse[1] < 365:
                    state = "play"

            if state == "over":

                if 250 < mouse[0] < 335 and 335 < mouse[1] < 370:
                    running = False
                    
                if 225 < mouse[0] < 370 and 260 < mouse[1] < 295:
                    state = "play"
                    snake_x = 240
                    snake_y = 180
                    snake_list = [(snake_x, snake_y)]
                    score_value = 0
                    snake_x_change = 0
                    snake_y_change = 0
                    score_change = 1
                    movement_count = 8
                    count = -1

        if event.type == pygame.KEYDOWN:

            if state == "play":

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if snake_x_change != snake_size:
                        snake_x_change = -snake_size
                        snake_y_change = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if snake_x_change != -snake_size:
                        snake_x_change = snake_size
                        snake_y_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if snake_y_change != snake_size:
                        snake_x_change = 0
                        snake_y_change = -snake_size
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if snake_y_change != -snake_size:
                        snake_x_change = 0
                        snake_y_change = snake_size

    if state == "play":
        count = (count + 1) % movement_count
        screen.blit(background_image, (0, 0))
        
        food_rect = pygame.Rect(food_x, food_y, snake_size, snake_size)
        pygame.draw.rect(screen, yellow, food_rect)
        score = font_score_play.render("Score : " + str(score_value), True, blue)
        screen.blit(score, (10, 10))

        for x, y in snake_list:
            snake_rect = pygame.Rect(x, y, snake_size, snake_size)
            pygame.draw.rect(screen, brown, snake_rect)

        if dead(snake_x, snake_y):
            state = "over"
            game_over_sound = pygame.mixer.Sound("Game Over.mp3")
            game_over_sound.play()
            screen.blit(game_over_image, (0, 0))
            snake_length = 1
            
        if count == movement_count - 1:
            snake_x += snake_x_change
            snake_y += snake_y_change

            snake_list.append((snake_x, snake_y))
            if snake_length < len(snake_list):
                snake_list.remove(snake_list[0])
    
            if snake_rect.colliderect(food_rect):
                game_over_sound = pygame.mixer.Sound("Food.mp3")
                game_over_sound.play()
                score_value += score_change
                snake_length += 1
                random_coordinate = food_coordinate()
                food_x = random_coordinate[0]
                food_y = random_coordinate[1]
                update()

    if state == "":
        
        game_title = font_title.render("Snake  Game", True, blue)
        name = font_credit.render("Made By : Sunny Kumar", True, yellow)
        branch = font_credit.render("BE  CSE", True, yellow)
        year = font_credit.render("2021 - 2025", True, yellow)

        mouse = pygame.mouse.get_pos()
        if 260 < mouse[0] < 335 and 325 < mouse[1] < 365:
            play = font_button.render("Play", True, green)
        else:
            play = font_button.render("Play", True, white)

        screen.blit(game_title, (160, 20))
        screen.blit(name, (140, 150))
        screen.blit(branch, (278, 200))
        screen.blit(year, (278, 250))
        screen.blit(play, (260, 315))

    elif state == "over":

        mouse = pygame.mouse.get_pos()
        if 225 < mouse[0] < 370 and 260 < mouse[1] < 295:
            restart = font_button.render("Restart", True, green)
        else:
            restart = font_button.render("Restart", True, blue)
        if 250 < mouse[0] < 335 and 335 < mouse[1] < 370:
            quit = font_button.render("Quit", True, green)
        else:
            quit = font_button.render("Quit", True, blue)
        
        score = font_score_over.render("Score : " + str(score_value), True, black)
        screen.blit(score, (190, 170))
        screen.blit(restart, (225, 250))
        screen.blit(quit, (250, 320))

    clock.tick(60)
    pygame.display.update()