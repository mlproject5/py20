import streamlit as st
import nltk
from transformers import pipeline
import time
import re
from faker import Faker


st.set_page_config(page_title='WordFlow', page_icon='w.png', layout="centered", initial_sidebar_state="auto", menu_items=None)


hide_streamlit_style = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def ps():
    summarizer = pipeline("summarization")

    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Text "
        "Summarizer</h1></center>",
        unsafe_allow_html=True)
    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 18px;'>Enter your text below and "
        "get a summary!</h1></center>",
        unsafe_allow_html=True)

    text = st.text_area("Enter text here")

    if st.button("Summarize"):
        if text:
            with st.spinner("Summarizing..."):
                summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
                sentences = nltk.sent_tokenize(summary)
                capitalized_sentences = [sentence.capitalize() for sentence in sentences]
                capitalized_summary = ' '.join(capitalized_sentences)

            st.success("Summary Generated Successfully!!")
            st.write(capitalized_summary)
        else:
            st.warning("Please enter some text to summarize.")


def wc():
    def count_words(text):
        words = text.split()
        return len(words)

    def count_sentences(text):
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        return len(sentences)

    def count_characters(text):
        return len(text)

    def main():
        st.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Word, Sentence, and Character Counter</h1></center>",
            unsafe_allow_html=True)
        text_input = st.text_area("Enter your text below", height=160)
        if st.button("Count"):
            with st.spinner("Counting..."):
                time.sleep(1)
                word_count = count_words(text_input)
                sentence_count = count_sentences(text_input)
                character_count = count_characters(text_input)
                st.success(f"Word count:\n**{word_count}**")
                st.info(f"Sentence count:\n**{sentence_count}**")
                st.warning(f"Character count:\n**{character_count}**")

    if __name__ == "__main__":
        main()


def lip():
    def generate_lorem_ipsum(amount, with_option):
        fake = Faker()
        if with_option == "Paragraphs":
            lorem_ipsum = '\n\n'.join(fake.paragraphs(nb=amount))
        elif with_option == "Words":
            words = fake.words(nb=amount)
            lorem_ipsum = ' '.join([word.capitalize() for word in words])
        else:
            lorem_ipsum = fake.texts(nb_texts=amount, max_nb_chars=200)
            lorem_ipsum = [text for text in lorem_ipsum if text.strip()]
            lorem_ipsum = '\n'.join(lorem_ipsum)
        return lorem_ipsum

    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Lorem Ipsum "
        "Generator</h1></center>",
        unsafe_allow_html=True)

    amount = st.number_input("Amount", min_value=1, step=1, value=1)

    with_option = st.radio("Select Option", ("Paragraphs", "Words", "Mixed Text"))

    if st.button("Generate"):
        with st.spinner("Generating..."):
            time.sleep(2)
            lorem_ipsum_text = generate_lorem_ipsum(amount, with_option)
        st.success("Text Generated Successfully!!")
        st.text_area("Lorem Ipsum Text", value=lorem_ipsum_text, height=200)


st.sidebar.markdown("""
            <style>
                .sidebar-text {
                    text-align: center;
                    font-weight: 600;
                    font-size: 24px;
                    font-family: 'Comic Sans MS', cursive;
                }
            </style>
            <p class="sidebar-text">WordFlow Toolkit</p>
            <br/>
        """, unsafe_allow_html=True)

st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTY3q_Y-AbbJY9NVINHJ4-C9W6q6HETulD21Q&usqp=CAU")
sidebar_options = {
    "Word Counter": wc,
    "Paragraph Summarizer": ps,
    "Lorem Ipsum Generator": lip,
}

selected_option = st.sidebar.radio("Please Select One:", list(sidebar_options.keys()))

if "prev_option" not in st.session_state:
    st.session_state.prev_option = selected_option

if st.session_state.prev_option != selected_option:
    if selected_option == "Word Counter":
        st.session_state.long_url_1 = ""
    elif selected_option == "Paragraph Summarizer":
        st.session_state.long_url_2 = ""
    elif selected_option == "Lorem Ipsum Generator":
        st.session_state.long_url_3 = ""


st.session_state.prev_option = selected_option
sidebar_options[selected_option]()
