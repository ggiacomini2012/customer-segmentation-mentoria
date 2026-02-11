import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_demographics(df, save_path=None):
    """Plot Age and Gender distribution."""
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    
    # Get unique customers to avoid overcounting events
    unique_customers = df[['cliente', 'idade', 'genero']].drop_duplicates()
    
    # Filter out age outliers (118 is used for nulls)
    valid_customers = unique_customers[unique_customers['idade'] < 100]
    
    sns.histplot(valid_customers['idade'], bins=30, kde=True, ax=ax[0])
    ax[0].set_title('Distribuição de Idade (Removido > 100)')
    
    sns.countplot(data=unique_customers, x='genero', ax=ax[1])
    ax[1].set_title('Distribuição de Gênero')
    
    if save_path:
        plt.savefig(f"{save_path}/demographics.png")
    plt.show()

def plot_funnel(df, save_path=None):
    """Plot Offer Funnel."""
    funnel_data = df[df['tipo_evento'].isin(['oferta visualizada', 'oferta concluída'])]
    funnel_counts = funnel_data.groupby(['oferta', 'tipo_evento']).size().reset_index(name='contagem')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=funnel_counts, x='oferta', y='contagem', hue='tipo_evento')
    plt.title('Funil de Oferta')
    
    if save_path:
        plt.savefig(f"{save_path}/funnel.png")
    plt.show()

def plot_rfm(rfm_df, save_path=None):
    """Plot RFM Clusters."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=rfm_df, x='Recency', y='Monetary', hue='Segment', alpha=0.6)
    plt.title('RFM Clusters')
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    if save_path:
        plt.savefig(f"{save_path}/rfm_clusters.png", bbox_inches='tight')
    plt.show()

def plot_channel_performance(df, portfolio, save_path=None):
    """Plot performance by channel (Reach vs Conversion)."""
    # 1. Explode channels from portfolio
    # (Similar to kpis.py but we need it here for merging)
    import ast
    port_copy = portfolio.copy()
    # Handle string representation of list if needed, or list
    try:
        port_copy['canais_lista'] = port_copy['canal'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    except:
        port_copy['canais_lista'] = port_copy['canal'] # Fallback
        
    offer_channels = port_copy[['id_oferta', 'canais_lista']].explode('canais_lista')
    offer_channels = offer_channels.rename(columns={'canais_lista': 'canal_individual'})
    
    # 2. Filter events
    relevant_events = df[df['tipo_evento'].isin(['oferta visualizada', 'oferta concluída', 'oferta recebida'])]
    
    # 3. Merge
    # This multiplies events by number of channels the offer is available on
    merged = relevant_events.merge(offer_channels, on='id_oferta', how='inner')
    
    # 4. Count
    channel_counts = merged.groupby(['canal_individual', 'tipo_evento']).size().reset_index(name='contagem')
    
    # 5. Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=channel_counts, x='canal_individual', y='contagem', hue='tipo_evento')
    plt.title('Performance por Canal (Multi-atribuição)')
    plt.ylabel('Quantidade de Eventos')
    plt.xlabel('Canal')
    
    if save_path:
        plt.savefig(f"{save_path}/channel_performance.png")
    plt.show()
