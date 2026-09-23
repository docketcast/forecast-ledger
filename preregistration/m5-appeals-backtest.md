# Pre-registration: M5 backtest (federal courts of appeals)

Written and published **before any M5 model was trained or scored**. Committed with a
signed commit and timestamped with OpenTimestamps (`m5-appeals-backtest.md.ots`).

- Evaluation code: private repository `docketcast/forecast`, commit
  `0c6c68552669a9daab6c0d91fb7552432c7f2b5a` (`src/forecast/appeals/`).

## Question

For argued civil appeals in the Second, Fifth and Ninth Circuits, can a model using facts
known at argument, including the three-judge panel, forecast whether the court affirms
better than the historical affirmance rate for that circuit and case type?

## What we had already seen

- Descriptive affirmance base rates for all circuits (published report: about 81% of merits
  decisions affirmed; counselled private civil appeals 62% when argued).
- Data coverage only: how many appeals link to CourtListener (80%), how many have a fully
  identified panel (61.5%), and how often the two panel sources agree (91.8%).
- **No model has been trained or scored, and no relationship between any feature and
  outcomes has been examined.**

## Data

- **Population** (fixed before any outcome analysis): appeals in the Second, Fifth and Ninth
  Circuits; civil (private or U.S. party), excluding prisoner petitions; appellant not
  pro se at filing; orally argued; not en banc; decided on the merits. Source: FJC
  Integrated Database, appeals file, snapshot 2026-06-30 (33,474 appeals).
- **Target:** affirmed (1) or not (0: reversed or vacated, or mixed).
- **Forecast time:** the argument date.
- **Panels:** from opinion headers and judge fields in CourtListener's public-domain data,
  judges identified with the FJC Biographical Directory.

## Features

Filing facts, known when the appeal is docketed: circuit; case type (private or U.S.
civil); nature-of-suit group; whether the United States is appellant or appellee;
district of origin; log days from docketing to argument. Trailing: the circuit and
case-type affirmance rate among appeals decided before the argument date (shrunk to
0.75 with weight 30).

Panel features (known from the argument calendar): number of judges appointed by a
Democratic president; number of visiting judges (not on the circuit at the time); and the
panel's mean affirmance record, where each judge's rate uses only panels decided before
the argument date, shrunk to the circuit and case-type rate with weight 20.

**Excluded as leak risks:** whether a panel is known for an appeal (it depends on whether
CourtListener holds the decision, which is related to publication and so to outcome); the
date the last brief was filed (its presence is recorded at termination); and publication
status, opinion type and judge involvement codes (known only after decision).

## Models (fixed; no tuning)

The same settings as M2: logistic regression (one-hot categories with fewer than 10 cases
pooled, standardised numerics, C = 0.5) and gradient boosting (depth 3, learning rate
0.05, 200 iterations, min 40 per leaf, L2 1.0, seed 0).

## Evaluation

- **Test years:** federal fiscal years 2014–2024 by argument date. For test year T, every
  model is trained only on appeals decided before 1 October of T−1.
- **Analysis A (primary):** appeals with a fully identified panel. Baseline: the
  circuit × case-type affirmance rate, fitted within the same subset.
  - **Primary comparison:** logistic regression with filing and panel features against
    that baseline, by Brier score pooled over test years; 95% interval from 2,000
    bootstrap resamples of whole fiscal years (seed 0).
  - **Success criterion:** the upper end of that interval is below zero.
  - **Secondary:** panel model against the filing-only model (what the panel adds); gradient
    boosting against the baseline; log loss; calibration; results by circuit.
- **Analysis B (secondary):** all appeals, filing features only, against the baseline.

## Known limitations, stated in advance

- Analysis A covers appeals whose decision is in CourtListener, which over-represents
  written opinions. Its results may not carry over to all appeals; live forecasts would
  get panels from court calendars for every argued appeal.
- The FJC file only contains appeals that have ended, so the latest test years
  under-represent slow appeals. This is why the test years stop at FY2024.

## Commitments

1. Results will be published on the scoreboard page whatever they show, labelled as a
   historical backtest.
2. No feature, model setting or test year will change after results are seen. Later
   analyses will be reported as exploratory and kept separate.
3. Bug fixes are allowed only if made without looking at M5 scores; any fix made after
   will be disclosed, and the pre-registered result reported as computed alongside it.
4. Live appeals forecasting starts only if the success criterion is met, and only after
   its own resolution rules are frozen and published.
