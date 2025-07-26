# --- Estágio 1: Base ---
# Começamos com uma imagem oficial do Python. Usar uma versão específica é uma boa prática.
FROM python:3.10-slim

# --- Estágio 2: Configuração do Ambiente ---
# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# --- Estágio 3: Instalação das Dependências ---
# Copia o arquivo de dependências para o contêiner.
COPY requirements.txt .

# Instala todas as bibliotecas listadas no requirements.txt.
# O '--no-cache-dir' economiza espaço na imagem final.
RUN pip install --no-cache-dir -r requirements.txt

# --- Estágio 4: Copiando o Código da Aplicação ---
# Copia todo o conteúdo da pasta atual (onde está o Dockerfile) para o diretório de trabalho do contêiner.
COPY . .

# --- Estágio 5: Comando de Execução ---
# Expõe a porta que o Streamlit usa.
EXPOSE 8501

# O comando que será executado quando o contêiner iniciar.
# Ele inicia o dashboard Streamlit.
# O dashboard, por sua vez, fará chamadas para a API FastAPI.
# Para isso, precisamos rodar os dois serviços. A melhor forma é usar um script de inicialização.
# Vamos criar um `start.sh` para isso.

# Copia o script de inicialização e o torna executável
COPY start.sh .
RUN chmod +x start.sh

# Comando final para iniciar o contêiner
CMD ["./start.sh"]
