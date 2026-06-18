# Save Tears UK Core Team Recruitment Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a verified seven-slide, fully English, editable PowerPoint that recruits two to four UK Telecom Engineering and Software Engineering students into the Save Tears core team.

**Architecture:** Build the deck in `create` mode with `@oai/artifact-tool`. Keep all generated code, source ledgers, assets, renders, layouts, and QA files in the external presentation workspace; export only the final PPTX to the repository. Drive slide copy from a tested content module so completed work, integration readiness, and research directions cannot be accidentally overstated.

**Tech Stack:** Bundled Node.js, `@oai/artifact-tool`, Node `test`, in-app browser capture, native editable PowerPoint shapes/charts/images, presentation render/layout export.

---

## Execution Environment

Run this setup block before implementation tasks:

```bash
NODE=/Users/tanxuebin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node
SCRATCH_ROOT="$($NODE -p "require('node:os').tmpdir()")"
THREAD_ID="${CODEX_THREAD_ID:-manual-save-tears-uk-deck}"
WORKSPACE="$SCRATCH_ROOT/codex-presentations/$THREAD_ID/save-tears-uk-core-team-recruitment"
TMP_DIR="$WORKSPACE/tmp"
SLIDES_DIR="$TMP_DIR/slides"
PREVIEW_DIR="$TMP_DIR/preview"
LAYOUT_DIR="$TMP_DIR/layout/final"
ASSET_DIR="$TMP_DIR/assets"
QA_DIR="$TMP_DIR/qa"
FINAL_PPTX=/Users/tanxuebin/Downloads/up-clean/output/ppt/save-tears-uk-core-team-recruitment.pptx
SKILL_DIR=/Users/tanxuebin/.codex/plugins/cache/openai-primary-runtime/presentations/26.614.11602/skills/presentations
export NODE SCRATCH_ROOT THREAD_ID WORKSPACE TMP_DIR SLIDES_DIR PREVIEW_DIR LAYOUT_DIR ASSET_DIR QA_DIR FINAL_PPTX SKILL_DIR
```

Do not delete or rewrite the existing `output/ppt/灰水新生-竞选队长PPT-陶嘉成.pptx`; it is user-owned and outside this task.

## File Map

| Path | Responsibility |
| --- | --- |
| `$TMP_DIR/source-notes.txt` | Provenance ledger for every claim and asset. |
| `$TMP_DIR/slide-plan.txt` | Slide order, exact style tokens, proof object, timing, and source mapping. |
| `$TMP_DIR/deck-content.mjs` | Single source of truth for titles, timings, metrics, statuses, roles, and forbidden claims. |
| `$TMP_DIR/tests/content.test.mjs` | Prevents inaccurate claims or slide-count drift. |
| `$SLIDES_DIR/common.mjs` | Academic Minimal palette, typography, margins, footer, cards, and helper functions. |
| `$SLIDES_DIR/slide-01.mjs` through `$SLIDES_DIR/slide-07.mjs` | One focused module per slide. |
| `$TMP_DIR/build-deck.mjs` | Creates, renders, lays out, and exports the deck. |
| `$TMP_DIR/tests/build.test.mjs` | Verifies manifest, slide count, preview count, and non-empty PPTX. |
| `$ASSET_DIR/product-home.png` | Verified Save Tears product screenshot. |
| `$PREVIEW_DIR/slide-01.png` through `$PREVIEW_DIR/slide-07.png` | Full-slide visual QA renders. |
| `$PREVIEW_DIR/contact-sheet.webp` | Deck-level visual QA montage. |
| `$LAYOUT_DIR/slide-01.layout.json` through `$LAYOUT_DIR/slide-07.layout.json` | Layout inspection evidence. |
| `$QA_DIR/visual-qa.txt` | Completed QA checklist and issue ledger. |
| `output/ppt/save-tears-uk-core-team-recruitment.pptx` | Final user-facing deliverable. |

### Task 1: Establish The Evidence Ledger And Slide Plan

