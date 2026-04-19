# Cross-Team Requirement Form Templates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 8 polished Word templates, in Chinese and English, for the Water treatment, Drainage, Application, and Derection groups to collect both feature requests and technical coordination details.

**Architecture:** Use one Python `python-docx` generator script to produce all 8 `.docx` files from one shared schema plus per-group prompt metadata. Keep document generation logic in one place, keep group-specific wording in structured data, and validate the outputs by reading the generated files back and rendering them through LibreOffice for layout review.

**Tech Stack:** Python 3, `python-docx`, LibreOffice `soffice`, Poppler `pdftoppm`, Markdown spec files, Git

---

## File Structure

### Files to create

- `tmp/docs/generate_requirement_form_templates.py`
  - Single source of truth for the bilingual content model and `.docx` generation logic.
- `tmp/docs/validate_requirement_form_templates.py`
  - Lightweight validation script that checks generated filenames, core section headings, and group-specific hints.
- `output/doc/水处理组需求采集表.docx`
- `output/doc/排水组需求采集表.docx`
- `output/doc/应用组需求采集表.docx`
- `output/doc/Derection组需求采集表.docx`
- `output/doc/Water_Treatment_Group_Requirement_Form.docx`
- `output/doc/Drainage_Group_Requirement_Form.docx`
- `output/doc/Application_Group_Requirement_Form.docx`
- `output/doc/Derection_Group_Requirement_Form.docx`

### Files to modify

- `docs/superpowers/specs/2026-03-27-cross-team-requirement-form-design.md`
  - No content changes expected. Use as the authoritative source while implementing the templates.

### Temporary render outputs

- `tmp/docs/rendered_requirement_forms/`
  - PDF and PNG render checks for layout review. Keep outside `output/doc/`.

---

### Task 1: Define the shared bilingual document schema

**Files:**
- Create: `tmp/docs/generate_requirement_form_templates.py`
- Create: `tmp/docs/validate_requirement_form_templates.py`

- [ ] **Step 1: Write the content schema into the generator script**

Create `tmp/docs/generate_requirement_form_templates.py` with the shared group metadata and document structure below:

