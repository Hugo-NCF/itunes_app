import streamlit as st
from itunes_api import search_itunes

# Configure the page title, icon, and wide layout for this app.
st.set_page_config(page_title="Itunes App Browser", page_icon="🎧", layout="wide")

# Initialize the authenticated flag the first time the app runs in a session.
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Initialize the username the first time the app runs in a session.
if "username" not in st.session_state:
    st.session_state["username"] = None

st.title("Itunes App")
st.caption("Logged in accounts only")

# If the visitor is already authenticated, skip the form and show a welcome message.
if st.session_state["authenticated"] == True:
    st.success(f"Logged in as {st.session_state['username']}.")
    st.write("Use the sidebar to open the Itunes pages.")
else:
    # st.form groups the two inputs and the submit button so the app only reruns once, on submit.
    login_form = st.form("login_form")

    # Add the username field inside the form.
    entered_username = login_form.text_input("Username")

    # Add the password field inside the form. type="password" masks the characters as they are typed.
    entered_password = login_form.text_input("Password", type="password")

    # Add the submit button inside the form.
    submitted = login_form.form_submit_button("Log in")

    # Only check credentials after the form has been submitted.
    if submitted == True:
        # Read the correct username out of secrets.toml.
        correct_username = st.secrets["credentials"]["username"]
        # Read the correct password out of secrets.toml.
        correct_password = st.secrets["credentials"]["password"]

        # Compare the entered credentials against the ones in secrets.toml.
        username_matches = entered_username == correct_username
        password_matches = entered_password == correct_password

        # Both fields must match before access is granted.
        if username_matches and password_matches:
            st.session_state["authenticated"] = True
            st.session_state["username"] = entered_username
            # Rerun so the welcome message replaces the form immediately.
            st.rerun()
        else:
            st.error("Incorrect username or password.")

    st.stop()

# Check whether the first artist's data has already been stored.
if "artist_1_name" not in st.session_state:
    st.session_state.artist_1_name = "BTS"
if "artist_1_results" not in st.session_state:
    st.session_state.artist_1_results = None

# Check whether the second artist's data has already been stored.
if "artist_2_name" not in st.session_state:
    st.session_state.artist_2_name = "Coldplay"
if "artist_2_results" not in st.session_state:
    st.session_state.artist_2_results = None

# Display the app title.
st.title("🎧 iTunes App Browser")
st.markdown(
    "Search two artists to explore their song previews, compare their discographies, "
    "and analyze their combined results across the app pages!"
)

st.subheader("Artist Compare & Search Controller")

# Create two equal-width columns, one per artist.
columns = st.columns(2)

# Build the first artist's search box inside the first column.
with columns[0]:
    name1 = st.text_input("Artist 1", value=st.session_state.artist_1_name, key="artist1_input")
    if st.button("Search Artist 1", key="artist1_button"):
        st.session_state.artist_1_name = name1
        st.session_state.artist_1_results = search_itunes(
            name1, entity="song", limit=15
        )

# Build the second artist's search box inside the second column.
with columns[1]:
    name2 = st.text_input("Artist 2", value=st.session_state.artist_2_name, key="artist2_input")
    if st.button("Search Artist 2", key="artist2_button"):
        st.session_state.artist_2_name = name2
        st.session_state.artist_2_results = search_itunes(
            name2, entity="song", limit=15
        )

# Single button to perform search for both simultaneously
if st.button("Search Both Artists", key="search_both_button"):
    st.session_state.artist_1_name = name1
    st.session_state.artist_1_results = search_itunes(name1, entity="song", limit=15)
    st.session_state.artist_2_name = name2
    st.session_state.artist_2_results = search_itunes(name2, entity="song", limit=15)

# Check whether both artists have been searched.
artist_1_ready = st.session_state.artist_1_results is not None
artist_2_ready = st.session_state.artist_2_results is not None

st.divider()

if artist_1_ready and artist_2_ready:
    st.success(f"Both '{st.session_state.artist_1_name}' and '{st.session_state.artist_2_name}' loaded successfully! Explore Details, Compare, and Results pages.")
else:
    st.info("Search both artists above to populate data across all app pages.")