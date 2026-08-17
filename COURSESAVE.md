# Coursera reading backup helper

This repository includes a helper script for saving Coursera reading pages that you can already access with your own account. It does not bypass Coursera login, payment, DRM, or access controls.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## Download authorized reading PDFs

Run this before your course access expires. The first run should use `--login`, which opens a browser profile where you sign in to Coursera manually.

```bash
python tools/download_coursera_readings.py \
  "https://www.coursera.org/learn/foundations-user-experience-design/supplement/G2Dwt/begin-the-google-ux-design-certificate" \
  --login \
  --out coursera-google-ux-readings
```

The script creates:

- `pdf-en/`: original English PDFs printed from each reading page.
- `markdown-en/`: extracted English text.
- `markdown-bilingual/`: English plus a Chinese section placeholder, or translations if enabled.
- `manifest.txt`: crawled reading URLs.

## Add Chinese translations

Set an OpenAI API key and rerun with `--translate`:

```bash
export OPENAI_API_KEY="sk-..."
python tools/download_coursera_readings.py \
  "https://www.coursera.org/learn/foundations-user-experience-design/supplement/G2Dwt/begin-the-google-ux-design-certificate" \
  --out coursera-google-ux-readings \
  --translate
```

You may set `OPENAI_MODEL` to choose a different translation model. The default is `gpt-4.1-mini`.

## Notes

- Use the exported files only as allowed by Coursera and the course provider's terms.
- If Coursera changes its page layout, inspect `manifest.txt` and rerun with a known reading URL.
- If the course has readings that are not linked from the start page, run the script again with another reading URL from that module.
