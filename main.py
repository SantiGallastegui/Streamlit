import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 
import datetime as dt

st.set_page_config(page_title = "Criptomonedas",
                    page_icon=":boom:",
                    layout="wide")

st.write("""
# Analisis de las 10 criptomonedas más populares de FTX """ )

ETH = requests.get('https://ftx.com/api/markets/ETH/USD/candles?resolution=86400&start_time=30000000').json()
BTC = requests.get('https://ftx.com/api/markets/BTC/USD/candles?resolution=86400&start_time=30000000').json()
ATOM = requests.get('https://ftx.com/api/markets/ATOM/USD/candles?resolution=86400&start_time=30000000').json()
BNB = requests.get('https://ftx.com/api/markets/BNB/USD/candles?resolution=86400&start_time=30000000').json()
EUR = requests.get('https://ftx.com/api/markets/EUR/USD/candles?resolution=86400&start_time=30000000').json()
FTT = requests.get('https://ftx.com/api/markets/FTT/USD/candles?resolution=86400&start_time=30000000').json()
LINK = requests.get('https://ftx.com/api/markets/LINK/USD/candles?resolution=86400&start_time=30000000').json()
SOL = requests.get('https://ftx.com/api/markets/SOL/USD/candles?resolution=86400&start_time=30000000').json()
USDT = requests.get('https://ftx.com/api/markets/USDT/USD/candles?resolution=86400&start_time=30000000').json()
XRP = requests.get('https://ftx.com/api/markets/XRP/USD/candles?resolution=86400&start_time=30000000').json()

def filtros(df,var):
    df = pd.DataFrame(df['result'])
    df.drop(['startTime'], axis = 1 , inplace = True)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['Cripto']= var
    df['20 SMA'] = df.close.rolling(20).mean()
    return df 

ETH = filtros(ETH, "ETH")
BTC = filtros(BTC, "BTC")
ATOM = filtros(ATOM, "ATOM")
BNB = filtros(BNB, "BNB")
EUR = filtros(EUR, "EUR")
FTT = filtros(FTT, "FTT")
LINK = filtros(LINK, "LINK")
SOL = filtros(SOL, "SOL")
USDT = filtros(USDT, "USDT")
XRP = filtros(XRP, "XRP")

anexo = pd.concat([ETH,BTC,ATOM,BNB,EUR,FTT,LINK,SOL,USDT,XRP])


st.sidebar.header("Coloque los filtros : ")

cripto = st.sidebar.radio(
    "Select the Cripto",
    options=anexo['Cripto'].unique(),

)
cripto1 = st.sidebar.multiselect(
    "Comparar con",
    options=anexo['Cripto'].unique(),
    default=cripto,
)


#fecha = st.sidebar.slider(
#    "Seleccione la fecha",
#    min_value= anexo.time.min().year, max_value= anexo.time.max().year
#)

df_selection = anexo.query(
    "Cripto == @cripto1"
)

view = st.checkbox("View Dataframe")

if view :
    st.dataframe(df_selection.head(5))


fig = go.Figure(data=[go.Candlestick(x = df_selection['time'],
                                    open = df_selection['open'],
                                    high = df_selection['high'],
                                   low = df_selection['low'],
                                   close = df_selection['close'],
                                   ),
                    go.Scatter(x=df_selection['time'], y=df_selection['20 SMA'], line=dict(color='purple', width=1))])
fig.update_layout(title="Precio historicos",yaxis_title='USD')

st.plotly_chart(fig)

fig1 = go.Figure(data=[go.Scatter(x=df_selection['time'], y=df_selection['volume'], line=dict(color='purple', width=1))])
fig1.update_layout(title="Volumen",yaxis_title='Transacciones')

st.plotly_chart(fig1)