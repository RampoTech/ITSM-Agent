from phi.knowledge.document import DocumentKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.embedder.ollama import OllamaEmbedder
from phi.document import Document
import dotenv
import os
from phi.knowledge.docx import DocxKnowledgeBase

dotenv.load_dotenv()

db_url = os.getenv("DB_URL")

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

# Read file manually
# with open("/home/ishva/Projects/Agentic_AI_Capstone/data/docs/Issues-Mail.docx", "r") as f:
#     content = f.read()

# documents = [
#     Document(
#         content=content,
#         meta_data={"source": "network_errors.txt"}
#     )
# ]

knowledge_base = DocxKnowledgeBase(
    path="data/docs",
    num_documents=1,
    vector_db=PgVector(
        table_name="documents",
        
        db_url=db_url,
        embedder=OllamaEmbedder(model="embeddinggemma:300m",host=OLLAMA_HOST,dimensions=768),
        
    ),
)
knowledge_base.load(recreate=False)