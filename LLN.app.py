import matplotlib
matplotlib.use("agg")

import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import requests


# ============================================================
# 1. 页面基础配置
# ============================================================

st.set_page_config(
    page_title="大数定律 (LLN) 交互式仿真平台",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. 中文字体配置
# ============================================================

def setup_chinese_font():
    """
    统一配置 Matplotlib 中文字体。
    优先使用项目 fonts/simhei.ttf。
    如果本地没有，则尝试从 GitHub 下载。
    """

    font_url = (
        "https://github.com/fenggeHan/"
        "CLT-Interactive-Simulation-Teaching-Platform/"
        "raw/main/simhei.ttf"
    )

    if "__file__" in locals():
        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )
    else:
        current_dir = os.getcwd()

    font_dir = os.path.join(
        current_dir,
        "fonts"
    )

    font_path = os.path.join(
        font_dir,
        "simhei.ttf"
    )

    # 避免重复加载
    if (
        "font_setup_done"
        not in st.session_state
    ):
        st.session_state.font_setup_done = False

    if st.session_state.font_setup_done:
        return

    # --------------------------------------------------------
    # 本地没有字体 → 尝试下载
    # --------------------------------------------------------

    if not os.path.exists(font_path):

        os.makedirs(
            font_dir,
            exist_ok=True
        )

        try:

            response = requests.get(
                font_url,
                timeout=15
            )

            response.raise_for_status()

            with open(
                font_path,
                "wb"
            ) as f:
                f.write(
                    response.content
                )

        except Exception:

            plt.rcParams["font.family"] = [
                "SimHei",
                "Microsoft YaHei",
                "WenQuanYi Zen Hei",
                "DejaVu Sans"
            ]

            plt.rcParams[
                "axes.unicode_minus"
            ] = False

            st.session_state.font_setup_done = True

            return

    # --------------------------------------------------------
    # 加载字体
    # --------------------------------------------------------

    try:

        fm.fontManager.addfont(
            font_path
        )

        font_prop = fm.FontProperties(
            fname=font_path
        )

        font_name = (
            font_prop.get_name()
        )

        plt.rcParams[
            "font.family"
        ] = font_name

        plt.rcParams[
            "font.sans-serif"
        ] = [font_name]

        plt.rcParams[
            "axes.unicode_minus"
        ] = False

        st.session_state.font_setup_done = True

    except Exception:

        plt.rcParams["font.family"] = [
            "SimHei",
            "Microsoft YaHei",
            "WenQuanYi Zen Hei",
            "DejaVu Sans"
        ]

        plt.rcParams[
            "axes.unicode_minus"
        ] = False

        st.session_state.font_setup_done = True


setup_chinese_font()


# ============================================================
# 3. 页面标题
# ============================================================

