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

### Traceability
- [List of linked FR/NFR/SFR IDs]

### Testing Strategy
- **Test Types:** [Unit, Integration, End-to-End, Manual, etc.]
- **Test Files:** [List of relevant test files]
- **Test Approach:**
  - [How each acceptance criterion will be verified]
- **Code Modules:** [List of code files/modules implementing the feature]
```

### Documentation Structure and Traceability

```
documentation/
  user_stories.md      # User stories, feature items, acceptance criteria, traceability, testing strategy
  project_structure.md # This process and structure description
  requirements.md      # (Optional) Glossary of FR/NFR/SFR, requirement IDs, etc.
  design/              # (Optional) Design diagrams, architecture docs

src/                   # Application code (modules, components)
controller_web/        # Web UI code
tests/                 # Automated BDD tests, step definitions
```

This structure ensures all information for each user story is grouped together, with clear links from requirements to design, implementation, and testing.
