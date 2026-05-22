import os
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Can Care Be Automated?",
    layout="wide"
)

DATA_DIR = os.path.join("data", "processed")

CHART_CONFIG = {
    "displayModeBar": False,
    "responsive": True
}


@st.cache_data
def load_data():
    respondent = pd.read_csv(os.path.join(DATA_DIR, "caregiver_respondent_clean.csv"))
    heatmap = pd.read_csv(os.path.join(DATA_DIR, "care_responsibility_heatmap.csv"))
    reasons = pd.read_csv(os.path.join(DATA_DIR, "reason_bubble_summary.csv"))

    readiness_path = os.path.join(DATA_DIR, "readiness_summary.csv")
    consequence_path = os.path.join(DATA_DIR, "consequence_summary.csv")
    oversight_path = os.path.join(DATA_DIR, "oversight_summary.csv")

    readiness_summary = pd.read_csv(readiness_path) if os.path.exists(readiness_path) else pd.DataFrame()
    consequence_summary = pd.read_csv(consequence_path) if os.path.exists(consequence_path) else pd.DataFrame()
    oversight_summary = pd.read_csv(oversight_path) if os.path.exists(oversight_path) else pd.DataFrame()

    return respondent, heatmap, reasons, readiness_summary, consequence_summary, oversight_summary


