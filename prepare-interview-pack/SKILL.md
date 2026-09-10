---
name: prepare-interview-pack
description: "Create an end-to-end, evidence-backed interview handbook and rehearsal plan from an active JD, resume, career assets, interview time, and interview round. Use for full interview preparation: recruiter first-impression screening, JD diagnosis, competency ranking, experience mapping, self-introductions, project stories, predicted questions, gap answers, memorization priorities, mock follow-ups, and Notion or Markdown publication. Do not use for resume rewriting, cover letters, offer evaluation, job discovery, or post-interview messages; use the relevant job-search skill for those tasks."
---

# Prepare Interview Pack

Build an adaptive interview-preparation system, not a fixed long report. Optimize for truthful claims, persuasive spoken delivery, and the candidate's remaining preparation time. Keep the answer library complete even when rehearsal time is short.

## Apply the Scope Boundary

Use this skill when the requested outcome is a complete interview handbook or rehearsal plan. If the user only wants a tailored resume, cover letter, offer review, job search, or follow-up message, route to the relevant job-search skill. If both are requested, complete the application artifact first, then use the approved facts here.

## Gate the Inputs

Locate:

- The complete JD.
- At least one candidate evidence source: current resume, canonical claim register, or career asset library.
- Interview time and round, when available.
- Desired output language and publication target.

Treat the JD and candidate evidence as critical. If either is absent and cannot be located, ask one concise question and pause the full handbook. Do not construct candidate stories from assumptions.

Treat interview time and round as important but non-blocking. If absent, use Standard mode and Hiring Manager round, then label both assumptions. Follow the user's language unless asked otherwise. Use Markdown unless the user explicitly requests a connected document service.

## Adapt to the Host

Run on Codex, WorkBuddy, or another host without assuming a specific invocation syntax or tool name. Inspect the capabilities available in the current session and use this fallback order:

1. **Candidate files:** read attached PDF, Word, image, Markdown, or text files with the host's available file tools. If a critical file cannot be parsed, ask for extracted text instead of guessing.
2. **Company research:** use web access when current company facts materially affect the answer. If browsing is unavailable, analyze the JD and supplied materials, label current company facts `Unverified-current`, lower STARS confidence, and list the facts to verify.
3. **Publication:** publish through the connected service requested by the user when that connector exists. Otherwise deliver a complete Markdown file or response that can be pasted into Notion, Tencent Docs, Word, or another editor without restructuring.
4. **Validation:** resolve `scripts/validate_pack.py` relative to this `SKILL.md`, not relative to the conversation workspace. Run it with Python 3 when shell execution is available. If Python or shell execution is unavailable, perform the equivalent manual checks from `references/quality-checklist.md` and disclose that automated validation did not run.
5. **Unsupported integrations:** preserve the completed handbook locally or in the response and give concise manual publication steps. Do not block the analysis solely because a connector is missing.

Do not require `$prepare-interview-pack`, slash commands, `$ARGUMENTS`, Codex-specific agents, or any other host-specific invocation mechanism. Natural-language requests are sufficient.

## Route Before Analyzing

Read [references/routing-and-scoring.md](references/routing-and-scoring.md), then select:

- **Sprint mode** for less than 24 hours.
- **Standard mode** for 1–3 days or an unknown deadline.
- **Deep mode** for more than 3 days.

Also select the interview-round lens: HR, Hiring Manager, Cross-functional, Final, or Mixed/Unknown. Let the user override either selection. Use the mode to change rehearsal priority and research depth, not to remove the core answer library.

When the user identifies an earlier handbook as a stronger reference or asks for a comparison, read the actual reference artifacts before drafting. Compare P0 discoverability, role specificity, spoken naturalness, evidence boundaries, useful depth, total length, and duplication. Reuse structural strengths, not role-specific claims. A newer handbook must not become harder to rehearse merely because it contains more analysis.

## Build the Evidence Ledger

