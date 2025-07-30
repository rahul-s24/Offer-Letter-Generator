print("✅ This is the REAL main.py being executed.")
from data import policy_paths
from data.employee_loader import load_employee
from embedding.embedder import load_and_chunk
from embedding.vector_store import create_vector_store
from agent.letter_generator import generate_letter
import os

print("🔥 main.py loaded")

def main():
    print("🚀 Inside main()") 
    employee_name = input("Enter employee name: ")
    
    print(f"👤 Employee selected: {employee_name}")

    # Load employee data
    employee = load_employee(employee_name, policy_paths.EMPLOYEE_CSV_PATH)

    # Load and chunk policies
    all_chunks = (
        load_and_chunk(policy_paths.LEAVE_POLICY_PATH)
        + load_and_chunk(policy_paths.TRAVEL_POLICY_PATH)
        + load_and_chunk(policy_paths.OFFER_LETTER_SAMPLE_PATH)
    )

    # Create vector store from policy chunks
    vector_db = create_vector_store(all_chunks)

    # Retrieve policy context
    query = f"Leave, WFO, and travel policies applicable to Band {employee['Band']}"
    results = vector_db.similarity_search(query, k=5)
    policy_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    # Generate the letter
    letter = generate_letter(employee, policy_text)

    # Save the letter
    os.makedirs("output/generated_letters", exist_ok=True)
    out_path = f"output/generated_letters/OfferLetter_{employee_name.replace(' ', '_')}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(letter)

    print(f"\n✅ Offer letter saved to: {out_path}")

if __name__ == "__main__":
    print("🔥 Starting main()...")
    main()