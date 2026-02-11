# Customer Segmentation & Marketing Analysis - Gelateria Lillo

Project focused on **data analysis, customer segmentation (RFM), and marketing efficacy visualization** for a fictional business case (Gelateria Lillo).

## 🚀 Overview
This repository contains the full data pipeline, from raw data ingestion to insightful visualizations. The goal is to maximize marketing ROI by understanding customer behavior and optimizing campaign targeting.

### Key Features
- **Data Pipeline**: Automated ETL process using Python and Pandas.
- **KPI Calculation**: Ticket Average, Channel Conversion Rates, Revenue Attribution.
- **RFM Segmentation**: Classification of customers into segments like *Champions*, *Loyal*, *At Risk*, etc.
- **Visualization**: Funnels, demographic distributions, and channel performance charts using Seaborn/Matplotlib.

## 📂 Project Structure
```
├── data/               # Raw CSV datasets
├── scripts/            # Executable scripts (main entry points)
│   └── run_pipeline.py # Main pipeline script
├── src/                # Source code modules
│   ├── data_loader.py  # Data loading and cleaning
│   ├── kpis.py         # Business logic and metrics
│   └── visualization.py# Plotting functions
├── reports/            # Generated reports and figures
│   ├── figures/        # PNG exports of visualizations
│   └── gallery.md      # Gallery of insights
└── requirements.txt    # Project dependencies
```

## 🛠️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/customer-segmentation-analysis.git
   cd customer-segmentation-analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis pipeline:**
   ```bash
   python scripts/run_pipeline.py
   ```
   This will process the data, calculate KPIs, print results to the console, and generate visualization images in `reports/figures/`.

## 📊 Results Preview
Check out the [Gallery of Insights](reports/figures/gallery.md) for detailed explanations of the findings.

### Example: Conversion Funnel
The analysis revealed significant drop-offs in specific offer types, leading to recommendations for optimizing the reward structure.

## 📝 License
This project is for educational/portfolio purposes.
