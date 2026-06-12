# Pull Request: Melhorias na Interface e Validações

## Descrição
Esta PR implementa melhorias significativas na interface do CEUCRUD e adiciona validações robustas para operações CRUD.

## Tipo de Mudança
- [x] Adição de novas funcionalidades
- [x] Melhoria na experiência do usuário
- [x] Refatoração de código

## Mudanças Principais

### 1. Sistema de Validações (ValidadorCampos)
- **Validação de CPF**: Verifica se contém exatamente 11 dígitos numéricos
- **Validação de Data**: Suporta formato DDMMYYYY com validação completa de data
- **Validação de Números**: Inteiros e decimais com limites personalizáveis
- **Validação de Salários**: Garante valores positivos e válidos
- **Validação de Duração de Curso**: Aceita valores entre 1 e 12 semestres
- **Validação de Texto**: Garante campos obrigatórios preenchidos

### 2. Sistema de Feedback Visual (NotificadorUso)
- **Mensagens de Sucesso** (verde): Confirmação de operações bem-sucedidas
- **Mensagens de Erro** (vermelho): Alertas com duração indefinida para leitura
- **Mensagens Informativas** (azul): Informações sobre operações em progresso
- Exibição em tempo real na interface
- Limpeza automática de mensagens após 3 segundos (exceto erros)

### 3. Tratamento de Exceções
- Try-except em todas as operações CRUD
- Mensagens de erro descritivas e amigáveis ao usuário
- Tratamento específico de erros do banco de dados
- Melhoria na exibição de erros no textbox

### 4. Melhorias por Módulo

#### Cursos
- Validação de nome não-vazio
- Validação de duração (1-12 semestres)
- Feedback visual em todas operações

#### Alunos
- Validação de CPF com 11 dígitos
- Validação de data de nascimento (DDMMYYYY)
- Validação de ID do curso
- Mensagens personalizadas por operação

#### Funcionários
- Validação de salário (positivo e numérico)
- Formatação de salário com 2 casas decimais (R$ X.XX)
- Validação de cargo não-vazio

#### Matérias
- Validação de nome não-vazio
- Validação de ID do curso

#### Matrículas
- Validação de semestre não-vazio
- Validação de ano (>= 1900)
- Validação de IDs de aluno e matéria

#### IBGE
- Validação de UF com 2 letras
- Tratamento específico de erros da API
- Exibição de quantidade de municipios encontrados

## Testes Realizados
- ✓ Validação de sintaxe Python (sem erros)
- ✓ Integração com banco de dados existente
- ✓ Funcionamento de todas operações CRUD
- ✓ Tratamento de erros e exceções

## Branch
- **Nome da Branch**: `guilherme`
- **Baseado em**: `main`

## Checklist
- [x] Código segue o padrão do projeto
- [x] Validações implementadas em todas operações
- [x] Feedback visual integrado
- [x] Tratamento de exceções completo
- [x] Sem erros de sintaxe Python
- [x] Compatível com código existente

## Screenshots/Demo
As mudanças incluem:
- Exibição de mensagens coloridas na parte inferior da janela
- Validação de entrada antes de qualquer operação
- Mensagens descritivas de erro em popup quando necessário
- Melhoria visual geral na experiência do usuário

## Notas Adicionais
- Todas as mudanças são backward-compatible
- Não altera a estrutura do banco de dados
- Melhora significativa na UX sem impacto na performance
