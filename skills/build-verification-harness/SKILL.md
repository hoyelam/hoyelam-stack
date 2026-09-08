---
name: build-verification-harness
description: Create or extend a repeatable project verification path when reliable real-application proof is missing.
---

# Build Verification Harness

Inspect repository launch commands, test drivers, observability, supported interactions, and isolation constraints. Reuse a working harness and extend only what the requested proof needs. Use the relevant iOS, macOS, Electron, or other available platform guidance without requiring a particular driver.

Make setup, interaction, expected outcomes, evidence capture, and cleanup discoverable to an agent without prior context. Existing scripts, scenarios, and docs may suffice. If no suitable convention exists, the [bundled verification-skill template](references/harness-contract.md) supplies an optional `verify-<app>` layout, feature map, and validator.

## Build the missing control path

- Document required environment and dependency versions, cache or network assumptions, launch command, read-only readiness and instance-identity checks, fixtures or authentication, isolation model, and evidence and cleanup paths.
- Add a small control CLI only when repeated operations would otherwise be improvised. Keep help available without a running app, outputs concise and machine-readable where consumed by tools, and failures explicit about cause and recovery. Use bounded checks for observable readiness or completion instead of fixed sleeps.
- Drive the real user boundary with stable selectors, semantic commands, routes, accessibility identifiers, or protocol inputs. Prove rendered locators against live state. Internal test setters do not replace the user path unless they are the production boundary under test.
- Record the action and resulting state. Use independent files, database values, logs, responses, or process evidence to prove relevant side effects.
- Isolate mutable resources; refuse concurrent driving when instances cannot be distinguished safely. Cleanup owns only the processes and scratch state created by the harness and preserves evidence.

Map the requested behavior using existing scenarios or a feature catalog: identify the user entry point, exact drive commands, expected state and side effects, and relevant fixtures, variants, or prerequisites. Expand coverage when requested or repeated verification needs it. Separate feature files are a bundled-template convention.

## Prove and hand off

Run the project's checks and, when selecting the bundled format, `python3 <this-skill>/scripts/validate_harness.py <project-verification-skill>`. Exercise setup or launch, readiness and identity, one scoped user behavior, evidence capture, and cleanup end to end against the real artifact. Confirm documented command results, current application and harness identities, and evidence that survives cleanup.

Fix harness failures and rerun affected paths. Report product failures separately unless changing the product is authorized. An unexercised harness remains a draft. Maintain later drift with the existing harness's checks or `$maintain-verification-harness` for the bundled format; report the precise behavior proved and any required blocked checks.
