# Import Streamlit
import streamlit as st
import pandas as pd
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# Function to load countries
def load_countries():
    # Assuming you have a file 'countries.csv' with country names
    return pd.read_csv("countries.csv")["Country Name"].tolist()


# # Start of Streamlit app
def main():
    st.title("GPT-4 Article Generator")

    # Initialize the session state for page navigation if it's not already set
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "User Input Form"

    # Display the current page based on session state
    if st.session_state["current_page"] == "User Input Form":
        user_input_form()
    elif st.session_state["current_page"] == "Article Configuration":
        basic_and_advanced_options()
    elif st.session_state["current_page"] == "Article Display":
        display_article()


def user_input_form():
    st.header("User Input Form")

    # User Input Fields
    target_keyword = st.text_input("Target Keyword", placeholder="Enter article topic")
    countries = load_countries()
    country = st.selectbox(
        "Country/Region", countries, index=countries.index("United States")
    )
    language = st.selectbox(
        "Language", ["English (US)", "Spanish", "French", "German", "Other"]
    )

    # Placeholder for next steps
    if st.button("NEXT"):
        st.session_state["target_keyword"] = target_keyword
        st.session_state["country"] = country
        st.session_state["language"] = language

        st.session_state["current_page"] = "Article Configuration"
        st.rerun()


def basic_and_advanced_options():
    st.header("Article Configuration")

    # Basic Options
    st.subheader("Basic Options")
    tone_of_voice = st.selectbox(
        "Tone of Voice",
        [
            "SEO Optimized",
            "Casual",
            "Excited",
            "Formal",
            "Friendly",
            "Humorous",
            "Professional",
        ],
    )
    point_of_view = st.selectbox(
        "Point of View",
        [
            "First person singular (I, me, my, mine)",
            "First person plural (we, us, our, ours)",
            "Second person (you, your, yours)",
            "Third person (he, she, it, they)",
        ],
    )
    faq_section = st.checkbox("Include FAQ Section")
    youtube_suggestions = st.checkbox("Include YouTube Suggestions")
    meta_description = st.checkbox("Include Meta Description")
    featured_image = st.checkbox("Include Featured Image")

    # Store the values in session state
    st.session_state["tone_of_voice"] = tone_of_voice
    st.session_state["point_of_view"] = point_of_view
    st.session_state["faq_section"] = faq_section
    st.session_state["youtube_suggestions"] = youtube_suggestions
    st.session_state["meta_description"] = meta_description
    st.session_state["featured_image"] = featured_image

    # Toggle for Advanced Options
    if st.checkbox("Show Advanced Options"):
        advanced_options()
    else:
        # Placeholder for next steps
        if st.button("Next"):
            # Redirect to the next page
            st.session_state["current_page"] = "Article Display"
            st.rerun()


def advanced_options():
    st.subheader("Advanced Options")
    extra_title_prompt = st.text_area("Extra Title Prompt")
    extra_intro_prompt = st.text_area("Extra Introduction Prompt")
    extra_content_prompt = st.text_area("Extra Content Prompt")
    keywords = st.text_area("Keywords")

    word_per_h2_section = st.number_input(
        "Word Count per H2 Section", min_value=300, step=10
    )
    word_per_h3_section = st.number_input(
        "Word Count per H3 Section", min_value=150, step=10
    )

    # Store the values in session state
    st.session_state["extra_title_prompt"] = extra_title_prompt
    st.session_state["extra_intro_prompt"] = extra_intro_prompt
    st.session_state["extra_content_prompt"] = extra_content_prompt
    st.session_state["keywords"] = keywords
    st.session_state["word_per_h2_section"] = word_per_h2_section
    st.session_state["word_per_h3_section"] = word_per_h3_section

    # Placeholder for next steps
    if st.button("Next"):
        # Redirect to the next page
        st.session_state["current_page"] = "Article Display"
        st.rerun()


def generate_prompt():
    prompt = f"Write an in-depth article about {st.session_state['target_keyword']}. With a good article title."

    if st.session_state.get("country"):
        prompt += f" Focus on its relevance in {st.session_state['country']}."

    if st.session_state.get("tone_of_voice"):
        prompt += f" Maintain a {st.session_state['tone_of_voice']} tone."

    if st.session_state.get("point_of_view"):
        prompt += f" Use a {st.session_state['point_of_view']}."

    if st.session_state.get("faq_section"):
        prompt += " Include an FAQ section addressing common questions."

    if st.session_state.get("youtube_suggestions"):
        prompt += " Provide YouTube video suggestions for further learning."

    if st.session_state.get("meta_description"):
        prompt += " Add a compelling meta description summarizing the article."

    if st.session_state.get("featured_image"):
        prompt += " Recommend a featured image that captures the essence of the topic."

    if st.session_state.get("extra_title_prompt"):
        prompt += f" {st.session_state['extra_title_prompt']}"

    if st.session_state.get("extra_intro_prompt"):
        prompt += f" {st.session_state['extra_intro_prompt']}"

    if st.session_state.get("extra_content_prompt"):
        prompt += f" {st.session_state['extra_content_prompt']}"

    if st.session_state.get("keywords"):
        prompt += (
            f" Incorporate these additional keywords: {st.session_state['keywords']}."
        )

    if st.session_state.get("word_per_h2_section"):
        prompt += f" Ensure each major heading section has at least {st.session_state['word_per_h2_section']} words."

    if st.session_state.get("word_per_h3_section"):
        prompt += f" Ensure each subheading section has at least {st.session_state['word_per_h3_section']} words."

    # New Enhancements
    prompt += " Include real-world case studies or examples for practical insights if relevant."
    prompt += " Customize the introduction and conclusion to add uniqueness, make it lengthy."
    prompt += " Tailor the content to the specified target audience if relevant."
    prompt += " Suggest interactive elements like polls or quizzes if relevant."
    prompt += " Recommend social media post ideas related to the article if relevant."
    prompt += " The entire article word count must be more than 1500 words, this is very important do not mention it in the article."

    return prompt


def get_gpt4_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a talented writer, a skilled professional in detailed, lengthy and robust writing skills.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=4096,
    )

    return completion.choices[0].message.content


def display_article():
    st.header("Generated Article")

    # Generate the prompt
    prompt = generate_prompt()

    # Show a spinner while waiting for the response
    with st.spinner("Generating article, please wait..."):
        generated_article = get_gpt4_response(prompt)

    # Display the article
    st.text_area("Article", generated_article, height=500)


# Run the app
if __name__ == "__main__":
    main()
