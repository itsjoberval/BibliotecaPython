from datetime import datetime
import sqlite3
import uuid
from abc import ABC, abstractmethod


class LivroAbstrato(ABC):
    @abstractmethod
    def __init__(self, titulo, autor, editora, genero, qtd_exemplares):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.genero = genero
        self.qtd_exemplares = qtd_exemplares

    @abstractmethod
    def cadastrar_livro(self, conexao, titulo, autor, editora, genero, qtd_exemplares):
        pass

    @abstractmethod
    def emprestar(self, conexao, titulo, id_usuario, data_emprestimo, data_devolucao):
        pass

    @abstractmethod
    def devolver(self, conexao, titulo, data_devolucao):
        pass


class Livro(LivroAbstrato):
    def __init__(self, titulo, autor, editora, genero, qtd_exemplares):
        super().__init__(titulo, autor, editora, genero, qtd_exemplares)

    def cadastrar_livro(self, conexao, titulo, autor, editora, genero, qtd_exemplares):
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO Livro(titulo, autor, editora, genero, qtd_exemplares) VALUES (?, ?, ?, ?, ?)",
            (titulo, autor, editora, genero, qtd_exemplares),
        )
        conexao.commit()

    def emprestar(self, conexao, titulo, id_usuario, data_emprestimo, data_devolucao):
        cursor = conexao.cursor()
        cursor.execute("SELECT qtd_exemplares FROM Livro WHERE titulo = ?", (titulo,))
        livro = cursor.fetchone()

        if livro is None or livro[0] <= 0:
            return "Não existem mais exemplares disponíveis, por favor, busque por outro título."
        else:
            cursor.execute(
                "INSERT INTO emprestimos(titulo, id_usuario, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)",
                (titulo, id_usuario, data_emprestimo, data_devolucao),
            )
            cursor.execute(
                "UPDATE Livro SET qtd_exemplares = qtd_exemplares - 1 WHERE titulo = ?",
                (titulo,),
            )
            conexao.commit()
            return "Empréstimo realizado com sucesso!"

    def devolver(self, conexao, titulo, data_devolucao):
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE emprestimos SET data_devolucao = ? WHERE titulo = ?", (data_devolucao, titulo)
        )
        cursor.execute(
            "UPDATE Livro SET qtd_exemplares = qtd_exemplares + 1 WHERE titulo = ?",
            (titulo,),
        )
        conexao.commit()
        return "Devolução realizada com sucesso!"


class Biblioteca:
    def __init__(self):
        pass

    @staticmethod
    def cadastrar_usuario(conexao, id, nome, nacionalidade, telefone):
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO Usuario (id, nome, nacionalidade, telefone) VALUES (?, ?, ?, ?)",
            (id, nome, nacionalidade, telefone),
        )
        conexao.commit()
        return "Usuário cadastrado com sucesso!"

    @staticmethod
    def listar_livros(conexao):
        cursor = conexao.cursor()
        livros = cursor.execute("SELECT * FROM Livro").fetchall()
        return livros

    @staticmethod
    def historico_emprestimos(conexao):
        cursor = conexao.cursor()
        result = cursor.execute(
            """
            SELECT Livro.titulo, Usuario.nome, Emprestimos.data_emprestimo, Emprestimos.data_devolucao
            FROM Livro
            INNER JOIN Emprestimos ON Livro.titulo = Emprestimos.titulo
            INNER JOIN Usuario ON Usuario.id = Emprestimos.id_usuario
            WHERE Emprestimos.data_devolucao IS NOT NULL
            """
        ).fetchall()
        return result


def menu():
    print("------------Biblioteca------------")
    print("1- Cadastrar usuário")
    print("2- Cadastrar livros")
    print("3- Emprestar livros")
    print("4- Devolver livros")
    print("5- Listar livros")
    print("6- Histórico de empréstimos")
    print("0- Sair")
    return input("Digite a opção desejada: ")


def main():
    conexao = sqlite3.connect("biblioteca_poo.db")
    livro = Livro("", "", "", "", "")

    while True:
        opcao = menu()
        if opcao == "1":
            id = str(uuid.uuid4())
            nome = input("Digite seu nome: ")
            nacionalidade = input("Digite sua nacionalidade: ")
            telefone = input("Digite seu telefone: ")
            print(Biblioteca.cadastrar_usuario(conexao, id, nome, nacionalidade, telefone))

        elif opcao == "2":
            titulo = input("Qual o título do livro: ")
            autor = input("Digite o nome do autor do livro: ")
            editora = input("Digite o nome da editora do livro: ")
            genero = input("Digite o gênero do livro: ")
            qtd_exemplares = int(input("Digite a quantidade de exemplares: "))
            livro.cadastrar_livro(conexao, titulo, autor, editora, genero, qtd_exemplares)
            print("Livro cadastrado com sucesso!")

        elif opcao == "3":
            titulo = input("Digite o título do livro: ")
            id_usuario = input("Insira o ID do usuário: ")
            data_emprestimo = input("Digite a data de empréstimo (YYYY-MM-DD): ")
            data_devolucao = input("Digite a data de devolução (YYYY-MM-DD): ")
            print(livro.emprestar(conexao, titulo, id_usuario, data_emprestimo, data_devolucao))

        elif opcao == "4":
            titulo = input("Digite o título do livro emprestado: ")
            data_devolucao = input("Insira a data de devolução (YYYY-MM-DD): ")
            print(livro.devolver(conexao, titulo, data_devolucao))

        elif opcao == "5":
            livros = Biblioteca.listar_livros(conexao)
            print("Livros cadastrados:")
            for livro in livros:
                print(livro)

        elif opcao == "6":
            historico = Biblioteca.historico_emprestimos(conexao)
            print("Histórico de empréstimos:")
            for registro in historico:
                print(registro)

        elif opcao == "0":
            conexao.close()
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
