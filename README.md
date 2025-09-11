# meta_repair_system (Oxord)

Starter repo for Oxord Computer Solutions — Odoo Community custom module development.

Contents:
- addons/oxord_repair/    -> Custom repair module skeleton (models, views, security)
- docker-compose.yml      -> Quick dev docker-compose (Odoo + Postgres) for local testing
- .gitignore
- LICENSE (AGPL-3)

Quick start (Docker, recommended):
1. Unzip this project to C:\meta_dev
2. Install Docker Desktop and enable WSL2 backend (Windows)
3. From the repo root (C:\meta_dev) run:
   docker compose up -d
4. Open http://localhost:8069 to access Odoo. Custom modules path is mounted at ./addons.

Quick start (Git + local clone to GitHub):
1. Install Git for Windows: https://git-scm.com/downloads
2. Configure git:
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
3. Optionally generate SSH key (use Git Bash):
   ssh-keygen -t ed25519 -C "you@example.com"
   copy the public key to GitHub > Settings > SSH and GPG keys
4. Create a repository on GitHub (website or gh cli) named `meta_repair_system`
5. In PowerShell or Git Bash:
   cd C:\
   mkdir meta_dev
   cd meta_dev
   git init
   (copy project files into this folder)
   git add .
   git commit -m "Initial commit: repo skeleton and oxord_repair module"
   git remote add origin git@github.com:YOUR_USERNAME/meta_repair_system.git
   git branch -M main
   git push -u origin main

See docs and Odoo official docs for more details on running Odoo from source or deploying to production.
