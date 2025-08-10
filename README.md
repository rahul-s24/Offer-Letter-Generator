# 📄 Offer Letter Generator

This project provides a simple yet effective system for generating customized offer letters for new employees. It leverages policy documents (Leave, Travel) and employee data to create tailored offer letters, ensuring compliance with company policies.

---

##  Features

- **Automated Offer Letter Generation** – Dynamically creates offer letters based on employee details and relevant company policies.  
- **Policy Integration** – Extracts pertinent information from PDF documents (e.g., HR Leave Policy, HR Travel Policy) to include in the offer letters.  
- **Employee Data Management** – Reads employee information from a CSV file to populate offer letter fields.  
- **Customizable Templates** – Uses a sample offer letter as a template, allowing for consistent formatting and content.  
- **Scalable** – Designed to be easily adaptable for different departments and band levels by retrieving relevant policy sections.  

---

## 🛠️ Technologies Used

- **Python** – Core programming language for the application logic.  
- **LangChain** – Document loading, splitting, and managing LLM interactions.  
- **Sentence Transformers** – Generates embeddings for policy documents for semantic search.  
- **FAISS** – Efficient similarity search and clustering of dense vectors, used as a vector store.  
- **Pandas** – CSV parsing and employee data handling.  
- **Hugging Face Transformers** – Text generation pipeline (`google/flan-t5-base`).  
- **PyPDFLoader** – Loads content from PDF documents.  

---
Feel free to fork this repository, submit issues, or propose pull requests. Contributions are welcome!

