import streamlit as st
import time
import os
import glob
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import PyPDF2
import base64
import io

# 页面配置
st.set_page_config(
    page_title="个人主页",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session_state
if 'animation_shown' not in st.session_state:
    st.session_state.animation_shown = False
if 'animation_complete' not in st.session_state:
    st.session_state.animation_complete = False
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "首页"  # 默认选中首页

# 开场动画
def show_intro_animation():
    if not st.session_state.animation_shown:
        # 开场动画 CSS（隐藏侧边栏，但这里侧边栏已移除，为安全保留）
        st.markdown("""
        <style id="hide-sidebar-style">
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            button[kind="header"] {
                display: none !important;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes drawLine {
                from { width: 0; }
                to { width: 100%; }
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            @keyframes fadeOutIntro {
                from { opacity: 1; }
                to { opacity: 0; pointer-events: none; }
            }
            .intro-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #fafafa 0%, #e0e0e0 100%);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                animation: fadeOutIntro 1s ease-in-out 4s forwards;
            }
            .intro-title {
                font-size: 4rem;
                font-weight: bold;
                color: #1a1a1a;
                text-align: center;
                animation: fadeIn 1s ease-out;
                font-family: 'Comic Sans MS', cursive, sans-serif;
                border: 4px solid #1a1a1a;
                padding: 20px 40px;
                border-radius: 20px;
                background: white;
                box-shadow: 8px 8px 0px #1a1a1a;
            }
            .intro-subtitle {
                font-size: 1.5rem;
                color: #333;
                margin-top: 30px;
                animation: fadeIn 1s ease-out 0.5s backwards;
                border-bottom: 3px solid #1a1a1a;
                padding-bottom: 10px;
            }
            .intro-doodle {
                display: flex;
                gap: 20px;
                margin-top: 40px;
                animation: fadeIn 1s ease-out 1s backwards;
            }
            .doodle-item {
                width: 60px;
                height: 60px;
                border: 3px solid #1a1a1a;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                background: white;
                box-shadow: 4px 4px 0px #1a1a1a;
                animation: bounce 0.6s ease-in-out infinite;
            }
            .doodle-item:nth-child(1) { animation-delay: 0s; }
            .doodle-item:nth-child(2) { animation-delay: 0.2s; }
            .doodle-item:nth-child(3) { animation-delay: 0.4s; }
            .doodle-item:nth-child(4) { animation-delay: 0.6s; }
            .intro-line {
                width: 200px;
                height: 4px;
                background: #1a1a1a;
                margin-top: 30px;
                animation: drawLine 1s ease-out 1.5s backwards;
                border-radius: 2px;
            }
            .loading-text {
                font-size: 1rem;
                color: #666;
                margin-top: 20px;
                animation: fadeIn 1s ease-out 2s backwards;
            }
            .loading-dots::after {
                content: '';
                animation: dots 1.5s steps(4, end) infinite;
            }
            @keyframes dots {
                0%, 20% { content: ''; }
                40% { content: '.'; }
                60% { content: '..'; }
                80%, 100% { content: '...'; }
            }
            .sketch-decoration {
                position: absolute;
                opacity: 0.3;
            }
            .sketch-decoration.top-left {
                top: 10%;
                left: 10%;
                font-size: 60px;
                animation: rotate 10s linear infinite;
            }
            .sketch-decoration.top-right {
                top: 15%;
                right: 15%;
                font-size: 50px;
                animation: bounce 2s ease-in-out infinite;
            }
            .sketch-decoration.bottom-left {
                bottom: 20%;
                left: 15%;
                font-size: 40px;
                animation: bounce 1.5s ease-in-out infinite 0.5s;
            }
            .sketch-decoration.bottom-right {
                bottom: 15%;
                right: 10%;
                font-size: 55px;
                animation: rotate 8s linear infinite reverse;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # 开场动画 HTML
        st.markdown("""
        <div class="intro-container" id="intro-container">
            <div class="sketch-decoration top-left">✨</div>
            <div class="sketch-decoration top-right">⭐</div>
            <div class="sketch-decoration bottom-left">📝</div>
            <div class="sketch-decoration bottom-right">🎯</div>
            <div class="intro-title">欢迎光临</div>
            <div class="intro-subtitle">王露露的个人主页</div>
            <div class="intro-doodle">
                <div class="doodle-item">💻</div>
                <div class="doodle-item">🎨</div>
                <div class="doodle-item">📱</div>
                <div class="doodle-item">🚀</div>
            </div>
            <div class="intro-line"></div>
            <div class="loading-text">正在加载<span class="loading-dots"></span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # 动画结束后移除隐藏侧边栏样式和动画容器
        st.markdown("""
        <script>
            setTimeout(function() {
                var styleTag = document.getElementById('hide-sidebar-style');
                if (styleTag) styleTag.remove();
                var intro = document.getElementById('intro-container');
                if (intro) intro.remove();
            }, 4500);
        </script>
        """, unsafe_allow_html=True)
        
        st.session_state.animation_shown = True

# 显示开场动画
show_intro_animation()

# 自定义CSS样式 - 黑白简笔画风格 + 顶部导航
st.markdown("""
<style>
    .stApp { background-color: #fafafa; }
    
    /* 顶部导航栏样式 */
    .top-nav {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 10px 0;
        margin-bottom: 30px;
        border-bottom: 2px solid #1a1a1a;
        flex-wrap: wrap;
    }
    .nav-button {
        background-color: white;
        border: 2px solid #1a1a1a;
        border-radius: 10px;
        padding: 8px 20px;
        font-size: 1rem;
        font-weight: bold;
        color: #1a1a1a;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 2px 2px 0px #1a1a1a;
        text-align: center;
        min-width: 80px;
    }
    .nav-button:hover {
        background-color: #1a1a1a;
        color: white;
        transform: translate(-2px, -2px);
        box-shadow: 4px 4px 0px #1a1a1a;
    }
    .nav-button-active {
        background-color: #1a1a1a;
        color: white;
        box-shadow: 2px 2px 0px #1a1a1a;
    }
    
    /* 原有样式 */
    .main-title {
        font-size: 2.5rem; font-weight: bold; color: #1a1a1a; text-align: center;
        padding: 20px; margin-bottom: 30px; border: 3px solid #1a1a1a; border-radius: 15px;
        background-color: white; box-shadow: 5px 5px 0px #1a1a1a;
    }
    .sub-title {
        font-size: 1.5rem; color: #333; text-align: center; margin-bottom: 20px;
        border-bottom: 2px dashed #666; padding-bottom: 10px;
    }
    .stButton > button {
        background-color: white; color: #1a1a1a; border: 2px solid #1a1a1a;
        border-radius: 10px; padding: 10px 25px; font-size: 1rem; font-weight: bold;
        transition: all 0.3s ease; box-shadow: 3px 3px 0px #1a1a1a;
    }
    .stButton > button:hover {
        background-color: #1a1a1a; color: white; transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0px #1a1a1a;
    }
    .card {
        background-color: white; border: 2px solid #1a1a1a; border-radius: 12px;
        padding: 20px; margin: 15px 0; box-shadow: 4px 4px 0px #1a1a1a;
    }
    .avatar {
        width: 180px; height: 180px; border: 4px solid #1a1a1a; border-radius: 50%;
        background-color: #f0f0f0; box-shadow: 5px 5px 0px #1a1a1a; margin: 0 auto;
        display: flex; align-items: center; justify-content: center; font-size: 80px;
    }
    .info-item {
        padding: 10px; margin: 10px 0; border-left: 4px solid #1a1a1a;
        background-color: rgba(255,255,255,0.8); font-size: 1.1rem;
    }
    .skill-bar {
        background-color: #e0e0e0; border: 2px solid #1a1a1a; border-radius: 10px;
        height: 25px; margin: 10px 0; overflow: hidden;
    }
    .skill-progress {
        background-color: #1a1a1a; height: 100%; display: flex;
        align-items: center; justify-content: center; color: white; font-weight: bold;
    }
    .project-card {
        background-color: white; border: 2px solid #1a1a1a; border-radius: 10px;
        padding: 15px; margin: 10px 0; box-shadow: 3px 3px 0px #1a1a1a;
        transition: all 0.3s;
    }
    .project-card:hover {
        transform: translate(-2px, -2px); box-shadow: 5px 5px 0px #1a1a1a;
    }
    .timeline-item {
        border-left: 3px solid #1a1a1a; padding-left: 25px; margin: 20px 0;
        position: relative; margin-left: 10px;
    }
    .timeline-item::before {
        content: ""; position: absolute; left: -9px; top: 3px; width: 14px; height: 14px;
        background-color: white; border: 3px solid #1a1a1a; border-radius: 50%;
        box-sizing: border-box;
    }
</style>
""", unsafe_allow_html=True)

# 顶部导航栏（使用自定义 HTML + Streamlit 按钮回调）
# 为了避免在动画期间显示导航栏，但动画容器会覆盖全屏，所以导航栏会被覆盖，不影响。
# 但为了代码整洁，我们直接在主内容区域放置导航栏。

# 定义一个函数来切换页面
def set_page(page_name):
    st.session_state.selected_page = page_name

# 显示导航栏（使用 st.columns 制作按钮）
nav_cols = st.columns(5)
pages = ["首页", "关于我", "成就", "作品", "联系"]
icons = ["🏠", "👤", "🏆", "🎨", "✉️"]

for idx, (page, icon) in enumerate(zip(pages, icons)):
    with nav_cols[idx]:
        # 判断当前按钮是否被选中
        if st.session_state.selected_page == page:
            st.button(f"{icon} {page}", key=f"nav_{page}", on_click=set_page, args=(page,), use_container_width=True, type="primary")
        else:
            st.button(f"{icon} {page}", key=f"nav_{page}", on_click=set_page, args=(page,), use_container_width=True)

# 根据选中的页面显示内容
selected = st.session_state.selected_page

# 首页
if selected == "首页":
    st.markdown('<div class="main-title">欢迎来到王露露的主页</div>', unsafe_allow_html=True)
    
    # 显示头像图片（居中、放大、圆形边框）
    if os.path.exists("icon/head.jpg"):
        # 读取图片并转为base64
        import base64
        with open("icon/head.jpg", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        
        # 使用HTML直接显示居中的圆形图片
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <img src="data:image/jpeg;base64,{img_base64}" 
                 style="width: 260px; height: 260px; 
                        border: 5px solid #1a1a1a; 
                        border-radius: 50%; 
                        box-shadow: 6px 6px 0px #1a1a1a;
                        object-fit: cover;">
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="avatar">👤</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-title">一个神秘的人</div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 简介")
    st.write("这是一个娱乐版的个人主页。")
    st.write("这里没什么东西吧应该。")
    st.write("也许你可以自己看看？")
    st.write("不看也行。")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📁 查看项目"):
            st.info("全是vibe出来的")
    with col2:
        if st.button("💼 我的简历"):
            st.info("我怎么可能把简历放到这种地方呢？")
    with col3:
        if st.button("📧 联系我"):
            st.info("最好别联系，因为我可能会当成诈骗")

# 关于我
elif selected == "关于我":
    st.markdown('<div class="main-title">关于我</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="avatar">👤</div>', unsafe_allow_html=True)
        st.markdown('\n')
        st.markdown('<div style="text-align: center;">我是谁啊？我到底是谁啊？</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("### 基本信息")
        st.markdown('<div class="info-item">📌 化名：王露露</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">📍 地点：中国科学技术大学</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">🎓 学历：高中</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">💼 职业：职业在哪，这个Agent有点笨了</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📖 教育经历")
    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.write("**2024至今** | 中国科学技术大学 | 人工智能专业")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.write("**2022 - 2024** | 新乡市天立高级中学")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.write("**2018 - 2022** | 郑州市宇华实验学校")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.write("**2012 - 2018** | 安阳市第一实验小学")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# 奖项
elif selected == "成就":
    st.markdown('<div class="main-title">荣誉奖项</div>', unsafe_allow_html=True)
    
    # 两列布局：正经奖项 vs 不太正经的奖项
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏅 正经奖项")
        
        serious_awards = [
            {"name": "“用英语讲科大故事”短视频大赛", "level": "最佳活力奖", "year": "2025"},
            {"name": "全国大学生数学竞赛", "level": "省一", "year": "2025"},
            {"name": "人工智能与数据科学学院“重温科大故事，传承精神谱系”征文活动", "level": "一等奖", "year": "2026"},
        ]
        
        for award in serious_awards:
            st.markdown(f"""
            <div style="border-left: 4px solid #1a1a1a; padding: 10px; margin: 10px 0; background-color: #f9f9f9; border-radius: 5px;">
                <strong>🏆 {award['name']}</strong><br>
                <span style="color: #666;">{award['level']} | {award['year']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎭 不太正经的奖项")
        
        funny_awards = [
            {"name": "大香蕉", "desc": "唱跳Rap，没有篮球", "year": "2024"},
            {"name": "搬史大王", "desc": "运营某个神秘史群", "year": "长期有效"},
            
        ]
        
        for award in funny_awards:
            st.markdown(f"""
            <div style="border-left: 4px solid #ff6b6b; padding: 10px; margin: 10px 0; background-color: #fff5f5; border-radius: 5px;">
                <strong>🎉 {award['name']}</strong><br>
                <span style="color: #666;">{award['desc']} | {award['year']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 作品
elif selected == "作品":
    st.markdown('<div class="main-title">我的作品</div>', unsafe_allow_html=True)
    
    # 创建三个板块标签页
    tab1, tab2, tab3 = st.tabs(["🖼️ 图像板块", "🎵 音乐板块", "📝 文章板块"])
    
    # 图像板块
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📷 图片展示")
        
        # 获取 pictures 文件夹中的图片
        pictures_dir = "pictures"
        if os.path.exists(pictures_dir):
            image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']
            image_files = []
            for ext in image_extensions:
                image_files.extend(glob.glob(os.path.join(pictures_dir, ext)))
            # 去重（Windows文件系统不区分大小写，可能重复匹配）
            image_files = list(set(image_files))
            
            if image_files:
                # 按文件名排序
                image_files = sorted(image_files, key=lambda x: os.path.basename(x).lower())
                st.write(f"共找到 {len(image_files)} 张图片")
                
                # 选择图片方式
                view_mode = st.radio("查看方式", ["单张查看", "画廊模式"], horizontal=True)
                
                if view_mode == "单张查看":
                    # 单张查看模式
                    selected_image = st.selectbox(
                        "选择图片",
                        options=image_files,
                        format_func=lambda x: os.path.basename(x)
                    )
                    if selected_image:
                        st.image(selected_image, caption=os.path.basename(selected_image), use_container_width=True)
                else:
                    # 画廊模式
                    cols_per_row = st.slider("每行显示数量", 1, 4, 2)
                    for i in range(0, len(image_files), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, col in enumerate(cols):
                            if i + j < len(image_files):
                                with col:
                                    st.image(image_files[i + j], use_container_width=True)
                                    st.caption(os.path.basename(image_files[i + j]))
            else:
                st.info("📁 pictures 文件夹中暂无图片，请添加图片到 pictures 文件夹")
        else:
            st.warning("⚠️ pictures 文件夹不存在")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 音乐板块
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎶 音乐播放")
        
        # 获取 music 文件夹中的音频
        music_dir = "music"
        if os.path.exists(music_dir):
            audio_extensions = ['*.mp3', '*.wav', '*.ogg', '*.m4a', '*.flac', '*.aac']
            audio_files = []
            for ext in audio_extensions:
                audio_files.extend(glob.glob(os.path.join(music_dir, ext)))
            # 去重（Windows文件系统不区分大小写，可能重复匹配）
            audio_files = list(set(audio_files))
            
            if audio_files:
                # 按文件名排序
                audio_files = sorted(audio_files, key=lambda x: os.path.basename(x).lower())
                # 两列布局：左边选择，右边播放
                music_col1, music_col2 = st.columns(2)
                
                with music_col1:
                    st.markdown("#### 🎵 选择音乐")
                    st.write(f"共找到 {len(audio_files)} 首音乐")
                    
                    # 播放列表
                    st.markdown("##### 📋 播放列表")
                    for i, audio in enumerate(audio_files, 1):
                        st.markdown(f"**{i}.** {os.path.basename(audio)}")
                
                with music_col2:
                    st.markdown("#### 🎧 播放区域")
                    
                    # 随机播放按钮
                    import random
                    if st.button("🔀 随机播放", use_container_width=True):
                        st.session_state.random_audio = random.choice(audio_files)
                    
                    # 获取当前选中的音乐
                    if 'random_audio' not in st.session_state:
                        st.session_state.random_audio = audio_files[0] if audio_files else None
                    
                    # 选择音乐播放
                    selected_audio = st.selectbox(
                        "选择要播放的音乐",
                        options=audio_files,
                        index=audio_files.index(st.session_state.random_audio) if st.session_state.random_audio in audio_files else 0,
                        format_func=lambda x: os.path.basename(x)
                    )
                    if selected_audio:
                        st.audio(selected_audio)
                        st.caption(f"正在播放: {os.path.basename(selected_audio)}")
            else:
                st.info("📁 music 文件夹中暂无音乐，请添加音乐文件到 music 文件夹")
        else:
            st.warning("⚠️ music 文件夹不存在")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 文章板块
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📚 文章阅读")
        
        # 获取 articles 文件夹中的文章
        articles_dir = "articles"
        if os.path.exists(articles_dir):
            article_extensions = ['*.txt', '*.md', '*.markdown', '*.html', '*.docx', '*.pdf']
            article_files = []
            for ext in article_extensions:
                article_files.extend(glob.glob(os.path.join(articles_dir, ext)))
            # 去重
            article_files = list(set(article_files))
            
            if article_files:
                # 按文件名排序
                article_files = sorted(article_files, key=lambda x: os.path.basename(x).lower())
                # 两列布局：左边选择列表，右边小窗阅读
                article_col1, article_col2 = st.columns(2)
                
                with article_col1:
                    st.markdown("#### 📖 选择文章")
                    st.write(f"共找到 {len(article_files)} 篇文章")
                    
                    # 文章列表
                    st.markdown("##### 📋 文章目录")
                    for i, article in enumerate(article_files, 1):
                        st.markdown(f"**{i}.** {os.path.basename(article)}")
                
                with article_col2:
                    # 选择文章阅读
                    selected_article = st.selectbox(
                        "选择要阅读的文章",
                        options=article_files,
                        format_func=lambda x: os.path.basename(x)
                    )
                    
                    if selected_article:
                        # 小窗模式展示文章
                        article_name = os.path.basename(selected_article)
                        
                        # 读取文章内容并构建HTML
                        content_html = ""
                        try:
                            file_ext = selected_article.lower()
                            
                            if file_ext.endswith('.docx'):
                                doc = Document(selected_article)
                                
                                for para in doc.paragraphs:
                                    text = para.text.strip()
                                    if text:
                                        # 转义HTML特殊字符
                                        text = text.replace('&', '&').replace('<', '<').replace('>', '>')
                                        style_name = para.style.name if para.style else ''
                                        font_size = None
                                        is_bold = False
                                        for run in para.runs:
                                            if run.font.size:
                                                font_size = run.font.size.pt
                                            if run.bold:
                                                is_bold = True
                                        
                                        if 'Heading 1' in style_name or (font_size and font_size >= 18):
                                            content_html += f"<h3 style='margin: 10px 0;'>{text}</h3>"
                                        elif 'Heading 2' in style_name or (font_size and font_size >= 16):
                                            content_html += f"<h4 style='margin: 10px 0;'>{text}</h4>"
                                        elif is_bold:
                                            content_html += f"<p style='margin: 8px 0;'><strong>{text}</strong></p>"
                                        else:
                                            content_html += f"<p style='margin: 8px 0; line-height: 1.6;'>{text}</p>"
                                
                            elif file_ext.endswith('.pdf'):
                                with open(selected_article, 'rb') as f:
                                    pdf_reader = PyPDF2.PdfReader(f)
                                    content = ''
                                    for page in pdf_reader.pages:
                                        content += page.extract_text() + '\n'
                                    content = content.replace('&', '&').replace('<', '<').replace('>', '>')
                                    content_html += f"<pre style='white-space: pre-wrap; font-family: inherit;'>{content}</pre>"
                            
                            elif file_ext.endswith('.md') or file_ext.endswith('.markdown'):
                                with open(selected_article, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                content = content.replace('&', '&').replace('<', '<').replace('>', '>')
                                content_html += f"<div style='line-height: 1.6; white-space: pre-wrap;'>{content}</div>"
                            
                            else:
                                with open(selected_article, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                content = content.replace('&', '&').replace('<', '<').replace('>', '>')
                                content_html += f"<pre style='white-space: pre-wrap; font-family: inherit;'>{content}</pre>"
                                
                        except Exception as e:
                            content_html = f"<p style='color: red;'>读取文章失败: {e}</p>"
                        
                        # 输出完整的小窗HTML
                        st.markdown(f"""
                        <div style="border: 3px solid #1a1a1a; border-radius: 12px; background-color: #fff; 
                                    box-shadow: 4px 4px 0px #1a1a1a; margin-top: 15px; overflow: hidden;">
                            <div style="background-color: #1a1a1a; color: white; padding: 10px 15px; 
                                        font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
                                <span>📄 {article_name}</span>
                                <div style="display: flex; gap: 6px;">
                                    <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #ff5f56;"></div>
                                    <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #ffbd2e;"></div>
                                    <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #27ca40;"></div>
                                </div>
                            </div>
                            <div style="height: 400px; overflow-y: auto; padding: 15px; background-color: #fafafa;">
                                {content_html}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📁 articles 文件夹中暂无文章，请添加文章文件（支持 .txt, .md, .html, .docx, .pdf 格式）到 articles 文件夹")
        else:
            st.warning("⚠️ articles 文件夹不存在")
        
        st.markdown('</div>', unsafe_allow_html=True)

# 联系
elif selected == "联系":
    st.markdown('<div class="main-title">联系我</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📬 联系方式")
        st.markdown('<div class="info-item">📧 Email: wanglulu114514@mail.ustc.edu.cn</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">💬 QQ: 我不会告诉你任何事情！</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🌐 社交媒体")
        st.markdown('<div class="info-item">GitHub: https://github.com/Wanglulu114514</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">Bilibili: https://space.bilibili.com/3546699511368153?spm_id_from=333.1007.0.0</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-item">博客: 没有</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💬 给我留言")
    name = st.text_input("您的姓名")
    email = st.text_input("您的邮箱")
    message = st.text_area("留言内容")
    if st.button("发送留言"):
        if name and email and message:
            st.success("我都不知道AI为什么要给我搓个这种东西，一点用没有，留了个棍木。")
        else:
            st.warning("别在这留言")
    st.markdown('</div>', unsafe_allow_html=True)
