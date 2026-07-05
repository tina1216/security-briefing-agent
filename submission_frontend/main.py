import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Add parent directory to sys.path to import the app.agent module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Load environment variables from the parent directory's .env file if it exists
dotenv_path = os.path.join(parent_dir, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Ensure GOOGLE_API_KEY is mapped to GEMINI_API_KEY for ADK / google-genai
if "GOOGLE_API_KEY" in os.environ:
    os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

from google.adk.runners import Runner  # noqa: E402
from google.adk.sessions import InMemorySessionService  # noqa: E402
from google.genai import types  # noqa: E402

from app.agent import root_agent  # noqa: E402

app = FastAPI(title="Daily Security Briefing Frontend")

# Setup ADK session service and runner
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    app_name="security-briefing-agent-frontend",
)


class RunPayload(BaseModel):
    query: str = "Generate my daily security briefing"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Security Briefing</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --bg-color: #121212;
            --surface-color: #1e1e1e;
            --surface-overlay: #272727;
            --accent-primary: #bb86fc; /* Material Dark Primary (Purple) */
            --accent-secondary: #03dac6; /* Material Dark Secondary (Teal) */
            --text-primary: rgba(255, 255, 255, 0.87);
            --text-secondary: rgba(255, 255, 255, 0.60);
            --text-disabled: rgba(255, 255, 255, 0.38);
            --error-color: #cf6679;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 3rem 2rem;
        }

        .container {
            width: 100%;
            max-width: 900px;
        }

        .card {
            background-color: var(--surface-color);
            border-radius: 8px;
            padding: 2.5rem;
            box-shadow: 0px 5px 5px -3px rgba(0,0,0,0.2),
                        0px 8px 10px 1px rgba(0,0,0,0.14),
                        0px 3px 14px 2px rgba(0,0,0,0.12);
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        h1 {
            font-size: 2.125rem;
            font-weight: 500;
            letter-spacing: 0.00735em;
            color: var(--text-primary);
            text-align: center;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            text-align: center;
            color: var(--accent-primary);
            font-size: 0.875rem;
            font-weight: 500;
            letter-spacing: 0.089em;
            text-transform: uppercase;
            margin-top: -1rem;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        label {
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.033em;
            color: var(--text-secondary);
        }

        .input-wrapper {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        input[type="text"] {
            flex: 1;
            background-color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.23);
            border-radius: 4px;
            padding: 1rem;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 1rem;
            transition: border-color 0.2s, box-shadow 0.2s;
            outline: none;
        }

        input[type="text"]:hover {
            border-color: rgba(255, 255, 255, 0.87);
        }

        input[type="text"]:focus {
            border-color: var(--accent-primary);
            border-width: 2px;
            padding: calc(1rem - 1px);
        }

        button {
            background-color: var(--accent-secondary);
            color: #000000;
            border: none;
            border-radius: 4px;
            padding: 1rem 2rem;
            font-family: inherit;
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.08928em;
            cursor: pointer;
            transition: background-color 0.2s, box-shadow 0.2s, transform 0.1s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            box-shadow: 0px 3px 1px -2px rgba(0,0,0,0.2),
                        0px 2px 2px 0px rgba(0,0,0,0.14),
                        0px 1px 5px 0px rgba(0,0,0,0.12);
        }

        button:hover {
            background-color: #04ebd5;
            box-shadow: 0px 2px 4px -1px rgba(0,0,0,0.2),
                        0px 4px 5px 0px rgba(0,0,0,0.14),
                        0px 1px 10px 0px rgba(0,0,0,0.12);
        }

        button:active {
            transform: scale(0.98);
        }

        button:disabled {
            background-color: rgba(255, 255, 255, 0.12);
            color: var(--text-disabled);
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }

        .spinner {
            width: 18px;
            height: 18px;
            border: 2px solid rgba(0, 0, 0, 0.2);
            border-radius: 50%;
            border-top-color: #000000;
            animation: spin 0.8s linear infinite;
            display: none;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .results-panel {
            background-color: var(--surface-overlay);
            border-radius: 8px;
            padding: 2rem;
            min-height: 250px;
            display: flex;
            flex-direction: column;
            transition: all 0.3s ease;
            box-shadow: inset 0px 2px 4px rgba(0,0,0,0.3);
        }

        .results-placeholder {
            margin: auto;
            color: var(--text-secondary);
            text-align: center;
            font-style: italic;
            font-size: 0.95rem;
        }

        .markdown-body {
            line-height: 1.7;
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.87);
        }

        .markdown-body h2 {
            font-size: 1.5rem;
            font-weight: 500;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--accent-primary);
        }

        .markdown-body h3 {
            font-size: 1.2rem;
            font-weight: 500;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            color: var(--accent-secondary);
        }

        .markdown-body p {
            margin-bottom: 1.25rem;
            color: rgba(255, 255, 255, 0.87);
        }

        .markdown-body ul, .markdown-body ol {
            margin-bottom: 1.25rem;
            padding-left: 1.5rem;
        }

        .markdown-body li {
            margin-bottom: 0.5rem;
        }

        .markdown-body table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 4px;
            overflow: hidden;
            background-color: var(--surface-color);
            box-shadow: 0px 2px 1px -1px rgba(0,0,0,0.2),
                        0px 1px 1px 0px rgba(0,0,0,0.14),
                        0px 1px 3px 0px rgba(0,0,0,0.12);
        }

        .markdown-body th, .markdown-body td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }

        .markdown-body th {
            background-color: rgba(255, 255, 255, 0.04);
            font-weight: 500;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-secondary);
        }

        .markdown-body tr:last-child td {
            border-bottom: none;
        }

        .markdown-body a {
            color: var(--accent-secondary);
            text-decoration: none;
            border-bottom: 1px dashed var(--accent-secondary);
            transition: color 0.2s, border-bottom-color 0.2s;
        }

        .markdown-body a:hover {
            color: var(--accent-primary);
            border-bottom: 1px solid var(--accent-primary);
        }

        .footer-references {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-top: 1rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.12);
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .footer-references a {
            color: var(--accent-primary);
            text-decoration: none;
            border-bottom: 1px dotted var(--accent-primary);
            transition: color 0.2s, border-bottom-color 0.2s;
        }

        .footer-references a:hover {
            color: var(--accent-secondary);
            border-bottom: 1px solid var(--accent-secondary);
        }

        @media (max-width: 640px) {
            body {
                padding: 1rem;
            }
            .card {
                padding: 1.5rem;
            }
            .input-wrapper {
                flex-direction: column;
                align-items: stretch;
            }
            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div>
                <h1>Daily Security Briefing</h1>
            </div>

            <div class="input-group">
                <label for="query">Custom Briefing Prompt</label>
                <div class="input-wrapper">
                    <input type="text" id="query" value="Generate my daily security briefing" placeholder="Describe scope or enter custom instructions...">
                    <button id="run-btn" onclick="runBriefing()">
                        <span class="spinner" id="spinner"></span>
                        <span id="btn-text">Run Briefing</span>
                    </button>
                </div>
            </div>

            <div class="results-panel" id="results-panel">
                <div class="results-placeholder" id="placeholder">
                    Click "Run Briefing" to compile today's security intelligence.
                </div>
                <div class="markdown-body" id="markdown-content" style="display: none;"></div>
            </div>

            <div class="footer-references">
                <span>Intelligence Sources:</span>
                <a href="https://nvd.nist.gov/" target="_blank" rel="noopener noreferrer">NIST NVD CVEs</a>
                <a href="https://html.duckduckgo.com/" target="_blank" rel="noopener noreferrer">DuckDuckGo Security News</a>
                <a href="https://cloud.google.com/vertex-ai" target="_blank" rel="noopener noreferrer">Vertex AI Models</a>
            </div>
        </div>
    </div>

    <script>
        // Configure marked renderer for link rendering (supporting newer single-object signature as well as old signature)
        const renderer = new marked.Renderer();
        renderer.link = function(token, title, text) {
            let hrefStr, titleStr, textStr;
            if (typeof token === 'object' && token !== null) {
                hrefStr = token.href;
                titleStr = token.title;
                textStr = token.text || token.raw || token.href;
            } else {
                hrefStr = token;
                titleStr = title;
                textStr = text || title || token;
            }
            return `<a href="${hrefStr}" title="${titleStr || ''}" target="_blank" rel="noopener noreferrer">${textStr}</a>`;
        };
        marked.use({ renderer });

        async function runBriefing() {
            const queryInput = document.getElementById('query');
            const runBtn = document.getElementById('run-btn');
            const spinner = document.getElementById('spinner');
            const btnText = document.getElementById('btn-text');
            const placeholder = document.getElementById('placeholder');
            const contentDiv = document.getElementById('markdown-content');

            runBtn.disabled = true;
            spinner.style.display = 'block';
            btnText.innerText = 'Analyzing...';
            placeholder.style.display = 'none';
            contentDiv.style.display = 'none';
            contentDiv.innerHTML = '';

            try {
                const response = await fetch('/api/run', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: queryInput.value })
                });

                const data = await response.json();

                if (response.ok) {
                    contentDiv.innerHTML = marked.parse(data.output);
                    contentDiv.style.display = 'block';
                } else {
                    placeholder.innerText = `Error: ${data.detail || 'An unknown error occurred.'}`;
                    placeholder.style.display = 'block';
                    placeholder.style.color = '#cf6679';
                }
            } catch (err) {
                placeholder.innerText = `Network Error: ${err.message}`;
                placeholder.style.display = 'block';
                placeholder.style.color = '#cf6679';
            } finally {
                runBtn.disabled = false;
                spinner.style.display = 'none';
                btnText.innerText = 'Run Briefing';
            }
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    return HTMLResponse(content=HTML_TEMPLATE)


