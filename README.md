# Daily Security Briefing Agent

An agent generated with `agents-cli` version `1.0.0` that gathers today's security news and CVEs to compile a highly structured penetration testing daily briefing.

## Features & Capabilities

- **Recent CVE Tracking**: Queries the NVD API for recent CVEs related to target pentesting topics (e.g., Android, iOS, JWT, OAuth, SSRF).
- **Security News Aggregation**: Searches the web using DuckDuckGo Search for daily updates on mobile security, web/API security, and AI/LLM threats.
- **PT-Focused Filtering**: Automatically filters results to prioritize critical & high-severity vulnerabilities (CVSS >= 7.0) and generates actionable takeaways for penetration testing teams.
- **Clickable Grounding Links**: Embeds direct reference links to source articles and NVD advisory pages.

---

## Project Structure

```
security-briefing-agent/
├── app/                      # Core agent code
│   ├── agent.py              # Main agent configuration (ADK App)
│   ├── config.py             # Target CVE keywords and news topics
│   ├── tools.py              # Custom tools (search_security_news, fetch_recent_cves)
│   ├── fast_api_app.py       # FastAPI Backend server
│   └── app_utils/            # App utilities and helpers
├── tests/                    # Unit, integration, and evaluation tests
├── GEMINI.md                 # AI-assisted development guide
└── pyproject.toml            # Project configuration and dependencies
```

> 💡 **Tip:** Use [Antigravity CLI](https://antigravity.google/) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

---

## Requirements

Before you begin, ensure you have:
- **uv**: Fast Python package manager (used for dependency management) - [Install](https://docs.astral.sh/uv/getting-started/installation/)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`
- **Google Cloud SDK**: (Optional) For GCP services / Vertex AI - [Install](https://cloud.google.com/sdk/docs/install)

---

## Configuration

Duplicate the `.env.example` file to `.env` and configure your API keys:
1. **Google AI Studio (Gemini API)**: Add your `GEMINI_API_KEY` (ensure Vertex AI variables are commented out).
2. **NVD API Key**: (Optional but recommended) Add your `NVD_API_KEY` to prevent rate-limiting during NVD CVE fetches.

---

## Quick Start

1. Install `agents-cli` and setup skills:
   ```bash
   uvx google-agents-cli setup
   ```

2. Install dependencies:
   ```bash
   agents-cli install
   ```

3. **Run the Daily Briefing Aggregator**:
   To generate today's daily briefing and write it directly to `daily_briefing.md`, run:
   ```bash
   uv run python app/main.py
   ```

4. **Launch Local Development Playground**:
   To interact with the agent in a web interface:
   ```bash
   agents-cli playground
   ```
   Access the UI at: [http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)

---

## Commands

| Command | Description |
| :--- | :--- |
| `agents-cli install` | Install dependencies using `uv` |
| `uv run python app/main.py` | Run the aggregator script to compile the daily briefing |
| `agents-cli playground` | Launch local development environment UI |
| `agents-cli lint` | Run code quality checks (ruff, codespell, ty) |
| `agents-cli eval` | Evaluate agent behavior behavior (see `agents-cli eval --help`) |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests |

---

## 🛠️ Project Management

| Command | What It Does |
| :--- | :--- |
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.

## A2A Inspector

This agent supports the [A2A Protocol](https://a2a-protocol.org/). Use the [A2A Inspector](https://github.com/a2aproject/a2a-inspector) to test interoperability.
See the [A2A Inspector docs](https://github.com/a2aproject/a2a-inspector) for details.
