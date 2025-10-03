import pygame, os, cadastro, login

pygame.init()

# ---------- Configurações da tela ----------
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("RPG MEDIEVAL FANTASIA")
clock = pygame.time.Clock()

# ---------- Fundo ----------
BG_FILE = "backgroud.png"
def load_image(path, size=None):
    if not os.path.exists(path):
        return None
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img

bg = load_image(BG_FILE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# ---------- Botões ----------
btn_cadastro = load_image("cadastrar.png", (500, 350))
btn_login = load_image("fazerlogin.png", (500, 350))

# ---------- Funções ----------
def posicoes_botoes():
    # Login em cima, cadastro embaixo
    x = SCREEN_WIDTH//2 - 250  # centralizado horizontalmente (500 / 2)
    y_login = SCREEN_HEIGHT//2 - 150
    y_cadastro = y_login + 200
    return x, y_login, x, y_cadastro

def botao_clicado(mx, my, x, y, w, h):
    return x <= mx <= x+w and y <= my <= y+h

# ---------- Loop principal ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            bg = load_image(BG_FILE, (SCREEN_WIDTH, SCREEN_HEIGHT))

    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        login_x, login_y, cad_x, cad_y = posicoes_botoes()
        if botao_clicado(mx, my, cad_x, cad_y, 500, 350):
            cadastro.tela_cadastro()
        elif botao_clicado(mx, my, login_x, login_y, 500, 350):
            login.tela_login()  # abre login em nova janela

    # ---------- Desenho ----------
    if bg:
        screen.blit(bg, (0,0))
    else:
        screen.fill((17,26,16))

    login_x, login_y, cad_x, cad_y = posicoes_botoes()
    if btn_login: screen.blit(btn_login, (login_x, login_y))
    if btn_cadastro: screen.blit(btn_cadastro, (cad_x, cad_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
