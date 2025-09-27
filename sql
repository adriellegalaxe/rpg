-- =====================================
-- RPG ONLINE - SCRIPT COMPLETO PARA SQLITE
-- Relações:
-- Mestre 1:N Jogadores
-- Jogador 1 Mestre
-- Classes ↔ Habilidades
-- Cenários ↔ Mestre
-- Jogos ↔ Jogador e Cenário
-- =====================================

-- ===============================
-- TABELAS PRINCIPAIS
-- ===============================

CREATE TABLE mestre (
    id_mestre INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE jogador (
    id_jogador INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    datanasc TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    id_mestre INTEGER NOT NULL,
    FOREIGN KEY (id_mestre) REFERENCES mestre(id_mestre)
);

CREATE TABLE classepersonagem (
    id_classe INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeclasse TEXT NOT NULL,
    descricao TEXT,
    itensiniciais TEXT,
    habilidadesespeciais TEXT
);

CREATE TABLE habilidade (
    id_habilidade INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    efeito TEXT,
    custoenergia INTEGER
);

CREATE TABLE classe_habilidade (
    id_classe INTEGER NOT NULL,
    id_habilidade INTEGER NOT NULL,
    PRIMARY KEY (id_classe, id_habilidade),
    FOREIGN KEY (id_classe) REFERENCES classepersonagem(id_classe),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade)
);

CREATE TABLE personagem (
    id_personagem INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    historia TEXT,
    caracteristicas TEXT,
    pontoforte TEXT,
    pontofraco TEXT,
    energia INTEGER,
    vida INTEGER,
    id_jogador INTEGER NOT NULL,
    id_classe INTEGER NOT NULL,
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (id_classe) REFERENCES classepersonagem(id_classe)
);

CREATE TABLE item (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT,
    efeito TEXT
);

CREATE TABLE personagem_item (
    id_personagem INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    quantidade INTEGER,
    PRIMARY KEY (id_personagem, id_item),
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem),
    FOREIGN KEY (id_item) REFERENCES item(id_item)
);

CREATE TABLE personagem_habilidade (
    id_personagem INTEGER NOT NULL,
    id_habilidade INTEGER NOT NULL,
    nivel INTEGER,
    PRIMARY KEY (id_personagem, id_habilidade),
    FOREIGN KEY (id_personagem) REFERENCES personagem(id_personagem),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade)
);

CREATE TABLE cenario (
    id_cenario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    obstaculos TEXT,
    itensdisponiveis TEXT,
    id_mestre INTEGER NOT NULL,
    FOREIGN KEY (id_mestre) REFERENCES mestre(id_mestre)
);

CREATE TABLE item_cenario (
    id_cenario INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    quantidade INTEGER,
    PRIMARY KEY (id_cenario, id_item),
    FOREIGN KEY (id_cenario) REFERENCES cenario(id_cenario),
    FOREIGN KEY (id_item) REFERENCES item(id_item)
);

CREATE TABLE jogar (
    id_jogo INTEGER PRIMARY KEY AUTOINCREMENT,
    data_inicio TEXT,
    status TEXT,
    id_jogador INTEGER NOT NULL,
    id_cenario INTEGER NOT NULL,
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (id_cenario) REFERENCES cenario(id_cenario)
);

-- ===============================
-- INSERÇÕES DE DADOS DE TESTE
-- ===============================

-- Mestres
INSERT INTO mestre (nome, login, senha) VALUES
('Lucas', 'lucas_mestre', 'mestre123'),
('Patrícia', 'patri_m', 'narra456'),
('Jorge', 'jorge_mestre', 'senha7'),
('Beatriz', 'bea_game', 'senha8'),
('Tiago', 'tiagom', 'senha9');

-- Jogadores
INSERT INTO jogador (nome, email, datanasc, login, senha, id_mestre) VALUES
('Alice', 'alice@gmail.com', '2005-04-15', 'alice123', 'senha1', 1),
('Bruno', 'bruno@gmail.com', '2004-08-23', 'bruno22', 'senha2', 1),
('Clara', 'clara@gmail.com', '2006-01-10', 'clara_cl', 'senha3', 2),
('Diego', 'diego@gmail.com', '2003-12-02', 'diegoplay', 'senha4', 2),
('Eloá', 'eloa@gmail.com', '2007-09-09', 'eloa99', 'senha5', 3);

