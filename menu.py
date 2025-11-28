from pygame import *
import sys

from settings import Settings, settings_loop

# Кольори
PURPLE = (142, 36, 108)
ORANGE = (225, 108, 68)
BLUE = (85, 118, 201)
WHITE = (255, 255, 255)

BUTTONS = ["ПОЧАТИ", "НАЛАШТУВАННЯ", "ВИХІД"]


class Button:
    def __init__(self, text, font, width, height, pos, round_top=False, round_bottom=False):
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.pos = pos
        self.round_top = round_top
        self.round_bottom = round_bottom
        self.rect = Rect(pos[0], pos[1], width, height)

    def draw(self, screen, selected=False):
        if self.text == "ПОЧАТИ":
            color = ORANGE if selected else PURPLE
        elif self.text == "НАЛАШТУВАННЯ":
            color = ORANGE if selected else BLUE
        else:
            color = ORANGE if selected else BLUE

        border_radius = 20
        top_left = border_radius if self.round_top else 0
        top_right = border_radius if self.round_top else 0
        bottom_left = border_radius if self.round_bottom else 0
        bottom_right = border_radius if self.round_bottom else 0

        draw.rect(screen, color, self.rect,
                  border_top_left_radius=top_left,
                  border_top_right_radius=top_right,
                  border_bottom_left_radius=bottom_left,
                  border_bottom_right_radius=bottom_right)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


def menu_loop(screen_width, screen_height, screen, settings):
    # init() # Не потрібно викликати init повторно
    display.set_caption("Меню")
    clock = time.Clock()
    mixer.init()
    play_menu_music(settings)
    try:
        MENU_CHOICE_SOUND = mixer.Sound('sounds/Menu Choice.mp3')
    except:
        class Dummy:
            def play(self): pass

        MENU_CHOICE_SOUND = Dummy()

    font_obj = font.Font(None, 40)
    button_width = 400
    button_height = 70
    gap = 10
    total_height = len(BUTTONS) * button_height + (len(BUTTONS) - 1) * gap
    start_y = (screen_height - total_height) // 2

    buttons = []
    for i, text in enumerate(BUTTONS):
        x = (screen_width - button_width) // 2
        y = start_y + i * (button_height + gap)
        round_top = i == 0
        round_bottom = i == len(BUTTONS) - 1
        buttons.append(Button(text, font_obj, button_width, button_height, (x, y), round_top, round_bottom))

    selected_index = 0

    while True:
        screen.fill((30, 30, 30))

        mx, my = mouse.get_pos()  # Отримуємо координати миші

        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()

            # --- ОБРОБКА МИШІ ---
            if e.type == MOUSEMOTION:
                for i, button in enumerate(buttons):
                    if button.rect.collidepoint(mx, my):
                        if selected_index != i:
                            MENU_CHOICE_SOUND.play()
                        selected_index = i

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:  # Ліва кнопка миші
                    if buttons[selected_index].rect.collidepoint(mx, my):
                        # Емуляція натискання Enter
                        if buttons[selected_index].text == 'ПОЧАТИ':
                            mixer.music.stop()
                            return
                        if buttons[selected_index].text == "ВИХІД":
                            quit()
                            sys.exit()
                        if buttons[selected_index].text == 'НАЛАШТУВАННЯ':
                            # Передаємо розміри екрану явно
                            play_menu_music(settings)
                            settings_loop(screen, screen_width, screen_height, settings)

            # --- ОБРОБКА КЛАВІАТУРИ ---
            if e.type == KEYDOWN:
                if e.key == K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                    MENU_CHOICE_SOUND.play()
                elif e.key == K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                    MENU_CHOICE_SOUND.play()
                elif e.key == K_RETURN:
                    if buttons[selected_index].text == 'ПОЧАТИ':
                        mixer.music.stop()
                        return
                    if buttons[selected_index].text == "ВИХІД":
                        quit()
                        sys.exit()
                    if buttons[selected_index].text == 'НАЛАШТУВАННЯ':
                        play_menu_music(settings)
                        settings_loop(screen, screen_width, screen_height, settings)

        for i, button in enumerate(buttons):
            button.draw(screen, selected=(i == selected_index))

        display.flip()
        clock.tick(60)


def play_menu_music(settings):
    if settings.music_enabled:
        try:
            mixer.music.set_volume(settings.volume)
            mixer.music.load('sounds/menu.mp3')
            mixer.music.play(-1)
        except:
            pass


def stop_music():
    mixer.music.stop()


def start_menu(WIDTH, HEIGHT, screen, default_host="localhost"):
    settings = Settings(host=default_host)
    menu_loop(WIDTH, HEIGHT, screen, settings)
    return settings