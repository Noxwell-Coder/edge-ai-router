import streamlit as st
from core.router import CascadingRouter

CLOUD_REQUEST_COST = 0.02


def init_session():
    if "router" not in st.session_state:
        st.session_state.router = CascadingRouter()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "cost_saved" not in st.session_state:
        st.session_state.cost_saved = 0.0
    if "cloud_cost" not in st.session_state:
        st.session_state.cloud_cost = 0.0
    if "total_requests" not in st.session_state:
        st.session_state.total_requests = 0
    if "local_requests" not in st.session_state:
        st.session_state.local_requests = 0


def render_sidebar():
    with st.sidebar:
        st.title("💰 Cost Control Dashboard")
        st.caption("Live session metrics — resets on page reload")
        st.divider()

        total = st.session_state.total_requests
        local = st.session_state.local_requests
        efficiency = (local / total * 100) if total > 0 else 0.0
        full_cloud_cost = (total * CLOUD_REQUEST_COST) if total > 0 else 0.0

        saved_delta = f"+${full_cloud_cost - st.session_state.cloud_cost:.4f} vs full-cloud baseline"
        st.metric(
            label="💚 Total Saved (Local Runs)",
            value=f"${st.session_state.cost_saved:.4f}",
            delta=saved_delta if total > 0 else None,
        )

        cloud_delta = f"-${st.session_state.cost_saved:.4f} vs full-cloud baseline"
        st.metric(
            label="☁️ Total Cloud Spend",
            value=f"${st.session_state.cloud_cost:.4f}",
            delta=cloud_delta if total > 0 else None,
            delta_color="inverse",
        )

        st.metric(
            label="⚡ Infrastructure Efficiency",
            value=f"{efficiency:.1f}%",
            help="Percentage of requests resolved locally via Cache or Edge AI",
        )

        st.divider()
        st.markdown("**System Status**")
        if total == 0:
            st.info("⚪ Idle — Awaiting requests")
        elif efficiency >= 70:
            st.success("🟢 Operational — Budget Optimizing")
        else:
            st.error("🔴 Cloud Burn Alert — Review Routing Policy")

        st.divider()
        st.markdown("**Session Breakdown**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total)
        col2.metric("Local", local)
        col3.metric("Cloud", total - local)

        st.divider()
        if st.button("🗑️ Reset Session", use_container_width=True, type="secondary"):
            for key in ["messages", "cost_saved", "cloud_cost",
                        "total_requests", "local_requests", "router"]:
                st.session_state.pop(key, None)
            st.rerun()


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
        return "⚡", "Tier 1 — Local Cache", f"Instant cache hit — zero compute, zero cost. `{latency:.2f}s`"
    if "Tier 2" in level:
        return "🖥️", "Tier 2 — On-Device Edge AI", f"Resolved on Apple Silicon — no cloud spend incurred. `{latency:.2f}s`"
    return "☁️", "Tier 3 — Cloud API", f"Escalated to cloud model — **${CLOUD_REQUEST_COST:.2f} charged**. `{latency:.2f}s`"


def process_prompt(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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

    with st.chat_message("assistant", avatar="⚙️"):
        st.markdown(router_content)

    with st.chat_message("assistant"):
        st.markdown(response)

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

st.title("⚡ Edge AI Cascading Router")
st.caption(
    "Intelligent routing pipeline: **Cache → Edge AI → Cloud**. "
    "Minimizes cloud spend by resolving every query at the cheapest viable tier."
)

if not st.session_state.messages:
    with st.container():
        st.info(
            "**How it works:**  \n"
            "- ⚡ **Tier 1 (Cache)** — Identical queries are served instantly from memory at $0.00  \n"
            "- 🖥️ **Tier 2 (Edge AI)** — Simple queries are resolved on-device by a local model at $0.00  \n"
            "- ☁️ **Tier 3 (Cloud)** — Complex queries are escalated to a cloud model at $0.02  \n\n"
            "Try asking something simple, then something complex (e.g. *'what is TCP/IP'* vs *'analyze this network architecture'*)."
        )

render_messages()

if prompt := st.chat_input("Ask anything..."):
    process_prompt(prompt)
