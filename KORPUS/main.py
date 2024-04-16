import pygame
import random
import pygame.mixer

# Цвета
TR = (0, 0, 0, 0)
GOLD = (204, 174, 111)
RIGII = (145, 85, 50)
icon = pygame.image.load("resources/background.icns")
pygame.display.set_icon(icon)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("resources/music.mp3")
pygame.mixer.music.play(-1)

# Создание окна
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("KORPUS")

# Определение шрифта и его размера
font = pygame.font.Font('resources/Font.ttf', 36)
# Количество игроков
count_players = 2
running = True
runningMenu = True
runningGame_qc = False
runningGame_qa = False
runningManual = False
runningGame_right_q = False
running_end_game = False

# Загрузка изображения фона
background_image = pygame.image.load("resources/background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

background_image_game = pygame.image.load("resources/background_game.png")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))

overlay_image = pygame.Surface((screen_width, screen_height))
overlay_alpha = 150  # Уровень прозрачности затемнения (от 0 до 255)
overlay_image.fill((0, 0, 0))
overlay_image.set_alpha(overlay_alpha)

rules_text = [
    "KORPUS – игра, в которой ты можешь проверить свои знания в области обучения,",
    "университета, общих знаний и с пользой отдохнуть. Удачи!",
    "Как начать играть:",
    "Выбирай количество игроков и заходи в игру",
    "Как играть:",
    "По очереди отвечай и зарабатывай баллы",
    "Выигрывай и гордись собой",
    "Цель игры:",
    "Доказать, что ты самый умный среди игроков"
]

class Question:
    def __init__(self, qt, qa1, qa2, qa3, qar):
        self.question_text = qt
        self.question_answer_1 = qa1
        self.question_answer_2 = qa2
        self.question_answer_3 = qa3
        self.question_answer_right = qar

#######################################

# Список общих вопросов
questions_general = []

questions_general_1 = Question("В какой степени родства находятся Посейдон, Зевс, Аид?", "Внуки", "Дяды", "Братья", 3)
questions_general.append(questions_general_1)
questions_general_2 = Question("Вопрос 2", "2 1", "2 2", "2 3", 2)
questions_general.append(questions_general_2)
questions_general_3 = Question("Вопрос 3", "3 1", "3 2", "3 3", 3)
questions_general.append(questions_general_3)

#######################################
#######################################

# Список вопросов хакерство
questions_hack = []

questions_hack_1 = Question("Вопрос 1", "1 1", "1 2", "1 3", 1)
questions_hack.append(questions_hack_1)
questions_hack_2 = Question("Вопрос 2", "2 1", "2 2", "2 3", 2)
questions_hack.append(questions_hack_2)
questions_hack_3 = Question("Вопрос 3", "3 1", "3 2", "3 3", 3)
questions_hack.append(questions_hack_3)

#######################################


# Определите размер и начальные координаты для отображения текста правил
rules_font_size = 24
rules_x = 100
rules_y = 100
rules_line_spacing = 10
rules_font = pygame.font.Font('resources/Font.ttf', rules_font_size)

def create_button(screen, rect, text_surface):
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

class Player():
    def __init__(self, pn, pb, pname):
        self.player_number = pn
        self.player_balance = pb
        self.player_name = pname

players = []
player_1 = Player(1, 0, "Пекус 1")
players.append(player_1)
player_2 = Player(2, 0, "Пекус 2")
players.append(player_2)
player_3 = Player(3, 0, "Пекус 3")
players.append(player_3)
player_4 = Player(4, 0, "Пекус 4")
players.append(player_4)

# Очерь по выбору вопроса и ответу
resp_player = 0
# Тема вопроса (0 - нет выбора, 1 - общ, 2 - спец)
question_id = None
question_text = None
question_answer_1 = None
question_answer_2 = None
question_answer_3 = None
questions_type = None #(1 - general/ 2 - hack)
player_answer = None
question_answer_right_txt = None
id_win_player = None

