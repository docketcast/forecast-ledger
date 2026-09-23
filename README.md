# Appellate forecast ledger

A public, append-only record of probability forecasts for US appellate cases,
each published **before** the ruling. Its purpose is a track record anyone can
verify: that each forecast existed before the decision, and that none has been
edited or removed since.

**Scoreboard:** https://docketcast.github.io/forecast-ledger/ (rebuilt from this
repository in every publishing commit; source in `docs/`).

**Informational only.** Nothing here is legal, financial, trading or investment
advice, or a recommendation to take any action.

## Files

| File | Contents |
|---|---|
| `forecasts.jsonl` | One forecast per line. Never edited; new forecasts are appended. |
| `resolutions.jsonl` | How each forecast resolved, and under which rule. |
| `resolution_rules.yaml` | The current rules for resolving forecasts, fixed before publication. |
| `resolution_rules_v<N>.yaml` | Every frozen version. Each forecast records the version it is resolved under. |
| `batches/*.txt`, `*.ots` | Record hashes for each publishing batch, with OpenTimestamps proofs. |
| `verify.py` | Hash-chain verifier (Python standard library only). |

Each forecast records the case, checkpoint (`cert_granted`, `briefs_filed`,
`post_argument`), UTC timestamp, probability, target, model version, feature
snapshot hash, code commit and resolution-rules version.

## How to verify

1. **Nothing edited or removed:** `python verify.py forecasts.jsonl resolutions.jsonl`.
   Each record contains the SHA-256 hash of the one before it, so any change to
   an earlier record breaks every later hash.
2. **Existed before the ruling:** each batch's `.ots` file anchors its record
   hashes in the Bitcoin blockchain. Run `ots verify batches/<file>.txt.ots`
   ([OpenTimestamps](https://opentimestamps.org)) and compare the attested time
   with the decision date. Check the record's hash is listed in that batch file.
3. **Who published it:** commits are signed; GitHub shows them as verified.

## Rules versions

- **v1** (frozen 2026-09-23 16:28:39 UTC) applies to the October 2026 forecasts.
- **v2** changes no scoring rule. It names the Court's docket judgment entry as the
  automated check (v1 named CourtListener, whose API needs a commercial agreement for
  this use) and states the unit as one argued case resolved by its lead docket. See
  `changes_from_v1` in the v2 file.

For forecasts under v1, the outcome still comes from the slip opinion's judgment line
and is cross-checked against the docket. CourtListener's website is also checked by
hand before each v1 resolution is published, and the resolution record says so. None
of the v1 cases is consolidated, so the unit wording makes no difference to them.

## Scoring

Resolved forecasts are scored with the Brier score and log loss, and compared with
historical base rates. Results are reported whether or not they are favourable.
