import pygame
import sys
import random

# Konstanta permainan
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
PIPE_GAP = 150  # Jarak antara pipa atas dan bawah
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
GRAVITY = 0.5
JUMP_HEIGHT = 10

# Warna
GREEN = (0, 255, 0)  # Warna pipa
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Fungsi untuk memuat gambar
def load_image(path, size=None):
    try:
        image = pygame.image.load(path)
        if size:
            return pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Unable to load image {path}: {e}")
        sys.exit()

# Memuat gambar
bird_image = load_image(r"C:\Users\Acer\Downloads\bird.png", (BIRD_WIDTH, BIRD_HEIGHT))
background_image = load_image(r"C:\Users\Acer\Downloads\background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fungsi untuk mendapatkan posisi pipa
def get_pipe_position():
    min_height = 100  # Tinggi minimum pipa atas
    max_height = SCREEN_HEIGHT - PIPE_GAP - 50  # Tinggi maksimum pipa atas
    return random.randint(min_height, max_height)

# Fungsi untuk menggambar pipa kotak
def draw_pipe(surface, x, y, is_top):
    if is_top:
        pygame.draw.rect(surface, GREEN, (x, 0, PIPE_WIDTH, y))
    else:
        pygame.draw.rect(surface, GREEN, (x, y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - y - PIPE_GAP))

# Fungsi untuk mereset permainan
def reset_game():
    global bird_x, bird_y, bird_vy, pipe_x, pipe_y, score, game_over
    bird_x = SCREEN_WIDTH / 4  # Inisialisasi posisi burung
    bird_y = SCREEN_HEIGHT / 2
    bird_vy = 0
    pipe_x = SCREEN_WIDTH
    pipe_y = get_pipe_position()
    score = 0
    game_over = False

# Variabel permainan
reset_game()  # Reset permainan saat pertama kali dijalankan

# Loop permainan
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()  # Reset permainan saat game over
                else:
                    bird_vy = -JUMP_HEIGHT

    if not game_over:
        # Update posisi burung
        bird_vy += GRAVITY
        bird_y += bird_vy

        # Gerakkan pipa
        pipe_x -= 5
        if pipe_x < -PIPE_WIDTH:
            pipe_x = SCREEN_WIDTH
            pipe_y = get_pipe_position()  # Dapatkan posisi pipa baru
            score += 1  # Tambah skor saat melewati pipa

        # Periksa tabrakan
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        top_pipe_rect = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_y)  # Pipa atas
        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_y - PIPE_GAP)  # Pipa bawah

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            game_over = True

        # Periksa jika burung menyentuh tanah atau langit
        if bird_y > SCREEN_HEIGHT or bird_y < 0:
            game_over = True

    # Gambar semuanya
    screen.blit(background_image, (0, 0))  # Gambar latar belakang
    screen.blit(bird_image, (bird_x, bird_y))  # Gambar burung
    draw_pipe(screen, pipe_x, pipe_y, is_top=True)  # Gambar pipa atas
    draw_pipe(screen, pipe_x, pipe_y, is_top=False)  # Gambar pipa bawah
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 20))  # Bar skor
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    if game_over:
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        restart_text = font.render("Press SPACE to Restart", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(30)  # Atur frame rate