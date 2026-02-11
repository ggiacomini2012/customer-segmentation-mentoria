import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# --- LOAD DATA (Steps 1-5 Logic) ---
try:
    portfolio = pd.read_csv('data/portfolio_ofertas.csv', encoding='latin-1')
    events = pd.read_csv('data/eventos_ofertas.csv', encoding='latin-1')
    profile = pd.read_csv('data/dados_clientes.csv', encoding='latin-1')
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Cleaning & Merging
profile['renda_anual'] = profile['renda_anual'].fillna(profile['renda_anual'].median())
profile['genero'] = profile['genero'].fillna('O')
portfolio = portfolio.rename(columns={'id': 'id_oferta'})
profile = profile.rename(columns={'id': 'cliente'})
merged_df = events.merge(portfolio, on='id_oferta', how='left').merge(profile, on='cliente', how='left')

print("Data loaded and merged.")

# --- 1. Demographics ---
print("Generating Demographic Plots...")
plt.figure(figsize=(10, 5))
sns.histplot(profile['idade'], bins=30, kde=True)
plt.title('Distribuição de Idade')
plt.xlabel('Idade')
plt.savefig('distribuicao_idade.png')
plt.close()

plt.figure(figsize=(10, 5))
sns.countplot(data=profile, x='genero')
plt.title('Distribuição de Gênero')
plt.savefig('distribuicao_genero.png')
plt.close()

# --- 2. Offer Funnel (View -> Complete) ---
print("Generating Funnel Plot...")
# Filter events
funnel_data = merged_df[merged_df['tipo_evento'].isin(['oferta visualizada', 'oferta concluída'])]
# Group by Offer Type and Event
funnel_counts = funnel_data.groupby(['oferta', 'tipo_evento']).size().reset_index(name='contagem')

plt.figure(figsize=(12, 6))
sns.barplot(data=funnel_counts, x='oferta', y='contagem', hue='tipo_evento')
plt.title('Funil de Oferta: Visualizada vs Concluída')
plt.ylabel('Quantidade de Eventos')
plt.savefig('funil_ofertas.png')
plt.close()

# --- 3. RFM Clusters ---
print("Generating RFM Plot...")
# Calculate RFM (Simplified for viz)
transactions = merged_df[merged_df['tipo_evento'] == 'transacao']
max_time = transactions['tempo_decorrido'].max()
rfm = transactions.groupby('cliente').agg({
    'tempo_decorrido': lambda x: max_time - x.max(),
    'cliente': 'count',
    'valor': 'sum'
}).rename(columns={'tempo_decorrido': 'Recency', 'cliente': 'Frequency', 'valor': 'Monetary'})

# Assign Segments (Simplified logic for viz, assuming same as before)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)

def segment_customer(row):
    r = row['R_Score']
    fm = (row['F_Score'] + row['M_Score']) / 2
    if r >= 4 and fm >= 4: return 'Campeoes'
    elif r >= 3 and fm >= 3: return 'Clientes Leais'
    elif r <= 2 and fm >= 3: return 'Em Risco'
    elif r <= 2 and fm < 3: return 'Hibernando'
    elif r >= 3 and fm < 3: return 'Promissores'
    else: return 'Precisa de Atencao'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Segment', alpha=0.6)
plt.title('RFM Clusters: Recência vs Valor Monetário')
plt.xlabel('Recência (Horas desde última compra)')
plt.ylabel('Valor Total Gasto ($)')
plt.yscale('log') # Log scale for monetary because it can be skewed
plt.savefig('rfm_clusters.png')
plt.close()

print("All plots generated successfully.")
