from langchain_community.embeddings import HuggingFaceEmbeddings
from constants import  MODEL_NAME
embeddings_model = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )