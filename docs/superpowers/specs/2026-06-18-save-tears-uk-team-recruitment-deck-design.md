# Save Tears UK Core Team Recruitment Deck Design

## Objective

Create a concise, fully English recruitment deck that persuades UK students in Telecom Engineering and Software Engineering to join the Save Tears project as long-term core members.

The presentation will be delivered in person during a UK-China summer camp or project-team recruitment session. It must fit a five-minute talk and support an immediate on-site decision. The target outcome is to recruit two to four core members.

## Audience

- UK Telecom Engineering students who can contribute sensors, gateways, ThingCloud integration, and data reliability.
- UK Software Engineering students who can contribute international deployment, backend and data pipelines, forecasting, and AI planning.
- Students should see a working product with meaningful open engineering problems, not a speculative idea or a conventional course report.

## Core Message

The deck will use the recruitment narrative:

> We built it. Now we need you.

Save Tears started during the winter camp and has progressed to a live web product with its own domain and server. The team now needs international collaborators to complete the next engineering stage: overseas deployment, real device data, and responsible greywater-aware planning.

## Truth And Evidence Boundaries

The presentation must distinguish current capabilities from future research.

| Status | Claim allowed in the deck |
| --- | --- |
| Live | The web product, domain, server, frontend, and backend are running. |
| Validated experiment | The normal-water forecasting experiment used 810 households and 131,220 supervised samples. Random Forest achieved MAE 3.0179, RMSE 5.0867, and R2 0.7498. |
| Integration-ready | The backend provides a ThingCloud-compatible ingestion endpoint, but real devices are not yet connected. |
| Research direction | Greywater-aware plan generation using allocation rules, RAG, and an open-source LLM has not yet been implemented. |

The forecasting model currently uses the previous six hours of water consumption plus time, rolling-window, and household-history features. Weather and temperature must be described as future extensions, not current inputs.

The deck must not claim that RAG or model fine-tuning is complete. It will refer to small open-source LLMs in general and will not name an unverified model such as `Gemma4-4B`.

## Technical Position

The proposed intelligent planning flow is:

```text
Sensors
  -> ThingCloud
  -> Backend and dual-source data
  -> Demand forecasting
  -> Water-allocation rules or optimizer
  -> RAG knowledge retrieval
  -> LLM explanation
  -> User-facing water-saving plan
```

The LLM must not invent the greywater ratio. A deterministic rule or optimization layer should decide allowed greywater uses, allocation limits, and safety constraints. RAG supplies domain knowledge, and the LLM converts the structured decision into a readable, personalized plan. Fine-tuning may be evaluated only after the team has collected enough greywater examples and defined a measurable evaluation set.

This division matters because it gives Telecom students a concrete path from devices to reliable data and gives Software Engineering students clear ownership of deployment, data processing, forecasting, planning logic, and user-facing AI.

## Slide Structure

The final deck will contain seven 16:9 slides.

### Slide 1 - We Built It. Now We Need You.

- Establish Save Tears as a UK-China student engineering project.
- State that the project progressed from a winter camp prototype to a live product.
- Show `savetear.cloud`, its own domain, and its own server as immediate proof.
- Target speaking time: 30 seconds.

### Slide 2 - From Winter Camp to a Live Product

- Present a short progression: winter camp idea, software development, live deployment.
- Use one verified product screenshot rather than a stock image.
- Mention the working frontend, backend, domain, and server without listing implementation details that do not help recruitment.
- Target speaking time: 35 seconds.

### Slide 3 - Three Challenges We Cannot Solve Alone

- International deployment and testing outside China.
- Real sensor data through ThingCloud.
- Greywater-aware AI planning.
- Present these as real ownership opportunities for new members.
- Target speaking time: 40 seconds.

### Slide 4 - Our First AI Result

