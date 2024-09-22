-- Cria o banco de dados
CREATE DATABASE IF NOT EXISTS padaria;
USE padaria;

-- Tabela clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) DEFAULT NULL,
    telefone VARCHAR(15) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL
);

-- Tabela produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(15, 2) NOT NULL,
    estoque INT NOT NULL
);

-- Tabela de usuarios do sistema
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) not null,
    senha VARCHAR(8) not null
);

-- Tabela intermediária cliente_produto para registrar compras
CREATE TABLE IF NOT EXISTS cliente_produto (
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    preco DECIMAL(15, 2) NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (id_cliente, id_produto),
    CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES produtos(id)
);

-- Trigger para atualizar o estoque de produtos quando a quantidade for alterada
DELIMITER //

CREATE TRIGGER atualiza_estoque_cliente_produto
AFTER INSERT ON cliente_produto
FOR EACH ROW
BEGIN
    -- Atualiza o estoque do produto
    UPDATE produtos
    SET estoque = estoque - NEW.quantidade
    WHERE id = NEW.id_produto;
END //

DELIMITER ;
