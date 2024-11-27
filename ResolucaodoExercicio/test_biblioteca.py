import sqlite3
import pytest
from main import Biblioteca

@pytest.fixture
def conexao_teste():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute(
        """
        CREATE TABLE Usuario (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            nacionalidade TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
        """
    )
    conexao.commit()
    yield conexao
    conexao.close()


def test_cadastrar_usuario(conexao_teste):
    biblioteca = Biblioteca()
    id_usuario = "123"
    nome = "Teste User"
    nacionalidade = "Brasil"
    telefone = "12345678"
    
    resultado = biblioteca.cadastrar_usuario(conexao_teste, id_usuario, nome, nacionalidade, telefone)
    assert resultado == "Usuário cadastrado com sucesso!"

    cursor = conexao_teste.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id_usuario,))
    usuario = cursor.fetchone()
    assert usuario is not None
    assert usuario[1] == nome
