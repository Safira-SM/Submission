import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    orders_df = pd.read_csv('C:\\Users\\Hp\\Documents\\Visual Studio Code\\Dashboard\\orders.csv')
    orders_payments_df = pd.read_csv('C:\\Users\\Hp\\Documents\\Visual Studio Code\\Dashboard\\orders_payments.csv')
    customers_df = pd.read_csv('C:\\Users\\Hp\\Documents\\Visual Studio Code\\Dashboard\\customers.csv')
    orders_reviews_df = pd.read_csv('C:\\Users\\Hp\\Documents\\Visual Studio Code\\Dashboard\\order_reviews_dataset.csv')
    return orders_df, orders_payments_df, customers_df, orders_reviews_df

def average_customers_per_payment(orders_df, orders_payments_df, customers_df):
    merged_orders = pd.merge(orders_df, orders_payments_df, on='order_id', how='inner')
    final_merged = pd.merge(merged_orders, customers_df, on='customer_id', how='inner')
    average_customers_per_payment = final_merged.groupby(['customer_city', 'payment_type']).agg({
        'customer_id' : 'nunique'
    }).reset_index()

    average_customers_per_payment = average_customers_per_payment.groupby('payment_type').agg({
        'customer_id' : 'mean'
    }).reset_index()

    average_customers_per_payment.columns = ['payment_type', 'average_unique_customers']
    return average_customers_per_payment

def plot_review_distribution(orders_reviews_df):
    plt.figure(figsize=(8, 6))
    plt.hist(orders_reviews_df['review_score'], bins=5, color='skyblue', edgecolor='black')
    plt.xlabel('Rating Pelanggan')
    plt.ylabel('Jumlah Pelanggan')
    plt.title('Distribusi Rating Pelanggan')
    plt.xticks(range(1, 6))
    st.pyplot(plt)

def main():
    st.title('Analisis Data Pelanggan dan Pembayaran')

    orders_df, orders_payments_df, customers_df, orders_reviews_df = load_data()

    average_customers = average_customers_per_payment(orders_df, orders_payments_df, customers_df)

    st.subheader('Rata-rata Jumlah Pelanggan Per Jenis Pembayaran')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='payment_type', y='average_unique_customers', data=average_customers, ax=ax)
    ax.set_title('Rata-ratta Jumlah Pelanggan Per Jenis Pembayaran')
    ax.set_xlabel('Jenis Pembayaran')
    ax.set_ylabel('Rata-rata JUmlah Pelanggan')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    payment_type = st.selectbox('Pilih Jenis Pembayaran untuk Melihat Distribusi Rating Pelanggan', average_customers['payment_type'].unique())

    filtered_orders = pd.merge(orders_df, orders_payments_df[orders_payments_df ['payment_type'] == payment_type], on='order_id')
    filtered_reviews = pd.merge(filtered_orders, orders_reviews_df, on='order_id')

    st.subheader(f'Distribusi Rating Pelanggan untuk Pembayaran : {payment_type}')
    plot_review_distribution(filtered_reviews)


if __name__ == "__main__" :
    main()