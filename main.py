import pygame
import random

WIDTH, HEIGHT = 400, 600
ROWS, COLS = 6, 5
TILE_SIZE = WIDTH // COLS
FONT_SIZE = TILE_SIZE // 2
PADDING = TILE_SIZE // 5
MARGIN_TOP = 50

BG_COLOR = (18, 18, 19)
LETTER_COLOR = (255, 255, 255)
TILE_COLOR = (58, 58, 60)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY = (58, 58, 60)

# Fonts
pygame.font.init()
FONT = pygame.font.Font(None, FONT_SIZE)

WORDS = ["SHAKE", "SHARE", "PANIC", "AMUSE", "SHADE"]

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.guesses = []

    def add_guess(self, guess):
        self.guesses.append(guess)

    def draw(self, screen, correct_word):
        for row in range(self.rows):
            for col in range(self.cols):
                tile_rect = pygame.Rect(col * TILE_SIZE + PADDING, row * TILE_SIZE + MARGIN_TOP, TILE_SIZE - 2 * PADDING, TILE_SIZE - 2 * PADDING)
                pygame.draw.rect(screen, TILE_COLOR, tile_rect, border_radius=5)

                if row < len(self.guesses):
                    letter = self.guesses[row][col]
                    color = self.get_tile_color(letter, col, correct_word)
                    pygame.draw.rect(screen, color, tile_rect, border_radius=5)

                    text_surface = FONT.render(letter, True, LETTER_COLOR)
                    screen.blit(text_surface, (tile_rect.x + TILE_SIZE // 3, tile_rect.y + TILE_SIZE // 4))

    def get_tile_color(self, letter, index, correct_word):
        if letter == correct_word[index]:
            return GREEN
        elif letter in correct_word:
            return YELLOW
        return GRAY

class InputHandler:
    def __init__(self):
        self.current_guess = ""

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key).isalpha() and len(self.current_guess) < COLS:
                self.current_guess += pygame.key.name(event.key).upper()
            elif event.key == pygame.K_BACKSPACE:
                self.current_guess = self.current_guess[:-1]
            elif event.key == pygame.K_RETURN and len(self.current_guess) == COLS:
                return self.current_guess
        return None

    def reset_guess(self):
        self.current_guess = ""

class WordChecker:
    def __init__(self, correct_word):
        self.correct_word = correct_word

    def is_correct_guess(self, guess):
        return guess == self.correct_word

class WordleGame:
    def __init__(self, screen):
        self.screen = screen
        self.grid = Grid(ROWS, COLS)
        self.input_handler = InputHandler()
        self.correct_word = random.choice(WORDS)
        self.word_checker = WordChecker(self.correct_word)
        self.attempts = 0
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill(BG_COLOR)
            self.handle_events()
            self.update_screen()
            pygame.display.flip()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            guess = self.input_handler.handle_input(event)
            if guess:
                self.process_guess(guess)

    def process_guess(self, guess):
        self.grid.add_guess(guess)
        self.attempts += 1

        if self.word_checker.is_correct_guess(guess):
            print("You win!")
            self.running = False
        elif self.attempts >= ROWS:
            print(f"You lose! The correct word was {self.correct_word}.")
            self.running = False

        self.input_handler.reset_guess()

    def update_screen(self):
        self.grid.draw(self.screen, self.correct_word)

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wordle")
    game = WordleGame(screen)
    game.run()
