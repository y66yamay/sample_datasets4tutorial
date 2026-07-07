# bandit_MDD_BPD_bandit

Behavioural data (two-armed bandit task) from **Dezfouli et al. (2019)** for
unipolar depression (MDD), bipolar disorder (BD) and healthy controls (HC),
retrieved, validated and preprocessed into an analysis-ready tidy format.

- **Task:** two-choice probabilistic bandit (arms R1 / R2).
- **Cohort:** 101 subjects — MDD 34, BD 33, HC 34.
- **Design:** 12 sequences per subject (6 reward conditions × 2 halves) →
  1212 sequences, 132,251 trials total.

## Papers
- Dezfouli, Ashtiani, Ghattas, Nock, Dayan, Ong. *Disentangled behavioural
  representations.* NeurIPS 2019.
- Dezfouli et al. *Models that learn how humans learn: The case of
  decision-making and its disorders.* PLOS Computational Biology, 2019.

## Layout
```
data/
  raw/
    choices_diagno.csv.zip   # verbatim upstream file
    SOURCE.md                # provenance, links, license
  processed/
    trials.csv               # one row per trial (analysis ready)
    subjects.csv             # one row per subject (group + clinical scores)
scripts/
  preprocess.py              # reproducible raw -> processed
docs/
  data_dictionary.md         # column-by-column reference
  UPSTREAM_LICENSE_Apache-2.0.txt
```

## Reproduce
```bash
pip install pandas
python3 scripts/preprocess.py
```
This reads `data/raw/choices_diagno.csv.zip`, asserts the cohort sizes
(34/33/34 = 101) and the 12-sequence structure, and (re)writes the two
processed tables.

## Data source & license
Raw data was obtained from the authors' implementation repository
<https://github.com/adezfouli/rnn_hypercoder> (`data/BD/`, Apache-2.0). The
canonical dataset is also on Figshare (article `8257259`); see
[`data/raw/SOURCE.md`](data/raw/SOURCE.md) for links and licensing. Please cite
the papers above when using this data.

> Note: at retrieval time (2026-07-07) Figshare / NeurIPS / bioRxiv hosts were
> not reachable from the build environment's network policy, so the raw file was
> sourced from the GitHub mirror, which distributes the identical behavioural
> data. See `data/raw/SOURCE.md`.

See [`docs/data_dictionary.md`](docs/data_dictionary.md) for full column
definitions and analysis caveats.
