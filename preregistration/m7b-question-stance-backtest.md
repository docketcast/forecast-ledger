# Pre-registration: M7b backtest (stance of the justices' questions)

Written and published **before our question classifier was trained and before any stance
feature was compared with outcomes**. Committed with a signed commit and timestamped with
OpenTimestamps (`m7b-question-stance-backtest.md.ots`).

- Code: private repository `docketcast/forecast`, commit
  `96c65e29862a8a954cfc613a2c7751ef6652a079` (`src/forecast/transcripts/questions.py`,
  `src/forecast/transcripts/stance_model.py`, `src/forecast/llm/`,
  `src/forecast/features/scotus.py`, `src/forecast/evaluate/backtest.py`).

## Question

M7 found that *how many* questions the justices ask each side does not improve on M2. Does
*what kind* of questions they ask (whether they challenge or help the lawyer arguing)
improve on M2 after oral argument?

## What we had already seen

- M1, M2, M5 and M7 results (published).
- Question labels from a large language model (about a quarter of the 20,000-question
  sample was labelled at publication; labelling continues unchanged), and a trial of three
  models on 200 questions: about two-thirds were labelled "challenges", a quarter
  "neutral" and a few percent "supports".
- How many cases were decided after the labelling model's knowledge cutoff (29).
- **No relationship between question stance and case outcomes has been examined.** Labels
  were produced and inspected without outcome data.

## Data

- Cases, labels, M2 features, test terms and the 14-day post-argument forecast time exactly
  as in the M7 pre-registration. Cases decided within 14 days of argument are excluded.
- Transcripts: supremecourt.gov, terms 2000–2025, 1,769 transcripts, 190,995 justice
  questions (turns of at least five words during a side's argument or rebuttal, excluding
  the presiding justice's hand-offs). Read to compute features only; never republished.

## Labels

- **Labeller:** OpenAI `gpt-6-astra`, reasoning effort "low", via the Batch API, September
  2026. OpenAI offers no dated snapshot of this model; the model string returned with every
  label is stored. Knowledge cutoff stated by OpenAI: 30 April 2026.
- **What it saw:** one justice turn plus the end of counsel's preceding answer. Lawyers'
  names, docket numbers and the words of the case name were replaced, and **which side was
  being questioned was withheld**. It labelled the question's stance toward whoever was
  arguing: `challenges`, `neutral` or `supports`.
- **Sample:** 20,000 questions spread evenly over terms 2000–2025 (seed 20260926).
- Questions whose label request failed are retried once; any still missing are left
  unlabelled.

## Our classifier

- ModernBERT-large (Apache-2.0) fine-tuned on the labels with fixed settings (learning rate
  2e-5, 2 epochs, batch 16, up to 384 tokens, seed 0). No tuning.
- **Cross-fitted by transcript:** transcripts fall into five fixed folds (hash of the
  transcript path); each fold's questions are scored by a model trained only on labelled
  questions from the other four folds.
- **Quality gate (checked before any outcome is used):** out-of-fold agreement with the
  labeller must be at least 75%, and above the share of the most common label. If the gate
  fails, the backtest is not run and that is published.

## Features

M7b = the M2 features plus three stance features, from the classifier's probabilities for
each question. Rebuttal counts for the petitioner; a reargued case uses its last argument:

| Feature | Definition |
|---|---|
| `stance_chal_diff` | mean P(challenges) of questions to the petitioner's side minus the same for the respondent's side |
| `stance_supp_diff` | the same for P(supports) |
| `stance_chal_ratio` | log((sum of P(challenges), petitioner side + 1) / (the same, respondent side + 1)) |

A case with no transcript, or with questions to only one side, gets zeros.

## Models (fixed; no tuning)

M7b logistic regression and gradient boosting, same settings as M2 and M7, trained each
test term on earlier cases with a docket page.

## Evaluation

- **Test terms:** 2008–2025, rolling origin.
- **Primary comparison:** M7b logistic regression against M2 logistic regression, by Brier
  score pooled over test terms, on the same cases; 95% interval from 2,000 bootstrap
  resamples of whole terms (seed 0).
- **Success criterion:** the upper end of that interval is below zero.
- **Secondary:** M7b against the historical base rates; log loss; calibration; M7b gradient
  boosting against M2 gradient boosting; per-term results; the classifier's agreement by
  class.

## Contamination checks

The labeller may remember how past cases were decided. Its labels could then lean toward
the eventual winner, and the backtest would overstate the gain.

1. **Recall test.** For every case in the test terms (2008–2025), the labeller is asked,
   with only the case name, docket number and term, whether the petitioner or respondent
   prevailed and whether it recognises the case. Its accuracy is compared with always
   answering "petitioner" (95% interval from 2,000 resamples of whole terms, seed 0).
   **Contamination is "detected" if the lower end of that interval is above zero.**
2. **After the cutoff.** M7b against M2 on the 29 cases decided after 30 April 2026,
   reported descriptively (too few cases for a test).

## Commitments

1. Results, including the gate and the contamination checks, will be published on the
   scoreboard page whatever they show, labelled as a historical backtest.
2. No feature, model setting, label, prompt or test period will change after results are
   seen. Later analyses will be reported as exploratory.
3. Bug fixes are allowed only if made without looking at M7b scores; any later fix will be
   disclosed, with the pre-registered result reported as computed alongside it.
4. **Adoption:**
   - If the criterion is met and contamination is **not** detected, M7b may be used for new
     post-argument forecasts (a separate `post_argument` checkpoint published after each
     argument).
   - If the criterion is met but contamination **is** detected, M7b is published only as a
     benchmark alongside M2's post-argument forecasts for the whole of OT2026, and adopted
     only if it beats M2 on that live record. Live forecasts cannot be contaminated: their
     outcomes do not exist yet.
   - Published forecasts are never changed.
