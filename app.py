
import streamlit as st
import json
import os
import random
from datetime import datetime

# ==========================================
# BENGAL AI CONTENT CREATOR
# Version 2.0
# ==========================================

st.set_page_config(
    page_title="Bengal AI Content Creator",
    page_icon="🎬",
    layout="centered"
)

# ==========================================
# MASTER PROMPT V2.1
# এখানে তোমার সম্পূর্ণ 20 Section Master Prompt
# স্থায়ীভাবে রাখা হবে।
# ==========================================

MASTER_PROMPT = """
ULTIMATE MASTER PROMPT V2.1
BENGAL + INDIA + WORLD NATURE & HUMAN LIFE
EXPANDED FANTASY EDITION

You are a professional AI Reel Director.

PROJECT DNA:
Nature + Human Life + Activity + Struggle
+ Travel + Discovery + Realistic Fantasy.

CONTENT CATEGORIES:
1. Bengal Village Life & Nature
2. India & World Nature and Human Life
3. Human Activity and Struggle
4. Fantasy Nature
5. Fantasy Architecture and Futuristic Civilizations

VIDEO FORMAT:
Vertical 9:16
5 Scenes
Approximately 8 seconds per scene
Total duration approximately 40 seconds.

MANDATORY SCENE STRUCTURE:
1. Story Purpose
2. Image/Video Prompt
3. Camera
4. Camera Movement
5. Subject Movement
6. Environment Movement
7. Sound Effects
8. Ambient Sound
9. Transition
10. Planned Exit State

CONTINUITY:
Character Lock
Location Lock
Environment Lock
Colour Lock
Lighting Lock
Material and Texture Lock
Motion Lock

VISUAL STYLE:
Photorealistic cinematic visuals.
Natural textures and believable physics.
Avoid plastic CGI, cartoon appearance,
unrealistic motion and excessive saturation.

FINAL OUTPUT:
Complete 5 Scene prompts.
Continuity instructions.
Audio design.
Quality audit.
Facebook caption.
Relevant hashtags.

EXPLANATION LANGUAGE: Bengali.
PRODUCTION PROMPTS: English.

IMPORTANT:
Preserve the Bengal + India + World project identity.
Fantasy and futuristic content are additions,
not replacements for village life and nature.
"""

# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

# ==========================================
# TOPIC COLLECTION
# ==========================================

TOPIC_COLLECTION = {
    "Bengal Village Life & Nature": [
        "Endless Green Village Road Tunnel",
        "A Peaceful Bengal Village Beside a River",
        "Ancient Banyan Tree Road in Monsoon",
        "A Fisherman's Journey Through Village Waters",
        "Golden Paddy Fields Under Dramatic Clouds"
    ],
    "India & World Nature": [
        "Meghalaya Living Root Bridge",
        "Giant Waterfall Hidden in a Green Forest",
        "Himalayan Valley Above the Clouds",
        "Wildlife Migration Across Vast Grasslands",
        "A Remote Island Surrounded by Turquoise Water"
    ],
    "Human Life & Struggle": [
        "A Farmer Working in a Vast Green Field",
        "A Fisherman Crossing a Wide River",
        "Village People Walking Through Heavy Rain",
        "Mountain Farmers on a Narrow Hill Path",
        "A Boat Journey Through a Dense Forest"
    ],
    "Fantasy Nature": [
        "The Giant Tree Above the Clouds",
        "An Endless Natural Green Tunnel",
        "A Hidden Waterfall Fantasy Valley",
        "A Giant Natural Bridge Above a Misty Forest",
        "A Magical Lake Inside an Ancient Forest"
    ],
    "Fantasy Architecture & Futuristic Civilizations": [
        "A Giant Fantasy City Ship Above the Ocean",
        "A Futuristic Floating Ocean City",
        "A Waterfall City Built Around Giant Trees",
        "A Sky City Above the Clouds",
        "A Forest Integrated Futuristic Civilization"
    ]
}

# ==========================================
# FUNCTIONS
# ==========================================

def get_new_suggestions():
    all_topics = []

    for category, topics in TOPIC_COLLECTION.items():
        for topic in topics:
            if topic not in st.session_state.history:
                all_topics.append((category, topic))

    random.shuffle(all_topics)
    return all_topics[:10]


def get_next_topic():
    available = []

    for category, topics in TOPIC_COLLECTION.items():
        for topic in topics:
            if topic not in st.session_state.history:
                available.append((category, topic))

    if not available:
        st.session_state.history = []
        available = [
            (category, topic)
            for category, topics in TOPIC_COLLECTION.items()
            for topic in topics
        ]

    return random.choice(available)


