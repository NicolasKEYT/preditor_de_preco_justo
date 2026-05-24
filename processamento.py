import pandas as pd

# ==============================================================================
# CONFIGURAÇÕES DE ENTRADA E SAÍDA
# ==============================================================================
nome_arquivo_entrada = 'COROLLA_SP_BRUTO.csv'
nome_arquivo_saida   = 'COROLLA_SP_ML_FINAL.csv'

print("🚀 Iniciando o pipeline unificado de Processamento de Dados (ETL)...")
df = pd.read_csv(nome_arquivo_entrada, dtype=str) 

linhas_originais = len(df)
print(f"📊 Linhas originais carregadas: {linhas_originais}")

# ==============================================================================
# ETAPA 1: LIMPEZA BÁSICA E TIPAGEM
# ==============================================================================
print("\n🧹 [Etapa 1] Limpeza de dados nulos, duplicatas e conversão de tipos...")

df = df[df['Marca'] != 'Marca'] # Remove cabeçalhos perdidos no meio da tabela

# Trata espaços vazios e transforma em nulos reais (NaN) para o pandas apagar
df = df.apply(lambda col: col.str.strip())
df = df.replace('', pd.NA) 
df = df.replace(r'^\s*$', pd.NA, regex=True)

df.dropna(how='any', inplace=True)
df.drop_duplicates(subset=['ID_Anuncio'], inplace=True)

# Tipagem rigorosa das variáveis numéricas
colunas_numericas = ['Preco_Real', 'Quilometragem', 'Percentual_FIPE', 'Ano_Fabricacao', 'Ano_Modelo']
for col in colunas_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(subset=colunas_numericas, inplace=True)

df['Ano_Fabricacao'] = df['Ano_Fabricacao'].astype(int)
df['Ano_Modelo']     = df['Ano_Modelo'].astype(int)
df['Quilometragem']  = df['Quilometragem'].astype(int)

linhas_pos_limpeza = len(df)
print(f" ✔ Linhas após limpeza básica: {linhas_pos_limpeza}")

# ==============================================================================
# ETAPA 2: TRATAMENTO DE OUTLIERS (ESTATÍSTICA E LÓGICA)
# ==============================================================================
print("\n🔍 [Etapa 2] Removendo outliers estatísticos (IQR) e limites lógicos...")

def remover_outliers_iqr(dataframe, coluna):
    Q1  = dataframe[coluna].quantile(0.25)
    Q3  = dataframe[coluna].quantile(0.75)
    IQR = Q3 - Q1

    limite_inf = Q1 - 1.5 * IQR
    limite_sup = Q3 + 1.5 * IQR

    filtro = (dataframe[coluna] >= limite_inf) & (dataframe[coluna] <= limite_sup)
    df_filtrado = dataframe[filtro]
    
    removidas = len(dataframe) - len(df_filtrado)
    return df_filtrado, removidas

# Aplica o IQR para as duas colunas principais
df, removidas_preco = remover_outliers_iqr(df, 'Preco_Real')
print(f" ✔ Preço_Real    — removidos: {removidas_preco}")

df, removidas_km = remover_outliers_iqr(df, 'Quilometragem')
print(f" ✔ Quilometragem — removidos: {removidas_km}")

# Aplica o limite de sanidade do mercado (FIPE)
antes_fipe = len(df)
df = df[(df['Percentual_FIPE'] >= 50) & (df['Percentual_FIPE'] <= 150)]
removidas_fipe = antes_fipe - len(df)
print(f" ✔ Percentual_FIPE — removidos: {removidas_fipe}")

# ==============================================================================
# ETAPA 3: DROP DE COLUNAS REDUNDANTES PARA O MODELO DE ML
# ==============================================================================
print("\n✂️ [Etapa 3] Removendo colunas desnecessárias para a IA...")
# Como o dataset é focado apenas em Corollas Sedã em SP, essas strings não servem para a matemática da regressão
colunas_para_dropar = ['ID_Anuncio', 'Marca', 'Modelo', 'Carroceria', 'Estado']
df.drop(columns=colunas_para_dropar, inplace=True, errors='ignore')

# ==============================================================================
# ETAPA 4: SALVAMENTO DO DATASET FINAL
# ==============================================================================
df.to_csv(nome_arquivo_saida, index=False, encoding='utf-8-sig')

total_lixo = linhas_originais - linhas_pos_limpeza
total_outliers = removidas_preco + removidas_km + removidas_fipe

print("\n" + "="*50)
print("✅ PIPELINE DE PROCESSAMENTO CONCLUÍDO!")
print(f"📊 Linhas originais:            {linhas_originais}")
print(f"🗑️ Total removidas (Lixo/NaN):  {total_lixo}")
print(f"🗑️ Total removidas (Outliers):  {total_outliers}")
print(f"🎯 Linhas finais p/ Treinamento: {len(df)}")
print(f"📁 Arquivo salvo como:          {nome_arquivo_saida}")
print("="*50)