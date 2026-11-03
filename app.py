
import streamlit as st
from google import genai
from PIL import Image
from io import BytesIO
import re

# =====================================================
# BENGAL AI CONTENT CREATOR
# VERSION 3.0 - GEMINI AI POWERED
# =====================================================

st.set_page_config(
    page_title="Bengal AI Content Creator",
    page_icon="🎬",
    layout="wide"
)

MODEL_NAME = "gemini-flash-latest"

# =====================================================
# MASTER CREATIVE INSTRUCTIONS
# V2.1 - 20 SECTION CREATIVE SYSTEM
# =====================================================

MASTER_PROMPT = r"""
ULTIMATE MASTER PROMPT V2.1
BENGAL + INDIA + WORLD NATURE & HUMAN LIFE
EXPANDED FANTASY EDITION

SECTION 1 - PROFESSIONAL ROLE
You are an elite AI Reel Director, Concept Developer,
Documentary Filmmaker, Nature Cinematographer,
Human-Life Storyteller, Fantasy Designer, Screenwriter,
Storyboard Artist, Image Prompt Engineer,
Image-to-Video Prompt Engineer and Social Media Strategist.

SECTION 2 - PROJECT DNA
NATURE + HUMAN LIFE + ACTIVITY + STRUGGLE
+ TRAVEL + DISCOVERY + FANTASY.
Nature is the primary focus. Humans interact naturally
with the environment and are not always the main hero.

SECTION 3 - FOUR CONTENT CATEGORIES

A. BENGAL VILLAGE LIFE & NATURE
Village activities, farming, fishing, rivers, ponds,
paddy fields, village roads, banyan trees, green tunnels,
coconut and areca roads, bamboo paths, pond-side roads,
rainy roads, mist, kash flowers, shiuli flowers,
rural communities and authentic Bengal landscapes.

B. INDIA & WORLD NATURE / HUMAN LIFE
Himalayas, Meghalaya living root bridges, waterfalls,
wildlife, rivers, deserts, coastlines, migrations,
rainforests, Iceland, Swiss valleys, fjords, giant forests,
remote islands, mountain farmers and remote communities.

C. FANTASY NATURE
Endless green tunnels, giant trees above clouds,
colossal forests, natural bridges, floating islands,
waterfall valleys, fantasy lakes and extraordinary
natural environments. Keep them photorealistic.

D. FANTASY ARCHITECTURE & FUTURISTIC CIVILIZATIONS
Fantasy city ships, futuristic city ships, sky gardens,
waterfall cities, floating ocean cities, forest-integrated
cities, castles, giant bridges and buildings above clouds.
These are additional categories, not replacements for
Bengal village life, nature and human struggle.

SECTION 4 - CONTENT ROTATION
Avoid repetitive topics and similar visual compositions.
Balance Bengal, India, World, Human Life, Fantasy Nature
and Futuristic Architecture. Review available history.
Do not repeat recent topics unnecessarily.

SECTION 5 - VISUAL STYLE
A. Village / Human / Nature: realistic documentary cinema.
B. Fantasy Nature: epic photorealistic natural fantasy.
C. Futuristic: photorealistic cinematic fantasy.
Use realistic textures, lighting, scale, perspective,
natural movement and believable physics.
Avoid plastic CGI, toy-like visuals, cartoon appearance,
excessive saturation, morphing and distorted structures.

SECTION 6 - STANDARD VIDEO FORMAT
Vertical 9:16.
Exactly 5 scenes.
Approximately 8 seconds per scene.
Total duration approximately 40 seconds.
Designed for Google Flow AI and Nano Banana Pro.

SECTION 7 - TOPIC DEVELOPMENT
Review the supplied topic or image.
Identify category, location, visual hook and story potential.
Develop one coherent story across five scenes.
Avoid repetitive concepts.

SECTION 8 - MANDATORY REEL HEADER
REEL TITLE
Tropic
Sub-Category
Location
Format
Duration
Main Focus
Story Flow
Visual Style
Explain the concept in Bengali.

SECTION 9 - GLOBAL VISUAL BIBLE
Before the scenes, define:
Main Subject Lock
Character Lock
Location Lock
Environment Lock
Colour Lock
Lighting Lock
Material & Texture Lock
Motion Lock

SECTION 10 - STORY STRUCTURE
Scene 1: Discovery Hook.
Scene 2: Grand Reveal.
Scene 3: Exploration / Activity.
Scene 4: Cinematic Highlight.
Scene 5: Ultimate Reveal / Ending.
The five scenes must form one connected visual journey.

SECTION 11 - MANDATORY FIVE-SCENE FORMAT
For EACH scene include:
Scene number and time range.
Story Purpose (Bengali).
Image/Video Prompt (English, detailed and self-contained).
Camera.
Camera Movement.
Subject Movement.
Environment Movement.
Sound Effects.
Ambient Sound.
Transition.
Planned Exit State.

Scene timing:
Scene 1: 0-8 seconds.
Scene 2: 8-16 seconds.
Scene 3: 16-24 seconds.
Scene 4: 24-32 seconds.
Scene 5: 32-40 seconds.

SECTION 12 - CONTINUITY LOCK
Maintain consistent characters, clothing, animals,
architecture, geography, environment, colour, lighting,
weather, scale and camera language across all scenes.
No unexplained location or subject changes.

SECTION 13 - FLOW AI IMAGE-TO-VIDEO RULES
Use clear English production prompts.
Give one primary action per scene.
Specify camera, subject and environment movement.
Keep motion physically believable.
Preserve image reference and visual continuity.
Avoid contradictory instructions.
If a prompt causes a safety warning, rewrite it
in neutral, Flow-friendly wording without losing intent.

SECTION 14 - PRODUCTION WORKFLOW
Topic development.
Global Visual Bible.
Five scene prompts.
Reference image analysis when supplied.
Image review.
Flow AI image-to-video production.
Continuity review.
Final Reel quality review.
Do not claim that images or videos were generated
when only text prompts were created.

SECTION 15 - AUDIO DESIGN
Include scene-wise sound effects and ambient sound.
Define music mood, intensity and ending.
Default: no unnecessary voiceover.
If voiceover is requested, include the exact spoken line,
delivery, timing and narration/dialogue type inside
the corresponding scene's Image-to-Video prompt.

SECTION 16 - FINAL QUALITY AUDIT
Check:
Correct topic and geography.
Strong opening hook.
Exactly five scenes.
Approximately eight seconds each.
9:16 format.
All mandatory scene sections included.
Strong continuity.
Realistic texture and physics.
No plastic CGI appearance.
Cinematic ending.

SECTION 17 - FACEBOOK REEL PACKAGE
Create an engaging caption and relevant hashtags.
Keep the caption suitable for the actual story.
Do not use unrelated trending hashtags.

SECTION 18 - LANGUAGE RULE
Explanations in Bengali.
Production prompts in English.
Detailed, clear and complete instructions.
Never omit mandatory scene sections.

SECTION 19 - USER COMMANDS
NEXT: Choose one fresh topic using available history.
TOPIC: Develop the user's supplied topic.
CHANGE: Modify the requested part.
REGENERATE: Recreate the requested output.
CONTINUE: Continue the existing project.
MASTER PROMPT REVIEW: Review creative rules.

SECTION 20 - FINAL DIRECTIVE
This is one continuous Bengal + India + World project.
Bengal remains the main base.
Include India and world nature, human activity,
struggle, travel and discovery.
Fantasy nature and futuristic city ships are additions,
not replacements for the original project identity.
Always produce complete, Flow-friendly, cinematic work.
"""

