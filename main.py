import random
import pygame
import math
from playsound import playsound

pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
Word_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
HINT_FONT = pygame.font.SysFont('Ariel', 25)

# load images
images = []
for i in range(7):
    img = pygame.image.load("hangman" + str(i) + ".png")
    images.append(img)

# window colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)


def draw():
    win.fill(WHITE)
    # draw title
    hint_title = LETTER_FONT.render("Hint : ", True, BLUE)
    win.blit(hint_title, ((WIDTH - hint_title.get_width()) / 2, 20))
    title = HINT_FONT.render(hint, True, GREEN)
    win.blit(title, ((WIDTH - title.get_width()) / 2, 50))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = Word_FONT.render(display_word, True, BLACK)
    win.blit(text, (300 + (WIDTH - 300 - text.get_width()) / 2, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # draw attempts left
    text = LETTER_FONT.render("Attempts Left : " + str(6 - hangman_status), True, RED)
    win.blit(text, ((WIDTH - text.get_width()) / 2 + 100, 300))

    win.blit(images[hangman_status], (100, 100))
    pygame.display.update()
    if hangman_status == 6:
        pygame.time.delay(1500)


def display_message(message):
    pygame.time.delay(200)
    win.fill(WHITE)
    text = Word_FONT.render(message, True, BLACK)
    win.blit(text, ((WIDTH - text.get_width()) / 2, (HEIGHT - text.get_height()) / 2))
    pygame.display.update()
    pygame.time.delay(100)


def play_again(i, won, lost):
    win.fill(WHITE)
    if i != 0:
        # show score
        score = TITLE_FONT.render("SCORE", True, BLUE)
        win.blit(score, ((WIDTH - score.get_width()) / 2, 60))
        w_count = TITLE_FONT.render("Won : " + str(won), True, GREEN)
        win.blit(w_count, (200, 150))
        l_count = TITLE_FONT.render("Lost : " + str(lost), True, RED)
        win.blit(l_count, (400, 150))
        # asking to play again
        title = TITLE_FONT.render("Wanna Play again?", True, BLACK)
        win.blit(title, ((WIDTH - title.get_width()) / 2, 300))
        pygame.draw.circle(win, GREEN, (274, 412), RADIUS + 15, 5)
        yes = LETTER_FONT.render("YES", True, BLACK)
        win.blit(yes, (248, 400))
        pygame.draw.circle(win, RED, (517, 412), RADIUS + 15, 5)
        no = LETTER_FONT.render("NO", True, BLACK)
        win.blit(no, (500, 400))
        pygame.display.update()
        pygame.time.delay(200)

        run = True
        while run:
            # clock.tick(FPS)

            pygame.time.delay(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    playsound('click.mp3')
                    m_x, m_y = pygame.mouse.get_pos()
                    dis_y = math.sqrt((274 - m_x) ** 2 + (412 - m_y) ** 2)
                    if dis_y < RADIUS + 15:
                        display_message("Good Luck!")
                        playsound('resume.mp3')
                        pygame.time.delay(200)
                        return True
                    dis_n = math.sqrt((517 - m_x) ** 2 + (412 - m_y) ** 2)
                    if dis_n < RADIUS + 15:
                        display_message("See You Again...")
                        playsound('end.mp3')
                        pygame.time.delay(200)
                        return False
    else:
        display_message("Loading Hangman Game...")
        playsound('loading.mp3')
        pygame.time.delay(500)
        return True


def main():
    global hangman_status, won, lost

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        pygame.time.delay(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                playsound("wrong.mp3")
                                hangman_status += 1
                            else:
                                playsound("correct.mp3")

        draw()
        if hangman_status == 6:
            display_message("YOU ARE HANGED!")
            playsound("lost.mp3")
            pygame.time.delay(2000)
            lost += 1
            break

        win = True
        for letter in word:
            if letter not in guessed:
                win = False
                break

        if win:
            display_message("YOU WON!")
            playsound("won.mp3")
            pygame.time.delay(2000)
            won += 1
            break


i = 0
won, lost = 0, 0
while True:
    signal = play_again(i, won, lost)
    if signal == True:
        # button variables
        RADIUS = 20
        GAP = 15
        letters = []
        startx = round((WIDTH - (RADIUS * 2 + GAP) * (13)) / 2)
        starty = 400
        A = 65
        for i in range(26):
            x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
            y = starty + ((i // 13) * (GAP + RADIUS * 2))
            letters.append([x, y, chr(A + i), True])

        # game variables
        hangman_status = 0
        words = open('words.txt').read().split()
        hints = open('hints.txt').read().split(';')
        w = random.choice(words)
        word = str(w).upper()
        hint = hints[words.index(w)]
        guessed = []

        main()
        i += 1
    else:
        pygame.quit()
# -----END OF THE CODE -----
