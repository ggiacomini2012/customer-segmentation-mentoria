import sys
import os

# Add project root to path to allow importing from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import get_processed_data, load_data
from src.kpis import calculate_ticket_average, calculate_channel_conversion, calculate_revenue_by_offer, calculate_rfm, segment_customer
from src.visualization import plot_demographics, plot_funnel, plot_rfm

def run():
    print("--- Starting Pipeline ---")
    
    # Project Root and Data Directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, 'data') + os.sep

    
    # 1. Load & Clean
    print("Step 1-3: Loading, Cleaning, and Merging Data...")
    try:
        final_df = get_processed_data(data_dir=data_dir)
        print(f"Data ready. Shape: {final_df.shape}")
    except Exception as e:
        print(f"Error in data processing: {e}")
        return

    # 2. KPIs
    print("\nStep 4: Calculating KPIs...")
    # Need portfolio for channel analysis
    # Re-load portfolio raw for channel conversion logic (or pass it through)
    # Ideally get_processed_data should return raw portfolio too if needed, but we can just reload it or modify src.
    # For now, let's reload just for the KPI function requirements.
    p_path = os.path.join(data_dir, 'portfolio_ofertas.csv')
    e_path = os.path.join(data_dir, 'eventos_ofertas.csv')
    pr_path = os.path.join(data_dir, 'dados_clientes.csv')
    
    portfolio, _, _ = load_data(p_path, e_path, pr_path)
    portfolio = portfolio.rename(columns={'id': 'id_oferta'})

    ticket = calculate_ticket_average(final_df)
    print(f"Ticket Average: {ticket:.2f}")
    
    conversion = calculate_channel_conversion(final_df, portfolio)
    print("Channel Conversion:")
    print(conversion)
    
    revenue = calculate_revenue_by_offer(final_df)
    print("Revenue by Offer:")
    print(revenue)
    
    # 3. RFM
    print("\nStep 5: Segmentation (RFM)...")
    rfm_df = calculate_rfm(final_df)
    rfm_df['Segment'] = rfm_df.apply(segment_customer, axis=1)
    print("Segments Distribution:")
    print(rfm_df['Segment'].value_counts())
    
    # 4. Visualization
    print("\nStep 6: Generating Visualizations...")
    save_dir = os.path.join(project_root, 'reports', 'figures')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    print(f"Saving plots to {save_dir}...")
    # Note: These functions call plt.show(), might block if interactive.
    # We should adjust src to not show if saving, or just let it run.
    # For a script, we usually want save only.
    # But current src has show().
    try:
        import matplotlib.pyplot as plt
        plt.ioff() # Turn off interactive mode to avoid blocking
        plot_demographics(final_df, save_path=save_dir)
        plot_funnel(final_df, save_path=save_dir)
        plot_rfm(rfm_df, save_path=save_dir)
        
        from src.visualization import plot_channel_performance
        plot_channel_performance(final_df, portfolio, save_path=save_dir)
        
        print("Visualizations saved.")
    except Exception as e:
        print(f"Error visualizing: {e}")

    print("\n--- Pipeline Completed Successfully ---")

if __name__ == "__main__":
    run()
