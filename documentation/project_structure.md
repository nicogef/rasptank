# Project Roles
| Role              | Tasks Description                                                   |
|-------------------|---------------------------------------------------------------------|
| Product Owner     | Defines needs, tests solutions, signs off requirements              |
| Architect         | Establishes overall system design and integration strategy          | 
| Robotics Engineer | Designs hardware, integrates with software (drivers)                |
| Software Engineer | Uses the actions received from the Front-End to command the drivers |
| Web Developer     | Builds UI and server, connects robot to web                         |
| QA/Tester         | Tests web interface and robot behaviors                             |
| DevOps            | Manages CI/CD, deployment, and infrastructure                       |

## Requirements Process

This project uses a 3-level requirements and BDD workflow, with all information for each user story grouped together, including the testing strategy.

### 1. User Story (What & Why)
- Located in: `documentation/user_stories.md`
- Each user story describes a feature from the end-user’s perspective, stating what is needed and why.

### 2. Feature Items (How & Who)
- For each user story, break it down into feature items (tasks, sub-features, or behaviors).
- Each item specifies:
  - How the feature will be realized (design, architecture, technical approach).
  - Who is responsible (system component, module, or role).
- Feature items and acceptance criteria are listed under each user story in `user_stories.md`.

### 3. Acceptance Criteria & Testing Strategy
- For each feature item, acceptance criteria are written as Gherkin scenarios or clear, testable statements.
- The testing strategy for each user story includes:
  - **Test Types:** (Unit, Integration, End-to-End, Manual, etc.)
  - **Test Files:** (List of relevant test files)
  - **Test Approach:** (How each acceptance criterion will be verified)
  - **Code Modules:** (List of code files/modules implementing the feature)
- All this information is grouped together for each user story in `user_stories.md`.

### 4. Traceability
- Each user story and feature item is linked to relevant FR/NFR/SFR IDs.
- Traceability is maintained within each user story entry in `user_stories.md`.

### Example User Story Entry
```
## US_000X: [Feature Title]
**What & Why:**  
As a [user], I want [feature], so that [value/goal].

### Feature Items (How & Who)
- US_000X_FI_0001: [Description of item, responsible module/component]
- US_000X_FI_0002: [Description of item, responsible module/component]

### Acceptance Criteria
- US_000X_AC_0001: [Testable statement or Gherkin scenario]
- US_000X_AC_0002: [Testable statement or Gherkin scenario]
```
### Documentation Structure

-   `documentation/`:
    -   `user_stories.md`: Contains user stories, feature items, acceptance criteria, traceability, and testing strategies.
    -   `project_structure.md`: Describes the project's organization, roles, and processes (this file).
    -   `requirements.md`: (Optional) A glossary of requirements (FR, NFR, etc.) and their corresponding IDs.
    -   `design/`: (Optional) A directory for design diagrams, architecture documents, and other visual materials.
-   `src/`: Houses the core application code, including modules and components.
-   `controller_web/`: Contains the code for the web-based user interface.
-   `tests/`: Includes automated BDD tests and their step definitions.

This structure ensures all information for each user story is grouped together, with clear links from requirements to design, implementation, and testing.

# Code Style and Quality

This project enforces a consistent code style and quality through a combination of automated tools and established best practices.

-   **Formatting**: Code formatting is standardized using **Black**. All contributions must be formatted before submission.
-   **Linting**: **Pylint** is used to identify and report code quality issues. Adherence to the rules defined in `.pylintrc` is required.
-   **Testing**: The project maintains a comprehensive test suite, including:
    -   **Unit Tests**: Located in the `tests/` directory, these verify individual components in isolation.
    -   **BDD Tests**: Found in the `bdd/` directory, these ensure that the system's behavior aligns with the specified requirements.

All checks are enforced automatically through the CI/CD pipeline.

# Design and CI/CD Constraints

- **CI/CD**: Governed by `.github/workflows/ci.yml`.
- **Local CI runner**: `scripts/ci.py` provides a local equivalent for CI checks.

### Design Constraints
- **CI Parity**: `scripts/ci.py` and `.github/workflows/ci.yml` shall be kept in sync. Any task added to one must be added to the other to ensure local and remote builds are consistent.
- **Python Version**: The project targets Python 3.11, as reflected in CI.
- **Code Style**: Black is used for formatting, and Pylint for linting. Configuration is in `pyproject.toml` and `.pylintrc`.
