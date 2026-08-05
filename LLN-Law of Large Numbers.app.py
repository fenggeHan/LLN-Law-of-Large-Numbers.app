# 必须第一行！Agg无图形后端
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import streamlit as st

# 加载仓库内的黑体字体文件
my_font = FontProperties(fname="./simhei.ttf")

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
    st.set_page_config(page_title="大数定理模拟", layout="wide")
    st.title("📊 大数定理交互式模拟", fontproperties=my_font)
    st.markdown("""
**大数定理核心思想**：样本量n充分大时，频率收敛于真实概率，样本均值收敛于总体期望。
- 伯努利大数定律：事件频率依概率收敛于真实概率
- 辛钦大数定律：样本均值依概率收敛于总体数学期望
""")

    with st.sidebar:
        st.header("参数设置")
        max_sample = st.slider("最大样本量 n", min_value=100, max_value=50000, value=20000, step=1000)
        p_input = st.slider("伯努利试验概率 p", min_value=0.01, max_value=0.99, value=0.5, step=0.01)
        run_btn = st.button("🔁 重新运行模拟", type="primary")

    if run_btn or "first_run" not in st.session_state:
        st.session_state["first_run"] = True
        freq_data = bernoulli_simulation(max_sample, p_input)
        mean_data, mu_true = khintchine_simulation(max_sample)

        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,9))
        x_axis = np.arange(1, max_sample+1)

        # 图1 伯努利
        ax1.plot(x_axis, freq_data, lw=0.6, color="#1f77b4")
        ax1.axhline(y=p_input, color="red", linestyle="--", label=f"真实概率 p={p_input:.2f}")
        ax1.set_title("伯努利大数定律｜频率随样本量变化", fontproperties=my_font)
        ax1.set_xlabel("样本量 n", fontproperties=my_font)
        ax1.set_ylabel("频率", fontproperties=my_font)
        ax1.legend(prop=my_font)
        ax1.grid(alpha=0.3)

        # 图2 辛钦
        ax2.plot(x_axis, mean_data, lw=0.6, color="#2ca02c")
        ax2.axhline(y=mu_true, color="red", linestyle="--", label=f"总体期望 μ={mu_true}")
        ax2.set_title("辛钦大数定律｜样本均值随样本量变化", fontproperties=my_font)
        ax2.set_xlabel("样本量 n", fontproperties=my_font)
        ax2.set_ylabel("样本均值", fontproperties=my_font)
        ax2.legend(prop=my_font)
        ax2.grid(alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("### 📝观察结论")
        st.write("1.小样本震荡剧烈，和真值偏差较大；")
        st.write("2.样本量增大，曲线逐步贴近理论红线；")
        st.write("3.依概率收敛不等于严格相等，始终存在小幅随机波动。")


if __name__ == "__main__":
    main()