- Show the six-hour input window and next-hour prediction task.
- Present 810 households and 131,220 supervised samples.
- Use an editable model-comparison chart and emphasize Random Forest at `R2 = 0.7498`.
- State the limitation: the current experiment predicts normal water demand from public data and does not yet include greywater, weather, or temperature.
- Target speaking time: 50 seconds.

### Slide 5 - Why Generic LLMs Are Not Enough

- Contrast generic tap-water advice with the actual dual-source decision problem.
- Explain that the system must decide where greywater is permitted, how much is available, and what proportion should replace tap water.
- Show the proposed flow: forecasting, allocation constraints, RAG knowledge, then LLM explanation.
- Label this clearly as the research direction rather than a finished feature.
- Target speaking time: 55 seconds.

### Slide 6 - Two Majors, One Working System

- Telecom Engineering: sensors and gateways, ThingCloud integration, and data reliability.
- Software Engineering: international deployment, backend and data pipeline, forecasting, and AI planning.
- Emphasize integration: both disciplines deliver one end-to-end system rather than separate demonstrations.
- Target speaking time: 40 seconds.

### Slide 7 - Join the Core Team

- Recruit two to four long-term core members.
- State the shared mission: deploy internationally, connect real data, and build a responsible dual-source planning system.
- Use an on-site call to action; no QR code or email is required because participants will choose during the session.
- Target speaking time: 30 seconds.

The remaining time is reserved for transitions and minor audience reaction.

## Visual Direction

Use the approved Academic Minimal direction.

- Canvas: 16:9 widescreen.
- Background: white or very light neutral.
- Primary color: restrained university blue.
- Accent color: muted red for decisions and key transitions.
- Supporting accent: muted gold only for selected highlights.
- Typography: an Office-safe sans-serif family for headings and body text, with a serif family used sparingly for major metrics.
- Layout: large margins, strong alignment, short text blocks, and visible evidence.
- Visual tone: serious student engineering project, not a corporate sales deck and not a course-report template.

The slides will use native editable shapes, text, diagrams, and charts. They will not use full-slide bitmaps. Stock photography and decorative AI imagery are out of scope because they would weaken the project's real evidence.

## Asset And Provenance Plan

- Product proof will come from the verified Save Tears deployment and local project materials.
- Model metrics will come from the user-provided artificial-intelligence course design report.
- The model comparison will be redrawn as an editable chart from the report values.
- The system flow and role split will be built as editable diagrams.
- Source footers will be short and audience-readable. Private local paths will not appear in the deck.
- No water-scarcity statistic, logo, university mark, or model benchmark will be added unless it has a verified source.

## Failure And Fallback Handling

- If the live website cannot be captured, use an existing verified local product screenshot.
- If a detailed page is visually cluttered, crop to one clear interface state rather than shrinking the entire page.
- If the model chart becomes too dense, show R2 values only and keep MAE/RMSE in the source notes.
- If the five-minute rehearsal runs long, shorten slide 2 and slide 4 narration before removing the role or call-to-action slides.
- If a statement cannot be traced to the repository, deployment notes, or the course report, remove or qualify it.

## Verification And Acceptance Criteria

The deck is complete only when all of the following are true:

- Exactly seven slides are present in the expected order.
- All visible slide content is in English.
- The deck can be delivered in five minutes without rushing.
- Product, ThingCloud, forecasting, and RAG/LLM statuses match the truth boundaries above.
- The model chart values match the course report.
- Every slide is rendered and visually inspected for clipping, overflow, accidental wrapping, misalignment, and unreadable footers.
- The final PPTX remains editable and uses native presentation elements.
- The final file is exported to `output/ppt/save-tears-uk-core-team-recruitment.pptx`.

## Out Of Scope

- Building the overseas deployment.
- Connecting real ThingCloud devices.
- Implementing RAG, fine-tuning, or the allocation optimizer.
- Creating a recruitment form or collecting participant contact details.
- Claiming model performance on domestic campus or real Save Tears production data.
