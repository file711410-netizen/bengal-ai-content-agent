
import streamlit as st
import random
import re
import hashlib
from PIL import Image
from google import genai


# =========================================================
# 1. APP SETTINGS
# =========================================================

st.set_page_config(
    page_title="Bengal AI Content Creator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Bengal AI Content Creator")

st.markdown(
    """
    **Bengal + India + World Nature & Human Life Reel Studio**

    Topic লিখে অথবা Reference Image Upload করে
    সম্পূর্ণ ৫-Scene AI Reel Production Prompt তৈরি করো।
    """
)


# =========================================================
# 2. TOPIC LIBRARY
# =========================================================

TOPIC_LIBRARY = [
    ("Bengal Village Life", "A Narrow Village Road Beneath Giant Banyan Trees"),
    ("Bengal Village Life", "A Quiet Pond Surrounded by Coconut Palms"),
    ("Bengal Village Life", "A Farmer Walking Through Golden Paddy Fields"),
    ("Bengal Village Life", "A Hidden Bamboo Tunnel in a Bengal Village"),
    ("Bengal Village Life", "Fishermen Crossing a Misty Village River"),
    ("Bengal Village Life", "A Beautiful Green Road Beside a Village Canal"),
    ("Bengal Village Life", "A Traditional Village Market at Sunrise"),
    ("Bengal Village Life", "A Small Boat Moving Through Water Lily Fields"),
    ("Bengal Village Life", "A Village Road Covered by Flowering Trees"),
    ("Bengal Village Life", "A Rural Journey Through Mustard Fields"),
    ("Bengal Village Life", "A Beautiful Village Road During Spring"),
    ("Bengal Village Life", "A Traditional Bengal Village After Rain"),
    ("Bengal Village Life", "A Fisherman Casting His Net at Sunrise"),
    ("Bengal Village Life", "A Bullock Cart Crossing a Green Village Road"),
    ("Bengal Village Life", "A Village Path Through Tall Areca Palm Trees"),

    ("India & World Nature", "Meghalaya's Living Root Bridge in the Mist"),
    ("India & World Nature", "A Hidden Waterfall Deep Inside a Rainforest"),
    ("India & World Nature", "A Mountain Village Above the Clouds"),
    ("India & World Nature", "Wild Elephants Crossing a Forest River"),
    ("India & World Nature", "A Vast Green Valley in the Himalayas"),
    ("India & World Nature", "A Remote Island Surrounded by Turquoise Water"),
    ("India & World Nature", "A Giant Waterfall in an Ancient Forest"),
    ("India & World Nature", "A Desert Caravan at Sunset"),
    ("India & World Nature", "A Fisherman's Journey Along a Rocky Coast"),
    ("India & World Nature", "A Swiss Valley Surrounded by Snowy Mountains"),
    ("India & World Nature", "A Giant Forest in the Western Ghats"),
    ("India & World Nature", "A Village Beside a Himalayan River"),
    ("India & World Nature", "A Wildlife Migration Across a Vast Grassland"),
    ("India & World Nature", "A Tropical Island Hidden in the Ocean"),
    ("India & World Nature", "A Mountain Trail Above the Clouds"),

    ("Fantasy Nature", "The Endless Green Village Road Tunnel"),
    ("Fantasy Nature", "The Giant Tree Above the Clouds"),
    ("Fantasy Nature", "A Colossal Forest with a Natural Stone Bridge"),
    ("Fantasy Nature", "A Hidden Lake Beneath Giant Waterfalls"),
    ("Fantasy Nature", "A Floating Island Covered with Ancient Trees"),
    ("Fantasy Nature", "A Giant Tree with a Waterfall Inside Its Trunk"),
    ("Fantasy Nature", "An Endless Forest Path Under Rounded Green Canopies"),
    ("Fantasy Nature", "A Magical Valley Filled with Giant Flowers"),
    ("Fantasy Nature", "A Natural Bridge Connecting Two Cloud Mountains"),
    ("Fantasy Nature", "A Crystal-Clear River Through a Giant Forest"),
    ("Fantasy Nature", "A Giant Green Tunnel Around a Winding Road"),
    ("Fantasy Nature", "A Forest of Colossal Trees Above a Misty Valley"),
    ("Fantasy Nature", "A Hidden Waterfall Inside a Giant Tree"),
    ("Fantasy Nature", "A Beautiful Green Island Floating Above Clouds"),
    ("Fantasy Nature", "An Ancient Forest with Towering Natural Arches"),

    ("Fantasy Architecture", "A Giant City Ship Sailing Across the Ocean"),
    ("Fantasy Architecture", "A Futuristic City Built Around Giant Trees"),
    ("Fantasy Architecture", "A Floating City Above the Clouds"),
    ("Fantasy Architecture", "A Waterfall City Inside a Mountain Valley"),
    ("Fantasy Architecture", "A Giant Sky Garden Civilization"),
    ("Fantasy Architecture", "A Fantasy Harbour with Colossal Ships"),
    ("Fantasy Architecture", "A Forest Civilization Connected by Bridges"),
    ("Fantasy Architecture", "A Grand Castle Above a Sea of Clouds"),
    ("Fantasy Architecture", "A Futuristic Ocean City at Sunrise"),
    ("Fantasy Architecture", "A Giant Ship Carrying a Beautiful Green City"),
    ("Fantasy Architecture", "A Floating Harbour with Giant Sailing Cities"),
    ("Fantasy Architecture", "A Futuristic City Surrounded by Waterfalls"),
    ("Fantasy Architecture", "A Giant Green City Ship Crossing the Ocean"),
    ("Fantasy Architecture", "A Sky Civilization Connected by Hanging Bridges"),
    ("Fantasy Architecture", "A Beautiful Ocean City with Giant Garden Towers")
]


