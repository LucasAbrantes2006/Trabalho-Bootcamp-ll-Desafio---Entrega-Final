"""
Testes para o módulo database.py
Utiliza mocks para não depender de credenciais reais ou banco de dados disponível no CI
"""
import unittest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
import sys
import os

# Adiciona o diretório pai ao path para importar database
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import (
    conectar,
    formatar_data_nascimento,
    inserir_curso,
    listar_cursos,
    atualizar_curso,
    excluir_curso,
    inserir_aluno,
    listar_alunos,
    atualizar_aluno,
    excluir_aluno,
    inserir_funcionario,
    listar_funcionarios,
    atualizar_funcionario,
    excluir_funcionario,
    inserir_materia,
    listar_materias,
    atualizar_materia,
    excluir_materia,
    inserir_matricula,
    listar_matriculas,
    atualizar_matricula,
    excluir_matricula,
)


class TestFormatarDataNascimento(unittest.TestCase):
    """Testes para a função de formatação de data"""
    
    def test_formatacao_data_valida(self):
        """Testa formatação de data válida"""
        resultado = formatar_data_nascimento("12082005")
        self.assertEqual(resultado, "2005-08-12")
    
    def test_formatacao_data_invalida_raises_error(self):
        """Testa que data inválida levanta ValueError"""
        with self.assertRaises(ValueError):
            formatar_data_nascimento("invalid_date")
    
    def test_formatacao_data_formato_incorreto(self):
        """Testa que formato incorreto levanta ValueError"""
        with self.assertRaises(ValueError):
            formatar_data_nascimento("2005-08-12")  # formato errado


class TestCursos(unittest.TestCase):
    """Testes para operações CRUD de Cursos"""
    
    @patch('database.conectar')
    def test_inserir_curso(self, mock_conectar):
        """Testa inserção de curso"""
        # Setup do mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Executa função
        inserir_curso("Engenharia", 8)
        
        # Verifica chamadas
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        
        # Verifica SQL correto
        call_args = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO tb_curso", call_args[0][0])
    
    @patch('database.conectar')
    def test_listar_cursos(self, mock_conectar):
        """Testa listagem de cursos"""
        # Setup do mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, "Engenharia", 8), (2, "Administração", 6)]
        
        # Executa função
        resultado = listar_cursos()
        
        # Verifica resultado
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0][1], "Engenharia")
    
    @patch('database.conectar')
    def test_atualizar_curso(self, mock_conectar):
        """Testa atualização de curso"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        atualizar_curso(1, "Engenharia Atualizada", 9)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("UPDATE tb_curso", call_args[0][0])
    
    @patch('database.conectar')
    def test_excluir_curso(self, mock_conectar):
        """Testa exclusão de curso"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        excluir_curso(1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("DELETE FROM tb_curso", call_args[0][0])


class TestAlunos(unittest.TestCase):
    """Testes para operações CRUD de Alunos"""
    
    @patch('database.conectar')
    def test_inserir_aluno(self, mock_conectar):
        """Testa inserção de aluno"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        inserir_aluno("João Silva", "12345678901", "2005-08-12", 1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO tb_aluno", call_args[0][0])
    
    @patch('database.conectar')
    def test_listar_alunos(self, mock_conectar):
        """Testa listagem de alunos"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "João Silva", "12345678901", "2005-08-12", "Engenharia")
        ]
        
        resultado = listar_alunos()
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][1], "João Silva")
    
    @patch('database.conectar')
    def test_atualizar_aluno(self, mock_conectar):
        """Testa atualização de aluno"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        atualizar_aluno(1, "João Santos", "98765432101", "2005-08-12", 2)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("UPDATE tb_aluno", call_args[0][0])
    
    @patch('database.conectar')
    def test_excluir_aluno(self, mock_conectar):
        """Testa exclusão de aluno"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        excluir_aluno(1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("DELETE FROM tb_aluno", call_args[0][0])


