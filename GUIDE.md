# Practical 09 – Continuous Testing with GitHub Actions (instead of Jenkins)

Project: library lending system (`library.py`) with 8 PyTest cases (`test_library.py`).
Pipeline: `.github/workflows/ci.yml`. Repo: https://github.com/anshul755/library-ci

## Steps
1. Create a public GitHub repo (done: `library-ci`).
2. Push the project:
   ```
   git init
   git add .
   git commit -m "Initial project: library lending + tests"
   git branch -M main
   git remote add origin https://github.com/anshul755/library-ci.git
   git push -u origin main
   ```
3. Open the repo -> **Actions** tab -> run "Continuous Testing" starts by itself. Open it to see
   Checkout, Setup Python, Install Dependencies, Run Tests. Green tick = 8 passed. **Screenshot.**
4. Defect demo: in `library.py` change `queue.pop(0)` to `queue.pop()`, then
   ```
   git commit -am "Introduce defect: waiting list served LIFO"
   git push
   ```
   Actions shows a red cross; open "Run Tests" to see `test_return_hands_book_to_first_in_queue` fail
   (`'meera' == 'ravi'`). **Screenshot.**
5. Fix: change back to `queue.pop(0)`, then
   ```
   git commit -am "Fix: waiting list is FIFO again"
   git push
   ```
   Green tick again. **Screenshot.**

## Mapping to the PDF
| PDF (Jenkins) | This practical (GitHub Actions) |
|---|---|
| Jenkins job / Jenkinsfile | `.github/workflows/ci.yml` |
| Checkout stage | `actions/checkout` step |
| Install Dependencies | `pip install -r requirements.txt` |
| Run Tests | `pytest -v` |
| Build #N, SUCCESS/FAILURE | Run #N, green tick / red cross |
| Build Now / webhook | Automatic trigger on every `git push` |
| Runs on student laptop | Runs on GitHub's cloud machine (`ubuntu-latest`) |
