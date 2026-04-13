import streamlit as st
import time
import os
import glob
from docx import Document
import base64
from streamlit.components.v1 import html as components_html

# 页面配置
st.set_page_config(
    page_title="王露露的个人主页",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化 session_state - 确保动画状态持久化
if 'animation_complete' not in st.session_state:
    st.session_state.animation_complete = False
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "首页"
if 'lulu_cmd' not in st.session_state:
    st.session_state.lulu_cmd = ""
if 'lulu_count' not in st.session_state:
    st.session_state.lulu_count = 8
if 'lulu_cmd' not in st.session_state:
    st.session_state.lulu_cmd = ""
if 'lulu_count' not in st.session_state:
    st.session_state.lulu_count = 8  # 初始头像数量

# 资源目录路径
pictures_dir = "pictures"
music_dir = "music"
articles_dir = "articles"

# 页面加载时标记动画完成
def mark_animation_complete():
    st.session_state.animation_complete = True

# ============ 开场动画 ============
def show_intro_animation():
    # 只有当动画未完成时才显示
    if not st.session_state.animation_complete:
        st.markdown("""
        <style>
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
        }
        @keyframes fadeOutAndRemove {
            0% { opacity: 1; }
            70% { opacity: 1; }
            100% { opacity: 0; visibility: hidden; pointer-events: none; }
        }
        .intro-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
            background-size: 400% 400%;
            animation: 
                gradientMove 2s ease infinite,
                fadeOutAndRemove 4s ease forwards;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 99999;
        }
        .intro-title {
            font-size: 4rem;
            font-weight: bold;
            color: white;
            text-align: center;
            animation: fadeInUp 0.8s ease-out;
            text-shadow: 0 0 30px rgba(255,255,255,0.5);
            margin-bottom: 20px;
        }
        .intro-subtitle {
            font-size: 1.8rem;
            color: rgba(255,255,255,1.0);
            margin-bottom: 40px;
            animation: fadeInUp 0.8s ease-out 0.3s backwards;
        }
        .intro-dots {
            display: flex;
            gap: 15px;
            animation: fadeInUp 0.8s ease-out 0.6s backwards;
        }
        .intro-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: white;
            animation: pulse 1.4s ease-in-out infinite;
        }
        .intro-dot:nth-child(2) { animation-delay: 0.2s; }
        .intro-dot:nth-child(3) { animation-delay: 0.4s; }
        .intro-sparkle {
            position: absolute;
            font-size: 2rem;
            animation: sparkle 2s ease-in-out infinite;
        }
        .intro-sparkle:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
        .intro-sparkle:nth-child(2) { top: 30%; right: 15%; animation-delay: 0.5s; }
        .intro-sparkle:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 1s; }
        .intro-sparkle:nth-child(4) { bottom: 35%; right: 10%; animation-delay: 1.5s; }
        .intro-float {
            animation: float 3s ease-in-out infinite;
        }
        </style>
        <div class="intro-container" id="intro-container">
            <span class="intro-sparkle">✨</span>
            <span class="intro-sparkle">⭐</span>
            <span class="intro-sparkle">💫</span>
            <span class="intro-sparkle">🌟</span>
            <div class="intro-float">
                <div class="intro-title">✨ 欢迎光临 ✨</div>
                <div class="intro-subtitle">王露露的个人主页</div>
            </div>
            <div class="intro-dots">
                <div class="intro-dot"></div>
                <div class="intro-dot"></div>
                <div class="intro-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 使用 iframe 内的脚本自动移除元素
        st.markdown("""
        <script>
        setTimeout(function() {
            var intro = document.getElementById('intro-container');
            if (intro && intro.parentNode) {
                intro.parentNode.removeChild(intro);
            }
        }, 4200);
        </script>
        """, unsafe_allow_html=True)
        
        st.session_state.animation_complete = True

# 显示开场动画
show_intro_animation()

# ============ 自定义CSS样式 ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    * { font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* 全局文字颜色 - 覆盖 st.markdown 默认黑色 */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: rgba(255, 255, 255, 1.0) !important;
    }
    
    /* Streamlit 通用文字颜色 */
    body, .stApp, p, div, span, label {
        color: rgba(255, 255, 255, 1.0) !important;
    }
    
    /* 标题颜色 */
    h1, h2, h3, h4, h5, h6 {
        color: rgba(255, 255, 255, 1.0) !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    /* 玻璃态卡片 */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* 主标题 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
    }
    
    /* 导航栏 */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        padding: 15px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .nav-btn {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 12px 25px;
        color: white;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .nav-btn:hover {
        background: linear-gradient(135deg, #667eea, #764ba2);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    .nav-btn-active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 头像样式 */
    .avatar-container {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto 30px;
    }
    .avatar-border {
        position: absolute;
        top: -5px;
        left: -5px;
        right: -5px;
        bottom: -5px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 300% 300%;
        animation: gradientMove 3s ease infinite;
        z-index: -1;
    }
    .avatar-img {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid rgba(255, 255, 255, 1.0);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 统计卡片 */
    .stat-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        color: rgba(255, 255, 255, 1.0);
        font-size: 1rem;
        margin-top: 5px;
    }
    
    /* 时间线 */
    .timeline {
        position: relative;
        padding-left: 30px;
    }
    .timeline::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(to bottom, #667eea, #764ba2, #f093fb);
        border-radius: 3px;
    }
    .timeline-item {
        position: relative;
        padding: 15px 20px;
        margin-bottom: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border-left: 3px solid transparent;
        transition: all 0.3s ease;
    }
    .timeline-item:hover {
        background: rgba(255, 255, 255, 0.1);
        border-left-color: #667eea;
        transform: translateX(5px);
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -36px;
        top: 20px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        color: rgba(255, 255, 255, 1.0);
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
    }
    
    /* 文章窗口 */
    .article-window {
        background: rgba(30, 30, 50, 0.9);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .article-header {
        background: linear-gradient(135deg, #2d2d44, #3d3d5c);
        padding: 12px 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .article-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    .article-content {
        padding: 20px;
        max-height: 400px;
        overflow-y: auto;
        color: rgba(255, 255, 255, 1.0);
        line-height: 1.8;
    }
    
    /* Canvas容器 */
    #lulu-canvas-container {
        position: relative;
        width: 100%;
        height: 70vh;
        border-radius: 20px;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    #luluCanvas {
        display: block;
        width: 100%;
        height: 100%;
        cursor: crosshair;
    }
    .canvas-hint {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 0.9rem;
        pointer-events: none;
    }
    
    /* 滚动条美化 */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.1); border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(#667eea, #764ba2); border-radius: 4px; }
    
    /* 信息项 */
    .info-item {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid #667eea;
        padding: 12px 18px;
        border-radius: 8px;
        margin: 10px 0;
        color: rgba(255, 255, 255, 1.0);
        transition: all 0.3s ease;
    }
    .info-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    /* 奖项卡片 */
    .award-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .award-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============ 页面切换逻辑 ============
def set_page(page_name):
    st.session_state.selected_page = page_name

# 顶部导航
pages = ["首页", "关于我", "成就", "作品", "露露", "联系"]
icons = ["🏠", "👤", "🏆", "🎨", "🎮", "✉️"]

st.markdown('<div class="nav-container">', unsafe_allow_html=True)
cols = st.columns(len(pages))
for idx, (page, icon) in enumerate(zip(pages, icons)):
    with cols[idx]:
        if st.session_state.selected_page == page:
            st.button(f"{icon} {page}", key=f"nav_{page}", on_click=set_page, args=(page,), type="primary", use_container_width=True)
        else:
            st.button(f"{icon} {page}", key=f"nav_{page}", on_click=set_page, args=(page,), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

selected = st.session_state.selected_page

# ============ 首页 ============
if selected == "首页":
    st.markdown('<div class="main-title">✨ 欢迎来到王露露的主页 ✨</div>', unsafe_allow_html=True)
    
    # 头像
    if os.path.exists("icon/head.jpg"):
        with open("icon/head.jpg", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div class="avatar-container">
            <div class="avatar-border"></div>
            <img src="data:image/jpeg;base64,{img_base64}" class="avatar-img">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; font-size: 120px;">👤</div>', unsafe_allow_html=True)
    
    st.markdown('<p style="text-align: center; color: rgba(255,255,255,1.0); font-size: 1.2rem;">中国科学技术大学 · 人工智能</p>', unsafe_allow_html=True)
    
    # 统计卡片
    pictures_dir = "pictures"
    music_dir = "music"
    articles_dir = "articles"
    
    pic_count = len([f for f in glob.glob(os.path.join(pictures_dir, "*.jpg"))]) if os.path.exists(pictures_dir) else 0
    music_count = len([f for f in glob.glob(os.path.join(music_dir, "*.mp3"))]) if os.path.exists(music_dir) else 0
    article_count = len([f for f in glob.glob(os.path.join(articles_dir, "*.docx"))]) if os.path.exists(articles_dir) else 0
    
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{pic_count}</div>
            <div class="stat-label">🎨 绘画作品</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{music_count}</div>
            <div class="stat-label">🎵 原创音乐</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{article_count}</div>
            <div class="stat-label">📝 文字作品</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[3]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">3</div>
            <div class="stat-label">🏆 获奖荣誉</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 快捷入口
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🚀 快速入口", unsafe_allow_html=True)
    quick_cols = st.columns(4)
    with quick_cols[0]:
        if st.button("📁 查看项目", use_container_width=True):
            st.info("全是vibe出来的")
    with quick_cols[1]:
        if st.button("💼 我的简历", use_container_width=True):
            st.info("我怎么可能把简历放到这种地方呢？")
    with quick_cols[2]:
        if st.button("🎮 露露游戏", use_container_width=True):
            set_page("露露")
            st.rerun()
    with quick_cols[3]:
        if st.button("📧 联系我", use_container_width=True):
            set_page("联系")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============ 关于我 ============
elif selected == "关于我":
    st.markdown('<div class="main-title">👤 关于我</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if os.path.exists("icon/head.jpg"):
            with open("icon/head.jpg", "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
            <div class="avatar-container">
                <div class="avatar-border"></div>
                <img src="data:image/jpeg;base64,{img_base64}" class="avatar-img">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center; font-size: 100px;">👤</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 基本信息", unsafe_allow_html=True)
        st.markdown('<div class="info-item">📌 姓名：王露露</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">📍 学校：中国科学技术大学</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">🎓 专业：人工智能</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">📧 Email：wanglulu114514@mail.ustc.edu.cn</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📖 教育经历", unsafe_allow_html=True)
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    
    education = [
        ("2024 - 至今", "中国科学技术大学", "人工智能专业 · 本科在读"),
        ("2022 - 2024", "新乡市天立高级中学", "高中"),
        ("2018 - 2022", "郑州市宇华实验学校", "初中"),
        ("2012 - 2018", "安阳市第一实验小学", "小学"),
    ]
    
    for year, school, desc in education:
        st.markdown(f"""
        <div class="timeline-item">
            <strong style="color: #667eea;">{year}</strong><br>
            <span style="font-size: 1.1rem;">{school}</span><br>
            <span style="color: rgba(255,255,255,1.0);">{desc}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============ 成就 ============
elif selected == "成就":
    st.markdown('<div class="main-title">🏆 荣誉奖项</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏅 正式奖项", unsafe_allow_html=True)
        
        awards = [
            ("“用英语讲科大故事”短视频大赛", "最佳活力奖", "2025"),
            ("全国大学生数学竞赛", "省级一等奖", "2025"),
            ("“重温科大故事，传承精神谱系”征文", "一等奖", "2026"),
        ]
        
        for name, level, year in awards:
            st.markdown(f"""
            <div class="award-card">
                <strong>🏆 {name}</strong><br>
                <span style="color: #f093fb;">{level}</span> · <span style="color: rgba(255,255,255,1.0);">{year}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎭 特殊荣誉", unsafe_allow_html=True)
        
        fun_awards = [
            ("大香蕉", "唱跳Rap，没有篮球", "2024"),
            ("搬史大王", "运营某个神秘史群", "长期有效"),
        ]
        
        for name, desc, year in fun_awards:
            st.markdown(f"""
            <div class="award-card" style="border-color: rgba(245, 87, 108, 0.3);">
                <strong>🎉 {name}</strong><br>
                <span style="color: #f5576c;">{desc}</span> · <span style="color: rgba(255,255,255,1.0);">{year}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============ 作品 ============
elif selected == "作品":
    st.markdown('<div class="main-title">🎨 我的作品</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🖼️ 绘画", "🎵 音乐", "📝 文章"])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📷 绘画作品展示", unsafe_allow_html=True)
        
        if os.path.exists(pictures_dir):
            image_files = [f for f in glob.glob(os.path.join(pictures_dir, "*.jpg"))]
            if image_files:
                image_files = sorted(image_files, key=lambda x: os.path.basename(x).lower())
                st.write(f"共 **{len(image_files)}** 幅作品")
                
                view_mode = st.radio("查看方式", ["单张查看", "画廊模式"], horizontal=True)
                
                if view_mode == "单张查看":
                    selected_image = st.selectbox("选择作品", image_files, format_func=lambda x: os.path.basename(x))
                    if selected_image:
                        st.image(selected_image, caption=os.path.basename(selected_image), use_container_width=True)
                else:
                    cols_per_row = st.slider("每行显示", 1, 4, 2)
                    for i in range(0, len(image_files), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, col in enumerate(cols):
                            if i + j < len(image_files):
                                with col:
                                    st.image(image_files[i + j], use_container_width=True)
                                    st.caption(os.path.basename(image_files[i + j]))
            else:
                st.info("暂无绘画作品")
        else:
            st.warning("pictures 文件夹不存在")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎶 原创音乐", unsafe_allow_html=True)
        
        if os.path.exists(music_dir):
            audio_files = [f for f in glob.glob(os.path.join(music_dir, "*.mp3"))]
            if audio_files:
                audio_files = sorted(audio_files, key=lambda x: os.path.basename(x).lower())
                st.write(f"共 **{len(audio_files)}** 首音乐")
                
                music_cols = st.columns([1, 2])
                with music_cols[0]:
                    st.markdown("#### 📋 播放列表")
                    for i, audio in enumerate(audio_files, 1):
                        st.markdown(f"**{i}.** {os.path.basename(audio)}")
                with music_cols[1]:
                    selected_audio = st.selectbox("选择音乐", audio_files, format_func=lambda x: os.path.basename(x))
                    if selected_audio:
                        st.audio(selected_audio)
                        st.success(f"🎵 正在播放: {os.path.basename(selected_audio)}")
            else:
                st.info("暂无音乐作品")
        else:
            st.warning("music 文件夹不存在")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📚 文字作品", unsafe_allow_html=True)
        
        if os.path.exists(articles_dir):
            article_files = [f for f in glob.glob(os.path.join(articles_dir, "*.docx"))]
            if article_files:
                article_files = sorted(article_files, key=lambda x: os.path.basename(x).lower())
                st.write(f"共 **{len(article_files)}** 篇文章")
                
                article_cols = st.columns([1, 2])
                with article_cols[0]:
                    st.markdown("#### 📖 文章目录")
                    for i, article in enumerate(article_files, 1):
                        st.markdown(f"**{i}.** {os.path.basename(article)}")
                
                with article_cols[1]:
                    selected_article = st.selectbox("阅读文章", article_files, format_func=lambda x: os.path.basename(x))
                    if selected_article:
                        try:
                            doc = Document(selected_article)
                            content = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
                            
                            st.markdown(f"""
                            <div class="article-window">
                                <div class="article-header">
                                    <div class="article-dot" style="background: #ff5f56;"></div>
                                    <div class="article-dot" style="background: #ffbd2e;"></div>
                                    <div class="article-dot" style="background: #27ca40;"></div>
                                    <span style="margin-left: 10px; color: rgba(255,255,255,1.0);">{os.path.basename(selected_article)}</span>
                                </div>
                                <div class="article-content">
                                    {content}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"读取失败: {e}")
            else:
                st.info("暂无文章")
        else:
            st.warning("articles 文件夹不存在")
        st.markdown('</div>', unsafe_allow_html=True)

# ============ 露露页面 - 物理模拟游戏 ============
elif selected == "露露":
    st.markdown('<div class="main-title">🎮 露露的物理世界</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: rgba(255,255,255,1.0);">点击鼠标产生震荡波，让头像们飞起来吧！</p>', unsafe_allow_html=True)
    
    # 获取头像 base64
    avatar_b64 = ""
    if os.path.exists("icon/head.jpg"):
        with open("icon/head.jpg", "rb") as f:
            avatar_b64 = base64.b64encode(f.read()).decode()
    
    # 获取命令和头像数量
    lulu_cmd = st.session_state.get('lulu_cmd', '')
    lulu_count = st.session_state.get('lulu_count', 8)
    
    # 使用 components.v1.html 注入游戏
    game_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }}
            #container {{ position: relative; width: 100vw; height: 80vh; }}
            #canvas {{ display: block; width: 100%; height: 100%; cursor: crosshair; }}
            .hint {{ 
                position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
                background: rgba(0,0,0,0.6); color: white; padding: 10px 20px;
                border-radius: 20px; font-size: 14px; pointer-events: none;
            }}
            .game-btn {{
                position: absolute; top: 15px; padding: 8px 18px;
                background: rgba(102, 126, 234, 0.8); color: white;
                border: none; border-radius: 20px; cursor: pointer;
                font-size: 14px; transition: all 0.3s; z-index: 10;
            }}
            .game-btn:hover {{ background: rgba(102, 126, 234, 1); transform: scale(1.05); }}
            #btn-reset {{ left: 15px; }}
            #btn-add {{ left: 100px; }}
            #btn-wave {{ left: 185px; }}
            #cmd-target {{ 
                position: absolute; top: -9999px; left: -9999px;
                width: 1px; height: 1px; opacity: 0;
            }}
        </style>
    </head>
    <body>
        <div id="container">
            <button class="game-btn" id="btn-reset" onclick="resetGame()">🔄 重置</button>
            <button class="game-btn" id="btn-add" onclick="addAvatar()">➕ 头像</button>
            <button class="game-btn" id="btn-wave" onclick="randomWave()">🎆 震荡</button>
            <canvas id="canvas"></canvas>
            <div class="hint">👆 点击画面产生震荡波</div>
        </div>
        <input type="text" id="cmd-target" readonly>
        <script>
            var avatarB64 = "{avatar_b64}";
            var img = new Image();
            img.src = "data:image/jpeg;base64," + avatarB64;
            var INIT_COUNT = {lulu_count};
            
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");
            var avatars = [];
            var waves = [];
            var GRAVITY = 0.4, FRICTION = 0.98, ROTATION_FRICTION = 0.96, BOUNCE = 0.7;
            var MIN_R = 40, MAX_R = 65;
            var WAVE_R = 180, WAVE_F = 30;
            
            var pendingCmd = "";
            
            function checkCommand() {{
                var el = document.getElementById("cmd-target");
                if(el && el.value && el.value !== pendingCmd) {{
                    pendingCmd = el.value;
                    if(pendingCmd === "reset") {{ resetGame(); }}
                    else if(pendingCmd === "add") {{ addAvatar(); }}
                    else if(pendingCmd === "wave") {{ randomWave(); }}
                    el.value = "";
                }}
            }}
            
            // 检查初始命令
            var INIT_CMD = "{lulu_cmd}";
            if(INIT_CMD === "reset") {{ setTimeout(resetGame, 100); }}
            else if(INIT_CMD === "add") {{ setTimeout(addAvatar, 100); }}
            else if(INIT_CMD === "wave") {{ setTimeout(randomWave, 100); }}
            
            function resetGame() {{
                avatars = [];
                var r = MIN_R + Math.random() * (MAX_R - MIN_R);
                for(var i = 0; i < INIT_COUNT; i++) {{
                    r = MIN_R + Math.random() * (MAX_R - MIN_R);
                    avatars.push(new CircleAvatar(
                        r + Math.random() * (canvas.width - r * 2),
                        r + Math.random() * (canvas.height * 0.4),
                        r
                    ));
                }}
            }}
            
            function addAvatar() {{
                if(avatars.length < 30) {{
                    var r = MIN_R + Math.random() * (MAX_R - MIN_R);
                    avatars.push(new CircleAvatar(
                        r + Math.random() * (canvas.width - r * 2),
                        r + Math.random() * (canvas.height * 0.3),
                        r
                    ));
                }}
            }}
            
            function randomWave() {{
                var cx = canvas.width / 2, cy = canvas.height / 2;
                var ox = (Math.random() - 0.5) * canvas.width * 0.6;
                var oy = (Math.random() - 0.5) * canvas.height * 0.4;
                waves.push(new Wave(cx + ox, cy + oy));
                for(var i = 0; i < avatars.length; i++) {{
                    var a = avatars[i], dx = a.x - (cx + ox), dy = a.y - (cy + oy);
                    var d = Math.sqrt(dx * dx + dy * dy);
                    if(d < WAVE_R && d > 0) {{
                        var f = (1 - d / WAVE_R) * WAVE_F * 1.5;
                        a.force((dx / d) * f + (Math.random() - 0.5) * 8, (dy / d) * f - Math.random() * 10);
                    }}
                }}
            }}
            
            function CircleAvatar(x, y, r) {{
                this.x = x; this.y = y; this.r = r;
                this.vx = (Math.random()-0.5)*4;
                this.vy = (Math.random()-0.5)*4;
                this.rot = 0; this.rotS = (Math.random()-0.5)*0.1;
            }}
            CircleAvatar.prototype.update = function(w, h) {{
                this.vy += GRAVITY; this.vx *= FRICTION; this.vy *= FRICTION;
                this.rotS *= ROTATION_FRICTION; // 旋转摩擦力
                this.x += this.vx; this.y += this.vy; this.rot += this.rotS;
                if(this.x-this.r<0){{this.x=this.r;this.vx*=-BOUNCE;}}
                if(this.x+this.r>w){{this.x=w-this.r;this.vx*=-BOUNCE;}}
                if(this.y-this.r<0){{this.y=this.r;this.vy*=-BOUNCE;}}
                if(this.y+this.r>h){{this.y=h-this.r;this.vy*=-BOUNCE;}}
            }};
            CircleAvatar.prototype.draw = function(ctx) {{
                ctx.save(); ctx.translate(this.x, this.y); ctx.rotate(this.rot);
                ctx.beginPath(); ctx.arc(0,0,this.r,0,Math.PI*2); ctx.clip();
                ctx.drawImage(img, -this.r, -this.r, this.r*2, this.r*2);
                ctx.restore();
            }};
            CircleAvatar.prototype.force = function(fx, fy){{
                this.vx+=fx; this.vy+=fy; 
                // 只有旋转速度较小时才添加随机旋转
                if(Math.abs(this.rotS) < 0.1) this.rotS=(Math.random()-0.5)*0.2;
            }};
            
            function Wave(x, y){{ this.x=x; this.y=y; this.r=0; this.a=1; }}
            Wave.prototype.update = function(){{ this.r+=6; this.a-=0.025; }};
            Wave.prototype.draw = function(ctx){{
                if(this.a<=0)return;
                ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
                ctx.strokeStyle="rgba(147,112,219,"+this.a+")"; ctx.lineWidth=3; ctx.stroke();
                ctx.beginPath(); ctx.arc(this.x,this.y,this.r*0.65,0,Math.PI*2);
                ctx.strokeStyle="rgba(255,182,193,"+(this.a*0.8)+")"; ctx.lineWidth=2; ctx.stroke();
            }};
            Wave.prototype.done = function(){{ return this.a<=0; }};
            
            function collide(a, b) {{
                var dx=b.x-a.x, dy=b.y-a.y, d=Math.sqrt(dx*dx+dy*dy);
                var m=a.r+b.r;
                if(d<m&&d>0){{
                    var o=(m-d)/2, nx=dx/d, ny=dy/d;
                    a.x-=o*nx; a.y-=o*ny; b.x+=o*nx; b.y+=o*ny;
                    var dvx=a.vx-b.vx, dvy=a.vy-b.vy, dvn=dvx*nx+dvy*ny;
                    if(dvn>0){{ a.vx-=dvn*nx*BOUNCE; a.vy-=dvn*ny*BOUNCE; b.vx+=dvn*nx*BOUNCE; b.vy+=dvn*ny*BOUNCE; }}
                }}
            }}
            
            function resize(){{
                canvas.width = canvas.parentElement.clientWidth;
                canvas.height = canvas.parentElement.clientHeight;
            }}
            
            function init(){{
                for(var i=0;i<INIT_COUNT;i++){{
                    var r=MIN_R+Math.random()*(MAX_R-MIN_R);
                    avatars.push(new CircleAvatar(r+Math.random()*(canvas.width-r*2), r+Math.random()*(canvas.height*0.4), r));
                }}
            }}
            
            canvas.addEventListener("click", function(e){{
                var rect=canvas.getBoundingClientRect();
                var x=e.clientX-rect.left, y=e.clientY-rect.top;
                waves.push(new Wave(x,y));
                for(var i=0;i<avatars.length;i++){{
                    var a=avatars[i], dx=a.x-x, dy=a.y-y, d=Math.sqrt(dx*dx+dy*dy);
                    if(d<WAVE_R&&d>0){{
                        var f=(1-d/WAVE_R)*WAVE_F;
                        a.force((dx/d)*f+(Math.random()-0.5)*6, (dy/d)*f-Math.random()*8);
                    }}
                }}
            }});
            
            function update(){{
                checkCommand();
                for(var i=0;i<avatars.length;i++) avatars[i].update(canvas.width,canvas.height);
                for(var i=0;i<avatars.length;i++){{
                    for(var j=i+1;j<avatars.length;j++) collide(avatars[i],avatars[j]);
                }}
                for(var i=0;i<waves.length;i++) waves[i].update();
                for(var i=waves.length-1;i>=0;i--) if(waves[i].done()) waves.splice(i,1);
            }}
            
            function draw(){{
                ctx.clearRect(0,0,canvas.width,canvas.height);
                for(var x=0;x<canvas.width;x+=40){{
                    for(var y=0;y<canvas.height;y+=40){{
                        if(Math.random()>0.7){{ ctx.fillStyle="rgba(255,255,255,0.03)"; ctx.fillRect(x,y,2,2); }}
                    }}
                }}
                for(var i=0;i<waves.length;i++) waves[i].draw(ctx);
                for(var i=0;i<avatars.length;i++) avatars[i].draw(ctx);
            }}
            
            function loop(){{ update(); draw(); requestAnimationFrame(loop); }}
            
            resize();
            if(img.complete) init();
            img.onload = init;
            loop();
        </script>
    </body>
    </html>
    """
    
    components_html(game_html, height=600)

# ============ 联系 ============
elif selected == "联系":
    st.markdown('<div class="main-title">✉️ 联系我</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📬 联系方式", unsafe_allow_html=True)
        st.markdown('<div class="info-item">📧 Email：wanglulu114514@mail.ustc.edu.cn</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">💬 QQ：我不告诉你！</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 社交媒体", unsafe_allow_html=True)
        st.markdown('<div class="info-item">GitHub：github.com/Wanglulu114514</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">Bilibili：space.bilibili.com/3546699511368153</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">博客：没有</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 给我留言", unsafe_allow_html=True)
    name = st.text_input("您的姓名")
    email = st.text_input("您的邮箱")
    message = st.text_area("留言内容")
    
    if st.button("🚀 发送留言", use_container_width=True):
        if name and email and message:
            st.success("收到你的留言啦！🎉")
        else:
            st.warning("请填写完整信息")
    st.markdown('</div>', unsafe_allow_html=True)

