import pygame, sqlite3, os

def tela_login():
    # Inicializa apenas se ainda não inicializado
    if not pygame.get_init():
        pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Login RPG")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 32)
    msg_font = pygame.font.SysFont(None, 28, bold=True)

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

    # Campos e mensagens
    campos = ["Login", "Senha"]
    valores = ["", ""]
    campo_atual = 0
    ativo = True
    msg_texto = ""
    msg_cor = (0,0,0)

    # Tipo de login: jogador ou mestre
    tipo_login = "jogador"

    # Posições das caixas e botões
    caixas = [pygame.Rect(50, 80, 300, 40), pygame.Rect(50, 160, 300, 40)]
    btn_entrar = pygame.Rect(50, 250, 150, 40)
    btn_fechar = pygame.Rect(SCREEN_WIDTH-40, 10, 30, 30)
    btn_tipo = pygame.Rect(50, 20, 200, 30)  # alternar login

    while ativo:
        mx, my = pygame.mouse.get_pos()

        # ---------- Eventos ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ativo = False
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                bg = load_image(BG_FILE, (SCREEN_WIDTH, SCREEN_HEIGHT))
                btn_fechar = pygame.Rect(SCREEN_WIDTH-40, 10, 30, 30)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    campo_atual = (campo_atual + 1) % len(campos)
                elif event.key == pygame.K_BACKSPACE:
                    valores[campo_atual] = valores[campo_atual][:-1]
                elif event.key == pygame.K_RETURN:
                    # Tentar login
                    try:
                        conn = sqlite3.connect("rpg.db")
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {tipo_login} WHERE login=? AND senha=?", 
                                       (valores[0], valores[1]))
                        user = cursor.fetchone()
                        conn.close()
                        if user:
                            msg_texto = f"Bem-vindo, {user[1]}"
                            msg_cor = (0,255,0)
                        else:
                            msg_texto = "Login inválido"
                            msg_cor = (255,0,0)
                    except sqlite3.OperationalError:
                        msg_texto = "Tabela não encontrada!"
                        msg_cor = (255,0,0)
                else:
                    valores[campo_atual] += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fechar
                if btn_fechar.collidepoint((mx,my)):
                    ativo = False
                # Focar em caixa
                for i, c in enumerate(caixas):
                    if c.collidepoint((mx,my)):
                        campo_atual = i
                # Clicar em entrar
                if btn_entrar.collidepoint((mx,my)):
                    try:
                        conn = sqlite3.connect("rpg.db")
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {tipo_login} WHERE login=? AND senha=?", 
                                       (valores[0], valores[1]))
                        user = cursor.fetchone()
                        conn.close()
                        if user:
                            msg_texto = f"Bem-vindo, {user[1]}"
                            msg_cor = (0,255,0)
                        else:
                            msg_texto = "Login inválido"
                            msg_cor = (255,0,0)
                    except sqlite3.OperationalError:
                        msg_texto = "Tabela não encontrada!"
                        msg_cor = (255,0,0)
                # Alternar jogador/mestre
                if btn_tipo.collidepoint((mx,my)):
                    tipo_login = "mestre" if tipo_login == "jogador" else "jogador"

        # ---------- Desenho ----------
        if bg:
            screen.blit(bg, (0,0))
        else:
            screen.fill((17,26,16))

        # Botão X
        pygame.draw.rect(screen, (255,0,0), btn_fechar)
        screen.blit(font.render("X", True, (255,255,255)), (SCREEN_WIDTH-32, 12))

        # Mensagem
        if msg_texto:
            screen.blit(msg_font.render(msg_texto, True, msg_cor), (50, 300))

        # Botão alternar Jogador/Mestre
        pygame.draw.rect(screen, (50,50,50), btn_tipo, border_radius=5)
        txt_tipo = font.render(f"Modo: {tipo_login.capitalize()}", True, (255,255,255))
        screen.blit(txt_tipo, (btn_tipo.x+10, btn_tipo.y+5))

        # Campos de texto
        for i, c in enumerate(caixas):
            pygame.draw.rect(screen, (255,255,255), c, border_radius=5)
            display_valor = valores[i] if i==0 else "*"*len(valores[i])
            screen.blit(font.render(display_valor, True, (0,0,0)), (c.x+5, c.y+5))
            label = font.render(f"{campos[i]}:", True, (255,255,255))
            screen.blit(label, (c.x, c.y - 25))

        # Botão entrar
        pygame.draw.rect(screen, (0,128,0), btn_entrar, border_radius=5)
        screen.blit(font.render("ENTRAR", True, (255,255,255)), (btn_entrar.x+20, btn_entrar.y+5))

        pygame.display.flip()
        clock.tick(60)
