import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Chargement et prétraitements
# -----------------------------
data = pd.read_csv('BP_data.csv', sep=';')
data['Prix_moy'] = (data['High'] + data['Low']) / 2
data['rt'] = np.log(data['Prix_moy'] / data['Prix_moy'].shift(1))
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# Filtre 2023-2024
data_2023 = data[(data['Date'] >= '2023-01-04') & (data['Date'] <= '2024-11-19')].copy()

# Paramètres
S0 = float(data_2023['Prix_moy'].iloc[-1])
sigma = data_2023['rt'].std() * np.sqrt(252)
r = 2.9 / 100
T = 0.5     # 6 mois
N = 500     # nombre de trajectoires Monte Carlo
n_steps = int(T * 252)
dt = T / n_steps

# -----------------------------
# Monte Carlo
# -----------------------------
sims = np.empty((N, n_steps))
for j in range(N):
    s = np.empty(n_steps)
    s[0] = S0
    for i in range(1, n_steps):
        s[i] = s[i-1] * np.exp((r - 0.5 * sigma**2) * dt +
                               sigma * np.sqrt(dt) * np.random.normal())
    sims[j] = s

mean_mc = sims.mean(axis=0)
low95 = np.percentile(sims, 2.5, axis=0)
high95 = np.percentile(sims, 97.5, axis=0)
final_mc = sims[:, -1]  # distribution finale

# -----------------------------
# Black-Scholes (trajectoire unique)
# -----------------------------
np.random.seed(42)
path_bs = [S0]
for i in range(1, n_steps):
    path_bs.append(
        path_bs[-1] * np.exp((r - 0.5 * sigma**2) * dt +
                             sigma * np.sqrt(dt) * np.random.normal())
    )
path_bs = np.array(path_bs)
final_bs = path_bs[-1]

# -----------------------------
# Markov Chains
# -----------------------------
n_bins = 10
bins = np.linspace(data_2023['Prix_moy'].min(), data_2023['Prix_moy'].max(), n_bins + 1)
labels = range(n_bins)
data_2023['State'] = pd.cut(data_2023['Prix_moy'], bins=bins, labels=labels, include_lowest=True).astype(int)

transition_matrix = np.zeros((n_bins, n_bins))
for i in range(len(data_2023) - 1):
    transition_matrix[data_2023['State'].iloc[i], data_2023['State'].iloc[i+1]] += 1
transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)

state = data_2023['State'].iloc[-1]
price_markov = [S0]
for _ in range(n_steps - 1):
    state = np.random.choice(labels, p=transition_matrix[state])
    centre = 0.5 * (bins[state] + bins[state + 1])
    price_markov.append(centre)
price_markov = np.array(price_markov)
final_mk = price_markov[-1]

# -----------------------------
# Histogramme des rendements
# -----------------------------
returns_mc = (final_mc - S0) / S0
return_bs = (final_bs - S0) / S0
return_mk = (final_mk - S0) / S0
var5 = np.percentile(final_mc, 5)
return_var5 = (var5 - S0) / S0

plt.figure(figsize=(12, 5))
plt.hist(returns_mc, bins=30, alpha=0.6, color="orange", label="Monte Carlo (rendements)")

plt.axvline(return_bs, color="green", linestyle="--", linewidth=2,
            label=f"Black-Scholes (rendement ~ {return_bs*100:.1f} %, prix ~ {final_bs:.2f} USD)")
plt.axvline(return_mk, color="red", linestyle="-.", linewidth=2,
            label=f"Markov (rendement ~ {return_mk*100:.1f} %, prix ~ {final_mk:.2f} USD)")
plt.axvline(return_var5, color="black", linestyle=":", linewidth=2,
            label=f"Seuil de perte extrême (VaR 5% = {return_var5*100:.1f} %, prix ~ {var5:.2f} USD)")

plt.title("Distribution des rendements finaux")
plt.xlabel("Rendement final (en % du prix initial)")
plt.ylabel("Fréquence (nb de scénarios)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.show()