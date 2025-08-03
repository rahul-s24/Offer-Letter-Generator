import torch
from transformers import pipeline
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def summarize_vector_policies(vector_db, employee):
    # Use GPU if available, else CPU
    device = 0 if torch.cuda.is_available() else -1
    print(f"Device set to use {'cuda' if device == 0 else 'cpu'}")

    # Load summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

    # Construct policy queries
    leave_query = f"leave policy for Band {employee['Band']} and Department {employee['Department']}"
    travel_query = f"travel policy for Band {employee['Band']} and Department {employee['Department']}"

    # Search top chunks from vector DB
    leave_docs = vector_db.similarity_search(leave_query, k=3)
    travel_docs = vector_db.similarity_search(travel_query, k=3)

    leave_summary, travel_summary = "", ""

    # Helper function to summarize safely
    def summarize_docs(docs, policy_type):
        summary = ""
        for doc in docs:
            try:
                content = doc.page_content[:3500]  # Truncate if too long
                result = summarizer(content, max_length=150, min_length=30, do_sample=False)
                summary += result[0]["summary_text"].strip() + "\n"
            except Exception as e:
                print(f"❌ Summarization failed for {policy_type}: {e}")
        return summary.strip() if summary.strip() else "Policy summary not available."

    # Perform summaries
    leave_summary = summarize_docs(leave_docs, "leave policy")
    travel_summary = summarize_docs(travel_docs, "travel policy")

    return {
        "leave": leave_summary,
        "travel": travel_summary
    }
