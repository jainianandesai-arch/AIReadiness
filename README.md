# AI Transformation Readiness Intelligence

A Streamlit executive diagnostic that identifies the most likely failure point behind AI transformation before an organization scales the wrong thing.

## What changed in this clean version

- Compact 3-column diagnostic using dropdown responses instead of long radio-button blocks.
- No external consulting-firm names in the app or download buttons.
- Context and data-handling declaration added at the top of the app.
- No database, tracking, persistent storage, or caching layer is included.
- Executive PDF redesigned as a clean two-page report.
- GPT integration remains optional and guardrailed. If no API key is present, the app uses a rules-based fallback.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Optional GPT setup

Create a `.env` file in the same folder as `app.py`:

```text
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

The scoring and failure-pattern logic do not depend on GPT. GPT is used only to draft a concise executive narrative from the structured evidence pack.

## Data handling note

This prototype does not include a database, persistent storage, analytics tracking, or cached response data. Streamlit session state is used only to keep responses active while the app session is open. If GPT is enabled, the structured evidence pack is sent to the configured OpenAI model for report drafting.
