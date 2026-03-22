# 🚗 Preditor de Preço Justo: Toyota Corolla Sedã (SP)

**Status do Projeto:** 🟢 Fase 1 (Entrega N1)

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

## 📊 Resultados da Fase 1 (N1)
Durante a Análise Exploratória de Dados, higienizamos os dados comerciais e comprovamos estatisticamente a correlação negativa entre a variável "Quilometragem" e o "Preço", validando a viabilidade de treinamento do modelo de regressão para a próxima etapa.

## 👥 Equipe
* [Seu Nome] - [Seu RA]
* [Nome do Integrante 2] - [RA do Integrante 2]
* [Nome do Integrante 3] - [RA do Integrante 3]
