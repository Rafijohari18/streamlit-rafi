import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_daily_orders_df(df):
    # Konversi kolom 'order_delivered_customer_date_x' ke tipe data datetime
    df['order_delivered_customer_date_x'] = pd.to_datetime(df['order_delivered_customer_date_x'])

    # Set kolom 'order_delivered_customer_date_x' sebagai indeks
    df.set_index('order_delivered_customer_date_x', inplace=True)

    # Resample berdasarkan hari dan melakukan agregasi
    daily_orders_df = df.resample(rule='D').agg({
        "order_id": "nunique",
        "price": "sum"
    })

    # Reset indeks
    daily_orders_df = daily_orders_df.reset_index()

    # Ubah nama kolom
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)

    return daily_orders_df


def create_bypayment_df(df):
    bypayment_df = df.groupby(by="payment_type").order_id.nunique().reset_index()
    bypayment_df.rename(columns ={
    "order_id": "order_count"
}, inplace=True)
    return bypayment_df

all_df = pd.read_csv("dashboard/all_data.csv")

bypayment_df = create_bypayment_df(all_df)
daily_orders_df = create_daily_orders_df(all_df)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

st.header('Dicoding Collection Dashboard :sparkles:')

st.subheader("Customer Demographics")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="order_count",
        x="payment_type",
        data=bypayment_df.sort_values(by="order_count", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Customer by Payment", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

st.caption('Copyright (c) Dicoding 2023')