def players_balance():
    if count_players == 2:
        player_1_rect = pygame.Rect(50, 658, 220, 60)
        player_2_rect = pygame.Rect(1010, 658, 220, 60)

        # Игрок 1
        create_button(screen, player_1_rect, font.render(f"{players[0].player_name} : {players[0].player_balance}", True, GOLD))

        # Игрок 2
        create_button(screen, player_2_rect, font.render(f"{players[1].player_name} : {players[1].player_balance}", True, GOLD))

    if count_players == 3:
        player_1_rect = pygame.Rect(50, 658, 220, 60)
        player_2_rect = pygame.Rect(530, 658, 220, 60)
        player_3_rect = pygame.Rect(1010, 658, 220, 60)

        # Игрок 1
        create_button(screen, player_1_rect, font.render(f"{players[0].player_name} : {players[0].player_balance}", True, GOLD))

        # Игрок 2
        create_button(screen, player_2_rect, font.render(f"{players[1].player_name} : {players[1].player_balance}", True, GOLD))

        # Игрок 3
        create_button(screen, player_3_rect, font.render(f"{players[2].player_name} : {players[2].player_balance}", True, GOLD))

    if count_players == 4:
        player_1_rect = pygame.Rect(50, 658, 220, 60)
        player_2_rect = pygame.Rect(370, 658, 220, 60)
        player_3_rect = pygame.Rect(690, 658, 220, 60)
        player_4_rect = pygame.Rect(1010, 658, 220, 60)

        # Игрок 1
        create_button(screen, player_1_rect, font.render(f"{players[0].player_name} : {players[0].player_balance}", True, GOLD))

        # Игрок 2
        create_button(screen, player_2_rect, font.render(f"{players[1].player_name} : {players[1].player_balance}", True, GOLD))

        # Игрок 3
        create_button(screen, player_3_rect, font.render(f"{players[2].player_name} : {players[2].player_balance}", True, GOLD))

        # Игрок 4
        create_button(screen, player_4_rect, font.render(f"{players[3].player_name} : {players[3].player_balance}", True, GOLD))

