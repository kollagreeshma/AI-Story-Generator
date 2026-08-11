import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

# =====================================================
# LOAD GROQ API KEY
# =====================================================

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()


# =====================================================
# SESSION STATE - MODEL
# =====================================================

if "model" not in st.session_state:

    st.session_state["model"] = init_chat_model(
        model="llama-3.3-70b-versatile",
        model_provider="groq",
        api_key=groq_api_key
    )

# =====================================================
# SESSION STATE - PROMPT TEMPLATE
# =====================================================

if "template" not in st.session_state:

    st.session_state["template"] = PromptTemplate(

        input_variables=[
            "language",
            "tone",
            "storyIdea",
            "length",
            "grammar",
            "plagiarism",
            "categories",
            "character_names",
            "time_period",
            "creativity",
            "audience"
        ],

        template="""
Act like a professional story writer who writes
fantastic and engaging stories.

Target Audience:
{audience}

Write the complete story in:
{language}

Important:
Even if the input is provided in English, the
complete output must be written in {language}.

Tone:
{tone}

Creativity Level:
{creativity}

Time Period:
{time_period}

Grammar Level:
{grammar}

Originality Level:
{plagiarism}

Story Length:
{length} paragraphs

Story Idea:
{storyIdea}

Category:
{categories}

Character Names:
{character_names}

Rules:
1. Write the complete story in {language}.
2. Do not mix languages.
3. Follow the selected tone.
4. Make the story creative and engaging.
5. Use the given character names.
6. Avoid emojis.
7. Follow the requested story length.
8. Make the story original.
"""
    )


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📖 AI Story Generator")


# Language
language = st.sidebar.pills(
    "Enter Language",
    [
        "English",
        "Telugu",
        "Hindi",
        "Tamil",
        "Urdu",
        "Kannada",
        "Chinese"
    ]
)


# Tone
tone = st.sidebar.segmented_control(
    "Select Tone",
    [
        "Friendly",
        "Narrative",
        "Poet"
    ]
)


# Story Idea
storyIdea = st.sidebar.text_area(
    "Tell me about your story idea",
    placeholder="Example: A boy discovers a magical forest..."
)


# Length
length = st.sidebar.slider(
    "Enter Number Of Paragraphs",
    min_value=1,
    max_value=10,
    value=3
)


# Grammar
grammar = st.sidebar.selectbox(
    "Specify Grammar",
    [
        "Beginner",
        "Intermediate",
        "Professional"
    ]
)


# Originality
plagiarism = st.sidebar.slider(
    "Specify Originality",
    min_value=0,
    max_value=100,
    value=100
)


# Category
categories = st.sidebar.radio(
    "Specify Category",
    [
        "Thriller",
        "Horror",
        "Suspense",
        "Adventure",
        "Comedy",
        "Family",
        "Drama",
        "Fantasy"
    ],
    horizontal=True
)


# Character Names
characterNames = st.sidebar.text_area(
    "Specify Character Names",
    placeholder="Rahul, Priya, Dragon..."
)


# Time Period
timePeriod = st.sidebar.segmented_control(
    "Specify Time Period",
    [
        "Ancient",
        "Modern",
        "Future"
    ]
)


# Creativity
creativity = st.sidebar.pills(
    "Specify Creativity",
    [
        "Low",
        "Medium",
        "High"
    ]
)


# Audience
audience = st.sidebar.segmented_control(
    "Enter Target Audience",
    [
        "Toddlers",
        "Kids",
        "Adults",
        "Old People"
    ]
)


# Submit Button
submit_button = st.sidebar.button(
    "🚀 Generate Story",
    width="stretch",
    type="primary"
)


# =====================================================
# GENERATE STORY
# =====================================================

if submit_button:

    # Check Story Idea
    if not storyIdea or not storyIdea.strip():

        st.warning("⚠️ Please enter your story idea.")

        st.stop()


    # Check selections
    if not language:
        st.warning("⚠️ Please select a language.")
        st.stop()

    if not tone:
        st.warning("⚠️ Please select a tone.")
        st.stop()

    if not creativity:
        st.warning("⚠️ Please select creativity level.")
        st.stop()

    if not timePeriod:
        st.warning("⚠️ Please select a time period.")
        st.stop()

    if not audience:
        st.warning("⚠️ Please select the target audience.")
        st.stop()


    # =================================================
    # CREATE FINAL PROMPT
    # =================================================

    final_prompt = st.session_state["template"].format(

        language=language,

        tone=tone,

        storyIdea=storyIdea,

        length=length,

        grammar=grammar,

        plagiarism=plagiarism,

        categories=categories,

        character_names=characterNames,

        time_period=timePeriod,

        creativity=creativity,

        audience=audience
    )


    # =================================================
    # GENERATE STORY
    # =================================================

    try:

        with st.spinner("🤖 Generating your story..."):

            response = st.session_state["model"].invoke(
                final_prompt
            )


        st.success("✅ Story Generated Successfully!")

        st.subheader("📚 Your Generated Story")

        st.write(response.content)


    except Exception as e:

        st.error("❌ Error while generating the story.")

        st.exception(e)

