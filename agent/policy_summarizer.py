import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def summarize_vector_policies(vector_db, employee):
    """Summarizes policies using the Gemini API."""
    api_key = "AIzaSyCk9bzsacfn92c-Ww2ZvO2ETxi6NV59bQI"

    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Construct policy queries
    leave_query = f"summarize the leave policy for Band {employee['Band']} and Department {employee['Department']}"
    travel_query = f"summarize the travel policy for Band {employee['Band']} and Department {employee['Department']}"
    wfo_query = f"summarize the work from office policy for Band {employee['Band']} and Department {employee['Department']}"

    # Search top chunks from vector DB
    leave_docs = vector_db.similarity_search(leave_query, k=3)
    travel_docs = vector_db.similarity_search(travel_query, k=3)
    wfo_docs = vector_db.similarity_search(wfo_query, k=3)

    leave_summary, travel_summary, wfo_summary = "", "", ""

    # Helper function to summarize safely
    def summarize_docs(docs, policy_type):
        summary_text = " ".join([doc.page_content for doc in docs])
        
        # Print the retrieved document text for debugging
        print(f"\n--- Retrieved text for {policy_type.upper()} ---")
        print(summary_text)

        prompt = f"Summarize the following {policy_type} in a concise paragraph:\n\n{summary_text}"
        
        # Print the full prompt for debugging
        print(f"\n--- Prompt for {policy_type.upper()} ---")
        print(prompt)

        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Summarization failed for {policy_type}: {e}")
            return "Policy summary not available."

    # Perform summaries
    leave_summary = summarize_docs(leave_docs, "leave policy")
    travel_summary = summarize_docs(travel_docs, "travel policy")
    wfo_summary = summarize_docs(wfo_docs, "work from office policy")


    # Add print statements for debugging
    print(f"\n✅ Leave Policy Summary: {leave_summary}")
    print(f"✅ Travel Policy Summary: {travel_summary}")
    print(f"✅ WFO Policy Summary: {wfo_summary}")


    return {
        "leave": leave_summary,
        "travel": travel_summary,
        "wfo": wfo_summary
    }