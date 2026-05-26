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
# Descrição: Extração de dados via API REST da Webmotors. Gera COROLLA_SP_BRUTO.csv.
#
# Histórico:
#   2026-03-24 — Gabriel Neman  — N1: Versão inicial com Selenium + BeautifulSoup
#   2026-05-14 — Gabriel Neman  — N2: Refatoração para consumo direto da API REST
#   2026-05-24 — Gabriel Neman  — N2: Validação final (3.470 anúncios coletados)
# ============================================================================
import os
import requests
import pandas as pd
import time
import random
import urllib.parse


# 1. CONFIGURAÇÕES DA EXTRAÇÃO (Foco: Corolla Sedã no Estado de SP)

# IMPORTANTE: Vá no site curlconverter.com/python, converta o seu cURL 
# e cole os blocos de cookies e headers atualizados aqui dentro.

# https://curlconverter.com/python/ -> Copy as cURL (bash).
cookies = {
    'AMCVS_3ADD33055666F1A47F000101%40AdobeOrg': '1',
    'AMCV_3ADD33055666F1A47F000101%40AdobeOrg': '179643557%7CMCIDTS%7C20592%7CMCMID%7C47183226649551224459222902131001159130%7CMCOPTOUT-1779073438s%7CNONE%7CvVersion%7C5.5.0',
    'kndctr_3ADD33055666F1A47F000101_AdobeOrg_identity': 'CiY0NzE4MzIyNjY0OTU1MTIyNDQ1OTIyMjkwMjEzMTAwMTE1OTEzMFIQCI_h9MTjMxgBKgNPUjIwA_ABj-H0xOMz',
    'kndctr_3ADD33055666F1A47F000101_AdobeOrg_cluster': 'or2',
    'at_check': 'true',
    'visitPageNum': '1',
    'userMarketingChannelv2': 'Direct',
    'mbox': 'session#6c931b2e78fd4c7e835dcc7f37d42580#1779068100|PC#6c931b2e78fd4c7e835dcc7f37d42580.34_0#1842311040',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'pt-BR,pt;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': 'AMCVS_3ADD33055666F1A47F000101%40AdobeOrg=1; AMCV_3ADD33055666F1A47F000101%40AdobeOrg=179643557%7CMCIDTS%7C20592%7CMCMID%7C47183226649551224459222902131001159130%7CMCOPTOUT-1779073438s%7CNONE%7CvVersion%7C5.5.0; kndctr_3ADD33055666F1A47F000101_AdobeOrg_identity=CiY0NzE4MzIyNjY0OTU1MTIyNDQ1OTIyMjkwMjEzMTAwMTE1OTEzMFIQCI_h9MTjMxgBKgNPUjIwA_ABj-H0xOMz; kndctr_3ADD33055666F1A47F000101_AdobeOrg_cluster=or2; at_check=true; visitPageNum=1; userMarketingChannelv2=Direct; mbox=session#6c931b2e78fd4c7e835dcc7f37d42580#1779068100|PC#6c931b2e78fd4c7e835dcc7f37d42580.34_0#1842311040',
}

response = requests.get('https://www.webmotors.com.br/api/filter/car/LocationSearch', cookies=cookies, headers=headers)


# 2. MOTOR DE EXTRAÇÃO ISOLADO

dados_extraidos = []

sessao = requests.Session()
sessao.headers.update(headers)
sessao.cookies.update(cookies)

print("\n🚀 Iniciando extração automatizada: TOYOTA COROLLA (Sedã) - Estado de SP")

pagina = 1 # O robô sempre começa da página 1