**Files:**
- Create: `$TMP_DIR/source-notes.txt`
- Create: `$TMP_DIR/slide-plan.txt`
- Reference: `docs/superpowers/specs/2026-06-18-save-tears-uk-team-recruitment-deck-design.md`
- Reference: `DEPLOYMENT.md`
- Reference: `README.md`
- Reference: `/Users/tanxuebin/Library/Containers/com.tencent.qq/Data/Downloads/人工智能课程设计，最终版 (1).docx`

- [ ] **Step 1: Create the external workspace directories**

Run:

```bash
mkdir -p "$SLIDES_DIR" "$PREVIEW_DIR" "$LAYOUT_DIR" "$ASSET_DIR" "$QA_DIR" "$TMP_DIR/tests"
```

Expected: all directories exist outside the Git repository.

- [ ] **Step 2: Write `source-notes.txt` with exact claim provenance**

Use `apply_patch` to create the file with these entries:

```text
Source notes — Save Tears UK Core Team Recruitment

1. User-provided project brief
   Supports: winter-camp origin, UK-student recruitment goal, three next challenges,
   target majors, target team size, and on-site selection.

2. Save Tears DEPLOYMENT.md
   Source path: /Users/tanxuebin/Downloads/up-clean/DEPLOYMENT.md
   Supports: https://savetear.cloud/, own domain/server, production frontend/backend,
   and recorded health-check endpoint.

3. Save Tears README.md and save_tears_backend/README.md
   Source paths: /Users/tanxuebin/Downloads/up-clean/README.md;
   /Users/tanxuebin/Downloads/up-clean/save_tears_backend/README.md
   Supports: ThingCloud-compatible ingestion endpoint, dual-source data concepts,
   backend responsibilities, and current rule-based plan fallback.

4. Artificial-intelligence course design report by Tao Jiacheng
   Source title: 基于多模型对比的家庭正常用水量预测研究
   Supports: 810 households, 131220 supervised samples, six-hour window,
   Random Forest MAE 3.0179, RMSE 5.0867, R2 0.7498, and model limitations.

5. Browser capture of https://savetear.cloud/
   Asset: assets/product-home.png
   Supports: product interface shown on slide 2.

Claim boundaries:
- Weather and temperature are future features, not current model inputs.
- Real ThingCloud devices are not connected yet.
- RAG, fine-tuning, and greywater-aware plan generation are research directions.
- The deck uses “small open-source LLMs” and does not name Gemma4-4B.
```

- [ ] **Step 3: Write `slide-plan.txt` with the approved design system**

Use this content:

```text
Mode: create
Slide size: 1280 x 720 (16:9)
Audience: UK Telecom Engineering and Software Engineering students
Length: 5 minutes
Slide count: 7

Palette:
- background #FFFFFF (about 70% visual weight)
- ink #172630
- university blue #2C6F88
- muted red #A23A35
- muted gold #C9A23B
- soft panel #F5F7F8
- line #D7DEE2
- muted text #5A6973

Fonts:
- headings: Aptos Display
- body: Aptos
- metrics: Georgia

Scale:
- cover title 56 px
- slide title 38 px
- kicker 13 px
- card heading 22 px
- body 18 px
- metric 54 px
- source/footer 10 px

Slides:
1. We Built It. Now We Need You. — live-domain proof
2. From Winter Camp to a Live Product — timeline plus product screenshot
3. Three Challenges We Cannot Solve Alone — three ownership cards
4. Our First AI Result — native R2 comparison chart and limitation note
5. Why Generic LLMs Are Not Enough — editable decision pipeline
6. Two Majors, One Working System — Telecom and Software role split
7. Join the Core Team — 2–4 members and on-site call to action
```

- [ ] **Step 4: Verify the ledgers contain no unsupported completion claims**

Run:

```bash
rg -n "RAG.*complete|fine-tun.*complete|real devices connected|weather.*current|Gemma4-4B" "$TMP_DIR/source-notes.txt" "$TMP_DIR/slide-plan.txt"
```