respondent, heatmap, reasons, readiness_summary, consequence_summary, oversight_summary = load_data()


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 8% 6%, rgba(77,171,247,0.18), transparent 25%),
            radial-gradient(circle at 92% 4%, rgba(255,107,107,0.18), transparent 25%),
            radial-gradient(circle at 50% 70%, rgba(255,209,102,0.08), transparent 32%),
            #0f1117;
        color: #f7f7f8;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1320px;
    }

    h1, h2, h3 {
        letter-spacing: -0.04em;
    }

    section[data-testid="stSidebar"] {
        background-color: #0f1117;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .hero-card {
        padding: 38px 42px;
        border-radius: 34px;
        background:
            linear-gradient(135deg, rgba(21,24,33,0.96) 0%, rgba(36,40,58,0.96) 100%);
        border: 1px solid rgba(255,255,255,0.10);
        margin-bottom: 24px;
        box-shadow: 0 30px 70px rgba(0,0,0,0.28);
    }

    .eyebrow {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(77,171,247,0.12);
        border: 1px solid rgba(77,171,247,0.30);
        color: #74c0fc;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    .hero-title {
        font-size: 64px;
        font-weight: 900;
        line-height: 0.98;
        margin-bottom: 18px;
        color: #ffffff;
        max-width: 1050px;
    }

    .hero-subtitle {
        font-size: 19px;
        color: #d6d8df;
        max-width: 1080px;
        line-height: 1.68;
    }

    .hero-rule {
        height: 1px;
        width: 100%;
        background: linear-gradient(90deg, rgba(255,107,107,0.85), rgba(77,171,247,0.55), transparent);
        margin-top: 26px;
        margin-bottom: 2px;
    }

    .story-strip {
        padding: 18px 20px;
        border-radius: 22px;
        background: rgba(255,255,255,0.050);
        border: 1px solid rgba(255,255,255,0.09);
        margin-bottom: 22px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.16);
    }

    .story-strip-title {
        font-size: 14px;
        color: #ff8787;
        font-weight: 850;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .story-strip-text {
        font-size: 17px;
        color: #f2f2f2;
        line-height: 1.58;
    }

    .chapter-card {
        padding: 19px 19px;
        border-radius: 24px;
        background: rgba(255,255,255,0.052);
        border: 1px solid rgba(255,255,255,0.09);
        min-height: 164px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.15);
    }

    .chapter-number {
        color: #ff6b6b;
        font-weight: 900;
        font-size: 14px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .chapter-title {
        color: #ffffff;
        font-size: 21px;
        font-weight: 850;
        line-height: 1.15;
        margin-bottom: 10px;
    }

    .chapter-copy {
        color: #d6d8df;
        font-size: 14px;
        line-height: 1.48;
    }

    .section-wrap {
        padding-top: 36px;
        padding-bottom: 16px;
    }

    .section-kicker {
        color: #ff8787;
        font-size: 14px;
        font-weight: 850;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .section-title {
        color: #ffffff;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 1.05;
        margin-bottom: 12px;
    }

    .section-copy {
        color: #d6d8df;
        font-size: 17px;
        line-height: 1.62;
        max-width: 980px;
        margin-bottom: 18px;
    }

    .question-card {
        padding: 15px 17px;
        border-radius: 17px;
        background: rgba(77,171,247,0.085);
        border: 1px solid rgba(77,171,247,0.23);
        color: #e7f5ff;
        margin-top: 8px;
        margin-bottom: 18px;
        line-height: 1.55;
    }

    .side-panel {
        padding: 18px 20px;
        border-radius: 24px;
        background: rgba(255,255,255,0.052);
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 18px 45px rgba(0,0,0,0.14);
    }

    .side-panel-title {
        font-size: 14px;
        color: #ffd166;
        font-weight: 850;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .side-panel-copy {
        color: #d6d8df;
        font-size: 14px;
        line-height: 1.55;
    }

    .section-note {
        padding: 16px 18px;
        border-radius: 18px;
        background: rgba(255, 107, 107, 0.09);
        border: 1px solid rgba(255, 107, 107, 0.25);
        color: #f2f2f2;
        margin-top: 12px;
        margin-bottom: 18px;
        line-height: 1.55;
    }

    .insight-card {
        padding: 18px 20px;
        border-radius: 20px;
        background: rgba(255,255,255,0.052);
        border: 1px solid rgba(255,255,255,0.09);
        min-height: 120px;
        box-shadow: 0 16px 36px rgba(0,0,0,0.14);
    }

    .insight-number {
        font-size: 34px;
        font-weight: 850;
        color: #ff6b6b;
        margin-bottom: 4px;
    }

    .insight-label {
        font-size: 14px;
        color: #d8dae2;
        line-height: 1.38;
    }

    .readiness-card {
        padding: 22px 22px 20px 22px;
        border-radius: 24px;
        background:
            linear-gradient(145deg, rgba(255,255,255,0.065), rgba(255,255,255,0.025));
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 18px 42px rgba(0,0,0,0.16);
        min-height: 210px;
    }

    .readiness-topline {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 10px;
    }

    .readiness-stage {
        color: #ffffff;
        font-size: 18px;
        font-weight: 850;
        line-height: 1.15;
    }

    .readiness-number {
        font-size: 36px;
        font-weight: 900;
        line-height: 1;
    }

    .readiness-subtitle {
        color: #d6d8df;
        font-size: 14px;
        line-height: 1.42;
        min-height: 58px;
        margin-top: 10px;
        margin-bottom: 16px;
    }

    .readiness-track {
        width: 100%;
        height: 9px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        overflow: hidden;
        margin-top: 10px;
    }

    .readiness-fill {
        height: 100%;
        border-radius: 999px;
    }

    .readiness-delta {
        margin-top: 14px;
        color: #adb5bd;
        font-size: 13px;
        line-height: 1.35;
    }

    .overview-metric-card {
        background: rgba(255,255,255,0.052);
        border: 1px solid rgba(255,255,255,0.09);
        padding: 16px;
        border-radius: 18px;
        box-shadow: 0 14px 34px rgba(0,0,0,0.15);
    }

    .overview-metric-card {
        background: rgba(255,255,255,0.052);
        border: 1px solid rgba(255,255,255,0.09);
        padding: 16px;
        border-radius: 18px;
        box-shadow: 0 14px 34px rgba(0,0,0,0.15);
        transition:
            transform 180ms ease,
            box-shadow 180ms ease,
            border-color 180ms ease,
            background 180ms ease;
    }

    .overview-metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(116,192,252,0.28);
        background:
            radial-gradient(circle at 85% 25%, rgba(116,192,252,0.08), transparent 36%),
            rgba(255,255,255,0.066);
        box-shadow: 0 24px 60px rgba(0,0,0,0.24);
    }

    .overview-metric-label {
        color: #d6d8df;
        font-size: 14px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .overview-metric-value {
        font-size: 32px;
        line-height: 1;
        font-weight: 850;
    }

    .hero-card,
    .story-strip,
    .chapter-card,
    .readiness-card,
    .side-panel,
    .insight-card,
    .overview-metric-card {
        transition:
            transform 180ms ease,
            box-shadow 180ms ease,
            border-color 180ms ease,
            background 180ms ease,
            filter 180ms ease;
    }

    .hero-card:hover {
        transform: translateY(-4px);
        border-color: rgba(77,171,247,0.34);
        box-shadow: 0 36px 90px rgba(0,0,0,0.36);
        filter: saturate(1.05);
    }

    .story-strip:hover {
        transform: translateY(-3px);
        border-color: rgba(255,107,107,0.32);
        background: rgba(255,255,255,0.066);
        box-shadow: 0 24px 60px rgba(0,0,0,0.22);
    }

    .chapter-card:hover {
        transform: translateY(-5px) scale(1.015);
        border-color: rgba(77,171,247,0.42);
        background:
            radial-gradient(circle at 85% 20%, rgba(77,171,247,0.13), transparent 38%),
            rgba(255,255,255,0.072);
        box-shadow: 0 26px 70px rgba(0,0,0,0.26);
    }

    .chapter-card:hover .chapter-number {
        color: #74c0fc;
    }

    .chapter-card:hover .chapter-title {
        color: #ffffff;
    }

    .readiness-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255,209,102,0.34);
        background:
            radial-gradient(circle at 80% 10%, rgba(255,209,102,0.10), transparent 34%),
            linear-gradient(145deg, rgba(255,255,255,0.080), rgba(255,255,255,0.032));
        box-shadow: 0 26px 68px rgba(0,0,0,0.24);
    }

    .side-panel:hover,
    .insight-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255,255,255,0.18);
        background: rgba(255,255,255,0.068);
        box-shadow: 0 24px 60px rgba(0,0,0,0.22);
    }

    .overview-metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255,107,107,0.32);
        background:
            radial-gradient(circle at 85% 25%, rgba(255,107,107,0.10), transparent 36%),
            rgba(255,255,255,0.066);
        box-shadow: 0 24px 60px rgba(0,0,0,0.24);
    }


    html {
        scroll-behavior: smooth;
    }

    .jump-anchor {
        display: block;
        position: relative;
        top: -88px;
        visibility: hidden;
    }

    .chapter-link,
    .chapter-link:visited,
    .chapter-link:hover,
    .chapter-link:active {
        color: inherit;
        text-decoration: none;
        display: block;
    }

    .chapter-link .chapter-card {
        cursor: pointer;
        transition:
            transform 180ms ease,
            box-shadow 180ms ease,
            border-color 180ms ease,
            background 180ms ease;
    }

    .chapter-link:hover .chapter-card {
        transform: translateY(-5px) scale(1.015);
        border-color: rgba(77,171,247,0.42);
        background:
            radial-gradient(circle at 85% 20%, rgba(77,171,247,0.13), transparent 38%),
            rgba(255,255,255,0.072);
        box-shadow: 0 26px 70px rgba(0,0,0,0.26);
    }

    .chapter-link:hover .chapter-number {
        color: #74c0fc;
    }


    .chapter-link,
    .chapter-link:visited,
    .chapter-link:hover,
    .chapter-link:active {
        color: inherit !important;
        text-decoration: none !important;
        display: block;
    }

    .chapter-link * {
        text-decoration: none !important;
    }

    .chapter-number {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .chapter-link .chapter-number::after {
        content: "↗";
        font-size: 12px;
        line-height: 1;
        color: rgba(116,192,252,0.95);
        opacity: 0.72;
        transform: translateY(-1px);
        transition: transform 160ms ease, opacity 160ms ease;
    }

    .chapter-link:hover .chapter-number::after {
        opacity: 1;
        transform: translate(2px, -3px);
    }

    .chapter-link:hover .chapter-title {
        color: #ffffff;
    }

    .chapter-link:hover .chapter-copy {
        color: #e9ecef;
    }


    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 20% 0%, rgba(77,171,247,0.10), transparent 28%),
            #0f1117;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff;
    }

    .sidebar-panel {
        padding: 14px 14px;
        border-radius: 16px;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.085);
        margin-bottom: 14px;
    }

    .sidebar-kicker {
        color: #74c0fc;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .sidebar-title {
        color: #ffffff;
        font-size: 16px;
        font-weight: 850;
        margin-bottom: 6px;
    }

    .sidebar-copy {
        color: #adb5bd;
        font-size: 13px;
        line-height: 1.42;
        margin-bottom: 4px;
    }

    .sidebar-status {
        padding: 13px 14px;
        border-radius: 16px;
        background:
            linear-gradient(145deg, rgba(255,107,107,0.10), rgba(77,171,247,0.06));
        border: 1px solid rgba(255,255,255,0.09);
        color: #f2f2f2;
        font-size: 13px;
        line-height: 1.45;
        margin-top: 10px;
    }

    .sidebar-status b {
        color: #ff8787;
    }

    section[data-testid="stSidebar"] [data-testid="stSelectbox"] label,
    section[data-testid="stSidebar"] [data-testid="stSlider"] label,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
        color: #f1f3f5;
        font-weight: 750;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 8px;
    }

    section[data-testid="stSidebar"] details {
        border-radius: 14px;
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.075);
        padding: 4px 8px;
    }

    section[data-testid="stSidebar"] summary {
        color: #f8f9fa;
        font-weight: 800;
    }


    .inline-control-panel {
        padding: 18px 20px;
        border-radius: 20px;
        background:
            linear-gradient(145deg, rgba(255,255,255,0.060), rgba(255,255,255,0.026));
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 16px 40px rgba(0,0,0,0.14);
        margin-top: 12px;
        margin-bottom: 22px;
    }

    .inline-control-kicker {
        color: #74c0fc;
        font-size: 13px;
        font-weight: 850;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .inline-control-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: 900;
        letter-spacing: -0.03em;
        margin-bottom: 5px;
    }

    .inline-control-copy {
        color: #d6d8df;
        font-size: 14px;
        line-height: 1.45;
    }

    .inline-status {
        padding: 13px 15px;
        border-radius: 16px;
        background: rgba(255,107,107,0.085);
        border: 1px solid rgba(255,107,107,0.22);
        color: #f2f2f2;
        font-size: 14px;
        line-height: 1.45;
        margin-top: 6px;
    }

    .inline-status b {
        color: #ff8787;
    }


    .audience-toolbar {
        padding: 14px 16px;
        border-radius: 18px;
        background:
            linear-gradient(145deg, rgba(255,255,255,0.052), rgba(255,255,255,0.024));
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 14px 34px rgba(0,0,0,0.13);
        margin-top: 10px;
        margin-bottom: 14px;
    }

    .audience-kicker {
        color: #74c0fc;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 3px;
    }

    .audience-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 850;
        letter-spacing: -0.02em;
        margin-bottom: 2px;
    }

    .audience-copy {
        color: #adb5bd;
        font-size: 13px;
        line-height: 1.35;
    }

    .audience-status {
        padding: 11px 13px;
        border-radius: 15px;
        background: rgba(255,107,107,0.078);
        border: 1px solid rgba(255,107,107,0.20);
        color: #f2f2f2;
        font-size: 13px;
        line-height: 1.38;
        margin-top: 3px;
    }

    .audience-status b {
        color: #ff8787;
    }


    .interaction-hint {
        padding: 12px 15px;
        border-radius: 16px;
        background: rgba(77,171,247,0.075);
        border: 1px solid rgba(77,171,247,0.22);
        color: #dbeafe;
        font-size: 14px;
        line-height: 1.45;
        margin-top: -2px;
        margin-bottom: 18px;
    }

    .interaction-hint b {
        color: #74c0fc;
    }



    .hero-meta-row {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 12px;
        margin-bottom: 15px;
        flex-wrap: wrap;
    }

    .hero-meta-row .eyebrow {
        margin-bottom: 0 !important;
    }

    .author-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        min-height: 36px;
        box-sizing: border-box;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.050);
        border: 1px solid rgba(255,255,255,0.10);
        color: #dbeafe;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.02em;
        white-space: nowrap;
    }

    .author-badge span {
        color: #ffffff;
        font-weight: 900;
    }

    .argument-strip {
        margin-top: 14px;
        margin-bottom: 22px;
        padding: 18px 22px;
        border-radius: 18px;
        background:
            linear-gradient(90deg, rgba(255,107,107,0.060), rgba(77,171,247,0.035));
        border-left: 3px solid rgba(255,135,135,0.62);
        border-top: 1px solid rgba(255,255,255,0.08);
        border-right: 1px solid rgba(255,255,255,0.06);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 14px 34px rgba(0,0,0,0.14);
    }

    .argument-label {
        color: #ff8787;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .argument-text {
        color: #f2f2f2;
        font-size: 17px;
        line-height: 1.55;
        max-width: 1120px;
    }

    .overview-navigation-anchor {
        display: block;
        position: relative;
        top: -88px;
        visibility: hidden;
    }

    .chapter-return-tip {
        display: none;
        position: sticky;
        top: 12px;
        z-index: 50;
        margin: 0 0 16px 0;
        padding: 12px 14px;
        border-radius: 16px;
        background:
            linear-gradient(145deg, rgba(77,171,247,0.16), rgba(255,107,107,0.08));
        border: 1px solid rgba(116,192,252,0.32);
        box-shadow: 0 18px 44px rgba(0,0,0,0.22);
        backdrop-filter: blur(10px);
        color: #e7f5ff;
        font-size: 14px;
        line-height: 1.45;
    }

    .jump-anchor:target + .chapter-return-tip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 14px;
    }

    .chapter-return-message b {
        color: #74c0fc;
    }

    .chapter-return-link,
    .chapter-return-link:visited,
    .chapter-return-link:hover,
    .chapter-return-link:active {
        color: #ffffff !important;
        text-decoration: none !important;
        font-weight: 850;
        white-space: nowrap;
        padding: 7px 11px;
        border-radius: 999px;
        background: rgba(255,255,255,0.09);
        border: 1px solid rgba(255,255,255,0.14);
    }

    .chapter-return-link:hover {
        background: rgba(116,192,252,0.18);
        border-color: rgba(116,192,252,0.42);
    }

    .takeaway-card {
        margin-top: 32px;
        margin-bottom: 40px;
        padding: 28px 32px;
        border-radius: 24px;
        background:
            linear-gradient(135deg, rgba(29,33,44,0.96) 0%, rgba(31,35,45,0.96) 55%, rgba(45,33,38,0.94) 100%);
        border: 1px solid rgba(255,255,255,0.11);
        box-shadow: 0 28px 80px rgba(0,0,0,0.24);
    }

    .takeaway-kicker {
        color: #74c0fc;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .takeaway-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 900;
        line-height: 1.12;
        letter-spacing: -0.04em;
        margin-bottom: 12px;
    }

    .takeaway-copy {
        color: #e9ecef;
        font-size: 18px;
        line-height: 1.65;
        max-width: 1120px;
    }

    .takeaway-copy b {
        color: #ff8787;
    }


    /* Force Streamlit native controls to stay dark across light/dark/system theme */
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.065) !important;
        color: #f7f7f8 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] span {
        color: #f7f7f8 !important;
    }

    div[data-baseweb="popover"] {
        background-color: #171a23 !important;
        color: #f7f7f8 !important;
    }

    ul[role="listbox"] {
        background-color: #171a23 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }

    li[role="option"] {
        background-color: #171a23 !important;
        color: #f7f7f8 !important;
    }

    li[role="option"]:hover {
        background-color: rgba(77,171,247,0.18) !important;
        color: #ffffff !important;
    }

    div[data-testid="stRadio"] label {
        color: #f7f7f8 !important;
    }

    div[data-testid="stRadio"] p {
        color: #f7f7f8 !important;
    }

    div[data-testid="stCheckbox"] label {
        color: #f7f7f8 !important;
    }

    div[data-testid="stSlider"] label {
        color: #f7f7f8 !important;
    }

    label, .stSelectbox label {
        color: #d6d8df !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


def weighted_percentage(data, column, positive_values):
    if column not in data.columns:
        return None

    valid = data.dropna(subset=[column, "weight"]).copy()

    if valid.empty:
        return None

    mask = valid[column].astype(str).isin(positive_values)
    numerator = valid.loc[mask, "weight"].sum()
    denominator = valid["weight"].sum()

    if denominator == 0:
        return None

    return round((numerator / denominator) * 100, 1)


def weighted_distribution(data, column):
    if column not in data.columns or "weight" not in data.columns:
        return pd.DataFrame()

    valid = data.dropna(subset=[column, "weight"]).copy()

    if valid.empty:
        return pd.DataFrame()

    grouped = (
        valid
        .groupby(column, dropna=False, observed=False)["weight"]
        .sum()
        .reset_index()
        .rename(columns={column: "response", "weight": "weighted_count"})
    )

    total = grouped["weighted_count"].sum()

    if total == 0:
        return pd.DataFrame()

    grouped["percentage"] = grouped["weighted_count"] / total * 100
    return grouped


def find_existing_column(data, candidates):
    for col in candidates:
        if col in data.columns:
            return col
    return None


def add_attitude_columns(data):
    out = data.copy()

    out["realism_state"] = out["realistic"].astype(str).map({
        "Extremely realistic": "Realistic",
        "Somewhat realistic": "Realistic",
        "Not very realistic": "Not realistic",
        "Not at all realistic": "Not realistic",
    })

    out["enthusiasm_state"] = out["enthusiastic"].astype(str).map({
        "Very enthusiastic": "Enthusiastic",
        "Somewhat enthusiastic": "Enthusiastic",
        "Not too enthusiastic": "Not enthusiastic",
        "Not at all enthusiastic": "Not enthusiastic",
    })

    out["willing_state"] = out["willing_to_use"].astype(str).map({
        "Yes": "Would use",
        "No": "Would not use",
    })

    return out


def get_readiness_rows(data, readiness_fallback):
    heard_column = find_existing_column(
        data,
        ["heard_before", "heard", "heard_about", "heard_read_thought", "heard_robot_caregiver"]
    )

    if heard_column is not None:
        valid = data.dropna(subset=[heard_column, "weight"]).copy()
        heard_mask = valid[heard_column].astype(str).isin(["A lot", "A little"])
        denominator = valid["weight"].sum()
        heard_pct = round(valid.loc[heard_mask, "weight"].sum() / denominator * 100, 1) if denominator else None
    elif not readiness_fallback.empty and "stage" in readiness_fallback.columns:
        match = readiness_fallback[readiness_fallback["stage"].astype(str).str.contains("Heard", case=False, na=False)]
        heard_pct = float(match.iloc[0]["percentage"]) if not match.empty else None
    else:
        heard_pct = None

    rows = [
        {
            "stage": "Familiarity",
            "long_stage": "Heard at least a little",
            "percentage": heard_pct,
            "color": "#74c0fc",
            "description": "Many respondents had not heard much about robot caregivers.",
        },
        {
            "stage": "Realism",
            "long_stage": "See it as realistic",
            "percentage": weighted_percentage(
                data,
                "realistic",
                ["Extremely realistic", "Somewhat realistic"]
            ),
            "color": "#4dabf7",
            "description": "A majority still found the idea realistic or imaginable.",
        },
        {
            "stage": "Enthusiasm",
            "long_stage": "Feel enthusiastic",
            "percentage": weighted_percentage(
                data,
                "enthusiastic",
                ["Very enthusiastic", "Somewhat enthusiastic"]
            ),
            "color": "#ffd166",
            "description": "Emotional acceptance is weaker than perceived realism.",
        },
        {
            "stage": "Willingness",
            "long_stage": "Would use it",
            "percentage": weighted_percentage(
                data,
                "willing_to_use",
                ["Yes"]
            ),
            "color": "#51cf66",
            "description": "Personal adoption remains lower than cultural imagination.",
        },
    ]

    return pd.DataFrame(rows).dropna(subset=["percentage"]).reset_index(drop=True)


def render_readiness_snapshot(data, readiness_fallback):
    plot_df = get_readiness_rows(data, readiness_fallback)

    if plot_df.empty:
        st.warning("No readiness data available.")
        return plot_df

    cols = st.columns(4)

    for i, row in plot_df.iterrows():
        pct = float(row["percentage"])
        color = str(row["color"])

        stage = html.escape(str(row["stage"]))
        description = html.escape(str(row["description"]))

        if i == 0:
            delta_html = "Starting point of public imagination"
        else:
            previous = float(plot_df.iloc[i - 1]["percentage"])
            delta = pct - previous
            sign = "+" if delta >= 0 else ""
            delta_color = "#ffd166" if delta >= 0 else "#ff8787"
            delta_html = (
                f'Change from previous stage: '
                f'<span style="color:{delta_color}; font-weight:850;">'
                f'{sign}{delta:.1f} pts'
                f'</span>'
            )

        card_html = (
            f'<div class="readiness-card">'
            f'<div class="readiness-topline">'
            f'<div class="readiness-stage">{stage}</div>'
            f'<div class="readiness-number" style="color:{color};">{pct:.1f}%</div>'
            f'</div>'
            f'<div class="readiness-subtitle">{description}</div>'
            f'<div class="readiness-track">'
            f'<div class="readiness-fill" style="width:{pct}%; background:{color};"></div>'
            f'</div>'
            f'<div class="readiness-delta">{delta_html}</div>'
            f'</div>'
        )

        with cols[i]:
            st.markdown(card_html, unsafe_allow_html=True)

    return plot_df


def make_sankey(data):
    flow_df = add_attitude_columns(data)
    flow_df = flow_df.dropna(subset=[
        "realism_state",
        "enthusiasm_state",
        "willing_state",
        "weight"
    ])

    total_weight = flow_df["weight"].sum()

    labels = [
        "Realistic",
        "Not realistic",
        "Enthusiastic",
        "Not enthusiastic",
        "Would use",
        "Would not use",
    ]

    label_to_index = {label: idx for idx, label in enumerate(labels)}

    source = []
    target = []
    value = []
    hover_text = []
    link_stage = []

    first_links = (
        flow_df
        .groupby(["realism_state", "enthusiasm_state"], observed=False)["weight"]
        .sum()
        .reset_index()
    )

    second_links = (
        flow_df
        .groupby(["enthusiasm_state", "willing_state"], observed=False)["weight"]
        .sum()
        .reset_index()
    )

    for _, row in first_links.iterrows():
        share = row["weight"] / total_weight * 100
        source.append(label_to_index[row["realism_state"]])
        target.append(label_to_index[row["enthusiasm_state"]])
        value.append(share)
        hover_text.append(
            f"{row['realism_state']} to {row['enthusiasm_state']}<br>{share:.1f}% of respondents"
        )
        link_stage.append("realism")

    for _, row in second_links.iterrows():
        share = row["weight"] / total_weight * 100
        source.append(label_to_index[row["enthusiasm_state"]])
        target.append(label_to_index[row["willing_state"]])
        value.append(share)
        hover_text.append(
            f"{row['enthusiasm_state']} to {row['willing_state']}<br>{share:.1f}% of respondents"
        )
        link_stage.append("enthusiasm")

    node_colors = [
        "#4dabf7",
        "#868e96",
        "#ffd166",
        "#868e96",
        "#51cf66",
        "#ff6b6b",
    ]

    link_colors = []

    for stage, text in zip(link_stage, hover_text):
        if stage == "realism":
            if "Not realistic" in text:
                link_colors.append("rgba(134,142,150,0.34)")
            else:
                link_colors.append("rgba(77,171,247,0.44)")
        else:
            if "Would not use" in text:
                link_colors.append("rgba(255,107,107,0.34)")
            else:
                link_colors.append("rgba(255,209,102,0.42)")

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="fixed",
                node=dict(
                    pad=24,
                    thickness=28,
                    line=dict(color="rgba(255,255,255,0.38)", width=0.8),
                    label=labels,
                    color=node_colors,
                    x=[0.02, 0.02, 0.50, 0.50, 0.96, 0.96],
                    y=[0.23, 0.73, 0.27, 0.72, 0.30, 0.75],
                    hovertemplate="<b>%{label}</b><extra></extra>"
                ),
                link=dict(
                    source=source,
                    target=target,
                    value=value,
                    color=link_colors,
                    customdata=hover_text,
                    hovertemplate="%{customdata}<extra></extra>"
                )
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="From Realism to Adoption: How Public Acceptance Breaks Down",
            font=dict(size=23, color="#f2f2f2")
        ),
        font=dict(size=16, color="#f2f2f2"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=650,
        margin=dict(l=15, r=15, t=92, b=28),
        annotations=[
            dict(
                x=0.02,
                y=1.08,
                xref="paper",
                yref="paper",
                text="1. Perceived realism",
                showarrow=False,
                font=dict(size=13, color="#adb5bd")
            ),
            dict(
                x=0.50,
                y=1.08,
                xref="paper",
                yref="paper",
                text="2. Emotional reaction",
                showarrow=False,
                font=dict(size=13, color="#adb5bd")
            ),
            dict(
                x=0.96,
                y=1.08,
                xref="paper",
                yref="paper",
                text="3. Adoption intent",
                showarrow=False,
                font=dict(size=13, color="#adb5bd")
            )
        ]
    )

    return fig


def remove_low_value_reasons(data):
    cleaned = data.copy()

    cleaned["reason_clean"] = cleaned["reason"].astype(str).str.lower().str.strip()

    remove_patterns = [
        "refused",
        "no answer",
        "other",
        "don't know",
        "do not know",
        "dk",
        "nan"
    ]

    for pattern in remove_patterns:
        cleaned = cleaned[~cleaned["reason_clean"].str.contains(pattern, na=False)]

    cleaned = cleaned.drop(columns=["reason_clean"])
    return cleaned


def make_reason_treemap(data, stance_choice, top_n):
    chart_data = data[data["percentage"] > 0].copy()
    chart_data = remove_low_value_reasons(chart_data)

    if stance_choice != "Both":
        chart_data = chart_data[chart_data["stance"] == stance_choice]

    if chart_data.empty:
        return None, chart_data

    chart_data = (
        chart_data
        .sort_values(["stance", "percentage"], ascending=[True, False])
        .groupby("stance", group_keys=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    darker_color_map = {
        "Would use": "#3F9EE8",
        "Would not use": "#D95B63"
    }

    labels = []
    parents = []
    ids = []
    values = []
    colors = []
    text_labels = []
    customdata = []

    stance_order = ["Would not use", "Would use"]

    for stance in stance_order:
        stance_df = chart_data[chart_data["stance"] == stance].copy()

        if stance_df.empty:
            continue

        stance_total = stance_df["weighted_count"].sum()
        stance_id = stance

        labels.append(stance)
        parents.append("")
        ids.append(stance_id)
        values.append(stance_total)
        colors.append(darker_color_map.get(stance, "#ADB5BD"))
        text_labels.append(f"<b>{stance}</b>")
        customdata.append([stance, stance, 100.0, stance_total])

        for _, row in stance_df.iterrows():
            reason = str(row["reason"])
            pct = float(row["percentage"])
            count = float(row["weighted_count"])
            node_id = f"{stance}-{reason}"

            labels.append(reason)
            parents.append(stance_id)
            ids.append(node_id)
            values.append(count)
            colors.append(darker_color_map.get(stance, "#ADB5BD"))

            if pct >= 3:
                display_text = f"<b>{reason}</b><br>{pct:.1f}%"
            else:
                display_text = ""

            text_labels.append(display_text)
            customdata.append([reason, stance, pct, count])

    fig = go.Figure(
        go.Treemap(
            labels=labels,
            parents=parents,
            ids=ids,
            values=values,
            branchvalues="total",
            marker=dict(
                colors=colors,
                line=dict(
                    color="rgba(255,255,255,0.34)",
                    width=1.2
                )
            ),
            text=text_labels,
            texttemplate="%{text}",
            textfont=dict(
                size=15,
                color="#FFFFFF"
            ),
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Group: %{customdata[1]}<br>"
                "Share within group: %{customdata[2]:.1f}%<br>"
                "Weighted mention count: %{customdata[3]:.1f}"
                "<extra></extra>"
            ),
            tiling=dict(
                packing="squarify",
                pad=3
            )
        )
    )

    fig.update_layout(
        title=dict(
            text="Reason Value Map",
            font=dict(size=24, color="#F2F2F2")
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=640,
        margin=dict(l=0, r=0, t=70, b=8),
        font=dict(
            color="#F2F2F2",
            size=14
        ),
        hoverlabel=dict(
            bgcolor="#202435",
            bordercolor="#D95B63",
            font_size=14,
            font_color="#FFFFFF"
        )
    )

    return fig, chart_data


def make_consequence_mirror(data):
    if data.empty:
        return None

    plot_df = data.copy()

    category_map = {
        "Benefit": "Promise",
        "Concern": "Anxiety",
        "Ambivalent": "Ambivalent"
    }

    plot_df["category_clean"] = plot_df["category"].map(category_map).fillna(plot_df["category"])

    plot_df["signed_percentage"] = plot_df.apply(
        lambda row: -row["percentage_likely"] if row["category_clean"] == "Anxiety" else row["percentage_likely"],
        axis=1
    )

    category_order = {
        "Anxiety": 0,
        "Ambivalent": 1,
        "Promise": 2
    }

    plot_df["category_order"] = plot_df["category_clean"].map(category_order).fillna(3)
    plot_df = plot_df.sort_values(["category_order", "signed_percentage"])

    color_map = {
        "Promise": "#51cf66",
        "Anxiety": "#ff6b6b",
        "Ambivalent": "#ffd166"
    }

    fig = go.Figure()

    for _, row in plot_df.iterrows():
        color = color_map.get(row["category_clean"], "#adb5bd")

        fig.add_trace(
            go.Scatter(
                x=[0, row["signed_percentage"]],
                y=[row["label"], row["label"]],
                mode="lines",
                line=dict(
                    color="rgba(255,255,255,0.18)",
                    width=5
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[row["signed_percentage"]],
                y=[row["label"]],
                mode="markers+text",
                marker=dict(
                    size=24,
                    color=color,
                    line=dict(
                        color="rgba(255,255,255,0.85)",
                        width=1.8
                    )
                ),
                text=[f"{row['percentage_likely']:.1f}%"],
                textposition="middle right" if row["signed_percentage"] >= 0 else "middle left",
                textfont=dict(
                    size=14,
                    color="#f2f2f2"
                ),
                customdata=[[row["label"], row["category_clean"], row["percentage_likely"], row["full_question"]]],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Reading: %{customdata[1]}<br>"
                    "Likely: %{customdata[2]:.1f}%<br>"
                    "%{customdata[3]}"
                    "<extra></extra>"
                ),
                cliponaxis=False,
                showlegend=False
            )
        )

    fig.add_vline(
        x=0,
        line_width=2,
        line_color="rgba(255,255,255,0.45)"
    )

    fig.add_annotation(
        x=-62,
        y=1.10,
        xref="x",
        yref="paper",
        text="Anxiety",
        showarrow=False,
        font=dict(
            size=15,
            color="#ff8787"
        )
    )

    fig.add_annotation(
        x=0,
        y=1.10,
        xref="x",
        yref="paper",
        text="Ambivalent",
        showarrow=False,
        font=dict(
            size=15,
            color="#ffd166"
        )
    )

    fig.add_annotation(
        x=66,
        y=1.10,
        xref="x",
        yref="paper",
        text="Promise",
        showarrow=False,
        font=dict(
            size=15,
            color="#69db7c"
        )
    )

    fig.update_layout(
        title=dict(
            text="Promise and Anxiety Map",
            font=dict(size=24, color="#f2f2f2")
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=560,
        showlegend=False,
        margin=dict(l=20, r=120, t=90, b=55),
        font=dict(color="#f2f2f2", size=14),
        xaxis=dict(
            title="Share saying this is likely",
            range=[-78, 86],
            tickvals=[-60, -40, -20, 0, 20, 40, 60, 80],
            ticktext=["60%", "40%", "20%", "0%", "20%", "40%", "60%", "80%"],
            gridcolor="rgba(255,255,255,0.10)",
            zeroline=False
        ),
        yaxis=dict(
            title="",
            gridcolor="rgba(255,255,255,0.045)",
            automargin=True
        ),
        hoverlabel=dict(
            bgcolor="#202435",
            bordercolor="#ff6b6b",
            font_color="#ffffff",
            font_size=14
        )
    )

    return fig


def make_oversight_triangle(data, oversight_fallback, include_refused):
    camera_col = find_existing_column(
        data,
        ["camera_human_operator", "camera_operator", "human_operator_camera", "camera_monitoring"]
    )

    if camera_col is not None:
        plot_df = weighted_distribution(data, camera_col)
    elif not oversight_fallback.empty:
        plot_df = oversight_fallback.copy()
    else:
        plot_df = pd.DataFrame()

    if plot_df.empty:
        return None, pd.DataFrame()

    if "variable" in plot_df.columns:
        plot_df = plot_df[
            plot_df["variable"].astype(str).str.contains("camera", case=False, na=False)
        ].copy()

    if not include_refused:
        plot_df = plot_df[
            ~plot_df["response"].astype(str).str.lower().str.contains("refused|no answer", na=False)
        ].copy()

    def get_pct(label):
        match = plot_df[plot_df["response"].astype(str) == label]
        return float(match.iloc[0]["percentage"]) if not match.empty else 0.0

    better = get_pct("Better")
    no_diff = get_pct("No difference")
    worse = get_pct("Worse")

    total = better + no_diff + worse

    if total == 0:
        return None, plot_df

    better_norm = better / total * 100
    no_diff_norm = no_diff / total * 100
    worse_norm = worse / total * 100
    net_comfort = better - worse
    point_color = "#FFD166" if net_comfort >= 0 else "#FF6B6B"

    fig = go.Figure()

    fig.add_trace(
        go.Scatterternary(
            a=[better_norm],
            b=[no_diff_norm],
            c=[worse_norm],
            mode="markers+text",
            text=[f"Net comfort<br>{net_comfort:+.1f} pts"],
            textposition="bottom center",
            marker=dict(
                size=38,
                color=point_color,
                line=dict(
                    color="rgba(255,255,255,0.92)",
                    width=2
                )
            ),
            customdata=[[better, no_diff, worse, net_comfort]],
            hovertemplate=(
                "<b>Oversight response composition</b><br>"
                "Better: %{customdata[0]:.1f}%<br>"
                "No difference: %{customdata[1]:.1f}%<br>"
                "Worse: %{customdata[2]:.1f}%<br>"
                "Net comfort: %{customdata[3]:+.1f} points"
                "<extra></extra>"
            ),
            showlegend=False
        )
    )

    fig.update_layout(
        title=dict(
            text="Comfort Control Triangle",
            font=dict(size=24, color="#F2F2F2")
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=560,
        margin=dict(l=10, r=10, t=85, b=20),
        font=dict(color="#F2F2F2", size=14),
        ternary=dict(
            sum=100,
            bgcolor="rgba(0,0,0,0)",
            aaxis=dict(
                title=dict(text="Better"),
                min=0,
                linewidth=2,
                linecolor="rgba(81,207,102,0.70)",
                gridcolor="rgba(255,255,255,0.10)",
                showticklabels=False,
                ticks=""
            ),
            baxis=dict(
                title=dict(text="No difference"),
                min=0,
                linewidth=2,
                linecolor="rgba(173,181,189,0.70)",
                gridcolor="rgba(255,255,255,0.10)",
                showticklabels=False,
                ticks=""
            ),
            caxis=dict(
                title=dict(text="Worse"),
                min=0,
                linewidth=2,
                linecolor="rgba(255,107,107,0.70)",
                gridcolor="rgba(255,255,255,0.10)",
                showticklabels=False,
                ticks=""
            )
        ),
        hoverlabel=dict(
            bgcolor="#202435",
            bordercolor="#FFD166",
            font_color="#FFFFFF",
            font_size=14
        )
    )

    return fig, plot_df


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-meta-row">
            <div class="eyebrow">DIGS 30004 Final Dashboard</div>
            <div class="author-badge">Author: <span>Yue Jin</span></div>
        </div>
        <div class="hero-title">Can Care Be Automated?</div>
        <div class="hero-subtitle">
            A data story about how American adults imagined robot caregivers. The dashboard treats public opinion
            not as a simple yes or no answer, but as a movement between readiness, realism, enthusiasm,
            family responsibility, social consequences, human values, and oversight.
        </div>
        <div class="hero-rule"></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="audience-toolbar">
    <div class="audience-kicker">Audience filter</div>
    <div class="audience-title">Select respondent group</div>
    <div class="audience-copy">
        Updates the overview, readiness, pathway, and oversight views.
    </div>
</div>
    """,
    unsafe_allow_html=True
)

care_options = ["All respondents"] + [
    x for x in respondent["care_responsibility"].dropna().astype(str).unique().tolist()
]

preferred_order = [
    "All respondents",
    "I am already doing this",
    "Very likely",
    "Somewhat likely",
    "Not too likely",
    "Not at all likely",
]

care_options = [x for x in preferred_order if x in care_options] + [
    x for x in care_options if x not in preferred_order
]

control_left, control_right = st.columns([0.36, 0.64])

with control_left:
    selected_group = st.selectbox(
        "Respondent group",
        care_options,
        label_visibility="collapsed",
        help="Filter the overview metrics, readiness cards, pathway chart, and oversight chart."
    )

with control_right:
    st.markdown(
        f"""
<div class="audience-status">
    <b>Current audience:</b> {selected_group} &nbsp; | &nbsp;
    Comparative chapters keep all groups visible where needed.
</div>
        """,
        unsafe_allow_html=True
    )

if selected_group == "All respondents":
    filtered_respondent = respondent.copy()
else:
    filtered_respondent = respondent[
        respondent["care_responsibility"].astype(str) == selected_group
    ].copy()

metric_realistic = weighted_percentage(
    filtered_respondent,
    "realistic",
    ["Extremely realistic", "Somewhat realistic"]
)

metric_enthusiastic = weighted_percentage(
    filtered_respondent,
    "enthusiastic",
    ["Very enthusiastic", "Somewhat enthusiastic"]
)

metric_worried = weighted_percentage(
    filtered_respondent,
    "worried",
    ["Very worried", "Somewhat worried"]
)

metric_would_use = weighted_percentage(
    filtered_respondent,
    "willing_to_use",
    ["Yes"]
)

overview_metrics = [
    ("Realistic", metric_realistic, "#4dabf7"),
    ("Enthusiastic", metric_enthusiastic, "#ffd166"),
    ("Worried", metric_worried, "#ff6b6b"),
    ("Would use", metric_would_use, "#51cf66"),
]

metric_cols = st.columns(4)

for col, (label, value, color) in zip(metric_cols, overview_metrics):
    with col:
        st.markdown(
            f"""
            <div class="overview-metric-card">
                <div class="overview-metric-label">{label}</div>
                <div class="overview-metric-value" style="color:{color};">{value}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <div class="argument-strip">
        <div class="argument-label">Central argument</div>
        <div class="argument-text">
            Robot caregivers are judged not only as machines, but as possible substitutes for human care,
            family responsibility, emotional presence, independence, isolation, and human oversight.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div id="overview-navigation" class="overview-navigation-anchor"></div>', unsafe_allow_html=True)

chapter_1, chapter_2, chapter_3, chapter_4, chapter_5, chapter_6 = st.columns(6)

with chapter_1:
    st.markdown(
        """
        <a href="#chapter-01" class="chapter-link">
        <div class="chapter-card">
            <div class="chapter-number">Chapter 01</div>
            <div class="chapter-title">Readiness</div>
            <div class="chapter-copy">
                Can the public imagine robot care as realistic or usable?
            </div>
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with chapter_2:
    st.markdown(
        """
        <a href="#chapter-02" class="chapter-link">
        <div class="chapter-card">
            <div class="chapter-number">Chapter 02</div>
            <div class="chapter-title">Pathway</div>
            <div class="chapter-copy">
                Does realism become enthusiasm and willingness?
            </div>
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with chapter_3:
    st.markdown(
        """
        <a href="#chapter-03" class="chapter-link">
        <div class="chapter-card">
            <div class="chapter-number">Chapter 03</div>
            <div class="chapter-title">Context</div>
            <div class="chapter-copy">
                Does caregiving responsibility change attitudes?
            </div>
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with chapter_4:
    st.markdown(
        """
        <a href="#chapter-04" class="chapter-link">
        <div class="chapter-card">
            <div class="chapter-number">Chapter 04</div>
            <div class="chapter-title">Consequences</div>
            <div class="chapter-copy">
                Does robot care feel like promise or anxiety?
            </div>
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with chapter_5:
    st.markdown(
        """
        <a href="#chapter-05" class="chapter-link">
        <div class="chapter-card">
            <div class="chapter-number">Chapter 05</div>
            <div class="chapter-title">Reasons</div>
            <div class="chapter-copy">
                What values drive acceptance and refusal?
            </div>
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with chapter_6:
    st.markdown(
        """
        <a href="#chapter-06" class="chapter-link">
        <div class="chapter-card">
            <div class="chapter-number">Chapter 06</div>
            <div class="chapter-title">Oversight</div>
            <div class="chapter-copy">
                Does monitoring create comfort or control?
            </div>
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-wrap">
        <div id="chapter-01" class="jump-anchor"></div>
        <div class="chapter-return-tip" id="return-tip-chapter-01"><div class="chapter-return-message">You are viewing <b>Chapter 01: Readiness</b>. Return to the chapter menu to choose another section.</div><a href="#overview-navigation" class="chapter-return-link">Back to chapter menu ↑</a></div>
        <div class="section-kicker">Chapter 01</div>
        <div class="section-title">Public readiness starts unevenly</div>
        <div class="section-copy">
            The first view establishes the baseline. Instead of showing another dot chart, it summarizes four
            thresholds of public readiness: familiarity, realism, enthusiasm, and personal willingness.
        </div>
        <div class="question-card">
            <b>Question:</b> Where does public imagination expand, and where does it contract?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
<div class="interaction-hint">
    <b>How to explore:</b> Change the audience filter above to see how these readiness thresholds shift.
    Current audience: <b>{selected_group}</b>.
</div>
    """,
    unsafe_allow_html=True
)

readiness_view = render_readiness_snapshot(filtered_respondent, readiness_summary)

st.markdown(
    """
    <div class="section-note">
        <b>Interpretation:</b> Readiness is uneven. Robot caregivers may be culturally imaginable even before many people
        have heard much about them. The gap between realism and willingness is where the social and emotional question begins.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-wrap">
        <div id="chapter-02" class="jump-anchor"></div>
        <div class="chapter-return-tip" id="return-tip-chapter-02"><div class="chapter-return-message">You are viewing <b>Chapter 02: Pathway</b>. Return to the chapter menu to choose another section.</div><a href="#overview-navigation" class="chapter-return-link">Back to chapter menu ↑</a></div>
        <div class="section-kicker">Chapter 02</div>
        <div class="section-title">Acceptance is a pathway, not a single opinion</div>
        <div class="section-copy">
            Seeing robot care as realistic does not automatically make people enthusiastic,
            and enthusiasm does not automatically become willingness to use it.
        </div>
        <div class="question-card">
            <b>Question:</b> Does seeing robot care as realistic actually translate into willingness to use it?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

left, right = st.columns([0.28, 0.72])

with left:
    st.markdown(
        """
        <div class="side-panel">
            <div class="side-panel-title">How to read this</div>
            <div class="side-panel-copy">
                Follow the flow from left to right. The first stage captures whether the scenario feels realistic.
                The second stage captures emotional reaction. The final stage captures whether the respondent would use it.
                <br><br>
                This should be read as a cross-tabulated attitude pathway, not as a causal or temporal process.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        f"""
<div class="interaction-hint">
    <b>How to explore:</b> Hover over each flow to inspect the weighted share.
    Change the audience filter above to compare pathways across respondent groups.
    Current audience: <b>{selected_group}</b>.
</div>
        """,
        unsafe_allow_html=True
    )

    fig_sankey = make_sankey(filtered_respondent)
    st.plotly_chart(fig_sankey, use_container_width=True, config=CHART_CONFIG)

st.markdown(
    """
    <div class="section-note">
        <b>Interpretation:</b> Public acceptance is not a single yes or no response.
        The pathway shows that robot caregivers may be imaginable without being emotionally accepted or personally desired.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-wrap">
        <div id="chapter-03" class="jump-anchor"></div>
        <div class="chapter-return-tip" id="return-tip-chapter-03"><div class="chapter-return-message">You are viewing <b>Chapter 03: Context</b>. Return to the chapter menu to choose another section.</div><a href="#overview-navigation" class="chapter-return-link">Back to chapter menu ↑</a></div>
        <div class="section-kicker">Chapter 03</div>
        <div class="section-title">Care responsibility changes the meaning of robot care</div>
        <div class="section-copy">
            Averages hide important differences. The matrix compares robot caregiver attitudes across people
            who already care for family members, people who expect to care, and people who do not expect to care.
        </div>
        <div class="question-card">
            <b>Question:</b> Do people closer to family caregiving imagine robot caregivers differently?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

metric_short_names = {
    "Heard at least a little": "Heard",
    "Realistic": "Realistic",
    "Enthusiastic": "Enthusiastic",
    "Worried": "Worried",
    "Would use": "Would use",
    "Camera feels better": "Camera better",
    "More independent": "Independent",
    "More isolated": "Isolated",
}

metric_order = [
    "Heard",
    "Realistic",
    "Enthusiastic",
    "Worried",
    "Would use",
    "Camera better",
    "Independent",
    "Isolated",
]

care_order = [
    "I am already doing this",
    "Very likely",
    "Somewhat likely",
    "Not too likely",
    "Not at all likely",
]

heatmap_view = heatmap.copy()
heatmap_view["metric_short"] = heatmap_view["metric"].map(metric_short_names)
heatmap_view = heatmap_view.dropna(subset=["metric_short"])

heatmap_view["metric_short"] = pd.Categorical(
    heatmap_view["metric_short"],
    categories=metric_order,
    ordered=True
)

heatmap_view["care_responsibility"] = pd.Categorical(
    heatmap_view["care_responsibility"],
    categories=care_order,
    ordered=True
)

st.markdown(
    f"""
<div class="interaction-hint">
    <b>How to explore:</b> Hover over each cell to inspect the weighted percentage.
    Use the focus selector to isolate one attitude measure across caregiving responsibility groups.
</div>
    """,
    unsafe_allow_html=True
)

focus_metric = st.selectbox(
    "Focus attitude measure",
    ["All measures"] + metric_order,
    index=0,
    help="Choose one attitude measure to focus the matrix, or keep all measures visible."
)

if focus_metric != "All measures":
    heatmap_view = heatmap_view[heatmap_view["metric_short"] == focus_metric]

heatmap_pivot = heatmap_view.pivot(
    index="care_responsibility",
    columns="metric_short",
    values="percentage"
)

fig_heatmap = px.imshow(
    heatmap_pivot,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale=[
        "#151821",
        "#283149",
        "#4dabf7",
        "#ffd166",
        "#ff6b6b"
    ],
    labels=dict(
        x="Attitude measure",
        y="Caregiving responsibility",
        color="Share"
    ),
    title="Care Responsibility Matrix" if focus_metric == "All measures" else f"Care Responsibility Matrix: {focus_metric}"
)

fig_heatmap.update_traces(
    xgap=4,
    ygap=4,
    textfont=dict(size=14, color="#f4f4f5"),
    hovertemplate=(
        "<b>%{y}</b><br>"
        "%{x}: %{z:.1f}% of respondents"
        "<extra></extra>"
    )
)

fig_heatmap.update_layout(
    height=610,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(size=14, color="#f2f2f2"),
    title=dict(
        text="Care Responsibility Matrix",
        font=dict(size=22, color="#f2f2f2")
    ),
    margin=dict(l=20, r=40, t=80, b=80),
    xaxis=dict(
        side="bottom",
        title="Attitude measure",
        tickfont=dict(size=13)
    ),
    yaxis=dict(
        title="Caregiving responsibility",
        tickfont=dict(size=13)
    ),
    coloraxis_colorbar=dict(
        title="Share",
        ticksuffix="%",
        thickness=16,
        len=0.72
    )
)

left, right = st.columns([0.22, 0.78])

with left:
    st.markdown(
        """
        <div class="side-panel">
            <div class="side-panel-title">Design logic</div>
            <div class="side-panel-copy">
                Each cell is a weighted percentage. Rows represent the respondent's relationship to family caregiving.
                Columns represent attitude measures.
                <br><br>
                This turns the survey into a compact comparison matrix instead of a single average.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.plotly_chart(fig_heatmap, use_container_width=True, config=CHART_CONFIG)

st.markdown(
    """
    <div class="section-note">
        <b>Interpretation:</b> The matrix makes the project more than a topline summary.
        It shows how the social position of the respondent changes the way robot care is imagined.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-wrap">
        <div id="chapter-04" class="jump-anchor"></div>
        <div class="chapter-return-tip" id="return-tip-chapter-04"><div class="chapter-return-message">You are viewing <b>Chapter 04: Consequences</b>. Return to the chapter menu to choose another section.</div><a href="#overview-navigation" class="chapter-return-link">Back to chapter menu ↑</a></div>
        <div class="section-kicker">Chapter 04</div>
        <div class="section-title">Robot care is imagined as both promise and anxiety</div>
        <div class="section-copy">
            The consequence mirror uses closed-ended consequence questions. It separates imagined benefits
            from imagined risks so the dashboard can show why robot care is not simply liked or disliked.
        </div>
        <div class="question-card">
            <b>Question:</b> What social consequences do people expect if robot caregivers are developed?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="interaction-hint">
    <b>How to explore:</b> Hover over each point to read the full consequence question.
    Use the category filter to focus on promise, anxiety, or ambivalent outcomes.
</div>
    """,
    unsafe_allow_html=True
)

consequence_focus = st.radio(
    "Consequence category",
    ["All", "Promise", "Anxiety", "Ambivalent"],
    horizontal=True,
    help="Filter the consequence map by interpretive category."
)

consequence_view = consequence_summary.copy()

if consequence_focus != "All" and not consequence_view.empty:
    category_map_for_filter = {
        "Benefit": "Promise",
        "Concern": "Anxiety",
        "Ambivalent": "Ambivalent"
    }
    consequence_view["category_clean"] = consequence_view["category"].map(category_map_for_filter).fillna(consequence_view["category"])
    consequence_view = consequence_view[consequence_view["category_clean"] == consequence_focus].copy()

fig_consequence = make_consequence_mirror(consequence_view)

if fig_consequence is not None:
    st.plotly_chart(fig_consequence, use_container_width=True, config=CHART_CONFIG)
else:
    st.warning("No consequence data available for this selection.")

st.markdown(
    """
    <div class="section-note">
        <b>Interpretation:</b> Robot caregivers are imagined through competing outcomes:
        independence and reduced family burden on one side, isolation and social substitution on the other.
        This makes the technology a moral and relational question, not only a practical tool.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-wrap">
        <div id="chapter-05" class="jump-anchor"></div>
        <div class="chapter-return-tip" id="return-tip-chapter-05"><div class="chapter-return-message">You are viewing <b>Chapter 05: Reasons</b>. Return to the chapter menu to choose another section.</div><a href="#overview-navigation" class="chapter-return-link">Back to chapter menu ↑</a></div>
        <div class="section-kicker">Chapter 05</div>
        <div class="section-title">Acceptance and refusal are driven by different values</div>
        <div class="section-copy">
            The value map uses coded written responses. It shows that acceptance is tied to independence,
            availability, quality of care, and reducing family burden, while refusal is strongly shaped by concern over losing the human factor.
        </div>
        <div class="question-card">
            <b>Question:</b> Are people accepting a practical tool, or rejecting the loss of human care?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="inline-control-panel">
    <div class="inline-control-kicker">Chapter 05 interaction</div>
    <div class="inline-control-title">Tune the reason value map</div>
    <div class="inline-control-copy">
        Choose whether the treemap shows acceptance reasons, refusal reasons, or both.
        You can also control how many top coded responses are shown.
    </div>
</div>
    """,
    unsafe_allow_html=True
)

stance_choice = st.radio(
    "Reason group",
    ["Both", "Would use", "Would not use"],
    horizontal=True,
    help="Choose whether the reason map shows acceptance reasons, refusal reasons, or both."
)

st.markdown(
    f"""
<div class="interaction-hint">
    <b>How to explore:</b> Current lens: <b>{stance_choice}</b>.
    Hover over each rectangle to see the exact reason, share, and weighted mention count.
</div>
    """,
    unsafe_allow_html=True
)

top_n_reasons = 7

fig_reason, reason_view = make_reason_treemap(
    reasons,
    stance_choice,
    top_n_reasons
)

if fig_reason is not None:
    st.plotly_chart(
        fig_reason,
        use_container_width=True,
        config=CHART_CONFIG
    )
else:
    st.warning("No reason data available for this selection.")

clean_reasons = remove_low_value_reasons(reasons.copy())

top_positive = (
    clean_reasons[clean_reasons["stance"] == "Would use"]
    .sort_values("percentage", ascending=False)
    .head(1)
)

top_negative = (
    clean_reasons[clean_reasons["stance"] == "Would not use"]
    .sort_values("percentage", ascending=False)
    .head(1)
)

col_a, col_b = st.columns(2)

if not top_positive.empty:
    pos_reason = top_positive.iloc[0]["reason"]
    pos_pct = top_positive.iloc[0]["percentage"]

    with col_a:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-number">{pos_pct:.1f}%</div>
                <div class="insight-label">
                    Top positive reason among people willing to use a robot caregiver:
                    {pos_reason}.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

if not top_negative.empty:
    neg_reason = top_negative.iloc[0]["reason"]
    neg_pct = top_negative.iloc[0]["percentage"]

    with col_b:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-number">{neg_pct:.1f}%</div>
                <div class="insight-label">
                    Top negative reason among people unwilling to use a robot caregiver:
                    {neg_reason}.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <div class="section-note">
        <b>Interpretation:</b> The value map makes the reasons easier to compare.
        Acceptance tends to cluster around independence, availability, care quality, and reducing family burden.
        Refusal is strongly shaped by the missing human factor, which supports the central argument that robot care is judged
        as a social and emotional substitute, not just a practical tool.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-wrap">
        <div id="chapter-06" class="jump-anchor"></div>
        <div class="chapter-return-tip" id="return-tip-chapter-06"><div class="chapter-return-message">You are viewing <b>Chapter 06: Oversight</b>. Return to the chapter menu to choose another section.</div><a href="#overview-navigation" class="chapter-return-link">Back to chapter menu ↑</a></div>
        <div class="section-kicker">Chapter 06</div>
        <div class="section-title">Human oversight is not just more safety</div>
        <div class="section-copy">
            If people worry that robot care lacks human presence, one possible response is human monitoring.
            But monitoring can also introduce a different concern: surveillance and control.
        </div>
        <div class="question-card">
            <b>Question:</b> Does camera monitoring by a human operator make robot care feel safer, neutral, or worse?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="inline-control-panel">
    <div class="inline-control-kicker">Chapter 06 interaction</div>
    <div class="inline-control-title">Adjust the oversight response view</div>
    <div class="inline-control-copy">
        The triangle focuses on substantive responses. Refused or no answer responses are excluded so the comparison stays focused on clear opinions.
    </div>
</div>
    """,
    unsafe_allow_html=True
)

include_refused = False


left, right = st.columns([0.27, 0.73])

with left:
    st.markdown(
        """
        <div class="side-panel">
            <div class="side-panel-title">How to read this</div>
            <div class="side-panel-copy">
                The triangle summarizes three possible reactions to camera monitoring by a human operator:
                better, no difference, and worse.
                <br><br>
                The point shows the overall balance of responses. A positive net comfort score means more people felt better than worse.
                <br><br>
                Hover over the point to see the current Better, No difference, Worse, and Net comfort values.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    fig_oversight, oversight_view = make_oversight_triangle(
        filtered_respondent,
        oversight_summary,
        include_refused
    )

    if fig_oversight is not None:
        st.plotly_chart(fig_oversight, use_container_width=True, config=CHART_CONFIG)
    else:
        st.warning("No oversight data available.")

st.markdown(
    """
    <div class="section-note">
        <b>Interpretation:</b> The final chart closes the loop.
        Robot caregivers are not only evaluated as autonomous machines. They are also evaluated as systems of human oversight,
        responsibility, privacy, and control.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="takeaway-card">
        <div class="takeaway-kicker">Project takeaway</div>
        <div class="takeaway-title">
            Robot care is not only a technology question. It is a social relationship question.
        </div>
        <div class="takeaway-copy">
            Robot caregivers were imagined through a tension between <b>care</b>, <b>companionship</b>,
            <b>independence</b>, <b>isolation</b>, and <b>control</b>. The dashboard moves from public
            readiness, to attitude pathways, to caregiving context, to social consequences, to reasons
            for acceptance and refusal, and finally to the governance question of human oversight.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)