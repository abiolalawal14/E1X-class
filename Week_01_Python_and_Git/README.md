# Week 1 – Python Fundamentals & Version Control

Two 2-hour classes (1 hr slides + 1 hr practical) for Data Science / AI / ML students.
Storyline: **Nurse Maya and Dr. Kofi at a community health clinic** (global, made-up patients only).

| File | Use |
|---|---|
| `Day1_Python_Fundamentals.pptx` | Day 1 slides (26) – syntax, variables, data types, control flow, functions. Speaker notes on every slide. |
| `Day1_Practical_Guide.docx` | Day 1 step-by-step practical (Jupyter), Steps 0–10 + challenges |
| `Day1_Starter_Notebook.ipynb` | Day 1 notebook students fill in (hidden "reveal" code per step) |
| `Day2_Git_GitHub_Versioning.pptx` | Day 2 slides (28) – Git, GitHub, branches, pull requests. Speaker notes on every slide. |
| `Day2_Practical_Guide.docx` | Day 2 step-by-step practical (Git Bash + Jupyter + GitHub), Steps 0–12 + conflict bonus |
| `Day1_Tutor_Verbatim_Script.docx` | Word-for-word tutor script: all 26 slides + the 60-min practical, with DO / ASK / Listen-for cues |
| `Day2_Tutor_Verbatim_Script.docx` | Word-for-word tutor script: all 28 slides + the 60-min practical |
| `Week1_Quiz.docx` | Weekly quiz, 24 marks (16 MCQ + 4 short answer) |
| `Week1_Tutor_Answer_Key.docx` | Tutor only: Day 1 solutions, challenge answers, quiz answers & marking |

## Rebuilding
All files are generated from `build/` (theme: warm sunny pastels).

```
cd build
python build_day1.py
python build_day2.py
python build_docs.py      # also runs every Day 1 snippet and checks expected output
python build_notebook.py
python build_scripts.py   # verbatim tutor scripts
```
Day 1 practical content (code + expected output) lives in `build/day1_content.py`, which is shared by the guide, the notebook and the answer key.
