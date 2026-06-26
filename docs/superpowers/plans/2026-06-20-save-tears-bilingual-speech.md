# Save Tears Bilingual Recruitment Speech Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an editable bilingual rehearsal script whose English section follows the existing seven-slide Save Tears recruitment deck and fits a five-minute on-site pitch.

**Architecture:** Keep one Markdown source as the content authority, verify its structure and factual claims with an automated script, then generate and render a polished DOCX from that source. English is the spoken layer; Chinese is a faithful rehearsal aid placed directly after each slide section.

**Tech Stack:** Markdown, Python 3, `python-docx`, bundled DOCX renderer, plain-text extraction for verification.

---

### Task 1: Define the Script Contract

**Files:**
- Create: `tmp/docs/verify_recruitment_speech.py`
- Test: `docs/speeches/2026-06-20-save-tears-bilingual-recruitment-speech.md`

- [ ] **Step 1: Write the failing verification script**

The verifier must require seven `## Slide N` sections, one `### English` and one `### 中文对照` subsection per slide, an English word count between 500 and 540, and the exact facts `810`, `131,220`, `0.7498`, `2–4`, `ThingCloud`, `RAG`, and `real devices are not connected yet`.

```python
from pathlib import Path
import re

source = Path("docs/speeches/2026-06-20-save-tears-bilingual-recruitment-speech.md")
text = source.read_text(encoding="utf-8")
assert len(re.findall(r"^## Slide [1-7]", text, re.M)) == 7
assert len(re.findall(r"^### English$", text, re.M)) == 7
assert len(re.findall(r"^### 中文对照$", text, re.M)) == 7
english = "\n".join(re.findall(r"### English\n(.*?)(?=\n### 中文对照)", text, re.S))
word_count = len(re.findall(r"\b[\w’'-]+\b", english))
assert 500 <= word_count <= 540, word_count
for fact in ["810", "131,220", "0.7498", "2–4", "ThingCloud", "RAG", "real devices are not connected yet"]:
    assert fact in english, fact
assert "weather and temperature are not current model inputs" in english
assert "The LLM explains the plan" in english
print(f"PASS: 7 slides, {word_count} spoken English words")
```

- [ ] **Step 2: Run the verifier and confirm the RED state**

Run: `python3 tmp/docs/verify_recruitment_speech.py`

Expected: failure because `docs/speeches/2026-06-20-save-tears-bilingual-recruitment-speech.md` does not exist.

### Task 2: Write the Seven-Slide Bilingual Script

**Files:**
- Create: `docs/speeches/2026-06-20-save-tears-bilingual-recruitment-speech.md`
- Test: `tmp/docs/verify_recruitment_speech.py`

- [ ] **Step 1: Write the source script**

Use this exact structure for every slide:

```markdown
## Slide 1 — We Built It. Now We Need You.

### English

Good afternoon. We started Save Tears during the winter camp, and today it is already a working web product.

### 中文对照

大家下午好。我们在冬令营期间启动了 Save Tears，如今它已经是一个可以运行的网页产品。
```

Keep the seven slide titles identical to the PPT. Target 520–540 spoken English words in total. Use short sentences, natural transitions, and only the factual claims defined in `docs/superpowers/specs/2026-06-20-save-tears-bilingual-speech-design.md`.

- [ ] **Step 2: Run the verifier and confirm the GREEN state**

Run: `python3 tmp/docs/verify_recruitment_speech.py`

Expected: `PASS: 7 slides, <500–540> spoken English words`.

- [ ] **Step 3: Review speaking pace**

Compute the approximate duration at 115 words per minute and confirm that the spoken English plus approximately 20 seconds of transitions stays near five minutes.

Run: `python3 -c 'words=530; print(round(words/115*60+20))'`

Expected: approximately 297 seconds; reduce wording if the measured result exceeds 300 seconds.

### Task 3: Generate the Editable Word Deliverable

**Files:**
- Create: `tmp/docs/build_recruitment_speech.py`
- Create: `output/doc/save-tears-bilingual-recruitment-speech.docx`
- Render: `tmp/docs/rendered_recruitment_speech/`

- [ ] **Step 1: Build the DOCX generator**

Use `python-docx` to create a US Letter document with a title page, usage note, and one rehearsal page for each of the seven slides. Apply the `compact_reference_guide` preset with a named Save Tears Academic Minimal colour and font override, dark-blue English headings, muted-red Chinese headings, readable body text, and page numbers. Preserve `[Pause]`, `[Point to the chart]`, and `[Next slide]` as italic stage directions.

- [ ] **Step 2: Generate the DOCX**

Run: `python3 tmp/docs/build_recruitment_speech.py`

Expected: `output/doc/save-tears-bilingual-recruitment-speech.docx` exists and is non-empty.

- [ ] **Step 3: Render every page**

Run the bundled document renderer against the generated DOCX and save page PNGs under `tmp/docs/rendered_recruitment_speech/`.

Expected: every page renders without conversion errors.

- [ ] **Step 4: Inspect the rendered pages and fix layout defects**

Check title hierarchy, English/Chinese pairing, paragraph spacing, page breaks, widows/orphans, clipped text, and footer readability. Rebuild and rerender after any correction.

### Task 4: Final Verification and Handoff

**Files:**
- Verify: `docs/speeches/2026-06-20-save-tears-bilingual-recruitment-speech.md`
- Verify: `output/doc/save-tears-bilingual-recruitment-speech.docx`

- [ ] **Step 1: Run the full content verifier**

Run: `python3 tmp/docs/verify_recruitment_speech.py`

Expected: seven slides, all required facts present, and 500–540 spoken English words.

- [ ] **Step 2: Extract DOCX text and compare required facts**

Confirm that the DOCX contains all seven slide titles, both language labels for every slide, and all required numerical and technical claims.

- [ ] **Step 3: Deliver both editable formats**

Provide links to the Markdown source and the DOCX. State the measured English word count and approximate speaking time.
