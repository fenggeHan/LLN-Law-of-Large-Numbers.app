import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. 页面配置
# ============================================================

st.set_page_config(
    page_title="大数定律交互实验室",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. 全局样式
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 20px;
        color: #666666;
        margin-bottom: 25px;
    }

    .experiment-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
    }

    .formula-box {
        padding: 18px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin: 15px 0;
    }

    .footer {
        text-align: center;
        color: #888888;
        font-size: 14px;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. 辅助函数
# ============================================================

def set_matplotlib_style():
    """统一 Matplotlib 图像样式"""
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False


set_matplotlib_style()


def generate_bernoulli_data(p, n, seed):
    """生成伯努利试验数据"""
    rng = np.random.default_rng(seed)

    trials = rng.binomial(
        n=1,
        p=p,
        size=n
    )

    cumulative_frequency = np.cumsum(trials) / np.arange(1, n + 1)

    return trials, cumulative_frequency


def generate_sample_mean_data(distribution, n, seed):
    """生成随机变量样本并计算累计样本均值"""

    rng = np.random.default_rng(seed)

    if distribution == "正态分布":
        mu = 0
        sigma = 1

        samples = rng.normal(
            loc=mu,
            scale=sigma,
            size=n
        )

        theoretical_mean = mu

    elif distribution == "均匀分布":
        a = 0
        b = 1

        samples = rng.uniform(
            low=a,
            high=b,
            size=n
        )

        theoretical_mean = (a + b) / 2

    elif distribution == "指数分布":
        scale = 1

        samples = rng.exponential(
            scale=scale,
            size=n
        )

        theoretical_mean = scale

    elif distribution == "骰子":
        samples = rng.integers(
            low=1,
            high=7,
            size=n
        )

        theoretical_mean = 3.5

    else:
        samples = rng.normal(
            0,
            1,
            n
        )

        theoretical_mean = 0

    cumulative_mean = np.cumsum(samples) / np.arange(1, n + 1)

    return samples, cumulative_mean, theoretical_mean


# ============================================================
# 4. 侧边栏导航
# ============================================================

st.sidebar.title("🎲 大数定律实验室")

st.sidebar.markdown(
    """
    **Law of Large Numbers**

    通过计算机模拟随机实验，
    直观理解概率论中的大数定律。
    """
)

page = st.sidebar.radio(
    "请选择实验",
    [
        "🏠 首页",
        "🪙 实验一：投掷硬币",
        "🎲 实验二：样本均值",
        "🔁 实验三：重复实验",
        "📊 实验四：大数定律 vs 中心极限定理",
        "📖 理论知识",
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Python + NumPy + Matplotlib + Streamlit"
)


# ============================================================
# 5. 首页
# ============================================================

if page == "🏠 首页":

    st.markdown(
        '<div class="main-title">🎲 大数定律交互实验室</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">通过计算机模拟，直观理解概率论中的“大数定律”</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        ## 什么是大数定律？

        大数定律是概率论中最重要的基本定理之一。

        它告诉我们：

        > 当一个随机实验重复进行大量次数时，
        > 随着试验次数不断增加，样本平均值会逐渐稳定并趋近于理论期望。

        对于独立同分布的随机变量：

        $$
        X_1,X_2,\\dots,X_n
        $$

        如果它们具有相同的数学期望：

        $$
        E(X_i)=\\mu
        $$

        那么大数定律告诉我们：

        $$
        \\frac{X_1+X_2+\\cdots+X_n}{n}
        \\rightarrow \\mu
        $$

        当：

        $$
        n\\rightarrow\\infty
        $$

        时，样本平均值会越来越接近理论平均值。
        """
    )

    st.divider()

    st.subheader("🧪 你可以进行哪些实验？")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 🪙 实验一

            **投掷硬币**

            观察正面出现的累计频率如何趋近理论概率。

            $$
            \\frac{S_n}{n}\\rightarrow p
            $$
            """
        )

    with col2:
        st.markdown(
            """
            ### 🎲 实验二

            **样本均值**

            使用正态分布、均匀分布、
            指数分布和骰子进行实验。

            $$
            \\bar X_n\\rightarrow E(X)
            $$
            """
        )

    with col3:
        st.markdown(
            """
            ### 🔁 实验三

            **重复实验**

            同时进行大量独立实验，
            观察最终结果的分布。

            体验“随机”背后的规律。
            """
        )

    st.divider()

    st.subheader("📊 一个重要的问题")

    st.info(
        """
        如果一次投掷硬币的结果是随机的，

        **为什么投掷次数越来越多以后，累计频率反而越来越稳定？**

        你可以通过左侧的实验亲自寻找答案。
        """
    )


# ============================================================
# 6. 实验一：投掷硬币
# ============================================================

elif page == "🪙 实验一：投掷硬币":

    st.title("🪙 实验一：投掷硬币")

    st.markdown(
        """
        我们首先研究最简单的伯努利试验。

        假设一枚硬币正面朝上的理论概率为：

        $$
        P(X=1)=p
        $$

        我们不断投掷硬币，并计算：

        $$
        \\frac{\\text{正面出现次数}}{\\text{总投掷次数}}
        $$

        这就是**累计频率**。
        """
    )

    st.divider()

    # 参数
    col1, col2, col3 = st.columns(3)

    with col1:
        n_trials = st.slider(
            "投掷次数 N",
            100,
            50000,
            5000,
            100
        )

    with col2:
        p = st.slider(
            "理论概率 p",
            0.05,
            0.95,
            0.50,
            0.05
        )

    with col3:
        seed = st.number_input(
            "随机种子",
            0,
            99999,
            42
        )

    # 模拟
    trials, cumulative_frequency = generate_bernoulli_data(
        p,
        n_trials,
        seed
    )

    n = np.arange(1, n_trials + 1)

    final_frequency = cumulative_frequency[-1]
    final_error = final_frequency - p

    # 指标
    st.subheader("📊 实验结果")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "试验次数",
        f"{n_trials:,}"
    )

    c2.metric(
        "理论概率",
        f"{p:.4f}"
    )

    c3.metric(
        "最终累计频率",
        f"{final_frequency:.4f}"
    )

    c4.metric(
        "绝对误差",
        f"{abs(final_error):.4f}"
    )

    st.divider()

    # 图像
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        n,
        cumulative_frequency,
        linewidth=1.5,
        label="累计频率"
    )

    ax.axhline(
        p,
        linestyle="--",
        linewidth=2,
        label=f"理论概率 p = {p:.2f}"
    )

    ax.set_xlabel("试验次数 N")
    ax.set_ylabel("累计频率")

    ax.set_title(
        "累计频率随着试验次数增加逐渐趋近理论概率"
    )

    ax.set_ylim(0, 1)

    ax.grid(
        True,
        linestyle=":",
        alpha=0.6
    )

    ax.legend()

    st.pyplot(fig)

    st.caption(
        "注意：累计频率并不是单调地接近理论概率。"
        "它仍然会产生波动，但总体上会越来越稳定。"
    )

    # 误差
    st.subheader("📉 观察误差")

    absolute_error = np.abs(
        cumulative_frequency - p
    )

    fig2, ax2 = plt.subplots(figsize=(12, 4))

    ax2.plot(
        n,
        absolute_error,
        linewidth=1.2
    )

    ax2.set_xlabel("试验次数 N")
    ax2.set_ylabel("|累计频率 − p|")

    ax2.set_title(
        "累计频率与理论概率之间的绝对误差"
    )

    ax2.grid(
        True,
        linestyle=":",
        alpha=0.6
    )

    st.pyplot(fig2)

    st.info(
        """
        **观察重点：**

        不要期待误差每一步都下降。

        大数定律描述的是一种“随着试验次数趋于无穷，
        样本平均值趋近理论值”的长期规律，
        而不是每一次实验结果都比上一次更准确。
        """
    )


