import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Details", page_icon="🖼️", layout="wide")

# Block access if the user is not logged in.
if not st.session_state.get("authenticated", False):
    st.error("🔒 You must log in before accessing this page.")
    st.stop()

st.title("🖼️ Details & Song Previews")

# Read both artists' data out of session state.
name1 = st.session_state.get("artist_1_name")
results1 = st.session_state.get("artist_1_results")
name2 = st.session_state.get("artist_2_name")
results2 = st.session_state.get("artist_2_results")

if results1 is None or results2 is None:
    st.warning("Please search both artists on the Home page first.")
    st.stop()

def display_artist_previews(artist_name, results):
    st.subheader(f"Previews for {artist_name}")
    if results is None or len(results) == 0:
        st.info(f"No songs found for '{artist_name}'.")
        return

    st.caption(f"{len(results)} results for '{artist_name}'")
    for row_label in results.index:
        row = results.loc[row_label]
        cols = st.columns([1, 4])
        with cols[0]:
            artwork = row.get("artworkUrl100")
            if isinstance(artwork, str) and artwork:
                st.image(artwork, width=100)
            else:
                st.write("No artwork")
        with cols[1]:
            track_name = row.get("trackName", "Unknown")
            st.write(f"**{track_name}**")
            st.write(row.get("collectionName", ""))
            preview = row.get("previewUrl")
            if isinstance(preview, str) and preview:
                st.audio(preview)
            else:
                st.caption("No preview available")
        st.divider()

# Create side-by-side columns for both artists' song previews
columns = st.columns(2)

with columns[0]:
    display_artist_previews(name1, results1)

with columns[1]:
    display_artist_previews(name2, results2)