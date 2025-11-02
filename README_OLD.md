# MannKiBaat — AI Mental Health Screener

One-line description
--------------------

MannKiBaat is a small, privacy-minded Streamlit demo that performs a fast, non-clinical screening of short free-text inputs for potential mental health risk using a (user-supplied) fine-tuned DistilBERT model.

Why this repo exists
---------------------

- Provide a simple, deployable demo of an NLP-based mental health screener for research, prototyping, or community projects.
- Prioritize safety and consent: clear warnings, helpline prominence, and a conservative fallback when model weights are not present (so the demo remains usable for workshops/demos).

Repository structure
--------------------

```
mannkibaat/
├── app.py                # Streamlit app entrypoint and UI
├── model/
│   ├── fine_tuned_model/ # Place your DistilBERT model weights and tokenizer here
│   └── inference.py      # Model loading, prediction, and fallback heuristic
├── preprocessing.py      # Text cleaning and tokenization helpers
├── utils.py              # Score→risk mapping and helpline text
├── requirements.txt      # Top-level Python dependencies (pin before production)
└── README.md             # This file
```

Key features
------------

- Simple Streamlit UI with example prompts and consent checkbox.
- Lazy model loading: app will use a conservative heuristic if the fine-tuned model is missing.
- Clear privacy and safety messaging; helpline/resource suggestions for each risk level.

Important safety note (READ BEFORE USING)
---------------------------------------

This tool is a non-clinical screener only. It does NOT provide a diagnosis. If you or someone is in immediate danger, call local emergency services or the helpline shown for High risk. The app is intended for prototyping and educational use only.

Privacy
-------

- The demo processes text locally in memory — nothing is sent externally by the code in this repo.
- Do NOT upload or commit sensitive personal data. If you use remote deployment, ensure secure handling of user data and appropriate retention policies.

Quick start (development)
-------------------------

On macOS / Linux (zsh):

```bash
cd /Users/zam/Downloads/mannkibaat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Notes on dependencies and pinning
--------------------------------

- `requirements.txt` is intentionally minimal. For reproducible deployments pin versions (e.g., `transformers==4.##.#`, `torch==1.##.#`).
- If you plan to keep model weights in the repo, use Git LFS or external storage — do not commit large binary model files directly.

Adding your fine-tuned model
----------------------------

1. Place model files under `model/fine_tuned_model/`. Typical files: `pytorch_model.bin` (or `pytorch_model.bin` inside a folder saved by `from_pretrained`), `config.json`, and tokenizer files if you saved them.
2. By default the app loads the model directory via `model/inference.py`.
3. If you've saved the tokenizer during fine-tuning, modify `_get_tokenizer()` in `model/inference.py` to load the tokenizer from `model/fine_tuned_model` instead of the base `distilbert-base-uncased` tokenizer.

If the model is missing
----------------------

The app includes a conservative heuristic fallback (`fallback_predict`) that detects high-risk phrases and returns a conservative score. This keeps the demo usable for workshops or when weights aren't available. For production, prefer deploying with a validated model and remove or disable the fallback if desired.

Usage & UX notes
-----------------

- The app asks users to confirm they understand this is not clinical advice before analysis.
- Example prompts are provided to help users craft inputs.
- Outputs include a risk level (Low / Medium / High), a confidence score in [0,1], and recommended resources.

Deployment and production considerations
--------------------------------------

- Host where Python+Streamlit is supported (Streamlit Cloud, Heroku, Docker, VPS). For higher scale, convert inference to a lightweight API (FastAPI) and serve model separately (dedicated GPU or CPU instance).
- Secure secrets and credentials (do not store in the repo). Use environment variables or secret managers.
- Add monitoring, rate-limiting, and logging that obfuscates user input to protect privacy.

Testing and checks
------------------

- Consider adding unit tests for `preprocessing.py` and `utils.py`. Example test cases: tokenization correctness, mapping thresholds, and fallback phrase detection.
- Before production deploy, pin dependency versions and run static checks (flake8/black, mypy) and a small integration run against a held-out dataset.

Roadmap / TODO
--------------

- [ ] Add pytest-based unit tests for preprocessing and utils (small test harness).
- [ ] Provide an optional admin toggle to force model-only prediction (no fallback).
- [ ] Add CI that runs linting and tests on PRs.
- [ ] Add a small script to download model weights from secure storage during deploy.

Inspiration and credits
-----------------------

This README and the app UI were updated based on the user-provided PDF (attached) which emphasized clear consent, helpline prominence, example inputs, and safe fallback behaviors. Specific changes inspired by the PDF include:

- Consent/notice text and privacy note in the UI.
- Example input buttons to guide user responses.
- Emphasis on helplines and safety-first messaging in `utils.py` and the app flow.

Contributing
------------

Contributions are welcome. Please open issues for feature requests or security/privacy concerns. If you add model weights automation, ensure secrets are not committed and follow data protection guidelines.

License
-------

This repo is provided for educational/demo purposes. Add a license file appropriate to your project (e.g., MIT) before publishing publicly.

Contact / help
---------------

If you want me to extract literal resource lists or particular sections from the attached PDF into the app or README, tell me which sections and I will add them verbatim (making sure you have permission to republish that content).

---
Last updated: 2025-10-31

Inspired content
----------------

This repo and the app UI were updated using the attached PDF as inspiration (user-supplied). Changes include:

- Clearer privacy and consent messaging in the Streamlit UI.
- Example responses to help users understand what to enter.
- A safe, conservative heuristic fallback so the app stays usable if your fine-tuned model isn't present — useful for demos and development.
- Slightly richer helpline/resource wording in `utils.py`.

If you'd like me to extract specific sections or text from the PDF and place them directly into the app (e.g., a full resource list), tell me which parts and I'll add them.
