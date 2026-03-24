.DEFAULT_GOAL := help

#Development ───────────────────────────────────────────────────────────────

.PHONY: setup
setup: #Sobe o Docker, cria as tabelas e injeta os dados de teste
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata people/seed/1_pessoas.json
	docker-compose exec web python manage.py loaddata people/seed/2_checkins.json
	docker-compose exec web python manage.py loaddata people/seed/3_servicos.json
	@echo "=================================================================="
	@echo "✅ SETUP CONCLUÍDO! O banco está pronto e cheio de dados."
	@echo "👉 Próximo passo: rode 'make createsuperuser' para criar seu login."
	@echo "=================================================================="

.PHONY: up
up: #Sobe os containers em background
	docker-compose up -d

.PHONY: down
down: #Derruba os containers e a rede (use 'docker-compose down -v' para limpar o banco)
	docker-compose down

.PHONY: logs
logs: #Mostra os logs do backend em tempo real
	docker-compose logs -f web

#Django management ─────────────────────────────────────────────────────────

.PHONY: makemigrations
makemigrations: #Cria novas migrações baseadas nas models
	docker-compose exec web python manage.py makemigrations

.PHONY: migrate
migrate: #Roda as migrações no banco de dados
	docker-compose exec web python manage.py migrate

.PHONY: createsuperuser
createsuperuser: #Cria um usuário administrador
	docker-compose exec web python manage.py createsuperuser

.PHONY: shell
shell: #Abre o shell interativo do Django
	docker-compose exec web python manage.py shell

#Code quality & Testing ────────────────────────────────────────────────────

.PHONY: test
test: #Roda a suíte de testes automatizados com pytest
	docker-compose exec web pytest

.PHONY: lint
lint: #Verifica a formatação do código usando flake8
	docker-compose exec web flake8 .

#Utilities ─────────────────────────────────────────────────────────────────

.PHONY: help
help: #Mostra os comandos disponíveis
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)