# Pre-registration: M2 backtest (docket features)

Written and published **before any M2 result was computed**. This file is committed with
a signed commit and timestamped with OpenTimestamps (`m2-backtest.md.ots`), so anyone
can confirm it existed before the results it describes.

- Evaluation code: private repository `docketcast/forecast`, commit
  `db5296b850bec2fb2d72bddb45ab5f48b8f4b40c` (model definitions in `src/forecast/models/zoo.py`, features in
  `src/forecast/features/`, backtest in `src/forecast/evaluate/backtest.py`).
- Resolution and labelling rules: `resolution_rules_v2.yaml` in this repository (the
  scoring rules are identical in v1 and v2).

## Question

Do features from the Supreme Court's docket, knowable before oral argument, improve
forecasts of whether the petitioner wins over (a) the historical base rate and (b) the
M1 model, which uses only case-caption features?

## What we had already seen

So that readers can judge this plan fairly:

- The M1 backtest results, which will be published together with M2 (no model beats the base rate; best Brier
  difference −0.0014, 95% interval [−0.0062, +0.0035], test terms 2008–2025).
- Docket feature *values* (not outcomes or scores) for about 40 cases, while testing
  the parser, and whether the docket judgment agrees with the opinion-text label for
  223 cases (99.5% agreement), while building the resolver.
- **No M2 model has been trained or scored, and no relationship between docket features
  and outcomes has been examined.**

## Data

- **Cases:** argued merits cases, October Terms 1988–2025, one per argued case (lead
  docket), from CourtListener's public-domain bulk data (snapshot 2026-06-30). Cases whose
  outcome label is held for manual review are excluded, as in M1.
- **Label:** petitioner wins (1) if the judgment is reversed or vacated in whole or part;
  0 if affirmed (including by an equally divided Court) or the writ is dismissed.
- **Forecast time (`as_of`):** the argument date.
- **Docket features:** from supremecourt.gov docket pages (available for dockets from about
  2000), using only entries dated **strictly before** `as_of`.

## Features

M2 = the nine M1 features plus nine docket features:

| Feature | Definition |
|---|---|
| `us_party` | Federal government (United States, a federal agency or officer) is petitioner, respondent, both or neither, from the docket title |
| `sg_amicus_side` | Side the United States supported as amicus at the merits stage (`party` if it is a party; `none` if no brief) |
| `cvsg` | Court invited the Solicitor General's views before granting review |
| `n_amicus_cert` | Amicus briefs filed before the grant |
| `n_amicus_pet`, `n_amicus_resp`, `n_amicus_neither` | Merits-stage amicus briefs by side. Side is taken from the entry text if stated; otherwise from the Rule 37.3 deadlines: filed after the respondent's merits brief supports the respondent, otherwise the petitioner |
| `amicus_balance` | log(1 + petitioner-side briefs) − log(1 + respondent-side briefs) |
| `days_grant_to_as_of` | Days from the grant to `as_of` |

## Models (fixed; no tuning)

- **M2 logistic regression** (primary): one-hot categoricals (categories with fewer than
  10 cases pooled), standardised numerics, L2 penalty C = 0.5.
- **M2 gradient boosting** (secondary): scikit-learn HistGradientBoosting, depth 3,
  learning rate 0.05, 200 iterations, min 40 samples per leaf, L2 1.0, seed 0.
- Both are trained, for each test term T, on cases from terms before T that have a docket
  page. Baselines and M1 models are trained exactly as in M1.

## Evaluation

- **Test terms:** 2008–2025, rolling origin (train on all earlier terms only).
- **Primary comparison:** M2 logistic regression against the historical base rate (all
  prior terms), by Brier score, pooled over test terms. 95% interval from 2,000 bootstrap
  resamples of whole terms (seed 0).
- **Success criterion:** the upper end of that interval is below zero.
- **Secondary:** M2 logistic regression against the lower-court base rate and against M1
  logistic regression; log loss; calibration (expected calibration error, reliability
  diagram); M2 gradient boosting against the same references; per-term scores.
- **Sensitivity analysis:** the same comparisons with labels corrected where the Court's
  docket judgment disagrees with the opinion-text label. The primary analysis uses the
  original labels.

## Commitments

1. The results will be published on the scoreboard page whatever they show, alongside M1,
   labelled as a historical backtest.
2. No feature, model setting or test period will be changed after seeing results. Any later
   analysis will be reported as exploratory and clearly separated from this one.
3. Bug fixes to data parsing are allowed only if made without looking at M2 scores, and
   every one will be listed in the report.
4. M2 replaces M1 as the published primary model for **future** forecasts only if the
   success criterion is met. Published forecasts are never changed.