# =========================================================
# 3. COMPLETE MASTER PROMPT
# =========================================================

MASTER_PROMPT = r"""
You are an elite AI Reel Director, Concept Developer,
Documentary Filmmaker, Nature Cinematographer,
Human-Life Storyteller, Fantasy Designer, Screenwriter,
Storyboard Artist, AI Prompt Engineer and Social Media Strategist.

PROJECT:
BENGAL + INDIA + WORLD NATURE & HUMAN LIFE REEL PROJECT

PROJECT DNA:
NATURE + HUMAN LIFE + ACTIVITY / STRUGGLE
+ TRAVEL / DISCOVERY + FANTASY.

Nature is the primary focus. Humans are part of the
environment and do not need to be the main hero in every scene.

==================================================
SECTION 1 — PROJECT ROLE
==================================================

Act as a professional creative director and production
prompt engineer. Create visually powerful, coherent,
photorealistic short-form cinematic reels.

==================================================
SECTION 2 — PROJECT DNA
==================================================

The project combines:
- Nature.
- Human life.
- Activity and struggle.
- Travel and discovery.
- Realistic fantasy.

Nature remains the central visual identity.
Human beings interact naturally with their surroundings.

==================================================
SECTION 3 — FOUR CONTENT CATEGORIES
==================================================

CATEGORY A — BENGAL VILLAGE LIFE & NATURE

Explore:
- Bengal village life and rural landscapes.
- Farming, fishing, harvesting and village work.
- Human struggle and everyday activities.
- Mud roads, brick roads and village pathways.
- Giant banyan trees and green tree tunnels.
- Coconut and areca palm roads.
- Bamboo paths and pond-side roads.
- Rivers, canals, ponds and wetlands.
- Paddy fields, mustard fields, kash flowers and shiuli flowers.
- Spring, summer, monsoon and winter village environments.
- Rural houses, boats, bridges and village markets.

CATEGORY B — INDIA & WORLD NATURE / HUMAN LIFE

Explore:
- Himalayas, Meghalaya and living root bridges.
- Waterfalls, forests, rivers and mountains.
- Wildlife, migration and natural habitats.
- Deserts, coastlines, islands and rainforests.
- Icelandic landscapes, Swiss valleys and fjords.
- Remote villages and mountain communities.
- Farmers, fishermen, explorers and local people.
- Human survival, travel, discovery and struggle.

CATEGORY C — FANTASY NATURE

Explore:
- Endless green tunnels.
- Giant trees above the clouds.
- Colossal forests and natural bridges.
- Floating islands and fantasy lakes.
- Waterfall valleys and extraordinary landscapes.
- Giant natural formations.
- Fantasy landscapes that still look physically believable.

CATEGORY D — FANTASY ARCHITECTURE & FUTURISTIC CIVILIZATIONS

Explore:
- Fantasy city ships and futuristic city ships.
- Floating ocean cities.
- Sky gardens and waterfall cities.
- Forest-integrated cities.
- Giant buildings above clouds.
- Fantasy castles, bridges and mega structures.
- Advanced civilizations surrounded by nature.

Fantasy architecture and futuristic cities are additional
categories. They must NOT replace Bengal village life,
human activity, nature and travel content.

==================================================
SECTION 4 — CONTENT ROTATION
==================================================

Maintain variety between reels.

Avoid repeating the same location, visual hook,
story concept or category unnecessarily.

Balance:
- Bengal village life.
- India and world nature.
- Human activity and struggle.
- Fantasy nature.
- Fantasy architecture and futuristic civilizations.

Do not make every reel about fantasy cities.
Do not make every reel about monsoon.
Do not force human characters into every scene.

==================================================
SECTION 5 — VISUAL STYLE
==================================================

Use photorealistic cinematic visuals.

Bengal village and documentary scenes:
Natural documentary realism.

Fantasy nature:
Epic photorealistic natural fantasy.

Fantasy architecture:
Photorealistic futuristic fantasy.

Use:
- Realistic lighting and shadows.
- Detailed natural textures.
- Believable perspective and scale.
- Natural movement and physics.
- Rich but realistic colours.
- Cinematic depth and atmosphere.

Avoid:
- Plastic-looking CGI.
- Toy-like buildings.
- Cartoon appearance.
- Cheap artificial 3D appearance.
- Excessive saturation.
- Unnatural morphing.
- Distorted objects and architecture.
- Unbelievable movement.

==================================================
SECTION 6 — STANDARD REEL FORMAT
==================================================

Format: Vertical 9:16.
Total scenes: 5.
Duration per scene: approximately 8 seconds.
Total duration: approximately 40 seconds.

Production prompts must be suitable for:
- Google Flow AI.
- Nano Banana Pro.
- Image-to-video workflows.

==================================================
SECTION 7 — TOPIC DEVELOPMENT
==================================================

Create a visually powerful topic with:
- A strong visual hook.
- A clear location or environment.
- A coherent five-scene story.
- A memorable cinematic highlight.
- A satisfying final reveal.

Avoid generic and repetitive ideas.

==================================================
SECTION 8 — MANDATORY REEL HEADER
==================================================

Start every reel with:

REEL NUMBER — TITLE
Tropic:
Sub-Category:
Location:
Format:
Duration:
Main Focus:
Story Flow:
Visual Style:

Explain the concept in Bengali.

==================================================
SECTION 9 — GLOBAL VISUAL BIBLE
==================================================

Before Scene 1 establish:

1. Main Subject Lock
2. Character Lock
3. Location Lock
4. Environment Lock
5. Colour Lock
6. Lighting Lock
7. Material & Texture Lock
8. Motion Lock

If there are no human characters, clearly state that.

Maintain the same main environment and visual identity
throughout the five scenes.

==================================================
SECTION 10 — FIVE-SCENE STORY STRUCTURE
==================================================

Scene 1 — Discovery Hook.
Scene 2 — Grand Reveal.
Scene 3 — Exploration or Activity.
Scene 4 — Cinematic Highlight.
Scene 5 — Ultimate Reveal and Ending.

Timing:
Scene 1: 0–8 seconds.
Scene 2: 8–16 seconds.
Scene 3: 16–24 seconds.
Scene 4: 24–32 seconds.
Scene 5: 32–40 seconds.

==================================================
SECTION 11 — COMPLETE SCENE STRUCTURE
==================================================

EVERY scene MUST contain all these sections:

1. Story Purpose — Bengali explanation.
2. Image/Video Prompt — detailed English production prompt.
3. Camera — camera type, lens feel and framing.
4. Camera Movement — exact camera movement.
5. Subject Movement — exact subject movement.
6. Environment Movement — natural environmental movement.
7. Sound Effects — specific sound effects.
8. Ambient Sound — background environmental sound.
9. Transition — connection to the next scene.
10. Planned Exit State — exact ending state.

Never omit any section.

Every Image/Video Prompt must be detailed,
self-contained and ready to use.

Avoid contradictory instructions.
Keep one primary action per scene.

==================================================
SECTION 12 — CONTINUITY LOCK
==================================================

Maintain continuity of:
- Characters and clothing.
- Animals and their appearance.
- Location and geography.
- Architecture and natural structures.
- Weather and atmosphere.
- Colour and lighting.
- Camera perspective and movement.

Each scene must connect naturally to the next.

==================================================
SECTION 13 — FLOW AI PROMPT ENGINEERING
==================================================

Use clear, natural English.

Specify:
- What is visible.
- What moves.
- How the camera moves.
- How the environment moves.
- How the scene ends.

Use believable physics and natural motion.
Keep prompts suitable for Flow AI.
Avoid contradictory instructions.

==================================================
SECTION 14 — PRODUCTION WORKFLOW
==================================================

Follow this order:

1. Develop the topic.
2. Establish the Global Visual Bible.
3. Build the five-scene story.
4. Write all five production prompts.
5. Review continuity.
6. Prepare prompts for image generation.
7. Prepare prompts for Flow AI video generation.
8. Perform final quality review.

Do not claim to generate actual images or videos
unless an image/video generation tool is connected.

==================================================
SECTION 15 — AUDIO DESIGN
==================================================

Include sound effects and ambient sound in every scene.

Create a complete audio flow across the reel.

Default:
No voice-over unless requested.

If narration is requested:
- Put the exact spoken line inside the corresponding scene.
- Specify narration or in-scene dialogue.
- Specify delivery style.
- Specify exact timing.
- Keep the spoken line inside that scene's Image/Video Prompt.

==================================================
SECTION 16 — FINAL QUALITY AUDIT
==================================================

Check:
- Strong opening hook.
- Clear five-scene story.
- Complete scene structure.
- Visual consistency.
- Realistic motion.
- No unnecessary repetition.
- Strong final scene.
- Flow AI compatibility.
- Correct 9:16 format.
- Approximately 40 seconds.

==================================================
SECTION 17 — SOCIAL MEDIA OUTPUT
==================================================

At the end include:
1. Facebook Reel Caption.
2. Relevant Hashtags.
3. Short memorable title.

==================================================
SECTION 18 — LANGUAGE RULE
==================================================

Explanations must be in Bengali.
Production prompts must be in English.

Do not shorten important production details.
Do not omit scene sections.
Do not ask unnecessary questions.

==================================================
SECTION 19 — COMMAND SYSTEM
==================================================

NEXT:
Create a fresh topic after reviewing available history.

TOPIC:
Develop a reel from the given topic.

CHANGE:
Change the requested element while preserving other details.

REGENERATE:
Regenerate the requested scene or section.

CONTINUE:
Continue the existing project.

MASTER PROMPT REVIEW:
Review the project rules and structure.

==================================================
SECTION 20 — CONTINUOUS PROJECT IDENTITY
==================================================

This is one continuous creative project.

Bengal remains the main base.
India and world nature provide geographical variety.
Human activity, village life, struggle, travel and discovery
remain essential project themes.

Fantasy nature and futuristic city ships are additional
creative categories, not replacements for the original DNA.

REFERENCE IMAGE RULE:
When a reference image is uploaded:
- Carefully analyse the visible subject.
- Identify location type, shapes, colours and atmosphere.
- Understand the visual composition.
- Develop a new five-scene story based on the reference.
- Preserve the main visual identity.
- Do not simply copy one static image into five scenes.
- Create cinematic progression and meaningful movement.

FINAL INSTRUCTION:
Always deliver a complete, production-ready five-scene reel.

Include:
- Reel header.
- Bengali concept explanation.
- Global Visual Bible.
- Five complete scenes.
- Every required scene section.
- Continuity locks.
- Complete audio flow.
- Final Quality Audit.
- Facebook caption and hashtags.

Never silently replace the project's original identity.
"""


