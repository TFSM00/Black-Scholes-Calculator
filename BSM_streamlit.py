import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import streamlit as st


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
        print("Please confirm all option parameters!")


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
        print("Please confirm all option parameters!")

def optionGamma (S, K, r, T, sigma):
    "Calculates option gamma"
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        gamma = norm.pdf(d1, 0, 1)/ (S * sigma * np.sqrt(T))
        return gamma
    except:
        print("Please confirm all option parameters!")

def optionTheta(S, K, r, T, sigma, type="c"):
    "Calculates option theta"
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    try:
        if type == "c":
            theta = -S * (norm.pdf(d1, 0, 1) * sigma / (2 * np.sqrt(T))) - r * K * np.exp(-r*T) * norm.cdf(d2, 0, 1)

        elif type == "p":
            theta = -S * (norm.pdf(d1, 0, 1) * sigma / (2 * np.sqrt(T))) + r * K * np.exp(-r*T) * norm.cdf(-d2, 0, 1)
        return theta/365
    except:
        print("Please confirm all option parameters!")

def optionVega (S, K, r, T, sigma):
    "Calculates option vega"
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        vega = S * np.sqrt(T) * norm.pdf(d1, 0, 1) * 0.01
        return vega
    except:
        print("Please confirm all option parameters!")

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
        print("Please confirm all option parameters!")

# print("Option Price: ", blackScholes(S, K, r, T, sigma, type="c"))
# print("Option Delta: ", optionDelta(S, K, r, T, sigma, type="c"))
# print("Option Gamma: ", optionGamma(S, K, r, T, sigma))
# print("Option Theta: ", optionTheta(S, K, r, T, sigma, type="c"))
# print("Option Vega: ", optionVega(S, K, r, T, sigma))
# print("Option Rho: ", optionRho(S, K, r, T, sigma, type="c"))






st.set_page_config(page_title="Black-Scholes", layout="wide")

sidebar_title = st.sidebar.header("Black-Scholes Visualization")
author = st.sidebar.write("Made by Tiago Moreira")
space = st.sidebar.header("")
r = st.sidebar.number_input("Risk-Free Rate", min_value=0.000, max_value=1.000, step=0.0001, value=0.03)
S = st.sidebar.number_input("Underlying Asset Price", min_value=1.00, step=0.01, value=30.00)
K = st.sidebar.number_input("Strike Price", min_value=1.00, step=0.01, value=50.00)
days_to_expiry = st.sidebar.number_input("Days left until Expiry Date", min_value=1, step=1, value=250)
sigma = st.sidebar.number_input("Volatility", min_value=0.000, max_value=1.000, step=0.0001, value=0.30)
type_input = st.sidebar.selectbox("Option Type",["Call", "Put"])

type=""
if type_input=="Call":
    type = "c"
elif type_input=="Put":
    type = "p"

T = days_to_expiry/365

run_button = st.sidebar.button("Run calculations")

days_array = [i for i in range(1, days_to_expiry + 1)]
days_array.sort(reverse=True)
underlying_price_var = [i for i in range(1, 101)]
strike_var = [i for i in range(1, 101)]
risk_free_var = np.linspace(0.0001, 0.25, 100)



variable = days_array

prices = []
deltas = []
gammas = []
thetas = []
vegas = []
rhos = []

if variable == days_array:
    for i in variable:
        i = i/365
        prices.append(blackScholes(S, K, r, i, sigma, type))
        deltas.append(optionDelta(S, K, r, i, sigma, type))
        gammas.append(optionGamma(S, K, r, i, sigma))
        thetas.append(optionTheta(S,K, r, i, sigma, type))
        vegas.append(optionVega(S, K, r, i, sigma))
        rhos.append(optionRho(S, K, r, i, sigma, type))
elif variable == underlying_price_var:
    for i in variable:
        prices.append(blackScholes(i, K, r, T, sigma, type))
        deltas.append(optionDelta(i, K, r, T, sigma, type))
        gammas.append(optionGamma(i, K, r, T, sigma))
        thetas.append(optionTheta(i,K, r, T, sigma, type))
        vegas.append(optionVega(i, K, r, T, sigma))
        rhos.append(optionRho(i, K, r, T, sigma, type))
elif variable == strike_var:
    for i in variable:
        prices.append(blackScholes(S, i, r, T, sigma, type))
        deltas.append(optionDelta(S, i, r, T, sigma, type))
        gammas.append(optionGamma(S, i, r, T, sigma))
        thetas.append(optionTheta(S,i, r, T, sigma, type))
        vegas.append(optionVega(S, i, r, T, sigma))
        rhos.append(optionRho(S, i, r, T, sigma, type))
elif variable == risk_free_var:
    for i in variable:
        prices.append(blackScholes(S, K, i, T, sigma, type))
        deltas.append(optionDelta(S, K, i, T, sigma, type))
        gammas.append(optionGamma(S, K, i, T, sigma))
        thetas.append(optionTheta(S,K, i, T, sigma, type))
        vegas.append(optionVega(S, K, i, T, sigma))
        rhos.append(optionRho(S, K, i, T, sigma, type))

fig1, ax1 = plt.subplots()
ax1.plot(variable, prices)
ax1.set_title("Option Price")

fig2, ax2 = plt.subplots()
ax2.plot(variable, deltas)
ax2.set_title("Delta")

fig3, ax3 = plt.subplots()
ax3.plot(variable, gammas)
ax3.set_title("Gamma")

fig4, ax4 = plt.subplots()
ax4.plot(variable, thetas)
ax4.set_title("Theta")

fig5, ax5 = plt.subplots()
ax5.plot(variable, vegas)
ax5.set_title("Vega")

fig6, ax6 = plt.subplots()
ax6.plot(variable, rhos)
ax6.set_title("Rho")

if variable==days_array:
    ax1.invert_xaxis()
    ax2.invert_xaxis()
    ax3.invert_xaxis()
    ax4.invert_xaxis()
    ax5.invert_xaxis()
    ax6.invert_xaxis()



if run_button:
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
    st.pyplot(fig4)
    st.pyplot(fig5)
    st.pyplot(fig6)
