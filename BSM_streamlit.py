import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import streamlit as st


def blackScholes(S, K, r, T, sigma, type="c"):
    "Calculate Black Scholes option price for a call/put"

    try:
        if type == "c":
            price = S * norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * norm.cdf(d2, 0, 1)
        elif type == "p":
            price = K * np.exp(-r * T) * norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)

        return price
    except:  
        st.sidebar.error("Please confirm all option parameters!")


def optionDelta (S, K, r, T, sigma, type="c"):
    "Calculates option delta"

    try:
        if type == "c":
            delta = norm.cdf(d1, 0, 1)
        elif type == "p":
            delta = -norm.cdf(-d1, 0, 1)

        return delta
    except:
        st.sidebar.error("Please confirm all option parameters!")

def optionGamma (S, K, r, T, sigma):
    "Calculates option gamma"
    
    try:
        gamma = norm.pdf(d1, 0, 1)/ (S * sigma * np.sqrt(T))
        return gamma
    except:
        st.sidebar.error("Please confirm all option parameters!")

def optionTheta(S, K, r, T, sigma, type="c"):
    "Calculates option theta"

    try:
        if type == "c":
            theta = -S * (norm.pdf(d1, 0, 1) * sigma / (2 * np.sqrt(T))) - r * K * np.exp(-r*T) * norm.cdf(d2, 0, 1)

        elif type == "p":
            theta = -S * (norm.pdf(d1, 0, 1) * sigma / (2 * np.sqrt(T))) + r * K * np.exp(-r*T) * norm.cdf(-d2, 0, 1)
        return theta/365
    except:
        st.sidebar.error("Please confirm all option parameters!")

def optionVega (S, K, r, T, sigma):
    "Calculates option vega"
    
    try:
        vega = S * np.sqrt(T) * norm.pdf(d1, 0, 1) * 0.01
        return vega
    except:
        st.sidebar.error("Please confirm all option parameters!")

def optionRho(S, K, r, T, sigma, type="c"):
    "Calculates option rho"

    try:
        if type == "c":
            rho = 0.01 * K * T * np.exp(-r*T) * norm.cdf(d2, 0, 1)
        elif type == "p":
            rho = 0.01 * -K * T * np.exp(-r*T) * norm.cdf(-d2, 0, 1)
        return rho
    except:
        st.sidebar.error("Please confirm all option parameters!")



st.set_page_config(page_title="Black-Scholes-Merton Model")

sidebar_title = st.sidebar.header("Black-Scholes-Merton Visualization")
author = st.sidebar.write("Made by Tiago Moreira")
space = st.sidebar.header("")
r = st.sidebar.number_input("Risk-Free Rate", min_value=0.000, max_value=1.000, step=0.001, value=0.030)
S = st.sidebar.number_input("Underlying Asset Price", min_value=1.00, step=0.10, value=30.00)
K = st.sidebar.number_input("Strike Price", min_value=1.00, step=0.10, value=50.00)
days_to_expiry = st.sidebar.number_input("Days left until Expiry Date", min_value=1, step=1, value=250)
sigma = st.sidebar.number_input("Volatility", min_value=0.000, max_value=1.000, step=0.01, value=0.30)
type_input = st.sidebar.selectbox("Option Type",["Call", "Put"])

type=""
if type_input=="Call":
    type = "c"
elif type_input=="Put":
    type = "p"

T = days_to_expiry/365

d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

run_button = st.sidebar.button("Run calculations")

days_array = [i for i in range(1, days_to_expiry + 1)]
days_array.sort(reverse=True)

prices = [blackScholes(S, K, r, i, sigma, type) for i in days_array]
deltas = [optionDelta(S, K, r, i, sigma, type) for i in days_array]
gammas = [optionGamma(S, K, r, i, sigma) for i in days_array]
thetas = [optionTheta(S, K, r, i, sigma, type) for i in days_array]
vegas = [optionVega(S, K, r, i, sigma) for i in days_array]
rhos = [optionRho(S, K, r, i, sigma, type) for i in days_array]

fig1, ax1 = plt.subplots()
ax1.plot(days_array, prices)
ax1.invert_xaxis()
ax1.set_title("Option Price")

fig2, ax2 = plt.subplots()
ax2.plot(days_array, deltas)
ax2.invert_xaxis()
ax2.set_title("Delta")

fig3, ax3 = plt.subplots()
ax3.plot(days_array, gammas)
ax3.invert_xaxis()
ax3.set_title("Gamma")

fig4, ax4 = plt.subplots()
ax4.plot(days_array, thetas)
ax4.invert_xaxis()
ax4.set_title("Theta")

fig5, ax5 = plt.subplots()
ax5.plot(days_array, vegas)
ax5.invert_xaxis()
ax5.set_title("Vega")

fig6, ax6 = plt.subplots()
ax6.plot(days_array, rhos)
ax6.invert_xaxis()
ax6.set_title("Rho")


if run_button:
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
    st.pyplot(fig4)
    st.pyplot(fig5)
    st.pyplot(fig6)
