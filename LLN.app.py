import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. 页面设置
# ============================================================

st.set_page_config(
    page_title="大数定律交互实验室",
    page_icon="🎲",
    layout="wide",
)


# ============================================================
# 2. 页面 CSS
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
        font-size: 19px;
        color: #666666;
        margin-bottom: 25px;
    }

    .experiment-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f7f8fa;
        border: 1px solid #dddddd;
        margin-bottom: 20px;
    }

    .result-number {
        font-size: 32px;
        font-weight: bold;
    }

    .small-text {
        color: #777777;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. 初始化随机实验状态
# ============================================================

if "experiment_data" not in st.session_state:
    st.session_state.experiment_data = None

if "experiment_name" not in st.session_state:
    st.session_state.experiment_name = None


# ============================================================
# 4. 标题
# ============================================================

st.markdown(
    '<div class="main-title">🎲 大数定律交互实验室</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '选择一个你感兴趣的随机实验，自己调整参数，'
    '观察随机性背后的规律。'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# 5. 选择实验
# ============================================================

experiment = st.selectbox(
    "🔬 请选择一个实验",
    [
        "🪙 抛硬币",
        "🎲 掷骰子",
        "🏀 篮球罚球",
        "🎯 射击命中",
        "🎁 抽奖箱",
        "👥 随机抽样",
    ]
)


# ============================================================
# 6. 实验一：抛硬币
# ============================================================

if experiment == "🪙 抛硬币":

    st.subheader("🪙 抛硬币实验")

    st.write(
        """
        一枚硬币正面朝上的概率可以自己设置。

        你的任务是观察：

        **当投掷次数越来越多时，正面出现的频率会发生什么变化？**
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        probability = st.slider(
            "正面概率",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.05,
        )

    with col2:
        trials = st.slider(
            "投掷次数",
            min_value=10,
            max_value=50000,
            value=1000,
            step=10,
        )

    with col3:
        seed = st.number_input(
            "随机种子",
            min_value=0,
            max_value=99999,
            value=42,
        )

    run = st.button(
        "🎲 开始实验",
        key="coin_run"
    )

    if run:

        rng = np.random.default_rng(seed)

        data = rng.binomial(
            1,
            probability,
            trials
        )

        cumulative = np.cumsum(data) / np.arange(
            1,
            trials + 1
        )

        st.session_state.experiment_data = (
            data,
            cumulative,
            probability
        )

        st.session_state.experiment_name = experiment


# ============================================================
# 7. 实验二：掷骰子
# ============================================================

elif experiment == "🎲 掷骰子":

    st.subheader("🎲 掷骰子实验")

    st.write(
        """
        我们不只观察骰子每个点数出现的频率，
        还观察**平均点数**如何逐渐稳定。

        例如普通六面骰子的理论平均值为：

        **3.5**
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        sides = st.selectbox(
            "骰子面数",
            [4, 6, 8, 10, 12, 20],
            index=1,
        )

    with col2:
        trials = st.slider(
            "投掷次数",
            10,
            50000,
            1000,
            10,
        )

    with col3:
        seed = st.number_input(
            "随机种子",
            0,
            99999,
            42,
        )

    run = st.button(
        "🎲 开始实验",
        key="dice_run"
    )

    if run:

        rng = np.random.default_rng(seed)

        data = rng.integers(
            1,
            sides + 1,
            trials
        )

        cumulative_mean = (
            np.cumsum(data)
            /
            np.arange(1, trials + 1)
        )

        theoretical_mean = (
            sides + 1
        ) / 2

        st.session_state.experiment_data = (
            data,
            cumulative_mean,
            theoretical_mean
        )

        st.session_state.experiment_name = experiment


# ============================================================
# 8. 实验三：篮球罚球
# ============================================================

elif experiment == "🏀 篮球罚球":

    st.subheader("🏀 篮球罚球命中率实验")

    st.write(
        """
        假设一名球员有一个稳定的真实罚球命中率。

        但是我们只能通过实际投篮来估计这个命中率。

        **问题：投篮次数越多，我们得到的命中率会不会越稳定？**
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        probability = st.slider(
            "真实命中率",
            0.1,
            0.95,
            0.75,
            0.05,
        )

    with col2:
        trials = st.slider(
            "投篮次数",
            10,
            50000,
            1000,
            10,
        )

    with col3:
        seed = st.number_input(
            "随机种子",
            0,
            99999,
            42,
        )

    run = st.button(
        "🏀 开始投篮",
        key="basketball_run"
    )

    if run:

        rng = np.random.default_rng(seed)

        data = rng.binomial(
            1,
            probability,
            trials
        )

        cumulative = np.cumsum(data) / np.arange(
            1,
            trials + 1
        )

        st.session_state.experiment_data = (
            data,
            cumulative,
            probability
        )

        st.session_state.experiment_name = experiment


# ============================================================
# 9. 实验四：射击
# ============================================================

elif experiment == "🎯 射击命中":

    st.subheader("🎯 射击命中率实验")

    st.write(
        """
        假设射击者每次射击命中的概率相同。

        通过大量射击，我们观察：

        **实际命中率是否逐渐接近真实命中率？**
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        probability = st.slider(
            "真实命中率",
            0.05,
            0.95,
            0.60,
            0.05,
        )

    with col2:
        trials = st.slider(
            "射击次数",
            10,
            50000,
            1000,
            10,
        )

    with col3:
        seed = st.number_input(
            "随机种子",
            0,
            99999,
            42,
        )

    run = st.button(
        "🎯 开始射击",
        key="shoot_run"
    )

    if run:

        rng = np.random.default_rng(seed)

        data = rng.binomial(
            1,
            probability,
            trials
        )

        cumulative = np.cumsum(data) / np.arange(
            1,
            trials + 1
        )

        st.session_state.experiment_data = (
            data,
            cumulative,
            probability
        )

        st.session_state.experiment_name = experiment


# ============================================================
# 10. 实验五：抽奖箱
# ============================================================

elif experiment == "🎁 抽奖箱":

    st.subheader("🎁 抽奖箱实验")

    st.write(
        """
        一个抽奖箱中有三种奖品：

        🥇 一等奖

        🥈 二等奖

        🥉 三等奖

        你可以自己设置一等奖和二等奖的概率，
        剩余概率自动作为三等奖。
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        p_first = st.slider(
            "一等奖概率",
            0.05,
            0.5,
            0.10,
            0.05,
        )

    with col2:
        p_second = st.slider(
            "二等奖概率",
            0.05,
            0.5,
            0.20,
            0.05,
        )

    with col3:
        trials = st.slider(
            "抽奖次数",
            10,
            50000,
            1000,
            10,
        )

    seed = st.number_input(
        "随机种子",
        0,
        99999,
        42,
    )

    if p_first + p_second >= 1:

        st.error(
            "一等奖和二等奖的概率之和必须小于 1。"
        )

    else:

        p_third = 1 - p_first - p_second

        st.info(
            f"""
            当前概率：

            🥇 一等奖：{p_first:.0%}

            🥈 二等奖：{p_second:.0%}

            🥉 三等奖：{p_third:.0%}
            """
        )

        run = st.button(
            "🎁 开始抽奖",
            key="lottery_run"
        )

        if run:

            rng = np.random.default_rng(seed)

            data = rng.choice(
                [1, 2, 3],
                size=trials,
                p=[
                    p_first,
                    p_second,
                    p_third
                ]
            )

            first_frequency = (
                np.cumsum(data == 1)
                /
                np.arange(1, trials + 1)
            )

            second_frequency = (
                np.cumsum(data == 2)
                /
                np.arange(1, trials + 1)
            )

            third_frequency = (
                np.cumsum(data == 3)
                /
                np.arange(1, trials + 1)
            )

            st.session_state.experiment_data = (
                data,
                first_frequency,
                second_frequency,
                third_frequency,
                p_first,
                p_second,
                p_third
            )

            st.session_state.experiment_name = experiment


# ============================================================
# 11. 实验六：随机抽样
# ============================================================

elif experiment == "👥 随机抽样":

    st.subheader("👥 随机抽样实验")

    st.write(
        """
        假设一个总体中有一定比例的人支持某个观点。

        我们无法调查所有人，
        只能随机抽取一部分人进行调查。

        **问题：样本越大，我们得到的结果是否越稳定？**
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        population_probability = st.slider(
            "总体真实比例",
            0.1,
            0.9,
            0.6,
            0.05,
        )

    with col2:
        sample_size = st.slider(
            "每次抽样人数",
            10,
            5000,
            100,
            10,
        )

    with col3:
        repetitions = st.slider(
            "重复抽样次数",
            10,
            1000,
            200,
            10,
        )

    seed = st.number_input(
        "随机种子",
        0,
        99999,
        42,
    )

    run = st.button(
        "👥 开始抽样",
        key="sample_run"
    )

    if run:

        rng = np.random.default_rng(seed)

        results = rng.binomial(
            sample_size,
            population_probability,
            repetitions
        ) / sample_size

        st.session_state.experiment_data = (
            results,
            population_probability
        )

        st.session_state.experiment_name = experiment


# ============================================================
# 12. 显示实验结果
# ============================================================

if (
    st.session_state.experiment_data is not None
    and
    st.session_state.experiment_name == experiment
):

    st.divider()

    st.subheader("📊 实验结果")

    data = st.session_state.experiment_data


    # ========================================================
    # 抛硬币 / 罚球 / 射击
    # ========================================================

    if experiment in [
        "🪙 抛硬币",
        "🏀 篮球罚球",
        "🎯 射击命中"
    ]:

        raw_data, cumulative, theoretical = data

        final_value = cumulative[-1]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "实验次数",
            f"{len(raw_data):,}"
        )

        col2.metric(
            "理论概率",
            f"{theoretical:.4f}"
        )

        col3.metric(
            "最终实验频率",
            f"{final_value:.4f}",
            delta=f"{final_value - theoretical:+.4f}"
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
        )

        x = np.arange(
            1,
            len(raw_data) + 1
        )

        ax.plot(
            x,
            cumulative,
            linewidth=1.5,
            label="实验频率"
        )

        ax.axhline(
            theoretical,
            linestyle="--",
            linewidth=2,
            label=f"理论概率 = {theoretical:.2f}"
        )

        ax.set_xlabel(
            "实验次数"
        )

        ax.set_ylabel(
            "累计频率"
        )

        ax.set_ylim(
            0,
            1
        )

        ax.set_title(
            "实验频率随实验次数的变化"
        )

        ax.grid(
            True,
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(fig)


    # ========================================================
    # 掷骰子
    # ========================================================

    elif experiment == "🎲 掷骰子":

        raw_data, cumulative_mean, theoretical_mean = data

        final_mean = cumulative_mean[-1]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "投掷次数",
            f"{len(raw_data):,}"
        )

        col2.metric(
            "理论平均值",
            f"{theoretical_mean:.4f}"
        )

        col3.metric(
            "最终样本平均值",
            f"{final_mean:.4f}",
            delta=f"{final_mean - theoretical_mean:+.4f}"
        )

        x = np.arange(
            1,
            len(raw_data) + 1
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
        )

        ax.plot(
            x,
            cumulative_mean,
            linewidth=1.5,
            label="累计平均值"
        )

        ax.axhline(
            theoretical_mean,
            linestyle="--",
            linewidth=2,
            label=f"理论平均值 = {theoretical_mean:.2f}"
        )

        ax.set_xlabel(
            "投掷次数"
        )

        ax.set_ylabel(
            "平均点数"
        )

        ax.set_title(
            "骰子平均点数的变化"
        )

        ax.grid(
            True,
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(fig)

        # 频数统计

        st.subheader("🎲 各点数出现次数")

        unique, counts = np.unique(
            raw_data,
            return_counts=True
        )

        fig2, ax2 = plt.subplots(
            figsize=(10, 4)
        )

        ax2.bar(
            unique,
            counts
        )

        ax2.set_xlabel(
            "点数"
        )

        ax2.set_ylabel(
            "出现次数"
        )

        ax2.set_title(
            "骰子各点数出现频数"
        )

        st.pyplot(fig2)


    # ========================================================
    # 抽奖箱
    # ========================================================

    elif experiment == "🎁 抽奖箱":

        (
            raw_data,
            first_frequency,
            second_frequency,
            third_frequency,
            p_first,
            p_second,
            p_third
        ) = data

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "一等奖最终频率",
            f"{first_frequency[-1]:.4f}",
            delta=f"{first_frequency[-1] - p_first:+.4f}"
        )

        col2.metric(
            "二等奖最终频率",
            f"{second_frequency[-1]:.4f}",
            delta=f"{second_frequency[-1] - p_second:+.4f}"
        )

        col3.metric(
            "三等奖最终频率",
            f"{third_frequency[-1]:.4f}",
            delta=f"{third_frequency[-1] - p_third:+.4f}"
        )

        x = np.arange(
            1,
            len(raw_data) + 1
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
        )

        ax.plot(
            x,
            first_frequency,
            label="一等奖"
        )

        ax.plot(
            x,
            second_frequency,
            label="二等奖"
        )

        ax.plot(
            x,
            third_frequency,
            label="三等奖"
        )

        ax.axhline(
            p_first,
            linestyle="--"
        )

        ax.axhline(
            p_second,
            linestyle="--"
        )

        ax.axhline(
            p_third,
            linestyle="--"
        )

        ax.set_xlabel(
            "抽奖次数"
        )

        ax.set_ylabel(
            "累计频率"
        )

        ax.set_title(
            "各奖项累计频率变化"
        )

        ax.grid(
            True,
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(fig)


    # ========================================================
    # 随机抽样
    # ========================================================

    elif experiment == "👥 随机抽样":

        results, true_probability = data

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "重复抽样次数",
            f"{len(results):,}"
        )

        col2.metric(
            "总体真实比例",
            f"{true_probability:.4f}"
        )

        col3.metric(
            "样本比例平均值",
            f"{np.mean(results):.4f}"
        )

        # 分布

        fig, ax = plt.subplots(
            figsize=(11, 5)
        )

        ax.hist(
            results,
            bins=25,
            alpha=0.75
        )

        ax.axvline(
            true_probability,
            linestyle="--",
            linewidth=2,
            label=f"总体真实比例 = {true_probability:.2f}"
        )

        ax.set_xlabel(
            "样本比例"
        )

        ax.set_ylabel(
            "出现次数"
        )

        ax.set_title(
            "重复抽样得到的样本比例分布"
        )

        ax.grid(
            True,
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(fig)


# ============================================================
# 13. 页面底部提示
# ============================================================

st.divider()

st.info(
    """
    💡 **实验提示**

    不要急着看理论结论。

    你可以尝试：

    **① 改变实验参数 → ② 重新实验 → ③ 比较结果 → ④ 思考你发现了什么。**

    当你在不同实验中反复看到类似的现象时，
    你就正在接近大数定律的核心思想。
    """
)

st.caption(
    "🎲 大数定律交互实验室 | Python + NumPy + Matplotlib + Streamlit"
)