@app.post("/api/run")
async def run_agent(payload: RunPayload):
    try:
        # Create session asynchronously to avoid deprecation warnings
        session = await session_service.create_session(
            user_id="frontend_user", app_name="security-briefing-agent-frontend"
        )

        query_text = payload.query
        if query_text.strip() == "Generate my daily security briefing":
            from app.config import CVE_KEYWORDS, NEWS_TOPICS

            query_text = (
                f"Please construct today's daily security briefing. Use the registered tools to:\n"
                f"1. Query NVD API for recent CVEs related to these keywords: {', '.join(CVE_KEYWORDS)}.\n"
                f"2. Search the web for today's security news for these topics: {', '.join(NEWS_TOPICS)}.\n"
                f"3. Filter and structure the briefing for penetration testing relevance as specified in your instructions."
            )

        message = types.Content(
            role="user", parts=[types.Part.from_text(text=query_text)]
        )

        briefing_output = ""
        accumulated_text = []

        # Run agent asynchronously
        async for event in runner.run_async(
            new_message=message,
            user_id="frontend_user",
            session_id=session.id,
        ):
            if event.is_final_response():
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    briefing_output = event.content.parts[0].text
            elif event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        accumulated_text.append(part.text)

        if not briefing_output:
            briefing_output = "".join(accumulated_text)

        return {"output": briefing_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
