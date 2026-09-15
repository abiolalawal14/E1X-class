# Instructor Guide — 2-Hour Delivery Plan

**Course:** Unsupervised Learning — Anomaly Detection Systems
**Audience:** Beginner Data Scientists (comfortable with Python, Pandas, basic ML)
**Format:** Hour 1 conceptual (slides), Hour 2 hands-on (Jupyter notebooks)

The whole session is one connected story: *"We have a bank with thousands of transactions.
We don't have labels for every transaction. How can we teach a machine to find unusual
behaviour?"* Keep returning to that framing — this is not a tour of separate algorithms.

---

## Before class

- Open `Unsupervised_Learning_Anomaly_Detection_Systems_Beginner_Course.pptx` in Google Slides
  or PowerPoint and skim speaker notes once.
- Confirm `data/bank_transaction_anomaly_dataset.csv` exists (regenerate with
  `python data/generate_data.py` if needed — it's deterministic, `random_state=42`).
- Have `notebooks/01`, `02`, `03` open and pre-run once so you're not debugging live.
- Decide whether students code along in real time or watch you build 02/03 and then do
  `exercises/anomaly_detection_exercise.ipynb` themselves — the timing below assumes the latter.

---

## Hour 1 — Concepts (Slides 1–34)

| Time | Slides | Focus |
|---|---|---|
| 0–10 min | 1–4 | Title, learning objectives, the real-life scenario, the labeling challenge |
| 10–20 min | 5–9 | What is an anomaly? Normal vs. anomalous. Supervised vs. unsupervised. How do we learn "normal"? Types of anomalies overview |
| 20–30 min | 10–13 | Point / contextual / collective anomalies in depth. The basic idea (data → learn normal → score → flag) |
| 30–40 min | 14–17 | The five approaches overview. Statistical, distance-based, density-based methods |
| 40–52 min | 18–27 | Isolation Forest: intuition, isolation visuals, algorithm steps, ensembles, parameters, contamination, anomaly score, predict(), business action |
| 52–60 min | 28–34 | Other methods table, choosing an approach, evaluation, final mental model, misconceptions, quiz, references |

**Pacing notes:**
- Slides 3 (real-life scenario) and 18–20 (isolation visuals) are the two moments worth
  slowing down for — they're where intuition actually forms. Don't rush them to protect time
  elsewhere.
- If you're behind schedule, the safest slides to compress are 14–17 (approaches overview) —
  read the bullets briskly, since Isolation Forest gets the deep treatment anyway.
- Run the Slide 33 quiz as a quick group call-and-response rather than individual writing, to
  keep it inside the 60-minute mark. Full answer key is in that slide's speaker notes.

---

## Hour 2 — Hands-On Coding

| Time | Activity | Notebook |
|---|---|---|
| 60–70 min | Load and explore the dataset | `notebooks/01_Anomaly_Detection_Introduction.ipynb` |
| 70–80 min | Feature selection and preprocessing | `notebooks/02_Isolation_Forest.ipynb` (steps 1–5) |
| 80–95 min | Build Isolation Forest, generate predictions | `notebooks/02_Isolation_Forest.ipynb` (steps 6–10) |
| 95–105 min | Detect and visualize anomalies, interpret results | `notebooks/03_Anomaly_Detection_Mini_Project.ipynb` (pipeline + investigation) |
| 105–115 min | Mini challenge (contamination comparison) | `notebooks/03_Anomaly_Detection_Mini_Project.ipynb` (mini challenge section) |
| 115–120 min | Recap + hand off capstone | `exercises/anomaly_detection_exercise.ipynb` (assign as take-home) |

**Delivery notes:**
- All three main notebooks have been executed end-to-end with no errors under the current
  scikit-learn version — you should not hit install or environment surprises live.
- The mini challenge (`03`, contamination sweep) has real numbers already computed on this
  dataset: `contamination=0.01` → 51 flagged, 0 false positives; `0.03` → 151 flagged, 4 false
  positives; `0.05` → 251 flagged, 97 false positives; `"auto"` → 456 flagged, 302 false
  positives. Use these to anchor the discussion if a live re-run behaves unexpectedly.
- `exercises/anomaly_detection_exercise.ipynb` is intentionally incomplete (`# TODO` cells with
  `...` placeholders) — it will NOT run as downloaded. That's by design: assign it as the
  30–45 minute capstone to complete after class, or as a guided in-class exercise if time
  allows. `solutions/anomaly_detection_exercise_solution.ipynb` is the fully worked, executed
  reference.
- Close Hour 2 by returning explicitly to the business-interpretation workflow (Slide 27 /
  Notebook 03's final section): flagged transactions require investigation, not automatic
  action. This is the single message you want students to leave with above all the code.

---

## Common questions to anticipate

- **"Why not just use a fixed threshold on transaction_amount?"** — Bring back the contextual
  anomaly example (Slide 11): a single global threshold misses anomalies that are only unusual
  in combination with other features (unusual hour + unusual distance), and it can't adapt to
  different customer segments (business vs. retail).
- **"Why Isolation Forest and not One-Class SVM or LOF?"** — It's fast, needs little tuning,
  handles multiple features naturally, and its core idea explains with a picture instead of a
  formula — appropriate for a first session. Slide 28 covers when you'd reach for the others.
- **"Isn't a 3% false-fraud rate still a lot of people?"** — Yes, and that's the point of the
  business-action slide (27): flagged ≠ guilty. This is exactly why investigation, not
  automatic blocking, is the recommended next step.
