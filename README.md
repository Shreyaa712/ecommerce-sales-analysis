# E-commerce Sales Analysis

An end-to-end e-commerce sales analysis project built in Python, using a cleaned online retail dataset and a Streamlit dashboard for interactive business intelligence.

## Overview

This repository analyzes retail transaction data to uncover:

- Monthly sales trends
- Best-performing countries and regions
- Top-selling products
- High-value customers
- Data quality issues such as cancellations and negative sales

The project combines:

- Data cleaning and preprocessing
- Exploratory data analysis in Jupyter notebooks
- An interactive Streamlit dashboard for reporting

## Project Structure

```text
.
├── dashboard.py                  # Streamlit dashboard application
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
├── data/
│   └── processed/
│       └── online_retail_cleaned.csv
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 03Data_integration.ipynb
│   ├── 05_eda.ipynb
│
├── visuals/                     # Project visuals/assets
└── README.md                    # Project documentation
```

## Dashboard Features

The dashboard includes:

- Total sales, invoice counts, customer counts, and average sales metrics
- Monthly sales trend visualization
- Top 10 countries by revenue
- Top 10 products by sales
- Top 10 customers by revenue
- Business insights cards
- Data quality explanations for cancellations and negative values

## Dataset

The analysis uses the processed retail dataset located at:

- `data/processed/online_retail_cleaned.csv`

This dataset contains cleaned online retail transaction data, including fields such as:

- Invoice date
- Invoice number
- Country
- Customer ID
- Product description
- Quantity
- Unit price
- Total sales

## Tech Stack

- Python
- Pandas
- Plotly
- Streamlit
- Jupyter Notebook
- OpenPyXL

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Shreyaa712/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

Start the Streamlit application:

```bash
streamlit run dashboard.py
```

Then open the local URL shown in the terminal, typically:

```text
http://localhost:8501
```

## Notebook Workflow

The notebooks in `notebooks/` cover the analytical workflow, including:

- Data understanding
- Data integration
- Exploratory data analysis

## Key Business Questions

This project is designed to answer questions like:

- Which countries drive the most revenue?
- What are the strongest sales months?
- Which products generate the highest value?
- Which customers contribute the most to sales?
- Are there anomalies such as returns or cancellations affecting revenue?

## License

This project does not currently include a license file.

## Author

Created by Shreya Salunkhe

## Notes

The dashboard is built for retail analytics and can be extended with additional features such as:

- Customer segmentation
- Product category analysis
- Forecasting
- Exportable reports
- Database-backed deployment