# O laço 'while True' permite que o robô rode infinitamente até o estoque acabar
while True:
    print(f"⏳ Baixando página {pagina}...")
    
    # 1. A URL dinâmica baseada na sua pesquisa exata para o Estado de São Paulo
    rota_site = f"https://www.webmotors.com.br/carros/sp/toyota/corolla?lkid=2243&tipoveiculo=carros&estadocidade=S%C3%A3o%20Paulo&marca1=TOYOTA&modelo1=COROLLA&page={pagina}"
    
    # 2. A Webmotors exige que essa rota seja codificada para ler os caracteres especiais
    rota_codificada = urllib.parse.quote(rota_site, safe='')
    
    # 3. A montagem da chamada para a API invisível (LocationSearch)
    url_api = f"https://www.webmotors.com.br/api/search/car?url={rota_codificada}&displayPerPage=47&actualPage={pagina}"
    
    try:
        response = sessao.get(url_api, timeout=15)
        
        # Proteção contra bloqueios (IP banido ou token expirado)
        if response.status_code != 200:
            print(f"❌ Bloqueio/Erro {response.status_code} da Webmotors. Interrompendo na página {pagina}.")
            break 
            
        json_data = response.json()
        resultados = json_data.get('SearchResults', [])
        
        # GATILHO DE PARADA: Se a API não devolver carros, é porque chegamos no fim do catálogo
        if not resultados:
            print(f"🏁 Fim do estoque alcançado na página {pagina}. Finalizando extração.")
            break 
            
        for anuncio in resultados:
            especificacoes = anuncio.get('Specification', {})
            precos = anuncio.get('Prices', {})
            vendedor = anuncio.get('Seller', {})
            
            estado = vendedor.get('State', '')
            carroceria = especificacoes.get('BodyType', '')
            
            # TRAVA DE SEGURANÇA (O "Filtro Anti-Patrocinado"): 
            # Rejeita imediatamente carros injetados pela plataforma que sejam de fora de SP ou não sejam Sedãs
            if 'SP' not in estado or carroceria != 'Sedã':
                continue
                
            dados_extraidos.append({
                'ID_Anuncio': anuncio.get('UniqueId'),
                'Marca': especificacoes.get('Make', {}).get('Value'),
                'Modelo': especificacoes.get('Model', {}).get('Value'),
                'Versao': especificacoes.get('Version', {}).get('Value'),
                'Ano_Fabricacao': especificacoes.get('YearFabrication'),
                'Ano_Modelo': especificacoes.get('YearModel'),
                'Quilometragem': especificacoes.get('Odometer'),
                'Cambio': especificacoes.get('Transmission'),
                'Carroceria': carroceria,
                'Preco_Real': precos.get('Price'),
                'Percentual_FIPE': anuncio.get('FipePercent'),
                'Estado': estado
            })
        
        # Pausas estratégicas para imitar comportamento humano e não esquentar o IP
        tempo_espera = random.uniform(2.5, 5.5)
        time.sleep(tempo_espera)
        
        # A cada 15 páginas, o robô faz uma pausa de 20 segundos
        if pagina % 15 == 0:
            print("☕ Pausa longa de 20 segundos para esfriar o IP e burlar o anti-bot...")
            time.sleep(20)
            
        pagina += 1 # Avança para a próxima aba
            
    except Exception as e:
        print(f"❌ Falha crítica no sistema de rede: {e}")
        break


# 3. EXPORTAÇÃO DINÂMICA (Modo Append)

if dados_extraidos:
    df = pd.DataFrame(dados_extraidos)
    
    # Remove qualquer anúncio que possa ter vindo duplicado na paginação da API
    df.drop_duplicates(subset=['ID_Anuncio'], inplace=True)
    
    nome_arquivo = "COROLLA_SP_BRUTO.csv"
    arquivo_existe = os.path.exists(nome_arquivo)
    
    # Salva adicionando os dados no final, assim você pode pausar e continuar depois sem perder nada
    df.to_csv(nome_arquivo, mode='a', header=not arquivo_existe, index=False, encoding='utf-8-sig')

    print(f"\n=======================================")
    print(f"✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"🚗 Total de Sedãs coletados em SP: {len(df)}")
    print(f"📁 Salvo no arquivo: {nome_arquivo}")
    print(f"=======================================")
else:
    print("\n⚠️ O robô rodou, mas nenhum dado válido foi encontrado para salvar. Verifique seus Cookies.")
