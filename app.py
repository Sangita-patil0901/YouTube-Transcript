import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for Gemini AI
prompt = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important points within 1000 words. 
Please provide the summary of the text given here:  """

# Function to extract transcript details in the desired language
def extract_transcript_details(youtube_video_url, language='en'):
    try:
        video_id = youtube_video_url.split("=")[1]
        # Fetch the transcript in the specified language
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript

    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        return f"Error: {str(e)}. Unable to fetch transcript in the desired language."

    except Exception as e:
        raise e

# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# List of languages
languages = {
    "Abkhazian": "ab", "Afar": "aa", "Afrikaans": "af", "Akan": "ak", "Albanian": "sq",
    "Amharic": "am", "Arabic": "ar", "Armenian": "hy", "Assamese": "as", "Aymara": "ay",
    "Azerbaijani": "az", "Bangla": "bn", "Bashkir": "ba", "Basque": "eu", "Belarusian": "be",
    "Bhojpuri": "bho", "Bosnian": "bs", "Breton": "br", "Bulgarian": "bg", "Burmese": "my",
    "Catalan": "ca", "Cebuano": "ceb", "Chinese (Simplified)": "zh-Hans", "Chinese (Traditional)": "zh-Hant",
    "Corsican": "co", "Croatian": "hr", "Czech": "cs", "Danish": "da", "Divehi": "dv",
    "Dutch": "nl", "Dzongkha": "dz", "English": "en", "Esperanto": "eo", "Estonian": "et",
    "Ewe": "ee", "Faroese": "fo", "Fijian": "fj", "Filipino": "fil", "Finnish": "fi",
    "French": "fr", "Ga": "gaa", "Galician": "gl", "Ganda": "lg", "Georgian": "ka",
    "German": "de", "Greek": "el", "Guarani": "gn", "Gujarati": "gu", "Haitian Creole": "ht",
    "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "iw", "Hindi": "hi", "Hmong": "hmn",
    "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga",
    "Italian": "it", "Japanese": "ja", "Javanese": "jv", "Kalaallisut": "kl", "Kannada": "kn",
    "Kazakh": "kk", "Khasi": "kha", "Khmer": "km", "Kinyarwanda": "rw", "Korean": "ko",
    "Krio": "kri", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
    "Latvian": "lv", "Lingala": "ln", "Lithuanian": "lt", "Luo": "luo", "Luxembourgish": "lb",
    "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms", "Malayalam": "ml", "Maltese": "mt",
    "Manx": "gv", "Māori": "mi", "Marathi": "mr", "Mongolian": "mn", "Morisyen": "mfe",
    "Nepali": "ne", "Newari": "new", "Northern Sotho": "nso", "Norwegian": "no", "Nyanja": "ny",
    "Occitan": "oc", "Odia": "or", "Oromo": "om", "Ossetic": "os", "Pampanga": "pam",
    "Pashto": "ps", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Portuguese (Portugal)": "pt-PT",
    "Punjabi": "pa", "Quechua": "qu", "Romanian": "ro", "Rundi": "rn", "Russian": "ru",
    "Samoan": "sm", "Sango": "sg", "Sanskrit": "sa", "Scottish Gaelic": "gd", "Serbian": "sr",
    "Seselwa Creole French": "crs", "Shona": "sn", "Sindhi": "sd", "Sinhala": "si", "Slovak": "sk",
    "Slovenian": "sl", "Somali": "so", "Southern Sotho": "st", "Spanish": "es", "Sundanese": "su",
    "Swahili": "sw", "Swati": "ss", "Swedish": "sv", "Tajik": "tg", "Tamil": "ta",
    "Tatar": "tt", "Telugu": "te", "Thai": "th", "Tibetan": "bo", "Tigrinya": "ti",
    "Tongan": "to", "Tsonga": "ts", "Tswana": "tn", "Tumbuka": "tum", "Turkish": "tr",
    "Turkmen": "tk", "Ukrainian": "uk", "Urdu": "ur", "Uyghur": "ug", "Uzbek": "uz",
    "Venda": "ve", "Vietnamese": "vi", "Waray": "war", "Welsh": "cy", "Western Frisian": "fy",
    "Wolof": "wo", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
}

# Streamlit UI
st.title("ScriptBot AI Transcriptor")
youtube_link = st.text_input("Enter YouTube Video Link:")

# Language dropdown
language = st.selectbox("Select Language", options=list(languages.keys()))

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Run ScriptBot"):
    transcript_text = extract_transcript_details(youtube_link, languages[language])

    if transcript_text.startswith("Error"):
        st.error(transcript_text)
    else:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Analysis:")
        st.write(summary)
