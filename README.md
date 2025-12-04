# AI-Powered Log Analyzer

This project is an automated log analysis tool that uses Google's Gemini API to parse server logs, identify critical errors, identify root causes, and suggest actionable solutions. It generates detailed reports in both Markdown and PDF formats.

## Features

-   **AI-Driven Analysis:** Uses Google Gemini (gemini-2.0-flash) to understand log context.
-   **Multi-Format Reports:** Generates `generated_log_report.md` and `generated_log_report.pdf`.
-   **Secure Configuration:** Uses `.env` file for secure API key management.
-   **Supports Multiple Log Types:** Analyzes Web Server, Database, and Application logs.

## Prerequisites

-   Python 3.x
-   A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Dattuog/Error_log.git
    cd Error_log
    ```

2.  Install dependencies:
    ```bash
    pip install google-generativeai markdown xhtml2pdf python-dotenv
    ```

## Configuration

1.  Create a `.env` file in the project root:
    ```bash
    touch .env  # On Windows use: type nul > .env
    ```

2.  Add your Gemini API key to the `.env` file:
    ```
    GEMINI_API_KEY=your_actual_api_key_here
    ```
    *Note: Never commit your `.env` file to version control.*

## Usage

1.  Place your log files in the `logs/` directory (e.g., `web_server.log`, `database.log`, `application.log`).
2.  Run the analyzer:
    ```bash
    python log_analyzer.py
    ```
3.  Check the generated reports:
    -   `generated_log_report.md`
    -   `generated_log_report.pdf`

## Project Structure

-   `log_analyzer.py`: Main script.
-   `logs/`: Directory for input log files.
-   `.env`: Configuration file for API keys (not in repo).
-   `generated_log_report.*`: Output reports.

## System Design & Workflow

The following diagram illustrates the workflow of the AI-Powered Log Analyzer:

```mermaid
graph TD
    A[Start] --> B{Check Configuration};
    B -- Missing API Key --> C[Error: Exit];
    B -- Config OK --> D[Read Log Files];
    D --> E{For Each Log File};
    E --> F[Read Content];
    F --> G[Construct Prompt];
    G --> H[Call Gemini API (gemini-2.0-flash)];
    H --> I[Receive Analysis];
    I --> J[Store Results];
    J --> E;
    E -- All Files Processed --> K[Generate Markdown Report];
    K --> L[Convert to PDF];
    L --> M[End];
```

### Workflow Steps

1.  **Initialization**: The script starts and checks for the `GEMINI_API_KEY` in the environment variables (loaded from `.env`).
2.  **Data Ingestion**: It iterates through the predefined log files (`web_server.log`, `database.log`, `application.log`) in the `logs/` directory.
3.  **AI Analysis**:
    -   For each file, it constructs a prompt acting as a generic System Administrator.
    -   It sends the log content to the **Google Gemini 2.0 Flash** model.
    -   The model identifies critical errors, root causes, and solutions.
4.  **Report Generation**:
    -   The analysis results are compiled into a structured **Markdown** report.
    -   The Markdown report is then converted into a professional **PDF** document using `xhtml2pdf`.

