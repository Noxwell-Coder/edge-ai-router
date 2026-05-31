import streamlit as st
from core.router import CascadingRouter

# Initialize the router once per session
if "router" not in st.session_state:
    st.session_state.router = CascadingRouter()
    st.session_state.cost_saved = 0.0
    st.session_state.cloud_cost = 0.0

st.set_page_config(page_title="Edge AI Cost Router", layout="wide")

st.title("⚡ Cascading AI Pipeline (Edge/Cloud Routing)")
st.markdown("Request routing simulator for minimizing costs.")

# Metrics at the top
col1, col2 = st.columns(2)
col1.metric("Money saved (local runs)", f"${st.session_state.cost_saved:.4f}")
col2.metric("Spent on cloud", f"${st.session_state.cloud_cost:.4f}")

st.divider()

user_input = st.text_input("Enter your AI query (e.g. 'what is a div', 'network architecture'):")

if st.button("Send"):
    if user_input:
        with st.spinner("Analyzing and routing..."):
            level, response, latency = st.session_state.router.process_request(user_input)

            # Simulated cost accounting
            # Assume cloud response costs $0.02, local costs $0.00
            if "Cloud" in level:
                st.session_state.cloud_cost += 0.02
            else:
                # If handled locally, we saved that money
                st.session_state.cost_saved += 0.02

            st.success("Done!")

            st.markdown(f"**Response:** {response}")
            st.info(f"**Processed via:** {level}")
            st.caption(f"**Latency:** {latency:.2f} sec")

            st.rerun() # Refresh metrics on screen
