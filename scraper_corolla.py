import time
import re
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

# ─── DEFINA O INTERVALO DE PÁGINAS AQUI ──────────────────────────────────────
pagina_inicial = 1
pagina_final   = 20
# ─────────────────────────────────────────────────────────────────────────────

arquivo_csv = 'dataset_corolla_sp_bruto.csv'

options = uc.ChromeOptions()
options.add_argument('--window-size=1920,1080')
driver = uc.Chrome(options=options)

# Abre a URL apenas UMA vez na página 1
url = (
    "https://www.webmotors.com.br/carros/sp-sao-paulo/toyota/corolla/carroceria.seda"
    "?lkid=2243&tipoveiculo=carros"
    "&localizacao=-23.5505199%2C-46.6333094x100km"
    "&estadocidade=S%C3%A3o%20Paulo-sao-paulo"
    "&marca1=TOYOTA&modelo1=COROLLA"
    "&page=1&carroceria=Sed%C3%A3"
)
driver.get(url)
time.sleep(6)

def checar_captcha():
    if 'captcha' in driver.page_source.lower() or 'perimeterx' in driver.page_source.lower():
        print("\n⚠️  CAPTCHA detectado!")
        input("   Resolva o CAPTCHA na janela do Chrome, espere os carros carregarem e pressione Enter aqui...")
        time.sleep(3)

def raspar_pagina_atual(pagina):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    checar_captcha()

    try:
        area = driver.find_element(By.CSS_SELECTOR, 'main, div#search-container, [class*="Search_"]')
        html = area.get_attribute('innerHTML')
    except:
        html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    cards = []
    for el in soup.find_all(True):
        t = el.get_text(separator=' ')
        if 'R$' in t and re.search(r'\d[\d.]*\s*[Kk][Mm]', t) and 'COROLLA' in t.upper() and '(SP)' in t:
            cards.append((len(t), el))

    cards.sort(key=lambda x: x[0])
    cards_unicos = []
    vistos = set()
    for _, card in cards:
        chave = card.get_text(separator='|', strip=True)[:100]
        if chave not in vistos:
            vistos.add(chave)
            cards_unicos.append(card)

    print(f"   Cards encontrados: {len(cards_unicos)}")

    dados = []
    for card in cards_unicos:
        try:
            linhas = [l.strip() for l in card.get_text(separator='\n', strip=True).split('\n') if l.strip()]
            nome   = next((l for l in linhas if 'COROLLA' in l.upper()), 'N/A')
            versao = next((l for l in linhas if any(x in l.lower() for x in ['vvt', 'hybrid', 'flex', 'direct', 'cvt'])), 'N/A')
            ano    = next((l for l in linhas if re.match(r'^\d{4}/\d{4}$', l)), 'N/A')
            km     = next((l for l in linhas if re.search(r'\d[\d.]*\s*[Kk][Mm]', l)), 'N/A')
            cidade = next((l for l in linhas if '(SP)' in l and 'km' not in l.lower()), 'N/A')
            preco  = next((l for l in linhas if 'R$' in l), 'N/A')
            if nome == 'N/A' or preco == 'N/A':
                continue
            dados.append({'Pagina': pagina, 'Nome': nome, 'Versao': versao,
                          'Ano': ano, 'Quilometragem': km, 'Cidade': cidade, 'Preco': preco})
        except:
            continue
    return dados

def clicar_proxima_pagina(pagina_destino):
    """Clica no botão do número da página desejada na paginação."""
    try:
        # Rola até o fim para garantir que a paginação esteja visível
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Tenta encontrar o botão com o número da página
        botoes = driver.find_elements(By.CSS_SELECTOR, 
            'button, a, [class*="page"], [class*="Page"], [class*="pagination"], [class*="Pagination"]')
        
        for botao in botoes:
            if botao.text.strip() == str(pagina_destino):
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", botao)
                print(f"   ✅ Clicou no botão da página {pagina_destino}")
                time.sleep(5)
                return True

        # Se não achou pelo número, tenta botão "próxima página" (seta >)
        proximos = driver.find_elements(By.CSS_SELECTOR,
            '[aria-label*="próxima"], [aria-label*="next"], [class*="next"], [class*="Next"]')
        if proximos:
            driver.execute_script("arguments[0].click();", proximos[0])
            print(f"   ✅ Clicou no botão 'próxima página'")
            time.sleep(5)
            return True

        print(f"   ❌ Botão da página {pagina_destino} não encontrado.")
        return False

    except Exception as e:
        print(f"   ❌ Erro ao clicar na paginação: {e}")
        return False

# ─── LOOP PRINCIPAL ───────────────────────────────────────────────────────────
for pagina in range(pagina_inicial, pagina_final + 1):
    print(f"\n📄 Raspando página {pagina}...")

    dados_pagina = raspar_pagina_atual(pagina)

    if not dados_pagina:
        print("   Nenhum dado encontrado. Encerrando.")
        break

    # Salva no CSV
    df_novo = pd.DataFrame(dados_pagina)
    df_novo.drop_duplicates(subset=['Versao', 'Ano', 'Quilometragem', 'Preco'], inplace=True)

    if os.path.exists(arquivo_csv):
        df_existente = pd.read_csv(arquivo_csv, encoding='utf-8-sig')
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        df_final.drop_duplicates(subset=['Versao', 'Ano', 'Quilometragem', 'Preco'], inplace=True)
    else:
        df_final = df_novo

    df_final.to_csv(arquivo_csv, index=False, encoding='utf-8-sig')
    print(f"   ✅ Página {pagina} salva. Total no CSV: {len(df_final)} anúncios.")

    # Navega para a próxima página clicando no botão
    if pagina < pagina_final:
        sucesso = clicar_proxima_pagina(pagina + 1)
        if not sucesso:
            print("   Não foi possível navegar para a próxima página. Encerrando.")
            break
        time.sleep(3)

driver.quit()
print("\n🏁 Extração concluída!")