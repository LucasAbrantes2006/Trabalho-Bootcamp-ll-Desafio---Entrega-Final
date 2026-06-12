import customtkinter as ctk
from database import *
from api_ibge import IBGEApiError, buscar_municipios_por_uf
from datetime import datetime
import re



# CONFIGURAÇÕES GERAIS
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("roxo_theme.json")


# ============================================================
# SISTEMA DE VALIDAÇÕES E FEEDBACK VISUAL
# ============================================================

class NotificadorUso:
    """Sistema centralizado para exibir mensagens de feedback ao usuário"""
    
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.label_mensagem = None
        
    def _criar_label_notificacao(self):
        """Cria um label para exibir mensagens"""
        if self.label_mensagem is not None:
            self.label_mensagem.destroy()
        
        self.label_mensagem = ctk.CTkLabel(
            self.janela_principal,
            text="",
            text_color="white",
            font=("Arial", 12)
        )
        self.label_mensagem.place(relx=0.5, rely=0.95, anchor="center")
    
    def sucesso(self, mensagem):
        """Exibe mensagem de sucesso (verde)"""
        self._criar_label_notificacao()
        self.label_mensagem.configure(text=f"✓ {mensagem}", text_color="lightgreen")
        self.janela_principal.after(3000, lambda: self.label_mensagem.configure(text=""))
    
    def erro(self, mensagem):
        """Exibe mensagem de erro (vermelho)"""
        self._criar_label_notificacao()
        self.label_mensagem.configure(text=f"✗ {mensagem}", text_color="#FF6B6B")
        # Não desaparece automaticamente para o usuário ler
    
    def info(self, mensagem):
        """Exibe mensagem informativa (azul)"""
        self._criar_label_notificacao()
        self.label_mensagem.configure(text=f"ℹ {mensagem}", text_color="lightblue")
        self.janela_principal.after(3000, lambda: self.label_mensagem.configure(text=""))
    
    def limpar(self):
        """Remove a mensagem"""
        if self.label_mensagem:
            self.label_mensagem.configure(text="")


class ValidadorCampos:
    """Sistema centralizado para validar entradas de usuário"""
    
    @staticmethod
    def validar_texto_nao_vazio(texto, nome_campo):
        """Valida se um campo de texto não está vazio"""
        if not texto or not texto.strip():
            raise ValueError(f"{nome_campo} não pode estar vazio")
        return texto.strip()
    
    @staticmethod
    def validar_cpf(cpf):
        """Valida CPF - apenas números"""
        cpf_limpo = re.sub(r'\D', '', cpf)
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos")
        if not cpf_limpo.isdigit():
            raise ValueError("CPF deve conter apenas números")
        return cpf_limpo
    
    @staticmethod
    def validar_data_nascimento(data_str):
        """Valida data no formato DDMMYYYY"""
        try:
            if len(data_str) != 8 or not data_str.isdigit():
                raise ValueError("Data deve ter 8 dígitos no formato DDMMYYYY")
            
            dia = int(data_str[0:2])
            mes = int(data_str[2:4])
            ano = int(data_str[4:8])
            
            # Validação básica de ranges
            if not (1 <= mes <= 12):
                raise ValueError("Mês inválido (deve estar entre 01 e 12)")
            if not (1 <= dia <= 31):
                raise ValueError("Dia inválido (deve estar entre 01 e 31)")
            if not (1900 <= ano <= datetime.now().year):
                raise ValueError(f"Ano inválido (deve estar entre 1900 e {datetime.now().year})")
            
            # Tenta criar a data para validar completamente
            datetime.strptime(data_str, "%d%m%Y")
            return data_str
        except ValueError as e:
            raise ValueError(f"Data inválida. {str(e)} Formato correto: DDMMYYYY")
    
    @staticmethod
    def validar_numero(valor, nome_campo, minimo=None, maximo=None):
        """Valida se um valor é numérico"""
        try:
            numero = float(valor)
            if minimo is not None and numero < minimo:
                raise ValueError(f"{nome_campo} não pode ser menor que {minimo}")
            if maximo is not None and numero > maximo:
                raise ValueError(f"{nome_campo} não pode ser maior que {maximo}")
            return numero
        except ValueError:
            raise ValueError(f"{nome_campo} deve ser um número válido")
    
    @staticmethod
    def validar_inteiro(valor, nome_campo, minimo=None):
        """Valida se um valor é um inteiro positivo"""
        try:
            numero = int(valor)
            if minimo is not None and numero < minimo:
                raise ValueError(f"{nome_campo} deve ser >= {minimo}")
            return numero
        except ValueError:
            raise ValueError(f"{nome_campo} deve ser um número inteiro válido")
    
    @staticmethod
    def validar_salario(valor_str):
        """Valida valor de salário"""
        try:
            salario = float(valor_str)
            if salario < 0:
                raise ValueError("Salário não pode ser negativo")
            return salario
        except ValueError:
            raise ValueError("Salário deve ser um valor numérico válido (ex: 3500.00)")
    
    @staticmethod
    def validar_duracao_curso(duracao_str):
        """Valida duração do curso em semestres"""
        try:
            duracao = int(duracao_str)
            if duracao <= 0 or duracao > 12:
                raise ValueError("Duração deve estar entre 1 e 12 semestres")
            return duracao
        except ValueError:
            raise ValueError("Duração deve ser um número inteiro entre 1 e 12")


class UniversidadeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Inicializar sistemas de validação e notificação
        self.notificador = NotificadorUso(self)
        self.validador = ValidadorCampos()
        
        #CONFIGURAÇÕES INICIAIS
        self.title("CEUCRUD")
        self.geometry("1920x1080")
        self.resizable(True , True)
        self.switch_tema = ctk.CTkSwitch(self , width=200, height=150 ,text="Modo Escuro" , command=self.alterar_tema)
        self.switch_tema.place(relx=0.95 , y=50 , anchor="center")
        if ctk.get_appearance_mode() == "dark":
            self.switch_tema.deselect()
        else:
            self.switch_tema.select()
        
        
        #TITULO PRINCIPAL
        titulo = ctk.CTkLabel(self, text="Sistema de Gerenciamento Universitário", font=("Arial", 30, "bold"))
        titulo.place(x=960 , y=50 , anchor="center")

        #TITULO CEUCRUD
        ceucrud = ctk.CTkLabel(self, text="CEUCRUD" , font=("Arial", 30,"bold") , text_color="purple")
        ceucrud.place(x=100 , y=50,anchor="center")
        
        # Tabs principais
        abas = ctk.CTkTabview(self, width=1280, height=720)
        abas.place(relx=0.5,rely=0.5,anchor="center")

        # Criação das abas
        aba_cursos = abas.add("Cursos")
        aba_alunos = abas.add("Alunos")
        aba_funcionarios = abas.add("Funcionários")
        aba_materias = abas.add("Matérias")
        aba_matriculas = abas.add("Matrículas")
        aba_ibge = abas.add("IBGE")

        # ABA CURSOS
            #NOME
        self.curso_nome = ctk.CTkEntry(aba_cursos, placeholder_text="Nome do Curso")
        self.curso_nome.place(relx=0.5 - 0.1 , rely=0.2 , anchor="center")
            #DURAÇÃO
        self.curso_duracao = ctk.CTkEntry(aba_cursos, placeholder_text="Duração (em semestres)")
        self.curso_duracao.place(relx=0.5 + 0.1 , rely=0.2 , anchor="center")
            #BANCO_DE_DADOS
        self.txt_cursos = ctk.CTkTextbox(aba_cursos, width=750, height=300)
        self.txt_cursos.place(relx=0.5 , rely=0.5 , anchor="center")
            #EXCLUIR
        self.txt_exc_curso = ctk.CTkEntry(aba_cursos,placeholder_text="Id para Excluir")
        self.txt_exc_curso.place(relx=0.5 + 0.1 , rely=0.85 , anchor="center")
        
        ctk.CTkButton(aba_cursos, text="Excluir" , command=self.deletar_curso).place(relx=0.5 + 0.22, rely=0.85 , anchor="center")
            #ADICIONAR
        ctk.CTkButton(aba_cursos, text="Adicionar Curso", command=self.adicionar_curso).place(relx=0.5 -0.21 , rely=0.85 , anchor="center")
            #LISTAR
        ctk.CTkButton(aba_cursos, text="Listar Cursos", command=self.listar_cursos).place(relx=0.5 -0.05 , rely=0.85 , anchor="center")
            #ATUALIZAR
        ctk.CTkButton(aba_cursos, text="Atualizar", command=self.popup_atualizar_curso).place(relx=0.07, rely=0.5)
        
        # ABA ALUNOS
            #NOME
        self.aluno_nome = ctk.CTkEntry(aba_alunos, placeholder_text="Nome do Aluno")
        self.aluno_nome.place(relx=0.5 - 0.22 , rely=0.2 , anchor="center")
            #CPF
        self.aluno_cpf = ctk.CTkEntry(aba_alunos, placeholder_text="CPF (somente números)")
        self.aluno_cpf.place(relx=0.5 - 0.08 , rely=0.2 , anchor="center")
            #DATA DE NASCIMENTO
        self.aluno_data = ctk.CTkEntry(aba_alunos, placeholder_text="Data de Nascimento - Somente Numeros")
        self.aluno_data.place(relx=0.5 + 0.07, rely=0.2 , anchor="center")
            #ID DO CURSO
        self.aluno_curso = ctk.CTkEntry(aba_alunos, placeholder_text="ID do Curso")
        self.aluno_curso.place(relx=0.5 + 0.22 , rely=0.2 , anchor="center")
            #BANCO_DE_DADOS
        self.txt_alunos = ctk.CTkTextbox(aba_alunos, width=750, height=300)
        self.txt_alunos.place(relx=0.5 , rely=0.5 , anchor="center")
            #EXCLUIR   
        self.txt_exc_aluno = ctk.CTkEntry(aba_alunos,placeholder_text="Id para Excluir")
        self.txt_exc_aluno.place(relx=0.5 + 0.1 , rely=0.85 , anchor="center")
        ctk.CTkButton(aba_alunos, text="Excluir" , command=self.deletar_aluno).place(relx=0.5 + 0.22, rely=0.85 , anchor="center")
            #ADICIONAR 
        ctk.CTkButton(aba_alunos, text="Adicionar Aluno", command=self.adicionar_aluno).place(relx=0.5 -0.21 , rely=0.85 , anchor="center")
            #LISTAR
        ctk.CTkButton(aba_alunos, text="Listar Alunos", command=self.listar_alunos).place(relx=0.5 -0.05 , rely=0.85 , anchor="center")
            #ATUALIZAR
        ctk.CTkButton(aba_alunos, text="Atualizar", command=self.popup_atualizar_aluno).place(relx=0.07, rely=0.5)

        # ABA FUNCIONÁRIOS
            #NOME FUNCIONARIO
        self.func_nome = ctk.CTkEntry(aba_funcionarios, placeholder_text="Nome do Funcionário")
        self.func_nome.place(relx=0.5 - 0.2 , rely = 0.2 , anchor="center")
            #CARGO
        self.func_cargo = ctk.CTkEntry(aba_funcionarios, placeholder_text="Cargo")
        self.func_cargo.place(relx=0.5 , rely = 0.2 , anchor="center")
            #SALARIO
        self.func_salario = ctk.CTkEntry(aba_funcionarios, placeholder_text="Salário (ex: 3500.00)")
        self.func_salario.place(relx=0.5 + 0.2 , rely = 0.2 , anchor="center")
            #BANCO_DE_DADOS
        self.txt_funcionarios = ctk.CTkTextbox(aba_funcionarios, width=750, height=300)
        self.txt_funcionarios.place(relx=0.5 , rely=0.5 , anchor="center")
            #ADICIONAR
        ctk.CTkButton(aba_funcionarios, text="Adicionar Funcionário", command=self.adicionar_funcionario).place(relx=0.5 -0.21 , rely=0.85 , anchor="center")
            #LISTAR
        ctk.CTkButton(aba_funcionarios, text="Listar Funcionários", command=self.listar_funcionarios).place(relx=0.5 - 0.04  , rely=0.85 , anchor="center")
            #EXCLUIR
        self.txt_exc_funcionario = ctk.CTkEntry(aba_funcionarios,placeholder_text="Id para Excluir")
        self.txt_exc_funcionario.place(relx=0.5 + 0.1 , rely=0.85 , anchor="center")
        ctk.CTkButton(aba_funcionarios, text="Excluir" , command=self.deletar_funcionario).place(relx=0.5 + 0.22, rely=0.85 , anchor="center")
            #ATUALIZAR
        ctk.CTkButton(aba_funcionarios, text="Atualizar", command=self.popup_atualizar_funcionario).place(relx=0.07, rely=0.5)

        # ABA MATÉRIAS
            #NOME MATERIA
        self.materia_nome = ctk.CTkEntry(aba_materias, placeholder_text="Nome da Matéria")
        self.materia_nome.place(relx=0.5 - 0.1 , rely=0.2 , anchor="center")
            #ID DO CURSO DA MATERIA
        self.materia_curso = ctk.CTkEntry(aba_materias, placeholder_text="ID do Curso")
        self.materia_curso.place(relx=0.5 + 0.1 , rely=0.2 , anchor="center")
            #BANCO_DE_DADOS
        self.txt_materias = ctk.CTkTextbox(aba_materias, width=750, height=300)
        self.txt_materias.place(relx=0.5 , rely=0.5 , anchor="center")
            #EXCLUIR
        self.txt_exc_materias = ctk.CTkEntry(aba_materias,placeholder_text="Id para Excluir")
        self.txt_exc_materias.place(relx=0.5 + 0.1 , rely=0.85 , anchor="center")
        ctk.CTkButton(aba_materias, text="Excluir" , command=self.deletar_materia).place(relx=0.5 + 0.22, rely=0.85 , anchor="center")
            #ADICIONAR
        ctk.CTkButton(aba_materias, text="Adicionar Matéria", command=self.adicionar_materia).place(relx=0.5 -0.21 , rely=0.85 , anchor="center")
            #LISTAR
        ctk.CTkButton(aba_materias, text="Listar Matérias", command=self.listar_materias).place(relx=0.5 -0.05 , rely=0.85 , anchor="center")
            #ATUALIZAR
        ctk.CTkButton(aba_materias, text="Atualizar", command=self.popup_atualizar_materia).place(relx=0.07, rely=0.5)

        # ABA MATRÍCULAS
            #ID DO ALUNO
        self.matricula_aluno = ctk.CTkEntry(aba_matriculas, placeholder_text="ID do Aluno")
        self.matricula_aluno.place(relx=0.5 - 0.22 , rely=0.2 , anchor="center")
            #ID DA MATERIA
        self.matricula_materia = ctk.CTkEntry(aba_matriculas, placeholder_text="ID da Matéria")
        self.matricula_materia.place(relx=0.5 - 0.08 , rely=0.2 , anchor="center")
            #SEMESTRE
        self.matricula_semestre = ctk.CTkEntry(aba_matriculas, placeholder_text="Semestre (ex: 1º, 2º, etc.)")
        self.matricula_semestre.place(relx=0.5 + 0.07, rely=0.2 , anchor="center")
            #ANO
        self.matricula_ano = ctk.CTkEntry(aba_matriculas, placeholder_text="Ano (ex: 2025)")
        self.matricula_ano.place(relx=0.5 + 0.22 , rely=0.2 , anchor="center")
            #BANCO_DE_DADOS
        self.txt_matriculas = ctk.CTkTextbox(aba_matriculas, width=750, height=300)
        self.txt_matriculas.place(relx=0.5 , rely=0.5 , anchor="center")
            #EXCLUIR
        self.txt_exc_matriculas = ctk.CTkEntry(aba_matriculas,placeholder_text="Id para Excluir")
        self.txt_exc_matriculas.place(relx=0.5 + 0.1 , rely=0.85 , anchor="center")
        ctk.CTkButton(aba_matriculas, text="Excluir" , command=self.deletar_matricula).place(relx=0.5 + 0.22, rely=0.85 , anchor="center")
            #ADICIONAR
        ctk.CTkButton(aba_matriculas, text="Adicionar Matrícula", command=self.adicionar_matricula).place(relx=0.5 -0.21 , rely=0.85 , anchor="center")
            #LISTAR
        ctk.CTkButton(aba_matriculas, text="Listar Matrículas", command=self.listar_matriculas).place(relx=0.5 -0.05 , rely=0.85 , anchor="center")
            #ATUALIZAR
        ctk.CTkButton(aba_matriculas, text="Atualizar", command=self.popup_atualizar_matricula).place(relx=0.07, rely=0.5)

        # ABA IBGE
        ctk.CTkLabel(
            aba_ibge,
            text="Consulta de municipios por UF - API publica do IBGE",
            font=("Arial", 20, "bold")
        ).place(relx=0.5, rely=0.14, anchor="center")

        self.ibge_uf = ctk.CTkEntry(aba_ibge, placeholder_text="UF (ex: SP)", width=160)
        self.ibge_uf.place(relx=0.43, rely=0.25, anchor="center")

        ctk.CTkButton(
            aba_ibge,
            text="Buscar Municipios",
            command=self.buscar_municipios_ibge
        ).place(relx=0.58, rely=0.25, anchor="center")

        self.txt_ibge = ctk.CTkTextbox(aba_ibge, width=750, height=350)
        self.txt_ibge.place(relx=0.5, rely=0.58, anchor="center")
        

    # FUNÇÕES DE CADA ABA

    #FUNÇÕES CURSO
    
    def adicionar_curso(self):
        try:
            nome = self.validador.validar_texto_nao_vazio(self.curso_nome.get(), "Nome do curso")
            duracao = self.validador.validar_duracao_curso(self.curso_duracao.get())
            
            inserir_curso(nome, duracao)
            self.notificador.sucesso(f"Curso '{nome}' adicionado com sucesso!")
            self.listar_cursos()
            self.curso_nome.delete(0, 'end')
            self.curso_duracao.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao adicionar curso: {str(e)}")

    def listar_cursos(self):
        try:
            self.txt_cursos.delete("1.0", "end")
            cursos = listar_cursos()
            
            if not cursos:
                self.txt_cursos.insert("end", "Nenhum curso cadastrado.")
                return
            
            for c in cursos:
                self.txt_cursos.insert("end", f"ID: {c[0]} | Nome: {c[1]} | Duração: {c[2]} semestres\n")
        except Exception as e:
            self.notificador.erro(f"Erro ao listar cursos: {str(e)}")
            self.txt_cursos.delete("1.0", "end")
            self.txt_cursos.insert("end", f"Erro ao recuperar dados: {str(e)}")
            
    def popup_atualizar_curso(self):
        try:
            popup = ctk.CTkToplevel(self)
            popup.title("Atualizar Curso")
            popup.geometry("400x300")
            popup.resizable(False , False)

            id_entry = ctk.CTkEntry(popup, placeholder_text="ID do Curso")
            id_entry.pack(pady=10)

            nome_entry = ctk.CTkEntry(popup, placeholder_text="Nome")
            nome_entry.pack(pady=10)

            dur_entry = ctk.CTkEntry(popup, placeholder_text="Duração (semestres)")
            dur_entry.pack(pady=10)

            def salvar():
                try:
                    id_curso = self.validador.validar_inteiro(id_entry.get(), "ID do curso", minimo=1)
                    nome = self.validador.validar_texto_nao_vazio(nome_entry.get(), "Nome do curso")
                    duracao = self.validador.validar_duracao_curso(dur_entry.get())
                    
                    atualizar_curso(id_curso, nome, duracao)
                    self.notificador.sucesso(f"Curso ID {id_curso} atualizado com sucesso!")
                    popup.destroy()
                    self.listar_cursos()
                except ValueError as e:
                    self.notificador.erro(str(e))
                except Exception as e:
                    self.notificador.erro(f"Erro ao atualizar curso: {str(e)}")

            ctk.CTkButton(popup, text="Salvar", command=salvar).pack(pady=10)
        except Exception as e:
            self.notificador.erro(f"Erro ao abrir janela de atualização: {str(e)}")

    def deletar_curso(self):
        try:
            id_curso = self.validador.validar_inteiro(self.txt_exc_curso.get(), "ID do curso", minimo=1)
            excluir_curso(id_curso)
            self.notificador.sucesso(f"Curso ID {id_curso} deletado com sucesso!")
            self.listar_cursos()
            self.txt_exc_curso.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao deletar curso: {str(e)}")

    #FUNÇÕES ALUNO
    def adicionar_aluno(self):
        try:
            nome = self.validador.validar_texto_nao_vazio(self.aluno_nome.get(), "Nome do aluno")
            cpf = self.validador.validar_cpf(self.aluno_cpf.get())
            data = self.validador.validar_data_nascimento(self.aluno_data.get())
            data_formatada = formatar_data_nascimento(data)
            id_curso = self.validador.validar_inteiro(self.aluno_curso.get(), "ID do curso", minimo=1)
            
            inserir_aluno(nome, cpf, data_formatada, id_curso)
            self.notificador.sucesso(f"Aluno '{nome}' adicionado com sucesso!")
            self.listar_alunos()
            self.aluno_nome.delete(0, 'end')
            self.aluno_cpf.delete(0, 'end')
            self.aluno_data.delete(0, 'end')
            self.aluno_curso.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao adicionar aluno: {str(e)}")

    def listar_alunos(self):
        try:
            alunos = listar_alunos()
            self.txt_alunos.delete("1.0", "end")
            
            if not alunos:
                self.txt_alunos.insert("end", "Nenhum aluno cadastrado.")
                return
            
            for a in alunos:
                self.txt_alunos.insert("end", f"ID: {a[0]} | Nome: {a[1]} | CPF: {a[2]} | Curso: {a[4]}\n")
        except Exception as e:
            self.notificador.erro(f"Erro ao listar alunos: {str(e)}")
            self.txt_alunos.delete("1.0", "end")
            self.txt_alunos.insert("end", f"Erro ao recuperar dados: {str(e)}")
            
    def popup_atualizar_aluno(self):
        try:
            popup = ctk.CTkToplevel(self)
            popup.geometry("400x350")
            popup.title("Atualizar Aluno")

            id_entry = ctk.CTkEntry(popup, placeholder_text="ID do Aluno")
            id_entry.pack(pady=10)

            nome_entry = ctk.CTkEntry(popup, placeholder_text="Nome")
            nome_entry.pack(pady=10)

            cpf_entry = ctk.CTkEntry(popup, placeholder_text="CPF (apenas números)")
            cpf_entry.pack(pady=10)

            data_entry = ctk.CTkEntry(popup, placeholder_text="Data Nasc (DDMMYYYY)")
            data_entry.pack(pady=10)

            curso_entry = ctk.CTkEntry(popup, placeholder_text="ID Curso")
            curso_entry.pack(pady=10)

            def salvar():
                try:
                    id_aluno = self.validador.validar_inteiro(id_entry.get(), "ID do aluno", minimo=1)
                    nome = self.validador.validar_texto_nao_vazio(nome_entry.get(), "Nome do aluno")
                    cpf = self.validador.validar_cpf(cpf_entry.get())
                    data = self.validador.validar_data_nascimento(data_entry.get())
                    data_formatada = formatar_data_nascimento(data)
                    id_curso = self.validador.validar_inteiro(curso_entry.get(), "ID do curso", minimo=1)
                    
                    atualizar_aluno(id_aluno, nome, cpf, data_formatada, id_curso)
                    self.notificador.sucesso(f"Aluno ID {id_aluno} atualizado com sucesso!")
                    popup.destroy()
                    self.listar_alunos()
                except ValueError as e:
                    self.notificador.erro(str(e))
                except Exception as e:
                    self.notificador.erro(f"Erro ao atualizar aluno: {str(e)}")

            ctk.CTkButton(popup, text="Salvar", command=salvar).pack(pady=10)
        except Exception as e:
            self.notificador.erro(f"Erro ao abrir janela de atualização: {str(e)}")

    def deletar_aluno(self):
        try:
            id_aluno = self.validador.validar_inteiro(self.txt_exc_aluno.get(), "ID do aluno", minimo=1)
            excluir_aluno(id_aluno)
            self.notificador.sucesso(f"Aluno ID {id_aluno} deletado com sucesso!")
            self.listar_alunos()
            self.txt_exc_aluno.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao deletar aluno: {str(e)}")
    
    # FUNÇÕES FUNCIONARIOS
    
    def adicionar_funcionario(self):
        try:
            nome = self.validador.validar_texto_nao_vazio(self.func_nome.get(), "Nome do funcionário")
            cargo = self.validador.validar_texto_nao_vazio(self.func_cargo.get(), "Cargo")
            salario = self.validador.validar_salario(self.func_salario.get())
            
            inserir_funcionario(nome, cargo, salario)
            self.notificador.sucesso(f"Funcionário '{nome}' adicionado com sucesso!")
            self.listar_funcionarios()
            self.func_nome.delete(0, 'end')
            self.func_cargo.delete(0, 'end')
            self.func_salario.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao adicionar funcionário: {str(e)}")

    def listar_funcionarios(self):
        try:
            funcionarios = listar_funcionarios()
            self.txt_funcionarios.delete("1.0", "end")
            
            if not funcionarios:
                self.txt_funcionarios.insert("end", "Nenhum funcionário cadastrado.")
                return
            
            for f in funcionarios:
                self.txt_funcionarios.insert("end", f"ID: {f[0]} | Nome: {f[1]} | Cargo: {f[2]} | Salário: R${f[3]:.2f}\n")
        except Exception as e:
            self.notificador.erro(f"Erro ao listar funcionários: {str(e)}")
            self.txt_funcionarios.delete("1.0", "end")
            self.txt_funcionarios.insert("end", f"Erro ao recuperar dados: {str(e)}")
            
    def popup_atualizar_funcionario(self):
        try:
            popup = ctk.CTkToplevel(self)
            popup.title("Atualizar Funcionário")
            popup.geometry("400x300")

            id_entry = ctk.CTkEntry(popup, placeholder_text="ID Funcionário")
            id_entry.pack(pady=10)

            nome_entry = ctk.CTkEntry(popup, placeholder_text="Nome")
            nome_entry.pack(pady=10)

            cargo_entry = ctk.CTkEntry(popup, placeholder_text="Cargo")
            cargo_entry.pack(pady=10)

            sal_entry = ctk.CTkEntry(popup, placeholder_text="Salário (ex: 3500.00)")
            sal_entry.pack(pady=10)

            def salvar():
                try:
                    id_func = self.validador.validar_inteiro(id_entry.get(), "ID do funcionário", minimo=1)
                    nome = self.validador.validar_texto_nao_vazio(nome_entry.get(), "Nome do funcionário")
                    cargo = self.validador.validar_texto_nao_vazio(cargo_entry.get(), "Cargo")
                    salario = self.validador.validar_salario(sal_entry.get())
                    
                    atualizar_funcionario(id_func, nome, cargo, salario)
                    self.notificador.sucesso(f"Funcionário ID {id_func} atualizado com sucesso!")
                    popup.destroy()
                    self.listar_funcionarios()
                except ValueError as e:
                    self.notificador.erro(str(e))
                except Exception as e:
                    self.notificador.erro(f"Erro ao atualizar funcionário: {str(e)}")

            ctk.CTkButton(popup, text="Salvar", command=salvar).pack(pady=10)
        except Exception as e:
            self.notificador.erro(f"Erro ao abrir janela de atualização: {str(e)}")
            
    def deletar_funcionario(self):
        try:
            id_func = self.validador.validar_inteiro(self.txt_exc_funcionario.get(), "ID do funcionário", minimo=1)
            excluir_funcionario(id_func)
            self.notificador.sucesso(f"Funcionário ID {id_func} deletado com sucesso!")
            self.listar_funcionarios()
            self.txt_exc_funcionario.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao deletar funcionário: {str(e)}")

    # FUNÇÕES MATERIA
    
    def adicionar_materia(self):
        try:
            nome = self.validador.validar_texto_nao_vazio(self.materia_nome.get(), "Nome da matéria")
            id_curso = self.validador.validar_inteiro(self.materia_curso.get(), "ID do curso", minimo=1)
            
            inserir_materia(nome, id_curso)
            self.notificador.sucesso(f"Matéria '{nome}' adicionada com sucesso!")
            self.listar_materias()
            self.materia_nome.delete(0, 'end')
            self.materia_curso.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao adicionar matéria: {str(e)}")

    def listar_materias(self):
        try:
            materias = listar_materias()
            self.txt_materias.delete("1.0", "end")
            
            if not materias:
                self.txt_materias.insert("end", "Nenhuma matéria cadastrada.")
                return
            
            for m in materias:
                self.txt_materias.insert("end", f"ID: {m[0]} | Matéria: {m[1]} | Curso: {m[2]}\n")
        except Exception as e:
            self.notificador.erro(f"Erro ao listar matérias: {str(e)}")
            self.txt_materias.delete("1.0", "end")
            self.txt_materias.insert("end", f"Erro ao recuperar dados: {str(e)}")
            
    def popup_atualizar_materia(self):
        try:
            popup = ctk.CTkToplevel(self)
            popup.title("Atualizar Matéria")
            popup.geometry("400x300")

            id_entry = ctk.CTkEntry(popup, placeholder_text="ID Matéria")
            id_entry.pack(pady=10)

            nome_entry = ctk.CTkEntry(popup, placeholder_text="Nome")
            nome_entry.pack(pady=10)

            curso_entry = ctk.CTkEntry(popup, placeholder_text="ID Curso")
            curso_entry.pack(pady=10)

            def salvar():
                try:
                    id_materia = self.validador.validar_inteiro(id_entry.get(), "ID da matéria", minimo=1)
                    nome = self.validador.validar_texto_nao_vazio(nome_entry.get(), "Nome da matéria")
                    id_curso = self.validador.validar_inteiro(curso_entry.get(), "ID do curso", minimo=1)
                    
                    atualizar_materia(id_materia, nome, id_curso)
                    self.notificador.sucesso(f"Matéria ID {id_materia} atualizada com sucesso!")
                    popup.destroy()
                    self.listar_materias()
                except ValueError as e:
                    self.notificador.erro(str(e))
                except Exception as e:
                    self.notificador.erro(f"Erro ao atualizar matéria: {str(e)}")

            ctk.CTkButton(popup, text="Salvar", command=salvar).pack(pady=10)
        except Exception as e:
            self.notificador.erro(f"Erro ao abrir janela de atualização: {str(e)}")
            
    def deletar_materia(self):
        try:
            id_materia = self.validador.validar_inteiro(self.txt_exc_materias.get(), "ID da matéria", minimo=1)
            excluir_materia(id_materia)
            self.notificador.sucesso(f"Matéria ID {id_materia} deletada com sucesso!")
            self.listar_materias()
            self.txt_exc_materias.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao deletar matéria: {str(e)}")

    #FUNÇÕES MATRICULA
    
    def adicionar_matricula(self):
        try:
            id_aluno = self.validador.validar_inteiro(self.matricula_aluno.get(), "ID do aluno", minimo=1)
            id_materia = self.validador.validar_inteiro(self.matricula_materia.get(), "ID da matéria", minimo=1)
            semestre = self.validador.validar_texto_nao_vazio(self.matricula_semestre.get(), "Semestre")
            ano = self.validador.validar_inteiro(self.matricula_ano.get(), "Ano", minimo=1900)
            
            inserir_matricula(id_aluno, id_materia, semestre, ano)
            self.notificador.sucesso(f"Matrícula adicionada com sucesso!")
            self.listar_matriculas()
            self.matricula_aluno.delete(0, 'end')
            self.matricula_materia.delete(0, 'end')
            self.matricula_semestre.delete(0, 'end')
            self.matricula_ano.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao adicionar matrícula: {str(e)}")

    def listar_matriculas(self):
        try:
            matriculas = listar_matriculas()
            self.txt_matriculas.delete("1.0", "end")
            
            if not matriculas:
                self.txt_matriculas.insert("end", "Nenhuma matrícula cadastrada.")
                return
            
            for m in matriculas:
                self.txt_matriculas.insert("end", f"ID: {m[0]} | Aluno: {m[1]} | Matéria: {m[2]} | {m[3]} - {m[4]}\n")
        except Exception as e:
            self.notificador.erro(f"Erro ao listar matrículas: {str(e)}")
            self.txt_matriculas.delete("1.0", "end")
            self.txt_matriculas.insert("end", f"Erro ao recuperar dados: {str(e)}")
            
    def popup_atualizar_matricula(self):
        try:
            popup = ctk.CTkToplevel(self)
            popup.geometry("400x350")
            popup.title("Atualizar Matrícula")

            id_entry = ctk.CTkEntry(popup, placeholder_text="ID Matrícula")
            id_entry.pack(pady=10)

            aluno_entry = ctk.CTkEntry(popup, placeholder_text="ID Aluno")
            aluno_entry.pack(pady=10)

            mat_entry = ctk.CTkEntry(popup, placeholder_text="ID Matéria")
            mat_entry.pack(pady=10)

            sem_entry = ctk.CTkEntry(popup, placeholder_text="Semestre (ex: 1º, 2º, etc.)")
            sem_entry.pack(pady=10)

            ano_entry = ctk.CTkEntry(popup, placeholder_text="Ano (ex: 2025)")
            ano_entry.pack(pady=10)

            def salvar():
                try:
                    id_matricula = self.validador.validar_inteiro(id_entry.get(), "ID da matrícula", minimo=1)
                    id_aluno = self.validador.validar_inteiro(aluno_entry.get(), "ID do aluno", minimo=1)
                    id_materia = self.validador.validar_inteiro(mat_entry.get(), "ID da matéria", minimo=1)
                    semestre = self.validador.validar_texto_nao_vazio(sem_entry.get(), "Semestre")
                    ano = self.validador.validar_inteiro(ano_entry.get(), "Ano", minimo=1900)
                    
                    atualizar_matricula(id_matricula, id_aluno, id_materia, semestre, ano)
                    self.notificador.sucesso(f"Matrícula ID {id_matricula} atualizada com sucesso!")
                    popup.destroy()
                    self.listar_matriculas()
                except ValueError as e:
                    self.notificador.erro(str(e))
                except Exception as e:
                    self.notificador.erro(f"Erro ao atualizar matrícula: {str(e)}")

            ctk.CTkButton(popup, text="Salvar", command=salvar).pack(pady=10)
        except Exception as e:
            self.notificador.erro(f"Erro ao abrir janela de atualização: {str(e)}")

    def deletar_matricula(self):
        try:
            id_matricula = self.validador.validar_inteiro(self.txt_exc_matriculas.get(), "ID da matrícula", minimo=1)
            excluir_matricula(id_matricula)
            self.notificador.sucesso(f"Matrícula ID {id_matricula} deletada com sucesso!")
            self.listar_matriculas()
            self.txt_exc_matriculas.delete(0, 'end')
        except ValueError as e:
            self.notificador.erro(str(e))
        except Exception as e:
            self.notificador.erro(f"Erro ao deletar matrícula: {str(e)}")

    # FUNCAO API IBGE
    def buscar_municipios_ibge(self):
        try:
            uf = self.validador.validar_texto_nao_vazio(self.ibge_uf.get(), "UF").upper()
            
            if len(uf) != 2 or not uf.isalpha():
                raise ValueError("UF deve ter 2 letras (ex: SP, RJ, MG)")
            
            self.txt_ibge.delete("1.0", "end")
            self.notificador.info(f"Buscando municipios para {uf}...")
            
            municipios = buscar_municipios_por_uf(uf)
            
            self.txt_ibge.insert("end", f"Municipios encontrados para {uf}:\n\n")
            for municipio in municipios:
                self.txt_ibge.insert("end", f"- {municipio}\n")
            
            self.notificador.sucesso(f"{len(municipios)} municipios encontrados para {uf}!")
        except ValueError as e:
            self.notificador.erro(str(e))
            self.txt_ibge.delete("1.0", "end")
            self.txt_ibge.insert("end", f"Erro de validação: {str(e)}\n")
        except IBGEApiError as e:
            self.notificador.erro(f"Erro na API do IBGE: {str(e)}")
            self.txt_ibge.delete("1.0", "end")
            self.txt_ibge.insert("end", f"Erro ao consultar API: {str(e)}\n")
        except Exception as e:
            self.notificador.erro(f"Erro ao buscar municipios: {str(e)}")
            self.txt_ibge.delete("1.0", "end")
            self.txt_ibge.insert("end", f"Erro: {str(e)}\n")
        
    #DEF ALTERAR TEMA (MODO ESCURO)
    def alterar_tema(self):
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("dark")
            self.switch_tema.configure(text="Modo Escuro")
        else:
            ctk.set_appearance_mode("light")
            self.switch_tema.configure(text="Modo Claro")

# EXECUÇÃO

if __name__ == "__main__":
    app = UniversidadeApp()
    app.mainloop()
