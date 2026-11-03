
import streamlit as st
import random
import re
from io import BytesIO
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

APP_TITLE = "Bengal AI Content Creator"

MODEL_LIST = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-2.5-flash"
]


# =========================================================
# 2. MASTER PROMPT
# =========================================================

MASTER_PROMPT = """
You are an elite AI Reel Director, Concept Developer,
Documentary Filmmaker, Nature Cinematographer,
Human-Life Storyteller, Fantasy Designer, Screenwriter,
Storyboard Artist, AI Prompt Engineer and Social Media Strategist.

PROJECT NAME:
BENGAL + INDIA + WORLD NATURE & HUMAN LIFE REEL PROJECT

PROJECT DNA:
NATURE + HUMAN LIFE + ACTIVITY / STRUGGLE
+ TRAVEL / DISCOVERY + FANTASY.

Nature remains the primary focus. Human beings should appear
as part of the environment, not necessarily as the main hero.

==================================================
SECTION 1: FOUR CONTENT CATEGORIES
==================================================

CATEGORY A — BENGAL VILLAGE LIFE & NATURE

Explore:
- Bengal village life and rural landscapes.
- Farming, fishing, harvesting and village work.
- Human struggle, travel and everyday activities.
- Mud roads, brick roads and village pathways.
- Giant banyan trees and green tree tunnels.
- Coconut and areca palm roads.
- Bamboo paths and pond-side roads.
- Rivers, canals, ponds and wetlands.
- Paddy fields, mustard fields, kash flowers and shiuli flowers.
- Village monsoon, dramatic clouds and heavy rain.
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
- Endless green road tunnels.
- Giant trees above the clouds.
- Colossal forests and natural bridges.
- Floating islands and fantasy lakes.
- Waterfall valleys and extraordinary landscapes.
- Giant natural formations.

Fantasy is allowed, but the visual result must feel believable,
photorealistic and physically convincing.

CATEGORY D — FANTASY ARCHITECTURE & FUTURISTIC CIVILIZATIONS

Explore:
- Fantasy city ships and futuristic city ships.
- Floating ocean cities.
- Sky gardens and waterfall cities.
- Forest-integrated cities.
- Giant buildings above clouds.
- Fantasy castles, bridges and mega structures.
- Advanced civilizations surrounded by nature.

These are additional categories.
They must NOT replace Bengal village life,
human activity, nature and travel content.

==================================================
SECTION 2: CONTENT ROTATION
==================================================

Create variety across different reels.

Review the available previous reel history.
Avoid repeating the same location, visual hook,
story concept or category unnecessarily.

Maintain a healthy balance between:
- Bengal village life.
- India and world nature.
- Human activity and struggle.
- Fantasy nature.
- Fantasy architecture and futuristic civilizations.

Do not make every reel about fantasy cities.
Do not make every reel about monsoon.
Do not force human characters into every scene.

==================================================
SECTION 3: VISUAL STYLE
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
SECTION 4: STANDARD REEL FORMAT
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
SECTION 5: TOPIC DEVELOPMENT
==================================================

Create a visually powerful topic.

The topic must have:
- A strong visual hook.
- A clear location or environment.
- A coherent five-scene story.
- A memorable cinematic highlight.
- A satisfying final reveal.

Avoid generic and repetitive ideas.

==================================================
SECTION 6: MANDATORY REEL HEADER
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
SECTION 7: GLOBAL VISUAL BIBLE
==================================================

Before Scene 1, establish:

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
SECTION 8: FIVE-SCENE STORY STRUCTURE
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
SECTION 9: COMPLETE SCENE STRUCTURE
==================================================

Every scene MUST contain all these sections:

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
SECTION 10: CONTINUITY LOCK
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
SECTION 11: FLOW AI PROMPT ENGINEERING
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
Avoid unnecessarily sensitive or ambiguous wording.

==================================================
SECTION 12: PRODUCTION WORKFLOW
==================================================

Follow this order:

1. Develop the topic.
2. Establish the Global Visual Bible.
3. Build the five-scene story.
4. Write all five production prompts.
5. Review continuity.
6. Prepare the prompts for image generation.
7. Prepare the prompts for Flow AI video generation.
8. Perform final quality review.

Do not claim to generate actual images or videos
unless an image/video generation tool is connected.

==================================================
SECTION 13: AUDIO DESIGN
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
SECTION 14: FINAL QUALITY AUDIT
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
SECTION 15: SOCIAL MEDIA OUTPUT
==================================================

At the end include:

1. Facebook Reel Caption.
2. Relevant Hashtags.
3. Short memorable title.

==================================================
SECTION 16: LANGUAGE RULE
==================================================

Explanations must be in Bengali.
Production prompts must be in English.

Do not shorten important production details.
Do not omit scene sections.
Do not ask unnecessary questions.

==================================================
SECTION 17: COMMAND SYSTEM
==================================================

NEXT:
Create a fresh topic after reviewing the available history.

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
SECTION 18: CONTINUOUS PROJECT IDENTITY
==================================================

This is one continuous creative project.

Bengal remains the main base.
India and world nature provide geographical variety.
Human activity, village life, struggle, travel and discovery
remain essential project themes.

Fantasy nature and futuristic city ships are additional
creative categories, not replacements for the original DNA.

==================================================
SECTION 19: REFERENCE IMAGE RULE
==================================================

When a reference image is uploaded:
- Carefully analyse the visible subject.
- Identify the location type, shapes, colours and atmosphere.
- Understand the visual composition.
- Develop a new five-scene story based on the reference.
- Preserve the main visual identity.
- Do not simply copy one static image into five scenes.
- Create cinematic progression and meaningful movement.

==================================================
SECTION 20: FINAL INSTRUCTION
==================================================

Always deliver a complete, production-ready five-scene reel.

The output must contain:
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
# 3. TOPIC LIBRARY
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

    ("Fantasy Architecture", "A Giant City Ship Sailing Across the Ocean"),
    ("Fantasy Architecture", "A Futuristic City Built Around Giant Trees"),
    ("Fantasy Architecture", "A Floating City Above the Clouds"),
    ("Fantasy Architecture", "A Waterfall City Inside a Mountain Valley"),
    ("Fantasy Architecture", "A Giant Sky Garden Civilization"),
    ("Fantasy Architecture", "A Fantasy Harbour with Colossal Ships"),
    ("Fantasy Architecture", "A Forest Civilization Connected by Bridges"),
    ("Fantasy Architecture", "A Grand Castle Above a Sea of Clouds"),
    ("Fantasy Architecture", "A Futuristic Ocean City at Sunrise"),
    ("Fantasy Architecture", "A Giant Ship Carrying a Beautiful Green City")
]


def get_fresh_topic():
    used = st.session_state.used_topics
    available = [item for item in TOPIC_LIBRARY if item[1] not in used]

    if not available:
        st.session_state.used_topics = []
        available = TOPIC_LIBRARY.copy()

    selected = random.choice(available)
    st.session_state.used_topics.append(selected[1])
    return selected


# =========================================================
# 4. GEMINI CONNECTION
# =========================================================

def get_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        raise RuntimeError(
            "GEMINI_API_KEY পাওয়া যায়নি। "
            "Streamlit Settings-এর Secrets অংশ পরীক্ষা করো।"
        )

    if not api_key:
        raise RuntimeError("Gemini API Key খালি আছে।")

    return genai.Client(api_key=api_key)


def ask_gemini(prompt, image=None):
    client = get_client()

    contents = [prompt]

    if image is not None:
        contents.append(image)

    last_error = None

    for model in MODEL_LIST:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )

            result = response.text

            if result and result.strip():
                return result

        except Exception as error:
            last_error = error
            error_text = str(error).lower()

            # API key / permission errors should not be hidden
            if "api key" in error_text or "permission" in error_text:
                raise RuntimeError(
                    "API Key বা Permission সংক্রান্ত সমস্যা হয়েছে। "
                    "Streamlit Secrets এবং Google AI Studio পরীক্ষা করো।"
                )

            # Try the next model for temporary model errors
            continue

    raise RuntimeError(
        "Gemini-র কোনো Model বর্তমানে উত্তর দিতে পারছে না। "
        "কিছুক্ষণ পরে আবার চেষ্টা করো। "
        f"শেষ Error: {last_error}"
    )


# =========================================================
# 5. TOPIC SUGGESTIONS
# =========================================================

def get_topic_suggestions():
    prompt = """
    Suggest exactly 10 fresh and visually powerful topics
    for the Bengal + India + World Nature & Human Life Reel Project.

    Include a balanced mixture of:
    Bengal village life, India/world nature,
    human activity, fantasy nature,
    fantasy architecture and futuristic city ships.

    Avoid generic and repetitive topics.

    Return exactly 10 lines in this format:
    Category | Topic

    No introduction or extra explanation.
    """

    result = ask_gemini(prompt)

    suggestions = []

    for line in result.splitlines():
        line = line.strip()
        if "|" in line:
            category, topic = line.split("|", 1)
            if topic.strip():
                suggestions.append((category.strip(), topic.strip()))

    return suggestions[:10]


def fallback_suggestions():
    used = st.session_state.used_topics
    available = [item for item in TOPIC_LIBRARY if item[1] not in used]

    if len(available) < 10:
        available = TOPIC_LIBRARY.copy()

    return random.sample(available, min(10, len(available)))


# =========================================================
# 6. REEL GENERATION
# =========================================================

def build_reel_prompt(topic, extra_instruction, history, reference_image=False):

    history_text = "\n".join(history[-10:]) if history else "No previous reels."

    prompt = f"""
{MASTER_PROMPT}