-- Classes
INSERT INTO classepersonagem (nomeclasse, descricao, itensiniciais, habilidadesespeciais) VALUES
('Mago', 'Especialista em magia elemental', 'Cajado mágico', 'Bola de Fogo'),
('Guerreiro', 'Combate corpo a corpo', 'Espada longa', 'Fúria'),
('Fada', 'Apoio com magias curativas', 'Pó mágico', 'Cura Total'),
('Ladino', 'Agilidade e furtividade', 'Adaga dupla', 'Golpe sombrio'),
('Arqueiro', 'Ataque à distância', 'Arco encantado', 'Tiro explosivo');

-- Habilidades
INSERT INTO habilidade (nome, efeito, custoenergia) VALUES
('Bola de Fogo', 'Explosão de fogo em área', 30),
('Fúria', 'Aumenta ataque em 50%', 20),
('Cura Total', 'Restaura toda a vida', 40),
('Golpe Sombrio', 'Ataque invisível', 25),
('Tiro Explosivo', 'Flecha com efeito explosivo', 35);

-- Classe ↔ Habilidade
INSERT INTO classe_habilidade (id_classe, id_habilidade) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- Personagens
INSERT INTO personagem (nome, historia, caracteristicas, pontoforte, pontofraco, energia, vida, id_jogador, id_classe) VALUES
('Eryn', 'Criada numa floresta mágica', 'leve e sábia', 'magia poderosa', 'pouca defesa', 80, 100, 1, 1),
('Thorg', 'Sobrevivente de batalhas', 'forte', 'resistência', 'pouca agilidade', 50, 200, 2, 2),
('Lumi', 'Fada do clã azul', 'curativa', 'ajuda em grupo', 'frágil', 90, 90, 3, 3),
('Shadow', 'Do reino das sombras', 'furtivo', 'invisibilidade', 'baixa defesa', 60, 110, 4, 4),
('Kiran', 'Arqueiro do deserto', 'precisão', 'visão noturna', 'pouco dano corpo a corpo', 70, 130, 5, 5);

-- Itens
INSERT INTO item (nome, tipo, efeito) VALUES
('Cajado', 'arma mágica', 'Aumenta poder mágico'),
('Espada', 'arma física', 'Dano extra em combate'),
('Poção de Cura', 'consumível', 'Recupera 50 de vida'),
('Armadura', 'defesa', 'Reduz dano em 10%'),
('Botas', 'equipamento', 'Aumenta velocidade');

-- Personagem_Item
INSERT INTO personagem_item (id_personagem, id_item, quantidade) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 2),
(4, 5, 1),
(5, 4, 1);

-- Personagem_Habilidade
INSERT INTO personagem_habilidade (id_personagem, id_habilidade, nivel) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1);

-- Cenários
INSERT INTO cenario (nome, descricao, obstaculos, itensdisponiveis, id_mestre) VALUES
('Floresta Encantada', 'Ambiente mágico com criaturas ocultas', 'Vines, Rochas', 'Poções, Cristais', 1),
('Campo de Batalha', 'Ruínas e destruição', 'Espinhos, Armadilhas', 'Espadas, Armaduras', 2),
('Caverna', 'Ambiente subterrâneo', 'Fendas, Escuridão', 'Mapas, Relíquias', 3),
('Vila Antiga', 'Área abandonada com casas', 'Ladrões, Buracos', 'Comida, Chaves', 4),
('Castelo', 'Palácio com guardas e tesouros', 'Soldados, Portões', 'Tesouros, Artefatos', 5);

-- Item_Cenario
INSERT INTO item_cenario (id_cenario, id_item, quantidade) VALUES
(1, 3, 2),
(2, 2, 1),
(3, 5, 1),
(4, 4, 1),
(5, 1, 1);

-- Jogos
INSERT INTO jogar (data_inicio, status, id_jogador, id_cenario) VALUES
('2025-06-01', 'em andamento', 1, 1),
('2025-06-03', 'finalizado', 2, 2),
('2025-06-05', 'em andamento', 3, 3),
('2025-06-06', 'pausado', 4, 4),
('2025-06-08', 'em andamento', 5, 5);