Expected: only the explicit negative claim boundary for `Gemma4-4B`; no positive completion claim.

### Task 2: Capture And Verify The Product Screenshot

**Files:**
- Create: `$ASSET_DIR/product-home.png`
- Modify: `$TMP_DIR/source-notes.txt`

- [ ] **Step 1: Load the `web-access` and `browser:control-in-app-browser` skills**

Reason: the screenshot must come from the actual public product and browser activity must use the in-app browser.

- [ ] **Step 2: Open the live product and verify the destination**

Navigate directly to:

```text
https://savetear.cloud/
```

Expected: the browser resolves to `savetear.cloud`, and the page shows the Save Tears interface rather than an error page or unrelated host.

- [ ] **Step 3: Capture the product viewport**

Set a 1440 x 900 browser viewport, capture the visible product state, and write the PNG bytes to:

```text
$ASSET_DIR/product-home.png
```

Do not include browser chrome, private account data, tokens, or developer tools. If the public page requires login, use the public landing/login state; do not transmit credentials.

- [ ] **Step 4: Verify the asset**

Run:

```bash
file "$ASSET_DIR/product-home.png"
```

Expected: PNG image data with non-zero dimensions.

Open it with `view_image` and confirm the crop is readable at slide size. If the public site is unavailable, start the repository's H5 frontend locally and capture the equivalent interface; record that fallback in `source-notes.txt`.

### Task 3: Define And Test The Content Contract

**Files:**
- Create: `$TMP_DIR/tests/content.test.mjs`
- Create: `$TMP_DIR/deck-content.mjs`

- [ ] **Step 1: Write the failing content contract test**

Create `$TMP_DIR/tests/content.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { deckContent } from "../deck-content.mjs";

test("deck has the approved seven-slide sequence", () => {
  assert.deepEqual(deckContent.slides.map((slide) => slide.title), [
    "We Built It. Now We Need You.",
    "From Winter Camp to a Live Product",
    "Three Challenges We Cannot Solve Alone",
    "Our First AI Result",
    "Why Generic LLMs Are Not Enough",
    "Two Majors, One Working System",
    "Join the Core Team",
  ]);
});

test("speaker timing stays inside five minutes", () => {
  assert.ok(deckContent.slides.reduce((sum, slide) => sum + slide.seconds, 0) <= 300);
});

test("forecast evidence matches the report", () => {
  assert.deepEqual(deckContent.forecast.randomForest, {
    mae: 3.0179,
    rmse: 5.0867,
    r2: 0.7498,
  });
  assert.equal(deckContent.forecast.households, 810);
  assert.equal(deckContent.forecast.samples, 131220);
  assert.equal(deckContent.forecast.windowHours, 6);
});

test("unfinished capabilities remain labelled as future work", () => {
  assert.equal(deckContent.status.thingCloud, "Integration-ready");
  assert.equal(deckContent.status.greywaterAI, "Research direction");
  assert.equal(deckContent.claims.weatherIsCurrent, false);
  assert.equal(deckContent.claims.ragIsComplete, false);
  assert.equal(deckContent.claims.fineTuningIsComplete, false);
});
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/content.test.mjs"
```

Expected: FAIL because `deck-content.mjs` does not exist.

- [ ] **Step 3: Implement `deck-content.mjs`**

Create the file with this complete content:

```js
export const deckContent = Object.freeze({
  slides: [
    { title: "We Built It. Now We Need You.", seconds: 30 },
    { title: "From Winter Camp to a Live Product", seconds: 35 },
    { title: "Three Challenges We Cannot Solve Alone", seconds: 40 },
    { title: "Our First AI Result", seconds: 50 },
    { title: "Why Generic LLMs Are Not Enough", seconds: 55 },
    { title: "Two Majors, One Working System", seconds: 40 },
    { title: "Join the Core Team", seconds: 30 },
  ],
  forecast: {
    households: 810,
    samples: 131220,
    windowHours: 6,
    randomForest: { mae: 3.0179, rmse: 5.0867, r2: 0.7498 },
    r2ByModel: {
      "Random Forest": 0.7498,
      "Gradient Boosting": 0.7279,
      LSTM: 0.7168,
      "Linear Regression": 0.6941,
      "Naive lag_1": 0.5326,
    },
  },
  status: {
    product: "Live",
    forecasting: "Validated experiment",
    thingCloud: "Integration-ready",
    greywaterAI: "Research direction",
  },
  claims: {
    weatherIsCurrent: false,
    ragIsComplete: false,
    fineTuningIsComplete: false,
  },
  roles: {
    telecom: ["Sensors and gateways", "ThingCloud integration", "Data reliability"],
    software: ["International deployment", "Backend and data pipeline", "Forecasting and AI planning"],
  },
});
```

