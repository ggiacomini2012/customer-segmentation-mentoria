import pandas as pd
import os

# Define file paths
portfolio_path = 'data/portfolio_ofertas.csv'
events_path = 'data/eventos_ofertas.csv'
profile_path = 'data/dados_clientes.csv'

print("Loading data...")
try:
    # Try reading all with a more permissive encoding or just try-catch.
    # Actually, I'll just change all to 'latin-1' as a safe bet for legacy/excel-exported CSVs in Brazil.
    portfolio = pd.read_csv(portfolio_path, encoding='latin-1')
    events = pd.read_csv(events_path, encoding='latin-1')
    profile = pd.read_csv(profile_path, encoding='latin-1')
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

print("\n--- Portfolio Info ---")
print(portfolio.info())
print("\n--- Portfolio Describe ---")
print(portfolio.describe())

print("\n--- Events Info ---")
print(events.info())
print("\n--- Events Describe ---")
print(events.describe())

print("\n--- Profile Info ---")
print(profile.info())
print("\n--- Profile Describe ---")
print(profile.describe())

print("\n--- Null Values Analysis (Profile) ---")
null_metrics = profile[['renda_anual', 'genero']].isnull().mean() * 100
print("Percentage of null values:")
print(null_metrics)

print("\n--- Inconsistent Age Analysis ---")
inconsistent_ages = profile[profile['idade'] > 100]
print(f"Number of records with age > 100: {len(inconsistent_ages)}")
if not inconsistent_ages.empty:
    print("Sample of inconsistent ages:")
    print(inconsistent_ages[['idade']].head())
    print("\nAge distribution summary:")
    print(profile['idade'].describe())
