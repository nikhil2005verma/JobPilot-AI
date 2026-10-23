"""Shared Streamlit styling and small UI helpers."""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Figtree', system-ui, sans-serif; }
.block-container { padding-top: 2rem; max-width: 1200px; }
h1, h2, h3 { letter-spacing: -0.01em; font-weight: 650; }
[data-testid="stMetric"] { background:#fff; border:1px solid #E3E7EE; border-radius:12px; padding:14px 16px; }
[data-testid="stMetricLabel"] p { color:#5B6678; font-size:0.85rem; }
[data-testid="stMetricValue"] { font-weight:650; }
[data-testid="stSidebar"] { border-right:1px solid #E3E7EE; }
.ja-hero { background:#2457F5; color:#fff; border-radius:14px; padding:22px 26px; margin-bottom:18px; }
.ja-hero h2 { color:#fff; margin:0 0 4px 0; }
.ja-hero p { margin:0; opacity:.85; }
.ja-chip { display:inline-block; padding:2px 10px; border-radius:999px; font-size:0.78rem; margin:0 6px 4px 0; background:#E9EEFF; color:#1B3FBF; }
.ja-chip.miss { background:#FDECEC; color:#A02323; }
.ja-chip.ok { background:#E3F6EA; color:#17703A; }
:focus-visible { outline:2px solid #2457F5; outline-offset:2px; }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="ja-hero"><h2>{title}</h2><p>{subtitle}</p></div>', unsafe_allow_html=True)


def chips(items: list[str], kind: str = "") -> None:
    if not items:
        st.caption("None")
        return
    html = "".join(f'<span class="ja-chip {kind}">{_esc(i)}</span>' for i in items)
    st.markdown(html, unsafe_allow_html=True)


def _esc(text: str) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
