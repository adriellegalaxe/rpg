import sqlite3

# Cria (ou abre) o banco
conn = sqlite3.connect("rpg.db")
cursor = conn.cursor()

# Script SQL completo
sql_script = """
-- Criação das tabelas

CREATE TABLE mestre (
    id_mestre INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE jogador (
    id_jogador INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    datanasc DATE NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    id_mestre INTEGER NOT NULL,
    FOREIGN KEY (id_mestre) REFERENCES mestre(id_mestre)
);

CREATE TABLE classepersonagem (
    id_classe INTEGER PRIMARY KEY,
    nomeclasse TEXT NOT NULL,
    descricao TEXT,
    itensiniciais TEXT,
    habilidadesespeciais TEXT
);

CREATE TABLE habilidade (
    id_habilidade INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    efeito TEXT,
    cursoenergia INTEGER
);

CREATE TABLE classe_habilidade (
    id_classe INTEGER NOT NULL,
    id_habilidade INTEGER NOT NULL,
    PRIMARY KEY (id_classe, id_habilidade),
    FOREIGN KEY (id_classe) REFERENCES classepersonagem(id_classe),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade)
);

CREATE TABLE personagem (
    id_personagem INTEGER PRIMARY KEY,
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
    id_item INTEGER PRIMARY KEY,
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
    id_cenario INTEGER PRIMARY KEY,
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
    id_jogo INTEGER PRIMARY KEY,
    data_inicio DATE,
    status TEXT,
    id_jogador INTEGER NOT NULL,
    id_cenario INTEGER NOT NULL,
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (id_cenario) REFERENCES cenario(id_cenario)
);

-- Inserindo dados de exemplo

INSERT INTO mestre VALUES (1, 'Lucas', 'lucas_mestre', 'mestre123');
INSERT INTO mestre VALUES (2, 'Patrícia', 'patri_m', 'narra456');
INSERT INTO mestre VALUES (3, 'Jorge', 'jorge_mestre', 'senha7');
INSERT INTO mestre VALUES (4, 'Beatriz', 'bea_game', 'senha8');
INSERT INTO mestre VALUES (5, 'Tiago', 'tiagom', 'senha9');

INSERT INTO jogador VALUES (1, 'Alice', 'alice@gmail.com', '2005-04-15', 'alice123', 'senha1', 1);
INSERT INTO jogador VALUES (2, 'Bruno', 'bruno@gmail.com', '2004-08-23', 'bruno22', 'senha2', 3);
INSERT INTO jogador VALUES (3, 'Clara', 'clara@gmail.com', '2006-01-10', 'clara_cl', 'senha3', 1);
INSERT INTO jogador VALUES (4, 'Diego', 'diego@gmail.com', '2003-12-02', 'diegoplay', 'senha4', 2);
INSERT INTO jogador VALUES (5, 'Eloá', 'eloa@gmail.com', '2007-09-09', 'eloa99', 'senha5', 5);

INSERT INTO classepersonagem VALUES (1, 'Mago', 'Especialista em magia elemental', 'Cajado mágico', 'Bola de Fogo');
INSERT INTO classepersonagem VALUES (2, 'Guerreiro', 'Combate corpo a corpo', 'Espada longa', 'Fúria');
INSERT INTO classepersonagem VALUES (3, 'Fada', 'Apoio com magias curativas', 'Pó mágico', 'Cura Total');
INSERT INTO classepersonagem VALUES (4, 'Ladino', 'Agilidade e furtividade', 'Adaga dupla', 'Golpe sombrio');
INSERT INTO classepersonagem VALUES (5, 'Arqueiro', 'Ataque à distância', 'Arco encantado', 'Tiro explosivo');

INSERT INTO habilidade VALUES (1, 'Bola de Fogo', 'Explosão de fogo em área', 30);
INSERT INTO habilidade VALUES (2, 'Fúria', 'Aumenta ataque em 50%', 20);
INSERT INTO habilidade VALUES (3, 'Cura Total', 'Restaura toda a vida', 40);
INSERT INTO habilidade VALUES (4, 'Golpe Sombrio', 'Ataque invisível', 25);
INSERT INTO habilidade VALUES (5, 'Tiro Explosivo', 'Flecha com efeito explosivo', 35);

INSERT INTO classe_habilidade VALUES (1, 1);
INSERT INTO classe_habilidade VALUES (2, 2);
INSERT INTO classe_habilidade VALUES (3, 3);
INSERT INTO classe_habilidade VALUES (4, 4);
INSERT INTO classe_habilidade VALUES (5, 5);

INSERT INTO personagem VALUES (1, 'Eryn', 'Criada numa floresta mágica', 'leve e sábia', 'magia poderosa', 'pouca defesa', 80, 100, 1, 1);
INSERT INTO personagem VALUES (2, 'Thorg', 'Sobrevivente de batalhas', 'forte', 'resistência', 'pouca agilidade', 50, 200, 2, 2);
INSERT INTO personagem VALUES (3, 'Lumi', 'Fada do clã azul', 'curativa', 'ajuda em grupo', 'frágil', 90, 90, 3, 3);
INSERT INTO personagem VALUES (4, 'Shadow', 'Do reino das sombras', 'furtivo', 'invisibilidade', 'baixa defesa', 60, 110, 4, 4);
INSERT INTO personagem VALUES (5, 'Kiran', 'Arqueiro do deserto', 'precisão', 'visão noturna', 'pouco dano corpo a corpo', 70, 130, 5, 5);

INSERT INTO item VALUES (1, 'Cajado', 'arma mágica', 'Aumenta poder mágico');
INSERT INTO item VALUES (2, 'Espada', 'arma física', 'Dano extra em combate');
INSERT INTO item VALUES (3, 'Poção de Cura', 'consumível', 'Recupera 50 de vida');
INSERT INTO item VALUES (4, 'Armadura', 'defesa', 'Reduz dano em 10%');
INSERT INTO item VALUES (5, 'Botas', 'equipamento', 'Aumenta velocidade');

INSERT INTO personagem_item VALUES (1, 1, 1);
INSERT INTO personagem_item VALUES (2, 2, 1);
INSERT INTO personagem_item VALUES (3, 3, 2);
INSERT INTO personagem_item VALUES (4, 5, 1);
INSERT INTO personagem_item VALUES (5, 4, 1);

INSERT INTO personagem_habilidade VALUES (1, 1, 1);
INSERT INTO personagem_habilidade VALUES (2, 2, 1);
INSERT INTO personagem_habilidade VALUES (3, 3, 1);
INSERT INTO personagem_habilidade VALUES (4, 4, 1);
INSERT INTO personagem_habilidade VALUES (5, 5, 1);

INSERT INTO cenario VALUES (1, 'Floresta Encantada', 'Ambiente mágico com criaturas ocultas', 'Vines, Rochas', 'Poções, Cristais', 1);
INSERT INTO cenario VALUES (2, 'Campo de Batalha', 'Ruínas e destruição', 'Espinhos, Armadilhas', 'Espadas, Armaduras', 2);
INSERT INTO cenario VALUES (3, 'Caverna', 'Ambiente subterrâneo', 'Fendas, Escuridão', 'Mapas, Relíquias', 3);
INSERT INTO cenario VALUES (4, 'Vila Antiga', 'Área abandonada com casas', 'Ladrões, Buracos', 'Comida, Chaves', 4);
INSERT INTO cenario VALUES (5, 'Castelo', 'Palácio com guardas e tesouros', 'Soldados, Portões', 'Tesouros, Artefatos', 5);

INSERT INTO item_cenario VALUES (1, 3, 2);
INSERT INTO item_cenario VALUES (2, 2, 1);
INSERT INTO item_cenario VALUES (3, 5, 1);
INSERT INTO item_cenario VALUES (4, 4, 1);
INSERT INTO item_cenario VALUES (5, 1, 1);

INSERT INTO jogar VALUES (1, '2025-06-01', 'em andamento', 1, 1);
INSERT INTO jogar VALUES (2, '2025-06-03', 'finalizado', 2, 2);
INSERT INTO jogar VALUES (3, '2025-06-05', 'em andamento', 3, 3);
INSERT INTO jogar VALUES (4, '2025-06-06', 'pausado', 4, 4);
INSERT INTO jogar VALUES (5, '2025-06-08', 'em andamento', 5, 5);"""
cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Banco criado com sucesso dentro do Python!")
