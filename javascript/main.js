async function analyzePdf(pdfUrl) {
    const analyzeUrl = `${config.DOC_INTEL_ENDPOINT}/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31`;
    const headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": config.DOC_INTEL_API_KEY
    };
    const data = JSON.stringify({ urlSource: pdfUrl });

    try {
        const response = await fetch(analyzeUrl, { method: 'POST', headers: headers, body: data });

        if (response.status === 202) {
            const operationLocation = response.headers.get("Operation-Location");

            while (true) {
                const resultResponse = await fetch(operationLocation, {
                    method: 'GET',
                    headers: { "Ocp-Apim-Subscription-Key": config.DOC_INTEL_API_KEY }
                });
                const resultJson = await resultResponse.json();

                if (resultJson.status === "succeeded") {
                    return resultJson.analyzeResult && resultJson.analyzeResult.content
                        ? resultJson.analyzeResult.content
                        : null;
                } else if (resultJson.status === "failed") {
                    console.error("Analysis failed:", resultJson);
                    return null;
                }

                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        } else {
            console.error("Error initiating analysis:", await response.json());
            return null;
        }
    } catch (error) {
        console.error("Error during PDF analysis:", error);
        return null;
    }
}

async function askOpenAI(question, context) {
    const headers = {
        "Content-Type": "application/json",
        "api-key": config.OPENAI_API_KEY
    };

    const messages = [
        { role: "user", content: `Context:\n${context}\n\nQuestion: ${question}` }
    ];

    const data = JSON.stringify({ messages: messages, max_tokens: 150, temperature: 0.7 });

    try {
        const response = await fetch(config.OPENAI_ENDPOINT, { method: 'POST', headers: headers, body: data });

        if (response.status === 200) {
            const resultJson = await response.json();
            return resultJson.choices[0].message.content.trim();
        } else {
            console.error("Error in OpenAI request:", await response.json());
            return null;
        }
    } catch (error) {
        console.error("Failed to decode JSON response from OpenAI:", error);
        return null;
    }
}

// Main execution
// Using a PDF file
document.getElementById('analyzeButton').addEventListener('click', async () => {
    const pdfUrl = "https://harmansinghstorage.blob.core.windows.net/pdf-files/AI-Driven_Project_Estimation_and_Team_Planning_Platform.pdf";
    const extractedText = await analyzePdf(pdfUrl);

    if (extractedText) {
        const userQuestion = `
            What is the project about? Answer the question in a few sentences, using JSON, in this format:
            {
                "project": "Project Name",
                "description": "Project Description"
            }
        `;

        const answer = await askOpenAI(userQuestion, extractedText);
        document.getElementById('result').innerText = "Answer:\n" + answer;
    } else {
        document.getElementById('result').innerText = "Failed to extract text from PDF.";
    }
});

// Using a CSV file
document.getElementById('analyzeCsvButton').addEventListener('click', async () => {
    const fileInput = document.getElementById('csvInput');
    if (fileInput.files.length === 0) {
        alert("Selecteer een CSV-bestand.");
        return;
    }

    const file = fileInput.files[0];
    const csvContent = await file.text();

    // Function to parse CSV to JSON
    function parseCsv(csv) {
        const lines = csv.trim().split("\n");
        const headers = lines[0].split(",");
        const data = lines.slice(1).map(line => {
            const values = line.split(",");
            return headers.reduce((obj, header, i) => {
                obj[header.trim()] = values[i].trim();
                return obj;
            }, {});
        });
        return data;
    }

    const csvData = parseCsv(csvContent);

    // Ask the LLM
    const userQuestion = `
        Wat zijn de belangrijkste inzichten van dit CSV-bestand? Geef een samenvatting in JSON-formaat zoals:
        {
            "key_points": ["Belangrijk punt 1", "Belangrijk punt 2", ...]
        }
    `;

    const answer = await askOpenAI(userQuestion, JSON.stringify(csvData));
    document.getElementById('result').innerText = "Answer:\n" + answer;
});
