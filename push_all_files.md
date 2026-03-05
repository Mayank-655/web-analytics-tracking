# Push all project files to GitHub

Only README was pushed because the other files weren't committed. Fix it:

## In PowerShell or Command Prompt

```powershell
cd "C:\Users\msk24\Data Science Projects\web-analytics-tracking"

# Add everything (docs, scripts, sql, .gitignore, run_funnel.bat, etc.)
# Dataset CSVs are ignored by .gitignore so they won't be added
git add .

# See what will be committed (should list docs/, scripts/, sql/, etc.)
git status

# Commit
git commit -m "Add docs, scripts, SQL, and run_funnel script"

# Push
git push origin main
```

After this, refresh the GitHub page — you should see the `docs/`, `scripts/`, `sql/` folders and other files.