Read all relevant candidate sources before drafting. Record each material claim with project, period, exact candidate role, actions, metric definition, baseline, result, denominator, timeframe, ownership scope, and source pointer.

Apply this source priority:

1. Candidate-approved canonical claims.
2. Resume and formal project records.
3. Contemporaneous work assets.
4. Prior interview drafts.

Assign one status to every claim:

- `Verified`: supported by documentary evidence and safe to speak.
- `Candidate-confirmed`: explicitly confirmed by the candidate and safe to speak within the confirmed metric, period, population, ownership, and publication boundaries. This may include historical numerical results when the approved career vault records them as `user-confirmed`.
- `Derived-safe`: a conservative method or interpretation derived from verified evidence; safe as analysis or future approach, not as a historical result.
- `Confirm`: plausible but requires candidate confirmation.
- `Conflict`: sources disagree.
- `Inference`: analysis rather than candidate fact.
- `Do not use`: unsupported or misleading.

Use `Verified` when documentary evidence supports the claim. A numerical result or historical ownership claim may instead be `Candidate-confirmed` when the candidate explicitly confirms it and its speaking boundary is complete enough to avoid a misleading comparison. Use `Derived-safe` only for clearly framed judgment, transferable method, or future action. Put `Confirm`, `Conflict`, and unsupported `Inference` items in a separate verification list. Never convert a team result into personal ownership. Distinguish owned, co-owned, participated, and inherited work.

When a Career Proof v0.2 vault is available, treat a claim as eligible for a speaking script only when all of these are true:

- `status` is `verified` or `user-confirmed`;
- `publication_permission` permits the intended use, such as `application-only` for a targeted resume or interview;
- there is no unresolved conflict affecting the statement;
- the available period, population, calculation, and ownership fields are sufficient for the exact wording used.

Map eligible `verified` claims to `Verified` and eligible `user-confirmed` claims to `Candidate-confirmed`. Do not downgrade an explicitly confirmed result value to `Confirm` merely because a finer detail such as the exact month remains optional. Put that missing detail in a refinement note. If populations differ across stages, state each stage separately rather than manufacturing a same-denominator trend. Claims with `not-approved` permission remain excluded even when their truth status is confirmed.

Evidence status and source provenance are analyst-facing metadata. A supported claim may enter a speaking script, but the script must state the experience directly in the candidate's first person; it must never say that a resume, document, work asset, or evidence record proves or records the claim. If a claim is not safe without citing its source, exclude it from the speaking script and place it in the verification list.

## Run the Recruiter First-Impression Lens

When a complete resume is available, read [references/resume-screening-lens.md](references/resume-screening-lens.md) before story selection. Simulate both HR and hiring-manager screening, then convert the result into:

- The candidate identity perceived in the first scan.
- The three most consequential interview validation risks.
- Missing, synonymous, adjacent, and unsupported JD language.
- Weak evidence in role-critical claims.
- The questions and proof needed to resolve those risks in interview.

Keep this diagnostic compact in the handbook. Do not rewrite the resume unless the user separately requests an application artifact. If only extracted text is available, label the result a content-order simulation; inspect the rendered first page when a PDF is available.

## Enforce Resume Project Coverage

When a complete resume is available, create a resume-project manifest before selecting stories. Include every named project, representative initiative, and recent project that an interviewer could point to on the resume. Do not limit the manifest to claims that already have complete metrics.

For every manifest item, assign one explicit disposition:

- `P0`: directly relevant to the JD or likely to be challenged in the interview; provide a complete spoken story.
- `P1`: relevant secondary proof; provide a safe 60–90 second answer.
- `P2`: background, gap-period, or lower-priority proof; retain a concise answer or fact boundary.
- `Excluded`: omit only when genuinely irrelevant, duplicated, prohibited, or outside the requested interview scope; record the reason.

Evidence quality changes what the candidate may claim, not whether a resume-listed project remains discoverable in the handbook. If a project has incomplete or conflicting result evidence, retain the project, write the strongest safe version using its verified role, judgment, and actions, and move only the unsafe result to the verification list. Never silently drop a resume project because its metric is `Confirm`, `Conflict`, or unavailable.