# ============================================================
# 7. 实验二：样本均值
# ============================================================

elif page == "🎲 实验二：样本均值":

    st.title("🎲 实验二：观察样本均值")

    st.markdown(
        """
        大数定律并不只适用于硬币。

        我们可以选择不同的随机变量，观察：

        $$
        \\bar X_n=
        \\frac{X_1+X_2+\\cdots+X_n}{n}
        $$

        是否趋近于理论期望：

        $$
        E(X)
        $$
        """
    )

    st.divider()

    distribution = st.selectbox(
        "选择随机变量",
        [
            "正态分布",
            "均匀分布",
            "指数分布",
            "骰子"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        n = st.slider(
            "样本数量 N",
            100,
            50000,
            5000,
            100
        )

    with col2:
        seed = st.number_input(
            "随机种子",
            0,
            99999,
            42
        )

    samples, cumulative_mean, theoretical_mean = \
        generate_sample_mean_data(
            distribution,
            n,
            seed
        )

    final_mean = cumulative_mean[-1]
    error = final_mean - theoretical_mean

    st.subheader("📊 实验结果")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "样本数量",
        f"{n:,}"
    )

    c2.metric(
        "理论期望",
        f"{theoretical_mean:.4f}"
    )

    c3.metric(
        "最终样本均值",
        f"{final_mean:.4f}"
    )

    c4.metric(
        "绝对误差",
        f"{abs(error):.4f}"
    )

    st.divider()

    # 样本均值曲线
    x = np.arange(1, n + 1)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        x,
        cumulative_mean,
        linewidth=1.5,
        label="累计样本均值"
    )

    ax.axhline(
        theoretical_mean,
        linestyle="--",
        linewidth=2,
        label=f"理论期望 = {theoretical_mean:.2f}"
    )

    ax.set_xlabel("样本数量 N")
    ax.set_ylabel("样本均值")

    ax.set_title(
        f"{distribution}：样本均值趋近理论期望"
    )

    ax.grid(
        True,
        linestyle=":",
        alpha=0.6
    )

    ax.legend()

    st.pyplot(fig)

    # 分布直方图
    st.subheader("📊 随机变量本身的分布")

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.hist(
        samples,
        bins=40,
        density=True,
        alpha=0.7
    )

    ax2.set_xlabel("随机变量取值")
    ax2.set_ylabel("频率密度")

    ax2.set_title(
        f"{distribution} 的模拟样本分布"
    )

    ax2.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    st.pyplot(fig2)


