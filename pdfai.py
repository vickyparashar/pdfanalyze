import PyPDF2
import requests

def extract_text(pdf_path):
    """Extracts text from the given PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def send_to_ollama(prompt_text):
    """Sends the combined prompt text to the Ollama API and returns the response."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:4b",
        "prompt": prompt_text,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error sending request: {e}")
        return {}

if __name__ == "__main__":
    # Step 1: Define the PDF file path (assumes it is in the same directory)
    pdf_path = "example.pdf"
    
    # Step 2: Extract text from the PDF.
    pdf_text = extract_text(pdf_path)
    if not pdf_text:
        print("Failed to extract any text from the PDF. Exiting.")
        exit(1)
    print("\nPDF text extracted successfully!")
    
    # Step 3: Ask the user for a question regarding the PDF.
    question = input("\nEnter your question about the PDF: ")
    
    # Step 4: Combine the PDF text with the user's question.
    full_prompt = (
        "Based on the following PDF content, please answer the question below:\n\n"
        f"PDF Content:\n{pdf_text}\n"
        f"Question: {question}"
    )
    
    # Step 5: Send the prompt to the Ollama API.
    print("\nSending your prompt to the API...")
    result = send_to_ollama(full_prompt)
    
    # Step 6: Print the API response.
    answer = result.get("response", "No response received.")
    print("\nAnswer from API:")
    print(answer)
