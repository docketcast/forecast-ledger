# Pre-registration: M7 backtest (oral argument transcripts)

Written and published **before any M7 model was trained or scored**. Committed with a
signed commit and timestamped with OpenTimestamps (`m7-transcripts-backtest.md.ots`).

- Evaluation code: private repository `docketcast/forecast`, commit
  `1f4d5fc86c55d61c6f780de7bdfcf5c052389acb` (`src/forecast/transcripts/`,
  `src/forecast/features/scotus.py`, `src/forecast/evaluate/backtest.py`).

## Question

After oral argument, does counting the justices' questions to each side improve on the
M2 model (which uses case and docket facts known before argument)?

## What we had already seen

- M1, M2 and M5 results (published).
- Transcript *format* only: parser checks that both sides' argument sections are found
  (50 transcripts from the 2000–2001 terms, all parsed) and that turn counts are plausible
  (median about 55 justice turns per side).
- **No relationship between transcript features and outcomes has been examined.**

## Data and timing

- Cases, labels and M2 features exactly as in the M2 pre-registration (terms 1988–2025,
  docket features from about 2000).
- Transcripts: supremecourt.gov argument transcripts, terms 2000–2025, read to compute
  features only (never republished).
- **Forecast time:** 14 days after argument, a conservative allowance for the years when
  transcripts were released some days after argument. Cases decided within 14 days of
  argument are excluded, since no post-argument forecast could have been made first.

## Features

M7 = the M2 features plus four transcript features, computed from justice speaking turns
(named justices, or "QUESTION" in older transcripts) during each side's argument time.
Amicus arguments count for the side they support; rebuttal is counted separately:

| Feature | Definition |
|---|---|
| `q_turn_ratio` | log((petitioner-side justice turns + 1) / (respondent-side justice turns + 1)) |
| `q_word_ratio` | the same ratio using justices' words |
| `q_total` | log(1 + all justice turns during both sides' arguments) |
| `q_rebuttal` | justice turns during the petitioner's rebuttal |

A case with no transcript gets zeros (no transcript flag is used).

## Models (fixed; no tuning)

M7 logistic regression and gradient boosting, same settings as M2, trained each test term
on earlier cases with a docket page, exactly as M2.

## Evaluation

- **Test terms:** 2008–2025, rolling origin, as M2.
- **Primary comparison:** M7 logistic regression against M2 logistic regression, by Brier
  score pooled over test terms, on the same cases; 95% interval from 2,000 bootstrap
  resamples of whole terms (seed 0).
- **Success criterion:** the upper end of that interval is below zero.
- **Secondary:** M7 against the historical base rate and the lower-court base rate; log
  loss; calibration; M7 gradient boosting against M2 gradient boosting; per-term results.

## Commitments

1. Results will be published on the scoreboard page whatever they show, labelled as a
   historical backtest.
2. No feature, model setting, lag or test period will change after results are seen.
   Later analyses will be reported as exploratory.
3. Bug fixes are allowed only if made without looking at M7 scores; any later fix will be
   disclosed, with the pre-registered result reported as computed alongside it.
4. If the criterion is met, M7 may be used for new post-argument forecasts (a separate
   `post_argument` checkpoint published after each argument). Published forecasts are never
   changed.
