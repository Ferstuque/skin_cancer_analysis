from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

# --- 1. Configuração da Aplicação ---
app = FastAPI(
    title="API de Diagnóstico de Câncer de Pele",
    version="1.0.0",
    description="Uma API para prever a probabilidade de uma lesão de pele ser Melanoma usando o melhor modelo XGBoost treinado."
)

# --- 2. Carregamento do Modelo e Colunas ---
# Caminhos relativos à raiz do projeto onde o servidor uvicorn será executado
model_path = "saved_models/best_model_v1.pkl"
columns_path = "saved_models/model_columns.pkl"

try:
    model = joblib.load(model_path)
    model_columns = joblib.load(columns_path)
    print("Modelo e colunas carregados com sucesso.")
except FileNotFoundError:
    print(f"Erro: Arquivo do modelo ou colunas não encontrado. Verifique os caminhos: {model_path}, {columns_path}")
    model = None
    model_columns = None

# --- 3. Definição do Modelo de Entrada (Payload) ---
# Usamos Field para definir valores padrão, tornando a API mais fácil de testar
class SkinLesionFeatures(BaseModel):
    age: float = Field(..., example=55.0, description="Idade do paciente")
    dx_type_confocal: int = Field(0, example=0, description="Diagnóstico por microscopia confocal")
    dx_type_consensus: int = Field(0, example=0, description="Diagnóstico por consenso de especialistas")
    dx_type_follow_up: int = Field(0, example=1, description="Lesão em acompanhamento")
    dx_type_histo: int = Field(0, example=0, description="Diagnóstico por histopatologia (biópsia)")
    sex_female: int = Field(0, example=0, description="Sexo feminino")
    sex_male: int = Field(1, example=1, description="Sexo masculino")
    sex_unknown: int = Field(0, example=0, description="Sexo desconhecido")
    localization_abdomen: int = Field(0, example=0)
    localization_acral: int = Field(0, example=0)
    localization_back: int = Field(0, example=0)
    localization_chest: int = Field(0, example=0)
    localization_ear: int = Field(0, example=0)
    localization_face: int = Field(0, example=0)
    localization_foot: int = Field(0, example=0)
    localization_genital: int = Field(0, example=0)
    localization_hand: int = Field(0, example=0)
    localization_lower_extremity: int = Field(1, example=1)
    localization_neck: int = Field(0, example=0)
    localization_scalp: int = Field(0, example=0)
    localization_trunk: int = Field(0, example=0)
    localization_unknown: int = Field(0, example=0)
    localization_upper_extremity: int = Field(0, example=0)

# --- 4. Endpoints da API ---
@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está funcionando."""
    return {"message": "Bem-vindo à API de Diagnóstico. Use o endpoint /predict para fazer uma previsão."}

@app.post("/predict", tags=["Prediction"])
def predict(lesion_features: SkinLesionFeatures):
    """
    Recebe os dados de uma lesão de pele e retorna a previsão de Melanoma.
    """
    if not model or not model_columns:
        raise HTTPException(status_code=503, detail="Modelo não está disponível. Verifique os logs do servidor.")

    try:
        # Converter os dados de entrada para um DataFrame do Pandas
        data = pd.DataFrame([lesion_features.dict()])
        
        # Garantir que a ordem das colunas seja exatamente a mesma do treinamento
        data = data[model_columns]
        
        # Fazer a predição
        prediction_proba = model.predict_proba(data)[0]
        prediction = model.predict(data)[0]

        # Formatar a resposta
        probability_melanoma = prediction_proba[1]
        diagnosis = "Melanoma" if prediction == 1 else "Não-Melanoma"

        return {
            "diagnostico": diagnosis,
            "probabilidade_melanoma": float(probability_melanoma)
        }
    except Exception as e:
        # Captura qualquer outro erro durante a predição
        raise HTTPException(status_code=500, detail=f"Erro durante a predição: {str(e)}")