Make the coverage ledger visible near the story-selection or requirement-to-evidence section. Before delivery, confirm that every manifest item appears with a P0, P1, P2, or Excluded disposition. When the validator is available, save the manifest as JSON or one project per line and pass it with `--resume-projects`.

## Decode the Role

Identify the hiring problem, outcome groups, must-haves, preferred qualifications, hidden constraints, and likely evaluation criteria.

Resolve company identity at four levels when relevant: recruiting entity, parent company, brand or business unit, and the actual team or market. Search user-provided sources first. If identity remains ambiguous, state the boundary, avoid high-confidence brand-specific claims, analyze the confirmed and provisional levels separately, and put one identity-confirmation question in P0.

Rank the five most relevant standard competencies with the scoring rubric in [references/routing-and-scoring.md](references/routing-and-scoring.md). Show the total score, decisive JD evidence, and interview implication. Do not invent keyword counts.

For STARS analysis:

- Assess parent company, business unit, and role separately when evidence allows.
- Use Start-up, Turnaround, Accelerated Growth, Realignment, Sustaining Success, or `Not classifiable`.
- State confidence and evidence for each conclusion.
- Describe culture as a testable hypothesis, not a confirmed fact.

Include a compact company-and-role STARS map in every mode, including Sprint. Compress the research detail when time is short, but never omit stage, priorities, culture hypotheses, and interview implications.

If current company facts materially affect the analysis, verify them with current authoritative sources unless the user asks not to browse. Prefer company sites, investor materials, official announcements, and authoritative industry sources over job-board summaries.

Describe the dream candidate through a typical day, plain-language superpower, representative success pattern, synthesized belief statement, and pain profile. Label the belief statement as a synthesis; never present it as an employer quotation.

## Map Evidence and Select Stories

Build a requirement-to-evidence map using `Strong`, `Transferable`, or `Gap`. Cite the exact project and eligible approved claim behind each match.

Score candidate stories with the rubric in [references/routing-and-scoring.md](references/routing-and-scoring.md), then select:

- One primary story that best solves the role's central pain and clears the directness threshold.
- One backup story covering a different top competency.
- One optional conflict, failure, or risk example when the chosen mode includes it.

If no story clears the directness threshold, ask for one role-critical example. When the interview is imminent, continue with the best available story but label it `provisional`, state what it cannot prove, and do not pretend that an adjacent system project is direct commercial ownership.

Frame domain-adjacent experience as transferable method only when the underlying decisions and work are genuinely comparable. Acknowledge material gaps directly.

## Generate Spoken Answers

Create a one-line positioning statement plus 60-second and 90-second introductions in every mode. Add a 30-second version when HR screening is likely. Structure project stories as conclusion → context → exact role → key judgment → actions → eligible result → transfer to the target role.

Follow the duration guidance in [references/routing-and-scoring.md](references/routing-and-scoring.md). Prefer short sentences and natural transitions. Mirror the candidate's normal vocabulary when evidence of their speaking style exists. Keep written analysis separate from words intended to be spoken.

Treat introductions, project scripts, complete question answers, transitions, stop sentences, and culture-fit phrases as candidate-facing speech. In those passages:

- Convert supported facts into direct first-person language. Preserve the actual metric boundary; for example, say `项目初期客户使用率为 15%，后期全量推广阶段整体覆盖率达到 100%` when the stages or populations differ.
- Never expose provenance or workflow labels such as `简历记录`, `简历中显示`, `根据简历`, `工作资料证明`, `Verified`, or `Confirm`.
- Express boundaries as ownership, metric, period, or domain limits, not as commentary about what the resume contains.
- Keep evidence anchors outside the spoken passage. Make them compact fact reminders; place source pointers and claim statuses only in the analysis appendix or final claim card.

