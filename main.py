import time
import streamlit as st
from api.coingecko import get_coins, get_price_history


st.set_page_config(page_title="Cryptocurrency Tracker", layout="wide")
st.title("Trader view")

currency = st.sidebar.selectbox("Select currency", ['USD', 'EUR', 'JPY', 'GBP'])
coins = get_coins(currency)

if coins:
    coin_names = [f"{coin.name} ({coin.symbol.upper()})" for coin in coins]
    selected_coin = st.sidebar.selectbox("Select coin", coin_names)
    coin_obj = coins[coin_names.index(selected_coin)]

    st.subheader(f"{coin_obj.name} ({coin_obj.symbol.upper()})")
    st.metric("Current Price", f"{coin_obj.current_price:,.2f} {currency.upper()}")

    column1, column2, column3 = st.columns(3)
    column1.metric("24h High", f"{coin_obj.high_24h:,.2f}")
    column2.metric("24h Low", f"{coin_obj.low_24h:,.2f}")
    column3.metric("Change (24h)", f"{coin_obj.price_change_percentage_24h:,.2f} %")

    df_history = get_price_history(coin_obj.id, vs_currency=currency)
    if not df_history.empty:
        st.line_chart(df_history.set_index('timestamp')['price'])
    else:
        st.info("No history available")
else:
    st.error("No cryptocurrency information available")


with st.empty():
    for i in range(60, 0, -1):
        st.info(f" Refreshing in {i} seconds")
        time.sleep(1)
    st.rerun()


