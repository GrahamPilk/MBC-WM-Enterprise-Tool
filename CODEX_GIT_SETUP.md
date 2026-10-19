# MBC-wm-ai: Git + GitHub setup with Codex

> **Status (19 Oct 2026):** the repo now exists, but not the way this plan describes. It's **public** at `GrahamPilk/MBC-WM-Enterprise-Tool`, under Graham's personal account rather than an org, with `main` as the default branch. Wherever this doc says `<ORG>/<REPO>`, read `GrahamPilk/MBC-WM-Enterprise-Tool`. Part A steps 1 and 3-6 are effectively done, though without `.gitignore`, `.gitattributes`, `README.md` or the `docs/` move. Branch protection, the merge settings and team access (steps 7-9) haven't been confirmed. The team's agent rules live in `Agents.md` at the repo root.

**Chosen approach:** one **private GitHub repo** owned by a **GitHub Organization**. Everyone signs in with the **GitHub CLI (`gh`)**, which handles HTTPS credentials, so nobody has to manage SSH keys. Work happens on short-lived **feature branches** that merge into a **protected `main`** through **pull requests**.

Why this setup:
- Codex works best with GitHub. Codex cloud tasks connect to GitHub repos through the ChatGPT GitHub connector.
- `gh` works the same on Windows, macOS and Linux.
- Branch protection stops anyone, human or agent, from pushing straight to `main`.

Placeholders to replace before sharing:
- `<ORG>`: the GitHub organization name, e.g. `mbc-wm-ai`.
- `<REPO>`: the repository name, e.g. `ai-native-enterprise-agent`.

---

## Part A: Tech lead, one-time setup (Graham)

Do these in the GitHub web UI first. They take about 5 minutes.
1. Create a free organization at https://github.com/organizations/new and name it `<ORG>`.
2. Invite each teammate by their GitHub username. Create a team `engineers` and give it **Write** access.

Then paste this into Codex, run from the `MBC-wm-ai` folder:

```text
You are setting up the central Git repository for our team project. Work in the current folder.
Explain each command before running it, and stop and ask me if anything fails.

1. Check that git and the GitHub CLI are installed (`git --version`, `gh --version`).
   If either is missing, tell me the install command for my OS
   (Windows: `winget install --id Git.Git -e` and `winget install --id GitHub.cli -e`;
   macOS: `brew install git gh`) and wait for me to confirm it is installed.
2. Run `gh auth status`. If I'm not logged in, run `gh auth login --hostname github.com --git-protocol https --web`
   and tell me to complete the browser step. Then run `gh auth setup-git`.
3. If this folder is not already a git repo, run `git init -b main`.
4. Create these files if they don't exist:
   - `.gitignore` covering Node, Python (__pycache__, .venv), OS junk (.DS_Store, Thumbs.db), `.env*`
     (but keep `.env.example`), and build output (dist/, build/, node_modules/).
   - `.gitattributes` with `* text=auto eol=lf` and `*.pdf binary`, so Windows and Mac line endings don't fight.
   - `README.md` with a short project description (revamp of West Monroe's AI-Native Enterprise Agent for MBC)
     and a "How we work" section: branch from main, open a PR, 1 approval required, squash merge.
   - `AGENTS.md` with the team conventions from the section "AGENTS.md contents" below.
   - Move `MBC-wm-ai_Tool_Spec.pdf` and `build_spec.py` into `docs/`.
5. Make the first commit: `git add -A` then `git commit -m "chore: initial project scaffold"`.
6. Create the private repo and push:
   `gh repo create <ORG>/<REPO> --private --source . --remote origin --push`
7. Protect main (needs admin rights, which I have as org owner):
   gh api -X PUT repos/<ORG>/<REPO>/branches/main/protection \
     -H "Accept: application/vnd.github+json" \
     -f "required_status_checks=null" \
     -F "enforce_admins=false" \
     -F "required_pull_request_reviews[required_approving_review_count]=1" \
     -F "required_pull_request_reviews[dismiss_stale_reviews]=true" \
     -f "restrictions=null" \
     -F "allow_force_pushes=false" -F "allow_deletions=false"
   If the flag syntax fails on my shell, write the JSON body to a temp file and use `--input` instead.
8. Allow squash merges only and auto-delete merged branches:
   `gh repo edit <ORG>/<REPO> --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false --delete-branch-on-merge`
9. Give the `engineers` team write access:
   `gh api -X PUT orgs/<ORG>/teams/engineers/repos/<ORG>/<REPO> -f permission=push`
10. Print the repo URL and a summary of what was configured.
```

