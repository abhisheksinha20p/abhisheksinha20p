# Setup

1. **Merge to `main`** of the `abhisheksinha20p/abhisheksinha20p` repo.
2. **Repo → Settings → Actions → General → Workflow permissions → Read and write**, then save. The workflows commit assets and push the `output` branch.
3. **Actions tab → run "Profile assets" and "Contribution snake" once** (they also run on every push to `main`, then every 6 / 12 hours). Until they finish, the language radar, stats card and snake images show as broken.
4. *(Optional)* Add a classic PAT with `read:user` as the repo secret `METRICS_TOKEN` so the activity panel and stats include private contributions.
5. Edit `assets/skills.json` (self-rated radar, currently placeholder values) and `assets/projects.json` (add `"repo": "<name>"` to a project for live stars/forks).
6. Put your photo at `assets/me.jpg` and run `pip install Pillow && python scripts/hologram.py --photo assets/me.jpg`, then commit `assets/hologram.svg`.

Preview offline: `python scripts/activity.py --demo` and `python scripts/hologram.py`.
