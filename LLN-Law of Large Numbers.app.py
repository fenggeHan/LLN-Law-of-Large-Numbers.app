import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 设置matplotlib中文
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def bernoulli_simulation(max_n: int, p: float):
    """伯努利大数定律模拟：抛硬币频率"""
    samples = np.random.binomial(n=1, p=p, size=max_n)
    freq_arr = np.cumsum(samples) / np.arange(1, max_n + 1)
    return freq_arr


def khintchine_simulation(max_n: int):
    """辛钦大数定律模拟，U[0,10]，理论期望=5"""
    samples = np.random.uniform(low=0, high=10, size=max_n)
    mean_arr = np.cumsum(samples) / np.arange(1, max_n + 1)
    true_mu = 5.0
    return mean_arr, true_mu


def main():
    st.set_page_config(page_title="大数定律模拟", layout="wide")
    st.title("📊 概率论 — 大数定理交互式模拟")
    st.markdown("""
    **大数定律核心：当样本量n足够大时，频率收敛于真实概率，样本均值收敛于总体期望。**
    - 伯努利大数定律：频率依概率收敛事件真实概率
    - 辛钦大数定律：样本均值依概率收敛总体数学期望
    """)

    # 侧边栏参数
    with st.sidebar:
        st.header("参数设置")
        max_sample = st.slider("最大样本量 n", min_value=100, max_value=50000, value=20000, step=1000)
        p_input = st.slider("伯努利试验真实概率 p", min_value=0.01, max_value=0.99, value=0.5, step=0.01)
        run_btn = st.button("🔁 重新生成模拟数据", type="primary")

    if run_btn or "first_run" not in st.session_state:
        st.session_state["first_run"] = True
        # 执行模拟
        freq_data = bernoulli_simulation(max_sample, p_input)
        mean_data, mu_true = khintchine_simulation(max_sample)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))
        x_axis = np.arange(1, max_sample + 1)

        # 图1 伯努利
        ax1.plot(x_axis, freq_data, lw=0.6, color="#1f77b4")
        ax1.axhline(y=p_input, color="red", linestyle="--", label=f"真实概率 p={p_input:.2f}")
        ax1.set_title("伯努利大数定律｜事件发生频率随样本量变化")
        ax1.set_xlabel("样本量 n")
        ax1.set_ylabel("频率")
        ax1.legend()
        ax1.grid(alpha=0.3)

        # 图2 辛钦
        ax2.plot(x_axis, mean_data, lw=0.6, color="#2ca02c")
        ax2.axhline(y=mu_true, color="red", linestyle="--", label=f"总体期望 μ={mu_true}")
        ax2.set_title("辛钦大数定律｜样本均值随样本量变化")
        ax2.set_xlabel("样本量 n")
        ax2.set_ylabel("样本均值")
        ax2.legend()
        ax2.grid(alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("### 📝观察结论")
        st.write("1. 小样本时震荡剧烈，和真值偏差很大；")
        st.write("2. 样本量不断增大，曲线逐步靠近红色虚线；")
        st.write("3. 依概率收敛 ≠ 等于，仍会存在小幅随机波动。")


if __name__ == "__main__":
    main()