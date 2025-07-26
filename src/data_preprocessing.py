
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np

def preprocess_tabular_data(csv_path):
    """
    Carrega e pré-processa os dados tabulares do dataset HAM10000.

    Esta função realiza as seguintes etapas:
    1. Carrega os dados do arquivo CSV.
    2. Preenche os valores ausentes na coluna 'age' com a mediana.
    3. Aplica One-Hot Encoding nas variáveis categóricas ('dx_type', 'sex', 'localization').
    4. Aplica StandardScaler na variável numérica 'age'.
    5. Limpa e padroniza TODOS os nomes de colunas como etapa final.
    """
    print(f"Carregando dados de: {csv_path}")
    df = pd.read_csv(csv_path)

    # --- 1. Tratamento de Valores Ausentes ---
    median_age = df['age'].median()
    df['age'].fillna(median_age, inplace=True)
    print(f"Valores nulos em 'age' preenchidos com a mediana ({median_age}).")

    # --- 2. Codificação de Variáveis Categóricas ---
    categorical_cols = ['dx_type', 'sex', 'localization']
    print(f"Aplicando One-Hot Encoding em: {categorical_cols}")
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_data = encoder.fit_transform(df[categorical_cols])
    encoded_cols_names = encoder.get_feature_names_out(categorical_cols)
    encoded_df = pd.DataFrame(encoded_data, columns=encoded_cols_names, index=df.index)
    df = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)

    # --- 3. Escalonamento de Variáveis Numéricas ---
    print("Aplicando StandardScaler na coluna 'age'.")
    scaler = StandardScaler()
    df['age'] = scaler.fit_transform(df[['age']])
    
    # --- 4. Limpeza Final dos Nomes das Colunas ---
    print("Limpando os nomes das colunas...")
    df.columns = df.columns.str.replace(' ', '_', regex=False)
    df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)
    print("Nomes das colunas padronizados.")

    print("\nPré-processamento concluído com sucesso!")

    return df
