# 💼 Sistema de Gestão de Estoque e Validade

Sistema web completo para controle de estoque, movimentações e validade de produtos, desenvolvido com Python, Flask e MySQL.

A aplicação simula um ambiente real de gestão para clínicas de estética, permitindo controle rigoroso de entradas e saídas, rastreabilidade por lotes e geração de relatórios gerenciais.

---

## 🚀 Demonstração

🔗 Acesse a aplicação:
(INSERIR LINK DO DEPLOY)

---

## 🧠 Regras de Negócio Implementadas

* O estoque **não pode ser alterado manualmente** — todas as mudanças ocorrem exclusivamente por movimentações
* Cada movimentação impacta automaticamente o saldo dos produtos
* Controle de validade por lote, com cálculo de dias restantes
* Alertas automáticos para:

  * Lotes vencidos
  * Lotes próximos do vencimento (≤ 30 dias)
  * Produtos abaixo do estoque mínimo
* Rastreamento completo por usuário

---

## 📸 Interface do Sistema

### 🔐 Login

(INSERIR PRINT)

### 📊 Dashboard / Relatórios

(INSERIR PRINT)

### 📦 Movimentações

(INSERIR PRINT)

### 📈 Relatório de Estoque

(INSERIR PRINT)

### ⏳ Controle de Validade

(INSERIR PRINT)

---

## ⚙️ Funcionalidades

### 🔐 Autenticação

* Login com controle de sessão
* Senhas protegidas com hash
* Área restrita por usuário

### 📦 Gestão de Estoque

* Cadastro de produtos com estoque mínimo
* Controle de categorias e fornecedores
* Gestão de lotes com validade

### 🔄 Movimentações

* Registro de entradas e saídas
* Atualização automática do estoque
* Registro de usuário responsável
* Histórico completo para auditoria

### 📊 Relatórios

* Relatório de estoque com status visual (OK / Baixo / Em falta)
* Relatório de movimentações com filtros avançados
* Relatório de validade com análise de vencimento
* Exportação em:

  * PDF
  * Excel
  * CSV

### 📈 Visualização de Dados

* Gráficos interativos com Chart.js
* Indicadores gerenciais de estoque
* Comparativos entre estoque atual e mínimo

---

## 🧱 Arquitetura do Projeto

O sistema foi organizado em camadas para melhor separação de responsabilidades:

```bash
pi-estetica/
│
├── models/        # Representação das entidades do banco
├── routes/        # Camada de controle (rotas Flask)
├── services/      # Regras de negócio e lógica da aplicação
├── templates/     # Interfaces HTML (Jinja2)
├── static/        # Arquivos estáticos (CSS, JS)
├── util/          # Funções auxiliares (auth, SQL builder)
│
├── app.py         # Arquivo principal da aplicação
├── script.sql     # Script de criação do banco
```

---

## 🛠️ Tecnologias Utilizadas

**Backend**

* Python 3
* Flask

**Banco de Dados**

* MySQL

**Frontend**

* HTML5
* CSS3
* JavaScript
* Jinja2

**Bibliotecas**

* Flask-Session
* mysql-connector-python
* ReportLab (PDF)
* XlsxWriter / OpenPyXL (Excel)
* Chart.js

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/helensjferreira-dev/sistema-estoque-flask.git
cd sistema-estoque-flask
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar banco de dados

* Criar banco MySQL
* Executar script.sql
* Ajustar credenciais no projeto

### 5. Executar aplicação

```bash
python app.py
```

---

## 📌 Melhorias Futuras

* Implementação de API REST
* Autenticação com JWT
* Deploy em ambiente cloud
* Containerização com Docker
* Testes automatizados
* Refatoração do frontend com framework moderno

---

## 👩‍💻 Autora

Desenvolvido por Hélén Ferreira
🔗 LinkedIn: https://linkedin.com/in/helensjferreira-dev
🔗 GitHub: https://github.com/helensjferreira-dev