# ============================================================
# 8. 实验三：重复实验
# ============================================================

elif page == "🔁 实验三：重复实验":

    st.title("🔁 实验三：重复实验")

    st.markdown(
        """
        前面的实验只进行了一次模拟。

        现在我们换一个问题：

        > 如果我们把“500 次投掷硬币”这个实验重复进行很多次，
        > 每一次实验最终得到的累计频率会完全一样吗？

        当然不会。

        但这些结果会不会呈现出某种规律？

        让我们一起看看。
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        experiment_count = st.slider(
            "重复实验次数",
            10,
            1000,
            200,
            10
        )

    with col2:
        trials_per_experiment = st.slider(
            "每次实验投掷次数",
            50,
            5000,
            500,
            50
        )

    with col3:
        p = st.slider(
            "理论概率 p",
            0.1,
            0.9,
            0.5,
            0.05
        )

    seed = st.number_input(
        "随机种子",
        0,
        99999,
        42
    )

    rng = np.random.default_rng(seed)

    results = rng.binomial(
        trials_per_experiment,
        p,
        size=experiment_count
    ) / trials_per_experiment

    mean_result = np.mean(results)
    std_result = np.std(results)

    st.subheader("📊 重复实验结果")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "重复次数",
        f"{experiment_count:,}"
    )

    c2.metric(
        "结果平均值",
        f"{mean_result:.4f}"
    )

    c3.metric(
        "结果标准差",
        f"{std_result:.4f}"
    )

    st.divider()

    # 结果分布
    fig, ax = plt.subplots(figsize=(11, 5))

    ax.hist(
        results,
        bins=30,
        alpha=0.75
    )

    ax.axvline(
        p,
        linestyle="--",
        linewidth=2,
        label=f"理论概率 p = {p:.2f}"
    )

    ax.axvline(
        mean_result,
        linestyle=":",
        linewidth=2,
        label=f"实验平均值 = {mean_result:.4f}"
    )

    ax.set_xlabel("每次实验的最终累计频率")
    ax.set_ylabel("实验次数")

    ax.set_title(
        "重复实验中最终累计频率的分布"
    )

    ax.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    ax.legend()

    st.pyplot(fig)

    st.success(
        f"""
        虽然每一次实验得到的结果都不完全相同，
        但是经过 {experiment_count:,} 次重复实验以后，

        这些结果的平均值约为：

        **{mean_result:.4f}**

        理论概率为：

        **{p:.4f}**

        这说明随机性和规律性可以同时存在。
        """
    )


# ============================================================
# 9. 实验四：大数定律 vs 中心极限定理
# ============================================================

elif page == "📊 实验四：大数定律 vs 中心极限定理":

    st.title("📊 实验四：大数定律 vs 中心极限定理")

    st.markdown(
        """
        这是概率论中非常重要的两个定理。

        它们经常被放在一起讨论，但研究的问题并不一样。
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📘 大数定律")

        st.markdown(
            """
            研究的是：

            **样本均值最终会趋近哪里？**

            $$
            \\bar X_n\\rightarrow \\mu
            $$

            核心关键词：

            **趋近理论期望**
            """
        )

    with col2:

        st.subheader("📗 中心极限定理")

        st.markdown(
            """
            研究的是：

            **样本均值的随机波动呈现什么分布？**

            当样本量足够大时：

            $$
            \\frac{\\bar X_n-\\mu}
            {\\sigma/\\sqrt n}
            \\approx N(0,1)
            $$

            核心关键词：

            **正态分布**
            """
        )

    st.divider()

    st.subheader("🧪 模拟中心极限定理")

    col1, col2, col3 = st.columns(3)

    with col1:
        sample_size = st.slider(
            "每组样本量 n",
            2,
            1000,
            30
        )

    with col2:
        repetitions = st.slider(
            "重复次数",
            100,
            5000,
            1000,
            100
        )

    with col3:
        seed = st.number_input(
            "随机种子",
            0,
            99999,
            42
        )

    rng = np.random.default_rng(seed)

    # 使用均匀分布作为总体
    samples = rng.uniform(
        0,
        1,
        size=(repetitions, sample_size)
    )

    sample_means = np.mean(
        samples,
        axis=1
    )

    mu = 0.5
    sigma = np.sqrt(1 / 12)

    standardized = (
        sample_means - mu
    ) / (
        sigma / np.sqrt(sample_size)
    )

    st.write(
        f"""
        总体：

        **Uniform(0, 1)**

        理论均值：

        **μ = {mu}**

        理论标准差：

        **σ ≈ {sigma:.4f}**
        """
    )

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.hist(
        standardized,
        bins=35,
        density=True,
        alpha=0.75
    )

    ax.set_xlabel("标准化样本均值")
    ax.set_ylabel("密度")

    ax.set_title(
        "标准化样本均值的分布"
    )

    ax.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    st.pyplot(fig)

    st.info(
        """
        **你看到的是什么？**

        随着每组样本量 n 增大，
        标准化后的样本均值分布会越来越接近标准正态分布。

        因此：

        **大数定律：告诉我们样本均值“去哪里”。**

        **中心极限定理：告诉我们样本均值“如何波动”。**
        """
    )


# ============================================================
# 10. 理论知识
# ============================================================

elif page == "📖 理论知识":

    st.title("📖 大数定律理论知识")

    st.markdown(
        """
        ## 1. 伯努利大数定律

        假设进行大量独立重复试验，每次试验成功的概率都是：

        $$
        p
        $$

        记：

        $$
        S_n=X_1+X_2+\\cdots+X_n
        $$

        那么成功的频率：

        $$
        \\frac{S_n}{n}
        $$

        会随着 n 的增加而趋近于：

        $$
        p
        $$

        即：

        $$
        \\frac{S_n}{n}\\rightarrow p
        $$
        """
    )

    st.divider()

    st.markdown(
        """
        ## 2. 弱大数定律

        设：

        $$
        X_1,X_2,\\dots,X_n
        $$

        相互独立同分布，并且：

        $$
        E(X_i)=\\mu
        $$

        那么样本均值：

        $$
        \\bar X_n=
        \\frac{1}{n}
        \\sum_{i=1}^{n}X_i
        $$

        满足：

        $$
        \\bar X_n
        \\xrightarrow{P}
        \\mu
        $$

        也就是说：

        对任意：

        $$
        \\varepsilon>0
        $$

        有：

        $$
        P(|\\bar X_n-\\mu|>\\varepsilon)
        \\rightarrow 0
        $$
        """
    )

    st.divider()

    st.markdown(
        """
        ## 3. 为什么大数定律很重要？

        大数定律建立了：

        **概率理论 → 现实世界数据**

        之间的重要联系。

        例如：

        - 抛硬币
        - 赌博游戏
        - 保险精算
        - 民意调查
        - 金融统计
        - 实验科学
        - 机器学习

        在这些问题中，我们往往无法直接知道总体规律，
        但可以通过大量观测数据估计它。
        """
    )

    st.divider()

    st.subheader("💡 最重要的一句话")

    st.success(
        """
        **随机事件单次看起来没有规律，
        但大量重复以后，整体会呈现稳定的统计规律。**
        """
    )


# ============================================================
# 11. 页脚
# ============================================================

st.markdown(
    """
    <div class="footer">
        🎲 大数定律交互实验室<br>
        Python · NumPy · Matplotlib · Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
