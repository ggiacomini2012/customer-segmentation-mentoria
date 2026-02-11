import pandas as pd
import numpy as np
from datetime import datetime

# Load data
try:
    portfolio = pd.read_csv('data/portfolio_ofertas.csv', encoding='latin-1')
    events = pd.read_csv('data/eventos_ofertas.csv', encoding='latin-1')
    profile = pd.read_csv('data/dados_clientes.csv', encoding='latin-1')
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# --- CLEANING (Step 2 Logic) ---
# Profile
# Correct column names if needed (checked and they seem to be lowercase in file, but script might need adjustment if they are not)
# My previous script used lowercase. Let's assume they are lowercase as verified.
# However, verify keys from file content:
# profile: "","genero","idade","id","membro_desde","renda_anual" -> lowercase confirmed.
# portfolio: ,recompensa,canal,valor_minimo,duracao,id,oferta -> lowercase confirmed.
# events: ,cliente,tempo_decorrido,valor,id_oferta,recompensa,tipo_evento -> lowercase confirmed.

# 1. Convert 'membro_desde'
profile['membro_desde'] = pd.to_datetime(profile['membro_desde'], format='%Y%m%d')

# 2. Fill Nulls
profile['renda_anual'] = profile['renda_anual'].fillna(profile['renda_anual'].median())
profile['genero'] = profile['genero'].fillna('O')

# 3. Feature Engineering
current_date = datetime.now()
profile['anos_de_membro'] = (current_date - profile['membro_desde']).dt.days / 365.25

print("Step 2 Cleaning Applied.")

# --- MERGE (Step 3 Logic) ---
print("\n--- Merging Data ---")

# 1. Rename columns for consistent keys
portfolio = portfolio.rename(columns={'id': 'id_oferta'})
profile = profile.rename(columns={'id': 'cliente'})

print("Renamed columns: portfolio['id'] -> 'id_oferta', profile['id'] -> 'cliente'.")

# 2. Merge Events + Portfolio
# Left join on 'id_oferta'
# Note: 'id_oferta' in events might have nulls for non-offer events (e.g. transactions without offer)?
# Let's check if 'id_oferta' is null in events.
# Actually, transaction events might not have offer id.
# But for now, let's just merge.
merged_df = events.merge(portfolio, on='id_oferta', how='left')

# 3. Merge Result + Profile
# Left join on 'cliente'
final_df = merged_df.merge(profile, on='cliente', how='left')

print("Merges completed.")

# --- VALIDATION ---
print("\n--- Validation ---")

initial_rows = len(events)
final_rows = len(final_df)

print(f"Initial Events Rows: {initial_rows}")
print(f"Final Merged Rows: {final_rows}")

if initial_rows == final_rows:
    print("SUCCESS: Row count maintained.")
else:
    print(f"WARNING: Row count changed! Diff: {final_rows - initial_rows}")

# Check for nulls in key columns (which shouldn't happen if keys exist)
# 'cliente' should be in profile.
# 'id_oferta' might be null in events (transactions), so it might be null here too.
# But if 'id_oferta' is NOT null in events, it should be found in portfolio.
# Let's check nulls in 'recompensa_y' (from portfolio) where 'id_oferta' is present.

# Check schema
print("\nFinal Schema:")
print(final_df.info())

# Preview
print("\nHead of Merged Data Framework:")
print(final_df.head())
