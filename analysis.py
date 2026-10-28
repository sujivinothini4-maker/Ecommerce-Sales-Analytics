import pandas as pd
import sqlite3
from pathlib import Path

def load_data():
    """Load e-commerce sales data from a CSV file."""

    file_path = Path(__file__).parent / "ecommerce_data.csv"

    df = pd.read_csv(file_path)

    # Calculate sales for each order
    df["Sales"] = df["Quantity"] * df["Unit_Price"]

    return df


def get_sales_summary(df):
    """Calculate important sales metrics."""

    return {
        "total_sales": df["Sales"].sum(),
        "total_orders": df["Order_ID"].nunique(),
        "average_order_value": df["Sales"].mean(),
        "total_quantity": df["Quantity"].sum(),
    }


def get_product_sales(df):
    """Calculate sales for each product."""

    return (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )


def get_region_sales(df):
    """Calculate sales for each region."""

    return (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )
def save_to_database(df):
    """Save sales data to a SQLite database."""

    db_path = Path(__file__).parent / "ecommerce.db"

    with sqlite3.connect(db_path) as connection:
        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False
        )
def get_database_sales():
    """Retrieve sales records using an SQL query."""

    db_path = Path(__file__).parent / "ecommerce.db"

    with sqlite3.connect(db_path) as connection:
        query = """
            SELECT
                Product,
                SUM(Quantity) AS Total_Quantity,
                SUM(Sales) AS Total_Sales
            FROM sales
            GROUP BY Product
            ORDER BY Total_Sales DESC
        """

        result = pd.read_sql_query(query, connection)

    return result
def get_monthly_sales(df):
    """Calculate total sales for each month."""

    df = df.copy()

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    df = df.dropna(subset=["Order_Date"])

    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

    monthly_sales = (
        df.groupby("Month")["Sales"]
        .sum()
        .sort_index()
    )

    return monthly_sales



