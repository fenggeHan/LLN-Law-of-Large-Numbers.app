import matplotlib
matplotlib.use("agg")

import time
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm
import requests


# ============================================================
# 页面基础配置
# ============================================================

st.set_page_config(
    page_title="大数定理（LLN）交互式实验室",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 中文字体配置
# ============================================================

def setup_chinese_font():
    """统一配置中文字体，优先加载项目中的字体，无则自动下载"""

    font_url = (
        "https://github.com/fenggeHan/"
        "CLT-Interactive-Simulation-Teaching-Platform/"
        "raw/main/simhei.ttf"
    )

    current_dir = (
        os.path.dirname(os.path.abspath(__file__))
        if "__file__" in locals()
        else os.getcwd()
    )

    font_dir = os.path.join(current_dir, "fonts")
    font_path = os.path.join(font_dir, "simhei.ttf")

    if not os.path.exists(font_path):
        os.makedirs(font_dir, exist_ok=True)

        try:
            response = requests.get(font_url, timeout=15)
            response.raise_for_status()

            with open(font_path, "wb") as f:
                f.write(response.content)

        except Exception:
            plt.rcParams["font.family"] = [
                "SimHei",
                "Microsoft YaHei",
                "WenQuanYi Zen Hei",
                "DejaVu Sans"
            ]
            plt.rcParams["axes.unicode_minus"] = False
            return

    try:
        fm.fontManager.addfont(font_path)

        font_prop = fm.FontProperties(fname=font_path)
        font_name = font_prop.get_name()

        plt.rcParams["font.family"] = font_name
        plt.rcParams["font.sans-serif"] = [font_name]
        plt.rcParams["axes.unicode_minus"] = False

    except Exception:
        plt.rcParams["font.family"] = [
            "SimHei",
            "Microsoft YaHei",
            "WenQuanYi Zen Hei",
            "DejaVu Sans"
        ]
        plt.rcParams["axes.unicode_minus"] = False


setup_chinese_font()


# ============================================================
# 页面 CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .main-description {
        font-size: 15px;
        color: #666666;
        margin-bottom: 18px;
    }

    .experiment-title {
        font-size: 25px;
        font-weight: 650;
        margin-bottom: 4px;
    }

    .experiment-description {
        font-size: 14px;
        color: #666666;
        margin-bottom: 12px;
    }

    .guide-text {
        font-size: 12px;
        color: #777777;
        line-height: 1.65;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.06);
        border-radius: 8px;
        padding: 10px 12px;
    }

    .stButton > button {
        border-radius: 7px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 页面标题
# ============================================================

st.markdown(
    '<div class="main-title">🎲 大数定理（LLN）交互式实验室</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-description">'
    '通过重复随机实验，观察实验结果如何随着次数增加逐渐趋于稳定。'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 8 个实验
# ============================================================

experiments = [
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
# 侧边栏：实验控制台
# ============================================================

st.sidebar.header("🔧 实验控制台")

experiment = st.sidebar.selectbox(
    "选择实验",
    experiments
)


# ============================================================
# 参数初始化
# ============================================================

N = 5000


# ============================================================
# 实验一：抛硬币
# ============================================================

if experiment == "🪙 抛硬币":

    st.sidebar.subheader("实验参数")

    p = st.sidebar.slider(
        "正面概率 p",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05
    )

    N = st.sidebar.slider(
        "模拟次数 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = p

    experiment_description = (
        "重复抛掷硬币，观察正面出现的累计频率逐渐接近理论概率。"
    )

    y_label = "正面累计频率"

    def generate_data(n):
        return np.random.binomial(1, p, n)


# ============================================================
# 实验二：掷骰子
# ============================================================

elif experiment == "🎲 掷骰子":

    st.sidebar.subheader("实验参数")

    sides = st.sidebar.slider(
        "骰子面数",
        min_value=4,
        max_value=20,
        value=6,
        step=1
    )

    N = st.sidebar.slider(
        "模拟次数 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = (sides + 1) / 2

    experiment_description = (
        "重复掷骰子，观察累计平均点数逐渐接近理论期望。"
    )

    y_label = "累计平均点数"

    def generate_data(n):
        return np.random.randint(
            1,
            sides + 1,
            n
        )


# ============================================================
# 实验三：篮球罚球
# ============================================================

elif experiment == "🏀 篮球罚球":

    st.sidebar.subheader("实验参数")

    p = st.sidebar.slider(
        "单次罚球命中概率",
        min_value=0.1,
        max_value=0.9,
        value=0.6,
        step=0.05
    )

    N = st.sidebar.slider(
        "罚球次数 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = p

    experiment_description = (
        "模拟连续罚球，观察长期命中率逐渐接近理论命中概率。"
    )

    y_label = "累计命中率"

    def generate_data(n):
        return np.random.binomial(
            1,
            p,
            n
        )


# ============================================================
# 实验四：射击命中
# ============================================================

elif experiment == "🎯 射击命中":

    st.sidebar.subheader("实验参数")

    p = st.sidebar.slider(
        "单次命中概率",
        min_value=0.1,
        max_value=0.95,
        value=0.7,
        step=0.05
    )

    N = st.sidebar.slider(
        "射击次数 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = p

    experiment_description = (
        "模拟连续射击，观察大量试验后实际命中率的稳定趋势。"
    )

    y_label = "累计命中率"

    def generate_data(n):
        return np.random.binomial(
            1,
            p,
            n
        )


# ============================================================
# 实验五：抽奖箱
# ============================================================

elif experiment == "🎁 抽奖箱":

    st.sidebar.subheader("实验参数")

    win_probability = st.sidebar.slider(
        "中奖概率",
        min_value=0.05,
        max_value=0.8,
        value=0.2,
        step=0.05
    )

    prize_value = st.sidebar.slider(
        "中奖奖金",
        min_value=10,
        max_value=1000,
        value=100,
        step=10
    )

    N = st.sidebar.slider(
        "抽奖次数 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = (
        win_probability * prize_value
    )

    experiment_description = (
        "重复进行抽奖，观察长期平均收益逐渐接近理论平均收益。"
    )

    y_label = "累计平均收益"

    def generate_data(n):

        win = np.random.binomial(
            1,
            win_probability,
            n
        )

        return win * prize_value


# ============================================================
# 实验六：随机抽样
# ============================================================

elif experiment == "👥 随机抽样":

    st.sidebar.subheader("总体参数")

    population_mean = st.sidebar.slider(
        "总体平均值",
        min_value=10.0,
        max_value=100.0,
        value=50.0,
        step=5.0
    )

    population_std = st.sidebar.slider(
        "总体标准差",
        min_value=1.0,
        max_value=30.0,
        value=10.0,
        step=1.0
    )

    sample_size = st.sidebar.slider(
        "每次抽取人数",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )

    N = st.sidebar.slider(
        "抽样次数 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = population_mean

    experiment_description = (
        "从随机总体中不断抽样，观察长期样本平均值逐渐稳定。"
    )

    y_label = "累计样本平均值"

    def generate_data(n):

        data = np.random.normal(
            population_mean,
            population_std,
            size=(n, sample_size)
        )

        return np.mean(
            data,
            axis=1
        )


# ============================================================
# 实验七：产品质量检测
# ============================================================

elif experiment == "🏭 产品质量检测":

    st.sidebar.subheader("生产参数")

    defect_rate = st.sidebar.slider(
        "理论次品率",
        min_value=0.01,
        max_value=0.3,
        value=0.05,
        step=0.01
    )

    N = st.sidebar.slider(
        "检测产品数量 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = defect_rate

    experiment_description = (
        "模拟产品质量检测，观察大量产品中的实际次品率逐渐接近理论值。"
    )

    y_label = "累计次品率"

    def generate_data(n):

        return np.random.binomial(
            1,
            defect_rate,
            n
        )


# ============================================================
# 实验八：随机等待时间
# ============================================================

elif experiment == "🚕 随机等待时间":

    st.sidebar.subheader("等待时间参数")

    average_wait = st.sidebar.slider(
        "理论平均等待时间",
        min_value=1.0,
        max_value=30.0,
        value=5.0,
        step=0.5
    )

    N = st.sidebar.slider(
        "等待次数 N",
        min_value=100,
        max_value=20000,
        value=5000,
        step=500
    )

    theoretical_value = average_wait

    experiment_description = (
        "模拟随机等待时间，观察大量等待事件的平均时间逐渐稳定。"
    )

    y_label = "累计平均等待时间"

    def generate_data(n):

        return np.random.exponential(
            scale=average_wait,
            size=n
        )


# ============================================================
# 控制按钮
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
    "🔄 重置实验",
    use_container_width=True
)


# ============================================================
# Session State
# ============================================================

if "experiment_data" not in st.session_state:
    st.session_state.experiment_data = None

if "last_experiment" not in st.session_state:
    st.session_state.last_experiment = experiment


# 切换实验时清除旧结果
if st.session_state.last_experiment != experiment:

    st.session_state.experiment_data = None
    st.session_state.last_experiment = experiment


# 重置
if reset_button:

    st.session_state.experiment_data = None

    st.rerun()


# ============================================================
# 开始实验
# ============================================================

if start_button:

    np.random.seed(None)

    st.session_state.experiment_data = generate_data(N)


# ============================================================
# 当前实验标题
# ============================================================

st.markdown(
    f'<div class="experiment-title">{experiment}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="experiment-description">'
    f'{experiment_description}'
    f'</div>',
    unsafe_allow_html=True
)


# ============================================================
# 尚未进行实验
# ============================================================

if st.session_state.experiment_data is None:

    st.info(
        "👈 请在左侧选择实验、调整参数，然后点击「开始实验」。"
    )

    st.markdown(
        """
        <div class="guide-text">
        💡 实验指南：尝试改变实验参数，并多次进行实验，观察随机结果的变化。
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 已经完成实验
# ============================================================

else:

    data = st.session_state.experiment_data

    # --------------------------------------------------------
    # 累计结果
    # --------------------------------------------------------

    x = np.arange(
        1,
        len(data) + 1
    )

    cumulative_values = (
        np.cumsum(data) / x
    )

    final_value = cumulative_values[-1]

    absolute_error = abs(
        final_value - theoretical_value
    )

    error_values = abs(
        cumulative_values - theoretical_value
    )


    # ========================================================
    # 核心指标
    # ========================================================

    st.subheader("📊 实验结果")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "实验次数",
            f"{len(data):,}"
        )

    with col2:

        st.metric(
            "理论值",
            f"{theoretical_value:.4f}"
        )

    with col3:

        st.metric(
            "最终实验值",
            f"{final_value:.4f}"
        )

    with col4:

        st.metric(
            "绝对误差",
            f"{absolute_error:.4f}"
        )


    # ========================================================
    # 累计结果图
    # ========================================================

    st.subheader("📈 累计结果变化")

    fig, ax = plt.subplots(
        figsize=(12, 5.5)
    )

    ax.plot(
        x,
        cumulative_values,
        label="累计实验值",
        color="#2E86AB",
        linewidth=1.5
    )

    ax.axhline(
        theoretical_value,
        color="#D62728",
        linestyle="--",
        linewidth=2,
        label=f"理论值 = {theoretical_value:.4f}"
    )

    ax.set_xlabel(
        "实验次数",
        fontsize=12
    )

    ax.set_ylabel(
        y_label,
        fontsize=12
    )

    ax.set_title(
        f"{experiment}：累计结果随实验次数的变化",
        fontsize=16,
        fontweight="bold"
    )

    ax.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    ax.legend(
        fontsize=11
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


    # ========================================================
    # 绝对误差图
    # ========================================================

    st.subheader("📉 绝对误差变化")

    fig2, ax2 = plt.subplots(
        figsize=(12, 3.8)
    )

    ax2.plot(
        x,
        error_values,
        color="#E67E22",
        linewidth=1.4
    )

    ax2.set_xlabel(
        "实验次数",
        fontsize=11
    )

    ax2.set_ylabel(
        "绝对误差",
        fontsize=11
    )

    ax2.set_title(
        "实验值与理论值之间的绝对误差",
        fontsize=14,
        fontweight="bold"
    )

    ax2.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    plt.tight_layout()

    st.pyplot(fig2)

    plt.close(fig2)


    # ========================================================
    # 实验指南
    # ========================================================

    st.markdown("---")

    st.markdown(
        f"""
        <div class="guide-text">
        <b>实验指南</b><br>
        当前实验进行了 {len(data):,} 次。
        理论值为 {theoretical_value:.4f}，
        最终实验值为 {final_value:.4f}。
        <br>
        可以尝试改变左侧参数，重新进行实验，
        观察实验次数增加后累计结果的变化。
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 动态演示
# ============================================================

if animation_button:

    st.markdown("---")

    st.subheader("🎬 动态演示")

    st.caption(
        "观察实验次数逐渐增加时，累计结果如何发生变化。"
    )

    chart_placeholder = st.empty()

    animation_N = min(
        N,
        3000
    )

    step = max(
        10,
        animation_N // 80
    )

    np.random.seed(None)

    animation_data = generate_data(
        animation_N
    )

    animation_cumulative = (
        np.cumsum(animation_data)
        / np.arange(
            1,
            animation_N + 1
        )
    )

    animation_x = np.arange(
        1,
        animation_N + 1
    )

    for current_n in range(
        step,
        animation_N + 1,
        step
    ):

        current_x = animation_x[:current_n]

        current_y = animation_cumulative[:current_n]

        fig_anim, ax_anim = plt.subplots(
            figsize=(12, 5.5)
        )

        ax_anim.plot(
            current_x,
            current_y,
            color="#2E86AB",
            linewidth=1.7,
            label="累计实验值"
        )

        ax_anim.axhline(
            theoretical_value,
            color="#D62728",
            linestyle="--",
            linewidth=2,
            label=f"理论值 = {theoretical_value:.4f}"
        )

        ax_anim.set_xlim(
            1,
            animation_N
        )

        y_min = min(
            np.min(current_y),
            theoretical_value
        )

        y_max = max(
            np.max(current_y),
            theoretical_value
        )

        margin = max(
            (y_max - y_min) * 0.15,
            0.1
        )

        ax_anim.set_ylim(
            y_min - margin,
            y_max + margin
        )

        ax_anim.set_xlabel(
            "实验次数",
            fontsize=12
        )

        ax_anim.set_ylabel(
            y_label,
            fontsize=12
        )

        ax_anim.set_title(
            f"{experiment}：N = {current_n:,}",
            fontsize=16,
            fontweight="bold"
        )

        ax_anim.grid(
            True,
            linestyle=":",
            alpha=0.5
        )

        ax_anim.legend(
            fontsize=11
        )

        plt.tight_layout()

        with chart_placeholder.container():

            st.pyplot(fig_anim)

            current_error = abs(
                current_y[-1] - theoretical_value
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "当前实验次数",
                    f"{current_n:,}"
                )

            with c2:

                st.metric(
                    "当前实验值",
                    f"{current_y[-1]:.4f}"
                )

            with c3:

                st.metric(
                    "当前绝对误差",
                    f"{current_error:.4f}"
                )

        plt.close(fig_anim)

        time.sleep(0.08)


# ============================================================
# 页面底部
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#999999;
        font-size:12px;
        padding-bottom:10px;
    ">
    大数定理（LLN）交互式实验室 · 随机实验与统计规律
    </div>
    """,
    unsafe_allow_html=True
)
