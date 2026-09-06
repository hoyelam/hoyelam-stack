# hoyelam-stack

`hoyelam-stack` captures how I like to work with coding agents: understand the problem, think through what success looks like, implement a focused solution, and gather evidence that it works.

I put particular emphasis on verification and quality assurance. I want to know that the original problem is actually fixed or that an addition behaves as intended. Tests, real usage, and review each help answer that question. After review changes the implementation, I want the affected behavior checked again.

Orchestration is also part of how I work. For larger projects, I want a lead agent to define clear units, delegate useful work, coordinate dependencies, and keep progress recoverable. Verification governs which results are accepted and when the overall project is complete.

The stack packages this method into skills and supporting tools for Codex, with instructions that remain usable by other coding agents.

## How I work

1. **Understand the issue.** Read the relevant code and context, reproduce the problem where possible, and identify its cause. For an addition, understand the need and how it fits the existing project.
2. **Define success.** Describe the behavior I expect to see when the work is done, including important failure cases and behavior that must keep working.
3. **Plan verification.** Decide how to prove those expectations before implementation: which tests or interactions to run, what they need, and what results would count as success.
4. **Implement.** Make the smallest complete change that solves the problem and fits the existing architecture. For larger work, verify small units before building on them.
5. **Verify quality.** Run the relevant tests, checks, and builds, and exercise the actual behavior. Check failure paths and nearby behavior that the change could affect.
6. **Review and resolve.** Review the complete change for correctness, clarity, and unnecessary complexity. Verify findings before fixing them, and resolve confirmed issues within scope. Use an independent reviewer for substantial or risky changes when available and authorized.
7. **Verify again.** After review fixes, rerun the affected checks against the final implementation. Return to the original issue or intended addition and confirm that the evidence still proves it works.
8. **Report the evidence.** Explain what changed, what was actually checked, what the results show, and what remains unverified.

## What gives me confidence

I want as much meaningful verification as practical for the change. A passing build tells me the project builds. Tests give evidence for the cases they cover. Exercising the real application, service, or command shows what happens through the interface people actually use. Review adds another opportunity to catch mistakes and challenge assumptions.

The depth should match the work and its risk. A documentation edit needs different checks from a migration or an application feature. If review makes no relevant changes, existing evidence can remain valid. Failed or blocked required checks mean verification is incomplete, and I expect that to be stated clearly.

The [project verification contract](skills/prove-the-work/references/project-verification.md) helps make this repeatable through supported commands, observable outcomes, and clear verification requirements. Changes to the workflow itself are checked through [isolated implementation tasks](skills/hoyelam-mode/references/workflow-validation.md), with the limits of that evidence recorded.

## How I coordinate larger work

I use [orchestrate-project](skills/orchestrate-project/SKILL.md) when work needs ongoing coordination across units or sessions. The lead defines success and verification before assigning work, proves one representative unit before scaling, and keeps each worker’s scope clear. It reviews results, resolves confirmed findings, integrates accepted changes, and verifies the combined outcome. Progress and evidence survive interruptions.

Small tasks stay direct. The project’s existing tools can carry the records; the bundled orchestration runtime is available when needed. My method does not depend on a particular agent platform, hosting service, or CI provider.

## My main platforms

iOS, macOS, and Electron are my main application platforms. The stack bundles `$verify-ios-apps`, `$verify-macos-apps`, and `$verify-electron-apps` to help agents select meaningful checks and exercise the actual application. They work with existing project harnesses and supported platform tools. Bundled diagnostics help where relevant; the evidence must still show that the intended behavior works.

## Using the stack

Follow the [installation guide](docs/local-install.md), then invoke `$hoyelam-mode` for implementation work. Installing the stack makes the method available; project instructions or skill invocation put it into use. The [workflow guide](docs/workflow.md) describes the full process.

- Use `$prove-the-work`, `$review-and-resolve`, or `$comment-discipline` for a focused pass.
- Use `$build-verification-harness` to establish a reusable real-app verification path, and `$maintain-verification-harness` to keep it accurate.
- Use `$verify-ios-apps`, `$verify-macos-apps`, or `$verify-electron-apps` for platform verification. See the [platform verification guide](docs/platform-verification.md).
- Use `$recall-context` to resume older work, `$checkpoint-work` to pause safely, and `$orchestrate-project` when work spans independent units or sessions.

See the [release process](docs/releases.md) and [changelog](CHANGELOG.md) for distribution and updates.

## License

MIT
