# Import Streamlit
import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import zipfile

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

exclusion_phrases = [
    "In conclusion",
    "It is evident that",
    "Research indicates",
    "Data suggests",
    "Studies show",
    "As previously mentioned",
    "It can be observed that",
    "It is a known fact",
    "To summarize",
    "Therefore, it can be concluded",
    "It is noteworthy to mention",
    "One might argue",
    "The evidence points to",
    "According to the data",
    "This leads to the conclusion",
    "Diving into the world",
]


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
    article_mode = st.radio(
        "Select Article Generation Mode:", ("Single", "Multiple"), index=0
    )

    if article_mode == "Single":
        target_keyword = st.text_input(
            "Target Keyword", placeholder="Enter article topic"
        )
        st.session_state["target_keywords"] = [target_keyword]
    else:  # For multiple articles
        if "num_features" not in st.session_state:
            st.session_state.num_features = 1  # Initial input field

        features_topic = []

        # Display the text areas for each feature
        for i in range(st.session_state.num_features):
            topic = st.text_input(
                f"Enter Target Keyword {i + 1}",
                placeholder=f"Enter article topic {i + 1}",
                key=f"new_feature_{i}",
            )
            features_topic.append(topic)

        # Button to add more features
        if st.button("Add Topic"):
            st.session_state.num_features += 1

        st.session_state["target_keywords"] = features_topic

    countries = load_countries()
    country = st.selectbox(
        "Country/Region", countries, index=countries.index("United States")
    )
    language = st.selectbox(
        "Language", ["English (US)", "Spanish", "French", "German", "Other"]
    )

    # Placeholder for next steps
    if st.button("NEXT"):
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


def generate_title(keyword):
    prompt = ""
    if st.session_state.get("extra_title_prompt"):
        prompt = f"{st.session_state['extra_title_prompt']}"

    title = f"Generate a single line blog title focused on {keyword}, ensuring it is engaging, SEO-optimized, and reflective of key themes in {keyword}. {prompt}"
    return title


def generate_intro(title, keyword):
    prompt = ""

    if st.session_state.get("country"):
        prompt += f" Focus on its relevance in {st.session_state['country']}."

    if st.session_state.get("tone_of_voice"):
        prompt += f" Maintain a {st.session_state['tone_of_voice']} tone."

    if st.session_state.get("point_of_view"):
        prompt += f" Use a {st.session_state['point_of_view']}."

    if st.session_state.get("extra_intro_prompt"):
        prompt = f" {st.session_state['extra_intro_prompt']}"

    intro = f"""
    Write an introduction for the article titled '{title}', 
    setting the stage for an in-depth exploration of {keyword}, 
    its importance in the relevant field, and its impact on users or industry trends
    {prompt}

    Do not add keywords like this {exclusion_phrases} be more creative.
    """
    return intro


def generate_body(keyword):
    prompt = ""

    if st.session_state.get("country"):
        prompt += f" Focus on its relevance in {st.session_state['country']}."

    if st.session_state.get("tone_of_voice"):
        prompt += f" Maintain a {st.session_state['tone_of_voice']} tone."

    if st.session_state.get("point_of_view"):
        prompt += f" Use a {st.session_state['point_of_view']}."

    if st.session_state.get("keywords"):
        prompt += (
            f" Incorporate these additional keywords: {st.session_state['keywords']}."
        )

    if st.session_state.get("word_per_h2_section"):
        prompt += f" Ensure each major heading section has at least {st.session_state['word_per_h2_section']} words."

    if st.session_state.get("word_per_h3_section"):
        prompt += f" Ensure each subheading section has at least {st.session_state['word_per_h3_section']} words."

    if st.session_state.get("extra_content_prompt"):
        prompt += f" {st.session_state['extra_content_prompt']}"

    body = f"""
    Discuss the fundamental principles or basics of {keyword}, and their relevance in the current context.
    Explore advanced concepts, trends, or strategies related to {keyword} and how they can be applied effectively.
    Share practical tips, insights, or case studies illustrating the successful application of {keyword}.
    {prompt}

    Do not add keywords like this {exclusion_phrases} be more creative.
    """
    return body


def generate_FAQ(keyword):
    faq = f"""
        Create a FAQ section addressing common questions and misconceptions about {keyword} providing clear and concise answers.
    """
    return faq


def generate_youtube(keyword):
    youtube = f"""
        List YouTube resources, such as channels or videos, offering valuable insights, tutorials, or case studies on {keyword} in  URL links.
    """
    return youtube


def generate_metadata(keyword):
    metadata = f"""
        Draft a compelling meta description for the article, summarizing its key points about {keyword} and inviting readers to explore in-depth
        Do not add keywords like this {exclusion_phrases} be more creative.
    """
    return metadata


def generate_image(keyword):
    img = f"""
        Give an ideal featured image for the article that visually represents the core themes or concepts of {keyword} in a URL link.
    """
    return img


def generate_conclusion(body, keyword):
    conclusion = f"""
        Give an ideal conclusion represents the core themes or concepts of {keyword}and supplements the body of the article: {body}.
        Do not add keywords like this {exclusion_phrases} be more creative.
    """
    return conclusion


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
    # st.header("Generated Article")

    articles = []  # List to store generated articles

    for keyword in st.session_state.get("target_keywords", []):
        # Initialize total steps
        total_steps = 4  # Base steps for Title, Intro, and Body

        # Increment total_steps based on selected options
        if st.session_state.get("faq_section"):
            total_steps += 1
        if st.session_state.get("youtube_suggestions"):
            total_steps += 1
        if st.session_state.get("meta_description"):
            total_steps += 1
        if st.session_state.get("featured_image"):
            total_steps += 1

        # Initialize the progress bar and status text
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Show a spinner while waiting for the response
        with st.spinner(f"Generating article for {keyword}, please wait..."):
            # Step 1: Generate Title
            update_progress(progress_bar, status_text, 1, total_steps)
            get_title = generate_title(keyword)
            generated_title = get_gpt4_response(get_title)

            # Step 2: Generate Intro
            update_progress(progress_bar, status_text, 2, total_steps)
            get_intro = generate_intro(generated_title, keyword)
            generated_intro = get_gpt4_response(get_intro)

            # Step 3: Generate Body
            update_progress(progress_bar, status_text, 3, total_steps)
            get_body = generate_body(keyword)
            generated_body = get_gpt4_response(get_body)

            current_step = 4

            generated_faq = ""
            generated_youtube = ""
            generated_metadata = ""
            generated_image = ""

            if st.session_state.get("faq_section"):
                # Generate FAQ
                update_progress(progress_bar, status_text, current_step, total_steps)
                get_faq = generate_FAQ(keyword)
                generated_faq = get_gpt4_response(get_faq)
                current_step += 1

            if st.session_state.get("youtube_suggestions"):
                # Generate YouTube Suggestions
                update_progress(progress_bar, status_text, current_step, total_steps)
                get_youtube = generate_youtube(keyword)
                generated_youtube = get_gpt4_response(get_youtube)
                current_step += 1

            if st.session_state.get("meta_description"):
                # Generate Metadata
                update_progress(progress_bar, status_text, current_step, total_steps)
                get_metadata = generate_metadata(keyword)
                generated_metadata = get_gpt4_response(get_metadata)
                current_step += 1

            if st.session_state.get("featured_image"):
                # Generate Image Suggestions
                update_progress(progress_bar, status_text, current_step, total_steps)
                get_image = generate_image(keyword)
                generated_image = get_gpt4_response(get_image)
                current_step += 1

            update_progress(progress_bar, status_text, current_step, total_steps)
            get_conclusion = generate_conclusion(generated_body, keyword)
            generated_conclusion = get_gpt4_response(get_conclusion)

        # # Update the status to indicate completion
        # status_text.text("Content generation complete!")

        # Display the article
        generated_article = f"""
{generated_title[1:-1]}

{generated_intro}

{generated_body}

    """
        if st.session_state.get("faq_section"):
            generated_article += f"""
{generated_faq}
"""
        if st.session_state.get("youtube_suggestions"):
            generated_article += f"""
{generated_youtube}
"""
        if st.session_state.get("meta_description"):
            generated_article += f"""
{generated_metadata}
"""
        if st.session_state.get("featured_image"):
            generated_article += f"""
{generated_image}
"""

        generated_article += f"""
Conclusion
{generated_conclusion}
"""
        # Append the generated article to the list
        articles.append(generated_article)

        status_text.text(f"Article {len(articles)} has been generated completely!")

        # Clear previous conversation
        conversation_history.clear()

    # Offer download option for generated articles
    if articles:
        if len(articles) == 1:
            st.subheader("Generated Article")
            st.text_area("Article", articles[0], height=600)
            st.download_button(
                "Download Article as TXT",
                articles[0],
                file_name="generated_article.txt",
            )
            st.write("Download successful!!!")
        else:
            with st.expander("Download All Articles as Zip"):
                with st.spinner("Generating zip file..."):
                    first_keyword = st.session_state.get(
                        "target_keywords", ["default_keyword"]
                    )[0]
                    zip_filename = f"{'_'.join(first_keyword.split()[:5])}.zip"
                    with zipfile.ZipFile(zip_filename, "w") as zipf:
                        for index, article in enumerate(articles):
                            filename = f"article_{index+1}_{st.session_state['target_keywords'][index]}.txt"
                            zipf.writestr(filename, article)

                    # Provide a download link to the zip file
                    with open(zip_filename, "rb") as f:
                        zip_data = f.read()

                    if st.download_button(
                        label=f"Download {zip_filename}",
                        data=zip_data,
                        file_name=zip_filename,
                        mime="application/zip",
                    ):

                        st.success(f"{zip_filename} downloaded successfully!")

                        # Delete the zip file after successful download
                        os.remove(zip_filename)
                        st.success(f"{zip_filename} deleted successfully!")

                        # Reset the app to the initial input page after download
                        st.session_state.clear()  # Clearing the entire session state

                        # Set specific default values if needed
                        st.session_state["current_page"] = "User Input Form"

                        st.rerun()

            st.success("Download ready!")

    conversation_history.clear()


# Run the app
if __name__ == "__main__":
    main()