After drafting, read every candidate-facing passage as if the candidate were saying it aloud. Rewrite any sentence that sounds like an analyst, recruiter, editor, or document narrator.

Generate at least 10–12 high-probability questions in every mode. Write a complete, natural spoken answer for every core question; add bullets only as a memory aid after the script. For the five P0 questions, also include an evidence anchor, the most likely follow-up, and a stop sentence or safe boundary. For remaining P1 questions, a complete answer plus one-line memory headline is sufficient unless the risk is material. Generate questions according to the round lens:

- HR: motivation, stability, compensation, transitions, and baseline fit.
- Hiring Manager: business judgment, project depth, metrics, prioritization, and execution.
- Cross-functional: collaboration, conflict, boundaries, dependencies, and influence.
- Final: strategic understanding, maturity, values, leadership range, and long-term potential.

For each introduction and project story, provide a transition sentence, a stop sentence, and two or three directions for optional expansion. Tie every culture-fit phrase to a real project. Draft gap answers as brief acknowledgement → adjacent evidence → learning method → early action plan. Tailor three interviewer questions to current priorities, success measures, decision rights, or blockers.

Keep the document strengths-led: spend most speaking content proving fit and capability. Keep warnings, gaps, and prohibitions compact and pair every material gap with the strongest truthful counter-evidence. Do not let risk controls dominate the candidate narrative.

## Create the Rehearsal Loop

Include three layers of follow-up for each P0 story:

1. Why did you make that judgment?
2. What did you personally do?
3. How was the result measured?

Provide a self-rehearsal scorecard for relevance, clarity, credibility, ownership precision, and spoken delivery. Do not claim that a mock interview occurred unless the candidate actually answered. When the user continues, run the questions interactively, score the responses, and revise the scripts from observed weaknesses.

## Prioritize and Publish

Read [references/output-template.md](references/output-template.md) and [references/gold-quality-standard.md](references/gold-quality-standard.md). Produce a two-layer artifact: a compact Battle Card first, followed by the complete answer library and analysis appendix. Keep the core spoken-answer sections complete in every mode. In Sprint mode, make the Battle Card independently usable, mark what to rehearse first, and compress analysis appendices instead of deleting answers.

Read [references/rapid-review-card.md](references/rapid-review-card.md) when the user asks for a last-minute card, the interview is within 24 hours, or the complete handbook is too long to use comfortably in one sitting. Produce the rapid-review card as a companion, never as a replacement for the complete answer library. Run `python3 <skill-directory>/scripts/validate_rapid_card.py <card.md>` when shell execution is available; otherwise complete the equivalent manual checks and disclose that automated validation did not run.

Read [references/quality-checklist.md](references/quality-checklist.md) before delivery.

Before delivery or publication, run `python3 <skill-directory>/scripts/validate_pack.py <handbook.md> --mode <sprint|standard|deep>` when shell execution is available. When a complete resume was read, also pass `--resume-projects <manifest.json|manifest.txt>`. Resolve `<skill-directory>` from the installed skill location; do not assume the current working directory. Treat every reported error as a required revision. Review warnings explicitly and fix those that are relevant. When automated validation is unavailable, complete the manual checklist and state that the script did not run. Never claim an automated pass unless the validator ran successfully.

When the user explicitly requests a connected document service, use the host's available publishing or knowledge-capture capability. Search exact role and artifact titles before writing when the service supports it. Update the existing role page by section unless the user requests a new page. Preserve unrelated content and candidate-approved facts. Add a last-updated date, avoid duplicate headings, read the result back when possible, and return the page or file link. If a rapid-review card is required, create or update it as a child or clearly related document, add a prominent link near the top of the full handbook when supported, and read both artifacts back. Verify required sections, link resolution, truncation, unknown blocks, and spoken-language provenance leaks when the host exposes those signals.

Otherwise deliver finished Markdown that can be pasted into a document editor without restructuring.

Lead with the immediate P0 rehearsal order. End with `Rehearse now`, `Review later`, and `Verify before speaking`.
