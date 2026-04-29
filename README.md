# Sistema de Gestão de Estoque para o Projeto Integrador II

Este projeto é uma aplicação web completa para gestão de estoque, desenvolvida em **Python** com **Flask**. O sistema foi projetado para controlar produtos, fornecedores, lotes e movimentações, com foco especial em produtos de estética/beleza, oferecendo relatórios detalhados e dashboards visuais.

## 📋 Funcionalidades

### 🔐 Autenticação e Usuários
* **Login Seguro:** Acesso restrito com hash de senhas.
* **Gestão de Usuários:** Cadastro e exclusão de utilizadores do sistema.

### 📦 Gestão de Estoque
* **Produtos:** Cadastro completo com controlo de stock mínimo e validade opcional.
* **Lotes:** Entrada de produtos por lotes, gerindo datas de validade e cadastro.
* **Movimentações:** Registo de entradas e saídas, com cálculo automático de valores e atualização de saldo.
* **Alertas:**
    * **Validade:** Destaque visual para lotes vencidos ou próximos do vencimento (≤ 30 dias).
    * **Stock Mínimo:** Alerta quando a quantidade atual é inferior ao mínimo definido.

### 📊 Relatórios e Dashboards
* **Relatório de Estoque:** Visão geral do inventário com gráficos (Chart.js) e indicadores de status.
* **Relatório de Validade:** Monitorização de produtos a expirar.
* **Exportação:** Geração de relatórios em **PDF**, **Excel** e **CSV**.

### 🗂️ Cadastros Auxiliares
* **Categorias:** Organização de produtos.
* **Fornecedores:** Gestão de contactos e parceiros.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Base de Dados:** MySQL
* **Frontend:** HTML5, CSS3, JavaScript
* **Bibliotecas Principais:**
    * `Flask-Cors`, `Flask-Session`
    * `mysql-connector-python`
    * `ReportLab` (PDFs)
    * `XlsxWriter` / `OpenPyXL` (Excel)
    * `Chart.js` (Gráficos)

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
* Python 3.x instalado.
* Servidor MySQL a correr.

### 2. Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/helensjferreira-dev/pi-estetica.git
   cd pi-estetica

