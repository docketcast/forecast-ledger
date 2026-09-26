# Pre-registration: M7c backtest (question stance, time-ordered classifier)

Written and published **before any M7c classifier was trained or any M7c result was
computed**. Committed with a signed commit and timestamped with OpenTimestamps
(`m7c-time-ordered-stance-backtest.md.ots`).

- Code: private repository `docketcast/forecast`, commit
  `758d435a7dc5f13e74998cc5f72a1820c2a256cc` (`stance_model.rolling`, `forecast stance-rolling`,
  `forecast evaluate --milestone m7c`).

## Why this analysis exists (designed after seeing M7b)

**This analysis was designed after the M7b results were known.** It is pre-registered so
that its settings are fixed before its own results exist, but readers should weigh it
accordingly.

M7b (pre-registered) met its criterion: Brier −0.0139 [−0.0196, −0.0082] against M2. Its
contamination check then showed that the labelling model (`gpt-6-astra`) names the winner
of 99.1% of past cases from the case name alone (781 of 1,103 cases asked before the
account's credit ran out). Its labels may therefore lean toward the eventual winner.

In M7b our classifier was cross-fitted by transcript, so a model scoring a 2010 case had
learned from labels on 2011–2025 cases. If those labels encode outcomes, later outcomes
reached earlier forecasts. **That design choice was ours, and it was a mistake.**

M7c removes that path. Each term's questions are scored by a classifier trained only on
labels from cases **decided before that term began**. Labels that encode earlier outcomes
are then no worse than knowing earlier outcomes, which any forecaster may use.

## What we had already seen

Everything in the M7b results: gate, backtest, recall test, and the 28 cases decided after
the labeller's cutoff (M7b − M2: −0.026). No M7c classifier has been trained.

## Design (everything else exactly as M7b)

- **Labels, questions, features, outcome models, test terms (2008–2025), forecast time and
  evaluation:** identical to the M7b pre-registration. Same 20,000 labels; no new labelling.
- **Classifier training:** for each argument term *t* from 2000 to 2025, a ModernBERT-large
  classifier (M7b's fixed settings) is trained on the labelled questions whose case was
  decided before 1 October of year *t*, then scores every question argued in term *t*.
  - A docket's decision date is the earliest decision under that docket number in our case
    table. Labelled questions with no decision date (769 of 20,000) are never used.
  - A reargued case's first-argument labels are unavailable until it has been decided.
  - Terms with fewer than 100 eligible labels are not scored; their cases get zero stance
    features (term 2000 only).
- **Outcome models:** trained each test term on earlier cases, as in M7b. Every case's
  stance features come from the classifier for its own argument term, so no feature
  anywhere depends on a label about a case decided after that term began.

## Evaluation

- **Primary comparison:** M7c logistic regression against M2 logistic regression, Brier
  score pooled over test terms 2008–2025, same cases; 95% interval from 2,000 bootstrap
  resamples of whole terms (seed 0).
- **Success criterion:** the upper end of that interval is below zero.
- **Secondary:** M7c against M7b (how much of M7b's gain survives time ordering); M7c
  gradient boosting against M2 gradient boosting; M7c against the base rates; log loss;
  calibration; per-term results; the 28 cases decided after the labeller's cutoff
  (descriptive).
- A known issue, disclosed with M7b, is kept as is for comparability: two cases appear
  twice in the case table. Results without the duplicates are reported alongside.

## Commitments

1. Results will be published on the scoreboard page whatever they show.
2. No setting will change after results are seen; later analyses are exploratory.
3. Bug fixes only without looking at M7c scores; any later fix disclosed, with this result
   as computed.
4. **Adoption** (this replaces M7b's adoption rule, for the reason above):
   - If M7c meets its criterion, the stance model (classifier trained on all labels,
     scoring new transcripts locally) may be used for new post-argument forecasts, published
     as a separate `post_argument` checkpoint alongside M2's.
   - If it does not, stance forecasts are published only as a benchmark alongside M2's
     post-argument forecasts for OT2026, and adopted only if they beat M2 on that live record.
   - Published forecasts are never changed.