# =========================================================
# 4. SESSION STATE
# =========================================================

defaults = {
    "selected_topic": "",
    "suggestions": [],
    "used_topics": [],
    "reel_history": [],
    "generated_reel": "",
    "last_topic": "",
    "topic_mode": "নিজে Topic লিখব",
    "request_in_flight": False,
    "last_request_fingerprint": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 5. FAST TOPIC FUNCTIONS
# =========================================================

def get_new_topic():
    used = st.session_state.used_topics

    available = [
        item for item in TOPIC_LIBRARY
        if item[1] not in used
    ]

    if not available:
        st.session_state.used_topics = []
        available = TOPIC_LIBRARY.copy()

    selected = random.choice(available)
    st.session_state.used_topics.append(selected[1])

    return selected


def get_ten_topics():
    used = st.session_state.used_topics

    available = [
        item for item in TOPIC_LIBRARY
        if item[1] not in used
    ]

    if len(available) < 10:
        available = TOPIC_LIBRARY.copy()

    return random.sample(available, 10)


# =========================================================
# 6. GEMINI CLIENT
# =========================================================

@st.cache_resource
def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)


def get_api_key():
    try:
        key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        raise RuntimeError(
            "GEMINI_API_KEY পাওয়া যায়নি। "
            "Streamlit Settings > Secrets পরীক্ষা করো।"
        )

    if not key or not str(key).strip():
        raise RuntimeError("GEMINI_API_KEY খালি আছে।")

    return str(key).strip()


