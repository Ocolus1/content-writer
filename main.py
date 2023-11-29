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
    prompt += (
        " Customize the introduction and conclusion to add uniqueness, make it lengthy."
    )
    prompt += " Tailor the content to the specified target audience if relevant."
    prompt += " Suggest interactive elements like polls or quizzes if relevant."
    prompt += " Recommend social media post ideas related to the article if relevant."
    prompt += " The entire article word count must be more than 1500 words, this is very important do not mention it in the article."

    return prompt


def generate_title():
    title = f"Generate a single line blog title focused on {st.session_state['target_keyword']}, ensuring it is engaging, SEO-optimized, and reflective of key themes in {st.session_state['target_keyword']}."
    return title


def generate_intro(title):
    intro = f"""
    Write an introduction for the article titled '{title}', 
    setting the stage for an in-depth exploration of {st.session_state['target_keyword']}, 
    its importance in the relevant field, and its impact on users or industry trends
    """
    return intro


def generate_body():
    body = f"""
    Discuss the fundamental principles or basics of {st.session_state['target_keyword']}, and their relevance in the current context.
    Explore advanced concepts, trends, or strategies related to {st.session_state['target_keyword']} and how they can be applied effectively.
    Share practical tips, insights, or case studies illustrating the successful application of {st.session_state['target_keyword']}.
    """
    return body


def generate_FAQ():
    faq = f"""
        Create a FAQ section addressing common questions and misconceptions about {st.session_state['target_keyword']} providing clear and concise answers.
    """
    return faq


def generate_youtube():
    youtube = f"""
        List YouTube resources, such as channels or videos, offering valuable insights, tutorials, or case studies on {st.session_state['target_keyword']} in  URL links.
    """
    return youtube


def generate_metadata():
    metadata = f"""
        Draft a compelling meta description for the article, summarizing its key points about {st.session_state['target_keyword']} and inviting readers to explore in-depth
    """
    return metadata


def generate_image():
    img = f"""
        Give  an ideal featured image for the article that visually represents the core themes or concepts of {st.session_state['target_keyword']} in a URL link.
    """
    return img


# def generate_prompts():
#     prompt = ""

#     intro = f""
#     pass


# Assuming you have a list to track the conversation history
conversation_history = []


def get_gpt4_response(prompt):
    # Add the new user prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Prepare the messages for the API call, including past messages
    messages = []
    for message in conversation_history[
        -14:
    ]:  # Include the last 10 interactions, for example
        messages.append(message)

    # GPT-4 API call
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=4096,
    )

    # Get the response and add it to the conversation history
    response = completion.choices[0].message.content
    conversation_history.append({"role": "system", "content": response})


    return response


# Function to update the progress bar and the status text
def update_progress(progress_bar, status_text, step, total_steps):
    progress = step / total_steps
    progress_bar.progress(progress)
    status_text.text(f"Generating content: Step {step}/{total_steps}...")


def display_article():
    st.header("Generated Article")

    # Total number of steps in the content generation process
    total_steps = 7

    # Initialize the progress bar and status text
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Show a spinner while waiting for the response
    with st.spinner("Generating article, please wait..."):
        # Step 1: Generate Title
        update_progress(progress_bar, status_text, 1, total_steps)
        get_title = generate_title()
        generated_title = get_gpt4_response(get_title)


        # Step 2: Generate Intro
        update_progress(progress_bar, status_text, 2, total_steps)
        get_intro = generate_intro(generated_title)
        generated_intro = get_gpt4_response(get_intro)


        # Step 3: Generate Body
        update_progress(progress_bar, status_text, 3, total_steps)
        get_body = generate_body()
        generated_body = get_gpt4_response(get_body)


        # Step 4: Generate FAQ
        update_progress(progress_bar, status_text, 4, total_steps)
        get_faq = generate_FAQ()
        generated_faq = get_gpt4_response(get_faq)


        # Step 5: Generate YouTube Suggestions
        update_progress(progress_bar, status_text, 5, total_steps)
        get_youtube = generate_youtube()
        generated_youtube = get_gpt4_response(get_youtube)


        # Step 6: Generate Metadata
        update_progress(progress_bar, status_text, 6, total_steps)
        get_metadata = generate_metadata()
        generated_metadata = get_gpt4_response(get_metadata)

        # Step 7: Generate Image Suggestions
        update_progress(progress_bar, status_text, 7, total_steps)
        get_image = generate_image()
        generated_image = get_gpt4_response(get_image)

    # Update the status to indicate completion
    status_text.text("Content generation complete!")

    # Display the article
    generated_article = f"""
{generated_title[1:-1]}

{generated_intro}

{generated_body}

{generated_faq}

{generated_youtube}

{generated_metadata}

{generated_image}

    """
    st.text_area("Article", generated_article, height=600)
    conversation_history.clear()


# Run the app
if __name__ == "__main__":
    main()
