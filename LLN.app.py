import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(page_title="大数定理交互演示", layout="wide")

st.title("🎲 大数定理 (Law of Large Numbers) 动态模拟")
st.write(
    "大数定理表明：在随机事件的大量重复试验中，事件发生的频率会无限接近其理论概率。"
)

# 侧边栏设置
st.sidebar.header("实验参数设置")
num_trials = st.sidebar.slider(
    "模拟投掷次数 (N)", min_value=100, max_value=20000, value=5000, step=500
)
p_true = st.sidebar.slider(
    "理论概率 (硬币正面朝上)",
    min_value=0.1,
    max_value=0.9,
    value=0.5,
    step=0.05,
)

# 模拟掷硬币 (1表示正面，0表示反面)
np.random.seed(42)
trials = np.random.binomial(1, p_true, num_trials)
cumulative_means = np.cumsum(trials) / np.arange(1, num_trials + 1)

# 绘图
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(
    range(1, num_trials + 1),
    cumulative_means,
    label="累计频率",
    color="#1f77b4",
    linewidth=1,
)
ax.axhline(
    y=p_true,
    color="r",
    linestyle="--",
    label=f"理论概率 ($p = {p_true}$)",
)
ax.set_xlabel("试验次数")
ax.set_ylabel("正面出现的累计频率")
ax.set_ylim(0, 1)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()

st.pyplot(fig)

# 指标展示
final_rate = cumulative_means[-1]
col1, col2, col3 = st.columns(3)
col1.metric("总试验次数", f"{num_trials:,}")
col2.metric("最终累计频率", f"{final_rate:.4f}")
col3.metric("相对误差", f"{abs(final_rate - p_true):.4f}")
