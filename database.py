import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# FUNÇÃO DE CONEXÃO
def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT", 4000)
        )
        return conexao
    except Error as e:
        print("Erro ao conectar ao MySQL:", e)
        return None

# O restante do arquivo (inserir_curso, etc.) continua igualzinho para baixo...


# CURSOS
def inserir_curso(nome, duracao):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO tb_curso (nome, duracao_semestres) VALUES (%s, %s)", (nome, duracao))
        con.commit()
        con.close()


def listar_cursos():
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tb_curso")
        dados = cursor.fetchall()
        con.close()
        return dados


def atualizar_curso(id_curso, nome, duracao):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("UPDATE tb_curso SET nome=%s, duracao_semestres=%s WHERE id_curso=%s",
                       (nome, duracao, id_curso))
        con.commit()
        con.close()


def excluir_curso(id_curso):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tb_curso WHERE id_curso=%s", (id_curso,))
        con.commit()
        con.close()


# ALUNOS

from datetime import datetime

def formatar_data_nascimento(data_str: str) -> str:
    try:
        data_formatada = datetime.strptime(data_str, "%d%m%Y").strftime("%Y-%m-%d")
        return data_formatada
    except ValueError:
        raise ValueError("Data inválida. Digite no formato DDMMYYYY (ex: 12082005).")


def inserir_aluno(nome, cpf, data_nascimento, id_curso):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO tb_aluno (nome, cpf, data_nascimento, id_curso) VALUES (%s, %s, %s, %s)",
            (nome, cpf, data_nascimento, id_curso)
        )
        con.commit()
        con.close()


def listar_alunos():
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT a.id_aluno, a.nome, a.cpf, a.data_nascimento, c.nome
            FROM tb_aluno a 
            INNER JOIN tb_curso c  ON a.id_curso = c.id_curso
        """)
        dados = cursor.fetchall()
        con.close()
        return dados


def atualizar_aluno(id_aluno, nome, cpf, data_nascimento, id_curso):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE tb_aluno 
            SET nome=%s, cpf=%s, data_nascimento=%s, id_curso=%s 
            WHERE id_aluno=%s
        """, (nome, cpf, data_nascimento, id_curso, id_aluno))
        con.commit()
        con.close()


def excluir_aluno(id_aluno):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tb_aluno WHERE id_aluno=%s", (id_aluno,))
        con.commit()
        con.close()


# FUNCIONÁRIOS
def inserir_funcionario(nome, cargo, salario):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO tb_funcionario (nome, cargo, salario)
            VALUES (%s, %s, %s)
        """, (nome, cargo, salario))
        con.commit()
        con.close()


def listar_funcionarios():
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tb_funcionario")
        dados = cursor.fetchall()
        con.close()
        return dados


def atualizar_funcionario(id_funcionario, nome, cargo, salario):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE tb_funcionario SET nome=%s, cargo=%s, salario=%s
            WHERE id_funcionario=%s
        """, (nome, cargo, salario, id_funcionario))
        con.commit()
        con.close()


def excluir_funcionario(id_funcionario):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tb_funcionario WHERE id_funcionario=%s", (id_funcionario,))
        con.commit()
        con.close()


# MATÉRIAS
def inserir_materia(nome, id_curso):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO tb_materia (nome, id_curso)
            VALUES (%s, %s)
        """, (nome, id_curso))
        con.commit()
        con.close()


def listar_materias():
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT m.id_materia, m.nome, c.nome
            FROM tb_materia m
            LEFT JOIN tb_curso c ON m.id_curso = c.id_curso
        """)
        dados = cursor.fetchall()
        con.close()
        return dados


def atualizar_materia(id_materia, nome, id_curso):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE tb_materia SET nome=%s, id_curso=%s WHERE id_materia=%s
        """, (nome, id_curso, id_materia))
        con.commit()
        con.close()


def excluir_materia(id_materia):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tb_materia WHERE id_materia=%s", (id_materia,))
        con.commit()
        con.close()


# MATRÍCULAS
def inserir_matricula(id_aluno, id_materia, semestre, ano):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO tb_matricula (id_aluno, id_materia, semestre, ano)
            VALUES (%s, %s, %s, %s)
        """, (id_aluno, id_materia, semestre, ano))
        con.commit()
        con.close()


def listar_matriculas():
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT m.id_matricula, a.nome, ma.nome, m.semestre, m.ano
            FROM tb_matricula m
            LEFT JOIN tb_aluno a ON m.id_aluno = a.id_aluno
            LEFT JOIN tb_materia ma ON m.id_materia = ma.id_materia
        """)
        dados = cursor.fetchall()
        con.close()
        return dados
    
def atualizar_matricula(id_matricula, id_aluno ,id_materia , semestre, ano):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE tb_matricula SET id_aluno=%s , id_materia=%s, semestre=%s , ano=%s WHERE id_matricula=%s
        """, (id_aluno, id_materia, semestre , ano , id_matricula))
        con.commit()
        con.close()


def excluir_matricula(id_matricula):
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tb_matricula WHERE id_matricula=%s", (id_matricula,))
        con.commit()
        con.close()
