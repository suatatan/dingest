import streamlit as st

from components.sidebar import sidebar

from ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)

from core.caching import bootstrap_caching

from core.parsing import read_file
from core.chunking import chunk_file
from core.embedding import embed_files
from core.qa import query_folder
from core.utils import get_llm
from core.directprompt import organize_info_from_invoice


EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="Dingest", page_icon="🫖", layout="wide")
st.header("🫖 Dingest")

# Enable caching for expensive functions
bootstrap_caching()

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")


if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )
# ----------------------------------
    
invoice_file = st.file_uploader('1️⃣Upload the invoice', type=['pdf'], help="Scanned documents are not supported yet!")
if not invoice_file:
    st.stop()
try:
    ifile = read_file(invoice_file)
except Exception as e:
    display_file_read_error(e, file_name=invoice_file.name)
extracted_invoice = ifile.docs[0].page_content
if not is_open_ai_key_valid(openai_api_key, MODEL_LIST[0]):
    st.stop()
# with st.spinner("Indexing document... This may take a while⏳"):
result = organize_info_from_invoice(extracted_invoice,openai_api_key=openai_api_key)

st.markdown(result, unsafe_allow_html=True)

# uploaded_file = st.file_uploader(
#     "Upload a pdf, docx, or txt file",
#     type=["pdf", "docx", "txt"],
#     help="Scanned documents are not supported yet!",
# )

# # model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

# model = MODEL_LIST[0]

# with st.expander("Advanced Options"):
#     return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
#     show_full_doc = st.checkbox("Show parsed contents of the document")


# if not uploaded_file:
#     st.stop()

# try:
#     file = read_file(uploaded_file)
# except Exception as e:
#     display_file_read_error(e, file_name=uploaded_file.name)

# chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

# if not is_file_valid(file):
#     st.stop()


# if not is_open_ai_key_valid(openai_api_key, model):
#     st.stop()


# with st.spinner("Indexing document... This may take a while⏳"):
#     folder_index = embed_files(
#         files=[chunked_file],
#         embedding=EMBEDDING if model != "debug" else "debug",
#         vector_store=VECTOR_STORE if model != "debug" else "debug",
#         openai_api_key=openai_api_key,
#     )


# with st.form(key="qa_form"):
#     options = ['List all pre existing conditions which may affect home insurance', 'Show the problematic components!', 'Show repair needs!']
#     query = st.selectbox('Select an option', options)
#     submit = st.form_submit_button("Submit")


# if show_full_doc:
#     with st.expander("Document"):
#         # Hack to get around st.markdown rendering LaTeX
#         st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


# if submit:
#     if not is_query_valid(query):
#         st.stop()

#     # Output Columns
#     answer_col, sources_col = st.columns(2)

#     llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
#     result = query_folder(
#         folder_index=folder_index,
#         query=query,
#         return_all=return_all_chunks,
#         llm=llm,
#     )

#     with answer_col:
#         st.markdown("#### Answer")
#         st.markdown(result.answer)

#     with sources_col:
#         st.markdown("#### Sources")
#         for source in result.sources:
#             st.markdown(source.page_content)
#             st.markdown(source.metadata["source"])
#             st.markdown("---")


