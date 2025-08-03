import os
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from agent.html_template_builder import build_html
from agent.prompt_builder import build_prompt
from agent.pdf_generator import generate_pdf
from agent.offer_letter_generator import generate_letter
from agent.policy_summarizer import summarize_vector_policies

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/pdfs", StaticFiles(directory="output/generated_letters"), name="pdfs")

# Initialize the vector database once at startup
try:
    documents = []
    data_dir = "data"
    for filename in os.listdir(data_dir):
        # Only process files that have "Policy" in the name
        if "Policy" in filename and filename.endswith(".pdf"):
            file_path = os.path.join(data_dir, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    
    if not documents:
        raise FileNotFoundError("No policy documents found in the 'data' directory.")

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    # Use a pre-trained embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a FAISS vector store
    vector_db = FAISS.from_documents(splits, embedding_model)
    print("Vector database created successfully.")
except Exception as e:
    vector_db = None
    print(f"❌ Failed to create vector database: {e}")
    print("Please ensure the 'data' directory contains policy PDF files and dependencies are installed.")

class EmployeeRequest(BaseModel):
    employee_name: str

@app.post("/generate-letter")
async def generate_letter_api(req: EmployeeRequest):
    try:
        if vector_db is None:
            return {"status": "error", "message": "Vector database is not initialized. Please check server logs for details."}
            
        df = pd.read_csv("data/Employee_List.csv")
        employee = df[df["Employee Name"].str.strip() == req.employee_name].iloc[0].to_dict()

        summaries = summarize_vector_policies(vector_db, employee)
        prompt = build_prompt(employee, summaries)
        letter = generate_letter(prompt)
        
        html_string = build_html(employee, summaries)
        pdf_path = generate_pdf(req.employee_name, html_string)
        filename = os.path.basename(pdf_path)

        return {
            "status": "success",
            "offer_letter": letter,
            "pdf_file": filename
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get-pdf/{filename}")
async def get_pdf(filename: str):
    file_path = os.path.join("output/generated_letters", filename)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        return Response(
            content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="{filename}"',
                "Access-Control-Allow-Origin": "*"
            }
        )
    return {"status": "error", "message": "File not found"}