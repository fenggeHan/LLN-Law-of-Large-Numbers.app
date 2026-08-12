import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 页面设置
# =========================================================

st.set_page_config(
    page_title="大数定律交互实验室",
    page_icon="🎲",
    layout="wide",
)


# =========================================================
# CSS：左右实验室布局
# =========================================================

st.markdown(
    """
    <style>

    /* 页面整体 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* 主标题 */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #666;
        margin-bottom: 20px;
    }

    /* 左侧控制台 */
    .control-panel {
        background-color: #f7f8fa;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e5e5e5;
    }

    /* 右侧结果区 */
    .result-panel {
        padding: 5px 15px;
    }

    /* 小标题 */
    .section-title {
        font-size: 20px;
        font-weight: 650;
        margin-bottom: 12px;
    }

    /* 实验说明 */
    .experiment-description {
        background-color: #f8f9fb;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4c78a8;
        margin-bottom: 18px;
    }

    /* 结果卡片 */
    .result-card {
        background-color: #f8f9fb;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #eeeeee;
    }

    .result-label {
        font-size: 14px;
        color: #777;
    }

    .result-value {
        font-size: 27px;
        font-weight: 700;
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# session_state
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "last_experiment" not in st.session_state:
    st.session_state.last_experiment = None


# =========================================================
# 页面标题
# =========================================================

st.markdown(
    '<div class="main-title">🎲 大数定律交互实验室</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '选择一个随机实验，自己调整参数，观察随机现象如何逐渐呈现稳定规律。'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# 左右布局
# =========================================================

left, right = st.columns(
    [1, 2.5],
    gap="large"
)


# =========================================================
# 左侧：实验控制台
# =========================================================

with left:

    st.markdown(
        '<div class="section-title">🔬 实验控制台</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # 实验选择
    # -----------------------------------------------------

    experiment = st.selectbox(
        "选择实验",
        [
            "🪙 抛硬币",
            "🎲 掷骰子",
            "🏀 篮球罚球",
            "🎯 射击命中",
            "🎁 抽奖箱",
            "👥 随机抽样",
        ],
    )

    st.divider()

    st.markdown(
        '<div class="section-title">⚙️ 实验参数</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # 硬币
    # =====================================================

    if experiment == "🪙 抛硬币":

        st.caption(
            "观察正面出现的累计频率如何变化。"
        )

        p = st.slider(
            "正面概率",
            0.05,
            0.95,
            0.50,
            0.05,
        )

        n = st.slider(
            "投掷次数",
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

        theoretical = p

        if st.button(
            "▶ 开始实验",
            use_container_width=True
        ):

            rng = np.random.default_rng(seed)

            data = rng.binomial(
                1,
                p,
                n
            )

            cumulative = (
                np.cumsum(data)
                /
                np.arange(1, n + 1)
            )

            st.session_state.result = {
                "type": "probability",
                "data": data,
                "cumulative": cumulative,
                "theoretical": theoretical,
            }

            st.session_state.last_experiment = experiment


    # =====================================================
    # 骰子
    # =====================================================

    elif experiment == "🎲 掷骰子":

        st.caption(
            "观察骰子的样本平均值如何接近理论期望。"
        )

        sides = st.selectbox(
            "骰子面数",
            [4, 6, 8, 10, 12, 20],
            index=1,
        )

        n = st.slider(
            "投掷次数",
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

        theoretical = (sides + 1) / 2

        if st.button(
            "▶ 开始实验",
            use_container_width=True
        ):

            rng = np.random.default_rng(seed)

            data = rng.integers(
                1,
                sides + 1,
                n
            )

            cumulative = (
                np.cumsum(data)
                /
                np.arange(1, n + 1)
            )

            st.session_state.result = {
                "type": "mean",
                "data": data,
                "cumulative": cumulative,
                "theoretical": theoretical,
            }

            st.session_state.last_experiment = experiment


    # =====================================================
    # 篮球
    # =====================================================

    elif experiment == "🏀 篮球罚球":

        st.caption(
            "模拟篮球运动员连续罚球。"
        )

        p = st.slider(
            "真实命中率",
            0.10,
            0.95,
            0.75,
            0.05,
        )

        n = st.slider(
            "投篮次数",
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

        theoretical = p

        if st.button(
            "▶ 开始实验",
            use_container_width=True
        ):

            rng = np.random.default_rng(seed)

            data = rng.binomial(
                1,
                p,
                n
            )

            cumulative = (
                np.cumsum(data)
                /
                np.arange(1, n + 1)
            )

            st.session_state.result = {
                "type": "probability",
                "data": data,
                "cumulative": cumulative,
                "theoretical": theoretical,
            }

            st.session_state.last_experiment = experiment


    # =====================================================
    # 射击
    # =====================================================

    elif experiment == "🎯 射击命中":

        st.caption(
            "观察大量射击后，实际命中率是否趋于稳定。"
        )

        p = st.slider(
            "真实命中率",
            0.05,
            0.95,
            0.60,
            0.05,
        )

        n = st.slider(
            "射击次数",
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

        theoretical = p

        if st.button(
            "▶ 开始实验",
            use_container_width=True
        ):

            rng = np.random.default_rng(seed)

            data = rng.binomial(
                1,
                p,
                n
            )

            cumulative = (
                np.cumsum(data)
                /
                np.arange(1, n + 1)
            )

            st.session_state.result = {
                "type": "probability",
                "data": data,
                "cumulative": cumulative,
                "theoretical": theoretical,
            }

            st.session_state.last_experiment = experiment


    # =====================================================
    # 抽奖箱
    # =====================================================

    elif experiment == "🎁 抽奖箱":

        st.caption(
            "观察不同奖项的出现频率。"
        )

        p1 = st.slider(
            "一等奖概率",
            0.05,
            0.50,
            0.10,
            0.05,
        )

        p2 = st.slider(
            "二等奖概率",
            0.05,
            0.50,
            0.20,
            0.05,
        )

        if p1 + p2 >= 1:

            st.error(
                "一等奖和二等奖概率之和必须小于 1。"
            )

            p3 = 0

        else:

            p3 = 1 - p1 - p2

            st.info(
                f"🥉 三等奖概率：{p3:.0%}"
            )

        n = st.slider(
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

        if p1 + p2 < 1:

            if st.button(
                "▶ 开始实验",
                use_container_width=True
            ):

                rng = np.random.default_rng(seed)

                data = rng.choice(
                    [1, 2, 3],
                    n,
                    p=[p1, p2, p3]
                )

                f1 = (
                    np.cumsum(data == 1)
                    /
                    np.arange(1, n + 1)
                )

                f2 = (
                    np.cumsum(data == 2)
                    /
                    np.arange(1, n + 1)
                )

                f3 = (
                    np.cumsum(data == 3)
                    /
                    np.arange(1, n + 1)
                )

                st.session_state.result = {
                    "type": "lottery",
                    "data": data,
                    "f1": f1,
                    "f2": f2,
                    "f3": f3,
                    "p1": p1,
                    "p2": p2,
                    "p3": p3,
                }

                st.session_state.last_experiment = experiment


    # =====================================================
    # 随机抽样
    # =====================================================

    elif experiment == "👥 随机抽样":

        st.caption(
            "观察随机样本比例如何围绕总体比例波动。"
        )

        population_p = st.slider(
            "总体真实比例",
            0.10,
            0.90,
            0.60,
            0.05,
        )

        sample_size = st.slider(
            "每次抽取人数",
            10,
            5000,
            100,
            10,
        )

        repetitions = st.slider(
            "重复抽样次数",
            10,
            2000,
            200,
            10,
        )

        seed = st.number_input(
            "随机种子",
            0,
            99999,
            42,
        )

        if st.button(
            "▶ 开始实验",
            use_container_width=True
        ):

            rng = np.random.default_rng(seed)

            results = (
                rng.binomial(
                    sample_size,
                    population_p,
                    repetitions
                )
                /
                sample_size
            )

            st.session_state.result = {
                "type": "sampling",
                "results": results,
                "theoretical": population_p,
            }

            st.session_state.last_experiment = experiment


    # -----------------------------------------------------
    # 重新实验按钮
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "↻ 清除实验结果",
        use_container_width=True
    ):

        st.session_state.result = None
        st.rerun()

    st.divider()

    st.markdown("### 💡 实验建议")

    st.caption(
        """
        不要只运行一次。

        可以尝试改变实验次数，
        再改变理论概率，
        比较不同情况下的结果。

        **你能发现什么规律？**
        """
    )


# =========================================================
# 右侧：实验结果
# =========================================================

with right:

    st.markdown(
        '<div class="section-title">📊 实验结果</div>',
        unsafe_allow_html=True
    )

    result = st.session_state.result


    # -----------------------------------------------------
    # 没有实验
    # -----------------------------------------------------

    if result is None:

        st.info(
            """
            👈 请先从左侧选择实验并调整参数。

            然后点击 **“开始实验”**。

            实验结果、统计数据和图像会显示在这里。
            """
        )

        st.markdown(
            """
            ### 🔍 你可以尝试

            - 改变实验次数
            - 改变真实概率
            - 重复实验
            - 比较不同参数下的结果

            **不要急着寻找答案，先观察。**
            """
        )


    # -----------------------------------------------------
    # 概率型实验
    # -----------------------------------------------------

    elif result["type"] == "probability":

        data = result["data"]
        cumulative = result["cumulative"]
        theoretical = result["theoretical"]

        final = cumulative[-1]

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                '<div class="result-card">'
                '<div class="result-label">实验次数</div>'
                f'<div class="result-value">{len(data):,}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                '<div class="result-card">'
                '<div class="result-label">理论概率</div>'
                f'<div class="result-value">{theoretical:.2%}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                '<div class="result-card">'
                '<div class="result-label">最终实验频率</div>'
                f'<div class="result-value">{final:.2%}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        st.markdown("### 📈 累计频率变化")

        fig, ax = plt.subplots(
            figsize=(11, 5)
        )

        x = np.arange(
            1,
            len(data) + 1
        )

        ax.plot(
            x,
            cumulative,
            linewidth=1.5,
            label="实验累计频率"
        )

        ax.axhline(
            theoretical,
            linestyle="--",
            linewidth=2,
            label=f"理论概率 = {theoretical:.2f}"
        )

        ax.set_xlabel("实验次数")
        ax.set_ylabel("累计频率")

        ax.set_ylim(
            max(0, theoretical - 0.5),
            min(1, theoretical + 0.5)
        )

        ax.grid(
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(
            fig,
            use_container_width=True
        )

        st.success(
            f"""
            最终结果为 **{final:.2%}**。

            与理论概率 **{theoretical:.2%}**
            的差值为 **{abs(final - theoretical):.4%}**。
            """
        )


    # -----------------------------------------------------
    # 平均值型实验：骰子
    # -----------------------------------------------------

    elif result["type"] == "mean":

        data = result["data"]
        cumulative = result["cumulative"]
        theoretical = result["theoretical"]

        final = cumulative[-1]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "投掷次数",
            f"{len(data):,}"
        )

        c2.metric(
            "理论平均值",
            f"{theoretical:.3f}"
        )

        c3.metric(
            "最终样本平均值",
            f"{final:.3f}",
            delta=f"{final - theoretical:+.3f}"
        )

        st.markdown("### 📈 样本平均值的变化")

        x = np.arange(
            1,
            len(data) + 1
        )

        fig, ax = plt.subplots(
            figsize=(11, 5)
        )

        ax.plot(
            x,
            cumulative,
            linewidth=1.5,
            label="累计平均值"
        )

        ax.axhline(
            theoretical,
            linestyle="--",
            linewidth=2,
            label=f"理论平均值 = {theoretical:.2f}"
        )

        ax.set_xlabel("投掷次数")
        ax.set_ylabel("样本平均值")

        ax.grid(
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(
            fig,
            use_container_width=True
        )

        st.markdown("### 🎲 点数分布")

        fig2, ax2 = plt.subplots(
            figsize=(11, 4)
        )

        values, counts = np.unique(
            data,
            return_counts=True
        )

        ax2.bar(
            values,
            counts
        )

        ax2.set_xlabel("点数")
        ax2.set_ylabel("出现次数")

        st.pyplot(
            fig2,
            use_container_width=True
        )


    # -----------------------------------------------------
    # 抽奖
    # -----------------------------------------------------

    elif result["type"] == "lottery":

        data = result["data"]

        f1 = result["f1"]
        f2 = result["f2"]
        f3 = result["f3"]

        p1 = result["p1"]
        p2 = result["p2"]
        p3 = result["p3"]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "一等奖",
            f"{f1[-1]:.2%}",
            delta=f"{f1[-1] - p1:+.2%}"
        )

        c2.metric(
            "二等奖",
            f"{f2[-1]:.2%}",
            delta=f"{f2[-1] - p2:+.2%}"
        )

        c3.metric(
            "三等奖",
            f"{f3[-1]:.2%}",
            delta=f"{f3[-1] - p3:+.2%}"
        )

        st.markdown(
            "### 📈 各奖项累计频率"
        )

        x = np.arange(
            1,
            len(data) + 1
        )

        fig, ax = plt.subplots(
            figsize=(11, 5)
        )

        ax.plot(
            x,
            f1,
            label="一等奖"
        )

        ax.plot(
            x,
            f2,
            label="二等奖"
        )

        ax.plot(
            x,
            f3,
            label="三等奖"
        )

        ax.axhline(
            p1,
            linestyle="--"
        )

        ax.axhline(
            p2,
            linestyle="--"
        )

        ax.axhline(
            p3,
            linestyle="--"
        )

        ax.set_xlabel("抽奖次数")
        ax.set_ylabel("累计频率")

        ax.grid(
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(
            fig,
            use_container_width=True
        )


    # -----------------------------------------------------
    # 随机抽样
    # -----------------------------------------------------

    elif result["type"] == "sampling":

        results = result["results"]
        theoretical = result["theoretical"]

        mean_result = np.mean(results)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "重复抽样次数",
            f"{len(results):,}"
        )

        c2.metric(
            "总体真实比例",
            f"{theoretical:.2%}"
        )

        c3.metric(
            "样本比例平均值",
            f"{mean_result:.2%}"
        )

        st.markdown(
            "### 📊 样本比例的分布"
        )

        fig, ax = plt.subplots(
            figsize=(11, 5)
        )

        ax.hist(
            results,
            bins=25
        )

        ax.axvline(
            theoretical,
            linestyle="--",
            linewidth=2,
            label=f"真实比例 = {theoretical:.2f}"
        )

        ax.set_xlabel("样本比例")
        ax.set_ylabel("出现次数")

        ax.grid(
            linestyle=":",
            alpha=0.5
        )

        ax.legend()

        st.pyplot(
            fig,
            use_container_width=True
        )

        st.success(
            f"""
            重复抽样得到的样本比例平均为
            **{mean_result:.2%}**，

            总体真实比例为
            **{theoretical:.2%}**。
            """
        )
