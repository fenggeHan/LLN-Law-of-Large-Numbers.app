# 必须放在最顶部！解决Streamlit Cloud matplotlib报错
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 云端无SimHei，改用开源支持中文的DejaVuSans fallback，避免字体报错
plt.rcParams["font.family"] = ["DejaVu Sans", "sans‑serif"]
plt.rcParams["axes.unicode_minus"] = False


def bernoulli_simulation(max_n: int, p: float):
    samples = np.random.binomial(n=1, p=p, size=max_n)
    freq_arr = np.cumsum(samples) / np.arange(1, max_n + 1)
    return freq_arr


def khintchine_simulation(max_n: int):
    samples = np.random.uniform(low=0, high=10, size=max_n)
    mean_arr = np.cumsum(samples) / np.arange(1, max_n + 1)
    true_mu = 5.0
    return mean_arr, true_mu


def main():
    st.set_page_config(page_title="Law of Large Numbers", layout="wide")
    st.title("📊 Law of Large Numbers Simulation 大数定理交互式模拟")
    st.markdown("""
    **Core Idea**: As sample size $n$ increases, frequency converges to true probability, sample mean converges to population expectation.
    - Bernoulli LLN: Frequency converges to true probability
    - Khinchine LLN: Sample mean converges to population expectation
    """)

    with st.sidebar:
        st.header("Parameter Settings")
        max_sample = st.slider("Max sample size n", min_value=100, max_value=50000, value=20000, step=1000)
        p_input = st.slider("Bernoulli probability p", min_value=0.01, max_value=0.99, value=0.5, step=0.01)
        run_btn = st.button("🔁 Re‑run Simulation", type="primary")

    if run_btn or "first_run" not in st.session_state:
        st.session_state["first_run"] = True
        freq_data = bernoulli_simulation(max_sample, p_input)
        mean_data, mu_true = khintchine_simulation(max_sample)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))
        x_axis = np.arange(1, max_sample + 1)

        ax1.plot(x_axis, freq_data, lw=0.6, color="#1f77b4")
        ax1.axhline(y=p_input, color="red", linestyle="--", label=f"True probability p={p_input:.2f}")
        ax1.set_title("Bernoulli LLN: Frequency vs Sample Size")
        ax1.set_xlabel("Sample size n")
        ax1.set_ylabel("Frequency")
        ax1.legend()
        ax1.grid(alpha=0.3)

        ax2.plot(x_axis, mean_data, lw=0.6, color="#2ca02c")
        ax2.axhline(y=mu_true, color="red", linestyle="--", label=f"Population mean μ={mu_true}")
        ax2.set_title("Khinchine LLN: Sample Mean vs Sample Size")
        ax2.set_xlabel("Sample size n")
        ax2.set_ylabel("Sample mean")
        ax2.legend()
        ax2.grid(alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("### 📝 Observation")
        st.write("1. Strong fluctuation for small sample size, large deviation from true value;")
        st.write("2. Curves gradually approach red dashed line as sample size grows;")
        st.write("3. Convergence in probability ≠ exact equality, small random fluctuations remain.")


if __name__ == "__main__":
    main()
