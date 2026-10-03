# Contributing through GitHub

This is a manual contribution workflow with local metadata and reproduction checks. The prototype does not yet ingest GitHub issues or pull requests as CRL events. The project's original protocol/documentation use CC BY 4.0 and its companion software uses Apache-2.0; see [license scope](LICENSE.md). Publication rights for each research artifact still need confirmation.

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

## Check a GitHub contribution without a key

The pilot uses `rights-and-attribution.json` and optional `records.draft.json` in each immediate `contributions/` subdirectory. These are **unsigned content drafts**, not signed CRL wire events. A question-only package has `QUESTION.md` and its rights file. The checker uses the first pilot's existing metadata format; it checks declared metadata, not actual identity, rights ownership, or proof correctness.

```sh
uv run python contribution_check.py
# Run only verifiers you have reviewed. This command is not a code sandbox.
uv run python contribution_check.py --reproduce
uv run pytest -q
```

Checks require a human contributor, stated AI roles, and explicit authorized text/code license metadata. When present, a package manifest must match VERSION, every package file hash/size, and the declared text/code license; it excludes itself and runtime cache. Record attribution must match the package rights file; artifacts and verifier output must exist inside the package. Draft references must resolve within the same problem. Exact duplicate draft records count once; different content under the same draft reference fails. Challenges remain counted even after a successful reproduction. Runtime Python version is reported separately; all other reproduction JSON fields must match the recorded output. Pure metadata checking does not execute contribution code.

The PR workflow runs these checks with read-only repository permissions. It also checks the fixed Git snapshot. A draft PR passes through human scope/review, versioned objections, and any linked revision before a maintainer decides inclusion. CI success and merge do not endorse the theorem. CI is configured by this workflow file; it becomes a main-branch contribution check after the engineering PR is merged.

## Fix the GitHub version for a citation

After review and an authorized merge, read the actual merged commit's **full 40-character SHA**. Link a contribution as `https://github.com/Li-Hongmin/citable-research-lineages/tree/<full-SHA>/contributions/<directory>` and individual files with `/blob/<full-SHA>/...`. Keep objections and replies needed to interpret a result in authorized versioned files: PR conversations are not included in Git archives. Use a linked new revision for later changes instead of changing the meaning of a published version.

Prepare a snapshot from an explicit commit. The output directory can be outside the repository; untracked files and working-tree edits are excluded.

```sh
SHA=$(git rev-parse HEAD)
uv run python tools/check_snapshot.py prepare --commit "$SHA" --output /tmp/crl-snapshot
uv run python tools/check_snapshot.py verify --archive "/tmp/crl-snapshot/$SHA.tar" --manifest "/tmp/crl-snapshot/$SHA.manifest.json"
```

Keep the manifest alongside the citation or reviewed distribution. It records the source SHA, SHA256 of the local tar, and each file's size/SHA256. Retrying the same preparation is deterministic; replacing different existing bytes fails. For an anonymously downloaded GitHub commit archive, pass `--github-archive` to `verify`: GitHub can change compression/container bytes, but every listed file byte must match. The manifest itself needs a trusted source; a matching hash establishes content equality, not an author's identity or a mathematical verdict. The tool does not fetch, merge, create tags, or publish anything.

A Git tag or ordinary release can move or be deleted; a commit-addressed GitHub link also depends on continued repository availability. This first version uses GitHub and content hashes, and makes no permanent-archival guarantee. DOI archiving may be added later as a separate optional publication step.
