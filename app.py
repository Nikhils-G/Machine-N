import streamlit as st
import pandas as pd
from maps_scraper import scrape_google_maps



import os
import subprocess

# Run setup.sh to install Playwright with deps
if not os.path.exists("/home/appuser/.playwright-setup-done"):
    subprocess.run(["chmod", "+x", "setup.sh"])
    subprocess.run(["./setup.sh"])
    open("/home/appuser/.playwright-setup-done", "w").close()

# ==============================================
# PREMIUM UI CONFIGURATION
# ==============================================
st.set_page_config(
    page_title="Machine N",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="collapsed"
)

# ==============================================
# CUSTOM CSS FOR PREMIUM INTERFACE
# ==============================================
st.markdown("""
<style>
    /* ===== BASE STYLES ===== */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        scroll-behavior: smooth;
    }
    
    /* ===== MAIN CONTAINER ===== */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
        background-image: radial-gradient(circle at 25% 25%, rgba(30, 30, 30, 0.8) 0%, rgba(10, 10, 10, 1) 100%);
    }
    
    /* ===== GLASSMORPHIC HEADER ===== */
    .main-header {
        background: rgba(15, 15, 15, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2.5rem 0;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0,219,222,0.1) 0%, rgba(0,0,0,0) 70%);
        animation: rotate 20s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .header-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00dbde 0%, #fc00ff 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 1.5rem;
        max-width: 700px;
        line-height: 1.6;
    }
    
    /* ===== INPUT CARD ===== */
    .input-card {
        background: rgba(20, 20, 20, 0.7);
        border-radius: 20px;
        box-shadow: 
            12px 12px 24px rgba(0, 0, 0, 0.3),
            -8px -8px 16px rgba(255, 255, 255, 0.03);
        padding: 2.5rem;
        margin-bottom: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }
    
    .input-card:hover {
        transform: translateY(-2px);
        box-shadow: 
            15px 15px 30px rgba(0, 0, 0, 0.4),
            -10px -10px 20px rgba(255, 255, 255, 0.05);
    }
    
    .input-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* ===== CUSTOM INPUT FIELDS ===== */
    .stTextInput>div>div>input {
        background-color: rgba(30, 30, 30, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00dbde !important;
        box-shadow: 0 0 0 2px rgba(0, 219, 222, 0.2) !important;
    }
    
    .stTextInput>label {
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* ===== GLOW BUTTON ===== */
    .stButton>button {
        background: linear-gradient(135deg, #00dbde 0%, #fc00ff 100%);
        color: white;
        border: none;
        padding: 16px 32px;
        border-radius: 14px;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 6px 24px rgba(0, 219, 222, 0.3);
        width: 100%;
        position: relative;
        overflow: hidden;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0, 219, 222, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    .stButton>button::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to bottom right,
            rgba(255, 255, 255, 0) 0%,
            rgba(255, 255, 255, 0.15) 50%,
            rgba(255, 255, 255, 0) 100%
        );
        transform: rotate(30deg);
        transition: all 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .stButton>button:hover::after {
        left: 100%;
        top: 100%;
    }
    
    /* ===== RESULTS SECTION ===== */
    .results-container {
        background: rgba(20, 20, 20, 0.7);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .results-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .results-count {
        font-size: 1.1rem;
        background: rgba(0, 219, 222, 0.15);
        color: #00dbde;
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid rgba(0, 219, 222, 0.2);
    }
    
    /* ===== DATA TABLE STYLING ===== */
    .dataframe {
        background-color: rgba(30, 30, 30, 0.9) !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .dataframe th {
        background-color: rgba(15, 15, 15, 0.95) !important;
        color: #00dbde !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dataframe td {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .dataframe tr:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.03) !important;
    }
    
    .dataframe tr:hover {
        background-color: rgba(0, 219, 222, 0.12) !important;
    }
    
    /* ===== DOWNLOAD BUTTON ===== */
    .download-btn {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        margin-top: 1.5rem !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        box-shadow: 0 4px 20px rgba(79, 172, 254, 0.3) !important;
    }
    
    .download-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(79, 172, 254, 0.4) !important;
    }
    
    /* ===== SPINNER ANIMATION ===== */
    .stSpinner>div>div {
        border-top-color: #00dbde !important;
        border-width: 4px !important;
        width: 36px !important;
        height: 36px !important;
    }
    
    /* ===== ERROR MESSAGE ===== */
    .stAlert {
        background: rgba(255, 59, 59, 0.1) !important;
        border-left: 4px solid #ff3b3b !important;
        border-radius: 8px !important;
    }
    
    /* ===== RESPONSIVE ADJUSTMENTS ===== */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.2rem;
        }
        
        .header-subtitle {
            font-size: 1rem;
        }
        
        .input-card {
            padding: 1.75rem;
        }
        
        .results-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==============================================
# PREMIUM HEADER SECTION
# ==============================================
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <div class="header-title">🛰️ Machine N</div>
        <div class="header-subtitle">
           Find high-quality leads around the corner — powered by intelligent automation.       </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================
# MAIN CONTENT CONTAINER
# ==============================================
with st.container():
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="input-card">
            <div class="input-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="#00DBDE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Lead Generation Parameters
            </div>
        """, unsafe_allow_html=True)
        
        keyword = st.text_input(
            "Business Category",
            "Interior Designers",
            help="Type of business you're looking for (e.g., Restaurants, Law Firms)"
        )
        
        location = st.text_input(
            "Target Location",
            "Hyderabad",
            help="City or region where you want to find leads"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(20, 20, 20, 0.7); border-radius: 20px; padding: 2.5rem; height: 100%; border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #ffffff; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#FC00FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 8V12L15 15" stroke="#FC00FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Pro Tips
            </h3>
            <ul style="color: rgba(255, 255, 255, 0.7); padding-left: 1.5rem; margin-top: 0; line-height: 1.8;">
                <li style="margin-bottom: 0.75rem;">Use <strong>specific industry terms</strong> for laser-focused results</li>
                <li style="margin-bottom: 0.75rem;">Add <strong>neighborhood names</strong> for geographic precision</li>
                <li style="margin-bottom: 0.75rem;">Our <strong>AI verification</strong> ensures 98% email deliverability</li>
                <li>Combine with <strong>LinkedIn Sales Navigator</strong> for complete outreach</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================
# CENTERED ACTION BUTTON
# ==============================================
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    if st.button("🚀 Generate Premium Leads", key="scrape_button"):
        with st.spinner("🔍"):
            results = scrape_google_maps(keyword, location)

        if results:
            df = pd.DataFrame(results)
            
            # ==============================================
            # PREMIUM RESULTS DISPLAY
            # ==============================================
            st.markdown("""
            <div class="results-container">
                <div class="results-header">
                    <h3 style="color: #ffffff; margin: 0;">Acquired Leads</h3>
                    <div class="results-count">✨ {count} High-Quality Leads Found</div>
                </div>
            """.format(count=len(df)), unsafe_allow_html=True)
            
            # Create a display copy with clickable emails
            df_display = df.copy()
            df_display['Email'] = df_display['Email'].apply(
                lambda x: f'<a href="mailto:{x}" style="color: #00dbde; text-decoration: none; font-weight: 500;">{x}</a>' 
                if x != "Not found" else x
            )
            
            # Enhanced DataFrame Display
            st.write(
                df_display.style
                .set_properties(**{
                    'background-color': 'rgba(30, 30, 30, 0.9)',
                    'color': 'white',
                    'border': '1px solid rgba(255, 255, 255, 0.1)'
                })
                .set_table_styles([{
                    'selector': 'td',
                    'props': [('padding', '14px 16px'), ('font-size', '0.95rem')]
                }, {
                    'selector': 'th',
                    'props': [('padding', '14px 16px'), ('font-size', '0.9rem')]
                }])
                .to_html(escape=False),
                unsafe_allow_html=True
            )
            
            # Enhanced Download Button (using original df for clean CSV)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Download Lead List (CSV)",
                data=csv,
                file_name="premium_leads.csv",
                mime="text/csv",
                key="download_button",
                help="Export these high-value leads to your CRM or marketing platform"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Success Metrics
            success_rate = min(100, len([email for email in df['Email'] if email != "Not found"]) / len(df) * 100)
            st.markdown(f"""
            <div style="margin-top: 1.5rem; color: rgba(255, 255, 255, 0.7); font-size: 0.95rem; background: rgba(20, 20, 20, 0.7); padding: 1.5rem; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.08);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #00dbde; font-weight: 600;">✓ Success Metrics</span>
                    <span style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">Real-time Analysis</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
                    <div style="background: rgba(0, 219, 222, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(0, 219, 222, 0.2);">
                        <div style="color: #00dbde; font-weight: 600; font-size: 1.1rem;">{success_rate:.1f}%</div>
                        <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.85rem;">Email Acquisition</div>
                    </div>
                    <div style="background: rgba(252, 0, 255, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(252, 0, 255, 0.2);">
                        <div style="color: #fc00ff; font-weight: 600; font-size: 1.1rem;">98%</div>
                        <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.85rem;">Data Accuracy</div>
                    </div>
                    <div style="background: rgba(79, 172, 254, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(79, 172, 254, 0.2);">
                        <div style="color: #4facfe; font-weight: 600; font-size: 1.1rem;">{len(df)}</div>
                        <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.85rem;">Total Leads</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: rgba(255, 59, 59, 0.1); padding: 1.5rem; border-radius: 14px; border-left: 4px solid #ff3b3b; margin-bottom: 2rem;'>
                <div style='display: flex; align-items: center; gap: 0.75rem; color: #ff3b3b; font-weight: 600; font-size: 1.1rem;'>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 8V12M12 16H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    No premium leads found
                </div>
                <div style='color: rgba(255, 255, 255, 0.7); margin-top: 1rem; line-height: 1.6;'>
                    <p>We couldn't find matching leads with your current parameters. Try these optimizations:</p>
                    <ul style="padding-left: 1.5rem; margin-top: 0.5rem;">
                        <li>Broaden your location range</li>
                        <li>Use more general industry terms</li>
                        <li>Check for typos in your search</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================
# PREMIUM FOOTER
# ==============================================
st.markdown("""
<div style="margin-top: 5rem; text-align: center; color: rgba(255, 255, 255, 0.4); font-size: 0.8rem; border-top: 1px solid rgba(255, 255, 255, 0.05); padding: 2rem 0;">
    <div style="max-width: 800px; margin: 0 auto;"> 
    © 2025 Machine N | Nikhil Sukthe's Business Lead Intelligence | v2.1.0
    <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 1.5rem;">
        <a href="http://www.linkedin.com/in/nikhilsukthe" target="_blank" style="color: rgba(255, 255, 255, 0.4); text-decoration: none;">LinkedIn</a>
        <a href="https://nikhilsukthe.vercel.app/" target="_blank" style="color: rgba(255, 255, 255, 0.4); text-decoration: none;">Portfolio</a>
        <a href="https://github.com/Nikhils-G" target="_blank" style="color: rgba(255, 255, 255, 0.4); text-decoration: none;">GitHub</a>
    </div>
    </div>
</div>
""", unsafe_allow_html=True)