# =========================================================
# 7. GEMINI GENERATION — one fixed model, one explicit request
# =========================================================

MODEL_NAME = "gemini-3.8-flash"


def quota_message(error):
    raw = str(error)
    match = re.search(r"retry in\s+(?:(\d+)h)?(?:(\d+)m)?([\d.]+)s", raw, re.I)
    if match:
        total = int(match.group(1) or 0) * 3600 + int(match.group(2) or 0) * 60 + int(float(match.group(3) or 0))
        parts = []
        if total >= 3600:
            parts.append(f"{total // 3600} ঘণ্টা")
        if total % 3600 >= 60:
            parts.append(f"{(total % 3600) // 60} মিনিট")
        if total % 60 or not parts:
            parts.append(f"{total % 60} সেকেন্ড")
        return "Gemini-র Free Tier quota আপাতত শেষ। আনুমানিক " + " ".join(parts) + " পরে আবার চেষ্টা করো।"
    return "Gemini-র Free Tier quota আপাতত শেষ বা সাময়িক সীমায় পৌঁছেছে। Google-এর quota reset হওয়া পর্যন্ত অপেক্ষা করে আবার চেষ্টা করো।"


def ask_gemini(prompt, uploaded_image=None):
    client = genai.Client(api_key=get_api_key())
    contents = [prompt]
    if uploaded_image is not None:
        contents.append(uploaded_image)
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=contents)
        result = response.text
        if not result or not result.strip():
            raise RuntimeError("Gemini কোনো লেখা উত্তর দেয়নি। আবার চেষ্টা করো।")
        return result
    except Exception as error:
        message = str(error)
        if "429" in message or "RESOURCE_EXHAUSTED" in message or "quota" in message.lower():
            raise RuntimeError(quota_message(error)) from None
        raise RuntimeError("Gemini-তে অনুরোধটি সম্পন্ন হয়নি। ইন্টারনেট সংযোগ বা Google AI Studio-র সেবা পরীক্ষা করে কিছুক্ষণ পর আবার চেষ্টা করো।") from None


