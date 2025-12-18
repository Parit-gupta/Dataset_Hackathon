"""
Theme Styles for GenAI Big Data Platform
Includes improved light theme with better contrast and readability
"""

import streamlit as st
from config import THEME_LIGHT, THEME_DARK

def get_theme_css():
    """
    Returns CSS based on current theme
    Fixed light theme with better contrast and visibility
    """
    if st.session_state.theme == THEME_DARK:
        return """
        <style>
        .stApp { 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
            color: #e0e0e0;
        }
        .title { 
            font-size: 34px; 
            font-weight: 800; 
            color: #ffffff; 
            margin-bottom: 0; 
        }
        .subtitle { 
            font-size: 16px; 
            color: #a0aec0; 
            margin-top: 5px; 
        }
        .card {
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 8px 20px rgba(0,0,0,0.6);
            color: #e0e0e0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .icon-card {
            background: linear-gradient(135deg, #2d3748 0%, #374151 100%);
            padding: 3rem 2rem;
            border-radius: 15px;
            box-shadow: 0px 8px 20px rgba(0,0,0,0.6);
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: #e0e0e0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .icon-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 12px 30px rgba(59,130,246,0.3);
            background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
            border: 1px solid rgba(59,130,246,0.5);
        }
        .icon-text { font-size: 60px; margin-bottom: 1rem; }
        .icon-title { font-size: 24px; font-weight: 700; margin-bottom: 0.5rem; color: #ffffff; }
        .icon-desc { font-size: 15px; color: #a0aec0; }
        .assessment-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8f 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 5px solid #3b82f6;
            color: #e0e0e0;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        }
        .teacher-card {
            background: linear-gradient(135deg, #3d2f5f 0%, #5a4a7f 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 5px solid #8b5cf6;
            color: #e0e0e0;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        }
        .stats-card {
            background: linear-gradient(135deg, #2d3748 0%, #374151 100%);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            color: #e0e0e0;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .question-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8f 100%);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 2px solid #3b82f6;
            color: #e0e0e0;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        }
        .question-text {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1rem;
        }
        .sentence-card {
            background: linear-gradient(135deg, #1e4d3a 0%, #2d6a4f 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 5px solid #10b981;
            color: #e0e0e0;
            font-size: 20px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        }
        .blank-space {
            display: inline-block;
            min-width: 100px;
            border-bottom: 2px dashed #3b82f6;
            padding: 0 10px;
            color: #60a5fa;
        }
        .progress-indicator {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8f 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1rem;
            color: #e0e0e0;
            border: 1px solid rgba(59,130,246,0.3);
        }
        .recording-option {
            background: linear-gradient(135deg, #2d3748 0%, #374151 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            color: #e0e0e0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .image-container {
            background: linear-gradient(135deg, #2d3748 0%, #374151 100%);
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        </style>
        """
    else:
        # IMPROVED LIGHT THEME with better contrast and readability
        return """
        <style>
        .stApp { 
            background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); 
        }
        .title { 
            font-size: 34px; 
            font-weight: 800; 
            color: #1e293b; 
            margin-bottom: 0;
            text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        }
        .subtitle { 
            font-size: 16px; 
            color: #475569; 
            margin-top: 5px; 
        }
        .card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            color: #1e293b;
        }
        .icon-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 3rem 2rem;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 2px solid #e2e8f0;
        }
        .icon-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 20px rgba(59,130,246,0.2);
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border: 2px solid #3b82f6;
        }
        .icon-text { 
            font-size: 60px; 
            margin-bottom: 1rem; 
        }
        .icon-title { 
            font-size: 24px; 
            font-weight: 700; 
            margin-bottom: 0.5rem; 
            color: #1e293b; 
        }
        .icon-desc { 
            font-size: 15px; 
            color: #64748b; 
        }
        .assessment-card {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 5px solid #2563eb;
            color: #1e293b;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
        }
        .teacher-card {
            background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 5px solid #7c3aed;
            color: #1e293b;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
        }
        .stats-card {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            color: #1e293b;
        }
        .question-card {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 2px solid #3b82f6;
            color: #1e293b;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
        }
        .question-text {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
        }
        .sentence-card {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 5px solid #059669;
            font-size: 20px;
            color: #1e293b;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
        }
        .blank-space {
            display: inline-block;
            min-width: 100px;
            border-bottom: 3px dashed #3b82f6;
            padding: 0 10px;
            color: #2563eb;
            font-weight: 600;
        }
        .progress-indicator {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1rem;
            color: #1e293b;
            border: 1px solid #93c5fd;
            font-weight: 600;
        }
        .recording-option {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 2px solid #e2e8f0;
            color: #1e293b;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        }
        .image-container {
            background: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
            border: 2px solid #e2e8f0;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        }
        </style>
        """


def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme = THEME_DARK if st.session_state.theme == THEME_LIGHT else THEME_LIGHT
    st.rerun()