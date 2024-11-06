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

//#region Main execution
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

//#endregion

//#region CSV generator

// Function to convert JSON data to CSV format
function jsonToCsv(json) {
    const tasks = json.list_of_all_tasks;
    const rows = [["Task", "Description", "Fitting Employees (Role and Count)", "Estimated Days (Min)", "Estimated Days (Most Likely)", "Estimated Days (Max)", "Potential Issues"]];

    Object.entries(tasks).forEach(([taskName, taskData]) => {
        const description = taskData.description;

        // Convert fitting employees to a JSON-like string representation
        const fittingEmployees = `"${taskData.fitting_employees
            .map(employee => `${employee.role}: ${employee.count}`)
            .join("\n")}"`;

        const { min, most_likely, max } = taskData.estimated_days;

        // Convert potential issues to a JSON-like string representation
        const potentialIssues = `"${taskData.potential_issues
            .map(issue => issue)
            .join("\n")}"`;

        // Add row for each task
        rows.push([taskName, description, fittingEmployees, min, most_likely, max, potentialIssues]);
    });

    // Join rows with newline characters and comma-separated values for each row
    return rows.map(row => row.join(";")).join("\n");
}

// Function to download the CSV file
function downloadCsv(data, filename) {
    const blob = new Blob([data], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    // Create a temporary link to download the file
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    // Cleanup after download
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 0);
}

// Button click event to generate and download CSV
document.getElementById('generateCsvButton').addEventListener('click', async () => {
    try {
        // Fetch the JSON data from answer.json
        const response = await fetch('/answer.json');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const jsonData = await response.json();

        const csvData = jsonToCsv(jsonData);
        downloadCsv(csvData, "example.csv");
    } catch (error) {
        console.error("Error fetching JSON data:", error);
    }
});

//#endregion