class TestFuncionarios(unittest.TestCase):
    """Testes para operações CRUD de Funcionários"""
    
    @patch('database.conectar')
    def test_inserir_funcionario(self, mock_conectar):
        """Testa inserção de funcionário"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        inserir_funcionario("Maria", "Professora", 5000.00)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO tb_funcionario", call_args[0][0])
    
    @patch('database.conectar')
    def test_listar_funcionarios(self, mock_conectar):
        """Testa listagem de funcionários"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Maria", "Professora", 5000.00)
        ]
        
        resultado = listar_funcionarios()
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][1], "Maria")
    
    @patch('database.conectar')
    def test_atualizar_funcionario(self, mock_conectar):
        """Testa atualização de funcionário"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        atualizar_funcionario(1, "Maria Silva", "Diretora", 6000.00)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("UPDATE tb_funcionario", call_args[0][0])
    
    @patch('database.conectar')
    def test_excluir_funcionario(self, mock_conectar):
        """Testa exclusão de funcionário"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        excluir_funcionario(1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("DELETE FROM tb_funcionario", call_args[0][0])


class TestMaterias(unittest.TestCase):
    """Testes para operações CRUD de Matérias"""
    
    @patch('database.conectar')
    def test_inserir_materia(self, mock_conectar):
        """Testa inserção de matéria"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        inserir_materia("Cálculo I", 1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO tb_materia", call_args[0][0])
    
    @patch('database.conectar')
    def test_listar_materias(self, mock_conectar):
        """Testa listagem de matérias"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Cálculo I", "Engenharia")
        ]
        
        resultado = listar_materias()
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][1], "Cálculo I")
    
    @patch('database.conectar')
    def test_atualizar_materia(self, mock_conectar):
        """Testa atualização de matéria"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        atualizar_materia(1, "Cálculo II", 1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("UPDATE tb_materia", call_args[0][0])
    
    @patch('database.conectar')
    def test_excluir_materia(self, mock_conectar):
        """Testa exclusão de matéria"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        excluir_materia(1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("DELETE FROM tb_materia", call_args[0][0])


class TestMatriculas(unittest.TestCase):
    """Testes para operações CRUD de Matrículas"""
    
    @patch('database.conectar')
    def test_inserir_matricula(self, mock_conectar):
        """Testa inserção de matrícula"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        inserir_matricula(1, 1, 1, 2024)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO tb_matricula", call_args[0][0])
    
    @patch('database.conectar')
    def test_listar_matriculas(self, mock_conectar):
        """Testa listagem de matrículas"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "João Silva", "Cálculo I", 1, 2024)
        ]
        
        resultado = listar_matriculas()
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][1], "João Silva")
    
    @patch('database.conectar')
    def test_atualizar_matricula(self, mock_conectar):
        """Testa atualização de matrícula"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        atualizar_matricula(1, 1, 2, 2, 2024)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("UPDATE tb_matricula", call_args[0][0])
    
    @patch('database.conectar')
    def test_excluir_matricula(self, mock_conectar):
        """Testa exclusão de matrícula"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        excluir_matricula(1)
        
        mock_conn.commit.assert_called_once()
        call_args = mock_cursor.execute.call_args
        self.assertIn("DELETE FROM tb_matricula", call_args[0][0])


class TestConexao(unittest.TestCase):
    """Testes para a conexão com o banco de dados"""
    
    @patch('database.mysql.connector.connect')
    @patch.dict(os.environ, {'DB_HOST': 'localhost', 'DB_USER': 'root', 'DB_PASSWORD': 'password', 'DB_NAME': 'test_db'})
    def test_conectar_sucesso(self, mock_connect):
        """Testa conexão bem-sucedida"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        resultado = conectar()
        
        self.assertIsNotNone(resultado)
        mock_connect.assert_called_once()
    
    @patch('database.mysql.connector.connect')
    @patch.dict(os.environ, {'DB_HOST': 'localhost', 'DB_USER': 'root', 'DB_PASSWORD': 'wrong', 'DB_NAME': 'test_db'})
    def test_conectar_falha(self, mock_connect):
        """Testa conexão falhada"""
        from mysql.connector import Error
        mock_connect.side_effect = Error("Erro de conexão")
        
        resultado = conectar()
        
        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
