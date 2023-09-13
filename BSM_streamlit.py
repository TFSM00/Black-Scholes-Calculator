import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import streamlit.components.v1 as components

def blackScholes(S, K, r, T, sigma, type="c"):
    "Calculate Black Scholes option price for a call/put"
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

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
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
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
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        gamma = norm.pdf(d1, 0, 1)/ (S * sigma * np.sqrt(T))
        return gamma
    except:
        st.sidebar.error("Please confirm all option parameters!")

def optionTheta(S, K, r, T, sigma, type="c"):
    "Calculates option theta"
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        if type == "c":
            theta = - ((S * norm.pdf(d1, 0, 1) * sigma) / (2 * np.sqrt(T))) - r * K * np.exp(-r*T) * norm.cdf(d2, 0, 1)

        elif type == "p":
            theta = - ((S * norm.pdf(d1, 0, 1) * sigma) / (2 * np.sqrt(T))) + r * K * np.exp(-r*T) * norm.cdf(-d2, 0, 1)
        return theta/365
    except:
        st.sidebar.error("Please confirm all option parameters!")

def optionVega (S, K, r, T, sigma):
    "Calculates option vega"
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        vega = S * np.sqrt(T) * norm.pdf(d1, 0, 1) * 0.01
        return vega
    except:
        st.sidebar.error("Please confirm all option parameters!")

def optionRho(S, K, r, T, sigma, type="c"):
    "Calculates option rho"
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        if type == "c":
            rho = 0.01 * K * T * np.exp(-r*T) * norm.cdf(d2, 0, 1)
        elif type == "p":
            rho = 0.01 * -K * T * np.exp(-r*T) * norm.cdf(-d2, 0, 1)
        return rho
    except:
        st.sidebar.error("Please confirm all option parameters!")



st.set_page_config(page_title="Black-Scholes Model")

sidebar_title = st.sidebar.header("Black-Scholes Parameters")
space = st.sidebar.header("")
r = st.sidebar.number_input("Risk-Free Rate", min_value=0.000, max_value=1.000, step=0.001, value=0.030)
S = st.sidebar.number_input("Underlying Asset Price", min_value=1.00, step=0.10, value=30.00)
K = st.sidebar.number_input("Strike Price", min_value=1.00, step=0.10, value=50.00)
days_to_expiry = st.sidebar.number_input("Time to Expiry Date (in days)", min_value=1, step=1, value=250)
sigma = st.sidebar.number_input("Volatility", min_value=0.000, max_value=1.000, step=0.01, value=0.30)
type_input = st.sidebar.selectbox("Option Type",["Call", "Put"])

type=""
if type_input=="Call":
    type = "c"
elif type_input=="Put":
    type = "p"

T = days_to_expiry/365


spot_prices = [i for i in range(0, int(S)+50 + 1)]

prices = [blackScholes(i, K, r, T, sigma, type) for i in spot_prices]
deltas = [optionDelta(i, K, r, T, sigma, type) for i in spot_prices]
gammas = [optionGamma(i, K, r, T, sigma) for i in spot_prices]
thetas = [optionTheta(i, K, r, T, sigma, type) for i in spot_prices]
vegas = [optionVega(i, K, r, T, sigma) for i in spot_prices]
rhos = [optionRho(i, K, r, T, sigma, type) for i in spot_prices]

sns.set_style("whitegrid")

fig1, ax1 = plt.subplots()
sns.lineplot(x=spot_prices, y=prices)
ax1.set_ylabel('Option Price')
ax1.set_xlabel("Underlying Asset Price")
ax1.set_title("Option Price")

fig2, ax2 = plt.subplots()
sns.lineplot(x=spot_prices, y=deltas)
ax2.set_ylabel('Delta')
ax2.set_xlabel("Underlying Asset Price")
ax2.set_title("Delta")

fig3, ax3 = plt.subplots()
sns.lineplot(x=spot_prices, y=gammas)
ax3.set_ylabel('Gamma')
ax3.set_xlabel("Underlying Asset Price")
ax3.set_title("Gamma")

fig4, ax4 = plt.subplots()
sns.lineplot(x=spot_prices, y=thetas)
ax4.set_ylabel('Theta')
ax4.set_xlabel("Underlying Asset Price")
ax4.set_title("Theta")

fig5, ax5 = plt.subplots()
sns.lineplot(x=spot_prices, y=vegas)
ax5.set_ylabel('Vega')
ax5.set_xlabel("Underlying Asset Price")
ax5.set_title("Vega")

fig6, ax6 = plt.subplots()
sns.lineplot(x=spot_prices, y=rhos)
ax6.set_ylabel('Rho')
ax6.set_xlabel("Underlying Asset Price")
ax6.set_title("Rho")

fig1.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
fig4.tight_layout()
fig5.tight_layout()
fig6.tight_layout()


st.markdown("<h2 align='center'>Black-Scholes Option Price Calculator</h2>", unsafe_allow_html=True)
st.markdown("<h5 align='center'>Made by Tiago Moreira</h5>", unsafe_allow_html=True)
st.header("")
st.markdown("<h6>See project's description and assumptions here: <a href='https://github.com/TFSM00/Black-Scholes-Calculator'>https://github.com/TFSM00/Black-Scholes-Calculator</a></h6>", unsafe_allow_html=True)
st.markdown("<h6>See all my other projects here: <a href='https://github.com/TFSM00'>https://github.com/TFSM00</a></h6>", unsafe_allow_html=True)
st.header("")
st.markdown("<h3 align='center'>Option Prices and Greeks</h3>", unsafe_allow_html=True)
st.header("")
col1, col2, col3, col4, col5 = st.columns(5)
col2.metric("Call Price", str(round(blackScholes(S, K, r, T, sigma,type="c"), 3)))
col4.metric("Put Price", str(round(blackScholes(S, K, r, T, sigma,type="p"), 3)))

bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
bcol1.metric("Delta", str(round(blackScholes(S, K, r, T, sigma,type="c"), 3)))
bcol2.metric("Gamma", str(round(optionGamma(S, K, r, T, sigma), 3)))
bcol3.metric("Theta", str(round(optionTheta(S, K, r, T, sigma,type="c"), 3)))
bcol4.metric("Vega", str(round(optionVega(S, K, r, T, sigma), 3)))
bcol5.metric("Rho", str(round(optionRho(S, K, r, T, sigma,type="c"), 3)))

st.header("")
st.markdown("<h3 align='center'>Visualization of the Greeks</h3>", unsafe_allow_html=True)
st.header("")
st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)
st.pyplot(fig4)
st.pyplot(fig5)
st.pyplot(fig6)

