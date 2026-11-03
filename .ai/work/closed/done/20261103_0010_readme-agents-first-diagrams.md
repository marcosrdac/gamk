---
status: done
origin: user conversation
branch: feat/readme-agents-first
worktree: .git-worktrees/readme-agents-first
---

# Reframe README diagrams around AGENTS.md first

## Objective

Replace the current README Mermaid flow with diagrams that explain the installed project's experience first: `AGENTS.md` is the entrypoint, it guides discovery of the project's `.ai/` memory structures in the same order as the instructions, and only then does GAMK appear as the source that generates `AGENTS.md` and `global/`.

## Requirements

- Make `AGENTS.md` the visual and narrative center of the consumer-project explanation.
- Reflect the discovery/startup order in the shared `AGENTS.md` template.
- Show the relationship between project-owned memory, optional `.ai/global`, and the agent.
- Add a separate source-side diagram showing GAMK generates the consumer `AGENTS.md` and supplies the `global/` directory it can link.
- Keep diagrams useful and limited; retain text trees where exact file hierarchy is clearer.

## Plan

1. Replace the source-first Mermaid with an AGENTS-first consumer diagram.
2. Add a second Mermaid diagram for GAMK source → generated consumer instruction/global source.
3. Align nearby prose with the diagrams and check Mermaid syntax/Markdown formatting.
4. Run relevant tests/static checks, close the task, integrate directly into `main`, and clean the worktree.

## Progress

- [x] Replaced the source-first consumer diagram with an `AGENTS.md`-first explanation.
- [x] Added three alternative Mermaid renderings of the project memory relationship.
- [x] Kept the source-side diagram that shows GAMK generating `AGENTS.md` and supplying `global/`.
- [x] Publish the three project-side renderings together so the user can compare them in GitHub.
- [x] Run checks, close the task, integrate directly into `main`, and clean the worktree.

## Relevant history and decisions

- The user asked to review several Mermaid alternatives in sequence before choosing the final visual; the alternatives are intentionally being integrated now for that review.
- The project-side diagrams must follow the `.ai/` structure order documented in the shared `AGENTS.md` template.

## Completion criteria

- [x] The first diagram starts at `AGENTS.md` and follows the shared startup/discovery order.
- [x] The second diagram explains GAMK's role as generator/source.
- [x] The README remains value-first and operationally accurate.
- [x] The README publishes the alternatives clearly enough for the user to compare their rendering.
- [x] Checks pass and the task/worktree lifecycle is completed.

## Next action

The review gallery is ready for integration; the next user feedback can choose the surviving project-side diagram.
