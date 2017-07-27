import wave, struct, sys, pygame
from operator import itemgetter

# Init pygame stuff

pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)

black = 0, 0, 0
grey = 100, 100, 100
red = 255, 0, 0
white = 255, 255, 255
font = pygame.font.SysFont('Monospace', 16)

screen = pygame.display.set_mode((1280, 720))

cursor = 0
speed = 1
zoom = 2

# Sound stuff

sound = wave.open("beep.wav")

values = []

for i in range(sound.getnframes()):
    frame = sound.readframes(1)
    data = struct.unpack("<h", frame)
    values.append((i, int(data[0])))


norm_vals = []
largest = max(values, key=itemgetter(1))

for value in values:
    norm_vals.append((value[0], int((-value[1] / largest[1]) * 360) + 360))

# Functions

def draw_text(text, x, y):
    textsurface = font.render(text, False, grey)
    screen.blit(textsurface, (x, y))

# Main loop

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP:
                speed += 1
            if event.key == pygame.K_PAGEDOWN:
                speed -= 1
            if event.key == pygame.K_SPACE:
                speed = 0
            if event.key == pygame.K_RIGHT:
                cursor += 1
            if event.key == pygame.K_LEFT:
                cursor -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                zoom *= 1.5
            if event.button == 5:
                zoom /= 1.5

    screen.fill(black)
    mousepos = pygame.mouse.get_pos()

    pygame.draw.line(screen, grey, (mousepos[0], 0), (mousepos[0], 720))

    draw_text("Frame: " + str(cursor + mousepos[0] / zoom), mousepos[0] + 2, 0)
    draw_text("Value: " + str(values[cursor+mousepos[0]][1]), mousepos[0] + 2, 20)

    for i in range(cursor, int(1280 / zoom + cursor)):
        if i+1 >= len(norm_vals) or i < 0:
            continue

        x = (norm_vals[i][0] - cursor) * zoom
        y = norm_vals[i][1]
        next_x = (norm_vals[i+1][0] - cursor) * zoom
        next_y = norm_vals[i+1][1]
        pygame.draw.line(screen, white, (x, y), (next_x, next_y))
        screen.set_at((int(x), int(y)), red)

    if cursor + speed + 1280 + zoom < sound.getnframes():
        cursor += speed
    else:
        speed = 1

    pygame.display.flip()
