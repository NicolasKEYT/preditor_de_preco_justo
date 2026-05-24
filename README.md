# 🚗 Preditor de Preço Justo — Toyota Corolla Sedã (SP)

> Projeto de Inteligência Artificial — UPM/FCI — 7º semestre de Sistemas de Informação
> Disciplina: Inteligência Artificial — Prof. Dr. Leandro Zerbinatti

## 📌 Sobre o Projeto

Este projeto desenvolve um modelo de Machine Learning (Regressão) capaz de estimar o preço justo de revenda do Toyota Corolla Sedã no mercado do estado de São Paulo.

O mercado de usados sofre de assimetria de informação, e ferramentas estáticas como a Tabela FIPE falham ao não considerar a quilometragem exata, a liquidez de versões específicas e o estado real do veículo. Nossa solução extrai dados diretamente do mercado via consumo de API REST interna, processa estatisticamente, e treina um modelo Random Forest que aprende a função de depreciação real do mercado.

## 🏆 Resultados Principais (N2 — entregue)

- **R² (precisão geral): 93,96%** — o modelo explica ~94% da variância de preço
- **MAE (erro médio): R$ 5.619,09** — desvio médio entre preço previsto e real
- **Erro relativo: ~4,76%** do preço médio do dataset
- **Dataset: 3.311 anúncios validados** (de 3.470 brutos coletados)
- **Correlações confirmadas:** Quilometragem × Preço = −0,808 | Ano × Preço = +0,907

## 🛠️ Tecnologias Utilizadas

- **Engenharia de Dados:** Python, `requests`, JSON parsing, contorno de anti-bot via injeção de headers/cookies extraídos de sessão legítima
- **Processamento (ETL):** Pandas, Regex, validação estatística com IQR e regra mercadológica (faixa FIPE 50–150%)
- **Análise Exploratória:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-Learn (`RandomForestRegressor`)
- **Serialização:** Joblib (`.pkl`)
- **Interface:** `ipywidgets` (Colab) + CLI (terminal local)

## 📂 Arquitetura do Repositório

Pipeline em 4 etapas executadas por scripts independentes:

| Arquivo | Responsável | Papel |
|---------|-------------|-------|
| `main.py` | **Motor de Extração** — varre a API REST interna da Webmotors, contorna paginação, filtra anúncios indesejados e salva os dados brutos |
| `processamento.py` | **Pipeline de Limpeza (ETL)** — consome a base bruta, remove lixo, aplica tipagem rigorosa, remove outliers estatísticos (IQR) e mercadológicos (FIPE) |
| `treinamento.py` | **Treinamento da IA** — treina o `RandomForestRegressor`, avalia com R² e MAE, salva o modelo e a ordem das features |
| `prever_interativo.py` | **Interface CLI + Testes** — carrega o modelo treinado e oferece menu interativo para estimar preços |
| `EDA_corolla_N1.ipynb` | Notebook da análise exploratória da fase N1 (mantido como histórico) |
| `Preditor_Corolla_SP.ipynb` | Notebook do Colab com pipeline completo (ETL + EDA + Treino + Previsão interativa) |
| `modelo_corolla.pkl` | — | Modelo treinado serializado |
| `colunas_treinamento.pkl` | Ordem das colunas após one-hot encoding |
## 📁 Estrutura dos Datasets

### Dataset Bruto: `COROLLA_SP_BRUTO.csv` (3.470 anúncios)

Arquivo gerado pelo `main.py`. Contém os dados em estado bruto exatamente como devolvidos pela API REST, com as colunas: `ID_Anuncio`, `Marca`, `Modelo`, `Versao`, `Ano_Fabricacao`, `Ano_Modelo`, `Quilometragem`, `Cambio`, `Carroceria`, `Preco_Real`, `Percentual_FIPE`, `Estado`.

### Dataset Limpo: `COROLLA_SP_ML_FINAL.csv` (3.311 anúncios)

Dataset higienizado pelo `processamento.py`, pronto para o treinamento:

- **Limpeza básica:** remoção de duplicatas (por `ID_Anuncio`), conversão de strings para tipos numéricos
- **Tratamento estatístico de outliers:** método IQR aplicado em `Preco_Real` e `Quilometragem`
- **Regra de negócio:** exclusão de veículos abaixo de 50% ou acima de 150% da Tabela FIPE (fraude, sinistro ou erro de cadastro)
- **Otimização de features:** descarte de colunas constantes (`Marca`, `Modelo`, `Estado`, `Carroceria`)

## 🚀 Como Executar

### Opção 1: Colab (recomendado)

1. Abra `Preditor_Corolla_SP.ipynb` no Google Colab
2. Execute as células em ordem
3. Faça upload do `COROLLA_SP_BRUTO.csv` quando solicitado
4. O notebook gera EDA, treina o modelo e exibe a interface interativa de previsão

### Opção 2: Local (terminal)

```bash
# Coleta dos dados (requer cookies/headers atualizados no main.py)
python main.py

# Limpeza e tratamento
python processamento.py

# Treinamento do modelo
python treinamento.py

# Previsão interativa via menu
python prever_interativo.py
```

## 📊 Evolução Metodológica (N1 → N2)

Na fase N1, a coleta usava Selenium + `undetected_chromedriver` + BeautifulSoup. Essa abordagem se mostrou frágil contra mecanismos anti-bot, lenta pela renderização de página e quebradiça frente a mudanças de HTML. Na N2, refatoramos para consumo direto da API REST interna (`/api/search/car`) via `requests`, ganhando robustez, velocidade e expansibilidade — o dataset cresceu de 991 anúncios (N1) para 3.470 brutos / 3.311 finais (N2).

## ⚖️ Aspectos Éticos e Governança Algorítmica

O projeto foi desenvolvido em conformidade com os princípios da **LGPD (Lei Geral de Proteção de Dados)**:

- **Privacidade:** a coleta incide exclusivamente sobre informações comerciais públicas (anúncios visíveis a qualquer visitante). Nenhum dado pessoal de usuários ou vendedores (nomes, contatos, endereços, documentos) foi extraído ou armazenado.
- **Uso responsável de recursos:** pausas aleatórias entre requisições garantem que o servidor da plataforma não sofra sobrecarga.
- **Prevenção de vieses:** o escopo foi deliberadamente restrito a um modelo (Corolla) e uma região (SP) para evitar discriminação geográfica ou contaminação por curvas de depreciação distintas entre carrocerias.
- **Transparência:** o modelo opera como ferramenta de suporte à decisão com margem de erro estatística declarada, e não como instrumento absoluto de fixação de preços.

## 👥 Integrantes e Responsabilidades

| Integrante | RA | Turma | Responsabilidade Principal |
|------------|-----|-------|----------------------------|
| Gabriel Neman Silva | 10403348 | 7K | Coleta de dados (API REST) |
| Gabriel Pastorelli | 10419046 | 7K | Processamento e limpeza (ETL) |
| Nicolas Gonçalves | 10418047 | 7K | Treinamento do modelo |
| Nicolai Zeroshenko | 10417221 | 7J | Interface e validação |

**Orientador:** Prof. Dr. Leandro Zerbinatti
**Instituição:** Universidade Presbiteriana Mackenzie — Faculdade de Computação e Informática (FCI)

## 🎥 Vídeo de Apresentação

[INSERIR LINK DO YOUTUBE APÓS GRAVAÇÃO]
