import time
import traceback
from pathlib import Path

import streamlit as st
from PIL import Image

from agents import search_agent, reader_agent, writer_chain, critic_chain

APP_NAME = "ResearchMind"
TAGLINE = "Search, read, write and review: a full AI research team in one click."
BRAIN_SVG = '<svg viewBox="0 0 24 24"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/></svg>'

st.set_page_config(
    page_title=f"{APP_NAME} · AI Research Team",
    page_icon=Image.open(Path(__file__).parent / "favicon.png"),
    layout="wide",
)

CSS = """
<style>
:root, .stApp {color-scheme: light;}
.stApp {
    background:
        radial-gradient(circle at 10% 0%, #d9defa 0%, transparent 40%),
        radial-gradient(circle at 90% 10%, #d5e6fa 0%, transparent 35%),
        #e9ecfa;
}
header[data-testid="stHeader"] {background: transparent;}
.stAppDeployButton, #MainMenu, footer {display: none;}
.block-container {padding-top: 3.5rem; max-width: 1200px;}
[data-testid="stMarkdownContainer"] :is(p, li, h1, h2, h3, h4, strong, em, td, th) {color: #141a3a;}
[data-testid="stMarkdownContainer"] a {color: #4338ca;}
[data-testid="stMarkdownContainer"] th {background: #dfe3fa;}
[data-testid="stMarkdownContainer"] td {background: #ffffff;}

/* Sidebar Toggle Buttons - Always Visible (Normal, Focus, Active) */
button[data-testid="stSidebarCollapseButton"], 
[data-testid="stSidebarHeader"] button,
header[data-testid="stHeader"] button,
button[data-testid="stSidebarCollapseButton"]:focus,
[data-testid="stSidebarHeader"] button:focus,
header[data-testid="stHeader"] button:focus {
    background-color: #312e81 !important;
    border-radius: 10px !important;
    padding: 6px !important;
    box-shadow: 0 4px 12px rgba(49, 46, 129, 0.25) !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Sidebar Toggle SVG Icon - Always Visible */
button[data-testid="stSidebarCollapseButton"] svg, 
[data-testid="stSidebarHeader"] button svg,
header[data-testid="stHeader"] button svg,
button[data-testid="stSidebarCollapseButton"]:focus svg,
[data-testid="stSidebarHeader"] button svg:focus,
header[data-testid="stHeader"] button svg:focus {
    fill: #ffffff !important;
    stroke: #ffffff !important;
    color: #ffffff !important;
    width: 22px !important;
    height: 22px !important;
    opacity: 1 !important;
}

/* Sidebar Toggle Hover State */
button[data-testid="stSidebarCollapseButton"]:hover, 
[data-testid="stSidebarHeader"] button:hover,
header[data-testid="stHeader"] button:hover {
    background-color: #4f46e5 !important;
    transform: scale(1.05);
}

.hero {
    position: relative; overflow: hidden; margin-bottom: 26px;
    padding: 46px 48px; border-radius: 28px;
    background: linear-gradient(120deg, #151a3d 0%, #312e81 55%, #4f46e5 100%);
    box-shadow: 0 20px 50px rgba(30, 35, 90, .35);
}
.hero::before, .hero::after {content: ""; position: absolute; border-radius: 50%; background: rgba(255,255,255,.07);}
.hero::before {width: 260px; height: 260px; right: -60px; top: -80px;}
.hero::after {width: 160px; height: 160px; right: 140px; bottom: -70px;}
.hero-badge {
    display: inline-block; margin-bottom: 14px; padding: 6px 14px; border-radius: 999px;
    background: rgba(255,255,255,.16); color: #fff; font-size: 13px; font-weight: 600;
}
.hero h1 {margin: 0; font-size: 58px; font-weight: 800; letter-spacing: -1.5px; line-height: 1.05;}
.hero p {margin: 12px 0 0 0; max-width: 640px; font-size: 19px; opacity: .95;}
.hero h1, .hero p {color: #ffffff !important;}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #eef0fc 100%);
    border-right: 1px solid #dde2f7;
}
.side-brand {font-size: 26px; font-weight: 800; color: #4338ca; letter-spacing: -.5px;}
.side-sub {margin-bottom: 10px; font-size: 13px; color: #6b74a8;}
.logo {display: flex; align-items: center; gap: 12px;}
.logo-mark {display: flex; align-items: center; justify-content: center; width: 44px; height: 44px;
            border-radius: 14px; background: linear-gradient(120deg, #312e81, #4f46e5);
            box-shadow: 0 6px 16px rgba(49, 46, 129, .3);}
.logo-mark svg {width: 26px; height: 26px; fill: none; stroke: #fff; stroke-width: 2;
                stroke-linecap: round; stroke-linejoin: round;}

.stTextInput label p {color: #2a3580; font-weight: 600;}
.stTextInput [data-baseweb="input"] {background: #ffffff; border-radius: 16px;}
.stTextInput input {
    padding: 16px 18px; font-size: 17px; color: #141a3a; background: #ffffff;
    border: 2px solid #cfd5f3; border-radius: 16px;
    -webkit-text-fill-color: #141a3a;
}
.stTextInput input::placeholder {color: #8e97c8; -webkit-text-fill-color: #8e97c8;}
.stButton > button {border-radius: 14px; font-weight: 600; transition: all .2s ease;}
.stButton > button[kind="secondary"] {background: #ffffff; border: 1px solid #dde2f7;}
.stButton > button[kind="secondary"] p {color: #2a3580;}
.stButton > button[kind="secondary"]:hover {background: #eef0fc; border-color: #6366f1;}
.stButton > button[kind="primary"] {
    padding: 12px 28px; border: none;
    background: linear-gradient(120deg, #312e81, #4f46e5);
    box-shadow: 0 10px 24px rgba(49, 46, 129, .35);
}
.stButton > button[kind="primary"] p, .stDownloadButton > button p {color: #fff;}
.stDownloadButton > button {padding: 10px 22px; border: none; border-radius: 14px; background: #312e81;}
.stDownloadButton > button:hover {background: #4f46e5;}

.section-title {margin: 26px 0 4px 0; font-size: 22px; font-weight: 800; color: #141a3a;}
.section-sub {margin-bottom: 8px; color: #4b5490;}
.pipeline {display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 8px 0 10px 0;}
.step {padding: 20px 18px; background: #ffffff; border: 2px solid #dde2f7; border-radius: 20px;
       box-shadow: 0 8px 24px rgba(60, 70, 150, .10); transition: all .3s ease;}
.step .icon {display: flex; align-items: center; justify-content: center; width: 48px; height: 48px;
             margin-bottom: 12px; border-radius: 14px; background: #eceffd; font-size: 24px;}
.step .title {font-size: 16px; font-weight: 700; color: #141a3a;}
.step .desc {min-height: 34px; margin-top: 3px; font-size: 13px; color: #5b6499;}
.step .badge {display: inline-block; margin-top: 12px; padding: 4px 12px; border-radius: 999px;
              font-size: 12px; font-weight: 700; background: #eceffd; color: #6b74a8;}
.step.running {border-color: #6366f1; box-shadow: 0 0 0 5px rgba(99,102,241,.15), 0 12px 30px rgba(99,102,241,.22);}
.step.running .icon {background: linear-gradient(120deg, #4338ca, #6366f1);}
.step.running .badge {background: #e4e7ff; color: #4338ca;}
.step.done {border-color: #a7e3c4;}
.step.done .icon, .step.done .badge {background: #dcf5e8;}
.step.done .badge {color: #12995a;}
.step.error {border-color: #ffb8c2;}
.step.error .icon, .step.error .badge {background: #ffe3e7;}
.step.error .badge {color: #d6294a;}

.metrics {display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin: 14px 0 22px 0;}
.metric {padding: 16px 18px; background: #ffffff; border: 1px solid #dde2f7; border-radius: 18px;
         box-shadow: 0 6px 18px rgba(60, 70, 150, .08);}
.metric .label {font-size: 12px; font-weight: 600; letter-spacing: .6px; text-transform: uppercase; color: #6b74a8;}
.metric .value {margin-top: 4px; font-size: 26px; font-weight: 800; color: #141a3a;}
.metric.total {border: none; background: linear-gradient(120deg, #312e81, #4f46e5);}
.metric.total .label {color: #c7d2fe;}
.metric.total .value {color: #fff;}

.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {padding: 10px 18px; background: #ffffff; border: 1px solid #dde2f7; border-radius: 12px;}
.stTabs [data-baseweb="tab"] p {font-weight: 600; color: #4b5490;}
.stTabs [aria-selected="true"] {background: linear-gradient(120deg, #312e81, #4f46e5); border: none;}
.stTabs [aria-selected="true"] p {color: #fff;}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display: none;}

@media (max-width: 900px) {
    .pipeline, .metrics {grid-template-columns: repeat(2, 1fr);}
    .hero {padding: 30px 26px;}
    .hero h1 {font-size: 40px;}
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

STEPS = [
    {"key": "search", "icon": "🔍", "title": "Search Agent", "desc": "Scours the web for sources"},
    {"key": "summary", "icon": "📖", "title": "Reader Agent", "desc": "Reads & distills key facts"},
    {"key": "report", "icon": "✍️", "title": "Writer Agent", "desc": "Drafts the full report"},
    {"key": "evaluation", "icon": "🧐", "title": "Critic Agent", "desc": "Reviews quality & gaps"},
]
BADGES = {"pending": "Waiting", "running": "Working…", "done": "Done ✓", "error": "Failed"}


def to_text(result) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if hasattr(result, "content"):
        return to_text(result.content)
    if isinstance(result, dict):
        if "output" in result:
            return to_text(result["output"])
        if "messages" in result and result["messages"]:
            return to_text(result["messages"][-1])
        if "text" in result:
            return to_text(result["text"])
        return str(result)
    if isinstance(result, list):
        parts = []
        for item in result:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
            else:
                parts.append(to_text(item))
        return "\n".join(p for p in parts if p)
    return str(result)


def stepper_html(states: dict, timings: dict) -> str:
    cards = []
    for s in STEPS:
        state = states.get(s["key"], "pending")
        badge = BADGES[state]
        if state == "done" and s["key"] in timings:
            badge = f"Done ✓ · {timings[s['key']]:.1f}s"
        cards.append(
            f'<div class="step {state}">'
            f'<div class="icon">{s["icon"]}</div>'
            f'<div class="title">{s["title"]}</div>'
            f'<div class="desc">{s["desc"]}</div>'
            f'<span class="badge">{badge}</span>'
            f"</div>"
        )
    return '<div class="pipeline">' + "".join(cards) + "</div>"


def metrics_html(timings: dict, report: str) -> str:
    words = len(report.split())
    items = [
        ("Search", f"{timings['search']:.1f}s", ""),
        ("Reader", f"{timings['summary']:.1f}s", ""),
        ("Writer", f"{timings['report']:.1f}s", ""),
        ("Critic", f"{timings['evaluation']:.1f}s", ""),
        ("Total time", f"{sum(timings.values()):.1f}s", "total"),
    ]
    html = "".join(
        f'<div class="metric {cls}"><div class="label">{label}</div>'
        f'<div class="value">{value}</div></div>'
        for label, value, cls in items
    )
    return f'<div class="metrics">{html}</div>' + (
        f'<div class="section-sub">📝 Report length: <b>{words:,}</b> words</div>'
    )


def build_markdown_report(topic, report, evaluation) -> str:
    return (
        f"# Research Report: {topic}\n\n"
        f"{report}\n\n---\n\n"
        f"## Critic Evaluation\n\n{evaluation}\n"
    )


def run_pipeline(topic: str, tracker):
    states = {s["key"]: "pending" for s in STEPS}
    timings, results = {}, {}

    def refresh():
        tracker.markdown(stepper_html(states, timings), unsafe_allow_html=True)

    def run_step(key, fn):
        states[key] = "running"
        refresh()
        t0 = time.time()
        try:
            out = fn()
        except Exception:
            states[key] = "error"
            refresh()
            raise
        timings[key] = time.time() - t0
        states[key] = "done"
        refresh()
        return out

    try:
        search_result = run_step("search", lambda: search_agent.invoke({"topic": topic}))
        results["search"] = to_text(search_result)

        summarized = run_step("summary", lambda: reader_agent.invoke({"research": search_result}))
        results["summary"] = to_text(summarized)

        draft = run_step(
            "report", lambda: writer_chain.invoke({"topic": topic, "research": summarized})
        )
        results["report"] = to_text(draft)

        evaluation = run_step("evaluation", lambda: critic_chain.invoke({"report": draft}))
        results["evaluation"] = to_text(evaluation)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
        with st.expander("Error details"):
            st.code(traceback.format_exc())
        return None

    results["timings"] = timings
    results["topic"] = topic
    return results


st.session_state.setdefault("results", None)
st.session_state.setdefault("topic_input", "")

EXAMPLES = [
    "Impact of AI on healthcare in 2026",
    "Future of solid-state batteries",
    "Recent breakthroughs in quantum computing",
    "Renewable energy trends in India",
    "How large language models are changing education",
]

with st.sidebar:
    st.markdown(
        f'<div class="logo"><div class="logo-mark">{BRAIN_SVG}</div>'
        f'<div class="side-brand">{APP_NAME}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-sub">Your AI research team</div>', unsafe_allow_html=True)

    st.markdown("**💡 Try a topic**")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
            st.session_state.topic_input = ex
            st.rerun()

    st.divider()
    st.markdown("**⚙️ How it works**")
    st.markdown(
        "1. 🔍 **Search** finds information\n"
        "2. 📖 **Reader** summarizes it\n"
        "3. ✍️ **Writer** drafts the report\n"
        "4. 🧐 **Critic** reviews the draft"
    )
    st.divider()
    if st.button("🗑️ Clear results", use_container_width=True):
        st.session_state.results = None
        st.session_state.topic_input = ""
        st.rerun()

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-badge">✨ Multi-Agent AI Research</div>
        <h1>{APP_NAME}</h1>
        <p>{TAGLINE} Enter any topic and watch your team of agents search, read, write and critique in real time.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_in, col_btn = st.columns([5, 1.3], vertical_alignment="bottom")
with col_in:
    topic = st.text_input(
        "What do you want to research?",
        key="topic_input",
        placeholder="e.g. The impact of AI on healthcare",
    )
with col_btn:
    run_clicked = st.button(
        "🚀 Research", type="primary", use_container_width=True, disabled=not topic.strip()
    )

st.markdown('<div class="section-title">Agent pipeline</div>', unsafe_allow_html=True)
tracker = st.empty()

if run_clicked:
    st.session_state.results = None
    st.session_state.results = run_pipeline(topic.strip(), tracker)
elif st.session_state.results:
    tracker.markdown(
        stepper_html({s["key"]: "done" for s in STEPS}, st.session_state.results["timings"]),
        unsafe_allow_html=True,
    )
else:
    tracker.markdown(
        stepper_html({s["key"]: "pending" for s in STEPS}, {}), unsafe_allow_html=True
    )

res = st.session_state.results
if res:
    st.markdown(f'<div class="section-title">Results: {res["topic"]}</div>', unsafe_allow_html=True)
    st.markdown(metrics_html(res["timings"], res["report"]), unsafe_allow_html=True)

    tab_report, tab_eval, tab_summary, tab_search = st.tabs(
        ["📄 Final Report", "🧐 Critic Review", "📖 Reader Summary", "🔍 Raw Search"]
    )
    with tab_report:
        with st.container(border=True):
            st.markdown(res["report"])
    with tab_eval:
        with st.container(border=True):
            st.markdown(res["evaluation"])
    with tab_summary:
        with st.container(border=True):
            st.markdown(res["summary"])
    with tab_search:
        with st.container(border=True):
            st.markdown(res["search"])

    st.write("")
    st.download_button(
        "⬇️ Download report (.md)",
        data=build_markdown_report(res["topic"], res["report"], res["evaluation"]),
        file_name="researchmind_report.md",
        mime="text/markdown",
    )