st.markdown(
    """
    <h1 style="
        font-size:32px;
        margin-bottom:20px;
    ">
        🎲 大数定律 (LLN) 交互式仿真平台
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    大数定律告诉我们：当一个随机实验被大量重复进行时，
    <b>随机结果的平均表现会逐渐趋近于一个稳定的理论值。</b>
    <br><br>
    本平台提供多个生活化随机实验，你可以自行调整参数，
    亲自观察“随机”如何逐渐呈现“稳定规律”。
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. 初始化 Session State
# ============================================================

if "lln_result" not in st.session_state:
    st.session_state.lln_result = None

if "lln_experiment" not in st.session_state:
    st.session_state.lln_experiment = None


# ============================================================
# 5. 实验名称
# ============================================================

experiment_list = [

    "🪙 抛硬币",

    "🎲 掷骰子",

    "🏀 篮球罚球",

    "🎯 射击命中",

    "🎁 抽奖箱",

    "👥 随机抽样",

    "🏭 产品质量检测",

    "🚕 随机等待时间"

]


# ============================================================
# 6. 侧边栏：实验控制台
# ============================================================

st.sidebar.header("🔧 实验控制台")

st.sidebar.markdown(
    "选择一个实验，并调整实验参数。"
)

st.sidebar.markdown("---")


experiment = st.sidebar.selectbox(
    "选择实验",
    experiment_list
)


# ============================================================
# 7. 实验说明
# ============================================================

experiment_description = {

    "🪙 抛硬币":
        "观察正面出现的累计频率是否逐渐接近理论概率。",

    "🎲 掷骰子":
        "观察骰子的样本平均值是否逐渐接近理论期望。",

    "🏀 篮球罚球":
        "模拟大量罚球，观察累计命中率的稳定过程。",

    "🎯 射击命中":
        "模拟射击实验，观察命中率如何逐渐稳定。",

    "🎁 抽奖箱":
        "观察多个奖项的累计频率是否逐渐接近设定概率。",

    "👥 随机抽样":
        "观察样本比例在重复抽样中的稳定趋势。",

    "🏭 产品质量检测":
        "模拟产品抽检，观察次品率估计如何逐渐稳定。",

    "🚕 随机等待时间":
        "模拟随机等待时间，观察平均等待时间逐渐接近理论值。"

}


st.sidebar.info(
    experiment_description[experiment]
)


# ============================================================
# 8. 参数初始化
# ============================================================

p = 0.5

n = 1000

sides = 6

p1 = 0.10
p2 = 0.20

population_p = 0.60

sample_size = 50

defect_rate = 0.05

mean_waiting = 10.0


# ============================================================
# 9. 不同实验的参数
# ============================================================

st.sidebar.subheader("⚙️ 实验参数")


# ------------------------------------------------------------
# 抛硬币
# ------------------------------------------------------------

if experiment == "🪙 抛硬币":

    p = st.sidebar.slider(
        "正面概率 p",
        min_value=0.05,
        max_value=0.95,
        value=0.50,
        step=0.05
    )

    n = st.sidebar.slider(
        "投掷次数 N",
        min_value=10,
        max_value=50000,
        value=1000,
        step=10
    )


# ------------------------------------------------------------
# 掷骰子
# ------------------------------------------------------------

elif experiment == "🎲 掷骰子":

    sides = st.sidebar.selectbox(
        "骰子面数",
        [4, 6, 8, 10, 12, 20],
        index=1
    )

    n = st.sidebar.slider(
        "投掷次数 N",
        min_value=10,
        max_value=50000,
        value=1000,
        step=10
    )


# ------------------------------------------------------------
# 篮球罚球
# ------------------------------------------------------------

elif experiment == "🏀 篮球罚球":

    p = st.sidebar.slider(
        "真实命中率",
        min_value=0.10,
        max_value=0.95,
        value=0.70,
        step=0.05
    )

    n = st.sidebar.slider(
        "罚球次数 N",
        min_value=10,
        max_value=50000,
        value=1000,
        step=10
    )


# ------------------------------------------------------------
# 射击
# ------------------------------------------------------------

elif experiment == "🎯 射击命中":

    p = st.sidebar.slider(
        "真实命中率",
        min_value=0.05,
        max_value=0.95,
        value=0.65,
        step=0.05
    )

    n = st.sidebar.slider(
        "射击次数 N",
        min_value=10,
        max_value=50000,
        value=1000,
        step=10
    )


# ------------------------------------------------------------
# 抽奖
# ------------------------------------------------------------

elif experiment == "🎁 抽奖箱":

    p1 = st.sidebar.slider(
        "一等奖概率",
        min_value=0.05,
        max_value=0.50,
        value=0.10,
        step=0.05
    )

    p2 = st.sidebar.slider(
        "二等奖概率",
        min_value=0.05,
        max_value=0.50,
        value=0.20,
        step=0.05
    )

    p3 = 1 - p1 - p2

    st.sidebar.write(
        f"🥉 三等奖概率：{p3:.0%}"
    )

    if p3 < 0:

        st.sidebar.error(
            "概率之和不能超过 100%"
        )

    n = st.sidebar.slider(
        "抽奖次数 N",
        min_value=10,
        max_value=50000,
        value=1000,
        step=10
    )


# ------------------------------------------------------------
# 随机抽样
# ------------------------------------------------------------

elif experiment == "👥 随机抽样":

    population_p = st.sidebar.slider(
        "总体比例",
        min_value=0.10,
        max_value=0.90,
        value=0.60,
        step=0.05
    )

    sample_size = st.sidebar.slider(
        "每次抽取人数",
        min_value=10,
        max_value=1000,
        value=50,
        step=10
    )

    n = st.sidebar.slider(
        "重复抽样次数",
        min_value=10,
        max_value=10000,
        value=1000,
        step=10
    )


# ------------------------------------------------------------
# 产品质量检测
# ------------------------------------------------------------

elif experiment == "🏭 产品质量检测":

    defect_rate = st.sidebar.slider(
        "真实次品率",
        min_value=0.01,
        max_value=0.30,
        value=0.05,
        step=0.01
    )

    n = st.sidebar.slider(
        "检测产品数量 N",
        min_value=10,
        max_value=50000,
        value=1000,
        step=10
    )


# ------------------------------------------------------------
# 随机等待时间
# ------------------------------------------------------------

elif experiment == "🚕 随机等待时间":

    mean_waiting = st.sidebar.slider(
        "理论平均等待时间（分钟）",
        min_value=1.0,
        max_value=60.0,
        value=10.0,
        step=1.0
    )

    n = st.sidebar.slider(
        "观察次数 N",
        min_value=10,
        max_value=50000,
        value=1000,
        step=10
    )


# ============================================================
# 10. 操作按钮
# ============================================================

st.sidebar.markdown("---")

start_button = st.sidebar.button(
    "▶ 开始实验",
    type="primary",
    use_container_width=True
)

reset_button = st.sidebar.button(
    "🔄 清除实验结果",
    use_container_width=True
)


# ============================================================
# 11. 清除结果
# ============================================================

if reset_button:

    st.session_state.lln_result = None

    st.session_state.lln_experiment = None

    st.rerun()


# ============================================================
# 12. 开始实验
# ============================================================

if start_button:

    rng = np.random.default_rng()

    result = {}


    # ========================================================
    # 抛硬币
    # ========================================================

    if experiment == "🪙 抛硬币":

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

        result = {
            "type": "probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": p,
            "unit": "累计正面频率",
            "title": "正面累计频率"
        }


    # ========================================================
    # 掷骰子
    # ========================================================

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

        theoretical = (
            sides + 1
        ) / 2

        result = {
            "type": "mean",
            "data": data,
            "cumulative": cumulative,
            "theoretical": theoretical,
            "unit": "样本平均值",
            "title": "骰子样本平均值"
        }


    # ========================================================
    # 篮球
    # ========================================================

    elif experiment == "🏀 篮球罚球":

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

        result = {
            "type": "probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": p,
            "unit": "累计命中率",
            "title": "罚球累计命中率"
        }


    # ========================================================
    # 射击
    # ========================================================

    elif experiment == "🎯 射击命中":

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

        result = {
            "type": "probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": p,
            "unit": "累计命中率",
            "title": "射击累计命中率"
        }


    # ========================================================
    # 抽奖
    # ========================================================

    elif experiment == "🎁 抽奖箱":

        if p3 >= 0:

            data = rng.choice(
                [1, 2, 3],
                size=n,
                p=[p1, p2, p3]
            )

            x = np.arange(
                1,
                n + 1
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

            result = {
                "type": "lottery",
                "data": data,
                "f1": f1,
                "f2": f2,
                "f3": f3,
                "p1": p1,
                "p2": p2,
                "p3": p3
            }


    # ========================================================
    # 随机抽样
    # ========================================================

    elif experiment == "👥 随机抽样":

        successes = rng.binomial(
            sample_size,
            population_p,
            n
        )

        sample_ratios = (
            successes
            /
            sample_size
        )

        cumulative_mean = (
            np.cumsum(sample_ratios)
            /
            np.arange(1, n + 1)
        )

        result = {
            "type": "sampling",
            "sample_ratios": sample_ratios,
            "cumulative": cumulative_mean,
            "theoretical": population_p,
            "sample_size": sample_size
        }


    # ========================================================
    # 产品质量
    # ========================================================

    elif experiment == "🏭 产品质量检测":

        data = rng.binomial(
            1,
            defect_rate,
            n
        )

        cumulative = (
            np.cumsum(data)
            /
            np.arange(1, n + 1)
        )

        result = {
            "type": "probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": defect_rate,
            "unit": "累计次品率",
            "title": "产品累计次品率"
        }


    # ========================================================
    # 随机等待时间
    # ========================================================

    elif experiment == "🚕 随机等待时间":

        # 指数分布
        data = rng.exponential(
            scale=mean_waiting,
            size=n
        )

        cumulative = (
            np.cumsum(data)
            /
            np.arange(1, n + 1)
        )

        result = {
            "type": "mean",
            "data": data,
            "cumulative": cumulative,
            "theoretical": mean_waiting,
            "unit": "平均等待时间",
            "title": "平均等待时间变化"
        }


    st.session_state.lln_result = result

    st.session_state.lln_experiment = experiment


# ============================================================
# 13. 主区域
# ============================================================

st.subheader("📈 实验结果")


result = st.session_state.lln_result


# ============================================================
# 14. 尚未开始
# ============================================================

if result is None:

    st.info(
        """
        👈 请先在左侧选择实验并调整参数。

        然后点击 **「▶ 开始实验」**。

        建议你尝试：

        **先进行较少次数的实验，再逐渐增加实验次数。**

        仔细观察实验结果是否越来越稳定。
        """
    )

    st.subheader("🔍 建议观察的问题")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### ① 实验次数较少时

            随机结果是否非常不稳定？

            每一次实验的结果是不是都有明显波动？
            """
        )

    with col2:

        st.markdown(
            """
            ### ② 实验次数增加以后

            曲线是否逐渐稳定？

            实验结果是否开始接近一个固定的理论值？
            """
        )


# ============================================================
# 15. 概率型实验
# ============================================================

elif result["type"] == "probability":

    data = result["data"]

    cumulative = result["cumulative"]

    theoretical = result["theoretical"]

    final_value = cumulative[-1]

    error = abs(
        final_value - theoretical
    )


    # --------------------------------------------------------
    # 指标
    # --------------------------------------------------------

    st.subheader("📊 模拟结果统计")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "实验次数 N",
            f"{len(data):,}"
        )

    with c2:

        st.metric(
            "理论值",
            f"{theoretical:.4f}"
        )

    with c3:

        st.metric(
            "最终实验值",
            f"{final_value:.4f}"
        )

    with c4:

        st.metric(
            "绝对误差",
            f"{error:.4f}"
        )


    # --------------------------------------------------------
    # 图像
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    x = np.arange(
        1,
        len(data) + 1
    )

    ax.plot(
        x,
        cumulative,
        color="#2E86AB",
        linewidth=1.8,
        label="累计实验值"
    )

    ax.axhline(
        theoretical,
        color="#E74C3C",
        linestyle="--",
        linewidth=2.2,
        label=f"理论值 = {theoretical:.4f}"
    )

    ax.set_title(
        f"{experiment}：{result['unit']}随实验次数的变化",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "实验次数 N",
        fontsize=12
    )

    ax.set_ylabel(
        result["unit"],
        fontsize=12
    )

    ax.grid(
        alpha=0.3
    )

    ax.legend(
        fontsize=11
    )

    fig.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


    # --------------------------------------------------------
    # 教学解释
    # --------------------------------------------------------

    st.info(
        f"""
        💡 **实验观察**

        本次实验进行了 **{len(data):,} 次**。

        理论值为 **{theoretical:.4f}**，
        最终实验值为 **{final_value:.4f}**。

        当前绝对误差为 **{error:.4f}**。

        可以尝试把实验次数继续增加，
        观察实验值是否越来越接近理论值。

        **这正是大数定律所描述的稳定现象。**
        """
    )


