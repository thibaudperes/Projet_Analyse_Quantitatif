# Quantitative Analysis of BP Stock (6 months)

##  Project Objective
Develop a quantitative analysis tool to project BP’s stock price over a 6-month horizon, comparing three approaches: **Monte Carlo**, **Black–Scholes**, and **Markov Chains**.  
The goal is to confront the results, analyze their differences, and highlight the strengths and limitations of each method.

---
##  Methods

### 1. Monte Carlo (Geometric Brownian Motion)
- Simulation of **500 random trajectories** based on GBM.  
- Formula (step update):  
  S_{t+Δt} = S_t * exp((r - 0.5 σ²) Δt + σ √Δt ε_t),   ε_t ~ N(0,1)  
- Produces a **full distribution** of outcomes and a **95% confidence interval**.

### 2. Black–Scholes (closed-form GBM)
- Uses the closed-form solution of GBM:  
  S_T = S_0 * exp((r - 0.5 σ²) T + σ W_T),   W_T ~ N(0,T)  
- Generates a **smooth, theoretical path**, widely used in option pricing.

### 3. Markov Chains
- Price discretized into **10 bins (states)**.  
- Transition matrix built from historical data:  
  P_{ij} = Prob(next=j | current=i).  
- Simulated trajectory = sequence of state centers → explains the **staircase shape**.

---

## Results (example, S0 ≈ 29 USD, σ ≈ 23.5%)

- **Monte Carlo mean:** ~29.5 USD (+1.5%)  
- **Monte Carlo 95% CI:** [22.1 , 37.0] USD  
- **Black–Scholes:** ~25.4 USD (−12.5%)  
- **Markov Chains:** ~37.8 USD (+30.1%)  
- **Value-at-Risk (VaR 5%):** −24% → 1 out of 20 scenarios end below ~22 USD.  

---

##  Interpretation

- **Monte Carlo (orange)**  
  Provides the **probabilistic view**: expected price stays close to current (~29.5 USD), but uncertainty widens over time (22 to 37 USD range).  
   Best suited to **capture risk distribution**.

- **Black–Scholes (green, 25.4 USD = −12.5%)**  
  Appears **more pessimistic**. Why?  
  - BS depends on the drift term \( r - 0.5σ^2 \).  
  - With high estimated volatility (σ ≈ 23.5%), the negative correction \( -0.5σ^2 \) reduces the expected growth.  
  - Result: a **mechanical downward drift** relative to the spot price (~29 USD).

- **Markov (red, 37.8 USD = +30.1%)**  
  Appears **overly optimistic**. Why?  
  - The most recent historical states were in the upper price range.  
  - Transition matrix favors staying in higher states.  
  - Result: the Markov path “locks” into optimistic states and projects continued growth.

- **Comparison**  
  - **Black–Scholes = conservative / theoretical** forecast, heavily influenced by volatility.  
  - **Markov = opportunistic / regime-dependent**, extrapolates recent dynamics.  
  - **Monte Carlo = balanced view**, offering both expected value and downside risk (VaR).  

- **VaR 5% (22.1 USD, −24%)**  
  Shows there is a **5% probability** of an extreme downside move below ~22 USD.  
   Demonstrates the added value of Monte Carlo for **risk management** compared to single-path models.

---

