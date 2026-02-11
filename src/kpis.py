import pandas as pd
import ast

def calculate_ticket_average(df):
    """Calculate mean transaction value."""
    transactions = df[df['tipo_evento'] == 'transacao']
    return transactions['valor'].mean()

def calculate_channel_conversion(df, portfolio):
    """Calculate conversion rate per channel."""
    # Explode portfolio channels
    port_copy = portfolio.copy()
    port_copy['canais_lista'] = port_copy['canal'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    offer_channels = port_copy[['id_oferta', 'canais_lista']].explode('canais_lista')
    offer_channels = offer_channels.rename(columns={'canais_lista': 'canal_individual'})

    # Filter events
    relevant_events = df[df['tipo_evento'].isin(['oferta visualizada', 'oferta concluída'])]
    relevant_events = relevant_events[['id_oferta', 'tipo_evento']]

    # Join
    events_with_channels = relevant_events.merge(offer_channels, on='id_oferta', how='inner')

    # Groupby
    stats = events_with_channels.groupby(['canal_individual', 'tipo_evento']).size().unstack(fill_value=0)
    
    if 'oferta concluída' in stats.columns and 'oferta visualizada' in stats.columns:
        stats['conversion_rate'] = stats['oferta concluída'] / stats['oferta visualizada']
        return stats.sort_values('conversion_rate', ascending=False)
    return stats

def calculate_revenue_by_offer(df):
    """Calculate revenue attribution by offer type."""
    completed = df[df['tipo_evento'] == 'oferta concluída'][['cliente', 'tempo_decorrido', 'oferta']]
    trans = df[df['tipo_evento'] == 'transacao'][['cliente', 'tempo_decorrido', 'valor']]
    
    attributed = completed.merge(trans, on=['cliente', 'tempo_decorrido'], how='inner')
    return attributed.groupby('oferta')['valor'].sum().sort_values(ascending=False)

def calculate_rfm(df):
    """Calculate RFM metrics and segments."""
    transactions = df[df['tipo_evento'] == 'transacao']
    max_time = transactions['tempo_decorrido'].max()
    
    rfm = transactions.groupby('cliente').agg({
        'tempo_decorrido': lambda x: max_time - x.max(),
        'cliente': 'count',
        'valor': 'sum'
    }).rename(columns={'tempo_decorrido': 'Recency', 'cliente': 'Frequency', 'valor': 'Monetary'})
    
    # Scoring
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    return rfm

def segment_customer(row):
    """Apply segmentation logic."""
    r = row['R_Score']
    fm = (row['F_Score'] + row['M_Score']) / 2
    
    if r >= 4 and fm >= 4: return 'Campeoes'
    elif r >= 3 and fm >= 3: return 'Clientes Leais'
    elif r <= 2 and fm >= 3: return 'Em Risco'
    elif r <= 2 and fm < 3: return 'Hibernando'
    elif r >= 3 and fm < 3: return 'Promissores'
    else: return 'Precisa de Atencao'
