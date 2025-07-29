# 🩺 Análise Preditiva de Câncer de Pele com IA

![GitHub language count](https://img.shields.io/github/languages/count/Ferstuque/skin_cancer_analysis?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/Ferstuque/skin_cancer_analysis?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/Ferstuque/skin_cancer_analysis?style=for-the-badge)

Este projeto foi desenvolvido como entrega do **Tech Challenge** da **Pós-Graduação IA para Devs** da **FIAP - Faculdade de Tecnologia**.

## 🎯 Objetivo do Projeto

O desafio consistiu em desenvolver uma solução de Inteligência Artificial para apoiar equipes médicas no diagnóstico de lesões de pele, utilizando o dataset público **HAM10000**. Para isso, foram criados dois modelos distintos:

1.  **Modelo Tabular (XGBoost):** Um classificador de alta performance que prevê o risco de uma lesão ser **Melanoma** com base em dados clínicos do paciente (idade, sexo, localização da lesão).
2.  **Modelo de Visão Computacional (CNN):** Um classificador de imagem, baseado na arquitetura **ResNet50V2**, que identifica o tipo da lesão (entre 7 classes) diretamente da foto.

A solução final é uma **aplicação web interativa**, empacotada com Docker, que permite a interação com ambos os modelos.

---

## 🚀 Como Executar a Aplicação Web (Docker)

A maneira mais simples e recomendada de executar este projeto é através do Docker, que garante um ambiente consistente e sem a necessidade de instalar dependências manualmente.

### **Pré-requisitos**

1.  **Git:** Para clonar o repositório.
2.  **Docker Desktop:** Para construir e executar o contêiner da aplicação.
3.  **Make:**
    *   **Linux/MacOS:** Recurso padrão disponível no Linux.
    *   **Windows:** Recomenda-se o uso do **Git Bash** (que já inclui o `make`) ou a instalação do `make` via **Chocolatey** no PowerShell (`choco install make`).

### **Instruções de Execução**

Abra seu terminal preferido (Bash para Linux/Mac, Git Bash ou PowerShell com Make para Windows) e siga os passos:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Ferstuque/skin_cancer_analysis.git
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd skin_cancer_analysis
    ```

3.  **Construa a imagem e execute a aplicação com um único comando:**
    ```bash
    make run
    ```
    *Este comando irá construir a imagem Docker (pode levar alguns minutos na primeira vez) e, em seguida, iniciar o contêiner da aplicação.*

4.  **Acesse o Dashboard:**
    Abra seu navegador e acesse o seguinte endereço:
    👉 **http://localhost:8501**

### **Explorando o Dashboard**

A aplicação possui duas abas principais:

*   **📊 Simulador com Dados Clínicos (XGBoost)**
    Nesta aba, você pode interagir com o modelo de Machine Learning que prevê a probabilidade de um paciente apresentar um quadro de **Melanoma** ou **Não-Melanoma**. Basta preencher o formulário com as características do paciente e da lesão para obter uma análise de risco.

*   **🖼️ Análise de Imagem (CNN)**
    Aqui, você pode testar o modelo de Visão Computacional. Faça o upload de uma imagem (JPG, JPEG, PNG) de uma lesão de pele. Para melhores resultados, utilize uma imagem nítida e bem enquadrada. O modelo irá classificar a lesão em uma das 7 categorias diagnósticas e mostrar o nível de confiança.

---

## 🔬 Análise dos Notebooks no Google Colab

Se o seu objetivo é explorar o processo de análise de dados e treinamento dos modelos, você pode executar os notebooks Jupyter diretamente no Google Colab.

### **Instruções para o Colab**

Não é necessário baixar o dataset ou criar as pastas manualmente. O primeiro notebook automatiza todo o setup.

1.  **Faça o upload da pasta do projeto** para o seu Google Drive.

2.  **Abra o notebook `01_Setup_e_Preprocessamento.ipynb`**.

3.  **❗ Ajuste o Caminho do Projeto:**
    Logo nas primeiras células de código, localize a variável `PROJECT_PATH` e ajuste o caminho para corresponder à localização da pasta no **seu** Google Drive. É crucial que mantenha o mesmo caminho nos outros notebooks.
    ```python
    PROJECT_PATH = '/content/drive/MyDrive/Seu/Caminho/Para/skin_cancer_analysis'
    ```

4.  **Execute o Notebook `01`:**
    Este notebook é crucial. Ele irá:
    *   Baixar e descompactar o dataset na pasta `/data`.
    *   Criar os scripts Python essenciais (`src/data_preprocessing.py`, `app/main.py`, etc.) necessários para os notebooks seguintes.

5.  **Execute os Notebooks `02` e `03`:**
    *   **`02_Analise_e_Modelagem.ipynb`:** Contém toda a análise exploratória (EDA), o processo de treinamento e escolha do modelo ideal **XGBoost**.
    *   **`03_Visao_Computacional_CNN.ipynb`:** Detalha o treinamento do modelo **ResNet50V2** para classificação de imagens.

---

### 📂 Estrutura do Projeto

```
.
├── app/                  # Contém os scripts da aplicação (API e Dashboard)
├── data/                 # Onde o dataset HAM10000 é armazenado
├── notebooks/            # Notebooks Jupyter com a análise e modelagem
├── saved_models/         # Modelos treinados (XGBoost e CNN)
├── src/                  # Scripts de pré-processamento de dados
├── Dockerfile            # Define a imagem Docker da aplicação
├── Makefile              # Atalhos para comandos Docker
├── requirements.txt      # Lista de dependências Python
└── start.sh              # Script para iniciar os serviços no contêiner
```
