# Two-row boundary-support pilot

Artifact version: **0.1.0-draft.1**. Human contributor: **Li Hongmin**. Status: public draft for review; a bounded finite verification, not a proof of Barnette.

Read [QUESTION](QUESTION.md), [RESULT](RESULT.md), and [REVIEW](REVIEW.md) together. The result is a self-contained theorem of an explicitly reduced finite relational language. The review preserves the objection that the original source's full marked types and partition joins have not been instantiated by this package. It does not assert graph realizability, actual rooted split-bond failure, or a solution of the main conjecture.

## Reproduce

From the repository root:

```sh
python3 contributions/barnette-reduced-support-v0.1.0/reproduce.py
```

The [verifier](reproduce.py) uses the Python standard library, no network, and no file writes. It independently enumerates all 256 edge subsets of one local patch, recovers its seven compatible patterns, evaluates the nonvacuous two-row antecedent, exhausts all 64 child admission/bond assignments, and checks singleton minimality. The [recorded output](reproduction-result.json) declares exact coverage and the Python version used. The [analytic proof](RESULT.md) explains why the finite computation is a check of the declared model, not an extrapolation to actual graphs.

## Records, rights and version

[records.draft.json](records.draft.json) holds PROBLEM, CLAIM, REPLICATION and retained CHALLENGE **content drafts**. Their references are internal draft references. They have no event IDs, keys or signatures; this is an artifact submission through the manual [GitHub workflow](../../CONTRIBUTING.md), not ingestion of signed CRL events. No identity or working key was created.

New text is **CC BY 4.0** and the new verifier is **Apache-2.0**, as explicitly scoped in [LICENSE.md](LICENSE.md) and [rights-and-attribution.json](rights-and-attribution.json). The disclosed Codex roles are preparation, bounded argument review, a new implementation independent of archived project scripts, and packaging. This is the same Codex task, not a separate human referee or different-model acceptance.

[sources.json](sources.json) contains fixed private-source ancestry fingerprints only. No original private proof, literature full text, raw chat, or archived computation is copied or relicensed. The new reduced theorem supplies all its assumptions and proof locally; inaccessible sources are not hidden public reproduction dependencies.

[package-manifest.json](package-manifest.json) fixes the exact new files by SHA-256. Cite this directory at the actual commit containing it, together with version 0.1.0-draft.1 and the retained review/challenge. A branch URL is mutable; no release, DOI, archival permanence or repository-wide freeze is claimed. Changed claims should receive a linked version/revision with their prior challenge retained.

The [three remaining-line questions](../four-lines-questions-v0.1.0/QUESTION.md) are unverified questions, not additional validated results.
