🚗 Preditor de Preço Justo: Toyota Corolla Sedã (SP)
👥 Equipe
7K - Gabriel Neman Silva - 10403348

7K - Nicolas Gonçalves - 10418047

7K - Gabriel Pastorelli - 10419046

7J - Nicolai Zeroshenko - 10417221

📌 Sobre o Projeto
Este projeto tem como objetivo desenvolver um modelo de Machine Learning (Regressão) capaz de estimar o preço justo de revenda do Toyota Corolla Sedã no mercado do estado de São Paulo.

O mercado de usados sofre de assimetria de informação e ferramentas estáticas como a Tabela FIPE falham ao não considerar a quilometragem exata, a liquidez de certas versões e o estado real do veículo. Nossa solução extrai dados diretamente do mercado via consumo de API para criar um precificador inteligente, superando as limitações do web scraping tradicional.

🛠️ Tecnologias Utilizadas
Engenharia de Dados (Extração Dinâmica): Python, requests, JSON Parsing (Contorno de bloqueios via injeção de Headers e Cookies).

Processamento e Limpeza (ETL): Pandas, Expressões Regulares (Regex).

Validação Estatística: Cálculo de Limites Lógicos e IQR (Intervalo Interquartil).

Visualização de Dados: Matplotlib, Seaborn.

Machine Learning (Fase N2): Scikit-Learn (A implementar).

📂 Arquitetura do Repositório
Abandonamos o scraping frágil via simuladores de navegador e construímos um pipeline de dados (ETL) em duas etapas sólidas:

main.py: O Motor de Extração. Script autônomo que varre a API invisível da plataforma, contorna paginações, filtra ativamente anúncios indesejados (patrocinados de outros estados ou carrocerias) e salva os dados brutos em lotes.

processamento.py: O Pipeline de Limpeza e Validação. Script unificado que consome a base bruta, remove lixo de formatação, aplica tipagem rigorosa, remove valores nulos e executa o corte de outliers estatísticos e mercadológicos.

Relatorio_N1.pdf: Documentação acadêmica detalhando justificativa, metodologia e aspectos éticos.

📁 Estrutura dos Datasets
1. Dataset Inicial: COROLLA_SP_BRUTO.csv
Arquivo gerado diretamente pelo motor de extração (main.py). Contém os dados do mercado paulista em estado bruto, exatamente como devolvidos pela API, incluindo informações redundantes e formatações inconsistentes (como espaços em branco e colunas de texto puramente descritivas).

2. Dataset Limpo: COROLLA_SP_ML_FINAL.csv
Dataset higienizado e rigorosamente tipado pelo processamento.py, pronto para o consumo do framework de Inteligência Artificial na N2.

Limpeza Básica: Remoção de anúncios duplicados e conversão de textos para números reais (int e float).

Tratamento de Outliers: Aplicação do método estatístico IQR para Preco_Real e Quilometragem, garantindo a remoção de valores irreais sem distorcer a curva matemática do mercado de sedãs.

Regras de Negócio Inseridas: Exclusão de veículos listados abaixo de 50% ou acima de 150% da Tabela FIPE (caracterizados como fraude, sinistro ou erro da plataforma).

Otimização de Features: Descarte de colunas puramente descritivas (Marca, Modelo, Estado) para entregar um dataset enxuto focado apenas nas variáveis que influenciam o algoritmo de regressão.

📊 Resultados da Fase 1 (N1)
O pipeline de dados provou ser escalável e imune a quebras de HTML. Higienizamos os dados comerciais reais de São Paulo e garantimos um dataset sem ruídos, comprovando estatisticamente a correlação negativa entre a variável de desgaste ("Quilometragem") e a Variável Alvo ("Preço"), validando totalmente a viabilidade do modelo preditivo para a próxima etapa.