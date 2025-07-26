import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Skin-Cancer-Analysis",
    page_icon="🩺",
    layout="wide"
)

# --- 2. Título e Descrição ---
st.title("Sistema de Apoio ao Diagnóstico de Câncer de Pele 🩺")
st.markdown("""
Esta é uma interface de demonstração para um sistema de Machine Learning treinado para prever a probabilidade de uma lesão de pele ser um Melanoma.
O sistema utiliza um modelo **XGBoost** treinado com dados do dataset **HAM10000**.

**Atenção:** Este é um protótipo desenvolvido com fins didáticos para a FIAP Faculdade de Tecnologia e **não substitui o diagnóstico médico**. Consulte sempre um especialista.
""")

# --- 3. Layout do Formulário de Predição ---
st.header("Simulador de Diagnóstico")
st.markdown("Preencha os campos abaixo com as informações da lesão para receber uma predição do modelo.")

with st.form("prediction_form"):
    # Criando colunas para um layout mais organizado
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Informações do Paciente")
        age = st.slider("Idade do Paciente", min_value=0, max_value=100, value=50, step=1)
        sex = st.selectbox("Sexo", ["Masculino", "Feminino", "Desconhecido"], index=0)

    with col2:
        st.subheader("Características da Lesão")
        localization_options = [
            'abdômen', 'acrál', 'costas', 'tórax', 'orelha', 'rosto', 'pé',
            'genital', 'mão', 'extremidade inferior', 'pescoço', 'couro cabeludo',
            'tronco', 'desconhecida', 'extremidade superior'
        ]
        localization_map = {
            'abdômen': 'abdomen', 'acrál': 'acral', 'costas': 'back', 'tórax': 'chest',
            'orelha': 'ear', 'rosto': 'face', 'pé': 'foot', 'genital': 'genital',
            'mão': 'hand', 'extremidade inferior': 'lower extremity', 'pescoço': 'neck',
            'couro cabeludo': 'scalp', 'tronco': 'trunk', 'desconhecida': 'unknown',
            'extremidade superior': 'upper extremity'
        }
        localization_display = st.selectbox("Localização da Lesão", options=localization_options, index=9)
        localization_internal = localization_map[localization_display]

        dx_type = st.selectbox("Método de Confirmação Inicial", ["Histopatologia", "Acompanhamento", "Consenso", "Confocal"], index=1)

    # Botão de submissão do formulário
    submit_button = st.form_submit_button(label="Realizar Previsão")

# --- 4. Lógica de Predição e Exibição de Resultados ---
if submit_button:
    # --- Preparar o Payload para a API ---
    # Inicializar todas as features com 0
    features = {
        'age': age, 'dx_type_confocal': 0, 'dx_type_consensus': 0, 'dx_type_follow_up': 0,
        'dx_type_histo': 0, 'sex_female': 0, 'sex_male': 0, 'sex_unknown': 0,
        'localization_abdomen': 0, 'localization_acral': 0, 'localization_back': 0,
        'localization_chest': 0, 'localization_ear': 0, 'localization_face': 0,
        'localization_foot': 0, 'localization_genital': 0, 'localization_hand': 0,
        'localization_lower_extremity': 0, 'localization_neck': 0,
        'localization_scalp': 0, 'localization_trunk': 0, 'localization_unknown': 0,
        'localization_upper_extremity': 0
    }

    # Atualizar as features com base na seleção do usuário
    # Sexo
    if sex == 'Masculino': features['sex_male'] = 1
    elif sex == 'Feminino': features['sex_female'] = 1
    else: features['sex_unknown'] = 1

    # Tipo de diagnóstico
    dx_type_key = f"dx_type_{dx_type.lower()}"
    if dx_type_key in features:
        features[dx_type_key] = 1
    
    # Localização
    localization_key = f"localization_{localization_internal.replace(' ', '_')}"
    if localization_key in features:
        features[localization_key] = 1
    
    # --- Chamar a API FastAPI ---
    with st.spinner('O modelo está analisando os dados...'):
        try:
            # URL da API. Altere se necessário.
            # Se usar Docker Compose, use o nome do serviço (ex: http://api:8000/predict)
            api_url = "http://127.0.0.1:8000/predict"
            
            response = requests.post(api_url, data=json.dumps(features))
            
            if response.status_code == 200:
                prediction_data = response.json()
                diagnostico = prediction_data['diagnostico']
                probabilidade = prediction_data['probabilidade_melanoma']

                # --- Exibir Resultados de forma visual ---
                st.subheader("Resultado da Análise do Modelo")
                
                if diagnostico == "Melanoma":
                    st.warning(f"**Diagnóstico Sugerido:** {diagnostico}")
                    st.markdown(f"O modelo identificou uma probabilidade de **{probabilidade:.2%}** de a lesão ser um Melanoma.")
                else:
                    st.success(f"**Diagnóstico Sugerido:** {diagnostico}")
                    st.markdown(f"A probabilidade de a lesão ser um Melanoma é de **{probabilidade:.2%}**.")
                
                # Gráfico de rosca para a probabilidade
                prob_data = pd.DataFrame({
                    'Categoria': ['Melanoma', 'Não-Melanoma'],
                    'Probabilidade': [probabilidade, 1 - probabilidade]
                })
                fig = px.pie(prob_data, values='Probabilidade', names='Categoria', 
                             hole=0.4, title='Distribuição de Probabilidade',
                             color_discrete_map={'Melanoma':'#ef553b', 'Não-Melanoma':'#636efa'})
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"Erro ao obter a previsão da API. Status: {response.status_code}")
                st.json(response.json())

        except requests.exceptions.ConnectionError:
            st.error("Falha na conexão com a API. Verifique se o serviço da API (FastAPI/Uvicorn) está em execução.")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
