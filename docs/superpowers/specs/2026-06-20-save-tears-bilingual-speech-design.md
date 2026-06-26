# Save Tears Bilingual Recruitment Speech Design

## Objective

Create a five-minute recruitment speech that follows the existing seven-slide English deck and persuades UK Telecom Engineering and Software Engineering students to join the Save Tears core team.

## Delivery Format

- English is the only language spoken on site.
- Chinese appears after each English slide section as a rehearsal and comprehension aid.
- The script is organised slide by slide so the speaker always knows when to advance.
- The English script targets about 520–540 words, suitable for a clear non-native speaking pace with short pauses.

## Tone

Use a natural technical-pitch style: direct, confident, and conversational. Avoid academic-paper phrasing, exaggerated claims, marketing clichés, and long sentences. Explain uncommon terms in plain English when they first matter.

## Seven-Part Story

1. Establish that Save Tears is already a live product and invite the audience into its next stage.
2. Summarise the progression from winter camp to deployment.
3. Turn the three unresolved challenges into concrete ownership opportunities.
4. Present the validated normal-water forecasting result and its limitations.
5. Explain why greywater planning needs deterministic allocation plus RAG and LLM explanation.
6. Show how Telecom and Software Engineering responsibilities connect into one system.
7. Ask 2–4 students to choose Save Tears during the on-site selection.

## Fact Boundaries

- The website has its own domain and server and its public entry was verified reachable.
- Do not claim that authenticated workflows or current backend health were freshly verified.
- The existing ThingCloud-compatible endpoint is integration-ready, but real devices are not connected yet.
- The machine-learning result uses public normal-water data: 810 households, 131,220 samples, six previous hours to predict the next hour, with Random Forest R² = 0.7498.
- Weather, temperature, and real greywater data are not current model inputs.
- Greywater-aware planning, RAG, fine-tuning, and allocation optimisation are next-stage research work.
- Deterministic rules or an optimiser choose safe greywater allocation; the LLM explains the result instead of inventing the greywater ratio.

## Usability Requirements

- Include brief stage directions such as `[Pause]`, `[Point to the chart]`, and `[Next slide]` only where they improve delivery.
- Use words that a second-year software engineering student can say naturally.
- Keep the Chinese translation faithful to the spoken meaning rather than translating word by word.
- End with a direct on-site call to action and no QR code or email instruction.

## Acceptance Criteria

- Every slide has one English spoken section and one Chinese reference section.
- The full English script fits approximately five minutes including transitions.
- All numerical claims match the approved PPT and source report.
- The script clearly distinguishes completed work, integration-ready work, and research directions.
- The final call asks for 2–4 long-term core members from the two target majors.