```python
from pathlib import Path


OUTPUT_DIR = Path("/Users/tanxuebin/Downloads/up-clean/output/doc")


GROUPS = [
    {
        "key": "water_treatment",
        "zh_filename": "水处理组需求采集表.docx",
        "en_filename": "Water_Treatment_Group_Requirement_Form.docx",
        "zh_title": "水处理组需求采集表",
        "en_title": "Water Treatment Group Requirement Collection Form",
        "zh_hints": [
            "请重点说明你们关注的水质指标、处理阶段、阈值告警和历史趋势需求。",
            "请写明你们组可以提供哪些检测数据、设备数据或文档资料。",
            "如果希望系统支持前后处理结果对比，请说明对比维度和展示方式。",
        ],
        "en_hints": [
            "Please focus on water quality indicators, treatment stages, threshold alerts, and trend-view needs.",
            "Please specify what monitoring data, device data, or documents your group can provide.",
            "If you want before-and-after treatment comparison, describe the comparison dimensions and preferred presentation format.",
        ],
    },
    {
        "key": "drainage",
        "zh_filename": "排水组需求采集表.docx",
        "en_filename": "Drainage_Group_Requirement_Form.docx",
        "zh_title": "排水组需求采集表",
        "en_title": "Drainage Group Requirement Collection Form",
        "zh_hints": [
            "请重点说明需要监测的排水点、异常工况和需要追踪的记录类型。",
            "请写明是否需要实时状态、周期记录、路径展示或区域影响信息。",
            "请说明你们组能够提供哪些现场数据、设备信号或流程资料。",
        ],
        "en_hints": [
            "Please focus on drainage points to monitor, abnormal conditions, and the record types that matter most.",
            "Please state whether you need real-time status, periodic records, route visibility, or area impact information.",
            "Please describe the field data, device signals, or process materials your group can provide.",
        ],
    },
    {
        "key": "application",
        "zh_filename": "应用组需求采集表.docx",
        "en_filename": "Application_Group_Requirement_Form.docx",
        "zh_title": "应用组需求采集表",
        "en_title": "Application Group Requirement Collection Form",
        "zh_hints": [
            "请重点说明目标用户是谁、他们最常做什么操作、最先需要看到什么信息。",
            "请说明哪些页面、流程或交互体验最值得优先完善。",
            "请尽量写出当前系统在使用体验上的问题和你们的改进建议。",
        ],
        "en_hints": [
            "Please focus on target users, their key actions, and the information they should see first.",
            "Please explain which pages, flows, or interaction problems should be improved first.",
            "Please describe the most important usability issues in the current system and your suggestions.",
        ],
    },
    {
        "key": "derection",
        "zh_filename": "Derection组需求采集表.docx",
        "en_filename": "Derection_Group_Requirement_Form.docx",
        "zh_title": "Derection组需求采集表",
        "en_title": "Derection Group Requirement Collection Form",
        "zh_hints": [
            "请重点说明决策、统筹、汇报或管理时最需要看到哪些信息。",
            "请说明是否需要总览面板、阶段汇总、统计报表或会议展示材料。",
            "请尽量明确你们最关注的关键指标、更新频率和结果形式。",
        ],
        "en_hints": [
            "Please focus on the information most needed for decision-making, coordination, reporting, or management.",
            "Please explain whether you need overview dashboards, stage summaries, statistics reports, or presentation materials.",
            "Please clarify the key indicators, update frequency, and preferred output format.",
        ],
    },
]


PART_A_FIELDS = [
    ("Group name", "小组名称"),
    ("Main responsibility", "主要负责内容"),
    ("Current progress or existing outputs", "当前已有成果"),
    ("What support is needed from our system", "希望我们的系统提供哪些支持"),
    ("What your group can provide", "你们组可以提供什么"),
    ("Related devices, data, documents, or interfaces", "相关设备、数据、文档或接口"),
    ("Main contact person", "主要联系人"),
    ("Preferred collaboration method", "希望的对接方式"),
]


PART_B_HEADERS = [
    ("Requirement title", "需求名称"),
    ("Problem to solve", "想解决的问题"),
    ("Expected function", "希望我们实现的功能"),
    ("Input needed", "需要的输入"),
    ("Who provides the input", "输入由谁提供"),
    ("Expected output", "期望输出"),
    ("Target users", "使用对象"),
    ("Priority", "优先级"),
    ("Preferred timeline", "希望完成时间"),
    ("Dependencies or risks", "依赖项或风险"),
    ("Remarks", "备注"),
]
```

- [ ] **Step 2: Add a validation helper script for the content model**

Create `tmp/docs/validate_requirement_form_templates.py`:

```python
from pathlib import Path
import runpy


GENERATOR_PATH = Path("/Users/tanxuebin/Downloads/up-clean/tmp/docs/generate_requirement_form_templates.py")


def main():
    namespace = runpy.run_path(str(GENERATOR_PATH))
    groups = namespace["GROUPS"]
    part_a_fields = namespace["PART_A_FIELDS"]
    part_b_headers = namespace["PART_B_HEADERS"]

    assert len(groups) == 4, f"Expected 4 groups, got {len(groups)}"
    assert len(part_a_fields) == 8, f"Expected 8 Part A fields, got {len(part_a_fields)}"
    assert len(part_b_headers) == 11, f"Expected 11 Part B headers, got {len(part_b_headers)}"

    required_keys = {
        "key",
        "zh_filename",
        "en_filename",
        "zh_title",
        "en_title",
        "zh_hints",
        "en_hints",
    }

    for group in groups:
        missing = required_keys - set(group)
        assert not missing, f"Missing keys for {group.get('key')}: {sorted(missing)}"
        assert len(group["zh_hints"]) >= 3, f"Chinese hints too short for {group['key']}"
        assert len(group["en_hints"]) >= 3, f"English hints too short for {group['key']}"

    print("PASS: content schema is complete")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run the schema validation**

Run:

```bash
python3 /Users/tanxuebin/Downloads/up-clean/tmp/docs/validate_requirement_form_templates.py
```

Expected:

```text
PASS: content schema is complete
```

- [ ] **Step 4: Commit the schema groundwork**

```bash
git add /Users/tanxuebin/Downloads/up-clean/tmp/docs/generate_requirement_form_templates.py /Users/tanxuebin/Downloads/up-clean/tmp/docs/validate_requirement_form_templates.py
git commit -m "chore: add schema for requirement form templates"
```

---

### Task 2: Implement the shared Word template layout

**Files:**
- Modify: `tmp/docs/generate_requirement_form_templates.py`
- Test: `tmp/docs/validate_requirement_form_templates.py`

- [ ] **Step 1: Add reusable `python-docx` layout helpers**

Extend `tmp/docs/generate_requirement_form_templates.py` with the shared layout helpers below:

```python
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def apply_page_setup(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    normal.font.size = Pt(10)


def add_title(doc, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = RGBColor(31, 78, 121)


def add_intro(doc, purpose, instructions):
    p = doc.add_paragraph()
    p.add_run("Purpose / 填写目的: ").bold = True
    p.add_run(purpose)

    p = doc.add_paragraph()
    p.add_run("Instructions / 填写说明: ").bold = True
    p.add_run(instructions)


def add_part_a_table(doc):
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    headers = table.rows[0].cells
    headers[0].text = "Field / 字段"
    headers[1].text = "Response / 填写内容"
    set_cell_shading(headers[0], "D9EAF7")
    set_cell_shading(headers[1], "D9EAF7")

    for en_label, zh_label in PART_A_FIELDS:
        row = table.add_row().cells
        row[0].text = f"{en_label} / {zh_label}"
        row[1].text = ""


def add_part_b_table(doc):
    table = doc.add_table(rows=4, cols=len(PART_B_HEADERS))
    table.style = "Table Grid"
    for index, (en_label, zh_label) in enumerate(PART_B_HEADERS):
        table.rows[0].cells[index].text = f"{en_label}\\n{zh_label}"
        set_cell_shading(table.rows[0].cells[index], "D9EAF7")
    for row_index in range(1, 4):
        for col_index in range(len(PART_B_HEADERS)):
            table.rows[row_index].cells[col_index].text = ""


def add_hint_list(doc, hints, heading):
    doc.add_paragraph(heading)
    for hint in hints:
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(hint)
```

- [ ] **Step 2: Add the per-document assembly function**

Add the assembly function to `tmp/docs/generate_requirement_form_templates.py`:

```python
def build_document(language, group):
    doc = Document()
    apply_page_setup(doc)

    if language == "zh":
        title = group["zh_title"]
        purpose = "本表用于收集贵组对系统功能、数据对接和协作方式的需求，以便后续统一复核与开发安排。"
        instructions = "每组填写一份；Part A 填写一次；Part B 可填写多条需求；若细节暂未确定，可先填写初步想法，后续会议再统一确认。"
        hint_heading = "Group-specific hints / 本组填写提示"
        follow_up = "Follow-up / 后续说明: 如有尚不明确的事项，可在后续统一复核会议中继续讨论并确认。"
    else:
        title = group["en_title"]
        purpose = "This form is used to collect your group's feature requests, technical coordination needs, and collaboration expectations for later review and planning."
        instructions = "Each group should complete one form. Fill Part A once. Use Part B for multiple requirement items. Rough answers are acceptable if details are not final yet."
        hint_heading = "Group-specific hints / 本组填写提示"
        follow_up = "Follow-up / 后续说明: If anything is still unclear, it can be discussed and confirmed in the later review meeting."

    add_title(doc, title)
    add_intro(doc, purpose, instructions)

    doc.add_heading("Part A. Group Overview / 小组概况", level=1)
    add_part_a_table(doc)

    doc.add_paragraph()
    doc.add_heading("Part B. Requirement Items / 需求明细", level=1)
    add_part_b_table(doc)

    doc.add_paragraph()
    add_hint_list(doc, group["zh_hints"] if language == "zh" else group["en_hints"], hint_heading)

    doc.add_paragraph()
    doc.add_paragraph(follow_up)
    return doc
```

- [ ] **Step 3: Add the output loop**

Add the save loop to `tmp/docs/generate_requirement_form_templates.py`:

```python
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for group in GROUPS:
        zh_doc = build_document("zh", group)
        zh_doc.save(OUTPUT_DIR / group["zh_filename"])

        en_doc = build_document("en", group)
        en_doc.save(OUTPUT_DIR / group["en_filename"])

    print("PASS: generated 8 requirement form templates")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run generation and validation**

Run:

```bash
python3 /Users/tanxuebin/Downloads/up-clean/tmp/docs/generate_requirement_form_templates.py
python3 /Users/tanxuebin/Downloads/up-clean/tmp/docs/validate_requirement_form_templates.py
```

Expected:

```text
PASS: generated 8 requirement form templates
PASS: content schema is complete
```

- [ ] **Step 5: Commit the shared layout**

```bash
git add /Users/tanxuebin/Downloads/up-clean/tmp/docs/generate_requirement_form_templates.py /Users/tanxuebin/Downloads/up-clean/output/doc
git commit -m "feat: generate bilingual requirement form templates"
```

---

### Task 3: Validate document contents and filenames

**Files:**
- Modify: `tmp/docs/validate_requirement_form_templates.py`
- Test: `output/doc/*.docx`

- [ ] **Step 1: Extend validation to inspect generated `.docx` content**

Replace the body of `main()` in `tmp/docs/validate_requirement_form_templates.py` with:

```python
from docx import Document


EXPECTED_FILES = [
    "水处理组需求采集表.docx",
    "排水组需求采集表.docx",
    "应用组需求采集表.docx",
    "Derection组需求采集表.docx",
    "Water_Treatment_Group_Requirement_Form.docx",
    "Drainage_Group_Requirement_Form.docx",
    "Application_Group_Requirement_Form.docx",
    "Derection_Group_Requirement_Form.docx",
]


def document_text(path):
    doc = Document(str(path))
    return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())


def main():
    namespace = runpy.run_path(str(GENERATOR_PATH))
    output_dir = namespace["OUTPUT_DIR"]
    groups = namespace["GROUPS"]

    for filename in EXPECTED_FILES:
        path = output_dir / filename
        assert path.exists(), f"Missing generated file: {filename}"

    chinese_checks = {
        "水处理组需求采集表.docx": ["水处理组需求采集表", "Part A. Group Overview / 小组概况", "本组填写提示"],
        "排水组需求采集表.docx": ["排水组需求采集表", "Part B. Requirement Items / 需求明细", "排水点"],
        "应用组需求采集表.docx": ["应用组需求采集表", "目标用户", "交互体验"],
        "Derection组需求采集表.docx": ["Derection组需求采集表", "关键指标", "汇总"],
    }

    english_checks = {
        "Water_Treatment_Group_Requirement_Form.docx": ["Water Treatment Group Requirement Collection Form", "Group-specific hints", "water quality indicators"],
        "Drainage_Group_Requirement_Form.docx": ["Drainage Group Requirement Collection Form", "Group-specific hints", "drainage points"],
        "Application_Group_Requirement_Form.docx": ["Application Group Requirement Collection Form", "target users", "usability issues"],
        "Derection_Group_Requirement_Form.docx": ["Derection Group Requirement Collection Form", "decision-making", "statistics reports"],
    }

    for filename, fragments in {**chinese_checks, **english_checks}.items():
        text = document_text(output_dir / filename)
        for fragment in fragments:
            assert fragment in text, f"{fragment!r} not found in {filename}"

    print("PASS: generated documents exist and contain expected headings")
```

- [ ] **Step 2: Run the content validation**

Run:

```bash
python3 /Users/tanxuebin/Downloads/up-clean/tmp/docs/validate_requirement_form_templates.py
```

Expected:

```text
PASS: generated documents exist and contain expected headings
```

- [ ] **Step 3: Manually inspect the output directory**

Run:

```bash
ls -1 /Users/tanxuebin/Downloads/up-clean/output/doc | rg "Requirement_Form|需求采集表"
```

Expected:

```text
Application_Group_Requirement_Form.docx
Derection_Group_Requirement_Form.docx
Drainage_Group_Requirement_Form.docx
Water_Treatment_Group_Requirement_Form.docx
Derection组需求采集表.docx
排水组需求采集表.docx
应用组需求采集表.docx
水处理组需求采集表.docx
```

- [ ] **Step 4: Commit the validation improvements**

```bash
git add /Users/tanxuebin/Downloads/up-clean/tmp/docs/validate_requirement_form_templates.py /Users/tanxuebin/Downloads/up-clean/output/doc
git commit -m "test: validate generated requirement form templates"
```

---

### Task 4: Render and review layout quality

**Files:**
- Modify: `tmp/docs/generate_requirement_form_templates.py`
- Test: `tmp/docs/rendered_requirement_forms/`

- [ ] **Step 1: Render all 8 documents through LibreOffice**

Run:

```bash
OUT=/Users/tanxuebin/Downloads/up-clean/tmp/docs/rendered_requirement_forms
rm -rf "$OUT"
mkdir -p "$OUT"
for file in /Users/tanxuebin/Downloads/up-clean/output/doc/*Requirement_Form.docx /Users/tanxuebin/Downloads/up-clean/output/doc/*需求采集表.docx; do
  soffice -env:UserInstallation=file:///tmp/lo_profile_requirement_forms --headless --convert-to pdf --outdir "$OUT" "$file"
done
ls -1 "$OUT"
```

Expected:

```text
... 8 PDF files ...
```

- [ ] **Step 2: Convert the rendered PDFs into PNG previews**

Run:

```bash
for pdf in /Users/tanxuebin/Downloads/up-clean/tmp/docs/rendered_requirement_forms/*.pdf; do
  base="${pdf%.pdf}"
  pdftoppm -png "$pdf" "$base"
done
ls -1 /Users/tanxuebin/Downloads/up-clean/tmp/docs/rendered_requirement_forms | rg "\\.png$"
```

Expected:

```text
... PNG previews for each rendered PDF ...
```

- [ ] **Step 3: If layout issues appear, tighten the document layout**

If page breaks or table overflow are visible, update `tmp/docs/generate_requirement_form_templates.py` with these adjustments:

```python
def apply_page_setup(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    normal.font.size = Pt(9.5)
```

Then rerun:

```bash
python3 /Users/tanxuebin/Downloads/up-clean/tmp/docs/generate_requirement_form_templates.py
python3 /Users/tanxuebin/Downloads/up-clean/tmp/docs/validate_requirement_form_templates.py
```

Expected:

```text
PASS: generated 8 requirement form templates
PASS: generated documents exist and contain expected headings
```

- [ ] **Step 4: Commit the layout-polish pass**

```bash
git add /Users/tanxuebin/Downloads/up-clean/tmp/docs/generate_requirement_form_templates.py /Users/tanxuebin/Downloads/up-clean/output/doc
git commit -m "style: polish requirement form template layout"
```

---

### Task 5: Final packaging and handoff check

**Files:**
- Test: `output/doc/*.docx`

- [ ] **Step 1: Verify the final filenames and sizes**

Run:

```bash
ls -lh /Users/tanxuebin/Downloads/up-clean/output/doc/*Requirement_Form.docx /Users/tanxuebin/Downloads/up-clean/output/doc/*需求采集表.docx
```

Expected:

```text
... 8 .docx files with non-zero size ...
```

- [ ] **Step 2: Verify one Chinese and one English file can be opened by `python-docx`**

Run:

```bash
python3 - <<'PY'
from docx import Document
files = [
    "/Users/tanxuebin/Downloads/up-clean/output/doc/水处理组需求采集表.docx",
    "/Users/tanxuebin/Downloads/up-clean/output/doc/Water_Treatment_Group_Requirement_Form.docx",
]
for path in files:
    doc = Document(path)
    print(path, len(doc.paragraphs))
PY
```

Expected:

```text
/Users/tanxuebin/Downloads/up-clean/output/doc/水处理组需求采集表.docx ...
/Users/tanxuebin/Downloads/up-clean/output/doc/Water_Treatment_Group_Requirement_Form.docx ...
```

- [ ] **Step 3: Commit the final generated package**

```bash
git add /Users/tanxuebin/Downloads/up-clean/output/doc
git commit -m "docs: add final cross-team requirement form templates"
```

---

## Self-Review

### Spec coverage

- 4 target groups covered: yes, via `GROUPS`
- 8 Word outputs covered: yes, via save loop and final checks
- Shared structure plus group-specific prompts covered: yes
- Word output requirement covered: yes
- Chinese and English parity covered: yes, through mirrored generation
- Cross-team coordination focus covered: yes, in Part A, Part B, and hint prompts

### Placeholder scan

- No `TBD`, `TODO`, or deferred placeholders in the tasks
- Exact file paths provided
- Exact commands provided
- Concrete content blocks provided for the generator and validator

### Type consistency

- `GROUPS`, `PART_A_FIELDS`, `PART_B_HEADERS`, `OUTPUT_DIR`, `build_document()`, and validator references are consistent across tasks

