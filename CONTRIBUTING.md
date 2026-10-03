# Contributing through GitHub

This is a proposed manual contribution workflow. The prototype does not yet ingest GitHub issues or pull requests as CRL events. The project's original protocol/documentation use CC BY 4.0 and its companion software uses Apache-2.0; see [license scope](LICENSE.md). Publication rights for each research artifact still need confirmation.

## Choose one contribution

Use a GitHub issue to scope a question or discuss a result. Use a draft pull request for a reviewable artifact. Keep the question, mathematical evidence, and review distinct:

| Reader label | Content | Existing prototype event kind |
|---|---|---|
| QUESTION | Exact object, quantifiers, known boundary, and one checkable question | PROBLEM |
| RESULT | A bounded theorem, counterexample, conditional reduction, or reproducible computation | CLAIM, with EVIDENCE or METHOD where needed |
| REVIEW | An independent argument check, replication, objection, or correction | REPLICATION, CHALLENGE, or REVISION, according to the actual action |
| WORK | One bounded task and its expiry | WORK |

QUESTION, RESULT, and REVIEW are guide labels, not new accepted wire kinds. Review text must not be silently interpreted as approval. A counterexample to a proposed mechanism is not a counterexample to its parent conjecture.

For contributions to the original protocol or software, explicitly confirm that you are authorized to submit the changes under CC BY 4.0 (protocol/documentation) or Apache-2.0 (software), as applicable. Research notes, datasets, and third-party artifacts require a separate explicit license statement; do not infer their terms from a filename. No copyright transfer is requested.

## Include enough to check it

A question or result should contain:

- A title, exact statement, assumptions, quantifiers, and a stable problem reference.
- The status: proposed, internally argued, independently checked within a stated scope, reproduced within a stated scope, challenged, corrected, or withdrawn. Say who performed each check and what it covered.
- The original proof or artifact, a fixed source commit or release, dependencies, reproducibility command and tool versions when computation carries the claim.
- The conclusion's limits and known objections, failed replications, corrections, and missing materials. Link later challenges as well as supporting ancestors.
- Human authors and contributors, their approved credit, and the AI tools' actual roles. An operator, signing key, or submitting agent is not automatically the mathematical author.
- Explicit rights and license for each artifact. Do not copy a paper, private correspondence, an AI chat export, or someone else's unpublished result merely because you can access it.

A computation proves only its declared finite coverage unless a separate argument justifies a general conclusion. Reproducing code output is not by itself a verification of a theorem. Do not describe the general Riemann hypothesis, P versus NP, Hodge conjecture, or another open conjecture as solved on the basis of a local lemma or conditional bridge.

Keep claims and reviews append-only in meaning: add a linked correction or withdrawal when the statement changes. Preserve challenged versions through Git history or a released artifact that is itself cleared for publication. Only an authorized author can withdraw their claim; a third party records a challenge.

## Scope a draft pull request

For a first pilot, place a short self-contained note and any minimal, redistributable verifier under a single contribution directory, with links from its README. Agree the directory and semantic version with maintainers before introducing a new schema. Avoid copying entire research workspaces or raw execution histories.

The PR description should state the mathematical change, the source version, the evidence checked, the remaining boundary, attribution and license, and the reproduction result. Maintainer merge means inclusion in this repository; it does not confer a global scientific verdict, priority, prize eligibility, or journal acceptance.

Private signing keys, credentials, environment files, local logs, private chats, personal identifiers, and unrelated research do not belong in a contribution. Keep keys outside the repository. Reviews of real research require specific publication rights even when the reviewer is an AI tool.

## Git and snapshot boundaries

A Git clone copies repository history; it does not automatically copy issue discussions or PR reviews. If those discussions carry an objection needed to understand a result, include an authorized versioned record or explicitly state the missing context. Use a commit hash for a fixed snapshot and preserve in-scope challenges, failed replications, revisions, and withdrawals.

The current signed-event profile has `protocol`, `kind`, `problem`, `author_key`, `created_at`, `relations`, and object-valued `content` in its body, with `id` and `signature` in the envelope. Domain-specific content is not yet enforced by a research schema. Human attribution and licenses must be recorded explicitly in the contribution; the demo does not validate them or implement the ownership/delegation design in the protocol draft.

No contribution request authorizes restarting research schedules, deploying a server, spending on compute, or submitting a paper elsewhere.
