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
# Descrição: Interface CLI para inferência do modelo. Filtros dinâmicos
#            por ano, versão e câmbio. Retorna o preço justo estimado.
#
# Histórico:
#   2026-05-14 — Nicolai Zeroshenko — N2: Criação da interface com filtros dinâmicos
#   2026-05-24 — Nicolai Zeroshenko — N2: Testes finais de validação do modelo
# ============================================================================
import pandas as pd
import joblib

# ==============================================================================
# 1. CARREGAR OS DADOS E O MODELO
# ==============================================================================
print("⏳ Ligando o motor da IA e lendo o mercado...")
modelo = joblib.load('modelo_corolla.pkl')
colunas_treinamento = joblib.load('colunas_treinamento.pkl')

df_base = pd.read_csv('COROLLA_SP_ML_FINAL.csv', usecols=['Ano_Fabricacao', 'Ano_Modelo', 'Versao', 'Cambio'])

# ==============================================================================
# 2. INTERFACE NO TERMINAL (MENU INTERATIVO)
# ==============================================================================
print("\n" + "="*50)
print(" 🤖 PREDITOR DE PREÇO JUSTO: TOYOTA COROLLA ")
print("="*50)

try:
    ano_fab = int(input("1. Digite o Ano de Fabricação (ex: 2021): "))
    ano_mod = int(input("2. Digite o Ano do Modelo (ex: 2022): "))
    km_bruto = int(input("3. Digite a Quilometragem (ex: 55000): "))

    # REGRA DE NEGÓCIOS: Arredonda o KM para os 500 mais próximos (ex: 55001 vira 55000)
    km = round(km_bruto / 500) * 500

    # FILTRO DINÂMICO 1: Busca apenas as versões que existiram naqueles anos específicos
    df_filtrado_ano = df_base[(df_base['Ano_Fabricacao'] == ano_fab) & (df_base['Ano_Modelo'] == ano_mod)]
    
    if df_filtrado_ano.empty:
        print("\n❌ ERRO: Não encontramos nenhum Corolla na base de dados com essa combinação de anos.")
        exit()

    versoes_disponiveis = df_filtrado_ano['Versao'].dropna().unique().tolist()

    print("\n--- VERSÕES DISPONÍVEIS PARA ESSE ANO ---")
    for i, versao in enumerate(versoes_disponiveis):
        print(f"[{i}] {versao}")
    
    escolha_versao = int(input("\n4. Digite o NÚMERO da versão correspondente: "))
    versao_escolhida = versoes_disponiveis[escolha_versao]

    # FILTRO DINÂMICO 2: Busca os câmbios que existem para essa versão e esse ano
    cambios_filtrados = df_filtrado_ano[df_filtrado_ano['Versao'] == versao_escolhida]['Cambio'].dropna().unique().tolist()

    if len(cambios_filtrados) == 1:
        cambio_escolhido = cambios_filtrados[0]
        print(f"\n✅ Câmbio detectado automaticamente: {cambio_escolhido}")
    else:
        print("\n--- CÂMBIOS DISPONÍVEIS PARA ESTA VERSÃO ---")
        for i, cambio in enumerate(cambios_filtrados):
            print(f"[{i}] {cambio}")
        
        escolha_cambio = int(input("\n5. Digite o NÚMERO do câmbio correspondente: "))
        cambio_escolhido = cambios_filtrados[escolha_cambio]

except (ValueError, IndexError):
    print("\n❌ ERRO: Você deve digitar números válidos correspondentes ao menu.")
    exit()

# ==============================================================================
# 3. PREPARAÇÃO DOS DADOS E PREVISÃO
# ==============================================================================
carro_consulta = {
    'Ano_Fabricacao': ano_fab,
    'Ano_Modelo': ano_mod,
    'Quilometragem': km,
    'Versao': versao_escolhida,
    'Cambio': cambio_escolhido
}

df_carro = pd.DataFrame([carro_consulta])
df_carro = pd.get_dummies(df_carro, columns=['Versao', 'Cambio'])
df_carro = df_carro.reindex(columns=colunas_treinamento, fill_value=0)

preco_estimado = modelo.predict(df_carro)[0]

# ==============================================================================
# 4. EXIBIÇÃO DO RESULTADO
# ==============================================================================
print("\n" + "="*50)
print(" 🚗 RELATÓRIO FINAL DE AVALIAÇÃO ")
print("="*50)
print(f"🔹 Veículo: Toyota Corolla Sedã")
print(f"🔹 Versão:  {versao_escolhida}")
print(f"🔹 Câmbio:  {cambio_escolhido}")
print(f"🔹 Ano:     {ano_fab}/{ano_mod}")
print(f"🔹 KM:      {km:,}".replace(',', '.'))
print("-" * 50)
print(f"💰 PREÇO JUSTO DE MERCADO: R$ {preco_estimado:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
print("="*50)
