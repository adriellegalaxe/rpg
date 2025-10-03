# cadastro.py
import pygame, sqlite3, os

def tela_cadastro():
    if not pygame.get_init():
        pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Cadastro RPG")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    msg_font = pygame.font.SysFont(None, 28, bold=True)

    # carregar fundo
    BG_FILE = "backgroud.png"
    def load_image(path, size=None):
        if not os.path.exists(path):
            return None
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    bg = load_image(BG_FILE, (SCREEN_WIDTH, SCREEN_HEIGHT))

    campos = ["Nome", "Email", "Data de Nascimento (YYYY-MM-DD)", "Login", "Senha"]
    valores = ["", "", "", "", ""]
    campo_atual = 0
    msg_texto = ""
    msg_cor = (0,0,0)
    ativo = True

    # modo: jogador ou mestre
    tipo_cadastro = "jogador"

    # rects
    caixas = [pygame.Rect(50, 80 + i*80, 400, 40) for i in range(len(campos))]
    btn_confirmar = pygame.Rect(50, 80 + len(campos)*80, 200, 50)
    btn_fechar = pygame.Rect(SCREEN_WIDTH-40, 10, 30, 30)
    btn_tipo = pygame.Rect(300, 20, 200, 30)  # alternar cadastro

    while ativo:
        mx, my = pygame.mouse.get_pos()

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
                    pass
                else:
                    if event.unicode and ord(event.unicode) >= 32:
                        valores[campo_atual] += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_fechar.collidepoint((mx,my)):
                    ativo = False
                for i, c in enumerate(caixas):
                    if c.collidepoint((mx,my)):
                        campo_atual = i
                if btn_confirmar.collidepoint((mx,my)):
                    try:
                        conn = sqlite3.connect("rpg.db")
                        cursor = conn.cursor()
                        cursor.execute(
                            f"INSERT INTO {tipo_cadastro} (nome,email,datanasc,login,senha,id_mestre) VALUES (?,?,?,?,?,?)",
                            (valores[0].strip(), valores[1].strip(), valores[2].strip(),
                             valores[3].strip(), valores[4], 1)
                        )
                        conn.commit()
                        conn.close()
                        msg_texto = f"Cadastro de {tipo_cadastro} realizado com sucesso!"
                        msg_cor = (0,255,0)
                    except sqlite3.IntegrityError:
                        msg_texto = "Login já existe!"
                        msg_cor = (255,0,0)
                    except sqlite3.OperationalError as e:
                        msg_texto = "Erro no banco: " + str(e)
                        msg_cor = (255,0,0)
                if btn_tipo.collidepoint((mx,my)):
                    tipo_cadastro = "mestre" if tipo_cadastro == "jogador" else "jogador"

        # desenhar
        if bg:
            screen.blit(bg, (0,0))
        else:
            screen.fill((17,26,16))

        # botão fechar
        pygame.draw.rect(screen, (255,0,0), btn_fechar)
        screen.blit(font.render("X", True, (255,255,255)), (btn_fechar.x+6, btn_fechar.y+2))

        # mensagem
        if msg_texto:
            screen.blit(msg_font.render(msg_texto, True, msg_cor), (50, 20))

        # botão alternar Jogador/Mestre
        pygame.draw.rect(screen, (50,50,50), btn_tipo, border_radius=5)
        txt_tipo = font.render(f"Modo: {tipo_cadastro.capitalize()}", True, (255,255,255))
        screen.blit(txt_tipo, (btn_tipo.x+10, btn_tipo.y+5))

        # campos
        for i, c in enumerate(caixas):
            pygame.draw.rect(screen, (255,255,255), c, border_radius=5)
            display = valores[i]
            screen.blit(font.render(display, True, (0,0,0)), (c.x+5, c.y+5))
            screen.blit(font.render(f"{campos[i]}:", True, (255,255,255)), (c.x, c.y-25))

        # botão confirmar
        pygame.draw.rect(screen, (0,128,0), btn_confirmar, border_radius=5)
        screen.blit(font.render("CONFIRMAR", True, (255,255,255)), (btn_confirmar.x+20, btn_confirmar.y+10))

        pygame.display.flip()
        clock.tick(60)

    return
