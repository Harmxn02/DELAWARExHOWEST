import requests
import time
import config

# Function to analyze the PDF using Document Intelligence
def analyze_pdf(pdf_url):
    analyze_url = f"{config.DOC_INTEL_ENDPOINT}/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": config.DOC_INTEL_API_KEY,
    }
    data = {"urlSource": pdf_url}

    response = requests.post(analyze_url, headers=headers, json=data)

    if response.status_code == 202:
        operation_location = response.headers["Operation-Location"]
        while True:
            result_response = requests.get(
                operation_location,
                headers={"Ocp-Apim-Subscription-Key": config.DOC_INTEL_API_KEY},
            )
            result_json = result_response.json()

            # Debugging output to understand the response structure
            # print("Response from Document Intelligence:", result_json)

            if result_json["status"] in ["succeeded", "failed"]:
                break
            time.sleep(1)

        # Check if the analysis succeeded
        if result_json["status"] == "succeeded":
            if (
                "analyzeResult" in result_json
                and "content" in result_json["analyzeResult"]
            ):
                extracted_text = result_json["analyzeResult"]["content"]
                # print("Extracted Text:\n", extracted_text)  # Print the extracted text
                return extracted_text
            else:
                print("No content found in the response.")
                return None
    else:
        print("Error in initiating analysis:", response.json())
        return None


# Function to query OpenAI
def ask_openai(question, context):
    headers = {"Content-Type": "application/json", "api-key": config.OPENAI_API_KEY}

    # Create the messages array for the chat model
    messages = [
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    data = {"messages": messages, "max_tokens": 150, "temperature": 0.7}

    response = requests.post(config.OPENAI_ENDPOINT, headers=headers, json=data)

    # Check the response status code
    print("OpenAI response status code:", response.status_code)

    # Print raw response for debugging
    try:
        # print("Raw OpenAI response text:", response.text)  # For debugging
        if response.status_code == 200:
            return response.json()["choices"][0]["message"][
                "content"
            ].strip()  # Updated structure
        else:
            print(
                "Error in OpenAI request:", response.json()
            )  # To see the error details
            return None
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response from OpenAI.")
        return None


# Main execution
if __name__ == "__main__":
    pdf_url = "https://harmansinghstorage.blob.core.windows.net/pdf-files/AI-Driven_Project_Estimation_and_Team_Planning_Platform.pdf"
    extracted_text = analyze_pdf(pdf_url)

    if extracted_text:
        # print("Extracted Text:\n", extracted_text)  # Show the full extracted text
        user_question = """
            What is the project about? Answer the question in a few sentences, using JSON, in this format:
            {
                "project": "Project Name",              // Name of the project
                "description": "Project Description"    // Long string, describing the project
            }
        """  # Example question
        answer = ask_openai(user_question, extracted_text)
        print("Answer:", answer)
