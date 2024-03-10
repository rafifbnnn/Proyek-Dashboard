import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from scipy import stats
from scipy.interpolate import make_interp_spline
import plotly.graph_objs as go
import streamlit as st

# Import dataset
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

# Tipe data menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Menangani outlier
def handle_outliers(df, column):
    Q1, Q3 = np.percentile(df[column], [25, 75])
    IQR = Q3 - Q1

    upper_bound = Q3 + (1.5 * IQR)
    lower_bound = Q1 - (1.5 * IQR)

    more_than = df[column] > upper_bound
    lower_than = df[column] < lower_bound

    df[column] = np.where(more_than, upper_bound, df[column])
    df[column] = np.where(lower_than, lower_bound, df[column])

# day_df
handle_outliers(day_df, 'hum')
handle_outliers(day_df, 'windspeed')
# hour_df
handle_outliers(hour_df, 'hum')
handle_outliers(hour_df, 'windspeed')

st.image("dashboard/pokemon-bike.png", use_column_width=True)
st.header("FBN Bike Sharing Dashboard :sparkle:")

tab1, tab2 = st.tabs(["Average Rentals per Day", "Relation between Temperature, Humidity and Rentals"])

with tab1:
    hourly_rentals = hour_df.groupby('hr')['cnt'].mean()

    colors = ['#ffc77d'] * len(hourly_rentals)
    colors[17] = '#ff7f0e'  # Hour dengan rataan penyewaan tertinggi

    trace_bar = go.Bar(
        x=hourly_rentals.index,
        y=hourly_rentals.values,
        marker=dict(color=colors),
        name='Average Rentals'
    )

    # Interpolasi kurva densitas
    x_new = np.linspace(hourly_rentals.index.min(), hourly_rentals.index.max(), 500)
    spl = make_interp_spline(hourly_rentals.index, hourly_rentals.values, k=3)
    y_smooth = spl(x_new)

    trace_density = go.Scatter(
        x=x_new,
        y=y_smooth,
        mode='lines',
        line=dict(color='brown'),
        fill='none',
        name='Density'
    )

    layout = go.Layout(
        title='Rataan Penyewaaan Sepeda per Hari',
        xaxis=dict(title='Hour', tickvals=np.arange(0, 25), ticktext=[str(i) for i in range(0, 25)]),
        yaxis=dict(title='Average Rentals')
    )

    fig = go.Figure(data=[trace_bar, trace_density], layout=layout)

    st.plotly_chart(fig)

    with st.expander(label='See Explanation', expanded=False):
        st.write('''Berdasarkan visualisasi di atas, dapat dilihat bahwa rata-rata penyewaaan sepeda yang tinggi berada pada jam berangkat dan pulang kerja.
                 Sementara itu, rata-rata penyewaaan sepeda yang rendah berada pada waktu orang-orang sedang beristirahat.
                 ''')

    st.write("Psst, you can actively interact with the plot ;)", fontsize=14)
    
with tab2:
    st.subheader("Temperature (Left) vs Humidity (Right)")

    sns.set_palette('crest')
    fig, ax = plt.subplots(ncols=2, figsize=(20, 8))  # Mengatur ukuran lebar menjadi 20

    sns.regplot(x=hour_df['temp'], y=hour_df['cnt'], ax=ax[0],
                color='deeppink', line_kws={"color": "#2654a1"},
                scatter_kws=dict(alpha=0.5, s=5))
    ax[0].set_xlabel("Temperature", fontsize=16)
    ax[0].set_ylabel("Number of Rentals", fontsize=16) 

    sns.regplot(x=hour_df['hum'], y=hour_df['cnt'], ax=ax[1],
                scatter_kws=dict(alpha=0.5, s=5), line_kws={"color": "red"})
    ax[1].set_xlabel("Humidity", fontsize=16)
    ax[1].set_ylabel("Number of Rentals", fontsize=16) 

    plt.tight_layout()
    
    st.pyplot(fig)  # Menampilkan plot dengan lebar 20

    with st.expander(label='See Explanation', expanded=False):
        st.write('''Visualisasi di atas merupakan plot regresi yang menunjukkan hubungan antara temperature dengan penyewaaan sepeda (kiri) dan kelembaban udara dengan penyewaan sepeda (kanan).
                 \nTemperature memiliki korelasi positif dengan penyewaaan sepeda, di mana semakin tinggi temperature, semakin tinggi jumlah penyewaan sepeda.
                \nKelembaban udara memiliki korelasi negatif dengan penyewaan sepeda, di mana semakin tinggi kelembaban udara, semakin rendah jumlah penyewaan sepeda.
                 ''')

st.caption('\nRafi Fabian Syah - M001D4KY2231')