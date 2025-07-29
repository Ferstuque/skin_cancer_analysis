# ==============================================================================
# Makefile para o Projeto de Análise de Câncer de Pele
#
# Regras de Uso:
#   make build      - Constrói a imagem Docker.
#   make run        - Executa a aplicação em um contêiner.
#   make stop       - Para o contêiner da aplicação.
#   make clean      - Remove a imagem Docker do projeto.
#   make all        - Executa 'build' e 'run' em sequência.
# ==============================================================================

# --- Variáveis (boa prática para evitar repetição) ---
IMAGE_NAME = skin-cancer-app
CONTAINER_PORT = 8501
HOST_PORT = 8501

# --- Regras Principais ---

# Alvo padrão, executado se você digitar apenas 'make'
.DEFAULT_GOAL := run

# Constrói a imagem Docker
build:
	@echo "🏗️  Construindo a imagem Docker '${IMAGE_NAME}'..."
	docker build -t $(IMAGE_NAME) .
	@echo "✅ Imagem construída com sucesso!"

# Executa o contêiner
run: build
	@echo "🚀 Executando a aplicacao na porta ${HOST_PORT}..."
	docker run --rm -p $(HOST_PORT):$(CONTAINER_PORT) $(IMAGE_NAME)

# Executa 'build' e 'run' em sequência
all: build run

# Para todos os contêineres baseados na nossa imagem
stop:
	@echo "🛑 Parando qualquer conteiner da aplicação em execucao..."
	-docker stop $(shell docker ps -a -q --filter ancestor=$(IMAGE_NAME))
	@echo "✅ Conteineres parados."

# Remove a imagem Docker
clean: stop
	@echo "🧹 Limpando a imagem Docker '${IMAGE_NAME}'..."
	-docker rmi $(IMAGE_NAME)
	@echo "✅ Imagem removida."

# Ajuda: exibe os comandos disponíveis
help:
	@echo ""
	@echo "Comandos disponíveis para o projeto:"
	@echo "-------------------------------------"
	@echo "make build      - Constrói a imagem Docker."
	@echo "make run        - Constrói (se necessário) e executa a aplicação."
	@echo "make stop       - Para o contêiner da aplicação."
	@echo "make clean      - Para o contêiner e remove a imagem Docker."
	@echo "make all        - Executa 'build' e 'run' em sequência."
	@echo ""

# Marcar alvos que não produzem arquivos para evitar conflitos
.PHONY: build run all stop clean help