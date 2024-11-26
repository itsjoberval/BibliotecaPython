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