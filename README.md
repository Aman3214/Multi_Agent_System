# Intelligent Document Processor (Placeholder Name - Please Change)

A Python-based application designed to automatically classify, process, and extract information from various file types like emails and JSON documents using Langchain agents and Hugging Face transformer models.

## Table of Contents

- [Features](#features)
- [File Structure](#file-structure)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Example Data](#example-data)

## Features

-   **Automatic File Classification**: Identifies the format (Email, JSON, PDF) and intent (RFQ, Invoice, Complaint, Regulation, Other) of input files.
-   **Agent-Based Processing**: Utilizes specialized Langchain agents for handling different document types:
    -   **Email Agent**: Extracts key information (sender, recipient, intent, urgency) from email content.
    -   **JSON Agent**: Validates and normalizes JSON data against a predefined schema.
-   **LLM Powered**: Leverages Hugging Face transformer models for classification (`facebook/bart-large-mnli`) and text generation/extraction (`google/flan-t5-large`).
-   **Persistent Memory**: Logs all processing steps, extracted information, and agent actions to an SQLite database (`memory.db`) for traceability and review.
-   **Command-Line Interface**: Easy to run via CLI, supporting processing of single or multiple files.
-   **Modular Design**: Separated components for agent management, classification, specific agent logic, and utility functions.

## File Structure

```
.
├── agents
│ ├── classifier.py # Handles input classification (format and intent)
│ ├── emailAgent.py # Agent logic for processing email files
│ └── jsonAgent.py # Agent logic for processing JSON files
├── data # Sample data files for testing
│ ├── complaint_email.txt
│ ├── invoice_submission.json
│ ├── new_regulation.json
│ └── rfq_email.txt
├── main.py # Main script to run the document processing
├── requirements.txt # Python dependencies
└── tools
├── memory.db # temp file generated on running the main.py file 
├── constants.py # Defines constant labels for classification
└── memory_interface.py # Handles interaction with the SQLite memory database
```
## Technologies Used

-   **Python 3.x**
-   **Langchain**: For building and managing LLM-powered agents and chains.
-   **Hugging Face Transformers**:
    -   `pipeline` for easy model inference.
    -   `facebook/bart-large-mnli` for zero-shot classification.
    -   `google/flan-t5-large` for text-to-text generation tasks (extraction, normalization).
-   **PyTorch**: As a backend for Hugging Face Transformers.
-   **SQLite**: For the `memory.db` logging database.
-   **python-magic**: (Listed in `requirements.txt`, though not explicitly used in the provided Python files for format detection. Current format detection is extension-based or uses zero-shot classification).

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/Aman3214/Multi_Agent_Systems
    cd multiAgent # change to your project repo
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    conda create --name multiAgent python=3.10
    conda activate multiAgent  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will download and install all necessary libraries, including PyTorch and Hugging Face models (which might take some time and disk space on first run).

4.  **Database:**
    The SQLite database `memory.db` will be created automatically in the project's root directory when the application is first run.

## Usage

The application is run from the command line using `main.py`. You need to provide one or more file paths as arguments.

**Processing one or more files:**

```bash
python main.py path/to/your/file1.txt path/to/your/file2.json
```
**Example using provided data files:**

python main.py data/rfq_email.txt data/invoice_submission.json



**Optional Arguments:**

--conversation_id <ID>: Specify a custom conversation ID. If not provided, a new UUID will be generated.

--dry_run: Perform a dry run (currently, the dry_run flag is passed to process_file but not explicitly used in the core processing logic of agents or classifier beyond logging).

**Output:**

The application will log processing information to the console.

Detailed logs, including extracted information, will be stored in the memory.db SQLite database. You can inspect this database using any SQLite browser.

The agents (EmailAgent, JSONAgent) will print their results to the console.

To view logs from the database for a specific conversation ID (or all logs if ID is omitted):
You can adapt the print_logs function in tools/memory_interface.py to be callable from a separate script or add CLI options to main.py for this. For example, to add a quick way to view logs, you could modify memory_interface.py to be runnable:

# tools/memory_interface.py (add at the end)

Then run: python tools/memory_interface.py [optional_conversation_id]

**How It Works**

Input: The main.py script takes file paths as input.

Classification: For each file:

agents/classifier.py reads the file content.

It detects the file format (Email, JSON, PDF) based on extension or using a zero-shot-classification model (facebook/bart-large-mnli).

It classifies the intent of the content using the same model and predefined labels (tools/constants.py) and then routes the control to the appropriate agent.

This initial classification is logged to memory.db.

**Specialized Processing:**

- EmailAgent (agents/emailAgent.py):

        Receives the email content.

        Uses an LLMChain with a google/flan-t5-large model and a specific prompt to extract sender, recipient, intent, and urgency.

        Logs the extracted information to memory.db.

- JSONAgent (agents/jsonAgent.py):

        Receives the JSON content.

        Uses an LLMChain with a google/flan-t5-large model and a specific prompt to normalize the JSON to a target schema and flag missing fields.

        Logs the processed information to memory.db.

- Logging: All significant steps and outcomes are logged to the memory.db SQLite database via tools/memory_interface.py, associated with a unique conversation_id.

**Example Data**

The data/ directory contains sample files you can use for testing:

- complaint_email.txt: An example of an email with a complaint.

- invoice_submission.json: An example of a JSON payload representing an invoice.

- new_regulation.json: An example of a JSON payload detailing a new regulation.

- rfq_email.txt: An example of an email containing a Request for Quotation.

Run the processor with these files:
```bash
python main.py data/complaint_email.txt data/invoice_submission.json data/new_regulation.json data/rfq_email.txt
```
or simply
```bash
python main.py data/
```
to process all the files in the directory
