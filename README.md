# E-Commerce Sales & Customer Insights Dashboard

## Project Overview

An interactive data analytics dashboard built using Python to analyze e-commerce sales, product performance, regional revenue, customer patterns, and monthly sales trends.

**Note:** The project currently uses a small illustrative sample dataset. It is intended for educational and portfolio purposes.

## Features

* Sales revenue and order summary
* Product-wise sales analysis
* Region-wise sales analysis
* Customer age-group analysis
* Monthly sales trend visualization
* CSV dataset upload
* Interactive product and region filters
* CSV export
* SQLite database integration
* SQL-based product performance analysis
* Automatic business insights

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Streamlit
* SQLite
* SQL
* CSV

## Project Structure

```text
Ecommerce_Sales_Analytics/
├── app.py
├── analysis.py
├── ecommerce_data.csv
├── ecommerce.db
├── requirements.txt
└── README.md
```

## Installation

1. Install Python.

2. Open the project folder in VS Code.

3. Install the required libraries:

   `py -m pip install pandas numpy matplotlib streamlit`

4. Run the dashboard:

   `py -m streamlit run app.py`

5. Open the local URL displayed in the terminal.

## Dataset

The included CSV file contains illustrative order records with product, category, quantity, price, customer age, region, and order date.

Users can upload another CSV file containing the required columns.

## Learning Outcomes

* Data cleaning and transformation
* Exploratory data analysis
* Data visualization
* SQL queries and database integration
* Interactive dashboard development
* Business insight generation

## Future Improvements

* Analyze a larger real-world dataset
* Add customer segmentation
* Improve data validation and error handling
* Add profit and discount analysis
* Deploy the dashboard online

## Disclaimer

The included data is illustrative and does not represent actual customer transactions.
