import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import cartopy.crs as ccrs
import cartopy
from mpl_toolkits.basemap import Basemap

st.title("Brazilian E-Commerce Dashboard :sparkle: :sparkle:")

dataPath = "D:/College Stuff/IPB University/Bangkit/Dicoding/Belajar Analisis Data dengan Python/Proyek/Proyek E-Commerce/"

customers = pd.read_csv(dataPath + "customers_dataset.csv")
geolocation = pd.read_csv(dataPath + "geolocation_dataset.csv")
orders = pd.read_csv(dataPath + "orders_dataset.csv")
order_items = pd.read_csv(dataPath + "order_items_dataset.csv")
order_payments = pd.read_csv(dataPath + "order_payments_dataset.csv")
order_reviews = pd.read_csv(dataPath + "order_reviews_dataset.csv")
products = pd.read_csv(dataPath + "products_dataset.csv")
product_cat_name_trans = pd.read_csv(dataPath + "product_category_name_translation.csv")
sellers = pd.read_csv(dataPath + "sellers_dataset.csv")

products = products.merge(product_cat_name_trans, left_on='product_category_name', right_on='product_category_name',how='left')

geolocation = geolocation.drop_duplicates()

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

order_items['shipping_limit_date'] = pd.to_datetime(order_items['shipping_limit_date'])

order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
order_reviews['review_answer_timestamp'] = pd.to_datetime(order_reviews['review_answer_timestamp'])

orders['year'] = orders['order_purchase_timestamp'].dt.strftime('%Y')
orders['month'] = orders['order_purchase_timestamp'].dt.strftime('%m-%Y')
orders['day'] = orders['order_purchase_timestamp'].dt.strftime('%d-%m-%Y')

sorted_orders = orders.sort_values(by='month')
orders_datetime = sorted_orders.groupby(by=["month","year"]).order_id.nunique().reset_index()
orders_datetime = orders_datetime.sort_values(by=['year', 'month'])
orders_datetime['month'] = pd.to_datetime(orders_datetime['month'], format='%m-%Y')
orders_datetime = orders_datetime.sort_values('month')

products = products.fillna("unknown")
order_reviews = order_reviews.fillna("-")

selected_viz = st.selectbox("Map Visualization Style", ["Cartopy", "Basemap 1", "Basemap 2"])

if selected_viz == "Cartopy":
    st.subheader('Peta Persebaran Pembelian Produk (Cartopy)')
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(projection=ccrs.PlateCarree()))

    lat = geolocation['geolocation_lat']
    lon = geolocation['geolocation_lng']

    ax.stock_img()
    ax.coastlines()

    ax.add_feature(cartopy.feature.BORDERS, linestyle='--', alpha=0.75)
    ax.set_extent([-75, -30, -35, 6])
    ax.scatter(lon, lat, zorder=10, alpha=0.5, color='tomato', s=1.5)
    ax.axis('off')

    plt.tight_layout(w_pad=5, h_pad=5)
    st.pyplot(fig)

elif selected_viz == "Basemap 1":
    st.subheader('Peta Persebaran Pembelian Produk (Basemap 1)')
    fig, ax = plt.subplots(figsize=(10, 5))

    lat = geolocation['geolocation_lat']
    lon = geolocation['geolocation_lng']

    m = Basemap(llcrnrlat=-35,
                llcrnrlon=-75,
                urcrnrlat=6,
                urcrnrlon=-30,
                resolution='l')
    m.bluemarble()
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')

    m.drawcountries()
    m.scatter(lon, lat, zorder=10, alpha=0.5, color='tomato', s=1)

    plt.tight_layout(w_pad=5, h_pad=5)
    st.pyplot(fig)

elif selected_viz == "Basemap 2":
    st.subheader('Peta Persebaran Pembelian Produk (Basemap 2)')
    fig, ax = plt.subplots(figsize=(10, 5))

    lat = geolocation['geolocation_lat']
    lon = geolocation['geolocation_lng']

    m = Basemap(llcrnrlat=-35,
                llcrnrlon=-75,
                urcrnrlat=6,
                urcrnrlon=-30,
                resolution='l')
    m.bluemarble()
    m.drawmapboundary(fill_color='#a5c5de')
    m.fillcontinents(color='#f2f2f2', lake_color='#a5c5de')
    m.drawcountries()

    sc = m.scatter(lon, lat, zorder=10, alpha=0.5,
                   c=geolocation.index, cmap='flare', s=1)

    clrbar = plt.colorbar(sc, label='Jumlah', shrink=0.6)
    clrbar.set_label('Jumlah Pembelian', fontsize=13)
    plt.tight_layout(w_pad=5, h_pad=5)
    st.pyplot(fig)

with st.expander("See Explanation"):
    st.write(
        "Visualisasi peta menunjukkan persebaran pembeli di mana negara bagian daerah pesisir pantai timur Brazil memiliki tingkat pembelian produk yang tinggi."
    )



st.subheader('State vs Number of Products Purchased')

fig3 = plt.figure(figsize=(16, 8))
ax3 = sns.countplot(x='geolocation_state', data=geolocation, 
                   order=geolocation['geolocation_state'].value_counts().sort_values().index,
                   palette='flare')
ax3.set_xlabel("State", fontsize=14)
ax3.set_ylabel("Orders", fontsize=14)

st.pyplot(fig3)

with st.expander("See Explanation"):
    st.write(
        "Berdasarkan visualisasi di atas, dapat dilihat bahwa São Paulo memiliki jumlah order produk tertinggi dibandingkan negara bagian lainnya di mana terdapat ketimpangan yang besar."
    )



st.subheader('Product Sale Trend')

fig4 = plt.figure(figsize=(16, 8))
ax4 = sns.lineplot(x='month', y='order_id', data=orders_datetime,
                  linewidth=2, color='purple')
ax4.set_xticks(orders_datetime['month'])
ax4.set_xticklabels(orders_datetime['month'].dt.strftime('%m-%Y'), rotation=45)

plt.ylabel("Orders", fontsize=14)
plt.xlabel("Date", fontsize=14)
st.pyplot(fig4)

with st.expander("See Explanation"):
    st.write(
        "Secara garis besar, visualisasi line plot tersebut menunjukkan bahwa penjualan produk di Brazil memiliki tren penjualan positif, di mana kenaikan terbesar berada pada bulan November 2011."
    )


st.caption('Rafi Fabian Syah - M001D4KY2231')