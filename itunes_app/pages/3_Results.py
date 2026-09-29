import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Results", page_icon="📄", layout="wide")

# Block access if the user is not logged in.
if not st.session_state.get("authenticated", False):
    st.error("🔒 You must log in before accessing this page.")
    st.stop()

st.title("📄 Combined Discography Results")

name1 = st.session_state.get("artist_1_name")
results1 = st.session_state.get("artist_1_results")
name2 = st.session_state.get("artist_2_name")
results2 = st.session_state.get("artist_2_results")

if results1 is None or results2 is None:
    st.warning("No search yet - go to the Home page and search both artists first.")
    st.stop()

# Combine both DataFrames
results = pd.concat([results1, results2], ignore_index=True)
result_count = len(results)

if result_count == 0:
    st.info(f"No songs found for '{name1}' or '{name2}'.")
    st.stop()

st.caption(f"{result_count} total results for '{name1}' & '{name2}' combined.")

preferred_columns = ["artistName", "trackName", "collectionName", "releaseDate"]
show_columns = [col for col in preferred_columns if col in results.columns]

st.dataframe(results[show_columns], use_container_width=True, hide_index=True)

st.subheader("Songs per album (Combined Results)")
if "collectionName" in results.columns:
    album_counts = results["collectionName"].value_counts()
    st.bar_chart(album_counts)