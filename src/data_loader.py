import pandas as pd
import numpy as np

def load_data(portfolio_path, events_path, profile_path):
    """Loads raw data from CSVs."""
    portfolio = pd.read_csv(portfolio_path, encoding='latin-1')
    events = pd.read_csv(events_path, encoding='latin-1')
    profile = pd.read_csv(profile_path, encoding='latin-1')
    return portfolio, events, profile

def clean_data(portfolio, events, profile):
    """Cleans and preprocesses data (Steps 1-2)."""
    # Profile
    profile['membro_desde'] = pd.to_datetime(profile['membro_desde'], format='%Y%m%d')
    profile['renda_anual'] = profile['renda_anual'].fillna(profile['renda_anual'].median())
    profile['genero'] = profile['genero'].fillna('O')
    
    # Feature Engineering
    current = pd.Timestamp.now()
    profile['anos_de_membro'] = (current - profile['membro_desde']).dt.days / 365.25
    
    return portfolio, events, profile

def merge_data(portfolio, events, profile):
    """Merges datasets into a master dataframe (Step 3)."""
    portfolio = portfolio.rename(columns={'id': 'id_oferta'})
    profile = profile.rename(columns={'id': 'cliente'})
    
    merged_df = events.merge(portfolio, on='id_oferta', how='left')
    merged_df = merged_df.merge(profile, on='cliente', how='left')
    
    return merged_df

def get_processed_data(data_dir='data/'):
    """High-level function to get the final merged dataframe."""
    p_path = f"{data_dir}portfolio_ofertas.csv"
    e_path = f"{data_dir}eventos_ofertas.csv"
    pr_path = f"{data_dir}dados_clientes.csv"
    
    port, ev, prof = load_data(p_path, e_path, pr_path)
    port, ev, prof = clean_data(port, ev, prof)
    final_df = merge_data(port, ev, prof)
    
    return final_df
