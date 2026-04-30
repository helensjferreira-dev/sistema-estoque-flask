
🇧🇷 [Português](#-português) | 🇺🇸 [English](#-english)

---

## 🇧🇷 Português

# 💼 Sistema de Gestão de Estoque e Validade

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)

Sistema web completo para controle de estoque, movimentações e validade de produtos, desenvolvido com Python, Flask e MySQL.

A aplicação simula um ambiente real de gestão para clínicas de estética, permitindo controle rigoroso de entradas e saídas, rastreabilidade por lotes e geração de relatórios gerenciais.

---

## 🚀 Demonstração

🔗 Acesse a aplicação:
(Deploy em andamento. O link será disponibilizado em breve.)

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

(INSERIR PRINT. As imagens da interface serão adicionadas após a refatoração do layout para versão profissional.)

### 📊 Dashboard / Relatórios

(INSERIR PRINT. As imagens da interface serão adicionadas após a refatoração do layout para versão profissional.)

### 📦 Movimentações

(INSERIR PRINT. As imagens da interface serão adicionadas após a refatoração do layout para versão profissional.)

### 📈 Relatório de Estoque

(INSERIR PRINT. As imagens da interface serão adicionadas após a refatoração do layout para versão profissional.)

### ⏳ Controle de Validade

(INSERIR PRINT. As imagens da interface serão adicionadas após a refatoração do layout para versão profissional.)

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

O sistema foi organizado em camadas para garantir separação de responsabilidades, facilitando manutenção, escalabilidade e clareza do código.

```bash
sistema-estoque-flask/
│
├── models/        # Representação das entidades do banco de dados
├── routes/        # Definição das rotas e controle das requisições (controllers)
├── services/      # Camada de regras de negócio e lógica da aplicação
├── templates/     # Interfaces HTML renderizadas com Jinja2
├── static/        # Arquivos estáticos (CSS, JavaScript)
├── util/          # Funções auxiliares (autenticação, SQL builder)
├── database/      # Arquivos relacionados ao banco de dados
│   ├── schema.sql          # criação das tabelas
│   ├── legacy_script.sql   # consultas e dados em refatoração
│   └── init_db.py          # script Python para inicializar o banco de dados
│
├── app.py         # Ponto de entrada da aplicação
```
### 🔍 Organização das Camadas

* **Models:** representam as entidades do sistema e estrutura dos dados
* **Routes:** responsáveis por receber requisições HTTP e direcionar para a lógica apropriada
* **Services:** concentram as regras de negócio, mantendo a aplicação organizada e desacoplada
* **Templates:** responsáveis pela renderização das páginas HTML
* **Static:** contém arquivos de estilo e scripts do frontend
* **Util:** funções auxiliares reutilizáveis, como autenticação e construção de queries


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

### 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## 🇺🇸 English

# 💼 Inventory and Expiration Management System

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge\&logo=python\&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge\&logo=flask\&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge\&logo=mysql\&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge\&logo=javascript\&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge\&logo=html5\&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge\&logo=css3\&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge\&logo=chart.js\&logoColor=white)

A complete web application for inventory management, stock movements, and product expiration control, developed with Python, Flask, and MySQL.

The system simulates a real-world business environment for beauty clinics, enabling strict control over stock entries and exits, batch traceability, and the generation of managerial reports.

---

## 🚀 Demo

🔗 Access the application:
(Deployment in progress. The link will be available soon.)

---

## 🧠 Business Rules

* Stock **cannot be manually adjusted** — all changes must be performed through recorded movements
* Each movement automatically updates product stock levels
* Batch-based expiration tracking with remaining days calculation
* Automatic alerts for:

  * Expired batches
  * Batches close to expiration (≤ 30 days)
  * Products below minimum stock level
* Full traceability by user

---

## 📸 Interface

### 🔐 Login

(Screenshots will be added after UI refactoring.)

### 📊 Dashboard / Reports

(Screenshots will be added after UI refactoring.)

### 📦 Movements

(Screenshots will be added after UI refactoring.)

### 📈 Inventory Report

(Screenshots will be added after UI refactoring.)

### ⏳ Expiration Control

(Screenshots will be added after UI refactoring.)

---

## ⚙️ Features

### 🔐 Authentication

* Session-based login
* Password hashing
* Restricted user access

### 📦 Inventory Management

* Product registration with minimum stock control
* Category and supplier management
* Batch management with expiration tracking

### 🔄 Stock Movements

* Entry and exit registration
* Automatic stock updates
* User tracking for each movement
* Full audit history

### 📊 Reports

* Inventory report with visual status (OK / Low / Out of stock)
* Movement report with advanced filters
* Expiration report for monitoring product shelf life
* Export options:

  * PDF
  * Excel
  * CSV

### 📈 Data Visualization

* Interactive charts using Chart.js
* Management indicators for stock control
* Comparison between current and minimum stock levels

---

## 🧱 Project Architecture

The system is structured in layers to ensure clear separation of concerns, improving maintainability, scalability, and code readability.

```bash
sistema-estoque-flask/
│
├── models/        # Database entities representation
├── routes/        # Route definitions and request handling (controllers)
├── services/      # Business logic layer
├── templates/     # HTML templates rendered with Jinja2
├── static/        # Static files (CSS, JavaScript)
├── util/          # Helper utilities (authentication, SQL builder)
├── database/      # Database structure and initialization
│   ├── schema.sql          # database schema (table creation)
│   ├── legacy_script.sql   # temporary queries and data under refactoring
│   └── init_db.py          # Python script to initialize the database
│
├── app.py         # Application entry point
```

### 🔍 Layer Organization

* **Models:** represent system entities and data structure
* **Routes:** handle HTTP requests and delegate actions to the appropriate logic
* **Services:** contain business rules, keeping the application organized and decoupled
* **Templates:** responsible for rendering HTML views
* **Static:** stores frontend assets such as styles and scripts
* **Util:** reusable helper functions, such as authentication and query building


---

## 🛠️ Technologies

**Backend**

* Python 3
* Flask

**Database**

* MySQL

**Frontend**

* HTML5
* CSS3
* JavaScript
* Jinja2

**Libraries**

* Flask-Session
* mysql-connector-python
* ReportLab (PDF generation)
* XlsxWriter / OpenPyXL (Excel)
* Chart.js

---

## ▶️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/helensjferreira-dev/sistema-estoque-flask.git
cd sistema-estoque-flask
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

* Create a MySQL database
* Run script.sql
* Update credentials in the project

### 5. Run the application

```bash
python app.py
```

---

## 📌 Future Improvements

* REST API implementation
* JWT-based authentication
* Cloud deployment
* Docker containerization
* Automated testing
* Frontend refactoring with modern framework

---

### 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 👩‍💻 Author / Autora

Desenvolvido por Hélen Ferreira  
🔗 LinkedIn: https://linkedin.com/in/helensjferreira-dev  
🔗 GitHub: https://github.com/helensjferreira-dev  
