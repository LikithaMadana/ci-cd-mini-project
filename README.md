# Hands-On CI/CD Mini Project

Goal: push this to a real GitHub repo and watch an actual pipeline run —
lint, test, Docker build, vulnerability scan, and a manual approval gate
before "deployment." This is the exact pipeline shape we discussed and
that you already described well in round 1.

Time: ~20-30 minutes.

---

## 1. Create a new GitHub repository

Go to https://github.com/new
- Name it anything, e.g. `ci-cd-mini-project`
- Keep it Public (Trivy action + Actions minutes are free on public repos)
- Do NOT initialize with a README (we already have one)

---

## 2. Push this project to it

Unzip this project, then in a terminal inside the folder:

```bash
cd ci-cd-mini-project
git init
git add .
git commit -m "Initial commit: CI/CD mini project"
git branch -M main
git remote add origin https://github.com/<your-username>/ci-cd-mini-project.git
git push -u origin main
```

---

## 3. Watch the pipeline run

Go to your repo on GitHub → click the **Actions** tab.

You'll see a workflow run start automatically (triggered by the push to
main). Click into it. You'll see three jobs running in sequence:

1. **lint-and-test** — installs dependencies, runs Ruff, runs pytest
2. **build-image** — builds the Docker image, scans it with Trivy
3. **deploy** — will be PAUSED here, waiting for manual approval

---

## 4. Set up the manual approval gate (do this once)

The `deploy` job uses `environment: production`, which is what creates
a real approval gate — exactly what we discussed as Stage 7 in the full
pipeline walkthrough.

To make GitHub actually pause and require your approval:
1. Go to your repo → **Settings** → **Environments**
2. Click **New environment**, name it exactly `production`
3. Under **Deployment protection rules**, check **Required reviewers**
4. Add yourself as a required reviewer
5. Save

Now re-run the pipeline (push any small change, or go to Actions → click
"Re-run all jobs" on the last run). This time, when it reaches the
`deploy` job, it will actually pause and show a "Review deployments"
button — click it, approve, and watch the deploy step run.

**This is the exact mechanic behind "manual approval gate before
production" that you've been describing in interview answers — now
you've actually triggered and approved one yourself.**

---

## 5. Watch it FAIL (just as valuable as watching it pass)

1. Open `tests/test_deliberately_broken.py.example`
2. Rename it to `test_deliberately_broken.py` (remove `.example`)
3. Commit and push:
   ```bash
   git add .
   git commit -m "Add a deliberately failing test"
   git push
   ```
4. Go to Actions — watch the `lint-and-test` job fail at the pytest step
5. Click into the failed step and read the actual pytest output — this
   is exactly what you'd see in a real "pipeline is failing" scenario

To fix it and watch it go green again, either delete that file or fix
the assertion, then commit and push again.

---

## 6. Look at the Trivy scan output

In the `build-image` job, click the "Scan image for vulnerabilities"
step. Even a small Python base image usually has a few known CVEs
listed — this is a good, honest look at what a real vulnerability scan
report actually looks like (severity, package name, CVE ID).

Note: `exit-code: "0"` in the workflow means findings are shown but
don't fail the pipeline. Change it to `"1"` in
`.github/workflows/ci-cd.yml` if you want to see it actually BLOCK the
pipeline on critical/high findings — that's the stricter, more
realistic setting for a production banking pipeline.

---

## What you should be able to say fluently after this

- "I've actually watched a GitHub Actions pipeline run end to end —
  lint, test, Docker build, vulnerability scan, and a manual approval
  gate using GitHub Environments with required reviewers."
- "I've seen a real Trivy vulnerability scan report and understand what
  the severity levels actually look like in practice."
- "I've deliberately broken a test and watched the pipeline correctly
  fail and block at the right stage, then fixed it and watched it pass."

Same principle as the Kubernetes mini project — this turns pipeline
concepts from something you can describe into something you've actually
triggered, approved, and debugged yourself.
