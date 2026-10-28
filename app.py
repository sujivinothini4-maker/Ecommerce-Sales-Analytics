
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import (
    load_data,
    get_sales_summary,
    get_product_sales,
    get_region_sales,
    save_to_database,
    get_database_sales,
    get_monthly_sales,
)
# Page configuration
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide",
)

# Dashboard title
st.title("🛒 E-Commerce Sales & Customer Insights Dashboard")
st.write("Analyze sales performance, products, and customer trends.")

# Load data
# Load default data
df = load_data()

# Allow users to upload their own sales dataset
st.sidebar.subheader("Upload Your Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    required_columns = [
        "Order_ID",
        "Product",
        "Category",
        "Quantity",
        "Unit_Price",
        "Customer_Age",
        "Region",
    ]

    if all(column in df.columns for column in required_columns):
        df["Sales"] = df["Quantity"] * df["Unit_Price"]
        st.sidebar.success("Dataset uploaded successfully!")
    else:
        st.error("Your CSV file is missing required columns.")
        st.stop()

# Sidebar filters
st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique()),
)

selected_product = st.sidebar.multiselect(
    "Select Product",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique()),
)

# Filter data
filtered_df = df[
    df["Region"].isin(selected_region)
    & df["Product"].isin(selected_product)
]

# Calculate metrics
summary = get_sales_summary(filtered_df)

st.subheader("📊 Sales Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{summary['total_sales']:,.0f}")
col2.metric("Total Orders", f"{summary['total_orders']:,}")
col3.metric("Average Order Value", f"₹{summary['average_order_value']:,.0f}")
col4.metric("Units Sold", f"{summary['total_quantity']:,}")

# Product sales chart
st.subheader("🏆 Sales by Product")

product_sales = get_product_sales(filtered_df)

fig1, ax1 = plt.subplots(figsize=(9, 4))
product_sales.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Product")
ax1.set_ylabel("Sales (₹)")
ax1.set_title("Product-wise Sales")
ax1.tick_params(axis="x", rotation=30)
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

# Regional sales chart
st.subheader("🌍 Sales by Region")

region_sales = get_region_sales(filtered_df)

fig2, ax2 = plt.subplots(figsize=(9, 4))
region_sales.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Region")
ax2.set_ylabel("Sales (₹)")
ax2.set_title("Region-wise Sales")
ax2.tick_params(axis="x", rotation=30)
fig2.tight_layout()

st.pyplot(fig2)
plt.close(fig2)

# Customer age analysis
st.subheader("👥 Customer Age Analysis")

fig3, ax3 = plt.subplots(figsize=(9, 4))
ax3.hist(filtered_df["Customer_Age"], bins=10, edgecolor="black")
ax3.set_xlabel("Customer Age")
ax3.set_ylabel("Number of Orders")
ax3.set_title("Distribution of Customer Ages")
fig3.tight_layout()

st.pyplot(fig3)
plt.close(fig3)

# Data table
st.subheader("📋 Sales Data")

st.dataframe(filtered_df, use_container_width=True)

# Download button
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Sales Data as CSV",
    data=csv_data,
    file_name="ecommerce_sales_data.csv",
    mime="text/csv",
)
# Customer Insights
st.header("👥 Customer Insights")

# Create customer age groups
customer_df = filtered_df.copy()

customer_df["Age_Group"] = pd.cut(
    customer_df["Customer_Age"],
    bins=[0, 25, 35, 50, 100],
    labels=["18-25", "26-35", "36-50", "50+"]
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Age Groups")

    age_counts = customer_df["Age_Group"].value_counts().sort_index()

    fig4, ax4 = plt.subplots(figsize=(7, 4))
    age_counts.plot(kind="bar", ax=ax4)
    ax4.set_xlabel("Age Group")
    ax4.set_ylabel("Number of Orders")
    ax4.set_title("Orders by Customer Age Group")
    ax4.tick_params(axis="x", rotation=0)
    fig4.tight_layout()

    st.pyplot(fig4)
    plt.close(fig4)

with col2:
    st.subheader("Product Purchase Quantities")

    product_quantity = (
        filtered_df.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(product_quantity)

# Automatic Business Insights
st.subheader("💡 Business Insights")

if not filtered_df.empty:
    best_product = get_product_sales(filtered_df).idxmax()
    best_region = get_region_sales(filtered_df).idxmax()

    st.write(f"🏆 **Top product by sales:** {best_product}")
    st.write(f"🌍 **Top region by sales:** {best_region}")

    st.write(
        f"💰 **Total revenue:** ₹{filtered_df['Sales'].sum():,.2f}"
    )

    st.write(
        f"🛒 **Total units sold:** {filtered_df['Quantity'].sum():,}"
    )
else:
    st.info("No records match the selected filters.")


st.success("Dashboard loaded successfully!")
# SQL Database Integration
st.header("🗄️ SQL Database")

if st.button("Save Sales Data to Database"):
    try:
        save_to_database(filtered_df)
        st.success("Sales data saved successfully to ecommerce.db!")
    except Exception as e:
        st.error(f"Database error: {e}")
        # SQL Query Analysis
st.header("📊 SQL Database Analysis")

if st.button("Run SQL Sales Analysis"):
    try:
        sql_results = get_database_sales()

        st.subheader("Product-wise Sales from SQL Database")
        st.dataframe(sql_results, use_container_width=True)

        if not sql_results.empty:
            st.bar_chart(
                sql_results.set_index("Product")["Total_Sales"]
            )

            top_product = sql_results.iloc[0]["Product"]
            st.success(f"Top product by sales: {top_product}")
        else:
            st.info("No sales records found in the database.")

    except Exception as e:
        st.error(
            "Unable to read the database. Save sales data to the "
            f"database first. Details: {e}"
        )
        
# Monthly Sales Trend Analysis
st.header("📈 Monthly Sales Trend")

if "Order_Date" in filtered_df.columns:
    monthly_sales = get_monthly_sales(filtered_df)

    if not monthly_sales.empty:
        st.line_chart(monthly_sales)

        best_month = monthly_sales.idxmax()
        best_month_sales = monthly_sales.max()

        st.success(
            f"Best sales month: {best_month} "
            f"(₹{best_month_sales:,.2f})"
        )
    else:
        st.info("No valid order dates are available.")
else:
    st.info("The dataset needs an Order_Date column.")