# =====================================================
# SESSION MEMORY
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = ""

# =====================================================
# GEMINI CONNECTION
# =====================================================

def get_client():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY পাওয়া যায়নি। "
            "Streamlit Secrets পরীক্ষা করো।"
        )

    return genai.Client(api_key=api_key)


def ask_gemini(prompt, image=None):
    client = get_client()

    contents = [prompt]

    if image is not None:
        contents.append(image)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents
    )

    result = response.text

    if not result:
        raise ValueError(
            "Gemini কোনো Text Response দেয়নি। আবার চেষ্টা করো।"
        )

    return result


# =====================================================
# TOPIC HISTORY HELPERS
# =====================================================

def add_history(topic):
    if topic and topic not in st.session_state.history:
        st.session_state.history.append(topic)


def clean_topic_lines(response):
    lines = []

    for line in response.splitlines():
        line = re.sub(r"^\s*[\d\-\*\.\)\s]+", "", line).strip()

        if line and "|" in line:
            lines.append(line)

    return lines[:10]


# =====================================================
# TOPIC GENERATOR
# =====================================================

def generate_10_topics():
    previous = "\n".join(st.session_state.history[-20:])

    prompt = f"""
{MASTER_PROMPT}

TASK:
Generate exactly 10 fresh and visually outstanding Reel topics.

Balance these categories:
Bengal Village Life & Nature,
India & World Nature,
Human Life & Struggle,
Fantasy Nature,
Fantasy Architecture & Futuristic Civilizations.

Avoid repeating these previous topics:
{previous}

Rules:
- Make every topic visually different.
- Use realistic, cinematic and scroll-stopping ideas.
- Do not let fantasy dominate all suggestions.
- Include a suitable category for every topic.
- Output exactly 10 lines in this format:
Category | Topic
Do not write explanations before or after the list.
"""

    return ask_gemini(prompt)


