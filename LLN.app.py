import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 页面配置
# ============================================================

st.set_page_config(
    page_title="大数定律实验室",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       全局
       ===================================================== */

    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }


    /* =====================================================
       顶部标题
       ===================================================== */

    .top-title {
        font-size: 34px;
        font-weight: 750;
        letter-spacing: -1px;
        color: #172033;
        margin-bottom: 2px;
    }

    .top-subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 12px;
    }


    /* =====================================================
       左侧控制区
       ===================================================== */

    .control-panel {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.04);
        min-height: 720px;
    }

    .panel-title {
        font-size: 19px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 4px;
    }

    .panel-description {
        font-size: 13px;
        color: #8a93a3;
        margin-bottom: 20px;
    }


    /* =====================================================
       实验选择卡片
       ===================================================== */

    .experiment-header {
        font-size: 13px;
        font-weight: 650;
        color: #6b7280;
        margin-bottom: 8px;
    }


    /* =====================================================
       右侧工作区
       ===================================================== */

    .workspace {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 28px 30px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.04);
        min-height: 720px;
    }

    .workspace-title {
        font-size: 22px;
        font-weight: 720;
        color: #172033;
        margin-bottom: 2px;
    }

    .workspace-subtitle {
        color: #7b8494;
        font-size: 14px;
        margin-bottom: 20px;
    }


    /* =====================================================
       指标卡片
       ===================================================== */

    .metric-card {
        background: #f8fafc;
        border: 1px solid #edf0f4;
        border-radius: 13px;
        padding: 16px 18px;
        height: 105px;
    }

    .metric-label {
        color: #8a93a3;
        font-size: 13px;
        margin-bottom: 5px;
    }

    .metric-value {
        color: #172033;
        font-size: 26px;
        font-weight: 720;
    }


    /* =====================================================
       图表标题
       ===================================================== */

    .chart-title {
        font-size: 17px;
        font-weight: 680;
        color: #172033;
        margin-top: 22px;
        margin-bottom: 8px;
    }


    /* =====================================================
       提示区域
       ===================================================== */

    .observation-box {
        background: #f8fafc;
        border: 1px solid #e7ebf1;
        border-radius: 13px;
        padding: 16px 18px;
        margin-top: 15px;
    }

    .observation-title {
        font-weight: 680;
        color: #172033;
        margin-bottom: 5px;
    }

    .observation-text {
        color: #687385;
        font-size: 14px;
        line-height: 1.6;
    }


    /* =====================================================
       按钮
       ===================================================== */

    .stButton > button {
        border-radius: 10px;
        font-weight: 650;
        height: 43px;
    }


    /* =====================================================
       分隔线
       ===================================================== */

    hr {
        border: none;
        border-top: 1px solid #edf0f4;
        margin: 15px 0;
    }


    /* =====================================================
       隐藏 Streamlit 默认菜单
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Session State
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "experiment" not in st.session_state:
    st.session_state.experiment = "🪙 抛硬币"


# ============================================================
# 顶部
# ============================================================

st.markdown(
    '<div class="top-title">🎲 大数定律实验室</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="top-subtitle">'
    '通过随机实验，亲自观察“随机”背后逐渐出现的稳定规律。'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 真正的左右布局
# ============================================================

control, workspace = st.columns(
    [1, 3.4],
    gap="large"
)


# ============================================================
# 左侧：控制面板
# ============================================================

with control:

    st.markdown(
        '<div class="control-panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">🔬 实验控制台</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-description">'
        '选择实验并调整参数'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 实验选择
    # --------------------------------------------------------

    st.markdown(
        '<div class="experiment-header">实验项目</div>',
        unsafe_allow_html=True
    )

    experiment = st.radio(
        "",
        [
            "🪙 抛硬币",
            "🎲 掷骰子",
            "🏀 篮球罚球",
            "🎯 射击命中",
            "🎁 抽奖箱",
            "👥 随机抽样",
        ],
        index=0,
        label_visibility="collapsed"
    )


    st.divider()


    # --------------------------------------------------------
    # 参数
    # --------------------------------------------------------

    st.markdown(
        '<div class="experiment-header">⚙️ 实验参数</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # 硬币
    # ========================================================

    if experiment == "🪙 抛硬币":

        st.caption(
            "观察正面频率逐渐趋近理论概率。"
        )

        p = st.slider(
            "正面概率",
            0.05,
            0.95,
            0.50,
            0.05
        )

        n = st.slider(
            "投掷次数",
            10,
            50000,
            1000,
            10
        )

        theoretical = p


    # ========================================================
    # 骰子
    # ========================================================

    elif experiment == "🎲 掷骰子":

        st.caption(
            "观察平均点数逐渐趋近理论期望。"
        )

        sides = st.selectbox(
            "骰子面数",
            [4, 6, 8, 10, 12, 20],
            index=1
        )

        n = st.slider(
            "投掷次数",
            10,
            50000,
            1000,
            10
        )

        theoretical = (sides + 1) / 2


    # ========================================================
    # 篮球
    # ========================================================

    elif experiment == "🏀 篮球罚球":

        st.caption(
            "观察实际命中率如何逐渐稳定。"
        )

        p = st.slider(
            "真实命中率",
            0.10,
            0.95,
            0.75,
            0.05
        )

        n = st.slider(
            "投篮次数",
            10,
            50000,
            1000,
            10
        )

        theoretical = p


    # ========================================================
    # 射击
    # ========================================================

    elif experiment == "🎯 射击命中":

        st.caption(
            "观察大量射击后的累计命中率。"
        )

        p = st.slider(
            "真实命中率",
            0.05,
            0.95,
            0.60,
            0.05
        )

        n = st.slider(
            "射击次数",
            10,
            50000,
            1000,
            10
        )

        theoretical = p


    # ========================================================
    # 抽奖
    # ========================================================

    elif experiment == "🎁 抽奖箱":

        st.caption(
            "观察奖品频率是否趋近设定概率。"
        )

        p1 = st.slider(
            "一等奖概率",
            0.05,
            0.50,
            0.10,
            0.05
        )

        p2 = st.slider(
            "二等奖概率",
            0.05,
            0.50,
            0.20,
            0.05
        )

        p3 = 1 - p1 - p2

        if p3 < 0:

            st.error(
                "概率设置不合法。"
            )

        else:

            st.caption(
                f"🥉 三等奖：{p3:.0%}"
            )

        n = st.slider(
            "抽奖次数",
            10,
            50000,
            1000,
            10
        )


    # ========================================================
    # 抽样
    # ========================================================

    elif experiment == "👥 随机抽样":

        st.caption(
            "观察样本比例围绕总体比例波动。"
        )

        population_p = st.slider(
            "总体真实比例",
            0.10,
            0.90,
            0.60,
            0.05
        )

        sample_size = st.slider(
            "每次抽样人数",
            10,
            5000,
            100,
            10
        )

        repetitions = st.slider(
            "重复抽样次数",
            10,
            2000,
            200,
            10
        )


    # --------------------------------------------------------
    # 开始实验
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "▶ 开始实验",
        use_container_width=True,
        type="primary"
    ):

        rng = np.random.default_rng()

        # ----------------------------------------------------
        # 硬币 / 篮球 / 射击
        # ----------------------------------------------------

        if experiment in [
            "🪙 抛硬币",
            "🏀 篮球罚球",
            "🎯 射击命中"
        ]:

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


        # ----------------------------------------------------
        # 骰子
        # ----------------------------------------------------

        elif experiment == "🎲 掷骰子":

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


        # ----------------------------------------------------
        # 抽奖
        # ----------------------------------------------------

        elif experiment == "🎁 抽奖箱":

            if p3 >= 0:

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
                    "p3": p3
                }


        # ----------------------------------------------------
        # 随机抽样
        # ----------------------------------------------------

        elif experiment == "👥 随机抽样":

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
                "theoretical": population_p
            }


    if st.button(
        "↻ 清除实验结果",
        use_container_width=True
    ):

        st.session_state.result = None
        st.rerun()


    st.divider()

    st.markdown(
        """
        **💡 实验建议**

        先运行一次。

        然后改变一个参数，再运行一次。

        比较两次结果有什么不同。

        **试着自己发现规律。**
        """
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 右侧：实验工作区
# ============================================================

with workspace:

    st.markdown(
        '<div class="workspace">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="workspace-title">{experiment}</div>',
        unsafe_allow_html=True
    )

    descriptions = {
        "🪙 抛硬币":
            "观察正面出现的累计频率如何随着实验次数增加而变化。",
        "🎲 掷骰子":
            "观察样本平均值如何逐渐接近骰子的理论期望。",
        "🏀 篮球罚球":
            "观察实际罚球命中率是否逐渐接近真实命中率。",
        "🎯 射击命中":
            "观察大量射击后累计命中率的变化。",
        "🎁 抽奖箱":
            "观察不同奖项的累计频率是否逐渐稳定。",
        "👥 随机抽样":
            "观察重复抽样得到的样本比例如何围绕总体比例变化。"
    }

    st.markdown(
        f'<div class="workspace-subtitle">'
        f'{descriptions[experiment]}'
        f'</div>',
        unsafe_allow_html=True
    )


    result = st.session_state.result


    # ========================================================
    # 没有结果
    # ========================================================

    if result is None:

        st.info(
            """
            👈 **从左侧开始你的实验**

            调整参数后点击 **“开始实验”**。

            实验数据和图像会显示在这里。
            """
        )

        st.markdown(
            """
            ### 🔍 实验过程中可以思考

            **①** 实验次数很少的时候，结果稳定吗？

            **②** 增加实验次数之后发生了什么？

            **③** 改变理论概率以后，最终结果会不会发生变化？

            **④** 不同的随机实验之间，有没有共同的现象？
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
        # 三个指标
        # ----------------------------------------------------

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">实验次数</div>
                    <div class="metric-value">
                        {len(data):,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">理论概率</div>
                    <div class="metric-value">
                        {theoretical:.2%}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">最终实验频率</div>
                    <div class="metric-value">
                        {final:.2%}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # 图表
        # ----------------------------------------------------

        st.markdown(
            '<div class="chart-title">'
            '📈 累计频率变化'
            '</div>',
            unsafe_allow_html=True
        )

        x = np.arange(
            1,
            len(data) + 1
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
        )

        ax.plot(
            x,
            cumulative,
            linewidth=1.8,
            label="实验累计频率"
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

        ax.grid(
            linestyle=":",
            alpha=0.35
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )


        # ----------------------------------------------------
        # 观察
        # ----------------------------------------------------

        error = abs(
            final - theoretical
        )

        st.markdown(
            f"""
            <div class="observation-box">

                <div class="observation-title">
                    💡 实验观察
                </div>

                <div class="observation-text">

                    最终实验频率为
                    <b>{final:.2%}</b>，

                    与理论概率
                    <b>{theoretical:.2%}</b>

                    的差值为
                    <b>{error:.2%}</b>。

                    <br><br>

                    可以尝试把实验次数调大，
                    再观察曲线的变化。

                </div>

            </div>
            """,
            unsafe_allow_html=True
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
            f"{len(data):,}"
        )

        c2.metric(
            "理论平均值",
            f"{theoretical:.3f}"
        )

        c3.metric(
            "样本平均值",
            f"{final:.3f}",
            delta=f"{final - theoretical:+.3f}"
        )

        st.markdown(
            '<div class="chart-title">'
            '📈 样本平均值变化'
            '</div>',
            unsafe_allow_html=True
        )

        x = np.arange(
            1,
            len(data) + 1
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
        )

        ax.plot(
            x,
            cumulative,
            linewidth=1.8,
            label="累计平均值"
        )

        ax.axhline(
            theoretical,
            linestyle="--",
            linewidth=2,
            label=f"理论平均值 = {theoretical:.2f}"
        )

        ax.set_xlabel(
            "投掷次数"
        )

        ax.set_ylabel(
            "样本平均值"
        )

        ax.grid(
            linestyle=":",
            alpha=0.35
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )


    # ========================================================
    # 抽奖
    # ========================================================

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
            f"{f1[-1]:.2%}"
        )

        c2.metric(
            "二等奖",
            f"{f2[-1]:.2%}"
        )

        c3.metric(
            "三等奖",
            f"{f3[-1]:.2%}"
        )

        st.markdown(
            '<div class="chart-title">'
            '📈 各奖项累计频率'
            '</div>',
            unsafe_allow_html=True
        )

        x = np.arange(
            1,
            len(data) + 1
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
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

        ax.set_xlabel(
            "抽奖次数"
        )

        ax.set_ylabel(
            "累计频率"
        )

        ax.grid(
            linestyle=":",
            alpha=0.35
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
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
            "重复抽样",
            f"{len(results):,} 次"
        )

        c2.metric(
            "总体真实比例",
            f"{theoretical:.2%}"
        )

        c3.metric(
            "样本比例平均值",
            f"{average:.2%}"
        )

        st.markdown(
            '<div class="chart-title">'
            '📊 样本比例分布'
            '</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
        )

        ax.hist(
            results,
            bins=25,
            alpha=0.75
        )

        ax.axvline(
            theoretical,
            linestyle="--",
            linewidth=2,
            label=f"总体比例 = {theoretical:.2f}"
        )

        ax.set_xlabel(
            "样本比例"
        )

        ax.set_ylabel(
            "出现次数"
        )

        ax.grid(
            linestyle=":",
            alpha=0.35
        )

        ax.legend()

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