# ============================================================
# 16. 样本平均值实验
# ============================================================

elif result["type"] == "mean":

    data = result["data"]

    cumulative = result["cumulative"]

    theoretical = result["theoretical"]

    final_value = cumulative[-1]

    error = abs(
        final_value - theoretical
    )


    # --------------------------------------------------------
    # 指标
    # --------------------------------------------------------

    st.subheader("📊 模拟结果统计")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "实验次数 N",
            f"{len(data):,}"
        )

    with c2:

        st.metric(
            "理论期望",
            f"{theoretical:.4f}"
        )

    with c3:

        st.metric(
            "最终样本平均",
            f"{final_value:.4f}"
        )

    with c4:

        st.metric(
            "绝对误差",
            f"{error:.4f}"
        )


    # --------------------------------------------------------
    # 图表
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    x = np.arange(
        1,
        len(data) + 1
    )

    ax.plot(
        x,
        cumulative,
        color="#2E86AB",
        linewidth=1.8,
        label="累计平均值"
    )

    ax.axhline(
        theoretical,
        color="#E74C3C",
        linestyle="--",
        linewidth=2.2,
        label=f"理论期望 = {theoretical:.4f}"
    )

    ax.set_title(
        f"{experiment}：样本平均值的稳定过程",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "实验次数 N",
        fontsize=12
    )

    ax.set_ylabel(
        "样本平均值",
        fontsize=12
    )

    ax.grid(
        alpha=0.3
    )

    ax.legend(
        fontsize=11
    )

    fig.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


    # --------------------------------------------------------
    # 观察
    # --------------------------------------------------------

    st.info(
        f"""
        💡 **实验观察**

        理论期望为 **{theoretical:.4f}**。

        当实验次数较少时，
        样本平均值可能产生较大波动。

        随着实验次数不断增加，
        样本平均值逐渐稳定在理论期望附近。

        当前实验平均值为 **{final_value:.4f}**，
        与理论期望相差 **{error:.4f}**。

        **这说明大数定律不仅可以表现为“频率趋近概率”，
        也可以表现为“样本平均趋近数学期望”。**
        """
    )


# ============================================================
# 17. 抽奖实验
# ============================================================