- [ ] **Step 4: Run the content test and verify it passes**

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/content.test.mjs"
```

Expected: 4 tests pass.

### Task 4: Build The Academic Minimal Presentation Kit

**Files:**
- Create: `$SLIDES_DIR/common.mjs`
- Test: `$TMP_DIR/tests/content.test.mjs`

- [ ] **Step 1: Add design-token assertions to the test**

Append:

```js
import { C, F, G } from "../slides/common.mjs";

test("Academic Minimal design tokens remain stable", () => {
  assert.equal(C.background, "#FFFFFF");
  assert.equal(C.blue, "#2C6F88");
  assert.equal(C.red, "#A23A35");
  assert.equal(F.heading, "Aptos Display");
  assert.equal(F.metric, "Georgia");
  assert.deepEqual(G.page, { left: 58, top: 46, width: 1164, height: 620 });
});
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/content.test.mjs"
```

Expected: FAIL because `slides/common.mjs` does not exist.

- [ ] **Step 3: Implement the shared presentation kit**

Create `$SLIDES_DIR/common.mjs`:

```js
export const C = Object.freeze({
  background: "#FFFFFF",
  ink: "#172630",
  blue: "#2C6F88",
  red: "#A23A35",
  gold: "#C9A23B",
  panel: "#F5F7F8",
  line: "#D7DEE2",
  muted: "#5A6973",
  white: "#FFFFFF",
});

export const F = Object.freeze({ heading: "Aptos Display", body: "Aptos", metric: "Georgia" });
export const G = Object.freeze({ page: { left: 58, top: 46, width: 1164, height: 620 } });

export function rect(slide, ctx, left, top, width, height, fill, line = fill) {
  return ctx.addShape(slide, { left, top, width, height, fill, line: ctx.line(line, 1) });
}

export function text(slide, ctx, value, left, top, width, height, options = {}) {
  return ctx.addText(slide, {
    left, top, width, height, text: value,
    fontSize: options.fontSize ?? 18,
    typeface: options.typeface ?? F.body,
    color: options.color ?? C.ink,
    bold: options.bold ?? false,
    align: options.align ?? "left",
    valign: options.valign ?? "top",
    insets: options.insets ?? { left: 0, right: 0, top: 0, bottom: 0 },
  });
}

export function base(slide, ctx, number, source) {
  rect(slide, ctx, 0, 0, ctx.W, ctx.H, C.background, C.background);
  rect(slide, ctx, 0, 0, ctx.W, 9, C.blue, C.blue);
  text(slide, ctx, source, 58, 684, 980, 16, { fontSize: 10, color: C.muted });
  text(slide, ctx, String(number).padStart(2, "0"), 1160, 684, 62, 16, { fontSize: 10, color: C.muted, align: "right" });
}

export function kicker(slide, ctx, value) {
  text(slide, ctx, value.toUpperCase(), 58, 42, 560, 20, { fontSize: 13, color: C.red, bold: true });
}

export function title(slide, ctx, value, width = 1100) {
  text(slide, ctx, value, 58, 78, width, 72, { fontSize: 38, typeface: F.heading, bold: true });
}

