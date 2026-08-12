import matplotlib
matplotlib.use("agg")

import os
import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import requests


# ============================================================
# 1. 页面基础配置
# ============================================================

st.set_page_config(
    page_title="大数定理交互式实验室",
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
    如果不存在，则尝试下载。
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

    if "font_setup_done" not in st.session_state:
        st.session_state.font_setup_done = False

    if st.session_state.font_setup_done:
        return

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

            plt.rcParams["axes.unicode_minus"] = False

            st.session_state.font_setup_done = True

            return

    try:

        fm.fontManager.addfont(
            font_path
        )

        font_prop = fm.FontProperties(
            fname=font_path
        )

        font_name = font_prop.get_name()

        plt.rcParams["font.family"] = font_name

        plt.rcParams["font.sans-serif"] = [
            font_name
        ]

        plt.rcParams["axes.unicode_minus"] = False

        st.session_state.font_setup_done = True

    except Exception:

        plt.rcParams["font.family"] = [
            "SimHei",
            "Microsoft YaHei",
            "WenQuanYi Zen Hei",
            "DejaVu Sans"
        ]

        plt.rcParams["axes.unicode_minus"] = False

        st.session_state.font_setup_done = True


setup_chinese_font()


# ============================================================
# 3. 自定义页面样式
# ============================================================

st.markdown(
    """
    <style>

    /* 页面顶部空间 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* 主标题 */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 16px;
        color: #666666;
        margin-bottom: 25px;
    }

    /* 实验标题 */
    .experiment-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    /* 小提示 */
    .experiment-desc {
        color: #666666;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* 指标卡片 */
    .metric-box {
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 14px 16px;
        background-color: rgba(248, 250, 252, 0.7);
        min-height: 95px;
    }

    .metric-label {
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 7px;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
    }

    .metric-note {
        font-size: 12px;
        color: #6B7280;
        margin-top: 5px;
    }

    /* 教学提示 */
    .teaching-box {
        padding: 16px;
        border-radius: 10px;
        background-color: #F5F9FF;
        border-left: 4px solid #2E86AB;
        margin-top: 12px;
        margin-bottom: 15px;
    }

    /* 实验室标签 */
    .lab-tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 15px;
        background-color: #EEF5FF;
        color: #2563EB;
        font-size: 13px;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. 页面标题
# ============================================================

st.markdown(
    '<div class="main-title">🎲 大数定理交互式实验室</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    '动手实验 · 观察随机 · 发现规律'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    大数定律告诉我们：当随机实验被大量重复进行时，
    <b>随机结果的长期平均表现会逐渐趋近于一个稳定的理论值。</b>
    <br><br>
    在这里，不需要先背公式。请选择一个实验、调整参数，
    然后亲眼观察随机性如何逐渐呈现出稳定规律。
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. Session State
# ============================================================

if "lln_result" not in st.session_state:
    st.session_state.lln_result = None

if "lln_experiment" not in st.session_state:
    st.session_state.lln_experiment = None

if "lln_history" not in st.session_state:
    st.session_state.lln_history = []

if "animation_running" not in st.session_state:
    st.session_state.animation_running = False


# ============================================================
# 6. 八个实验
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


experiment_description = {

    "🪙 抛硬币":
        "大量抛掷硬币，观察正面累计频率逐渐接近理论概率。",

    "🎲 掷骰子":
        "重复掷骰子，观察样本平均点数逐渐接近理论期望。",

    "🏀 篮球罚球":
        "模拟大量罚球，观察累计命中率如何逐渐稳定。",

    "🎯 射击命中":
        "模拟射击实验，观察长期命中率逐渐接近真实命中率。",

    "🎁 抽奖箱":
        "重复抽奖，观察多个奖项的累计频率分别趋近理论概率。",

    "👥 随机抽样":
        "重复进行随机抽样，观察样本比例的长期平均表现。",

    "🏭 产品质量检测":
        "模拟产品质量抽检，观察累计次品率逐渐接近真实次品率。",

    "🚕 随机等待时间":
        "模拟随机等待时间，观察平均等待时间逐渐接近理论平均值。"

}


# ============================================================
# 7. 侧边栏实验控制台
# ============================================================

st.sidebar.header("🔧 实验控制台")

experiment = st.sidebar.selectbox(
    "选择实验",
    experiment_list
)

st.sidebar.info(
    experiment_description[experiment]
)

st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ 实验参数")


# ============================================================
# 8. 参数初始化
# ============================================================

p = 0.5
n = 1000

sides = 6

p1 = 0.10
p2 = 0.20
p3 = 0.70

population_p = 0.60
sample_size = 50

defect_rate = 0.05

mean_waiting = 10.0


# ============================================================
# 9. 不同实验参数
# ============================================================

if experiment == "🪙 抛硬币":

    p = st.sidebar.slider(
        "正面概率 p",
        0.05,
        0.95,
        0.50,
        0.05
    )

    n = st.sidebar.slider(
        "实验次数 N",
        10,
        50000,
        1000,
        10
    )


elif experiment == "🎲 掷骰子":

    sides = st.sidebar.selectbox(
        "骰子面数",
        [4, 6, 8, 10, 12, 20],
        index=1
    )

    n = st.sidebar.slider(
        "实验次数 N",
        10,
        50000,
        1000,
        10
    )


elif experiment == "🏀 篮球罚球":

    p = st.sidebar.slider(
        "真实命中率",
        0.10,
        0.95,
        0.70,
        0.05
    )

    n = st.sidebar.slider(
        "罚球次数 N",
        10,
        50000,
        1000,
        10
    )


elif experiment == "🎯 射击命中":

    p = st.sidebar.slider(
        "真实命中率",
        0.05,
        0.95,
        0.65,
        0.05
    )

    n = st.sidebar.slider(
        "射击次数 N",
        10,
        50000,
        1000,
        10
    )


elif experiment == "🎁 抽奖箱":

    p1 = st.sidebar.slider(
        "一等奖概率",
        0.05,
        0.50,
        0.10,
        0.05
    )

    p2 = st.sidebar.slider(
        "二等奖概率",
        0.05,
        0.50,
        0.20,
        0.05
    )

    p3 = 1 - p1 - p2

    st.sidebar.write(
        f"🥉 三等奖概率：{p3:.1%}"
    )

    if p3 < 0:

        st.sidebar.error(
            "概率之和不能超过 100%"
        )

    n = st.sidebar.slider(
        "抽奖次数 N",
        10,
        50000,
        1000,
        10
    )


elif experiment == "👥 随机抽样":

    population_p = st.sidebar.slider(
        "总体比例",
        0.10,
        0.90,
        0.60,
        0.05
    )

    sample_size = st.sidebar.slider(
        "每次抽取人数",
        10,
        1000,
        50,
        10
    )

    n = st.sidebar.slider(
        "重复抽样次数",
        10,
        10000,
        1000,
        10
    )


elif experiment == "🏭 产品质量检测":

    defect_rate = st.sidebar.slider(
        "真实次品率",
        0.01,
        0.30,
        0.05,
        0.01
    )

    n = st.sidebar.slider(
        "检测产品数量",
        10,
        50000,
        1000,
        10
    )


elif experiment == "🚕 随机等待时间":

    mean_waiting = st.sidebar.slider(
        "理论平均等待时间（分钟）",
        1.0,
        60.0,
        10.0,
        1.0
    )

    n = st.sidebar.slider(
        "观察次数 N",
        10,
        50000,
        1000,
        10
    )


# ============================================================
# 10. 按钮
# ============================================================

st.sidebar.markdown("---")

start_button = st.sidebar.button(
    "▶ 开始实验",
    type="primary",
    use_container_width=True
)

animation_button = st.sidebar.button(
    "🎬 动态演示",
    use_container_width=True
)

reset_button = st.sidebar.button(
    "🔄 清除实验结果",
    use_container_width=True
)


# ============================================================
# 11. 生成实验数据函数
# ============================================================

def generate_experiment(
    experiment,
    n,
    p=0.5,
    sides=6,
    p1=0.1,
    p2=0.2,
    population_p=0.6,
    sample_size=50,
    defect_rate=0.05,
    mean_waiting=10.0
):

    rng = np.random.default_rng()

    x = np.arange(
        1,
        n + 1
    )


    # --------------------------------------------------------
    # 抛硬币
    # --------------------------------------------------------

    if experiment == "🪙 抛硬币":

        data = rng.binomial(
            1,
            p,
            n
        )

        cumulative = (
            np.cumsum(data)
            / x
        )

        return {
            "kind": "mean_or_probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": p,
            "label": "累计正面频率",
            "unit": "",
            "theory_name": "理论概率"
        }


    # --------------------------------------------------------
    # 掷骰子
    # --------------------------------------------------------

    elif experiment == "🎲 掷骰子":

        data = rng.integers(
            1,
            sides + 1,
            n
        )

        cumulative = (
            np.cumsum(data)
            / x
        )

        theoretical = (
            sides + 1
        ) / 2

        return {
            "kind": "mean_or_probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": theoretical,
            "label": "累计平均点数",
            "unit": "",
            "theory_name": "理论期望"
        }


    # --------------------------------------------------------
    # 篮球
    # --------------------------------------------------------

    elif experiment == "🏀 篮球罚球":

        data = rng.binomial(
            1,
            p,
            n
        )

        cumulative = (
            np.cumsum(data)
            / x
        )

        return {
            "kind": "mean_or_probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": p,
            "label": "累计命中率",
            "unit": "",
            "theory_name": "理论命中率"
        }


    # --------------------------------------------------------
    # 射击
    # --------------------------------------------------------

    elif experiment == "🎯 射击命中":

        data = rng.binomial(
            1,
            p,
            n
        )

        cumulative = (
            np.cumsum(data)
            / x
        )

        return {
            "kind": "mean_or_probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": p,
            "label": "累计命中率",
            "unit": "",
            "theory_name": "理论命中率"
        }


    # --------------------------------------------------------
    # 抽奖
    # --------------------------------------------------------

    elif experiment == "🎁 抽奖箱":

        p3 = 1 - p1 - p2

        if p3 < 0:

            return None

        data = rng.choice(
            [1, 2, 3],
            size=n,
            p=[p1, p2, p3]
        )

        f1 = (
            np.cumsum(data == 1)
            / x
        )

        f2 = (
            np.cumsum(data == 2)
            / x
        )

        f3 = (
            np.cumsum(data == 3)
            / x
        )

        return {
            "kind": "lottery",
            "data": data,
            "f1": f1,
            "f2": f2,
            "f3": f3,
            "p1": p1,
            "p2": p2,
            "p3": p3
        }


    # --------------------------------------------------------
    # 随机抽样
    # --------------------------------------------------------

    elif experiment == "👥 随机抽样":

        successes = rng.binomial(
            sample_size,
            population_p,
            n
        )

        sample_ratios = (
            successes
            / sample_size
        )

        cumulative = (
            np.cumsum(sample_ratios)
            / x
        )

        return {
            "kind": "sampling",
            "data": sample_ratios,
            "cumulative": cumulative,
            "theoretical": population_p,
            "sample_size": sample_size
        }


    # --------------------------------------------------------
    # 产品质量
    # --------------------------------------------------------

    elif experiment == "🏭 产品质量检测":

        data = rng.binomial(
            1,
            defect_rate,
            n
        )

        cumulative = (
            np.cumsum(data)
            / x
        )

        return {
            "kind": "mean_or_probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": defect_rate,
            "label": "累计次品率",
            "unit": "",
            "theory_name": "理论次品率"
        }


    # --------------------------------------------------------
    # 等待时间
    # --------------------------------------------------------

    elif experiment == "🚕 随机等待时间":

        data = rng.exponential(
            scale=mean_waiting,
            size=n
        )

        cumulative = (
            np.cumsum(data)
            / x
        )

        return {
            "kind": "mean_or_probability",
            "data": data,
            "cumulative": cumulative,
            "theoretical": mean_waiting,
            "label": "累计平均等待时间",
            "unit": "分钟",
            "theory_name": "理论平均等待时间"
        }


    return None


# ============================================================
# 12. 开始普通实验
# ============================================================

if start_button:

    result = generate_experiment(
        experiment,
        n,
        p=p,
        sides=sides,
        p1=p1,
        p2=p2,
        population_p=population_p,
        sample_size=sample_size,
        defect_rate=defect_rate,
        mean_waiting=mean_waiting
    )

    if result is not None:

        st.session_state.lln_result = result

        st.session_state.lln_experiment = experiment

        final_value = (
            result["cumulative"][-1]
            if "cumulative" in result
            else None
        )

        if final_value is not None:

            theoretical = result["theoretical"]

            error = abs(
                final_value - theoretical
            )

            st.session_state.lln_history.append(
                {
                    "实验": experiment,
                    "实验次数": n,
                    "理论值": theoretical,
                    "最终结果": final_value,
                    "绝对误差": error
                }
            )


# ============================================================
# 13. 清除结果
# ============================================================

if reset_button:

    st.session_state.lln_result = None

    st.session_state.lln_experiment = None

    st.session_state.lln_history = []

    st.session_state.animation_running = False

    st.rerun()


# ============================================================
# 14. 主区域
# ============================================================

result = st.session_state.lln_result


if result is None:

    st.markdown(
        '<div class="lab-tag">🧪 实验室准备就绪</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="experiment-title">'
        '请选择一个实验开始探索'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="experiment-desc">'
        '左侧可以选择实验类型并自由调整参数。'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 🔍 你可以观察什么？

            - 实验次数少的时候，结果是否很随机？
            - 实验次数增加以后，结果是否逐渐稳定？
            - 最终结果是否接近理论值？
            - 误差是否总体变小？
            """
        )

    with col2:

        st.markdown(
            """
            ### 💡 建议实验方法

            **先小后大。**

            先把实验次数设置得比较小，
            观察随机波动。

            然后逐渐增加实验次数，
            看看规律是怎样出现的。
            """
        )

    st.info(
        "👈 请从左侧选择一个实验，然后点击「▶ 开始实验」。"
    )


# ============================================================
# 15. 普通实验结果
# ============================================================

elif result["kind"] in [
    "mean_or_probability",
    "sampling"
]:

    cumulative = result["cumulative"]

    theoretical = result["theoretical"]

    final_value = cumulative[-1]

    error = abs(
        final_value - theoretical
    )

    total_n = len(cumulative)


    # --------------------------------------------------------
    # 标题
    # --------------------------------------------------------

    st.markdown(
        '<div class="lab-tag">🧪 当前实验</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="experiment-title">{experiment}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="experiment-desc">'
        f'{experiment_description[experiment]}'
        f'</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 核心指标
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">
                    实验次数
                </div>
                <div class="metric-value">
                    {total_n:,}
                </div>
                <div class="metric-note">
                    当前模拟规模
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">
                    {result["theory_name"]}
                </div>
                <div class="metric-value">
                    {theoretical:.4f}
                </div>
                <div class="metric-note">
                    理论稳定值
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">
                    当前实验值
                </div>
                <div class="metric-value">
                    {final_value:.4f}
                </div>
                <div class="metric-note">
                    最终累计结果
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">
                    当前绝对误差
                </div>
                <div class="metric-value">
                    {error:.4f}
                </div>
                <div class="metric-note">
                    |实验值 − 理论值|
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("")


    # ========================================================
    # 收敛曲线
    # ========================================================

    st.subheader("📈 大数定律：结果如何逐渐稳定？")

    fig, ax = plt.subplots(
        figsize=(12, 5.5)
    )

    x = np.arange(
        1,
        total_n + 1
    )

    ax.plot(
        x,
        cumulative,
        linewidth=1.8,
        color="#2E86AB",
        label="累计实验值"
    )

    ax.axhline(
        theoretical,
        color="#E74C3C",
        linestyle="--",
        linewidth=2,
        label=f"理论值 = {theoretical:.4f}"
    )

    ax.set_xlabel(
        "实验次数 N",
        fontsize=12
    )

    ax.set_ylabel(
        result["label"],
        fontsize=12
    )

    ax.set_title(
        "随机结果的长期平均逐渐趋近理论值",
        fontsize=16,
        fontweight="bold"
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


    # ========================================================
    # 误差曲线
    # ========================================================

    st.subheader("📉 实验误差的变化")

    errors = np.abs(
        cumulative - theoretical
    )

    fig2, ax2 = plt.subplots(
        figsize=(12, 4)
    )

    ax2.plot(
        x,
        errors,
        linewidth=1.5,
        color="#8E44AD"
    )

    ax2.axhline(
        0,
        color="#555555",
        linewidth=1
    )

    ax2.set_xlabel(
        "实验次数 N",
        fontsize=12
    )

    ax2.set_ylabel(
        "绝对误差",
        fontsize=12
    )

    ax2.set_title(
        "实验值与理论值之间的误差",
        fontsize=15,
        fontweight="bold"
    )

    ax2.grid(
        alpha=0.3
    )

    fig2.tight_layout()

    st.pyplot(
        fig2,
        use_container_width=True
    )

    plt.close(fig2)


    # ========================================================
    # 最近实验表现
    # ========================================================

    st.subheader("🔎 最近实验表现")

    recent_sizes = [
        10,
        50,
        100,
        500
    ]

    recent_sizes = [
        size
        for size in recent_sizes
        if size <= total_n
    ]

    cols = st.columns(
        len(recent_sizes)
    )

    for col, size in zip(
        cols,
        recent_sizes
    ):

        value = cumulative[size - 1]

        recent_error = abs(
            value - theoretical
        )

        with col:

            st.metric(
                f"N = {size}",
                f"{value:.4f}",
                f"误差 {recent_error:.4f}"
            )


    # ========================================================
    # 教学解释
    # ========================================================

    st.markdown(
        f"""
        <div class="teaching-box">

        <b>💡 实验观察</b>

        <br><br>

        当前实验进行了 <b>{total_n:,}</b> 次。

        理论值为 <b>{theoretical:.4f}</b>，
        最终实验值为 <b>{final_value:.4f}</b>。

        当前绝对误差为 <b>{error:.4f}</b>。

        <br><br>

        请注意：误差曲线并不会严格地一直下降。

        在随机实验中，误差仍然会不断上下波动，
        但随着实验次数越来越大，
        实验结果总体上会越来越接近理论值。

        <br><br>

        <b>
        这就是我们通过实验观察到的大数定律。
        </b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 16. 抽奖实验
# ============================================================

elif result["kind"] == "lottery":

    data = result["data"]

    f1 = result["f1"]
    f2 = result["f2"]
    f3 = result["f3"]

    total_n = len(data)


    # --------------------------------------------------------
    # 指标
    # --------------------------------------------------------

    st.subheader("🎁 抽奖实验结果")

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
    # 动态累计频率
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 5.5)
    )

    x = np.arange(
        1,
        total_n + 1
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
        alpha=0.5
    )

    ax.axhline(
        result["p2"],
        linestyle="--",
        alpha=0.5
    )

    ax.axhline(
        result["p3"],
        linestyle="--",
        alpha=0.5
    )

    ax.set_xlabel(
        "抽奖次数 N"
    )

    ax.set_ylabel(
        "累计频率"
    )

    ax.set_title(
        "多个随机事件同时体现大数定律",
        fontsize=16,
        fontweight="bold"
    )

    ax.grid(
        alpha=0.3
    )

    ax.legend()

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
        """
        💡 **观察重点**

        抽奖次数较少时，每个奖项的实际频率都可能出现明显偏差。

        随着抽奖次数不断增加，
        一等奖、二等奖、三等奖的累计频率
        会分别逐渐接近各自的理论概率。

        注意：

        **大数定律并不是只对某一个事件成立，
        而可以同时体现在多个随机事件上。**
        """
    )


# ============================================================
# 17. 动态演示
# ============================================================

if animation_button:

    st.session_state.animation_running = True

    st.markdown("---")

    st.subheader("🎬 动态实验演示")

    st.write(
        "观察实验结果如何随着实验次数增加而逐渐稳定。"
    )

    chart_placeholder = st.empty()

    metric_placeholder = st.empty()

    progress_placeholder = st.empty()

    info_placeholder = st.empty()


    # 动态演示最大次数
    animation_max = min(
        n,
        5000
    )

    # 生成完整数据
    animation_result = generate_experiment(
        experiment,
        animation_max,
        p=p,
        sides=sides,
        p1=p1,
        p2=p2,
        population_p=population_p,
        sample_size=sample_size,
        defect_rate=defect_rate,
        mean_waiting=mean_waiting
    )

    if animation_result is not None:

        # 每一帧增加多少
        step = max(
            10,
            animation_max // 80
        )

        for current_n in range(
            step,
            animation_max + 1,
            step
        ):

            if not st.session_state.animation_running:
                break

            # ------------------------------------------------
            # 普通实验动画
            # ------------------------------------------------

            if animation_result["kind"] in [
                "mean_or_probability",
                "sampling"
            ]:

                cumulative = animation_result[
                    "cumulative"
                ][:current_n]

                theoretical = animation_result[
                    "theoretical"
                ]

                current_value = cumulative[-1]

                current_error = abs(
                    current_value
                    - theoretical
                )

                x = np.arange(
                    1,
                    current_n + 1
                )

                fig, ax = plt.subplots(
                    figsize=(12, 5.5)
                )

                ax.plot(
                    x,
                    cumulative,
                    linewidth=2,
                    color="#2E86AB",
                    label="累计实验值"
                )

                ax.axhline(
                    theoretical,
                    color="#E74C3C",
                    linestyle="--",
                    linewidth=2,
                    label=f"理论值 = {theoretical:.4f}"
                )

                ax.set_xlim(
                    1,
                    animation_max
                )

                ax.set_xlabel(
                    "实验次数 N"
                )

                ax.set_ylabel(
                    animation_result["label"]
                )

                ax.set_title(
                    f"动态实验：N = {current_n:,}",
                    fontsize=16,
                    fontweight="bold"
                )

                ax.grid(
                    alpha=0.3
                )

                ax.legend()

                fig.tight_layout()

                with chart_placeholder.container():

                    st.pyplot(
                        fig,
                        use_container_width=True
                    )

                plt.close(fig)


                # --------------------------------------------
                # 实时指标
                # --------------------------------------------

                with metric_placeholder.container():

                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric(
                        "实验次数",
                        f"{current_n:,}"
                    )

                    c2.metric(
                        "理论值",
                        f"{theoretical:.4f}"
                    )

                    c3.metric(
                        "当前实验值",
                        f"{current_value:.4f}"
                    )

                    c4.metric(
                        "当前误差",
                        f"{current_error:.4f}"
                    )


                # --------------------------------------------
                # 进度
                # --------------------------------------------

                progress_placeholder.progress(
                    current_n / animation_max,
                    text=(
                        f"实验进度："
                        f"{current_n:,} / "
                        f"{animation_max:,}"
                    )
                )


                # --------------------------------------------
                # 教学提示
                # --------------------------------------------

                if current_n < animation_max * 0.2:

                    message = (
                        "🔵 实验刚刚开始："
                        "随机波动通常比较明显。"
                    )

                elif current_n < animation_max * 0.6:

                    message = (
                        "🟡 实验正在进行："
                        "累计结果开始逐渐稳定。"
                    )

                else:

                    message = (
                        "🟢 实验次数已经较多："
                        "观察累计结果是否逐渐接近理论值。"
                    )

                info_placeholder.info(
                    message
                )


                time.sleep(
                    0.08
                )


        st.session_state.animation_running = False

        progress_placeholder.progress(
            1.0,
            text="🎉 动态实验完成"
        )


# ============================================================
# 18. 停止动画
# ============================================================

if st.session_state.animation_running:

    if st.sidebar.button(
        "⏹ 停止动态演示",
        use_container_width=True
    ):

        st.session_state.animation_running = False

        st.rerun()


# ============================================================
# 19. 实验记录
# ============================================================

if len(st.session_state.lln_history) > 0:

    st.markdown("---")

    st.subheader("📋 我的实验记录")

    history = st.session_state.lln_history

    for i, record in enumerate(
        history[-10:],
        start=1
    ):

        cols = st.columns(5)

        cols[0].write(
            record["实验"]
        )

        cols[1].write(
            f"N = {record['实验次数']:,}"
        )

        cols[2].write(
            f"理论值：{record['理论值']:.4f}"
        )

        cols[3].write(
            f"实验值：{record['最终结果']:.4f}"
        )

        cols[4].write(
            f"误差：{record['绝对误差']:.4f}"
        )


# ============================================================
# 20. 底部教学说明
# ============================================================

st.markdown("---")

st.subheader("📝 实验室使用指南")

st.markdown(
    """
    ### 第一步：选择一个随机实验

    左侧下拉菜单提供 8 种不同的随机实验。

    ### 第二步：调整参数

    尝试改变概率、骰子类型、样本大小、
    实验次数等参数。

    ### 第三步：先做小规模实验

    建议先从较小的实验次数开始，
    观察随机结果的波动。

    ### 第四步：逐渐增加实验次数

    点击「▶ 开始实验」或者「🎬 动态演示」，
    观察实验结果是否越来越稳定。

    ### 第五步：观察误差

    不要只看最终结果。

    请重点观察：

    \[
    |实验值 - 理论值|
    \]

    是否随着实验次数增加而总体趋近于 0。

    ---

    ### 💡 最重要的思考

    **大数定律并不是说随机性消失了。**

    每一次实验仍然具有随机性。

    真正发生变化的是：

    > 当实验次数越来越多时，
    > 随机结果的长期平均表现越来越稳定，
    > 并逐渐接近理论值。

    **这就是你在这个实验室中需要亲眼发现的规律。**
    """
)
