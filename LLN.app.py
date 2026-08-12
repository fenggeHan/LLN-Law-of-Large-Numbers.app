import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# ============================================================
# 页面基本设置
# ============================================================

st.set_page_config(
    page_title="大数定理交互实验室",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 页面标题
# ============================================================

st.title("🎲 大数定理交互实验室")

st.markdown(
    """
    ### Law of Large Numbers

    > **当随机试验重复进行大量次数时，样本的平均结果会逐渐稳定并趋近于理论期望。**

    下面通过不断重复投掷一枚“可能不公平的硬币”，
    观察 **累计频率** 如何逐渐接近理论概率。
    """
)

st.divider()

# ============================================================
# 侧边栏：实验参数
# ============================================================

st.sidebar.header("⚙️ 实验参数")

num_trials = st.sidebar.slider(
    "模拟投掷次数 N",
    min_value=100,
    max_value=50000,
    value=5000,
    step=500,
)

p_true = st.sidebar.slider(
    "理论概率 p",
    min_value=0.05,
    max_value=0.95,
    value=0.50,
    step=0.05,
)

seed = st.sidebar.number_input(
    "随机种子",
    min_value=0,
    max_value=9999,
    value=42,
    step=1,
)

st.sidebar.divider()

st.sidebar.info(
    """
    **实验说明**

    每一次试验中：

    - 1 = 正面
    - 0 = 反面

    理论上，正面出现的概率为：

    **p = {:.2f}**
    """.format(p_true)
)

# ============================================================
# 随机模拟
# ============================================================

np.random.seed(seed)

trials = np.random.binomial(
    1,
    p_true,
    num_trials
)

n = np.arange(1, num_trials + 1)

# 累计频率
cumulative_means = np.cumsum(trials) / n

# 累计误差
errors = cumulative_means - p_true

absolute_errors = np.abs(errors)

# ============================================================
# 核心指标
# ============================================================

final_rate = cumulative_means[-1]
final_error = final_rate - p_true
absolute_error = abs(final_error)

max_error = np.max(absolute_errors)

# ============================================================
# 指标卡片
# ============================================================

st.subheader("📊 实验结果")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "实验次数",
    f"{num_trials:,}"
)

col2.metric(
    "理论概率",
    f"{p_true:.4f}"
)

col3.metric(
    "最终累计频率",
    f"{final_rate:.4f}",
    delta=f"{final_error:+.4f}"
)

col4.metric(
    "最终绝对误差",
    f"{absolute_error:.4f}"
)

st.divider()

# ============================================================
# 第一张图：累计频率
# ============================================================

st.subheader("📈 实验一：累计频率逐渐趋近理论概率")

fig1, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(
    n,
    cumulative_means,
    label="累计频率",
    linewidth=1.5,
)

ax1.axhline(
    y=p_true,
    linestyle="--",
    linewidth=2,
    label=f"理论概率 p = {p_true:.2f}",
)

ax1.set_xlabel("试验次数 N")
ax1.set_ylabel("累计频率")

ax1.set_ylim(
    max(0, p_true - 0.5),
    min(1, p_true + 0.5)
)

ax1.set_title(
    "随着试验次数增加，累计频率逐渐稳定"
)

ax1.grid(
    True,
    linestyle=":",
    alpha=0.6
)

ax1.legend()

st.pyplot(fig1)

st.caption(
    "观察蓝色曲线：在试验次数较少时，累计频率波动较大；"
    "随着 N 增大，累计频率逐渐稳定在理论概率附近。"
)

# ============================================================
# 第二张图：误差变化
# ============================================================

st.subheader("📉 实验二：观察误差如何变化")

fig2, ax2 = plt.subplots(figsize=(12, 4))

ax2.plot(
    n,
    absolute_errors,
    linewidth=1.2,
)

ax2.set_xlabel("试验次数 N")
ax2.set_ylabel("|累计频率 − 理论概率|")

ax2.set_title(
    "累计频率与理论概率之间的绝对误差"
)

ax2.grid(
    True,
    linestyle=":",
    alpha=0.6
)

st.pyplot(fig2)

st.caption(
    "大数定律并不是说误差每一次试验都会下降，"
    "而是说随着试验次数不断增加，样本平均值趋近于理论值。"
)

# ============================================================
# 理论解释
# ============================================================

st.divider()

st.subheader("📚 为什么会发生这种现象？")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        ### ① 直观理解

        假设一枚硬币正面朝上的理论概率为：

        $$
        P(X=1)=p
        $$

        如果只投掷几次，结果可能非常随机。

        例如：

        - 10 次试验 → 可能出现 7 次正面
        - 100 次试验 → 可能出现 57 次正面
        - 10,000 次试验 → 通常会更加接近理论概率

        **试验次数越多，随机波动对整体结果的影响越小。**
        """
    )

with col2:

    st.markdown(
        """
        ### ② 数学表达

        设：

        $$
        X_1,X_2,\dots,X_n
        $$

        是相互独立且同分布的随机变量，并且：

        $$
        E(X_i)=\\mu
        $$

        则大数定律告诉我们：

        $$
        \\frac{X_1+X_2+\\cdots+X_n}{n}
        \\rightarrow \\mu
        $$

        当：

        $$
        n\\rightarrow\\infty
        $$

        时，样本平均值会趋近于总体期望。
        """
    )

# ============================================================
# 实验总结
# ============================================================

st.divider()

st.subheader("🧠 本次实验总结")

st.success(
    f"""
    本次实验进行了 **{num_trials:,} 次**随机试验。

    理论概率：

    **p = {p_true:.4f}**

    最终累计频率：

    **{final_rate:.4f}**

    最终绝对误差：

    **{absolute_error:.4f}**

    通过增加试验次数 N，可以观察到累计频率总体上越来越接近理论概率。
    这正是大数定律所描述的核心现象。
    """
)

# ============================================================
# 页脚
# ============================================================

st.divider()

st.caption(
    "🎓 大数定律交互实验室 | 使用 Python + NumPy + Matplotlib + Streamlit 构建"
)