export function card(slide, ctx, left, top, width, height, accent, heading, body) {
  rect(slide, ctx, left, top, width, height, C.panel, C.line);
  rect(slide, ctx, left, top, width, 5, accent, accent);
  text(slide, ctx, heading, left + 18, top + 24, width - 36, 34, { fontSize: 22, typeface: F.heading, bold: true });
  text(slide, ctx, body, left + 18, top + 70, width - 36, height - 88, { fontSize: 17, color: C.muted });
}
```

- [ ] **Step 4: Re-run the test**

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/content.test.mjs"
```

Expected: 5 tests pass.

### Task 5: Implement Slides 1–3

**Files:**
- Create: `$SLIDES_DIR/slide-01.mjs`
- Create: `$SLIDES_DIR/slide-02.mjs`
- Create: `$SLIDES_DIR/slide-03.mjs`

- [ ] **Step 1: Implement slide 1 as the live-product recruitment hook**

The module must create a white Academic Minimal cover with the exact title `We Built It. Now We Need You.`, the subtitle `From a winter camp prototype to a live greywater platform`, and a right-side proof panel containing `LIVE`, `savetear.cloud`, `Own domain`, and `Own server`.

- [ ] **Step 2: Implement slide 2 as a three-stage timeline plus screenshot**

Use the exact stages `Winter Camp`, `Working Product`, and `Live Deployment`. Add `$ASSET_DIR/product-home.png` with `ctx.addImage`, `fit: "cover"`, and alt text `Save Tears live product interface`. Keep the screenshot on the right half and the timeline on the left.

- [ ] **Step 3: Implement slide 3 as three equal ownership cards**

Use these cards:

```js
const challenges = [
  ["01", "International deployment", "Deploy and test Save Tears outside China.", C.blue],
  ["02", "Real-world data", "Connect sensors through ThingCloud and replace mock data.", C.red],
  ["03", "Greywater-aware AI", "Forecast demand and generate safe dual-source plans.", C.gold],
];
```

The title must be `Three Challenges We Cannot Solve Alone`.

- [ ] **Step 4: Run static content checks**

Run:

```bash
rg -n "We Built It|savetear.cloud|Winter Camp|International deployment|Real-world data|Greywater-aware AI" "$SLIDES_DIR/slide-01.mjs" "$SLIDES_DIR/slide-02.mjs" "$SLIDES_DIR/slide-03.mjs"
```

Expected: all six approved phrases are present.

### Task 6: Implement The Native Forecasting Chart On Slide 4

**Files:**
- Create: `$SLIDES_DIR/slide-04.mjs`
- Modify: `$TMP_DIR/source-notes.txt`

- [ ] **Step 1: Create the native bar chart with report values**

Use `slide.charts.add("bar", config)` with:

```js
categories: ["Random Forest", "Gradient Boosting", "LSTM", "Linear Regression", "Naive lag_1"],
series: [{ name: "R²", values: [0.7498, 0.7279, 0.7168, 0.6941, 0.5326], fill: "#2C6F88" }],
hasLegend: false,
dataLabels: { showValue: true, position: "outEnd" },
xAxis: { minimumScale: 0, maximumScale: 0.8 },
```

If `xAxis.minimumScale` or `maximumScale` is rejected by runtime help, remove only those two properties and record the runtime limitation in `$QA_DIR/visual-qa.txt`; keep the chart native.

- [ ] **Step 2: Add the proof metrics and limitation note**

The slide must show:

```text
810 households
131,220 supervised samples
6 hours -> next hour
Random Forest R² = 0.7498
Current scope: public normal-water data; no greywater, weather, or temperature yet.
```

