import pandas as pd
import numpy as np
from datetime import datetime

# --- LOAD (Replicate Merge) ---
try:
    portfolio = pd.read_csv('data/portfolio_ofertas.csv', encoding='latin-1')
    events = pd.read_csv('data/eventos_ofertas.csv', encoding='latin-1')
    profile = pd.read_csv('data/dados_clientes.csv', encoding='latin-1')
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

portfolio = portfolio.rename(columns={'id': 'id_oferta'})
profile = profile.rename(columns={'id': 'cliente'})
merged_df = events.merge(portfolio, on='id_oferta', how='left')
merged_df = merged_df.merge(profile, on='cliente', how='left')

# --- RFM CALCULATION ---
print("Calculating RFM...")

# Filter for transactions to get monetary value and frequency (of purchase)
transactions = merged_df[merged_df['tipo_evento'] == 'transacao']

# If no transactions, we can't do Monetary/Frequency based on purchase.
# Assuming transactions exist (checked in step 4).

# Recency: Days since last transaction
# Using 'tempo_decorrido' (hours).
# Formula: Max Global Time - Customer Max Time
# Or just use the 'tempo_decorrido' directly as recency proxy?
# Higher 'last_time' = More Recent.
# So Recency Score should be higher for higher 'last_time'.
# Standard RFM: Recency is "Days Ago", so Lower is Better.
# Here we have "Time Generated". Higher is Newer.
# So we can use max(time) - customer_time = "Hours Ago".

max_time = merged_df['tempo_decorrido'].max()

rfm = transactions.groupby('cliente').agg({
    'tempo_decorrido': lambda x: max_time - x.max(), # Recency (Hours Ago)
    'cliente': 'count', # Frequency
    'valor': 'sum' # Monetary
})

rfm.rename(columns={
    'tempo_decorrido': 'Recency',
    'cliente': 'Frequency',
    'valor': 'Monetary'
}, inplace=True)

print(f"RFM Table Created with {len(rfm)} customers.")

# --- SCORING (1-5) ---
# Recency: Lower is better (5 for lowest quantile)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])

# Frequency: Higher is better (5 for highest quantile)
# Note: Frequency might have ties, use 'rank' method='first' or distinct binning if needed.
# qcut with duplicates='drop' is safer.
try:
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    # Using rank because many customers might have 1, 2, 3 purchases, causing duplicate edges.
except Exception as e:
    print(f"Error binning Frequency: {e}")
    rfm['F_Score'] = 1 # Fallback

# Monetary: Higher is better
try:
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
except Exception as e:
    print(f"Error binning Monetary (likely ties): {e}")
    rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

# Convert to int
rfm['R_Score'] = rfm['R_Score'].astype(int)
rfm['F_Score'] = rfm['F_Score'].astype(int)
rfm['M_Score'] = rfm['M_Score'].astype(int)

# --- SEGMENTATION ---
# Logic:
# Champions: R=4-5, F+M Avg=4-5 (Recent, frequent, high spender)
# Loyal: R=2-5, F=3-5 (Consistent)
# At Risk: R=1-2, F+M > 3 (High value but havent seen them lately)
# Hibernating: R=1-2, F+M < 3
# Others: Need Attention

def segment_customer(row):
    r = row['R_Score']
    fm = (row['F_Score'] + row['M_Score']) / 2
    
    if r >= 4 and fm >= 4:
        return 'Campeoes'
    elif r >= 3 and fm >= 3:
        return 'Clientes Leais'
    elif r <= 2 and fm >= 3:
        return 'Em Risco'
    elif r <= 2 and fm < 3:
        return 'Hibernando'
    elif r >= 3 and fm < 3:
        return 'Promissores' # New/Recent but low value
    else:
        return 'Precisa de Atencao'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print("\n--- Distribution of Segments ---")
print(rfm['Segment'].value_counts())

print("\n--- Sample RFM Data ---")
print(rfm.head())

# Stats per segment
print("\n--- Mean Monetary by Segment ---")
print(rfm.groupby('Segment')['Monetary'].mean().sort_values(ascending=False))
