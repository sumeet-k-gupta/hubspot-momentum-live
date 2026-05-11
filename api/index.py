import os
import subprocess
import json

# Set up paths relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.join(PROJECT_ROOT, "..")
DATA_DIR = os.path.join(BASE_DIR, "data")
ANALYZER_PATH = os.path.join(BASE_DIR, "analyzer.py")
GENERATOR_PATH = os.path.join(BASE_DIR, "data_generator.py")
DASHBOARD_GEN_PATH = os.path.join(BASE_DIR, "dashboard_generator.py")
DASHBOARD_HTML_PATH = os.path.join(BASE_DIR, "dashboard.html")

def handler(event, context):
    """
    Vercel Serverless Function entry point.
    """
    try:
        # 1. Run Generation
        subprocess.run(["python3", GENERATOR_PATH], check=True, capture_output=True)
        
        # 2. Run Analysis
        subprocess.run(["python3", ANALYZER_PATH], check=True, capture_output=True)
        
        # 3. Run Dashboard Generation
        subprocess.run(["python3", DASHBOARD_GEN_PATH], check=True, capture_output=True)

        # 4. Read the generated dashboard
        if not os.path.exists(DASHBOARD_HTML_PATH):
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Dashboard generation failed: HTML not found."})
            }

        with open(DASHBOARD_HTML_PATH, "r") as f:
            html_content = f.read()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html",
                "Access-Control-Allow-Origin": "*"
            },
            "body": html_content
        }

    except subprocess.CalledProcessError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Pipeline execution failed",
                "stdout": e.stdout.decode(),
                "stderr": e.stderr.decode()
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
