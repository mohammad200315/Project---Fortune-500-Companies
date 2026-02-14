import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import warnings
import os
from datetime import datetime
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Fortune 500 | Executive Analytics",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Cairo:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0817 0%, #1a1530 50%, #0a0817 100%);
        position: relative;
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 15% 25%, rgba(212, 175, 55, 0.18) 0%, transparent 25%),
            radial-gradient(circle at 85% 65%, rgba(212, 175, 55, 0.15) 0%, transparent 30%),
            radial-gradient(circle at 45% 80%, rgba(255, 215, 0, 0.12) 0%, transparent 35%),
            radial-gradient(circle at 75% 15%, rgba(212, 175, 55, 0.12) 0%, transparent 28%),
            radial-gradient(circle at 25% 55%, rgba(255, 215, 0, 0.1) 0%, transparent 32%);
        pointer-events: none;
        z-index: 0;
        animation: floatParticles 20s ease-in-out infinite;
    }
    
    @keyframes floatParticles {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.8; }
        50% { transform: scale(1.1) rotate(2deg); opacity: 1; }
    }
    
    .royal-card {
        background: rgba(18, 14, 30, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 40px;
        padding: 35px;
        margin: 25px 0;
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.6),
            0 0 0 1px rgba(212, 175, 55, 0.2) inset,
            0 0 40px rgba(212, 175, 55, 0.25);
        position: relative;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .royal-card:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 40px 80px rgba(0, 0, 0, 0.8),
            0 0 0 2px rgba(212, 175, 55, 0.4) inset,
            0 0 60px rgba(212, 175, 55, 0.4);
    }
    
    .royal-card::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 30%, rgba(212, 175, 55, 0.15), transparent 70%);
        opacity: 0.6;
        pointer-events: none;
        animation: goldSpin 15s linear infinite;
    }
    
    @keyframes goldSpin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .royal-header {
        background: linear-gradient(135deg, rgba(28, 22, 45, 0.98) 0%, rgba(18, 12, 35, 0.98) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.45);
        border-radius: 50px;
        padding: 60px 50px;
        margin-bottom: 40px;
        text-align: center;
        box-shadow: 
            0 40px 80px rgba(0, 0, 0, 0.7),
            0 0 0 2px rgba(212, 175, 55, 0.25) inset,
            0 0 60px rgba(212, 175, 55, 0.35);
        position: relative;
        overflow: hidden;
    }
    
    .royal-header::before {
        content: "⚜️ FORTUNE 500 ⚜️";
        position: absolute;
        top: 20px;
        right: 40px;
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 900;
        color: rgba(212, 175, 55, 0.2);
        letter-spacing: 6px;
        transform: rotate(90deg);
        transform-origin: right top;
        white-space: nowrap;
    }
    
    .royal-header::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 10%;
        width: 80%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.8), transparent);
    }
    
    .royal-header h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 4.2rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #fff8e7, #d4af37, #fff8e7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
        text-shadow: 0 0 30px rgba(212, 175, 55, 0.5);
        letter-spacing: 2px;
    }
    
    .royal-header p {
        font-family: 'Cairo', sans-serif !important;
        font-size: 1.6rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
        margin-top: 15px !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .gold-badge {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.25) 0%, rgba(212, 175, 55, 0.15) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(212, 175, 55, 0.6);
        border-radius: 30px;
        padding: 15px 30px;
        display: inline-block;
        margin-top: 20px;
    }
    
    .gold-badge p {
        font-family: 'Cairo', sans-serif !important;
        font-size: 1.3rem !important;
        color: #d4af37 !important;
        margin: 0 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    .metric-gold {
        background: rgba(28, 22, 45, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 25px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .metric-gold:hover {
        transform: scale(1.05);
        border-color: rgba(212, 175, 55, 0.8);
        box-shadow: 0 15px 40px rgba(212, 175, 55, 0.3);
    }
    
    .metric-gold label {
        font-family: 'Cairo', sans-serif !important;
        color: #a0aec0 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .metric-gold div {
        font-family: 'Playfair Display', serif !important;
        color: #d4af37 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(18, 14, 30, 0.6);
        padding: 12px;
        border-radius: 40px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 30px;
        color: white !important;
        padding: 15px 35px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        font-family: 'Cairo', sans-serif !important;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        color: #0a0817 !important;
        border: none;
        box-shadow: 0 5px 20px rgba(212, 175, 55, 0.5);
        font-weight: 700;
    }
    
    .stSelectbox label, .stDropdown label {
        font-family: 'Cairo', sans-serif !important;
        color: #d4af37 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(28, 22, 45, 0.8) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #d4af37 !important;
        text-shadow: 0 2px 15px rgba(212, 175, 55, 0.3) !important;
        letter-spacing: 1px !important;
    }
    
    .stMarkdown p, .stMarkdown span {
        font-family: 'Cairo', sans-serif !important;
        color: rgba(255,255,255,0.95) !important;
        font-size: 1.1rem !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        color: #0a0817 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 30px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 20px rgba(212, 175, 55, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.7) !important;
        background: linear-gradient(135deg, #e5c25f 0%, #d4af37 100%) !important;
    }
    
    .stDataFrame {
        background: rgba(18, 14, 30, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 20px !important;
        padding: 15px !important;
    }
    
    .stDataFrame td, .stDataFrame th {
        font-family: 'Cairo', sans-serif !important;
        color: white !important;
        background: transparent !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2) !important;
    }
    
    .stDataFrame th {
        background: rgba(212, 175, 55, 0.15) !important;
        color: #d4af37 !important;
        font-weight: 700 !important;
    }
    
    .stSidebar {
        background: rgba(10, 8, 23, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid rgba(212, 175, 55, 0.3) !important;
    }
    
    .stSidebar h3 {
        color: #d4af37 !important;
        font-size: 1.8rem !important;
    }
    
    .stRadio > div {
        background: rgba(28, 22, 45, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 25px !important;
        padding: 15px !important;
    }
    
    .stRadio label {
        font-family: 'Cairo', sans-serif !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 10px !important;
    }
    
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.8), transparent) !important;
        margin: 30px 0 !important;
    }
    
    .footer {
        background: linear-gradient(135deg, rgba(18, 14, 30, 0.95) 0%, rgba(10, 8, 23, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 40px;
        padding: 40px;
        margin-top: 50px;
        text-align: center;
    }
    
    .footer p {
        font-family: 'Cairo', sans-serif !important;
        color: white !important;
        font-size: 1.2rem !important;
    }
    
    .footer .gold {
        color: #d4af37 !important;
        font-weight: 700 !important;
    }
    
    .floating-gold {
        animation: floatGold 3s ease-in-out infinite;
    }
    
    @keyframes floatGold {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

image_path = r"WhatsApp Image 2026-02-11 at 3.32.24 PM.jpeg"
if os.path.exists(image_path):
    image_base64 = get_base64_of_image(image_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

lang = st.sidebar.radio("", ["🇬🇧 English", "🇸🇦 العربية"], index=0)

def _(en, ar):
    return en if lang == "🇬🇧 English" else ar

@st.cache_data
def load_data():
    files = {}
    try:
        files['main'] = pd.read_csv('fortune500_cleaned.csv')
    except:
        files['main'] = pd.DataFrame()
    try:
        files['pred2024'] = pd.read_csv('fortune500_2024_predictions.csv')
    except:
        files['pred2024'] = pd.DataFrame()
    try:
        files['models'] = pd.read_csv('fortune500_models_performance.csv')
    except:
        files['models'] = pd.DataFrame()
    try:
        files['test'] = pd.read_csv('fortune500_test_predictions.csv')
    except:
        files['test'] = pd.DataFrame()
    return files

data = load_data()
df = data['main']

if df.empty:
    st.error(_("Main data file not found!", "ملف البيانات الرئيسي غير موجود!"))
    st.stop()

df['profit_margin'] = (df['profit_mil'] / df['revenue_mil']) * 100
df['revenue_bil'] = df['revenue_mil'] / 1000
df['profit_bil'] = df['profit_mil'] / 1000

st.markdown(f"""
<div class="royal-header">
    <h1>{_('FORTUNE 500', 'فورتشن 500')}</h1>
    <p>{_('Executive Analytics Dashboard', 'لوحة التحليل التنفيذية')}</p>
    <div class="gold-badge floating-gold">
        <p>{_('1996 - 2024', '١٩٩٦ - ٢٠٢٤')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h3 style="color: #d4af37; font-size: 2rem; margin: 0;">⚜️</h3>
        <h3 style="color: #d4af37; font-family: 'Playfair Display', serif;">EXECUTIVE</h3>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        _("Select Analysis", "اختر التحليل"),
        [
            _("📅 Year Analysis", "📅 تحليل السنوات"),
            _("🏢 Company Analysis", "🏢 تحليل الشركات"),
            _("📈 Year Comparison", "📈 مقارنة السنوات"),
            _("🤖 Predictions", "🤖 التوقعات"),
            _("📋 Overview", "📋 نظرة عامة")
        ]
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: rgba(212,175,55,0.1); border-radius: 20px; border: 1px solid rgba(212,175,55,0.3);">
        <p style="color: #d4af37; margin: 0; font-family: 'Cairo', sans-serif;">{_('Developed by', 'تم التطوير بواسطة')}</p>
        <p style="color: white; font-size: 1.3rem; margin: 5px 0; font-family: 'Playfair Display', serif;">Mohammad Naser</p>
        <p style="color: #a0aec0; margin: 0;">⚜️ {_('Data Analyst', 'محلل بيانات')} ⚜️</p>
    </div>
    """, unsafe_allow_html=True)

if menu == _("📅 Year Analysis", "📅 تحليل السنوات"):
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header(_("📅 Year Analysis", "📅 تحليل السنوات"))
    
    col1, col2 = st.columns([3,1])
    with col1:
        year = st.selectbox(_("Select Year", "اختر السنة"), sorted(df['year'].unique(), reverse=True))
    with col2:
        top_n = st.number_input(_("Companies", "الشركات"), 5, 50, 15)
    
    df_year = df[df['year'] == year]
    
    if not df_year.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Companies', 'الشركات')}</label>
                <div>{len(df_year):,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Total Revenue', 'إجمالي الإيرادات')}</label>
                <div>${df_year['revenue_bil'].sum():,.1f}B</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Avg Revenue', 'متوسط الإيرادات')}</label>
                <div>${df_year['revenue_bil'].mean():,.1f}B</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Avg Margin', 'متوسط الهامش')}</label>
                <div>{df_year['profit_margin'].mean():.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        tabs = st.tabs([
            _("🏆 Top Companies", "🏆 أفضل الشركات"),
            _("📊 Distribution", "📊 التوزيع"),
            _("🏭 Industries", "🏭 الصناعات")
        ])
        
        with tabs[0]:
            top = df_year.nlargest(top_n, 'revenue_mil')
            fig = px.bar(top, x='revenue_bil', y='name', orientation='h',
                        title=f"{_('Top', 'أفضل')} {top_n} {_('Companies', 'شركة')} - {year}",
                        color='revenue_bil', color_continuous_scale='gray')
            fig.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white', size=12), title_font_color='#d4af37')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(top[['rank','name','revenue_bil','profit_bil','profit_margin','industry']],
                        use_container_width=True)
        
        with tabs[1]:
            fig = px.histogram(df_year, x='revenue_bil', nbins=50,
                              title=_("Revenue Distribution (Billions $)", "توزيع الإيرادات (بالمليارات)"))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            height=400, font=dict(color='white'), title_font_color='#d4af37')
            st.plotly_chart(fig, use_container_width=True)
        
        with tabs[2]:
            ind = df_year.groupby('industry').agg({
                'revenue_bil': 'sum',
                'profit_margin': 'mean'
            }).sort_values('revenue_bil', ascending=False).head(15)
            
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(ind.reset_index(), x='revenue_bil', y='industry', orientation='h',
                            title=_("Revenue by Industry (B$)", "الإيرادات حسب الصناعة"),
                            color='revenue_bil', color_continuous_scale='gray')
                fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 height=500, font=dict(color='white'), title_font_color='#d4af37')
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = px.bar(ind.reset_index(), x='profit_margin', y='industry', orientation='h',
                            title=_("Margin by Industry", "الهامش حسب الصناعة"),
                            color='profit_margin', color_continuous_scale='gray')
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 height=500, font=dict(color='white'), title_font_color='#d4af37')
                st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == _("🏢 Company Analysis", "🏢 تحليل الشركات"):
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header(_("🏢 Company Analysis", "🏢 تحليل الشركات"))
    
    company = st.selectbox(_("Select Company", "اختر الشركة"), sorted(df['name'].unique()))
    df_comp = df[df['name'] == company].sort_values('year')
    
    if not df_comp.empty:
        latest = df_comp.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Years in List', 'السنوات في القائمة')}</label>
                <div>{len(df_comp)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Latest Revenue', 'آخر إيرادات')}</label>
                <div>${latest['revenue_bil']:,.1f}B</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Latest Rank', 'آخر ترتيب')}</label>
                <div>#{int(latest['rank'])}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Latest Margin', 'آخر هامش')}</label>
                <div>{latest['profit_margin']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(df_comp, x='year', y='revenue_bil',
                          title=_("Revenue Trend (Billions $)", "اتجاه الإيرادات (بالمليارات)"),
                          markers=True)
            fig1.update_traces(line=dict(color='#d4af37', width=4),
                              marker=dict(color='#d4af37', size=10))
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                             height=400, font=dict(color='white'), title_font_color='#d4af37')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.line(df_comp, x='year', y='rank',
                          title=_("Rank Trend", "اتجاه الترتيب"),
                          markers=True)
            fig2.update_traces(line=dict(color='#a0aec0', width=4),
                              marker=dict(color='#a0aec0', size=10))
            fig2.update_yaxes(autorange="reversed")
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                             height=400, font=dict(color='white'), title_font_color='#d4af37')
            st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader(_("📋 Historical Data", "📋 البيانات التاريخية"))
        st.dataframe(df_comp[['year','rank','revenue_bil','profit_bil','profit_margin']],
                    use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == _("📈 Year Comparison", "📈 مقارنة السنوات"):
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header(_("📈 Year Comparison", "📈 مقارنة السنوات"))
    
    years = sorted(df['year'].unique(), reverse=True)
    col1, col2 = st.columns(2)
    with col1:
        y1 = st.selectbox(_("First Year", "السنة الأولى"), years, index=3)
    with col2:
        y2 = st.selectbox(_("Second Year", "السنة الثانية"), years, index=0)
    
    if y1 != y2:
        d1 = df[df['year'] == y1]
        d2 = df[df['year'] == y2]
        
        rev_growth = ((d2['revenue_bil'].sum() - d1['revenue_bil'].sum()) / d1['revenue_bil'].sum()) * 100
        avg_growth = ((d2['revenue_bil'].mean() - d1['revenue_bil'].mean()) / d1['revenue_bil'].mean()) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Revenue Growth', 'نمو الإيرادات')}</label>
                <div>{rev_growth:+.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Avg Growth', 'متوسط النمو')}</label>
                <div>{avg_growth:+.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-gold">
                <label>{_('Companies Change', 'تغير الشركات')}</label>
                <div>{len(d2)-len(d1):+d}</div>
            </div>
            """, unsafe_allow_html=True)
        
        comp = pd.DataFrame({
            _("Year", "السنة"): [str(y1), str(y2)],
            _("Total Revenue (B$)", "إجمالي الإيرادات"): [d1['revenue_bil'].sum(), d2['revenue_bil'].sum()],
            _("Avg Revenue (B$)", "متوسط الإيرادات"): [d1['revenue_bil'].mean(), d2['revenue_bil'].mean()],
            _("Companies", "الشركات"): [len(d1), len(d2)]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name=_("Total Revenue", "إجمالي الإيرادات"),
                            x=comp[_("Year", "السنة")], y=comp[_("Total Revenue (B$)", "إجمالي الإيرادات")],
                            marker_color='#d4af37'))
        fig.add_trace(go.Bar(name=_("Avg Revenue", "متوسط الإيرادات"),
                            x=comp[_("Year", "السنة")], y=comp[_("Avg Revenue (B$)", "متوسط الإيرادات")],
                            marker_color='#a0aec0'))
        fig.update_layout(barmode='group', height=400,
                         plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='white', size=12), title_font_color='#d4af37',
                         legend_font_color='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == _("🤖 Predictions", "🤖 التوقعات"):
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header(_("🤖 AI Predictions", "🤖 التوقعات الذكية"))
    
    if not data['pred2024'].empty:
        st.subheader(_("📊 2024 Predictions", "📊 توقعات 2024"))
        df_pred = data['pred2024']
        
        revenue_col = None
        name_col = None
        
        for col in df_pred.columns:
            col_lower = col.lower()
            if 'revenue' in col_lower or 'rev' in col_lower:
                revenue_col = col
            if 'name' in col_lower or 'company' in col_lower:
                name_col = col
        
        if revenue_col is None and len(df_pred.select_dtypes(include=[np.number]).columns) > 0:
            revenue_col = df_pred.select_dtypes(include=[np.number]).columns[0]
        
        if revenue_col and name_col:
            df_pred_sorted = df_pred.sort_values(revenue_col, ascending=False).head(20)
            fig = px.bar(df_pred_sorted, x=revenue_col, y=name_col, orientation='h',
                        title=_("Top 20 Predicted Companies 2024", "أفضل 20 شركة متوقعة 2024"),
                        color=revenue_col, color_continuous_scale='gray')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            height=500, font=dict(color='white'), title_font_color='#d4af37')
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_pred.head(50), use_container_width=True)
    else:
        st.info(_("2024 predictions file not available", "ملف توقعات 2024 غير متوفر"))
    
    if not data['models'].empty:
        st.subheader(_("📈 Model Performance", "📈 أداء النماذج"))
        df_models = data['models']
        st.dataframe(df_models, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header(_("📋 Data Overview", "📋 نظرة عامة"))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-gold">
            <label>{_('Total Years', 'إجمالي السنوات')}</label>
            <div>{df['year'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-gold">
            <label>{_('Unique Companies', 'الشركات الفريدة')}</label>
            <div>{df['name'].nunique():,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-gold">
            <label>{_('Total Revenue', 'إجمالي الإيرادات')}</label>
            <div>${df['revenue_bil'].sum()/1000:,.1f}T</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        avg_growth = df.groupby('year')['revenue_bil'].mean().pct_change().mean() * 100
        st.markdown(f"""
        <div class="metric-gold">
            <label>{_('Avg Growth', 'متوسط النمو')}</label>
            <div>{avg_growth:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    yearly = df.groupby('year').agg({
        'revenue_bil': 'mean',
        'profit_bil': 'mean',
        'profit_margin': 'mean'
    }).reset_index()
    
    fig = make_subplots(rows=3, cols=1,
                       subplot_titles=(
                           _("Average Revenue Trend (B$)", "اتجاه متوسط الإيرادات"),
                           _("Average Profit Trend (B$)", "اتجاه متوسط الأرباح"),
                           _("Average Margin Trend", "اتجاه متوسط الهامش")
                       ))
    
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['revenue_bil'],
                            name=_("Revenue","الإيرادات"), line=dict(color='#d4af37', width=4)), row=1, col=1)
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['profit_bil'],
                            name=_("Profit","الأرباح"), line=dict(color='#48BB78', width=4)), row=2, col=1)
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['profit_margin'],
                            name=_("Margin","الهامش"), line=dict(color='#ECC94B', width=4)), row=3, col=1)
    
    fig.update_layout(height=700, showlegend=True,
                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     font=dict(color='white', size=12), title_font_color='#d4af37',
                     legend_font_color='white')
    
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)', gridwidth=1)
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)', gridwidth=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    top = df.groupby('name')['revenue_bil'].max().nlargest(15)
    fig2 = px.bar(x=top.values, y=top.index, orientation='h',
                 title=_("Top 15 Companies All Time", "أفضل 15 شركة على الإطلاق"),
                 color=top.values, color_continuous_scale='gray')
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      height=500, font=dict(color='white', size=12), title_font_color='#d4af37')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    <p style="font-size: 2rem; margin-bottom: 20px;">👑</p>
    <p><span class="gold">{_('Fortune 500 Executive Analytics', 'فورتشن 500 للتحليل التنفيذي')}</span></p>
    <p style="margin-top: 20px;">{_('Developed by', 'تم التطوير بواسطة')} <span class="gold">Mohammad Naser</span></p>
    <p style="color: #a0aec0; margin-top: 10px;">⚜️ {_('Data Analyst', 'محلل بيانات')} ⚜️</p>
    <p style="color: #a0aec0; margin-top: 20px;">1996-{datetime.now().year}</p>
    <p style="color: #a0aec0; font-size: 0.9rem; margin-top: 30px;">© {_('All Rights Reserved', 'جميع الحقوق محفوظة')}</p>
</div>
""", unsafe_allow_html=True)
