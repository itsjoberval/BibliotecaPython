import sqlite3
import pytest
from main import Livro

@pytest.fixture
def conexao_teste():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute(
        """
        CREATE TABLE Livro (
            titulo TEXT PRIMARY KEY,
            autor TEXT NOT NULL,
            editora TEXT NOT NULL,
            genero TEXT NOT NULL,
            qtd_exemplares INTEGER NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE emprestimos (
            titulo TEXT NOT NULL,
            id_usuario TEXT NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT
        )
        """
    )
    conexao.commit()
    yield conexao
    conexao.close()