def save_topic(topic):
    if topic and topic not in st.session_state.history:
        st.session_state.history.append(topic)


# ==========================================
# APP HEADER
# ==========================================

st.title("🎬 Bengal AI Content Creator")
st.subheader("Your Personal AI Reel Director")

st.write(
    "তোমার Bengal + India + World Nature & Human Life "
    "Reel Project-এর জন্য একটি Content Creation Studio।"
)

st.divider()

# ==========================================
# TOPIC SELECTION
# ==========================================

st.header("1. Choose Your Topic")

mode = st.radio(
    "কীভাবে Topic নির্বাচন করবে?",
    [
        "Write My Own Topic",
        "Get 10 Topic Ideas",
        "NEXT - New Topic",
        "Upload Reference Image"
    ]
)

topic = ""

if mode == "Write My Own Topic":

    topic = st.text_input(
        "তোমার Reel Topic লিখো",
        placeholder="Example: Endless Green Village Road Tunnel"
    )

    if st.button("Use This Topic", type="primary"):
        if topic.strip():
            st.session_state.selected_topic = topic.strip()
            save_topic(topic.strip())
            st.success("Topic Selected Successfully!")
        else:
            st.warning("আগে একটি Topic লিখো।")


elif mode == "Get 10 Topic Ideas":

    if st.button("Generate 10 Topic Ideas", type="primary"):
        st.session_state.suggestions = get_new_suggestions()

    if st.session_state.suggestions:
        options = [
            f"{category} — {name}"
            for category, name in st.session_state.suggestions
        ]

        selected = st.selectbox(
            "পছন্দের Topic নির্বাচন করো",
            options
        )

        if st.button("Select This Topic"):
            selected_name = selected.split(" — ", 1)[1]
            st.session_state.selected_topic = selected_name
            save_topic(selected_name)
            st.success(f"Selected: {selected_name}")


elif mode == "NEXT - New Topic":

    if st.button("NEXT - Give Me a New Topic", type="primary"):
        category, new_topic = get_next_topic()
        st.session_state.selected_topic = new_topic
        save_topic(new_topic)

        st.success(f"Category: {category}")
        st.subheader(new_topic)


elif mode == "Upload Reference Image":

    uploaded_image = st.file_uploader(
        "Reference Image Upload করো",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_image:
        st.image(
            uploaded_image,
            caption="Your Reference Image",
            use_container_width=True
        )

        st.info(
            "Image input গ্রহণ করা হয়েছে। "
            "পরবর্তী ধাপে AI Vision যুক্ত হলে ছবির "
            "বিষয় বিশ্লেষণ করে Reel তৈরি করা যাবে।"
        )

        image_topic = st.text_input(
            "ছবি সম্পর্কে কিছু বলতে চাইলে লিখো (Optional)"
        )

        if st.button("Use Reference Image", type="primary"):
            st.session_state.selected_topic = (
                image_topic.strip()
                if image_topic.strip()
                else "Image Reference Based Reel"
            )
            st.success("Reference Image Selected!")


# ==========================================
# SELECTED TOPIC
# ==========================================

st.divider()

st.header("2. Your Selected Topic")

if st.session_state.selected_topic:
    st.success(st.session_state.selected_topic)

    st.write(
        "এই Topic ব্যবহার করে পরবর্তী ধাপে "
        "সম্পূর্ণ 5 Scene Reel Plan তৈরি করা হবে।"
    )

else:
    st.info("এখনও কোনো Topic নির্বাচন করা হয়নি।")


# ==========================================
# HISTORY
# ==========================================

st.divider()

st.header("3. Recent Topic History")

if st.session_state.history:
    for number, old_topic in enumerate(
        reversed(st.session_state.history[-10:]),
        start=1
    ):
        st.write(f"{number}. {old_topic}")
else:
    st.caption("এখনও কোনো Topic History নেই।")


# ==========================================
# MASTER PROMPT INFORMATION
# ==========================================

st.divider()

with st.expander("Master Prompt V2.1 - Project Rules"):
    st.write(
        "Master Prompt-এর Creative Rules এই অ্যাপের "
        "ভিতরে সংরক্ষিত আছে।"
    )
    st.code(MASTER_PROMPT, language="text")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Bengal AI Content Creator | Version 2.0"
)
