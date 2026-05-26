# ============================================================================
# UNIVERSIDADE PRESBITERIANA MACKENZIE — FCI
# Disciplina: Inteligência Artificial — Prof. Dr. Leandro Zerbinatti
# Projeto: Modelo Preditivo de Precificação de Veículos Usados
#
# Integrantes:
#   - Gabriel Neman      — RA [10403348]
#   - Nicolas Gonçalves  — RA [10418047]
#   - Nicolai Zeroshenko — RA [10417221]
#   - Gabriel Pastoreli  — RA [10419046]
#
# Descrição: Treinamento do RandomForestRegressor. Gera modelo_corolla.pkl
#            e colunas_treinamento.pkl.
#
# Histórico:
#   2026-05-14 — Nicolas Gonçalves — N2: Criação do pipeline de treinamento
#   2026-05-24 — Nicolas Gonçalves — N2: Validação final (R² 93,96% / MAE R$ 5.619,09)
# ============================================================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS

print("🧠 Iniciando o treinamento do Modelo de Inteligência Artificial...")
df = pd.read_csv('COROLLA_SP_ML_FINAL.csv')

# Separando o que queremos prever (y) das informações do carro (X)
# Removemos o Percentual_FIPE para evitar o Data Leakage
y = df['Preco_Real']
X = df.drop(columns=['Preco_Real', 'Percentual_FIPE'])

print(f"📊 Total de registros para treinamento: {len(df)}")


# 2. ENCODING 

X = pd.get_dummies(X, columns=['Versao', 'Cambio'], drop_first=True)

# Guardamos o formato exato das colunas
colunas_treinamento = X.columns
joblib.dump(colunas_treinamento, 'colunas_treinamento.pkl')


# 3. SEPARAÇÃO (Treino vs Teste)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"📚 Estudando com {len(X_train)} carros...")
print(f"📝 Testando com {len(X_test)} carros...")


# 4. O TREINAMENTO (Random Forest Calibrado)

modelo = RandomForestRegressor(
    n_estimators=150, 
    min_samples_leaf=5, 
    random_state=42, 
    n_jobs=-1
)
modelo.fit(X_train, y_train)


# 5. AVALIAÇÃO DO MODELO

previsoes = modelo.predict(X_test)
erro_medio = mean_absolute_error(y_test, previsoes)
precisao = r2_score(y_test, previsoes)

print("\n" + "="*50)
print("🏆 RESULTADOS DA INTELIGÊNCIA ARTIFICIAL")
print(f"🎯 Precisão Geral (R²): {precisao * 100:.2f}%")
print(f"💸 Erro Médio (MAE): R$ {erro_medio:,.2f}")
print("="*50)

# 6. SALVANDO O CÉREBRO DA IA

joblib.dump(modelo, 'modelo_corolla.pkl')
print("\n✅ Modelo salvo com sucesso como 'modelo_corolla.pkl'")
