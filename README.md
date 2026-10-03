# Citable Research Lineages

CRL is an experimental format for citable research contributions and their dependencies, challenges, replications, revisions, and withdrawals. Its central question is whether moving a research record between copies can preserve known objections as well as supporting material.

The current collaboration direction uses **GitHub**. It does not require the former Tokyo VM, a hosted CRL endpoint, cryptocurrency, or paid computation. This repository contains a design proposal and a local prototype; publishing it does not establish a solution to a mathematical problem or a validated decentralized research network.

## Read and contribute

- [Contribution guide](CONTRIBUTING.md): a manual GitHub workflow with local checks for scoped questions, results, and reviews, with attribution, evidence, licensing, and dispute handling.
- [Paper draft](paper.md) and [PDF](paper.pdf): the protocol's motivation and evaluation proposal.
- [Protocol draft in Chinese](protocol-v0.1.md): proposed identity and event semantics. WebAuthn ownership, agent delegation, revocation, and recovery are design requirements, not implemented features.
- [Related work](literature-map.md): source map and the limits of the comparisons.
- [Historical pilot](pilot-plan.md): bounded local and VM experiments; no current infrastructure dependency.

Start with one independently checkable mathematical statement, counterexample, correction, or reproduction. State exact assumptions and quantifiers and link the original evidence. A partial result or conditional reduction must retain its boundary. A public problem's prestige, a valid signature, and passing software tests do not establish a proof.

Original protocol and documentation are licensed under **CC BY 4.0**; original companion software is licensed under **Apache-2.0**. See [license scope](LICENSE.md) and the included official terms. Research contributions require their authors' explicit artifact-level license and approved attribution; third-party materials retain their own terms.

## Run the local example

Requires Python 3.11 or later and the dependencies in `pyproject.toml`.

```sh
uv sync --group dev
uv run python crl_events.py
uv run --group dev pytest -q
uv run python -m tests.simulate_research_map
uv run python contribution_check.py
```

The first example uses temporary agent keys and synthetic integer claims. The simulation starts two temporary services on numeric loopback addresses and shuts them down on completion. It exercises a failed replication, challenge, revision, request, expiring work, and transfer of the provided snapshot. It uses no historical research or remote VM.

The client and server are optional local test tools. If testing them manually, start a loopback server with `crl_server.py --db <local-event-file> --port 8765`, then use `crl_client.py --help`. Keep persistent private keys outside the repository and shared folders. The server accepts any valid agent signature; it does not enforce human ownership or delegation. Its HTTP submission commands are not a GitHub contribution interface.

## What the prototype establishes

The separate `crl/0.1-agent-key-demo` profile signs JCS-canonicalized event bodies with Ed25519 agent keys. An event ID identifies its body. Export follows cited references and incoming dispute/context links within the supplied snapshot and reports missing event IDs.

The optional state view records `view_policy`, `snapshot_id`, and `coverage`. `OPEN`, `DISPUTED`, and `CANDIDATE_SOLUTION` are interpretations of that snapshot. A `resolves` relation is an author's assertion; a reply does not automatically close a challenge. Failed replications remain visible. WORK expires and is not mathematical evidence.

The implementation does not establish human identity, originality, scientific correctness, global completeness, artifact availability, spam resistance, formal verification, or an official problem verdict. It has no implemented GitHub ingestion adapter. Comparisons with structured Git and nanopublications remain proposed experiments; no advantage over those baselines has been established.
