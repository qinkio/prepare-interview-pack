# Basic Company Verification

Read before company-specific analysis in every mode. Keep research proportional to the interview deadline, but finish the baseline on the first pass.

## Coverage

1. **identity**: exact recruiting name checked against the original JD/image; legal entity, parent, brand and actual team where relevant. Do not merge similarly named companies. If unresolved, preserve alternatives and ask one targeted identity question.
2. **scale_and_model**: business model, product/customer, team or store footprint, direct/franchise/channel structure when relevant. Distinguish job-board staff labels, dated brand totals and actual hiring team. Do not invent financials.
3. **recent_developments**: search recent role-relevant announcements, financing, expansion, contraction or business changes. Use approximately the past year as a starting window, expanding only when useful; preserve publication/event dates. A hiring list alone does not prove accelerated growth.
4. **conflicts**: compare material claims across supplied and public evidence: names, ownership, address, founding date, funding and scale. Show disagreements and limits. Syndicated copies count as one evidence origin. No material conflict found is a bounded conclusion about sources checked.
5. **interview_implications**: connect findings to likely priorities, candidate positioning and at least one tailored answer or question. Separate sourced facts, STARS inference and culture hypotheses. Use `Not classifiable` when stage evidence is insufficient.

Start with supplied sources, then search exact company and brand names. Prefer company announcements, official registries and authoritative industry sources; label recruiting pages and secondary sources honestly. For small/private companies, missing public facts are acceptable after a relevant search. Record unavailable facts and the best confirmation question. Do not prolong research merely to fill every field with a positive fact.

Honor explicit instructions not to browse. When tools are unavailable, record the failure and use supplied evidence without claiming current verification. For every supported topic, store `evidence` entries with `source_id`, a precise `locator` (image name, block ID, page or paragraph), and a short `excerpt` actually observed. Several screenshots from one conversation are separate sources when they support different claims. Check each finding against its specific excerpt; do not attach an address claim to a salary/KPI screenshot merely because both belong to the same chat.

Keep `published_at` and `updated_at` separate. Unknown dates are null; access/crawl dates are not publication dates. A non-null date requires `date_evidence` containing the observed label and location. If a dynamic page changes on re-read, record the observed update and access date; retain an excerpt or snapshot when available, and do not overwrite the original observation without noting the difference.

A timeout is not proof that a page contains a fact; a search snippet is not a source read. Reuse previous research only after checking entity match, dates and coverage.

## Local Research Ledger

Save `company-research.json` beside the handbook. Use this schema:

```json
{
  "checked_at": "YYYY-MM-DD",
  "mode": "searched",
  "exception_reason": "",
  "sources": [
    {"id": "s1", "pointer": "https://example.com/company", "kind": "official", "accessed_at": "YYYY-MM-DD", "published_at": null, "updated_at": null, "date_evidence": ""}
  ],
  "searches": [
    {"id": "q1", "query": "exact company name recent developments", "outcome": "read", "source_ids": ["s1"]}
  ],
  "topics": {
    "identity": {"status": "supported", "finding": "Replace with source-grounded identity and original-name check.", "source_ids": ["s1"], "search_ids": ["q1"], "evidence": [{"source_id": "s1", "locator": "company introduction paragraph", "excerpt": "Replace with a short passage actually read."}]},
    "scale_and_model": {"status": "partial", "finding": "Replace with business-model finding and limits.", "source_ids": ["s1"], "search_ids": ["q1"], "evidence": [{"source_id": "s1", "locator": "company introduction paragraph", "excerpt": "Replace with a short passage actually read."}]},
    "recent_developments": {"status": "not-found", "finding": "Replace with what was searched and what remains unavailable.", "source_ids": [], "search_ids": ["q1"], "evidence": []},
    "conflicts": {"status": "partial", "finding": "Replace with conflicts or bounded comparison outcome.", "source_ids": ["s1"], "search_ids": ["q1"], "evidence": [{"source_id": "s1", "locator": "company introduction paragraph", "excerpt": "Replace with a short passage actually read."}]},
    "interview_implications": {"status": "supported", "finding": "Replace with evidence-linked preparation implication, labeled as inference.", "source_ids": ["s1"], "search_ids": [], "evidence": [{"source_id": "s1", "locator": "company introduction paragraph", "excerpt": "Replace with a short passage actually read."}]}
  }
}
```

- `mode`: `searched`, `provided-only` (explicit user no-browsing instruction), or `unavailable` (tool/access failure). The latter two require a concrete `exception_reason`; they must not be chosen merely to save time.
- Source `pointer`: URL or supplied file/block pointer actually read. `kind`: describe provenance (official, registry, recruiting, media, secondary, user-provided). `accessed_at` and `checked_at`: ISO dates; preserve publication and update dates independently when available, otherwise null. Known dates require `date_evidence` with the observed date label and location.
- Search `outcome`: `read`, `no-results`, or `blocked`. Read searches link sources actually inspected. Empty searches are allowed only with a justified exception mode.
- Topic `status`: `supported`, `partial`, `not-found`, or `blocked`. Every topic needs a substantive `finding` and an `evidence` list (empty for genuinely missing facts). Supported/partial topics need at least one precise excerpt from a listed source. Excerpts for implications ground the underlying facts; the implication itself remains labeled inference. Supported/partial findings link sources; searched factual topics also link relevant search attempts. Implications may use supplied evidence without a search link. Missing facts cite attempts rather than invented sources.

Run `scripts/validate_pack.py <handbook.md> --mode <mode> --company-research <ledger.json>` and add the resume manifest when applicable. Missing or invalid research evidence is an error in every mode. The script reports structural validity and `research_status` separately: `searched`, `searched-with-gaps`, `provided-only`, `unavailable`, or `invalid`. A ledger marked `searched` with only blocked attempts is invalid; record `unavailable` with the actual failure instead. Legitimate exceptions permit useful preparation but do not establish current public research. The script checks coverage, dates and reference integrity; it cannot prove browsing occurred or facts are true. Manually compare the ledger with actual source content and handbook statements before publication.
