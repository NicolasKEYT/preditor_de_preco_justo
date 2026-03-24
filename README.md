# 🚗 Preditor de Preço Justo: Toyota Corolla Sedã (SP)

## 👥 Equipe
* 7K - Gabriel Neman Silva - 10403348
* 7K - Nicolas Gonçalves - 10418047
* 7K - Gabriel Pastorelli - 10419046
* 7J - Nicolai  Zeroshenko - 10417221

## 📌 Sobre o Projeto
Este projeto tem como objetivo desenvolver um modelo de *Machine Learning* (Regressão) capaz de estimar o preço justo de revenda do **Toyota Corolla Sedã** no mercado de São Paulo. 

O mercado de usados sofre de assimetria de informação e ferramentas estáticas como a Tabela FIPE falham ao não considerar a quilometragem exata e as diferentes versões de um veículo. Nossa solução extrai dados reais de mercado para criar um precificador inteligente.

## 🛠️ Tecnologias Utilizadas
* **Extração de Dados:** Python, Selenium, Undetected Chromedriver, BeautifulSoup.
* **Análise e Limpeza (EDA):** Pandas, NumPy.
* **Visualização de Dados:** Matplotlib, Seaborn.
* **Machine Learning (Fase N2):** Scikit-Learn (A implementar).

## 📂 Estrutura do Repositório
* `scraper_corolla.py`: Script de *web scraping* desenvolvido para burlar bloqueios anti-bot e extrair dados da plataforma.
* `EDA_corolla.ipynb`: Jupyter Notebook contendo a Análise Exploratória de Dados, limpeza de *outliers* e sanitização matemática.
* `dataset_corolla_sp_bruto.csv`: Dataset original com os dados recém-extraídos.
* `dataset_corolla_limpo_ML.csv`: Dataset processado e formatado para o treinamento da IA.
* `Relatorio_N1.pdf`: Documentação acadêmica detalhando justificativa, metodologia e aspectos éticos (LGPD).

### Dataset Inicial. `dataset_corolla_sp_bruto.csv`
Arquivo gerado diretamente pelo script de *web scraping*. Contém os dados em estado bruto, exatamente como foram renderizados no HTML da plataforma, incluindo ruídos, caracteres especiais e formatos inconsistentes.
* **Ano:** String composta (ex: `2023/2024`).
* **Quilometragem:** String com sufixo (ex: `75.000 Km`).
* **Preco:** String com prefixo e pontuação (ex: `R$ 133.900`).

### Dataset Limpo. `dataset_corolla_limpo_ML.csv`
Dataset higienizado e rigorosamente tipado, pronto para o consumo do framework de Machine Learning na N2. 
* **Tratamento:** Remoção de *outliers* (preços irreais ou fora do padrão do mercado de sedãs) e linhas com dados faltantes (`N/A`).
* **Features de Treinamento (Novas Colunas Numéricas):**
  * `Preco_Limpo`: Variável Alvo (*Target*). Numérico inteiro, sem símbolos (ex: `133900`).
  * `KM_Limpo`: Feature de desgaste. Numérico inteiro (ex: `75000`).
  * `Ano_Modelo`: Feature temporal. Numérico inteiro extraído da string original para cálculo da curva de depreciação (ex: `2024`).

## 📊 Resultados da Fase 1 (N1)
Durante a Análise Exploratória de Dados, higienizamos os dados comerciais e comprovamos estatisticamente a correlação negativa entre a variável "Quilometragem" e o "Preço", validando a viabilidade de treinamento do modelo de regressão para a próxima etapa.