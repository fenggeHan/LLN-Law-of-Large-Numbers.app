import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. 页面配置
# ============================================================

st.set_page_config(
    page_title="大数定律实验室",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. 页面 CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- 整体页面 ---------- */

    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }


    /* ---------- 顶部 ---------- */

    .page-title {
        font-size: 34px;
        font-weight: 750;
        color: #172033;
        line-height: 1.2;
        margin-bottom: 4px;
    }

    .page-subtitle {
        font-size: 15px;
        color: #737d8d;
        margin-bottom: 12px;
    }


    /* ---------- 左侧控制台 ---------- */

    .control-card {
        background: #ffffff;
        border: 1px solid #e4e8ef;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 3px 14px rgba(0, 0, 0, 0.035);
    }

    .control-title {
        font-size: 20px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 3px;
    }

    .control-subtitle {
        font-size: 13px;
        color: #8a93a3;
        margin-bottom: 17px;
    }

    .control-section {
        font-size: 13px;
        font-weight: 700;
        color: #626c7c;
        margin-bottom: 7px;
    }


    /* ---------- 右侧实验区 ---------- */

    .result-card {
        background: #ffffff;
        border: 1px solid #e4e8ef;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 3px 14px rgba(0, 0, 0, 0.035);
    }

    .result-title {
        font-size: 22px;
        font-weight: 720;
        color: #172033;
        margin-bottom: 3px;
    }

    .result-subtitle {
        font-size: 14px;
        color: #7c8696;
        margin-bottom: 18px;
    }


    /* ---------- 指标 ---------- */

    .metric-box {
        background: #f7f9fc;
        border: 1px solid #edf0f4;
        border-radius: 12px;
        padding: 13px 16px;
    }

    .metric-name {
        font-size: 12px;
        color: #8a93a3;
        margin-bottom: 3px;
    }

    .metric-number {
        font-size: 23px;
        font-weight: 720;
        color: #172033;
    }


    /* ---------- 图表标题 ---------- */

    .chart-heading {
        font-size: 17px;
        font-weight: 700;
        color: #172033;
        margin-top: 20px;
        margin-bottom: 5px;
    }


    /* ---------- 实验观察 ---------- */

    .observation {
        background: #f7f9fc;
        border-left: 4px solid #6c8ebf;
        border-radius: 8px;
        padding: 13px 16px;
        margin-top: 14px;
    }

    .observation-title {
        font-size: 14px;
        font-weight: 700;
        color: #253047;
        margin-bottom: 4px;
    }

    .observation-text {
        font-size: 13px;
        line-height: 1.65;
        color: #687385;
    }


    /* ---------- 开始按钮 ---------- */

    .stButton > button {
        border-radius: 9px;
        min-height: 40px;
        font-weight: 650;
    }


    /* ---------- Streamlit 默认元素 ---------- */

    div[data-testid="stMetric"] {
        background: #f7f9fc;
        border: 1px solid #edf0f4;
        padding: 10px;
        border-radius: 10px;
    }

    hr {
        margin: 12px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. Session State
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "last_experiment" not in st.session_state:
    st.session_state.last_experiment = None


# ============================================================
# 4. 顶部标题
# ============================================================

st.markdown(
    '<div class="page-title">🎲 大数定律实验室</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">'
    '通过亲自进行随机实验，观察随机现象如何逐渐呈现稳定规律。'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# 5. 左右主体
# ============================================================

left, right = st.columns(
    [1, 3.2],
    gap="medium",
)


# ============================================================
# 6. 左侧：实验控制台
# ============================================================

with left:

    st.markdown(
        """
        <div class="control-card">

            <div class="control-title">
                🔬 实验控制台
            </div>

            <div class="control-subtitle">
                选择实验并调整参数
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # 实验选择
    # --------------------------------------------------------

    st.markdown(
        '<div class="control-section">实验项目</div>',
        unsafe_allow_html=True,
    )

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
        label_visibility="collapsed",
    )


    st.divider()


    # --------------------------------------------------------
    # 实验说明
    # --------------------------------------------------------

    descriptions = {

        "🪙 抛硬币":
            "观察正面出现的累计频率。",

        "🎲 掷骰子":
            "观察骰子的样本平均值。",

        "🏀 篮球罚球":
            "观察罚球命中率的变化。",

        "🎯 射击命中":
            "观察大量射击后的命中率。",

        "🎁 抽奖箱":
            "观察不同奖项出现的频率。",

        "👥 随机抽样":
            "观察样本比例的变化。",
    }

    st.caption(
        descriptions[experiment]
    )


    # ========================================================
    # 参数区域
    # ========================================================

    st.markdown(
        '<div class="control-section">⚙️ 实验参数</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # 抛硬币
    # ========================================================

    if experiment == "🪙 抛硬币":

        p = st.slider(
            "正面概率",
            min_value=0.05,
            max_value=0.95,
            value=0.50,
            step=0.05,
        )

        n = st.slider(
            "投掷次数",
            min_value=10,
            max_value=50000,
            value=1000,
            step=10,
        )


    # ========================================================
    # 骰子
    # ========================================================

    elif experiment == "🎲 掷骰子":

        sides = st.selectbox(
            "骰子面数",
            [4, 6, 8, 10, 12, 20],
            index=1,
        )

        n = st.slider(
            "投掷次数",
            min_value=10,
            max_value=50000,
            value=1000,
            step=10,
        )


    # ========================================================
    # 篮球
    # ========================================================

    elif experiment == "🏀 篮球罚球":

        p = st.slider(
            "真实命中率",
            min_value=0.10,
            max_value=0.95,
            value=0.75,
            step=0.05,
        )

        n = st.slider(
            "投篮次数",
            min_value=10,
            max_value=50000,
            value=1000,
            step=10,
        )


    # ========================================================
    # 射击
    # ========================================================

    elif experiment == "🎯 射击命中":

        p = st.slider(
            "真实命中率",
            min_value=0.05,
            max_value=0.95,
            value=0.60,
            step=0.05,
        )

        n = st.slider(
            "射击次数",
            min_value=10,
            max_value=50000,
            value=1000,
            step=10,
        )


    # ========================================================
    # 抽奖
    # ========================================================

    elif experiment == "🎁 抽奖箱":

        p1 = st.slider(
            "一等奖概率",
            min_value=0.05,
            max_value=0.50,
            value=0.10,
            step=0.05,
        )

        p2 = st.slider(
            "二等奖概率",
            min_value=0.05,
            max_value=0.50,
            value=0.20,
            step=0.05,
        )

        p3 = 1 - p1 - p2

        if p3 < 0:

            st.error(
                "概率之和不能超过 1"
            )

        else:

            st.caption(
                f"🥉 三等奖概率：{p3:.0%}"
            )

        n = st.slider(
            "抽奖次数",
            min_value=10,
            max_value=50000,
            value=1000,
            step=10,
        )


    # ========================================================
    # 随机抽样
    # ========================================================

    elif experiment == "👥 随机抽样":

        population_p = st.slider(
            "总体真实比例",
            min_value=0.10,
            max_value=0.90,
            value=0.60,
            step=0.05,
        )

        sample_size = st.slider(
            "每次抽样人数",
            min_value=10,
            max_value=5000,
            value=100,
            step=10,
        )

        repetitions = st.slider(
            "重复抽样次数",
            min_value=10,
            max_value=2000,
            value=200,
            step=10,
        )


    # ========================================================
    # 操作按钮
    # ========================================================

    st.divider()

    if st.button(
        "▶ 开始实验",
        type="primary",
        use_container_width=True,
    ):

        rng = np.random.default_rng()

        # ----------------------------------------------------
        # 概率型实验
        # ----------------------------------------------------

        if experiment in [
            "🪙 抛硬币",
            "🏀 篮球罚球",
            "🎯 射击命中",
        ]:

            data = rng.binomial(
                1,
                p,
                n,
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
                "theoretical": p,
            }


        # ----------------------------------------------------
        # 骰子
        # ----------------------------------------------------

        elif experiment == "🎲 掷骰子":

            data = rng.integers(
                1,
                sides + 1,
                n,
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
                "theoretical": (sides + 1) / 2,
            }


        # ----------------------------------------------------
        # 抽奖
        # ----------------------------------------------------

        elif experiment == "🎁 抽奖箱":

            if p3 >= 0:

                data = rng.choice(
                    [1, 2, 3],
                    size=n,
                    p=[p1, p2, p3],
                )

                x = np.arange(
                    1,
                    n + 1,
                )

                f1 = (
                    np.cumsum(data == 1)
                    /
                    x
                )

                f2 = (
                    np.cumsum(data == 2)
                    /
                    x
                )

                f3 = (
                    np.cumsum(data == 3)
                    /
                    x
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


        # ----------------------------------------------------
        # 随机抽样
        # ----------------------------------------------------

        elif experiment == "👥 随机抽样":

            results = (
                rng.binomial(
                    sample_size,
                    population_p,
                    repetitions,
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


    if st.button(
        "↻ 清除实验结果",
        use_container_width=True,
    ):

        st.session_state.result = None
        st.rerun()


    # --------------------------------------------------------
    # 左侧底部提示
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        """
        **💡 小提示**

        不要只做一次实验。

        可以先用较少次数运行，
        再把实验次数逐渐增加。

        **观察曲线发生了什么变化。**
        """
    )


# ============================================================
# 7. 右侧：实验结果
# ============================================================

with right:

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="result-title">{experiment}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="result-subtitle">'
        f'{descriptions[experiment]}'
        f'</div>',
        unsafe_allow_html=True,
    )


    result = st.session_state.result


    # ========================================================
    # 尚未开始实验
    # ========================================================

    if result is None:

        st.info(
            """
            👈 **请从左侧开始实验**

            调整实验参数后，点击
            **“▶ 开始实验”**。

            实验结果将在这里显示。
            """
        )

        st.markdown(
            """
            ### 🔍 建议观察

            **实验次数较少时：**

            结果是否非常不稳定？

            **逐渐增加实验次数：**

            曲线是否出现某种趋势？

            **改变实验参数：**

            最终结果是否随之改变？
            """
        )


    # ========================================================
    # 概率型实验
    # ========================================================

    elif result["type"] == "probability":

        data = result["data"]
        cumulative = result["cumulative"]
        theoretical = result["theoretical"]

        final = cumulative[-1]

        # ----------------------------------------------------
        # 指标
        # ----------------------------------------------------

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-name">
                        实验次数
                    </div>

                    <div class="metric-number">
                        {len(data):,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-name">
                        理论概率
                    </div>

                    <div class="metric-number">
                        {theoretical:.2%}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-name">
                        最终实验频率
                    </div>

                    <div class="metric-number">
                        {final:.2%}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


        # ----------------------------------------------------
        # 图表
        # ----------------------------------------------------

        st.markdown(
            '<div class="chart-heading">'
            '📈 累计频率变化'
            '</div>',
            unsafe_allow_html=True,
        )

        x = np.arange(
            1,
            len(data) + 1,
        )

        fig, ax = plt.subplots(
            figsize=(11, 4.8),
        )

        ax.plot(
            x,
            cumulative,
            linewidth=1.7,
            label="实验累计频率",
        )

        ax.axhline(
            theoretical,
            linestyle="--",
            linewidth=1.8,
            label=f"理论概率 = {theoretical:.2f}",
        )

        ax.set_xlabel(
            "实验次数"
        )

        ax.set_ylabel(
            "累计频率"
        )

        ax.set_ylim(
            0,
            1,
        )

        ax.grid(
            linestyle=":",
            alpha=0.35,
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True,
        )


        # ----------------------------------------------------
        # 观察
        # ----------------------------------------------------

        error = abs(
            final - theoretical
        )

        st.markdown(
            f"""
            <div class="observation">

                <div class="observation-title">
                    💡 实验观察
                </div>

                <div class="observation-text">

                    最终实验频率为
                    <b>{final:.2%}</b>，

                    理论概率为
                    <b>{theoretical:.2%}</b>。

                    当前两者相差
                    <b>{error:.2%}</b>。

                    <br>

                    可以增加实验次数，
                    看看这种差距是否会进一步缩小。

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # 骰子
    # ========================================================

    elif result["type"] == "mean":

        data = result["data"]
        cumulative = result["cumulative"]
        theoretical = result["theoretical"]

        final = cumulative[-1]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "投掷次数",
            f"{len(data):,}",
        )

        c2.metric(
            "理论平均值",
            f"{theoretical:.3f}",
        )

        c3.metric(
            "实际平均值",
            f"{final:.3f}",
            delta=f"{final - theoretical:+.3f}",
        )


        st.markdown(
            '<div class="chart-heading">'
            '📈 样本平均值变化'
            '</div>',
            unsafe_allow_html=True,
        )

        x = np.arange(
            1,
            len(data) + 1,
        )

        fig, ax = plt.subplots(
            figsize=(11, 4.8),
        )

        ax.plot(
            x,
            cumulative,
            linewidth=1.7,
            label="累计平均值",
        )

        ax.axhline(
            theoretical,
            linestyle="--",
            linewidth=1.8,
            label=f"理论平均值 = {theoretical:.2f}",
        )

        ax.set_xlabel(
            "投掷次数"
        )

        ax.set_ylabel(
            "样本平均值"
        )

        ax.grid(
            linestyle=":",
            alpha=0.35,
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True,
        )


    # ========================================================
    # 抽奖
    # ========================================================

    elif result["type"] == "lottery":

        data = result["data"]

        f1 = result["f1"]
        f2 = result["f2"]
        f3 = result["f3"]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "一等奖",
            f"{f1[-1]:.2%}",
        )

        c2.metric(
            "二等奖",
            f"{f2[-1]:.2%}",
        )

        c3.metric(
            "三等奖",
            f"{f3[-1]:.2%}",
        )


        st.markdown(
            '<div class="chart-heading">'
            '📈 各奖项累计频率'
            '</div>',
            unsafe_allow_html=True,
        )

        x = np.arange(
            1,
            len(data) + 1,
        )

        fig, ax = plt.subplots(
            figsize=(11, 4.8),
        )

        ax.plot(
            x,
            f1,
            label="一等奖",
        )

        ax.plot(
            x,
            f2,
            label="二等奖",
        )

        ax.plot(
            x,
            f3,
            label="三等奖",
        )

        ax.axhline(
            result["p1"],
            linestyle="--",
            alpha=0.6,
        )

        ax.axhline(
            result["p2"],
            linestyle="--",
            alpha=0.6,
        )

        ax.axhline(
            result["p3"],
            linestyle="--",
            alpha=0.6,
        )

        ax.set_xlabel(
            "抽奖次数"
        )

        ax.set_ylabel(
            "累计频率"
        )

        ax.grid(
            linestyle=":",
            alpha=0.35,
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True,
        )


    # ========================================================
    # 随机抽样
    # ========================================================

    elif result["type"] == "sampling":

        results = result["results"]
        theoretical = result["theoretical"]

        average = np.mean(results)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "重复抽样次数",
            f"{len(results):,}",
        )

        c2.metric(
            "总体比例",
            f"{theoretical:.2%}",
        )

        c3.metric(
            "样本比例平均值",
            f"{average:.2%}",
        )


        st.markdown(
            '<div class="chart-heading">'
            '📊 样本比例分布'
            '</div>',
            unsafe_allow_html=True,
        )

        fig, ax = plt.subplots(
            figsize=(11, 4.8),
        )

        ax.hist(
            results,
            bins=25,
            alpha=0.75,
        )

        ax.axvline(
            theoretical,
            linestyle="--",
            linewidth=1.8,
            label=f"总体比例 = {theoretical:.2f}",
        )

        ax.set_xlabel(
            "样本比例"
        )

        ax.set_ylabel(
            "出现次数"
        )

        ax.grid(
            linestyle=":",
            alpha=0.35,
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True,
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )
