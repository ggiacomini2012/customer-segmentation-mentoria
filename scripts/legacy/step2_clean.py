import pandas as pd
import numpy as np
from datetime import datetime

# Load data with correct encoding
try:
    portfolio = pd.read_csv('data/portfolio_ofertas.csv', encoding='latin-1')
    events = pd.read_csv('data/eventos_ofertas.csv', encoding='latin-1')
    profile = pd.read_csv('data/dados_clientes.csv', encoding='latin-1')
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# --- CLEANING PROFILE DATA ---
print("\n--- Cleaning Profile Data ---")

# 1. Convert 'membro_desde' to datetime
# Format appears to be YYYYMMDD based on head() output (e.g., 20170212)
try:
    profile['membro_desde'] = pd.to_datetime(profile['membro_desde'], format='%Y%m%d')
    print("Converted 'membro_desde' to datetime.")
except Exception as e:
    print(f"Error converting 'membro_desde': {e}")

# 2. Handle Nulls in 'renda_anual' (Fill with Median)
median_income = profile['renda_anual'].median()
profile['renda_anual'] = profile['renda_anual'].fillna(median_income)
print(f"Filled null 'renda_anual' with median: {median_income}")

# 3. Handle Nulls in 'genero' (Fill with 'O' for Other/Unknown)
profile['genero'] = profile['genero'].fillna('O')
print("Filled null 'genero' with 'O'.")

# 4. Handle Age 118 (Treat as NaN or separate category? Task says "Avaliar")
# Strategy: Replace 118 with NaN for now to avoid skewing stats, or keep as is if it represents "Unknown".
# Given the high count (2180), it's likely "Unknown".
# I will leave it as is for now but note it, or maybe replace with NaN if I need to calculate age stats.
# The task says: "Avaliar se linhas sem gênero/idade devem ser removidas ou categorizadas como 'Não Informado'".
# Since I filled Gender with 'O', I will treat Age 118 as "Unknown" implicitly, but for calculations, it might vary.
# Let's check overlap:
unknown_age_count = profile[profile['idade'] == 118].shape[0]
print(f"Records with age 118: {unknown_age_count}")

# 5. Create 'anos_de_membro'
# Reference date: Let's use the max date in the dataset or today?
# Usually for static analysis of past data, using the max date in events or a specific "analysis date" is better.
# However, "data atual" usually implies today. But for reproducibility, I'll check the max date in events usually.
# Let's use today's date for now as requested ("data atual"), slightly risky if data is old.
# Let's check max date in profile 'membro_desde'.
max_date = profile['membro_desde'].max()
print(f"Max member date: {max_date}")
# Let's use a fixed date relative to the dataset for consistency, e.g., 2018-12-31 or just today.
# Prompt says "data atual". I will use datetime.now().
current_date = datetime.now()
profile['anos_de_membro'] = (current_date - profile['membro_desde']).dt.days / 365.25
print("Created 'anos_de_membro' column.")

# --- VERIFICATION ---
print("\n--- Verification ---")
print(profile.info())
print("\nNull values after cleaning:")
print(profile[['renda_anual', 'genero', 'membro_desde']].isnull().sum())
print("\nSample of 'anos_de_membro':")
print(profile[['membro_desde', 'anos_de_membro']].head())