# =========================================================
# 9. BUILD REEL REQUEST
# =========================================================

def build_reel_request(topic, extra_instruction, image_present):

    history = st.session_state.reel_history[-10:]

    history_text = "\n".join(
        f"- {item}" for item in history
    )

    if not history_text:
        history_text = "No previous reel history."

    prompt = f"""
{MASTER_PROMPT}

==================================================
CURRENT REEL REQUEST
==================================================

TOPIC:
{topic}

ADDITIONAL USER INSTRUCTION:
{extra_instruction if extra_instruction.strip() else "No additional instruction."}

PREVIOUS REEL TOPICS:
{history_text}

REFERENCE IMAGE:
{"A reference image is attached. Carefully analyse it and build the reel around its visual identity." if image_present else "No reference image attached."}

IMPORTANT OUTPUT INSTRUCTIONS:

1. Create one complete five-scene reel.
2. Review the previous topics and avoid unnecessary repetition.
3. Explain the concept in Bengali.
4. Write production prompts in English.
5. Include the complete Global Visual Bible.
6. Include all ten required sections in EVERY scene.
7. Keep the five scenes connected as one continuous story.
8. Include continuity locks, audio flow and final quality audit.
9. Include Facebook caption and hashtags.
10. Do not omit any section.
11. Make every Image/Video Prompt detailed and self-contained.
12. Keep the output suitable for Flow AI.
13. Do not claim an actual video has been generated.

Now generate the complete reel.
"""

    return prompt