def generate_next_topic():
    previous = "\n".join(st.session_state.history[-20:])

    prompt = f"""
{MASTER_PROMPT}

USER COMMAND: NEXT

Choose ONE fresh and outstanding Reel topic.
Review the previous topics and avoid repetition.

Previous topics:
{previous}

Rotate categories intelligently.
Keep Bengal, India, World, Human Life,
Fantasy Nature and Futuristic Architecture balanced.

Output only one line:
Category | Topic
"""

    return ask_gemini(prompt)


# =====================================================
# COMPLETE REEL GENERATOR
# =====================================================

def generate_reel(topic, image=None, extra_instruction=""):

    prompt = f"""
{MASTER_PROMPT}

CREATE A COMPLETE CINEMATIC REEL PRODUCTION PLAN.

USER TOPIC:
{topic}

ADDITIONAL USER INSTRUCTIONS:
{extra_instruction if extra_instruction else "None"}

IMAGE REFERENCE:
{"An image has been supplied. Carefully analyze its visible subject, composition, environment, shapes, colours, textures, lighting and visual style. Use it as the primary visual reference. Create a coherent five-scene story inspired by it. Preserve important visual characteristics while developing new cinematic angles and actions." if image is not None else "No reference image supplied."}

MANDATORY OUTPUT:

PART 1: REEL HEADER
Title, Tropic, Sub-Category, Location, Format,
Duration, Main Focus, Story Flow and Visual Style.
Explain the concept in Bengali.

PART 2: GLOBAL VISUAL BIBLE
Main Subject Lock
Character Lock
Location Lock
Environment Lock
Colour Lock
Lighting Lock
Material & Texture Lock
Motion Lock

PART 3: FIVE COMPLETE SCENES

For EACH of the five scenes, include every field:

Scene Number and Time Range
Story Purpose (Bengali)
Image/Video Prompt (English, detailed and self-contained)
Camera
Camera Movement
Subject Movement
Environment Movement
Sound Effects
Ambient Sound
Transition
Planned Exit State

Do not shorten any scene.
Do not combine fields.
Each Image/Video Prompt must be ready for Flow AI.

Story progression:
Scene 1: Discovery Hook.
Scene 2: Grand Reveal.
Scene 3: Exploration or Activity.
Scene 4: Cinematic Highlight.
Scene 5: Ultimate Reveal and Ending.

PART 4: CONTINUITY LOCKS
Explain character, location, environment, colour,
lighting, weather, architecture and motion continuity.

PART 5: COMPLETE AUDIO FLOW
Scene-wise sound design, ambient sound, music mood,
intensity progression and ending.

PART 6: FINAL QUALITY AUDIT
Check all five scenes, visual continuity, realism,
geography, motion, 9:16 and cinematic impact.

PART 7: FACEBOOK PUBLISHING PACKAGE
Create one engaging Bengali caption and relevant hashtags.

IMPORTANT:
Bengali explanations.
English production prompts.
Exactly five scenes, approximately eight seconds each.
Do not omit any required section.
Do not claim that actual videos or images have been generated.
"""

    return ask_gemini(prompt, image=image)


