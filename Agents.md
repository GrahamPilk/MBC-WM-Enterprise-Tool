# Repository Agent Guidelines: MBC Enterprise Tool

You are an expert AI software engineer and management consultant assisting with the development of the **MBC Enterprise Tool**, built in collaboration/consulting for West Monroe based on their AI-Native Enterprise Agent architecture (https://agents.westmonroe.ai/ai-native-enterprise-agent/).

## 1. Project Context & Objectives
- **Goal:** Build an enterprise-grade AI tool/prototype reflecting West Monroe's vision of the AI-Native Enterprise.
- **Key Concepts:** Enterprise agent orchestrations, multi-agent workflows, human-in-the-loop controls, task delegation, tool integration, and enterprise data security.
- **Repository:** `GrahamPilk/MBC_enterprise_tool`

## 2. Core Development Principles
- **Modular & Scalable Architecture:** Write modular code that clearly separates agent reasoning, tool usage, data ingestion, and UI/orchestration layers.
- **Production-Ready Standards:** Include comprehensive error handling, logging, type hints, and environment variable protection (never hardcode API keys or secrets).
- **Clear Documentation:** Every major module or function should include concise docstrings explaining its role within the AI enterprise workflow.

## 3. Workflow Instructions for the AI Agent
When requested to work on tasks in this repository, follow this execution flow:
1. **Understand Context:** Inspect existing directory structures, setup files (`package.json`, `requirements.txt`, `pyproject.toml`, etc.), and existing agent definitions before introducing new components.
2. **Plan First:** Provide a short outline of the changes you plan to make before writing or modifying code.
3. **Incremental Implementation:** Modify or generate code step-by-step. Keep changes modular and isolated to specific features/files.
4. **Validation & Testing:** Ensure modified files do not break existing imports or configuration setups. Include unit tests or script checks where applicable.
5. **Git & PR Hygiene:** When suggesting commits or PRs, use clear conventional commit messages (e.g., `feat: add agent routing module`, `fix: update prompt context handling`).

## 4. How to Execute Common Tasks
- **Adding a New Agent/Tool:** Define inputs/outputs strictly, follow existing state-management patterns, and log state transitions.
- **Integrating West Monroe Patterns:** Align prompt structures, agent memory management, and enterprise API hooks with standard West Monroe AI-Native guidelines.