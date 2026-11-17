# Week 3 – Preparing Data & Building Pipelines

Two 2-hour Zoom classes (1 hr slides + 1 hr practical). The story continues: the district funded a follow-up programme, but a third of patients don't come back. **Nurse Maya and Dr. Kofi** want to predict who will miss, so Maya can phone them first. This is the students' first week of machine learning. All data is made up.

- **Day 1:** Handling Missing Data and Preparing Features, Tue 17 Nov, 7:00 PM WAT
- **Day 2:** Cross-Validation and ML Pipelines, Sat 21 Nov, 1:00 PM WAT

| File | Use | Share with students? |
|---|---|---|
| `Day1_Handling_Missing_Data_and_Preparing_Features.pptx` | Day 1 slides (26), with speaker notes | Optional |
| `Day1_Practical_Guide.docx` | Day 1 step-by-step practical, Steps 0–10 + challenges | Yes |
| `Day1_Starter_Notebook.ipynb` | Day 1 notebook students fill in | Yes |
| `followup_visits.csv` | Data for **both** practicals (raw, with gaps) | Yes |
| `Day2_Cross_Validation_and_ML_Pipelines.pptx` | Day 2 slides (28), with speaker notes | Optional |
| `Day2_Practical_Guide.docx` | Day 2 step-by-step practical, Steps 1–10 + challenges | Yes |
| `Day2_Starter_Notebook.ipynb` | Day 2 notebook students fill in | Yes |
| `Week3_Quiz.docx` | Weekly quiz, 24 marks | Yes |
| `Week3_Exercises_Feature_Prep.ipynb` | ALX-style exercises, 40 marks | Yes |
| `Week3_Exercises_CV_Pipelines.ipynb` | ALX-style exercises, 35 marks | Yes |
| `immunisation_households.csv` | Data for the exercises | Yes |
| `Day1_Tutor_Verbatim_Script.docx`, `Day2_Tutor_Verbatim_Script.docx` | Word-for-word tutor scripts | **No** |
| `Week3_Tutor_Answer_Key.docx` | Solutions, quiz answers, marking guide | **No** |
| `Week3_Exercises_Solutions_TUTOR.ipynb` | Executed exercise solutions | **No** |

## How the week bridges into machine learning

Weeks 1–2 never showed a model, so Week 3 introduces the ideas as it needs them:

- **Day 1** opens with "what is a model, features and a target", prepares the data, and ends by training one simple model (k-nearest neighbours) with and without scaling: 69.4% → 75.0%.
- **Day 2** opens with train/test split, fit/predict/score and a lazy baseline (68.8%), then shows that one split can be lucky (74.3% vs a cross-validated 67.7%), names Day 1's leak, and fixes it with a pipeline (78.0%, final test 78.5%).

## Rebuilding

```
cd build
python make_data.py        # only if you want to regenerate the data
python build_day1.py
python build_day2.py
python build_docs.py
python build_notebooks.py
python build_scripts.py
```

Practical code and outputs live in `day1_content.py` and `day2_content.py`, and every expected output is captured by running the code. Slide speaker notes and the Word tutor scripts share one source: `script_day1.py` and `script_day2.py`. The Day 2 deck quotes scores from `day2_content.py`; if you regenerate the data, re-run that file and update the numbers in `build_day2.py` and the scripts.