---

## Part B: Every team member (copy and paste this into Codex)

Run it from the parent folder where you keep code, e.g. `C:\Users\<you>\code` or `~/code`.

```text
Set up my machine to work on our team's central GitHub repository <ORG>/<REPO>.
Explain each step briefly before running it. If something fails, stop and tell me the fix; don't improvise
destructive commands (no force-push, no reset --hard, no deleting folders).

1. Check tools: `git --version` and `gh --version`.
   If missing, give me the install command for my OS and wait:
   - Windows: `winget install --id Git.Git -e` and `winget install --id GitHub.cli -e` (then reopen the terminal)
   - macOS:   `brew install git gh`
   - Linux:   use the distro package manager for git, and https://cli.github.com for gh
2. Ask me for my full name and the email on my GitHub account. Then set:
   git config --global user.name "<my name>"
   git config --global user.email "<my github email>"
   git config --global init.defaultBranch main
   git config --global pull.rebase true
   git config --global fetch.prune true
   git config --global core.autocrlf input    (on Windows use: git config --global core.autocrlf true)
3. Log in to GitHub: run `gh auth status`. If not logged in, run
   `gh auth login --hostname github.com --git-protocol https --web`
   and tell me to finish the step in my browser. Then run `gh auth setup-git` so git uses gh for credentials.
4. Confirm I can see the repo: `gh repo view <ORG>/<REPO>`.
   If it returns "not found", tell me to accept the org invite at https://github.com/<ORG> and ask the tech lead for access.
5. Clone it: `gh repo clone <ORG>/<REPO>` and move into that folder.
6. Verify the setup:
   - `git remote -v` shows origin pointing at github.com/<ORG>/<REPO>
   - `git status` is clean on branch main
   - Create a test branch `git switch -c chore/<my-first-name>-setup-check`, add my name to the
     "Team" list in README.md, commit with message "chore: add <name> to team list",
     push with `git push -u origin HEAD`, and open a PR with
     `gh pr create --fill --base main`.
7. Read AGENTS.md in the repo and summarize the team conventions back to me in 5 bullets.
8. Print the PR URL and tell me to ask a teammate to review it.
```

---

## Part C: Daily workflow (humans and Codex follow the same rules)

```bash
git switch main
git pull
git switch -c feat/short-description
```

Commit small and often, then push and open a PR:

```bash
git push -u origin HEAD
gh pr create --fill --base main
```

After the PR is squash-merged, clean up:

```bash
git switch main
git pull
git branch -d feat/short-description
```

When your branch falls behind main:

```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

`--force-with-lease` is only for your own feature branch. Never use it on `main`.

Branch prefixes: `feat/`, `fix/`, `chore/`, `docs/`, `spike/`.
Commit style: Conventional Commits, e.g. `feat: add company resolver`.

**Codex cloud (optional):** in ChatGPT, open Codex, go to Settings and connect GitHub, then grant access to `<ORG>/<REPO>`. Cloud tasks then work on their own branches and open PRs. Review those PRs like anyone else's.

---

## AGENTS.md contents (Codex reads this automatically)

```markdown
# AGENTS.md — MBC-wm-ai

## Project
Revamp of West Monroe's AI-Native Enterprise Agent (agents.westmonroe.ai/ai-native-enterprise-agent).
The current-state spec is in docs/MBC-wm-ai_Tool_Spec.pdf.

## Git rules for agents
- Never commit or push to `main`. Always work on a branch: feat/, fix/, chore/, docs/, spike/.
- Pull/rebase on origin/main before starting work.
- Keep commits small; use Conventional Commit messages.
- Open a PR with `gh pr create --fill --base main`; describe what changed and how it was tested.
- Never force-push to main. Use `--force-with-lease` only on your own feature branch.
- Never commit secrets. API keys go in `.env` (git-ignored); document required vars in `.env.example`.
- Don't run destructive commands (reset --hard, clean -fdx, branch -D on others' branches) without asking.

## Before opening a PR
- Run the project's lint and tests (commands will be listed here once the stack is chosen).
- Update docs/ if behavior or architecture changed.
```
