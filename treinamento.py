import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# ==============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==============================================================================
print("🧠 Iniciando o treinamento do Modelo de Inteligência Artificial...")
df = pd.read_csv('COROLLA_SP_ML_FINAL.csv')

# Separando o que queremos prever (y) das informações do carro (X)
# Removemos o Percentual_FIPE para evitar o Data Leakage
y = df['Preco_Real']
X = df.drop(columns=['Preco_Real', 'Percentual_FIPE'])

print(f"📊 Total de registros para treinamento: {len(df)}")

# ==============================================================================
# 2. ENCODING (Traduzindo texto para matemática)
# ==============================================================================
X = pd.get_dummies(X, columns=['Versao', 'Cambio'], drop_first=True)

# Guardamos o formato exato das colunas
colunas_treinamento = X.columns
joblib.dump(colunas_treinamento, 'colunas_treinamento.pkl')

# ==============================================================================
# 3. SEPARAÇÃO (Treino vs Teste)
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"📚 Estudando com {len(X_train)} carros...")
print(f"📝 Testando com {len(X_test)} carros...")

# ==============================================================================
# 4. O TREINAMENTO (Random Forest Calibrado)
# ==============================================================================
# O min_samples_leaf=5 obriga a IA a generalizar o mercado e evita o Overfitting
modelo = RandomForestRegressor(
    n_estimators=150, 
    min_samples_leaf=5, 
    random_state=42, 
    n_jobs=-1
)
modelo.fit(X_train, y_train)

# ==============================================================================
# 5. AVALIAÇÃO DO MODELO
# ==============================================================================
previsoes = modelo.predict(X_test)
erro_medio = mean_absolute_error(y_test, previsoes)
precisao = r2_score(y_test, previsoes)

print("\n" + "="*50)
print("🏆 RESULTADOS DA INTELIGÊNCIA ARTIFICIAL")
print(f"🎯 Precisão Geral (R²): {precisao * 100:.2f}%")
print(f"💸 Erro Médio (MAE): R$ {erro_medio:,.2f}")
print("="*50)

# ==============================================================================
# 6. SALVANDO O CÉREBRO DA IA
# ==============================================================================
joblib.dump(modelo, 'modelo_corolla.pkl')
print("\n✅ Modelo salvo com sucesso como 'modelo_corolla.pkl'")