- [ ] **Step 3: Verify all displayed values against the content contract**

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/content.test.mjs"
```

Expected: all tests pass.

### Task 7: Implement The Responsible AI Pipeline On Slide 5

**Files:**
- Create: `$SLIDES_DIR/slide-05.mjs`

- [ ] **Step 1: Draw the editable six-stage pipeline**

Create six native shape boxes connected left-to-right:

```text
Forecast demand
Greywater availability
Allocation rules
RAG knowledge
LLM explanation
User plan
```

Use blue for data/prediction, muted red for the allocation decision, and gold for the research-stage RAG/LLM segment.

- [ ] **Step 2: Add the engineering judgment callout**

Use the exact callout:

```text
The LLM explains the plan. It does not invent the greywater ratio.
```

Add a `RESEARCH DIRECTION` pill and the note `Fine-tuning comes after real greywater examples and a measurable evaluation set.`

- [ ] **Step 3: Check the module for forbidden completion language**

Run:

```bash
rg -n "RAG.*complete|fine-tun.*complete|already trained|production AI" "$SLIDES_DIR/slide-05.mjs"
```

Expected: no matches.

### Task 8: Implement Slides 6–7

**Files:**
- Create: `$SLIDES_DIR/slide-06.mjs`
- Create: `$SLIDES_DIR/slide-07.mjs`

- [ ] **Step 1: Implement the two-discipline integration slide**

Slide 6 must use two equal role panels joined by a visible `ONE SYSTEM` connector.

Telecom Engineering panel:

```text
Sensors and gateways
ThingCloud integration
Data reliability
```

Software Engineering panel:

```text
International deployment
Backend and data pipeline
Forecasting and AI planning
```

- [ ] **Step 2: Implement the final on-site call to action**

Slide 7 must contain:

```text
Join the Core Team
2–4 long-term members
Deploy internationally
Connect real data
Build responsible dual-source intelligence
Choose Save Tears today.
```

Do not add a QR code, email, or fabricated logo.

- [ ] **Step 3: Verify role and call-to-action copy**

Run:

```bash
rg -n "Telecom Engineering|Software Engineering|ONE SYSTEM|2–4 long-term members|Choose Save Tears today" "$SLIDES_DIR/slide-06.mjs" "$SLIDES_DIR/slide-07.mjs"
```

Expected: all five phrases are present.

### Task 9: Build, Render, And Structurally Verify The Deck

**Files:**
- Create: `$TMP_DIR/build-deck.mjs`
- Create: `$TMP_DIR/tests/build.test.mjs`
- Create: `$TMP_DIR/artifact-build-manifest.json`
- Create: `$PREVIEW_DIR/slide-01.png` through `$PREVIEW_DIR/slide-07.png`
- Create: `$LAYOUT_DIR/slide-01.layout.json` through `$LAYOUT_DIR/slide-07.layout.json`
- Create: `$PREVIEW_DIR/contact-sheet.webp`
- Create: `output/ppt/save-tears-uk-core-team-recruitment.pptx`

- [ ] **Step 1: Implement the build script with artifact-tool workspace setup**

The script must:

1. Import `ensureArtifactToolWorkspace`, `importArtifactTool`, `createSlideContext`, and `saveBlobToFile` from `$SKILL_DIR/scripts/artifact_tool_utils.mjs`.
2. Create a `Presentation` at 1280 x 720.
3. Import and execute `slide01` through `slide07` in order.
4. Export every slide as PNG and layout JSON.
5. Export a montage as WebP.
6. Export the final PPTX using `PresentationFile.exportPptx(presentation)`.
7. Write a JSON manifest with `slideCount: 7`, final output bytes, and all preview/layout paths.

Use this export sequence:

```js
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await saveBlobToFile(
    await presentation.export({ slide, format: "png", scale: 1 }),
    path.join(process.env.PREVIEW_DIR, `${stem}.png`),
  );
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(process.env.LAYOUT_DIR, `${stem}.layout.json`), await layout.text());
}

await saveBlobToFile(
  await presentation.export({ format: "webp", montage: true, scale: 1 }),
  path.join(process.env.PREVIEW_DIR, "contact-sheet.webp"),
);

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(process.env.FINAL_PPTX);
```

- [ ] **Step 2: Run all unit tests before building**

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/content.test.mjs"
```

Expected: all content and design-token tests pass.

- [ ] **Step 3: Build the deck**

Run:

```bash
"$NODE" "$TMP_DIR/build-deck.mjs"
```

Expected: seven PNGs, seven layout JSON files, one contact sheet, one manifest, and the final PPTX.