# =========================================================
# 10. APP TOPIC SELECTION
# =========================================================

st.divider()
st.subheader("1️⃣ Reel Topic নির্বাচন করো")

topic_mode = st.radio(
    "কীভাবে Topic দিতে চাও?",
    [
        "নিজে Topic লিখব",
        "AI থেকে 10টি Topic নেব",
        "Reference Image Upload করব"
    ],
    horizontal=False,
    key="topic_mode"
)

topic_input = ""
reference_image = None


# ---------------------------------------------------------
# MODE A — MANUAL TOPIC
# ---------------------------------------------------------

if topic_mode == "নিজে Topic লিখব":

    topic_input = st.text_input(
        "তোমার Reel Topic লিখো",
        value=st.session_state.selected_topic,
        placeholder="Example: Endless Green Village Road Tunnel"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎲 NEXT — নতুন Topic", use_container_width=True):
            category, topic = get_new_topic()
            st.session_state.selected_topic = topic
            st.rerun()

    with col2:
        if st.button("🧹 Clear Topic", use_container_width=True):
            st.session_state.selected_topic = ""
            st.rerun()


# ---------------------------------------------------------
# MODE B — TOPIC LIBRARY
# ---------------------------------------------------------

elif topic_mode == "AI থেকে 10টি Topic নেব":

    st.caption(
        "দ্রুত কাজ করার জন্য Topic Library ব্যবহার করা হচ্ছে। "
        "এতে Gemini API call লাগে না।"
    )

    if st.button(
        "✨ Get 10 Topic Ideas",
        use_container_width=True
    ):
        st.session_state.suggestions = get_ten_topics()
        st.rerun()

    if st.session_state.suggestions:

        selected = st.selectbox(
            "একটি Topic বেছে নাও",
            options=st.session_state.suggestions,
            format_func=lambda item: f"{item[0]} | {item[1]}"
        )

        topic_input = selected[1]

        st.write(f"**Selected Topic:** {topic_input}")

        if st.button("🎲 NEXT — অন্য 10টি Topic", use_container_width=True):
            st.session_state.suggestions = get_ten_topics()
            st.rerun()

    else:
        st.info("Get 10 Topic Ideas চাপো।")


# ---------------------------------------------------------
# MODE C — REFERENCE IMAGE
# ---------------------------------------------------------

else:

    uploaded_file = st.file_uploader(
        "Reference Image Upload করো",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file is not None:

        try:
            reference_image = Image.open(uploaded_file).convert("RGB")

            st.image(
                reference_image,
                caption="Uploaded Reference Image",
                use_container_width=True
            )

            topic_input = st.text_input(
                "ছবির জন্য Topic / নির্দেশনা",
                placeholder="Create a cinematic reel inspired by this image"
            )

            if not topic_input.strip():
                topic_input = (
                    "Create a cinematic five-scene reel "
                    "inspired by the uploaded reference image."
                )

        except Exception as error:
            st.error("ছবিটি খোলা যাচ্ছে না। অন্য ছবি Upload করো।")
            st.code(str(error))


# =========================================================
# 11. ADDITIONAL INSTRUCTIONS
# =========================================================

st.divider()
st.subheader("2️⃣ অতিরিক্ত নির্দেশনা (ঐচ্ছিক)")

extra_instruction = st.text_area(
    "বিশেষ নির্দেশনা থাকলে লিখো",
    placeholder=(
        "Example: Make the green road tunnel thicker, "
        "rounder and more beautiful. Keep the visuals realistic."
    ),
    height=100
)


# =========================================================
# 12. GENERATE REEL
# =========================================================

st.divider()
st.subheader("3️⃣ সম্পূর্ণ Reel Prompt তৈরি করো")

if st.button(
    "🚀 GENERATE COMPLETE REEL",
    type="primary",
    use_container_width=True,
    disabled=st.session_state.request_in_flight
):

    if not topic_input or not topic_input.strip():
        st.error("প্রথমে একটি Topic নির্বাচন বা লিখে নাও।")

    else:

        prompt = build_reel_request(topic=topic_input, extra_instruction=extra_instruction, image_present=reference_image is not None)
        image_bytes = reference_image.tobytes() if reference_image is not None else b""
        fingerprint = hashlib.sha256(prompt.encode("utf-8") + image_bytes).hexdigest()
        if fingerprint == st.session_state.last_request_fingerprint:
            st.info("এই একই Topic ও নির্দেশনার Reel ইতিমধ্যে তৈরি হয়েছে। নতুন অনুরোধ করতে Topic বা নির্দেশনা বদলাও।")
        elif st.session_state.request_in_flight:
            st.info("অনুরোধটি ইতিমধ্যে চলছে। একটু অপেক্ষা করো।")
        else:
            st.session_state.request_in_flight = True
            st.session_state.last_request_fingerprint = fingerprint
            with st.spinner("Gemini-তে একটি Reel তৈরি হচ্ছে..."):
                try:

                    result = ask_gemini(
                    prompt=prompt,
                    uploaded_image=reference_image
                )

                    st.session_state.generated_reel = result
                    st.session_state.last_topic = topic_input

                    if topic_input not in st.session_state.reel_history:
                        st.session_state.reel_history.append(topic_input)
                    st.success("সম্পূর্ণ Reel Prompt তৈরি হয়েছে!")
                except Exception as error:
                    st.session_state.generated_reel = ""
                    st.session_state.last_request_fingerprint = ""
                    st.error(str(error))
                finally:
                    st.session_state.request_in_flight = False


# =========================================================
# 13. DISPLAY RESULT
# =========================================================

if st.session_state.generated_reel:

    st.divider()
    st.subheader("🎬 তোমার সম্পূর্ণ Reel Production Prompt")

    st.markdown(st.session_state.generated_reel)

    safe_name = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        st.session_state.last_topic
    ).strip("_")

    if not safe_name:
        safe_name = "bengal_reel"

    file_content = (
        "TOPIC: "
        + st.session_state.last_topic
        + "\n\n"
        + st.session_state.generated_reel
    )

    st.download_button(
        "📥 Download Complete Reel Prompt",
        data=file_content,
        file_name=f"{safe_name}.txt",
        mime="text/plain",
        use_container_width=True
    )

    if st.button("🗑️ Clear Generated Reel", use_container_width=True):
        st.session_state.generated_reel = ""
        st.session_state.last_topic = ""
        st.rerun()


# =========================================================
# 14. RECENT HISTORY
# =========================================================

st.divider()

with st.expander("📚 Recent Reel Topic History"):

    if st.session_state.reel_history:

        for index, item in enumerate(
            reversed(st.session_state.reel_history[-20:]),
            start=1
        ):
            st.write(f"{index}. {item}")

    else:
        st.info("এখনও কোনো Reel তৈরি করা হয়নি।")


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.caption(
    "Bengal AI Content Creator | "
    "Bengal + India + World Nature & Human Life"
)

st.caption(
    "This app generates production prompts. "
    "Actual image and video generation requires a connected tool."
)
