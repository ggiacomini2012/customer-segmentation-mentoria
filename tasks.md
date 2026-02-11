
# 🍦 Roadmap de Execução: Case Gelateria Lillo

Este documento serve como guia de execução para o Agente (Cursor/Composer). O objetivo é realizar o nivelamento técnico de análise de dados focado em segmentação de clientes e estratégia de marketing.

## 📁 Estrutura de Arquivos Disponível

* `portifolio_ofertas.xlsx` (11x7)
* `eventos_ofertas.csv` (306k x 7)
* `dados_clientes.csv` (17k x 6)

---

## 🚀 Passo 1: Setup e Inspeção Inicial

**Objetivo:** Carregar os dados e identificar "sujeira" na base.

* [ ] Criar um Jupyter Notebook `analise_exploratoria.ipynb`.
* [ ] Carregar os três arquivos usando Pandas.
* [ ] Executar `.info()` e `.describe()` em todas as bases.
* [ ] Identificar o percentual de valores nulos em `Renda_anual` e `Gênero`.
* [ ] Checar se existem idades inconsistentes (ex: acima de 100 anos).

## 🧹 Passo 2: Limpeza e Tipagem (Data Cleaning)

**Objetivo:** Garantir que os dados estejam prontos para cálculos.

* [ ] Converter `Membro_desde` para o formato datetime.
* [ ] Tratar valores nulos:
* Preencher `Renda_anual` com a mediana da coluna.
* Avaliar se linhas sem gênero/idade devem ser removidas ou categorizadas como "Não Informado".


* [ ] Criar uma coluna `Anos_de_Membro` calculando a diferença entre a data atual e `Membro_desde`.

## 🔗 Passo 3: Enriquecimento de Dados (The Big Merge)

**Objetivo:** Unificar as bases em um DataFrame Mestre.

* [ ] Realizar merge de `eventos_ofertas` com `portifolio_ofertas` via `id_oferta`.
* [ ] Realizar merge do resultado anterior com `dados_clientes` via `id` do cliente.
* [ ] **Validação:** Verificar se o número total de linhas de eventos se manteve após os joins (garantir que não houve perda de dados transacionais).

## 📊 Passo 4: Análise de Negócio e KPIs

**Objetivo:** Extrair as métricas principais para a Gerente da Lillo.

* [ ] Calcular o **Ticket Médio** por transação.
* [ ] Identificar qual **Canal** (Redes Sociais, Email, etc.) tem a maior taxa de conversão (Oferta Vista -> Oferta Finalizada).
* [ ] Calcular a receita total gerada por cada tipo de oferta (`desconto` vs `compre 1 leve 2`).

## 🎯 Passo 5: Segmentação de Clientes (RFM)

**Objetivo:** Agrupar os clientes por comportamento.

* [ ] Criar uma tabela agregada por cliente contendo:
* **Recência:** Dias desde a última compra.
* **Frequência:** Quantidade total de transações.
* **Valor (Monetário):** Soma total gasta.


* [ ] Atribuir scores de 1 a 5 para cada pilar do RFM.
* [ ] Criar categorias: `Campeões`, `Clientes Leais`, `Em Risco`, `Hibernando`.

## 📈 Passo 6: Visualização e Insights

**Objetivo:** Gerar insumos para os slides.

* [ ] Criar gráficos de distribuição de renda por segmento.
* [ ] Gerar um gráfico de barras comparando a taxa de resposta às ofertas por faixa etária.
* [ ] Exportar as tabelas finais de segmentação para `.csv` (para entrega).

---

## 💡 Instruções para o Cursor:

1. Sempre que terminar um passo, salve o progresso no notebook.
2. Comente as descobertas (ex: "Identificado que 10% dos clientes não possuem renda informada").
3. Priorize o uso de **Pandas** e **Seaborn** para visualizações.

