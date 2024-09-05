import streamlit as st
import googletrans as gt
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()


##from google.cloud.translate import 
##from googletrans import Translator
##translator = Translator()

##text="hello how are you"
##translated_text = translator.translate(text=text, src='auto', dest='fr').text
##translated_text

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def translate_with_gemini(text, target_language):
    """
    Translates the given text to the target language using Gemini Pro.
    
    Args:
        text: The text to be translated.
        target_language: The target language code (e.g., 'ml' for Malayalam).

    Returns:
        The translated text.
    """
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Translate the following text to {target_language}: {text}"
    response = model.generate_content(prompt)
    return response.text

# Prompt for generating summaries
prompt = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important points in bullet points
within 250 words. Please provide the summary of the text given here: """

# Function to extract transcript details
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None

# Function to generate content using Gemini AI
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Streamlit UI setup
st.title("YouTube Transcript to Detailed Notes Converter")

youtube_video_url = st.text_input("Enter YouTube video link:")

if youtube_video_url:
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except IndexError:
        st.error("Invalid YouTube URL")

if st.button("Get Detailed Notes"):
    with st.spinner('Extracting transcript and generating summary...'):
        transcript_text = extract_transcript_details(youtube_video_url)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            sum1 = translate_with_gemini(summary,"hi")
            if summary:
                st.markdown("## Detailed Notes:")

                st.write(summary)
                st.write(sum1)