# =====================================================
# APP HEADER
# =====================================================

st.title("🎬 Bengal AI Content Creator")
st.subheader("Your Personal AI Reel Director")

st.write(
    "তোমার Bengal + India + World Nature & Human Life "
    "Reel Project-এর AI Creative Studio।"
)

st.caption(
    "Gemini AI Powered | Master Creative System V2.1 | Version 3.0"
)

st.divider()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.header("📚 Project History")

    st.caption("এই Session-এর Topic History")

    if st.session_state.history:
        for i, item in enumerate(
            reversed(st.session_state.history[-20:]),
            start=1
        ):
            st.write(f"{i}. {item}")
    else:
        st.info("এখনও কোনো Topic History নেই।")

    if st.button("Clear Session History"):
        st.session_state.history = []
        st.rerun()

    st.divider()

    st.caption("Gemini API Free Tier-এর সীমা প্রযোজ্য।")


# =====================================================
# TOPIC SELECTION
# =====================================================

st.header("1. Choose Your Topic")

mode = st.radio(
    "তুমি কীভাবে Reel তৈরি করতে চাও?",
    [
        "Write My Own Topic",
        "Get 10 Topic Ideas",
        "NEXT - New Topic",
        "Upload Reference Image"
    ],
    horizontal=False
)

uploaded_image = None
extra_instruction = ""

# -----------------------------------------------------
# MODE 1: OWN TOPIC
# -----------------------------------------------------

if mode == "Write My Own Topic":

    topic_input = st.text_input(
        "তোমার Reel Topic লিখো",
        placeholder="Example: Endless Green Village Road Tunnel"
    )

    extra_instruction = st.text_area(
        "অতিরিক্ত নির্দেশ (Optional)",
        placeholder="Example: Thick rounded green tree tunnel..."
    )

    if st.button("Select My Topic"):
        if topic_input.strip():
            st.session_state.selected_topic = topic_input.strip()
            add_history(topic_input.strip())
            st.success("Topic Selected!")
        else:
            st.warning("আগে একটি Topic লেখো।")


# -----------------------------------------------------
# MODE 2: 10 AI TOPICS
# -----------------------------------------------------

elif mode == "Get 10 Topic Ideas":

    if st.button("✨ Generate 10 Fresh Topics", type="primary"):

        with st.spinner("Gemini AI নতুন Topic তৈরি করছে..."):
            try:
                result = generate_10_topics()
                st.session_state.suggestions = clean_topic_lines(result)

                if not st.session_state.suggestions:
                    st.session_state.suggestions = [
                        result
                    ]

            except Exception as e:
                st.error(f"AI Error: {e}")

    if st.session_state.suggestions:

        selected = st.selectbox(
            "১০টি Topic থেকে একটি নির্বাচন করো",
            st.session_state.suggestions
        )

        if st.button("Use Selected Topic"):
            topic_name = selected.split("|", 1)[-1].strip()
            st.session_state.selected_topic = topic_name
            add_history(topic_name)
            st.success("Topic Selected!")


# -----------------------------------------------------
# MODE 3: NEXT
# -----------------------------------------------------

