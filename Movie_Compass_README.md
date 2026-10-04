# Movie Compass Recommendation Project

Download **Movie_Compass_Source.zip**, extract it, and follow `recommendation_system/README.md`. It includes the complete source tree, MovieLens data with its original terms, pinned dependencies, tests, evaluation results, and foundation-project attribution. The archive does not contain credentials or a virtual environment.

**Movie_Compass_Report.docx** is the APA report with six body pages, a title page, and two reference pages.

Developed for James Ristine, MSAI-631-A02, October 4, 2026.

The local GUI uses genre TF-IDF and cosine similarity, with explanations, multiple favorites, filters, and hide/undo controls. All 22 automated tests passed. The offline evaluation is intentionally reported with its limitations: only 28 users qualified, and this genre-only model did not outperform the popularity baseline.

To run after extracting:

```powershell
cd recommendation_system
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5055. No API key is needed. Installation requires internet; the app works offline afterward.
