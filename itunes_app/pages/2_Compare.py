import streamlit as st

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Compare", page_icon="⚖️", layout="wide")

# Block access if the user is not logged in.
if not st.session_state.get("authenticated", False):
    st.error("🔒 You must log in before accessing this page.")
    st.stop()

st.title("⚖️ Compare Artists")

# Read both artists' names and results out of session state.
name1 = st.session_state.get("artist_1_name")
results1 = st.session_state.get("artist_1_results")
name2 = st.session_state.get("artist_2_name")
results2 = st.session_state.get("artist_2_results")

# Make sure both artists have been searched before showing a comparison.
if not name1 or not name2 or results1 is None or results2 is None:
    st.warning("Search both artists on the Home page first.")
    st.stop()

preferred_columns = ["trackName", "collectionName"]

columns = st.columns(2)

# First artist summary
with columns[0]:
    st.subheader(name1)
    result_count = len(results1)
    if result_count == 0:
        st.info(f"No songs found for '{name1}'.")
    else:
        st.metric("Songs found", result_count)
        if "collectionName" in results1.columns:
            st.write("Albums represented:", results1["collectionName"].nunique())
        show_columns = [col for col in preferred_columns if col in results1.columns]
        st.dataframe(results1[show_columns], use_container_width=True, hide_index=True)

# Second artist summary
with columns[1]:
    st.subheader(name2)
    result_count = len(results2)
    if result_count == 0:
        st.info(f"No songs found for '{name2}'.")
    else:
        st.metric("Songs found", result_count)
        if "collectionName" in results2.columns:
            st.write("Albums represented:", results2["collectionName"].nunique())
        show_columns = [col for col in preferred_columns if col in results2.columns]
        st.dataframe(results2[show_columns], use_container_width=True, hide_index=True)