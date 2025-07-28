
import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
from PIL import Image
import numpy as np
import tensorflow as tf

# --- 1. Configuração da Página e Dicionários ---
st.set_page_config(
    page_title="Skin Cancer Analysis",
    page_icon="🩺",
    layout="wide"
)

# Dicionário para mapear rótulos para nomes completos
lesion_type_full_name = {
    'nv': 'Nevo Melanocítico',
    'mel': 'Melanoma',
    'bkl': 'Ceratose Benigna',
    'bcc': 'Carcinoma Basocelular',
    'akiec': 'Ceratose Actínica',
    'vasc': 'Lesão Vascular',
    'df': 'Dermatofibroma'
}
class_labels_inv = {v: k for k, v in lesion_type_full_name.items()}

# --- 2. Função para Carregar o Modelo CNN (com cache) ---
@st.cache_resource
def load_cnn_model():
    """Carrega o modelo CNN treinado. O cache evita recarregar a cada interação."""
    try:
        model_path = 'saved_models/cnn_resnet_best.h5'
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo de Visão Computacional: {e}")
        return None

# Carregar o modelo
cnn_model = load_cnn_model()

# --- 3. Título Principal ---
st.title("Sistema de Apoio ao Diagnóstico de Câncer de Pele 🩺")
st.markdown("""
Esta interface demonstra duas abordagens de IA para análise de lesões de pele, baseadas no dataset **HAM10000**.
**Atenção:** Este é um protótipo para fins educacionais e **não substitui um diagnóstico médico**.
""")

# --- 4. Criação das Abas ---
tab1, tab2 = st.tabs(["**Simulador com Dados Clínicos**", "**Análise de Imagem**"])


# --- ABA 1: MODELO TABULAR (XGBOOST) ---
with tab1:
    st.header("Previsão de Melanoma com Base em Dados Clínicos")
    st.markdown("Preencha os campos abaixo com as informações da lesão para receber uma predição do modelo XGBoost, que é especializado em **identificar o risco de Melanoma**.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Informações do Paciente")
            age = st.slider("Idade do Paciente", min_value=0, max_value=100, value=50, step=1)
            sex = st.selectbox("Sexo", ["Masculino", "Feminino", "Desconhecido"], index=0)
        with col2:
            st.subheader("Características da Lesão")
            localization_options = ['abdômen', 'acrál', 'costas', 'tórax', 'orelha', 'rosto', 'pé', 'genital', 'mão', 'extremidade inferior', 'pescoço', 'couro cabeludo', 'tronco', 'desconhecida', 'extremidade superior']
            localization_map = {'abdômen': 'abdomen', 'acrál': 'acral', 'costas': 'back', 'tórax': 'chest', 'orelha': 'ear', 'rosto': 'face', 'pé': 'foot', 'genital': 'genital', 'mão': 'hand', 'extremidade inferior': 'lower_extremity', 'pescoço': 'neck', 'couro cabeludo': 'scalp', 'tronco': 'trunk', 'desconhecida': 'unknown', 'extremidade superior': 'upper_extremity'}
            localization_display = st.selectbox("Localização da Lesão", options=localization_options, index=9)
            localization_internal = localization_map[localization_display]
            dx_type = st.selectbox("Método de Confirmação Inicial", ["Histopatologia", "Acompanhamento", "Consenso", "Confocal"], index=1)
        
        submit_button = st.form_submit_button(label="Analisar Risco de Melanoma")

    if submit_button:
        features = {'age': age, 'dx_type_confocal': 0, 'dx_type_consensus': 0, 'dx_type_follow_up': 0, 'dx_type_histo': 0, 'sex_female': 0, 'sex_male': 0, 'sex_unknown': 0, 'localization_abdomen': 0, 'localization_acral': 0, 'localization_back': 0, 'localization_chest': 0, 'localization_ear': 0, 'localization_face': 0, 'localization_foot': 0, 'localization_genital': 0, 'localization_hand': 0, 'localization_lower_extremity': 0, 'localization_neck': 0, 'localization_scalp': 0, 'localization_trunk': 0, 'localization_unknown': 0, 'localization_upper_extremity': 0}
        if sex == 'Masculino': features['sex_male'] = 1
        elif sex == 'Feminino': features['sex_female'] = 1
        else: features['sex_unknown'] = 1
        dx_type_key = f"dx_type_{dx_type.lower()}"
        if dx_type_key in features: features[dx_type_key] = 1
        localization_key = f"localization_{localization_internal}"
        if localization_key in features: features[localization_key] = 1
        
        with st.spinner('O modelo XGBoost está analisando os dados...'):
            try:
                api_url = "http://127.0.0.1:8000/predict"
                response = requests.post(api_url, data=json.dumps(features))
                if response.status_code == 200:
                    prediction_data = response.json()
                    diagnostico = prediction_data['diagnostico']
                    probabilidade = prediction_data['probabilidade_melanoma']
                    
                    st.subheader("Resultado da Análise (XGBoost)")
                    if diagnostico == "Melanoma":
                        st.warning(f"**Diagnóstico Sugerido:** {diagnostico}")
                    else:
                        st.success(f"**Diagnóstico Sugerido:** {diagnostico}")
                    st.metric(label="Probabilidade de ser Melanoma", value=f"{probabilidade:.2%}")
                    st.progress(probabilidade)
                else:
                    st.error(f"Erro ao chamar a API: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Falha na conexão com a API. Verifique se o serviço FastAPI está em execução.")

# --- ABA 2: MODELO DE IMAGEM (CNN) ---
with tab2:
    st.header("Classificação de Lesão por Análise de Imagem")
    st.markdown("Faça o upload de uma imagem de lesão de pele para que o modelo ResNet50V2 tente classificar o tipo da lesão entre as 7 categorias.")

    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None and cnn_model is not None:
        image = Image.open(uploaded_file)
        
        col1_img, col2_img = st.columns(2)
        with col1_img:
            st.image(image, caption='Imagem Enviada.', use_container_width=True)
        
        with st.spinner('O modelo CNN está analisando a imagem...'):
            # Pré-processamento
            img_resized = image.resize((224, 224))
            img_array = np.array(img_resized)
            img_array_normalized = img_array / 255.0
            img_batch = np.expand_dims(img_array_normalized, axis=0)
            
            # Predição
            prediction_proba = cnn_model.predict(img_batch)[0]
            predicted_class_index = np.argmax(prediction_proba)
            class_labels_map = {0: 'akiec', 1: 'bcc', 2: 'bkl', 3: 'df', 4: 'mel', 5: 'nv', 6: 'vasc'}
            predicted_class_abbr = class_labels_map[predicted_class_index]
            predicted_class_full_name = lesion_type_full_name[predicted_class_abbr]
            confidence = prediction_proba[predicted_class_index]
            
            with col2_img:
                st.subheader("Resultado da Análise (CNN)")
                st.success(f"**Tipo de Lesão Predita:** {predicted_class_full_name.upper()}")
                st.metric(label="Nível de Confiança", value=f"{confidence:.2%}")
                
                # Gráfico de probabilidades
                prob_data = pd.DataFrame({
                    'Probabilidade': prediction_proba,
                    'Tipo de Lesão': [lesion_type_full_name[cls] for cls in class_labels_map.values()]
                })
                fig = px.bar(prob_data, x='Probabilidade', y='Tipo de Lesão', orientation='h', title='Probabilidades por Classe')
                st.plotly_chart(fig, use_container_width=True)
