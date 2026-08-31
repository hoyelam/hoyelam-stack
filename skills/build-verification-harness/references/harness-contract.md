# Project verification harness contract

Use this contract when a repository needs a reusable control surface rather than another task-specific verification recipe. Fit the names and tools to the repository's conventions.

## Project-local shape

Create one discoverable `verify-<app>` skill containing:

1. A `SKILL.md` written for an agent arriving without prior task context.
2. Executable control helpers when repeated operations would otherwise require new shell fragments or throwaway scripts.
3. `references/features/README.md` as the behavior index and one Markdown file per mapped feature.

The skill names the exact setup or launch command, readiness signal, read-only doctor, drive surface, evidence directory, isolation model, and cleanup command. It distinguishes environment readiness from behavior proof.

## Control CLI

Prefer a small CLI when the application has a meaningful runtime surface. Include only commands the repository can support reliably. Useful command groups are:

- Health and identity: `info`, `doctor`.
- Lifecycle: `setup`, `build`, `launch`, `stop`, `restart`, `cleanup`.
- Inspection: `snapshot`, `screenshot`, `logs`, `network`, `state`.
- Navigation and interaction: application-specific semantic commands backed by stable routes, labels, identifiers, or protocol inputs.
- Performance: `trace`, `profile`, or metrics commands when performance work is supported.

The CLI contract is:

1. `--help` lists commands, flags, prerequisites, and examples without requiring the application to be running.
2. Standard output is one JSON object suitable for another tool to consume. Diagnostic prose goes to standard error.
3. Success and failure use stable exit codes and include a concrete recovery action when one is known.
4. Potentially destructive reset or cleanup commands provide `--dry-run` or an equally explicit preview before they can affect persistent state. Preview mode must not require the mutable application, device, process, or service to be available.
5. Commands report the instance they addressed and refuse ambiguous shared instances.
6. Fixed sleeps do not stand in for observable readiness or completion conditions.
7. Failures retain their real category and recovery path. In particular, do not report a sandbox, permission, or bind-probe failure as an occupied port or shared instance.

A compact result shape is sufficient:

```json
{
  "ok": true,
  "command": "doctor",
  "instance": "isolated-instance-id",
  "artifacts": [],
  "details": {}
}
```

## Environment and isolation

Document the required runtime and dependency versions, lockfile or cache assumptions, build-time network access, configuration, seed data, test users, authentication, and unavailable external services. Use production boundaries with safe fixtures; do not route around the layer being verified.

Declare whether the harness supports concurrent instances. When it does, derive or allocate separate ports, profiles, data directories, containers, Simulators, or external test resources. When it does not, name the exclusive resource and refuse a second driver. Never copy private user data into a verification fixture.

When cleanup owns a background process, persist and verify identity beyond a PID, such as process birth time plus the expected command, checkout, and instance. A recycled PID is not proof that the harness started the current process.

## Feature map

Use stable kebab-case feature identifiers. The index gives each feature a one-line user-facing description and links to its file. Each feature file contains:

1. `## Sub-features`
2. `## User path`
3. `## Harness drive`
4. `## Proof`
5. `## Gotchas`

Record relevant entry points, modes, enabled variants, success and failure states, persistence checks, permissions, entitlements, fixtures, and unreachable prerequisites. Keep entries grounded in current source and observable state. For rendered web interactions, record the role-and-name or equally semantic locator that succeeded in the live application; source markup alone does not prove a control path.

## Evidence receipt

Every runtime proof identifies:

- The application revision or artifact identifier.
- The verification skill name and revision.
- Mapped feature identifiers exercised.
- Doctor status and instance identity.
- Evidence artifact references.
- Concrete limitations or unreachable paths.

Rendered web proof also records page identity, meaningful DOM content, framework-overlay absence, console health, the interaction state transition, and a screenshot. Exercise a materially relevant responsive breakpoint when the behavior or layout changes across breakpoints.

Orchestrated work should record these as structured receipt fields rather than burying them in narrative prose.

## Completion

Run the bundled `validate_harness.py` against the generated skill, then prove it by running its own setup or launch, doctor, one mapped feature, evidence capture, and cleanup. Confirm the proof artifacts remain afterward and no process, port, test profile, or mutable external resource created by the run remains active.