while running:

    if runningMenu:
        screen.fill(GOLD)
        screen.blit(background_image, (0, 0))

        # Кнопка Старт
        button_start_rect = pygame.Rect(700, 23, 192, 64)
        create_button(screen, button_start_rect, font.render("Старт", True, GOLD))

        # Кнопка Количество игроков
        button_cp_rect = pygame.Rect(714, 70, 192, 64)
        cp_text = f"Игроки: {count_players}"
        create_button(screen, button_cp_rect, font.render(cp_text, True, GOLD))

        # Кнопка Правила
        button_manual_rect = pygame.Rect(920, 23, 192, 64)
        create_button(screen, button_manual_rect, font.render("Правила", True, GOLD))

        # Кнопка Выход
        button_exit_rect = pygame.Rect(920, 74, 192, 64)
        create_button(screen, button_exit_rect, font.render("Выход", True, GOLD))

    elif runningGame_qc:
        screen.fill(GOLD)
        screen.blit(background_image_game, (0, 0))

        questions_q_rect = pygame.Rect(200, 220, 800, 60)
        create_button(screen, questions_q_rect, font.render(f"{players[resp_player].player_name} выбирает тему", True, GOLD))

        button_block_general_questions_txt = None
        if len(questions_general) > 0:
            button_block_general_questions_txt = "Знания пекуса"
        else:
            button_block_general_questions_txt = "-- Знания пекуса --"

        # Блок общих вопросов
        button_block_general_questions_rect = pygame.Rect(200, 320, 800, 30)
        create_button(screen, button_block_general_questions_rect, font.render(button_block_general_questions_txt, True, GOLD))

        button_block_focused_questions_txt = None
        if len(questions_hack) > 0:
            button_block_focused_questions_txt = "Хакерство"
        else:

            button_block_focused_questions_txt = "-- Хакерство --"

        # Блок узконаправленных знаний
        button_block_focused_questions_rect = pygame.Rect(200, 370, 800, 30)
        create_button(screen, button_block_focused_questions_rect, font.render(button_block_focused_questions_txt, True, GOLD))

        # Кнопки выхода в меню
        button_exit_game_rect = pygame.Rect(920, 23, 192, 64)
        create_button(screen, button_exit_game_rect, font.render("В меню", True, GOLD))

        players_balance()

    elif runningGame_qa:
        screen.fill(GOLD)
        screen.blit(background_image_game, (0, 0))

        players_balance()

        # Кнопки выхода в меню
        button_exit_game_rect = pygame.Rect(920, 23, 192, 64)
        create_button(screen, button_exit_game_rect, font.render("В меню", True, GOLD))

        # Вывод случайного вопроса
        questions_qa_rect = pygame.Rect(200, 220, 800, 60)
        create_button(screen, questions_qa_rect, font.render(question_text, True, GOLD))

        # Вывод вариантов ответов
        question_answer_1_rect = pygame.Rect(200, 300, 800, 30)
        create_button(screen, question_answer_1_rect, font.render(question_answer_1, True, GOLD))
        question_answer_2_rect = pygame.Rect(200, 380, 800, 30)
        create_button(screen, question_answer_2_rect, font.render(question_answer_2, True, GOLD))
        question_answer_3_rect = pygame.Rect(200, 460, 800, 30)
        create_button(screen, question_answer_3_rect, font.render(question_answer_3, True, GOLD))

    elif runningManual:
        screen.fill(GOLD)
        screen.blit(background_image, (0, 0))
        screen.blit(overlay_image, (0, 0))

        for i, rule in enumerate(rules_text):
            rule_surface = rules_font.render(rule, True, GOLD)
            rule_rect = rule_surface.get_rect()
            rule_rect.topleft = (rules_x, rules_y + (rules_font_size + rules_line_spacing) * i)
            screen.blit(rule_surface, rule_rect)

        # Кнопка выхода в меню
        button_exit_manual_rect = pygame.Rect(920, 23, 192, 64)
        create_button(screen, button_exit_manual_rect, font.render("В меню", True, GOLD))

    elif runningGame_right_q:
        screen.fill(GOLD)
        screen.blit(background_image_game, (0, 0))

        players_balance()

        # Кнопки выхода в меню
        button_exit_game_rect = pygame.Rect(920, 23, 192, 64)
        create_button(screen, button_exit_game_rect, font.render("В меню", True, GOLD))

        right_or_not = None #(1 - right/ 2 - not)
        if questions_type == 1:
            if player_answer == question_answer_right:
                right_or_not = 1
            else:
                right_or_not = 2
        if questions_type == 2:
            if player_answer == question_answer_right:
                right_or_not = 1
            else:
                right_or_not = 2

        right_or_not_txt = None
        if right_or_not == 1:
            right_or_not_txt = "Верно"
        if right_or_not == 2:
            right_or_not_txt = "Не верно"

        # Текст с результатом (правильно/не правильно)
        right_question_rect = pygame.Rect(200, 220, 800, 60)
        create_button(screen, right_question_rect, font.render(right_or_not_txt, True, GOLD))

        # Текст с правильным ответом
        question_answer_right_txt_rect = pygame.Rect(200, 220, 800, 260)
        create_button(screen, question_answer_right_txt_rect, font.render(question_answer_right_txt, True, GOLD))

        # Кнопка далее
        next_q_rect = pygame.Rect(700, 530, 192, 64)
        create_button(screen, next_q_rect, font.render("Далее", True, GOLD))

    elif running_end_game:
        screen.fill(GOLD)
        screen.blit(background_image_game, (0, 0))

        # Кнопки выхода в меню
        button_exit_game_rect = pygame.Rect(920, 23, 192, 64)
        create_button(screen, button_exit_game_rect, font.render("В меню", True, GOLD))

        win_player_txt = players[id_win_player].player_name

        # Информация о победителе
        win_player_rect = pygame.Rect(200, 220, 800, 60)
        create_button(screen, win_player_rect, font.render(f"{win_player_txt } выйграл", True, GOLD))

    if runningMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Проверка нажатия на кнопку старт
                if button_start_rect.collidepoint(event.pos):
                    runningMenu = False
                    runningGame_qc = True
                # Количество игроков
                elif button_cp_rect.collidepoint(mouse_pos):
                    count_players += 1
                    if count_players > 4:
                        count_players = 2
                # Проверка нажатия на кнопку правила
                elif button_manual_rect.collidepoint(event.pos):
                    runningMenu = False
                    runningManual = True
                # Проверка нажатия на кнопку выход
                elif button_exit_rect.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 4 or event.button == 5):
                if runningMenu and button_cp_rect.collidepoint(event.pos):
                    if event.button == 4:  # Прокрутка вверх
                        count_players += 1
                        if count_players > 4:
                            count_players = 2
                    elif event.button == 5:  # Прокрутка вниз
                        count_players -= 1
                        if count_players < 2:
                            count_players = 4

    if runningGame_qc:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Проверка нажатия на кнопку завершения игры
                if button_exit_game_rect.collidepoint(event.pos):
                    runningGame_qc = False
                    runningMenu = True
                if button_block_general_questions_rect.collidepoint(event.pos):
                    if len(questions_general) > 0:
                        runningGame_qc = False
                        runningGame_qa = True
                        question_id = random.randint(0, len(questions_general) - 1)
                        question_text = questions_general[question_id].question_text
                        question_answer_1 = questions_general[question_id].question_answer_1
                        question_answer_2 = questions_general[question_id].question_answer_2
                        question_answer_3 = questions_general[question_id].question_answer_3
                        question_answer_right = questions_general[question_id].question_answer_right
                        questions_type = 1
                        if question_answer_right == 1:
                            question_answer_right_txt = questions_general[question_id].question_answer_1
                        if question_answer_right == 2:
                            question_answer_right_txt = questions_general[question_id].question_answer_2
                        if question_answer_right == 3:
                            question_answer_right_txt = questions_general[question_id].question_answer_3
                        questions_general.pop(question_id)
                if button_block_focused_questions_rect.collidepoint(event.pos):
                    if len(questions_hack) > 0:
                        runningGame_qc = False
                        runningGame_qa = True
                        question_id = random.randint(0, len(questions_hack) - 1)
                        question_text = questions_hack[question_id].question_text
                        question_answer_1 = questions_hack[question_id].question_answer_1
                        question_answer_2 = questions_hack[question_id].question_answer_2
                        question_answer_3 = questions_hack[question_id].question_answer_3
                        question_answer_right = questions_hack[question_id].question_answer_right
                        questions_type = 2
                        if question_answer_right == 1:
                            question_answer_right_txt = questions_hack[question_id].question_answer_1
                        if question_answer_right == 2:
                            question_answer_right_txt = questions_hack[question_id].question_answer_2
                        if question_answer_right == 3:
                            question_answer_right_txt = questions_hack[question_id].question_answer_3
                        questions_hack.pop(question_id)

    if runningGame_qa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Проверка нажатия на кнопку завершения игры
                if button_exit_game_rect.collidepoint(event.pos):
                    runningGame_qa = False
                    runningMenu = True
                if question_answer_1_rect.collidepoint(event.pos):
                    player_answer = 1
                    if question_answer_right == 1:
                        players[resp_player].player_balance += 1
                        runningGame_qa = False
                        runningGame_right_q = True
                    else:
                        runningGame_qa = False
                        runningGame_right_q = True
                if question_answer_2_rect.collidepoint(event.pos):
                    player_answer = 2
                    if question_answer_right == 2:
                        players[resp_player].player_balance += 1
                        runningGame_qa = False
                        runningGame_right_q = True
                    else:
                        runningGame_qa = False
                        runningGame_right_q = True
                if question_answer_3_rect.collidepoint(event.pos):
                    player_answer = 3
                    if question_answer_right == 3:
                        players[resp_player].player_balance += 1
                        runningGame_qa = False
                        runningGame_right_q = True
                    else:
                        runningGame_qa = False
                        runningGame_right_q = True

    if runningGame_right_q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Проверка нажатия на кнопку завершения игры
                if button_exit_game_rect.collidepoint(event.pos):
                    runningGame_qa = False
                    runningMenu = True
                # Проверка нажатия на кнопку далее
                if next_q_rect.collidepoint(event.pos):
                    for i in range(0, 3):
                        if players[i].player_balance == 1:
                            id_win_player = i
                            runningGame_right_q = False
                            running_end_game = True
                    for i in range(0, 3):
                        if players[i].player_balance != 1:
                            runningGame_qa = False
                            runningGame_qc = True
                            resp_player += 1
                            if resp_player == count_players:
                                resp_player = 0

    if runningManual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Проверка нажатия на кнопку выхода из правил
                if button_exit_manual_rect.collidepoint(event.pos):
                    runningManual = False
                    runningMenu = True

    if running_end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Проверка нажатия на кнопку завершения игры
                if button_exit_game_rect.collidepoint(event.pos):
                    running_end_game = False
                    runningMenu = True

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()