elif result["type"] == "lottery":

    data = result["data"]

    f1 = result["f1"]

    f2 = result["f2"]

    f3 = result["f3"]


    # --------------------------------------------------------
    # 指标
    # --------------------------------------------------------

    st.subheader("📊 各奖项最终频率")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "一等奖",
            f"{f1[-1]:.2%}",
            f"理论 {result['p1']:.2%}"
        )

    with c2:

        st.metric(
            "二等奖",
            f"{f2[-1]:.2%}",
            f"理论 {result['p2']:.2%}"
        )

    with c3:

        st.metric(
            "三等奖",
            f"{f3[-1]:.2%}",
            f"理论 {result['p3']:.2%}"
        )


    # --------------------------------------------------------
    # 图表
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    x = np.arange(
        1,
        len(data) + 1
    )

    ax.plot(
        x,
        f1,
        linewidth=1.8,
        label="一等奖累计频率"
    )

    ax.plot(
        x,
        f2,
        linewidth=1.8,
        label="二等奖累计频率"
    )

    ax.plot(
        x,
        f3,
        linewidth=1.8,
        label="三等奖累计频率"
    )

    ax.axhline(
        result["p1"],
        linestyle="--",
        alpha=0.6
    )

    ax.axhline(
        result["p2"],
        linestyle="--",
        alpha=0.6
    )

    ax.axhline(
        result["p3"],
        linestyle="--",
        alpha=0.6
    )

    ax.set_title(
        "抽奖实验：各奖项累计频率的变化",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "抽奖次数 N",
        fontsize=12
    )

    ax.set_ylabel(
        "累计频率",
        fontsize=12
    )

    ax.grid(
        alpha=0.3
    )

    ax.legend(
        fontsize=11
    )

    fig.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


    st.info(
        """
        💡 **实验观察**

        注意观察三条曲线：

        当抽奖次数较少时，
        各奖项的实际频率可能与理论概率差异很大。

        随着抽奖次数不断增加，
        各奖项的累计频率逐渐稳定，
        并分别接近各自的理论概率。

        **多个随机事件也可以同时体现大数定律。**
        """
    )


# ============================================================
# 18. 随机抽样实验
# ============================================================

elif result["type"] == "sampling":

    sample_ratios = result[
        "sample_ratios"
    ]

    cumulative = result[
        "cumulative"
    ]

    theoretical = result[
        "theoretical"
    ]

    final_value = cumulative[-1]

    error = abs(
        final_value - theoretical
    )


    # --------------------------------------------------------
    # 指标
    # --------------------------------------------------------

    st.subheader("📊 模拟结果统计")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "每次抽样人数",
            result["sample_size"]
        )

    with c2:

        st.metric(
            "总体比例",
            f"{theoretical:.2%}"
        )

    with c3:

        st.metric(
            "最终累计平均",
            f"{final_value:.2%}"
        )

    with c4:

        st.metric(
            "绝对误差",
            f"{error:.2%}"
        )


    # --------------------------------------------------------
    # 图表
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    x = np.arange(
        1,
        len(cumulative) + 1
    )

    ax.plot(
        x,
        cumulative,
        color="#2E86AB",
        linewidth=1.8,
        label="样本比例累计平均"
    )

    ax.axhline(
        theoretical,
        color="#E74C3C",
        linestyle="--",
        linewidth=2.2,
        label=f"总体比例 = {theoretical:.2%}"
    )

    ax.set_title(
        "随机抽样：样本比例逐渐稳定",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "重复抽样次数",
        fontsize=12
    )

    ax.set_ylabel(
        "比例",
        fontsize=12
    )

    ax.grid(
        alpha=0.3
    )

    ax.legend(
        fontsize=11
    )

    fig.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


    st.info(
        f"""
        💡 **实验观察**

        每次随机抽取 **{result['sample_size']} 人**。

        虽然每一次抽样得到的样本比例都可能不同，
        但大量重复抽样以后，
        样本比例的平均表现逐渐接近总体比例
        **{theoretical:.2%}**。

        可以尝试改变每次抽样人数，
        看看实验结果有什么不同。
        """
    )


# ============================================================
# 19. 页面底部教学说明
# ============================================================

st.markdown("---")

st.subheader("📝 实验使用说明")

st.markdown(
    """
    **① 选择实验**

    在左侧下拉菜单中选择你感兴趣的随机实验。

    **② 调整参数**

    尝试改变概率、实验次数、样本大小等参数。

    **③ 开始实验**

    点击「▶ 开始实验」，观察实验结果。

    **④ 改变实验次数**

    建议先使用较小的实验次数，再逐渐增加实验次数。

    **⑤ 思考**

    当实验次数越来越大时，
    实验结果是否越来越稳定？
    是否逐渐接近某一个理论值？

    > **不要急着背诵大数定律。**
    >
    > 先观察随机实验中出现的规律，
    > 再思考为什么会出现这种规律。
    """
)
