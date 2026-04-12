# How to Add a Risk Pattern

Risk patterns are pre-configured risk item clusters that trigger automatically when an AI system matches a category and purpose keyword combination.

## When to add a pattern

Add a pattern when:
- A specific combination of Annex III category + use case creates a well-known, documented risk cluster
- The risk cluster has established Article references in the EU AI Act or related regulation
- The risk is specific enough to generate useful pre-populated risk items (not just generic statements)

## Step 1: Edit the patterns file

Patterns live in `src/riskforge/_data/patterns/patterns.yaml`.

Add a pattern block:

```yaml
- pattern_id: YOUR_PATTERN_ID        # SCREAMING_SNAKE_CASE, unique
  name: "Human-readable pattern name"
  triggers:
    annex_iii_category: employment   # One Annex III category
    purpose_keywords: ["keyword1", "keyword2"]   # Any of these words in the system purpose
  risks:
    - dimension: discrimination
      title: "Short, specific risk title"
      description: "One to two sentences. Cite the Article that creates the obligation."
      likelihood_hint: 3
      severity_hint: 4
      article_refs: ["Art.9(2)(a)"]
      nist_rmf_ref: "MEASURE 2.9"
      iso42001_ref: "Clause A.7"
```

## Guidelines

- Each pattern should generate 2-4 risk items, not just one
- `likelihood_hint` and `severity_hint` are starting points — assessors always override
- `purpose_keywords` should be lowercase; matching is case-insensitive
- Include at least one NIST AI RMF reference and one ISO/IEC 42001 reference per risk
