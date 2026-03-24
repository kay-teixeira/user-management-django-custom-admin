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

Para otimizar o processo de building, todo o setup inicial foi automatizado.

### Requisitos Prévios
* **Docker** e **Docker Compose** instalados na máquina.
* Utilitário **Make** (Nativo no Linux/Mac; no Windows via WSL ou Git Bash).

### 1. Setup Simplificado (Via Make)
Na raiz do projeto, execute o comando abaixo. Ele fará o build das imagens, subirá o banco de dados, rodará as migrações e populará as tabelas com os dados de teste (fixtures):

```bash
make setup
```

*(Se precisar desligar a aplicação e limpar o banco de dados completamente, rode: `docker-compose down -v`)*

> **Não possui o utilitário `make`?** Execute os comandos manualmente:
> ```bash
> docker-compose up -d
> docker-compose exec web python manage.py migrate
> docker-compose exec web python manage.py loaddata people/seed/1_pessoas.json
> docker-compose exec web python manage.py loaddata people/seed/2_checkins.json
> docker-compose exec web python manage.py loaddata people/seed/3_servicos.json
> ```

### 2. Criação do Acesso Administrativo
Para acessar o painel de gestão, crie o seu usuário (será solicitado login, email e senha):

```bash
make createsuperuser
```

### 3. Acessando a Aplicação
Com os serviços em execução, acesse as seguintes rotas no navegador:

* **Dashboard Gerencial:** [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
* **Painel Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **Documentação (Swagger):** [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)

---
*Desenvolvido por Kaylane Raquel.*