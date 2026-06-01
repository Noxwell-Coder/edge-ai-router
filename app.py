import streamlit as st
from core.router import CascadingRouter

CLOUD_REQUEST_COST = 0.02

MOCK_HISTORY = [
    "Python basics",
    "Deployment strategies",
    "Docker vs Kubernetes",
    "REST API design",
    "ML model optimization",
    "Network security review",
    "CI/CD pipeline setup",
]


def init_session():
    defaults = {
        "router": CascadingRouter(),
        "messages": [],
        "show_stats": True,
        "cost_saved": 0.0,
        "cloud_cost": 0.0,
        "total_requests": 0,
        "local_requests": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def toggle_stats():
    st.session_state.show_stats = not st.session_state.show_stats


def reset_session():
    for key in ["messages", "cost_saved", "cloud_cost",
                "total_requests", "local_requests", "router"]:
        st.session_state.pop(key, None)


def render_sidebar():
    with st.sidebar:
        # Scope the blue override to only this sidebar's primary button
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] [data-testid="baseButton-primary"] {
                background-color: #2563eb;
                border-color: #2563eb;
                color: #ffffff;
            }
            [data-testid="stSidebar"] [data-testid="baseButton-primary"]:hover {
                background-color: #1d4ed8;
                border-color: #1d4ed8;
                color: #ffffff;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.button("➕ New Chat", use_container_width=True,
                  type="primary", on_click=reset_session)

        st.divider()
        st.caption("Recent Conversations")
        for item in MOCK_HISTORY:
            st.markdown(f"💬 &nbsp; {item}")


def render_stats_panel():
    st.subheader("💰 Cost Control Dashboard")
    st.caption("Live session metrics — resets on page reload")

    total = st.session_state.total_requests
    local = st.session_state.local_requests
    efficiency = (local / total * 100) if total > 0 else 0.0
    full_cloud_cost = total * CLOUD_REQUEST_COST

    st.metric(
        label="🟢 Total Money Saved (Local Runs)",
        value=f"${st.session_state.cost_saved:.4f}",
        delta=(f"+${full_cloud_cost - st.session_state.cloud_cost:.4f} vs full-cloud"
               if total > 0 else None),
    )
    st.metric(
        label="☁️ Total Cloud Spending",
        value=f"${st.session_state.cloud_cost:.4f}",
        delta=(f"-${st.session_state.cost_saved:.4f} vs full-cloud"
               if total > 0 else None),
        delta_color="inverse",
    )
    st.metric(
        label="⚡ Infrastructure Efficiency",
        value=f"{efficiency:.1f}%",
        help="Percentage of requests resolved locally via Cache or Edge AI",
    )

    st.divider()
    st.markdown("**System State**")
    if total == 0:
        st.info("⚪ Idle — Awaiting requests")
    elif efficiency >= 70:
        st.success("🟢 Operational — Budget Optimizing")
    else:
        st.error("🔴 Cloud Burn Alert — Review Routing Policy")

    st.divider()
    st.markdown("**Session Breakdown**")
    b1, b2, b3 = st.columns(3)
    b1.metric("Total", total)
    b2.metric("Local", local)
    b3.metric("Cloud", total - local)


def render_messages():
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant"):
                st.markdown(content)
        elif role == "router":
            with st.chat_message("assistant", avatar="⚙️"):
                st.markdown(content)


def _tier_metadata(level: str, latency: float) -> tuple[str, str, str]:
    if "Tier 1" in level:
        return ("⚡", "Tier 1 — Local Cache",
                f"Instant cache hit — zero compute, zero cost. `{latency:.2f}s`")
    if "Tier 2" in level:
        return ("🖥️", "Tier 2 — On-Device Edge AI",
                f"Resolved on Apple Silicon — no cloud spend incurred. `{latency:.2f}s`")
    return ("☁️", "Tier 3 — Cloud API",
            f"Escalated to cloud model — **${CLOUD_REQUEST_COST:.2f} charged**. `{latency:.2f}s`")


def process_prompt(prompt: str):
    with st.spinner("Routing and generating..."):
        level, response, latency = st.session_state.router.process_request(prompt)

    is_cloud = "Tier 3" in level
    st.session_state.total_requests += 1
    if is_cloud:
        st.session_state.cloud_cost += CLOUD_REQUEST_COST
    else:
        st.session_state.cost_saved += CLOUD_REQUEST_COST
        st.session_state.local_requests += 1

    icon, tier_label, tier_note = _tier_metadata(level, latency)
    router_content = f"{icon} **Routed via: {tier_label}** — {tier_note}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "router", "content": router_content})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()


# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Edge AI Router",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()
render_sidebar()

# Header
title_col, btn_col = st.columns([5, 1])
with title_col:
    st.title("⚡ Edge AI Cascading Router")
with btn_col:
    btn_label = "✖ Stats" if st.session_state.show_stats else "📊 Stats"
    st.button(btn_label, key="toggle_stats", on_click=toggle_stats,
              use_container_width=True)

# Main content
if st.session_state.show_stats:
    chat_col, stats_col = st.columns([3, 1], gap="large")
else:
    chat_col = st.container()
    stats_col = None

with chat_col:
    if len(st.session_state.messages) == 0:
        st.info(
            "**How the routing pipeline works:**  \n"
            "- ⚡ **Tier 1 — Cache:** Identical queries served instantly at $0.00  \n"
            "- 🖥️ **Tier 2 — Edge AI:** Simple queries resolved on-device at $0.00  \n"
            "- ☁️ **Tier 3 — Cloud:** Complex queries escalated to cloud at $0.02  \n\n"
            "Try something simple (*'what is TCP/IP'*) then something complex "
            "(*'analyze this network architecture'*) to see the router in action."
        )

    render_messages()

    if prompt := st.chat_input("Ask anything..."):
        process_prompt(prompt)

if stats_col is not None:
    with stats_col:
        render_stats_panel()
