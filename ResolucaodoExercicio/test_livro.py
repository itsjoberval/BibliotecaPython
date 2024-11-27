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

    def test_cadastrar_livro(conexao_teste):
        livro = Livro("Teste", "Autor", "Editora", "Gênero", 10)
        resultado = livro.cadastrar_livro(
            conexao_teste, "Teste", "Autor", "Editora", "Gênero", 10
        )
        assert resultado is None

        cursor = conexao_teste.cursor()
        cursor.execute("SELECT * FROM Livro WHERE titulo = ?", ("Teste",))
        livro_cadastrado = cursor.fetchone()
        assert livro_cadastrado is not None
        assert livro_cadastrado[1] == "Autor"

    def test_emprestar_livro(conexao_teste):
        livro = Livro("Teste", "Autor", "Editora", "Gênero", 10)
        livro.cadastrar_livro(
            conexao_teste, "Teste", "Autor", "Editora", "Gênero", 10
        )

        resultado = livro.emprestar(
            conexao_teste, "Teste", "123", "2024-11-26", "2024-12-10"
        )
        assert resultado == "Empréstimo realizado com sucesso!"

        cursor = conexao_teste.cursor()
        cursor.execute("SELECT qtd_exemplares FROM Livro WHERE titulo = ?", ("Teste",))
        exemplares = cursor.fetchone()[0]
        assert exemplares == 9

    def test_devolver_livro(conexao_teste):
        livro = Livro("Teste", "Autor", "Editora", "Gênero", 10)
        livro.cadastrar_livro(
            conexao_teste, "Teste", "Autor", "Editora", "Gênero", 10
        )
        livro.emprestar(
            conexao_teste, "Teste", "123", "2024-11-26", "2024-12-10"
        )

        resultado = livro.devolver(conexao_teste, "Teste", "2024-12-10")
        assert resultado == "Devolução realizada com sucesso!"

        cursor = conexao_teste.cursor()
        cursor.execute("SELECT qtd_exemplares FROM Livro WHERE titulo = ?", ("Teste",))
        exemplares = cursor.fetchone()[0]
        assert exemplares == 10