- [ ] **Step 4: Write and run the build artifact test**

Create `$TMP_DIR/tests/build.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";

test("final presentation artifacts are complete", async () => {
  const manifest = JSON.parse(await fs.readFile(path.join(process.env.TMP_DIR, "artifact-build-manifest.json"), "utf8"));
  assert.equal(manifest.slideCount, 7);
  assert.equal(manifest.previewPaths.length, 7);
  assert.equal(manifest.layoutPaths.length, 7);
  assert.ok(manifest.outputBytes > 10000);
  const stat = await fs.stat(process.env.FINAL_PPTX);
  assert.ok(stat.size > 10000);
});
```

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/build.test.mjs"
```

Expected: 1 test passes.

### Task 10: Perform Visual QA, Fix Defects, And Commit The Deliverable

**Files:**
- Create: `$QA_DIR/visual-qa.txt`
- Modify as required: `$SLIDES_DIR/slide-01.mjs` through `$SLIDES_DIR/slide-07.mjs`
- Regenerate: `$PREVIEW_DIR/*`, `$LAYOUT_DIR/*`, `$FINAL_PPTX`
- Stage: `output/ppt/save-tears-uk-core-team-recruitment.pptx`

- [ ] **Step 1: Inspect the contact sheet and every slide render**

Open `$PREVIEW_DIR/contact-sheet.webp` with `view_image`, then inspect all seven full-size PNGs. Record every issue in `$QA_DIR/visual-qa.txt` using the presentation skill's visual QA template.

Check specifically:

- title-only storyline is coherent;
- no three-slide run repeats the same macro-layout;
- no clipping, overflow, detached connectors, or unreadable source footer;
- chart labels match the source values;
- product screenshot is readable and not distorted;
- `Live`, `Integration-ready`, and `Research direction` are not visually confused;
- slide 5 clearly assigns the ratio decision to rules/optimization rather than the LLM.

- [ ] **Step 2: Inspect layout JSON for overflow signals**

Run:

```bash
rg -n 'overflow|clip|outOfBounds|warning' "$LAYOUT_DIR" || true
```

Expected: no unresolved layout warnings. Any false positive must be explained in `visual-qa.txt`.

- [ ] **Step 3: Fix every blocker and rerender**

For each blocker, change only the responsible slide module, run the build script again, and reopen the updated render. Do not shrink important body text below 18 px; rewrite or relayout instead.

- [ ] **Step 4: Verify PPTX structure and fonts**

Run:

```bash
test -s "$FINAL_PPTX"
unzip -l "$FINAL_PPTX" | rg 'ppt/slides/slide[0-9]+.xml' | wc -l
unzip -p "$FINAL_PPTX" 'ppt/slides/slide*.xml' | rg -o 'typeface="[^"]+"' | sort -u
```

Expected:

- file is non-empty;
- slide XML count is 7;
- intended typefaces include Aptos/Aptos Display and Georgia, with no unintended fallback replacing them.

- [ ] **Step 5: Run the final verification suite**

Run:

```bash
"$NODE" --test "$TMP_DIR/tests/content.test.mjs" "$TMP_DIR/tests/build.test.mjs"
git status --short -- output/ppt/save-tears-uk-core-team-recruitment.pptx
```

Expected: all tests pass and only the intended new PPTX appears for this task.

- [ ] **Step 6: Commit only the final PPTX**

Run:

```bash
git add output/ppt/save-tears-uk-core-team-recruitment.pptx
git diff --cached --name-status
git commit -m "Add UK core team recruitment deck"
```

Expected: the staged list contains only `output/ppt/save-tears-uk-core-team-recruitment.pptx`, and the commit succeeds without including existing user changes.

## Final Handoff

Return:

- the absolute clickable path to `output/ppt/save-tears-uk-core-team-recruitment.pptx`;
- confirmation that the deck has seven slides and all were rendered and inspected;
- the content/build test result;
- any accepted visual or runtime caveat recorded in `$QA_DIR/visual-qa.txt`.
