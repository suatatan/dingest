import streamlit as st

from components.faq import faq
from dotenv import load_dotenv
import os

load_dotenv()


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How can I help you?\n"
           
            "1. Upload a pdf, docx, or txt file of home inspection report📄\n"
            "2. Ask a question about the report\n"
            "2. Or use existing extractor button to see analyzes. ⭐\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )
        
        st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "☘️ReportIO allows you to ask questions about your "
            "home inspection reports and get accurate answers with instant citations. "
        )
        st.markdown(
            "This tool is a work in progress. "
        )
        st.markdown("Made by S.Atan")
        st.markdown("---")

        faq()