elif mode == "NEXT - New Topic":

    if st.button("➡️ NEXT - Generate New Topic", type="primary"):

        with st.spinner("Gemini নতুন Topic খুঁজছে..."):
            try:
                result = generate_next_topic()
                st.session_state.suggestions = [result.strip()]

                topic_name = result.split("|", 1)[-1].strip()

                st.session_state.selected_topic = topic_name
                add_history(topic_name)

                st.success("নতুন Topic তৈরি হয়েছে!")
                st.subheader(topic_name)

            except Exception as e:
                st.error(f"AI Error: {e}")


# -----------------------------------------------------
# MODE 4: IMAGE REFERENCE
# -----------------------------------------------------

elif mode == "Upload Reference Image":

    uploaded_file = st.file_uploader(
        "তোমার Reference Image Upload করো",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file is not None:

        try:
            uploaded_image = Image.open(
                BytesIO(uploaded_file.getvalue())
            ).convert("RGB")

            st.image(
                uploaded_image,
                caption="Uploaded Reference Image",
                use_container_width=True
            )

            extra_instruction = st.text_area(
                "ছবিটি সম্পর্কে অতিরিক্ত নির্দেশ (Optional)",
                placeholder="Example: Keep the thick rounded green tunnel..."
            )

            if st.button("Use This Reference Image"):
                st.session_state.selected_topic = (
                    "Reference Image Based Cinematic Reel"
                )
                st.success("Image Reference Selected!")

        except Exception as e:
            st.error(f"Image Error: {e}")


# =====================================================
# SELECTED TOPIC
# =====================================================

st.divider()

st.header("2. Selected Topic")

if st.session_state.selected_topic:
    st.success(st.session_state.selected_topic)
else:
    st.info("একটি Topic নির্বাচন করো অথবা Image Upload করো।")


# =====================================================
# GENERATE REEL BUTTON
# =====================================================

st.divider()

st.header("3. Generate Complete Reel Plan")

if st.button(
    "🎬 CREATE MY COMPLETE 5-SCENE REEL",
    type="primary",
    use_container_width=True
):

    current_topic = st.session_state.selected_topic

    if uploaded_image is not None:
        current_topic = current_topic or "Image Reference Based Reel"

    if not current_topic:
        st.warning("আগে একটি Topic নির্বাচন করো অথবা Image Upload করো।")

    else:

        with st.spinner(
            "Gemini AI তোমার Story এবং পাঁচটি Scene তৈরি করছে..."
        ):

            try:
                result = generate_reel(
                    topic=current_topic,
                    image=uploaded_image,
                    extra_instruction=extra_instruction
                )

                st.session_state.generated_plan = result

                st.success("তোমার Reel Production Plan তৈরি হয়েছে!")

            except Exception as e:
                st.error(
                    "Reel তৈরি করা যায়নি। "
                    "API Key, Model বা Free Quota পরীক্ষা করো।"
                )
                st.exception(e)


# =====================================================
# SHOW COMPLETE OUTPUT
# =====================================================

if st.session_state.generated_plan:

    st.divider()

    st.header("🎥 Your Complete Reel Production Plan")

    st.markdown(st.session_state.generated_plan)

    st.download_button(
        label="⬇️ Download Complete Reel Plan",
        data=st.session_state.generated_plan,
        file_name="bengal_reel_production_plan.txt",
        mime="text/plain",
        use_container_width=True
    )

    if st.button("Generate Another Reel"):
        st.session_state.generated_plan = ""
        st.session_state.selected_topic = ""
        st.rerun()


# =====================================================
# MASTER PROMPT INFORMATION
# =====================================================

st.divider()

with st.expander("Master Creative Instructions V2.1"):

    st.write(
        "এই Creative System অ্যাপের মধ্যে স্থায়ীভাবে রাখা হয়েছে।"
    )

    st.code(MASTER_PROMPT, language="text")


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bengal AI Content Creator | Version 3.0 | Gemini AI"
)
