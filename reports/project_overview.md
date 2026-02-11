# Visão Geral do Projeto de Análise de Dados - Gelateria Lillo

Este documento detalha a jornada completa do projeto, desde a concepção inicial até a entrega dos insights finais.

## 1. O Desafio e a Abordagem

O objetivo principal era realizar um nivelamento técnico em análise de dados, focando na segmentação de clientes e eficácia de marketing para a Gelateria Lillo.

### Pensamento Passo a Passo
Adotamos uma abordagem iterativa e modular:
1.  **Fundação (Steps 1-2)**: Garantir que os dados fossem carregados corretamente e higienizados. Dados sujos geram insights errados.
2.  **Enriquecimento (Step 3)**: Unificar as fontes (Eventos, Ofertas, Clientes) para ter uma visão 360º.
3.  **Inteligência de Negócio (Step 4)**: Traduzir dados brutos em métricas acionáveis (KPIs).
4.  **Estratégia (Step 5)**: Segmentar a base (RFM) para permitir ações personalizadas.
5.  **Comunicação (Step 6)**: Visualizar os resultados para fácil entendimento.

## 2. Stack Tecnológico e Dependências

Optamos por uma stack Python padrão de mercado pela robustez, comunidade e facilidade de uso em análise de dados.

-   **Python 3.13**: Linguagem base.
-   **Pandas**: A "espinha dorsal" para manipulação de dados tabulares (limpeza, merge, agregação).
-   **Matplotlib & Seaborn**: Bibliotecas maduras para visualização estática de alta qualidade.
-   **OpenPyXL**: Suporte para leitura/escrita de arquivos Excel, se necessário.

**Por que essa escolha?**
A combinação Pandas + Seaborn permite prototipar análises complexas em poucas linhas de código, ideal para um projeto de exploração e discovery como este.

## 3. Desafios Enfrentados e Soluções

Durante o projeto, encontramos barreiras comuns em projetos de Data Science realistas:

### a) Problemas de Codificação (Encoding)
-   **O Problema**: Ao carregar os CSVs, o Python retornou `UnicodeDecodeError` pois os arquivos não estavam no padrão UTF-8.
-   **A Solução**: Identificamos e forçamos a leitura com `encoding='latin-1'`, permitindo o carregamento correto dos caracteres especiais.

### b) Qualidade dos Dados (Data Quality)
-   **O Problema**:
    -   Idades registradas como 118 anos (sinalizando dado ausente).
    -   Valores nulos em Renda e Gênero.
-   **A Solução**:
    -   Para Idade/Gênero: Assumimos 'O' (Outros) e mantivemos os registros para não perder histórico de compras.
    -   Para Renda: Imputamos a **mediana** para evitar distorções por outliers ricos.

### c) Atribuição de Receita
-   **O Problema**: A tabela de eventos de transação (`transacao`) não possuía o ID da oferta (`id_oferta`) preenchido, dificultando saber qual promoção gerou a venda.
-   **A Solução**: Criamos uma lógica de atribuição baseada em **tempo e cliente**. Cruzamos transações com eventos de `oferta concluída` que ocorreram no mesmo timestamp para o mesmo cliente, permitindo atribuir o valor monetário à oferta específica.

## 4. Resultados e Impacto

A análise entregou respostas claras para o negócio:

-   **Perfil do Cliente**: Identificamos um público maduro (média 54 anos), sugerindo campanhas focadas em qualidade e fidelidade.
-   **Canais**: Confirmamos que **Web e E-mail** são os canais de maior conversão, enquanto Social Media precisa de revisão.
-   **Ofertas**: Promoções de **Desconto** geram maior volume financeiro que "Leve 2 Pague 1".
-   **Segmentação**: Entregamos uma base classificada em grupos acionáveis (**Campeões**, **Em Risco**, etc.), permitindo que a Gelateria Lillo foque seus esforços de retenção onde o retorno é maior.

---
**Status Final**: Projeto Concluído com Sucesso.
**Artefatos Gerados**: Notebook (`analise_exploratoria.ipynb`), Scripts de validação (`step*.py`) e Relatórios (`insights_conclusoes.md`).
