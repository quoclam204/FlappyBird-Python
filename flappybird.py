import pygame, sys, random

# Hàm tạo sàn di chuyển liên tục
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

# Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height) # VT ngẫu nhiên của ống 
    bottom_pipe = pipe_surface.get_rect(midtop = (500,  random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,  random_pipe_pos-700))
    return bottom_pipe, top_pipe

# Hàm di chuyển ống 
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Hàm hiển thị ống lên màn hình
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Hàm xử lý va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play( )
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

# Hàm hiệu ứng cho chim 
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movevent*3, 1)
    return new_bird

# Hàm tạo hiệu ứng đập cánh
def bird_aniation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

# Hàm hiển thị điểm
def score_display(game_state):
    # Trò chơi đang hoạt động
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    # Nếu trò choi kết thúc
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)

        hight_score_surface = game_font.render(f'Hight Score: {int(high_score)}', True, (255, 255, 255))
        hight_score_rect = hight_score_surface.get_rect(center = (216, 630))
        screen.blit(hight_score_surface, hight_score_rect)

# Hàm cập nhật điểm
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# Tạo các biến cho trò chơi
gravity = 0.25
bird_movevent = 0
game_active = True
score = 0
high_score = 0

# Chèn backGround
backGround = pygame.image.load('assets/background-night.png').convert()
backGround = pygame.transform.scale2x(backGround) # BackGround chiếm toán bộ khung hình

# Chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0 # Di chuyển

# Tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 2
bird = bird_list[bird_index]
#bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 384))

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] # Chứa tất cả ống vừa mới tạo ra

# Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400] # Tạo chiều cao ống ngẫu nhiên

# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdow = 100

# Tạo cửa sổ game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active: # Game hoạt động
                bird_movevent = 0
                bird_movevent = -11
                flap_sound.play(  )
            if event.key == pygame.K_SPACE and game_active == False: # Game kết thúc
                game_active = True # Chơi lại
                pipe_list.clear() # Reset lại
                bird_rect. center = (100, 384)
                bird_movevent = 0
                score = 0
        # Sự kiện tạo ống
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

        # Sự kiện chim đập cánh
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_aniation()

    screen.blit(backGround, (0, 0))
    if game_active:
        # Chim
        bird_movevent += gravity
        rotated_bird = rotate_bird(bird) # Hiệu ứng chim
        bird_rect.centery += bird_movevent
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01 # Cộng điểm
        score_display('main game')
        score_sound_countdow -= 1
        if score_sound_countdow <= 0:
            score_sound.play()
            score_sound_countdow = 100
    
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Sàn
    floor_x_pos -= 1 # Di chuyển 
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120) # FPS
