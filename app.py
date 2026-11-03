
import streamlit as st

st.set_page_config(
    page_title="Bengal AI Content Creator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Bengal AI Content Creator")
st.subheader("Your Personal AI Video Director")

st.write("বাংলায় Topic লিখুন। আমরা আপনার Reel তৈরির কাজ শুরু করব।")

topic = st.text_input(
    "আপনার Reel-এর Topic লিখুন",
    placeholder="Example: Endless Green Village Road Tunnel"
)

if st.button("Create Reel Plan"):
    if topic.strip():
        st.success(f"আপনার Topic: {topic}")
        st.info("পরবর্তী ধাপে AI Story ও 5 Scene Generator যুক্ত হবে।")
    else:
        st.warning("আগে একটি Topic লিখুন।")

st.caption("Bengal AI Content Creator | Version 1.0")
