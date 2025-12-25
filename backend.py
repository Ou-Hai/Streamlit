import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


@st.cache_data
def load_data():
    data = pd.read_csv("supermarket_sales.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    return data


def get_summary(data):
    summary = pd.DataFrame(
        {
            "Total Sales": [data["Total"].sum()],
            "Average Rating": [data["Rating"].mean()],
            "Total Transactions": [data["Invoice ID"].nunique()],
        }
    )
    return summary


def plot_sales_over_time(data):
    data["Date"] = pd.to_datetime(data["Date"])
    sales_over_time = data.groupby(data["Date"].dt.date)["Total"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sales_over_time.index, sales_over_time.values)
    ax.set_title("Sales Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()

    return fig
