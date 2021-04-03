import pygame, sys, random

WIDTH = 576
HEIGHT = 1024
FLOOR_Y = 900
PIPE_SPEED = 4

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, FLOOR_Y))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, FLOOR_Y))

def create_pipe():
    pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes[-4:]:
        pipe.centerx -= PIPE_SPEED

def draw_pipes(pipes):
    for pipe_rect in pipes[-4:]:
        if pipe_rect.top <= 0:  # top pipe
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe_rect)
        else:
            screen.blit(pipe_surface, pipe_rect)

def is_collision(pipes):
    for pipe_rect in pipes[-4:]:
        if bird_rect.colliderect(pipe_rect):
            death_sound.play()
            return True

    if bird_rect.top <= -100 or bird_rect.bottom >= FLOOR_Y:
        return True
    return False

def rotate_bird_surface(bird):
    new_bird = pygame.transform.rotozoom(bird, -3 * bird_movement, 1)
    return new_bird

def bird_animation(index):
    new_bird_surface = bird_frames[index]
    new_bird_rect = new_bird_surface.get_rect(center=(100, bird_rect.centery))
    return new_bird_surface, new_bird_rect

def score_display():
    score_surface = game_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(288, 100))
    screen.blit(score_surface, score_rect)
    if game_over:
        high_score_surface = game_font.render(f"High score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

pygame.init()
screen = pygame.display.set_mode((WIDTH, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 40)

# Game Variables
GRAVITY = 0.25
bird_movement = 0
game_over = False
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, HEIGHT // 2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
pipe_rect_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(WIDTH//2, HEIGHT//2))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

old_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                if game_over:
                    game_over = False
                    pipe_rect_list.clear()
                    score = 0
                    bird_rect.center = (100, HEIGHT // 2)
                else:
                    flap_sound.play()
                    bird_movement -= 8

        if event.type == SPAWNPIPE:
            pipe_rect_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % len(bird_frames)
            bird_surface, bird_rect = bird_animation(bird_index)
    screen.blit(bg_surface, (0, 0))

    if not game_over:
        # Bird
        bird_movement += GRAVITY
        bird_rect.centery += bird_movement
        rotated_bird_surface = rotate_bird_surface(bird_surface)
        screen.blit(rotated_bird_surface, bird_rect)

        # Pipes
        move_pipes(pipe_rect_list)
        draw_pipes(pipe_rect_list)
        game_over = is_collision(pipe_rect_list)

        # Score
        score = len(pipe_rect_list) // 2
        if score != old_score:
            score_sound.play()
            old_score = score
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = max(high_score, score)
    score_display()

    floor_x_pos -= 1
    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0
    draw_floor()

    pygame.display.update()
    clock.tick(120)
