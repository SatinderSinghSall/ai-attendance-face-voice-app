import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""
<div style="
background:white;
border-radius:18px;
border:1px solid #e5e7eb;
padding:24px;
margin-bottom:18px;
box-shadow:0 2px 8px rgba(0,0,0,0.06);
border: 1px solid black;
">

<div style="display:flex; justify-content:space-between; align-items:center;">
<h3 style="margin:0; color:#1e293b; font-size:1.4rem;">
{name}
</h3>

<span style="
background:#E0E7FF;
color:#4F46E5;
padding:4px 10px;
border-radius:8px;
font-weight:600;
font-size:0.85rem;
">
{code}
</span>
</div>

<p style="
margin-top:6px;
color:#64748b;
font-size:0.9rem;
">
Section • <b>{section}</b>
</p>
"""

    if stats:
        html += '<div style="display:flex; gap:10px; margin-top:14px; flex-wrap:wrap;">'

        for icon, label, value in stats:
            html += f"""
<div style="
background:#f8fafc;
border:1px solid #e2e8f0;
padding:6px 12px;
border-radius:999px;
font-size:0.85rem;
color:#334155;
">
{icon} <b>{value}</b> {label}
</div>
"""

        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
        
