import pandas as pd
import numpy as np
import ast

# --- LOAD & PREPROCESS (Steps 1-3) ---
try:
    portfolio = pd.read_csv('data/portfolio_ofertas.csv', encoding='latin-1')
    events = pd.read_csv('data/eventos_ofertas.csv', encoding='latin-1')
    profile = pd.read_csv('data/dados_clientes.csv', encoding='latin-1')
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Rename
portfolio = portfolio.rename(columns={'id': 'id_oferta'})
profile = profile.rename(columns={'id': 'cliente'})

# Merge
merged_df = events.merge(portfolio, on='id_oferta', how='left')
merged_df = merged_df.merge(profile, on='cliente', how='left')

print("Data loaded and merged.")

# --- KPI 1: Ticket Average ---
# Filter for 'transacao' events (assuming 'tipo_evento' == 'transacao' or similar)
# Let's check unique event types first
event_types = merged_df['tipo_evento'].unique()
print(f"Event Types: {event_types}")

# Assuming 'transacao' is the label for transactions
transactions = merged_df[merged_df['tipo_evento'] == 'transacao']
transactions_count = len(transactions)

if transactions_count > 0:
    ticket_average = transactions['valor'].mean()
    print(f"\n1. Ticket Médio: R$ {ticket_average:.2f}")
else:
    print("\n1. Ticket Médio: No 'transacao' events found or checked wrong label.")
    # Check if 'valor' is populated for other types
    print(merged_df.groupby('tipo_evento')['valor'].count())


# --- KPI 2: Channel Conversion ---
print("\n2. Channel Conversion Analysis")
# Parse channels in portfolio
# Channels are strings "['web', 'email']", need to eval
# We need to map 'id_oferta' to its channels
# 1. Create a helper df for offer-channels
portfolio['canais_lista'] = portfolio['canal'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# 2. Explode portfolio to have one row per offer-channel
offer_channels = portfolio[['id_oferta', 'canais_lista']].explode('canais_lista')
offer_channels = offer_channels.rename(columns={'canais_lista': 'canal_individual'})

# 3. Merge with events (only for Offer Viewed and Offer Completed)
# We want conversion from Viewed -> Completed
relevant_events = merged_df[merged_df['tipo_evento'].isin(['oferta visualizada', 'oferta concluída'])]
relevant_events = relevant_events[['id_oferta', 'tipo_evento']] # Keep it light

# Join with exploded channels
# This means if an offer has 3 channels, the event will assume 3 rows (one for each key)
# This assumes "Credit" is given to all channels present on the offer.
events_with_channels = relevant_events.merge(offer_channels, on='id_oferta', how='inner')

# 4. Group by Channel and Event Type
channel_stats = events_with_channels.groupby(['canal_individual', 'tipo_evento']).size().unstack(fill_value=0)

if 'oferta visualizada' in channel_stats.columns and 'oferta concluída' in channel_stats.columns:
    channel_stats['conversion_rate'] = channel_stats['oferta concluída'] / channel_stats['oferta visualizada']
    print(channel_stats.sort_values('conversion_rate', ascending=False))
else:
    print("Columns for conversion calculation missing.")
    print(channel_stats)

# --- KPI 3: Revenue by Offer Type ---
print("\n3. Revenue by Offer Type")
# We need to link revenue ('valor') to offer type ('oferta')
# 'valor' is usually in 'transacao'. 'oferta' is in portfolio.
# 'transacao' events usually do NOT have 'id_oferta' filled in this dataset (standard Starbucks dataset).
# However, 'oferta concluida' usually implies a purchase was made.
# Does 'oferta concluída' have a 'valor'?
completed_offers = merged_df[merged_df['tipo_evento'] == 'oferta concluída']
print(f"Completed Offers with Value: {completed_offers['valor'].count()} / {len(completed_offers)}")

# Check for overlap between 'transacao' and 'oferta concluída'
# Group by cliente and tempo_decorrido
events_grouped = merged_df.groupby(['cliente', 'tempo_decorrido'])

def check_overlap(group):
    has_transaction = 'transacao' in group['tipo_evento'].values
    has_completion = 'oferta concluída' in group['tipo_evento'].values
    return has_transaction and has_completion

# We can just filter for groups with > 1 row and check types
overlap_count = 0
revenue_by_offer = {}

# Iterate/Filter is slow, let's join.
completed = merged_df[merged_df['tipo_evento'] == 'oferta concluída'][['cliente', 'tempo_decorrido', 'oferta', 'id_oferta']]
trans = merged_df[merged_df['tipo_evento'] == 'transacao'][['cliente', 'tempo_decorrido', 'valor']]

# Merge on cliente and time
# This assumes the transaction happens at the exact same 'tempo_decorrido' (time elapsed).
attributed_revenue = completed.merge(trans, on=['cliente', 'tempo_decorrido'], how='inner')

print(f"\nAttributed Transactions: {len(attributed_revenue)}")
if len(attributed_revenue) > 0:
    print(attributed_revenue.groupby('oferta')['valor'].sum())
else:
    print("No direct time overlap found. Cannot attribute revenue simply.")
    print("Will report Total Revenue and Count of Completed Offers by Type.")

# Print Ticket Average again
print(f"Ticket Average: {transactions['valor'].mean()}")

# Print Channel Conversion again properly
print("\nChannel Conversion:")
print(channel_stats['conversion_rate'])
