import streamlit as st
from sections.crypto_wallet import crypto_wallet_section
from sections.fiat_wallet import fiat_wallet_section
from sections.footer import footer_section
from sections.header import header_section
from sections.overview import overview_section
from sections.sidebar import sidebar_section
from sections.visa_card import visa_card_section

st.set_page_config(initial_sidebar_state='expanded')

sidebar_section()

header_section()

overview_section()

visa_card_section()

crypto_wallet_section()

fiat_wallet_section()

footer_section()