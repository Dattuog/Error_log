import os
import google.generativeai as genai
import markdown
from xhtml2pdf import pisa
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def analyze_log_with_gemini(file_path, log_type):
    """Sends log content to Gemini API for analysis."""
    if not GEMINI_API_KEY:
        return {
            "error": "Missing API Key",
            "content": "Please set the GEMINI_API_KEY environment variable or create a .env file."
        }

    if not os.path.exists(file_path):
        return {"error": "File Not Found", "content": f"File {file_path} does not exist."}

    try:
        with open(file_path, 'r') as f:
            log_content = f.read()

        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        You are an expert System Administrator and DevOps Engineer.
        Analyze the following {log_type} log file content.
        
        Identify the top 3 critical errors or issues.
        For each issue, provide:
        1. The specific error message or pattern.
        2. The root cause.
        3. A specific, actionable solution.

        Format your response in Markdown.

        Log Content:
        ```
        {log_content}
        ```
        """

        response = model.generate_content(prompt)
        return {"success": True, "content": response.text}

    except Exception as e:
        return {"error": "API Error", "content": str(e)}

def generate_report(results, output_file="generated_log_report.md"):
    """Generates a Markdown report from the analysis results."""
    report_content = ""
    report_content += "# Automated Log Analysis Report (Powered by Gemini)\n\n"
    report_content += f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for log_type, data in results.items():
        report_content += f"## {log_type.replace('_', ' ').title()} Analysis\n"
        report_content += f"**File:** `{data['file_path']}`\n\n"
        
        if "error" in data['result']:
            report_content += f"**Error:** {data['result']['error']}\n"
            report_content += f"{data['result']['content']}\n\n"
        else:
            report_content += data['result']['content']
            report_content += "\n\n"
        
        report_content += "---\n\n"

    with open(output_file, 'w') as f:
        f.write(report_content)
        
    print(f"Markdown Report generated successfully: {output_file}")
    return report_content

def generate_pdf(markdown_content, output_file="generated_log_report.pdf"):
    """Converts Markdown content to PDF."""
    try:
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Add basic styling
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Helvetica, sans-serif; font-size: 12px; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                h2 {{ color: #34495e; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
                code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
                pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Generate PDF
        with open(output_file, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(styled_html, dest=pdf_file)

        if pisa_status.err:
            print(f"Error generating PDF: {pisa_status.err}")
        else:
            print(f"PDF Report generated successfully: {output_file}")
            
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

def main():
    log_dir = "logs"
    md_output_file = "generated_log_report.md"
    pdf_output_file = "generated_log_report.pdf"
    
    # Map filenames to log types
    files_to_check = [
        ("web_server.log", "web_server"),
        ("database.log", "database"),
        ("application.log", "application")
    ]
    
    print("Starting Automated Log Analysis with Gemini...\n")
    
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY not found.")
        print("Please set it in the .env file or as an environment variable.")
        # We continue to demonstrate PDF generation even if API fails (it will report errors)
    else:
        genai.configure(api_key=GEMINI_API_KEY)
    
    results = {}
    
    for filename, log_type in files_to_check:
        file_path = os.path.join(log_dir, filename)
        print(f"Analyzing {filename}...")
        result = analyze_log_with_gemini(file_path, log_type)
        results[log_type] = {
            "file_path": file_path,
            "result": result
        }

    markdown_content = generate_report(results, md_output_file)
    generate_pdf(markdown_content, pdf_output_file)
    print("Analysis Complete.")

if __name__ == "__main__":
    main()
