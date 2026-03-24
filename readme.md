# Sistema de Gestão - Casa de Apoio (API & Dashboard)

Projeto desenvolvido como resolução do desafio técnico para estruturação e evolução de uma API Django para gestão de uma casa de apoio. O foco foi atualizar dependências, documentar endpoints, criar um dashboard MVT e implementar melhorias focadas na integridade e extração de dados.

---

## Entregas do Desafio

- [x] **1. Deploy Local:** Configuração refatorada para rodar exclusivamente via Docker Compose.
- [x] **2. Atualização de Bibliotecas:** Dependências do `requirements.txt` atualizadas.
- [x] **3. Documentação da API:** Implementada utilizando `drf-spectacular` (Swagger).
- [x] **4 e 5. Implementação de 3 Melhorias Técnicas:** Descritas na seção abaixo.
- [x] **6. Refatoração de Seeds:** Banco de dados populado via fixtures nativas do Django.
- [x] **7. Dashboard (MVT):** Dashboard interativo construído com Server-Side Rendering (SSR), Bootstrap 5 e Chart.js, acessível via `/dashboard/`.

---

## Melhorias Implementadas

Para garantir a confiabilidade dos dados e facilitar a prestação de contas da casa de apoio, desenvolvi as seguintes melhorias na arquitetura e nas regras de negócio:

1. **Prevenção de Duplicidade (Trava de Check-in):** Implementação de validação na camada de Models/Views que impede a criação de um novo check-in se a pessoa já possuir uma estadia ativa (`active=True`), garantindo a consistência da ocupação.
2. **Soft Delete (Exclusão Lógica):** Arquitetura de banco de dados modificada para interceptar o método `.delete()`. Registros deletados têm a flag `is_deleted=True` ativada e são ocultados via Custom Manager (`QuerySet`), preservando o histórico para auditorias.
3. **Exportação de Relatórios CSV:** Criação de uma `admin.action` customizada no Django Admin para permitir o download rápido e formatado da listagem de check-ins em planilhas (`.csv`).

**Melhorias Complementares (UX/DX):**
* Bloqueio *readonly* no painel Admin que impede a reativação acidental de check-ins já finalizados.
* Auto-preenchimento via parâmetros GET: Clicar em "Check-out" no Dashboard encaminha o usuário para o Admin com o formulário já preenchido.
* Inclusão de campos de busca (`search_fields`) otimizados e textos de ajuda (`search_help_text`) nas telas do Django Admin, guiando o usuário de forma clara e intuitiva na navegação do sistema.
* Criação de um `Makefile` para orquestrar o ambiente Docker.

---

## Tecnologias Utilizadas

* **Backend:** Python 3.10, Django, Django REST Framework (DRF)
* **Banco de Dados:** PostgreSQL
* **Infraestrutura:** Docker, Docker Compose, Make
* **Frontend:** HTML5, Bootstrap 5, Chart.js, Bootstrap Icons
* **Qualidade:** Pytest, Flake8, Coverage

---

## Como rodar o projeto localmente

Pensando na diversidade de ambientes operacionais, disponibilizo duas formas de executar o projeto: **Via Docker (Recomendado e Automatizado)** ou **Nativamente (Python/Venv)**. O código-fonte é o mesmo para ambas as abordagens.

---

### Opção A: Execução via Docker (Recomendado)
Ideal para quem deseja subir a aplicação e o banco de dados em segundos, sem instalar dependências no sistema operacional.

**Pré-requisitos por Sistema Operacional:**
* **Windows / WSL2:** Instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/). Certifique-se de ir em *Settings > Resources > WSL Integration* e ativar a chave do Ubuntu (ou sua distro).
* **Linux (Ubuntu/Debian):** Instale o Docker Engine e o Docker Compose. Adicione seu usuário ao grupo do docker (`sudo usermod -aG docker $USER`) para conseguir rodar os comandos sem a necessidade de `sudo`.

**Passo a passo:**
1. Abra o terminal na raiz do projeto e execute o comando abaixo. Ele fará o build da imagem, subirá o banco PostgreSQL, aplicará as migrações e populará o banco com os dados iniciais de teste (seeds):
   ```bash
   make setup
   ```
   *(Nota: Se o seu terminal não reconhecer o `make`, execute manualmente: `docker-compose up -d` seguido de `docker-compose exec web python manage.py migrate` e a injeção dos arquivos json de seed).*

2. Crie seu usuário administrador com o comando:
   ```bash
   make createsuperuser
   ```

---

### Opção B: Execução Nativa (Sem Docker / Venv)
Ideal para quem prefere rodar o projeto diretamente no sistema, utilizando o ambiente virtual padrão do Python e o banco SQLite (para desenvolvimento).

**Passo a passo:**
1. Certifique-se de ter o **Python 3.10+** instalado em sua máquina.
2. Na raiz do projeto, crie e ative um ambiente virtual:
   ```bash
   # No Windows (CMD/PowerShell)
   python -m venv venv
   venv\Scripts\activate

   # No Linux / Mac / WSL
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```
4. Aplique as migrações no banco de dados:
   ```bash
   python manage.py migrate
   ```
5. Popule o banco com os dados de teste (Seeds):
   ```bash
   python manage.py loaddata people/seed/1_pessoas.json
   python manage.py loaddata people/seed/2_checkins.json
   python manage.py loaddata people/seed/3_servicos.json
   ```
6. Crie um usuário para acessar os painéis:
   ```bash
   python manage.py createsuperuser
   ```
7. Inicie o servidor local:
   ```bash
   python manage.py runserver
   ```

---

### Acessando a Aplicação
Independente do método escolhido (Docker ou Nativo), o servidor estará rodando na porta `8000`. Acesse as rotas abaixo no seu navegador:

* **Dashboard Gerencial:** [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
* **Painel Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **Documentação Mapeada (Swagger):** [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)

---
*Desenvolvido por Kaylane Raquel.*