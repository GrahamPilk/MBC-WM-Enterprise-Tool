# MBC-wm-ai
Pre-build analysis workspace for revamping West Monroe's public "AI-Native Enterprise Agent" (https://agents.westmonroe.ai/ai-native-enterprise-agent/) for MBC. Graham is tech lead. There is no application code yet, and the files never say what "MBC" stands for.

## Stack & layout
- Not a git repo. No source tree, package manifest or chosen stack; the product stack is still undecided.
- `build_spec.py`: ReportLab script that generates `MBC-wm-ai_Tool_Spec.pdf` (the spec; all content is hard-coded in the script).
- `MBC-wm-ai_Tool_Spec.pdf`: generated output (6 pages), "Draft v0.2", dated 23 Sep 2026.
- `West Monroe AI-Native Enterprise Agent Senior Consultant Overview.pdf`: 3-page review dated 5 Oct 2026.
- `CODEX_GIT_SETUP.md`: copy-paste prompts for a GitHub org repo setup, branch protection and daily workflow, plus a draft `AGENTS.md`.

## Commands
- `python build_spec.py` regenerates the spec PDF. Run it from this folder: the output path is relative to the working directory, and it overwrites the existing PDF. Needs `reportlab` (importable here under `python`).

## How to work here
- Edit `build_spec.py`, never the PDF, then regenerate and check the pages.
- Planned team workflow (not yet in effect, because no repo exists): private GitHub repo under an org, short-lived branches (`feat/`, `fix/`, `chore/`, `docs/`, `spike/`), PRs into a protected `main` with 1 approval, squash merge, Conventional Commits, secrets only in git-ignored `.env`. The team also uses Codex; if an `AGENTS.md` appears, follow it and don't duplicate it here.

## Gotchas
- `CODEX_GIT_SETUP.md` is a plan, not a record. `<ORG>`/`<REPO>` are unfilled, no repo or remote exists, and its step to move the spec and script into `docs/` hasn't happened.
- The two PDFs differ in scope. The spec covers hands-on runs (Ameren, Chipotle). The overview covers the landing page and setup form only and says no brief was generated, so don't take output-quality claims from it.
- Spec items marked "(inferred)" are unconfirmed; there is no repo or backend access to West Monroe's tool.
- The spec's PDF-export test was skipped because it needs a real name and email. Don't submit personal details to the live tool without asking Graham.
- Spec numbering is off: the heading "6. Recommended improvements" contains subsections 5.1-5.4, and the flaws section is 5.

## Docs
- `MBC-wm-ai_Tool_Spec.pdf`: current-state spec (purpose, research framework, user flow, observed architecture, data model), test results, flaws and risks, recommended improvements, phasing, kickoff questions.
- `West Monroe ... Senior Consultant Overview.pdf`: short consultant view with strengths, gaps and eight ranked recommendations.
- `CODEX_GIT_SETUP.md`: repo setup for the tech lead (Part A), setup for each team member (Part B), and the daily git workflow (Part C).