==================================================
CURRENT REEL REQUEST
==================================================

Topic:
{topic}

Additional user instruction:
{extra_instruction if extra_instruction else "No additional instruction."}

Previous reel history:
{history_text}

Reference image supplied:
{"Yes. Analyse the uploaded image carefully." if reference_image else "No."}

IMPORTANT:
1. Create a completely new five-scene reel.
2. Do not repeat previous topics unnecessarily.
3. Explain the concept and story purpose in Bengali.
4. Write all production prompts in detailed English.
5. Every scene must contain all 10 mandatory sections.
6. Do not skip the Global Visual Bible.
7. Include continuity, complete audio flow and final quality audit.
8. Finish with a Facebook caption and hashtags.
9. Output must be ready for Flow AI image-to-video production.
10. Do not claim that an actual video has been generated.

Now create the complete production-ready reel.
"""

    return prompt


def generate_reel(topic, extra_instruction, image=None):
    history = st.session_state.reel_history

    prompt = build_reel_prompt(
        topic=topic,
        extra_instruction=extra_instruction,
        history=history,
        reference_image=image is not None
    )

    return ask_gemini(prompt, image=image)


# =========================================================
# 7. SESSION STATE
# =========================================================

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "reel_history" not in st.session_state:
    st.session_state.reel_history = []

if "used_topics" not in st.session_state:
    st.session_state.used_topics = []

if "generated_reel" not in st.session_state:
    st.session_state.generated_reel = ""

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""


# =========================================================
# 8. APP HEADER
# =========================================================

st.title("🎬 Bengal AI Content Creator")

st.markdown(
    """
    **তোমার Bengal + India + World Nature & Human Life Reel Studio**

    Topic লিখে অথবা Reference Image Upload করে
    সম্পূর্ণ ৫-Scene AI Reel Production Prompt তৈরি করো।
    """
)

st.divider()


# =========================================================
# 9. TOPIC SELECTION
# =========================================================

st.subheader("1️⃣ Reel Topic নির্বাচন করো")

topic_mode = st.radio(
    "কীভাবে Topic দিতে চাও?",
    [
        "নিজে Topic লিখব",
        "AI থেকে 10টি Topic নেব",
        "Reference Image Upload করব"
    ]
)

reference_image = None
topic_input = ""
extra_instruction = ""


# ---------------------------------------------------------
# MODE A: MANUAL TOPIC
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
            category, topic = get_fresh_topic()
            st.session_state.selected_topic = topic
            st.rerun()

    with col2:
        if st.button("🧹 Topic Clear", use_container_width=True):
            st.session_state.selected_topic = ""
            st.rerun()

    if topic_input:
        st.caption(f"Selected Topic: {topic_input}")


# ---------------------------------------------------------
# MODE B: AI TOPIC SUGGESTIONS
# ---------------------------------------------------------

elif topic_mode == "AI থেকে 10টি Topic নেব":

    if st.button("✨ Get 10 Topic Ideas", use_container_width=True):
        with st.spinner("নতুন Topic তৈরি হচ্ছে..."):
            try:
                st.session_state.suggestions = get_topic_suggestions()
                st.success("AI Topic Suggestions তৈরি হয়েছে।")

            except Exception as error:
                st.warning(
                    "AI Topic তৈরি করা যায়নি। "
                    "এবার Offline Topic Library থেকে দেখানো হচ্ছে।"
                )
                st.session_state.suggestions = fallback_suggestions()

                with st.expander("Error Details"):
                    st.code(str(error))

    if st.session_state.suggestions:

        selected = st.selectbox(
            "একটি Topic বেছে নাও",
            options=st.session_state.suggestions,
            format_func=lambda x: f"{x[0]} | {x[1]}"
        )

        topic_input = selected[1]

        st.write(f"**Selected Topic:** {topic_input}")

        if st.button("🎲 NEXT — অন্য Topic", use_container_width=True):
            category, topic = get_fresh_topic()
            st.session_state.suggestions = [(category, topic)]
            st.rerun()


# ---------------------------------------------------------
# MODE C: IMAGE REFERENCE
# ---------------------------------------------------------

else:

    uploaded_file = st.file_uploader(
        "Reference Image Upload করো",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file is not None:
        reference_image = Image.open(uploaded_file).convert("RGB")

        st.image(
            reference_image,
            caption="Uploaded Reference Image",
            use_container_width=True
        )

        topic_input = st.text_input(
            "ছবির জন্য Topic / নির্দেশনা",
            placeholder="Example: Create a five-scene reel inspired by this image"
        )

        if not topic_input:
            topic_input = "Create a cinematic five-scene reel inspired by the uploaded reference image."


# =========================================================
# 10. ADDITIONAL INSTRUCTIONS
# =========================================================

st.divider()

st.subheader("2️⃣ অতিরিক্ত নির্দেশনা (ঐচ্ছিক)")

extra_instruction = st.text_area(
    "কোনো বিশেষ নির্দেশনা থাকলে লিখো",
    placeholder=(
        "Example: Make the green road tunnel thicker, "
        "rounder and more beautiful. Keep the visuals realistic."
    ),
    height=100
)


# =========================================================
# 11. GENERATE REEL
# =========================================================

st.divider()

st.subheader("3️⃣ সম্পূর্ণ Reel Prompt তৈরি করো")

if st.button("🚀 GENERATE COMPLETE REEL", type="primary", use_container_width=True):

    if not topic_input.strip():
        st.error("প্রথমে একটি Topic নির্বাচন বা লিখে নাও।")

    else:
        with st.spinner(
            "তোমার সম্পূর্ণ ৫-Scene Reel তৈরি হচ্ছে। "
            "কিছুক্ষণ অপেক্ষা করো..."
        ):

            try:
                result = generate_reel(
                    topic=topic_input,
                    extra_instruction=extra_instruction,
                    image=reference_image
                )

                st.session_state.generated_reel = result
                st.session_state.last_topic = topic_input

                if topic_input not in st.session_state.reel_history:
                    st.session_state.reel_history.append(topic_input)

                st.success("তোমার Reel Prompt তৈরি হয়েছে!")

            except Exception as error:
                st.error("Reel তৈরি করা যায়নি।")

                st.warning(
                    "Gemini Model ব্যস্ত থাকতে পারে, "
                    "API quota শেষ হতে পারে অথবা সংযোগে সমস্যা হতে পারে। "
                    "কিছুক্ষণ পরে আবার চেষ্টা করো।"
                )

                with st.expander("Error Details"):
                    st.code(str(error))


# =========================================================
# 12. DISPLAY GENERATED REEL
# =========================================================

if st.session_state.generated_reel:

    st.divider()

    st.subheader("🎬 তোমার সম্পূর্ণ Reel Production Prompt")

    st.markdown(st.session_state.generated_reel)

    file_content = (
        f"TOPIC: {st.session_state.last_topic}\n\n"
        + st.session_state.generated_reel
    )

    safe_name = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        st.session_state.last_topic
    ).strip("_")

    if not safe_name:
        safe_name = "bengal_reel"

    st.download_button(
        label="📥 Download Complete Reel Prompt",
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
# 13. RECENT TOPIC HISTORY
# =========================================================

st.divider()

with st.expander("📚 Recent Reel Topic History"):

    if st.session_state.reel_history:

        for index, topic in enumerate(
            reversed(st.session_state.reel_history[-20:]),
            start=1
        ):
            st.write(f"{index}. {topic}")

    else:
        st.info("এখনও কোনো Reel তৈরি করা হয়নি।")


# =========================================================
# 14. FOOTER
# =========================================================

st.divider()

st.caption(
    "Bengal AI Content Creator | "
    "Bengal + India + World Nature & Human Life"
)

st.caption(
    "This app creates AI production prompts. "
    "Actual image and video generation requires a connected generation tool."
)
