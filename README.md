# CEUCRUD - Sistema de Gerenciamento Universitario

Deploy: https://lucasabrantes2006.github.io/Trabalho-Bootcamp-ll-Desafio---Entrega-Final/  
Repositorio: https://github.com/LucasAbrantes2006/Trabalho-Bootcamp-ll-Desafio---Entrega-Final.git

## Descricao do Projeto

O **CEUCRUD** e um sistema de gerenciamento universitario desenvolvido em **Python** com **CustomTkinter**, criado para realizar operacoes de cadastro, consulta, atualizacao e exclusao de dados academicos.

O projeto foi evoluido ao longo das etapas do bootcamp e, nesta entrega final, passou a contemplar:

- trabalho colaborativo em equipe com uso de **branches** e **Pull Requests**
- revisao de codigo entre integrantes
- integracao com **API publica do IBGE**
- persistencia de dados em **banco de dados em nuvem**
- manutencao de **testes automatizados**, **CI** e **deploy**

## Integrantes da Equipe

- Lucas Abrantes
- Eduardo Rocha
- Yuri Bolis
- Daniel Scartezini
- Guilherme Soato

## Objetivo da Entrega Final

Esta etapa tem como foco demonstrar a capacidade da equipe de colaborar em um mesmo repositorio sem comprometer a estabilidade do sistema, aplicando boas praticas de desenvolvimento, versionamento, revisao de codigo, integracao continua e documentacao.

## Funcionalidades do Sistema

O sistema permite o gerenciamento das seguintes entidades academicas:

- Cursos
- Alunos
- Funcionarios
- Materias
- Matriculas

Operacoes disponiveis:

- Adicionar registros
- Listar registros
- Atualizar registros
- Excluir registros

Funcionalidade extra integrada:

- Consulta de municipios por UF utilizando a **API publica de Localidades do IBGE**

## Banco de Dados

A aplicacao utiliza um banco de dados **MySQL** com estrutura definida no arquivo `bd_universidade.sql`.

Nesta entrega final, a aplicacao foi adaptada para trabalhar com **configuracao por variaveis de ambiente**, facilitando a conexao com um **banco de dados em nuvem** e evitando expor credenciais diretamente no codigo-fonte.

Banco utilizado pela equipe:

- Provedor: TiDB Cloud
- Tecnologia: MySQL
- Tipo de persistencia: remota/em nuvem

## API Externa Utilizada

A aplicacao consome a API publica do IBGE para consultar municipios a partir da sigla de um estado brasileiro.

Endpoint utilizado:

```text
https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios
Exemplo:
https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios
Tecnologias Utilizadas
Python 3
CustomTkinter
MySQL
mysql-connector-python
API publica do IBGE
unittest
pytest
GitHub Actions
GitHub Pages
TiDB Cloud
Estrutura do Projeto
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── ISSUE_ENTREGA_INTERMEDIARIA.md
│   └── index.html
├── tests/
│   ├── test_api_ibge.py
│   └── test_database.py
├── api_ibge.py
├── bd_universidade.sql
├── database.py
├── main.py
├── requirements.txt
├── roxo_theme.json
├── .env.example
└── README.md
Configuracao do Ambiente
1. Clonar o repositorio
git clone https://github.com/LucasAbrantes2006/Trabalho-Bootcamp-ll-Desafio---Entrega-Final.git
cd Trabalho-Bootcamp-ll-Desafio---Entrega-Final
2. Criar e ativar ambiente virtual
No Windows:
python -m venv venv
venv\Scripts\activate
3. Instalar dependencias
pip install -r requirements.txt
4. Configurar variaveis de ambiente
Crie um arquivo .env com base no arquivo .env.example.
Exemplo:
DB_HOST=seu-host
DB_PORT=3306
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
DB_NAME=universidade
DB_TIMEOUT=10
DB_SSL_DISABLED=false
Configuracao do Banco
Execute o script SQL para criar a base inicial:
SOURCE bd_universidade.sql;
O script cria:
banco universidade
tabelas do sistema
relacionamentos
dados ficticios para testes
Como Executar a Aplicacao
Com as dependencias instaladas e o banco configurado, execute:
python main.py
Como Executar os Testes
Testes com unittest
python -m unittest discover -s tests
Testes com pytest
pytest tests/ -v
Os testes cobrem:
validacao da integracao com a API do IBGE
validacao da camada de banco com uso de mocks
seguranca da pipeline sem dependencia de credenciais reais
Integracao Continua
A pipeline de CI esta configurada com GitHub Actions no arquivo:
.github/workflows/ci.yml
A esteira realiza:
instalacao das dependencias
execucao de testes automatizados
validacao de integracao antes do merge
geracao de cobertura de testes
Deploy
O projeto possui pagina publicada em:
https://lucasabrantes2006.github.io/Trabalho-Bootcamp-ll-Desafio---Entrega-Final/
Caso a equipe utilize GitHub Pages, a publicacao pode ser feita a partir da pasta docs/.
Fluxo de Trabalho em Equipe
Para atender aos requisitos da entrega final, a equipe adotou o seguinte fluxo:
cada integrante trabalhou em sua propria branch
cada tarefa foi vinculada a uma issue
cada integrante abriu pelo menos 1 Pull Request
os PRs foram revisados por outro membro da equipe
o merge para a branch principal ocorreu apenas apos aprovacao e validacao da pipeline
Exemplo de fluxo Git:
git checkout -b feature/nome-da-tarefa
git add .
git commit -m "Descricao objetiva da alteracao"
git push -u origin feature/nome-da-tarefa
Depois disso:
abrir Pull Request para main
aguardar CI ficar verde
solicitar revisao de outro integrante
fazer merge apos aprovacao
Divisao Colaborativa da Equipe
A entrega foi organizada para garantir colaboracao real entre os membros, incluindo:
configuracao e integracao com banco em nuvem
refatoracao da camada de banco
validacoes e melhorias de interface
testes automatizados e pipeline CI
documentacao, deploy e organizacao final da entrega
Evidencias Esperadas no Repositorio
O professor podera validar a participacao individual por meio de:
historico de commits
branches criadas
Pull Requests abertos
revisoes realizadas
merges aprovados
atualizacao da branch principal com pipeline funcional
Documentacao da Entrega
Para a entrega na plataforma, o PDF do grupo deve conter:
nome completo de todos os integrantes
matricula de todos os integrantes
nome do projeto
breve descricao
link do repositorio publico
link da aplicacao publicada
Observacoes Importantes
As credenciais do banco nao devem ser enviadas para o repositorio.
O arquivo .env deve permanecer ignorado no Git.
O projeto foi mantido com foco em colaboracao, rastreabilidade e qualidade.
A pipeline deve permanecer funcional apos o merge na branch principal.
Licenca
Este projeto esta sob a licenca MIT.
