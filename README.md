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
