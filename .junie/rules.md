# Junie Guidelines and Constraints

This document provides human-readable guidelines that accompany the machine-readable policy in `.junie/config.yaml`.

Last updated: 2025-10-12

## 1. Scope and Directory Policy
- Day-to-day development is limited to the curated set of paths:
  - src/**, tests/**, scripts/**, .github/**, controller_web/**, .junie/**.
- The root .gitignore enforces a "default-deny" policy; everything outside the curated set is ignored.
- If you need to add a new top-level area, propose it via PR and update both `.gitignore` and `.junie/config.yaml` accordingly.

## 2. Code Quality
- Python version: target Python ≥ 3.10; CI may run newer.
- Formatting: Black with line length 127.
- Linting: Pylint; aim for zero errors. Warnings should be actionable or justified with inline comments.
- Type checking: Optional for now; feel free to use typing where helpful.

## 3. Testing & CI
- Unit tests are required for control logic. Use mocks for hardware.
- Run local CI via `python -m scripts.ci all` before pushing.
- Coverage outputs (coverage.xml, htmlcov/) are ignored by default; CI uploads artifacts from its run.

## 4. Security & Secrets
- Do not commit secrets or credentials. Use environment variables or separate, ignored config.
- Secret scanning is assumed; treat findings seriously.
- Protected files: `.junie/config.yaml` and `.junie/rules.md` should be changed in dedicated PRs with reviewer approval.

## 5. Git Hygiene
- Branch naming: feat/*, fix/*, chore/*, docs/*, refactor/*, test/*.
- Keep commits focused and messages meaningful. Reference issues where applicable.
- PRs should include a brief rationale and testing notes.

## 6. Change Management
- Requirements reside in REQUIREMENTS.md. Keep changes traceable to code/tests/docs.
- For structural changes (new directories, build system changes), update both `.gitignore` and `.junie/config.yaml`, and amend README accordingly.

## 7. How to extend the curated set
1) Edit `.gitignore` to un-ignore the new top-level folder (e.g., `!new_area/` and `!new_area/**`).
2) Add the same folder to `allowed_paths` in `.junie/config.yaml`.
3) Document the purpose of the folder in README under the Project Policy section.

## 8. Exceptions
- Temporary exceptions (e.g., bringing in a one-off artifact) should be handled via local .git/info/exclude or a temporary patch that is reverted before merge.

## 9. Ownership & Contacts
- Repository owners: see `.junie/config.yaml` metadata. For questions, open an issue or ping maintainers.
