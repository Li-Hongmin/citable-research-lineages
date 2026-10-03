# Citable Research Lineages: An Agent-Native Protocol for Public Research Commons

**Working paper · internal draft · 2 October 2026**

## Abstract

AI agents can perform parts of research work, but independently operated agents need shared interfaces to participate in public scientific problems. We propose Citable Research Lineages (CRL), an application-level event and reference model for an open research commons in which a result is individually citable, explicitly linked to its dependencies and later challenges, and portable across indexes without silently losing known dissent. A problem and each agent-authored claim, evidence artifact, replication, challenge, correction, and withdrawal has a stable identifier. Participants exchange signed, content-addressed events and keep partial local replicas; there is no assumed complete global ledger or mandatory scientific acceptance authority. Human operators manage identity through WebAuthn credentials and delegate bounded authority to separate agent keys. A view declares its input snapshot and selection policy. The central proposed property is *dispute-preserving portability*: relative to a declared snapshot, migration preserves in-scope incoming challenges as well as a claim's cited support, or explicitly reports missing material. Timestamp anchoring is optional and does not determine truth, priority, or authorship. A local example exercises agent signatures and dispute-context export; owner authentication, delegation and a federated deployment remain unimplemented. The contribution is a design and falsifiable evaluation proposal, not evidence of improved scientific discovery or a validated network.

## 1. The problem

Consider a public research problem to which many people, laboratories, and institutions send independently operated AI agents. One agent proposes a lemma; another finds a counterexample; a third repairs the statement. A shared repository can store these changes and support independent forks, although a particular project's default branch or presentation may be maintainer-controlled. Neither a default branch nor token-weighted voting should be confused with scientific validity. CRL asks a narrower question: **can independent parties exchange citable research progress while preserving known objections across migrations and competing interpretations?**

The social motivation is broader than workflow efficiency. AI changes the relation between personal expertise and research capacity: a participant may contribute by operating an agent that can read, compute, formalize, reproduce, or challenge work beyond the participant's own specialist training. The intended norm is therefore: participation should be open, while scientific validity remains earned through evidence, challenge, and reproduction. CRL lowers the coordination barrier, not the evidentiary standard.

The answer sought is not unanimous truth. It is durable, independently inspectable disagreement with low-cost discovery of useful results. A protocol can make omission and alteration detectable relative to observed peers; it cannot compel every peer to retain all data, make confidential ideas safe to reveal, or decide open scientific questions by consensus.

## 2. Prior work and boundary of the contribution

The broad conjunction of decentralized science and autonomous agents has already been described in DeScAI [1]. Traxia specifies agent identities, signed publishing, peer review, reputation, and a living knowledge graph; its review pipeline culminates in a human accept/reject decision [2]. Agent-Native Research Artifacts (Ara) organize claims, execution, exploration history, and evidence inside research packages [3]. The Claims white paper describes decentralized extraction and evaluation of claim-evidence records from papers [4]. These works motivate structured, inspectable contributions but do not by themselves establish public participation at scale.

Separation of publication from higher-level interpretation predates agentic science: nanopublications provide a decentralized provenance-aware publication network and explicitly separate low-level publishing from higher-level services [5]. Clarus describes open research collaboration through project, agent and resource objects, including identity and resource permissions [6]. XScientist defines local-first, typed, content-addressed research state and portable artifacts for continuation [7]. Symposium provides immutable community research histories used by heterogeneous agents, including new publications that challenge or correct prior records [8]. Its illustrative synthetic community is not a demonstration of autonomous discovery. These are direct architectural baselines, not merely adjacent applications.

Large Knowledge Model links addressable claims to supporting and contradicting evidence [9]. Its retrieval evaluation does not establish dispute-preserving export, and the reported extraction audit measures hallucination rather than omission. Agentic Economies identifies credit, resource allocation and misuse as institutional problems in autonomous science [10]. Co-Scientist demonstrates multi-agent hypothesis generation and selected laboratory validations, but is not a public multi-operator interchange protocol [11]. Capability results and collaboration-protocol results therefore require different endpoints.

CRL does not claim to invent open agent collaboration, signed provenance, claim graphs, portable research state, or separation of records from scientific acceptance. The candidate contribution is a common convention for retaining incoming disputes in exports of a declared snapshot, together with measurable effects on discovery and continuation. Whether this convention adds value beyond structured Git, nanopublications, XScientist or Symposium remains a comparative question. The literature comparison is bounded by sources retrieved on 2 October 2026; protocol descriptions are not treated as demonstrated deployment guarantees.

## 3. Model and objects

A problem record specifies a question, scope, admissible evidence, evaluation suggestions, and optional resource offers. It does not create ownership over the research direction. A participant controls owner credentials and delegates specific problem and event permissions to agent signing keys. A participant may run several agents, and keys do not imply distinct human identities [12]. The operator remains responsible for resource permissions and publication decisions; cryptographic attribution alone cannot establish legal accountability.

An event body contains protocol version, type, problem and contributor identifiers, agent key, delegation reference, timestamp assertion, typed relations, artifact digests and locations, license, and domain content. Its identifier is `sha256(JCS(body))`, using JSON Canonicalization Scheme [15]. A separate envelope carries the signature and authorization proofs, outside the body's hash input. The agent signature binds a protocol-specific domain separator and the canonical body; the same signature must not authorize login or resource execution. Types include `PROBLEM`, `CLAIM`, `EVIDENCE`, `METHOD`, `CHALLENGE`, `REPLICATION`, `REVISION`, `WITHDRAWAL`, and `ATTESTATION`. A claim states its exact proposition, assumptions, scope, dependencies, and what would count as failure. Evidence events reference an artifact and describe how to inspect it; a digest alone is not evidence availability. Revision never overwrites an old claim. Only an appropriately authorized contributor's withdrawal represents that contributor's position; a third party's objection is not the author's withdrawal.

Every peer may accept a well-formed event into its local store, exchange it with other peers, and issue a signed receipt identifying the event digest. Events form a directed acyclic dependency graph by parent reference. Wall-clock timestamps are assertions; an independently witnessed receipt or external timestamp can constrain ordering, but no event proves sole intellectual priority. A public problem may have many unrelated candidate solutions. Branches are not forced to merge.

**View policy** is a separately versioned, publishable program or rule description mapping an available event set to a presentation: e.g., all claims with reproducible artifacts, only formal-checker-passing proofs, or all unresolved challenges. View outputs cite both the policy version and the event-set snapshot. A view is an interpretation, not the network's scientific verdict. Users may subscribe to several views, compare them, or fork a policy. This deliberately avoids a canonical scientific `merge`.

## 4. What can be checked

Verification is layered. **L0 (record validity)** checks serialization, content digests, signatures, parent references, and receipt integrity. **L1 (artifact availability)** confirms that disclosed evidence can actually be retrieved by the entitled verifier. **L2 (procedural reproduction)** reruns an explicitly specified method in a documented environment and compares the declared observable outputs. **L3 (substantive validity)** examines whether the evidence establishes the scoped claim, including confounders, proof gaps, and novelty. L0 is automatable; L2 applies only to reproducible work; L3 may remain disputed. No chain or signature promotes L0 to L3.

For formal mathematics, a checker may establish a theorem under stated axioms and exact code; it does not establish that the theorem answers the motivating problem. For empirical work, matching a run is not independent replication, and an encrypted or unavailable dataset cannot be publicly reproduced. Views must expose these distinctions rather than flatten them into a single score.

## 5. Replication, censorship, and governance

No peer can be forced to carry every event. A small, adversarial set could hide a submission or flood indexes. CRL therefore targets **declared coverage, observable commitments, and portable exit**, not guaranteed universal publication. A submitter should obtain receipts from independent peers, mirror the payload where permitted, and retain an exportable event bundle. Peers gossip event identifiers and receipts; conflicting histories or missing referenced payloads can be reported as evidence. A newcomer can choose multiple indexes and compare their event-set snapshots. If all reachable peers collude or a payload disappears, the protocol cannot repair the loss.

Network rules should be minimal: structural schemas, cryptographic verification, reference semantics, and interoperability tests. No governance process may rewrite historic signed events. Software forks may change schemas and policies; interoperability then depends on declared version support. Moderation of a local index is allowed, but it must not be misrepresented as deletion from all replicas. Illegal, unsafe, or private material requires local access controls and removal procedures; irrevocable public storage is not a universal design goal.

A public deployment should separate protocol governance from problem governance. Polycentric governance offers an institutional background, not empirical validation of this particular design [16]. A foundation or similar public-interest operator may maintain servers, documentation, trademarks, grants, reference software, and a problem registry. It should not be able to declare a scientific claim true merely by administrative authority. Problem stewards may define scope, evidence forms, benchmark tasks and entry materials. They cannot alter signed challenges undetectably, although any local host can refuse to serve records. A safety process decides which problem classes the public commons will list, index, and support with resources. Early deployments should use an allowlisted registry: public mathematics is the first target; weapons development, CBRN optimization, and harm-oriented cyber operations are outside the intended scope. An open protocol cannot prevent third parties from repurposing its code outside this commons.

## 6. Credit and incentives

The ledger can show a concrete sequence of contribution and challenge, not infer deserved authorship from token balances or event counts. Agents are tools operated by people or organizations; authorship, intellectual property, payment, and publication require separate human agreements and applicable rules. Computing resources may be priced as services. One may later experiment with rewards for accepted, independently reproduced marginal contributions, but paying for volume or votes invites spam, identity splitting, collusion, and correlated agent judgments. The first protocol version requires no native cryptocurrency.

An open problem forfeits secrecy over whatever is disclosed. A private-idea marketplace is a different product and would need staged disclosure and contractual controls. CRL cannot stop a better-resourced laboratory from pursuing a publicly announced direction. Its potential benefit is faster coordination and more legible priority evidence, not exclusive rights.

## 7. Threat model and limitations

Adversaries may control many agent keys, replay old results, fabricate citations, create mutually endorsing reviews, selectively withhold evidence, submit poisoned artifacts, or exploit view rankings. Signatures stop undetected editing of signed bytes but do not prove identity, originality, honest experimentation, or independence. Reproductions from correlated models may share the same mistake. A useful view policy should expose provenance, dependency overlap, unresolved challenges, and the exact basis for any status label. Private research may require trusted execution or restricted storage, neither assumed here. Privacy, abuse response, data licensing, and long-term availability remain open engineering and governance problems.

The proposed owner interface uses WebAuthn passkeys, including but not restricted to Apple's implementation [13, 14]. The relying party verifies the expected challenge, RP ID, origin, credential and user verification. Management assertions bind the operation, delegation digest and a single-use nonce; an ordinary login assertion cannot be reused to authorize a different agent key. Agent permissions have a problem scope, event scope and expiry, and do not include credential changes or recovery. Owner secrets remain outside model context. The application must also protect sessions, signing interfaces and recovery paths: passkeys are phishing-resistant credentials, not a guarantee against compromised endpoints or coerced authorization.

Passkeys are RP-scoped, not universal credentials for arbitrary domains. Cross-domain migration therefore needs an old-credential authorization for the new credential, plus proof of control at the new RP, or a previously registered independent recovery method. Synced copies of one passkey do not provide independent recovery authorities. If every credential and recovery method is lost, the same identity cannot be cryptographically restored without additional evidence. Revocations require dissemination: a verifier must disclose its authorization-state freshness, and an offline peer cannot promise immediate revocation. Attacker and legitimate signatures become indistinguishable after key compromise; event timestamps cannot resolve that ambiguity. These requirements remain design obligations, not implemented capabilities of the local example.

## 8. A decisive pilot

Choose one bounded public mathematical or computational problem with a machine-checkable intermediate result. The first public-interest deployment should be mathematics-only. A Millennium-problem commons is an appropriate flagship because the targets are public, prestigious, non-laboratory problems whose intermediate claims can often be decomposed, challenged, and sometimes formalized. The goal of the pilot is not to claim a prize solution; it is to test whether independently operated agents can maintain a useful, contestable research lineage around a hard public problem.

Recruit independently operated agent teams with distinct keys and budgets, and document shared model, training and source dependencies rather than assuming independence from key count. Publish the problem and a frozen evaluation rubric. Permit open submissions, explicit challenges, revisions and alternative views. Compare with structured, multi-remote signed Git and nanopublication exchange using the same claims, typed relationships and discovery interface, under matched time and compute budgets. XScientist and Symposium should be compared at the artifact and publication layers where their interfaces permit. Clay's prize process remains separate from protocol validation [17].

Measure: independently verified useful results; time from a false claim to a valid challenge; cost per retained result; third-party reconstruction success; and whether a contributor can exit one index and rebuild the same evidence graph from other peers. Log false positives, withheld artifacts, unresolved claims, and human adjudication effort. The proposal is weakened if ordinary version control plus a public issue tracker yields the same outcomes with less complexity, or if noise and Sybil activity prevent useful discovery. Until such a test succeeds, the asserted network advantage is a hypothesis.

## 9. Dispute-preserving portability

Each contribution references prior identifiers with typed edges: `depends-on`, `supports`, `challenges`, `reproduces`, `revises`, or `withdraws`. A later paper may cite an exact event and snapshot, rather than merely a mutable problem homepage. The agent's delegated key signs its event; signatures identify the signing key, not an independent scientific mind. An agent should read known incoming challenges before extending a claim and publish which snapshot it consulted. This does not guarantee it found every challenge.

The structure is a **directed, branching citation graph**, not a single blockchain of conclusions. Nodes keep partial local event sets; a blockchain or transparency log may optionally anchor a batch digest for timing and tamper evidence. Proofs, code, data, and contesting evidence remain in accessible off-chain artifacts. An anchor does not make the scientific proposition true or grant ownership of a public direction. There is no protocol-wide merge authority: local indexes can filter, but must state their coverage and should expose an export path. Payments, native tokens, and automatic authorship are outside the first version.

The research object must remain citeable *with its dispute context*. Given a declared problem scope, snapshot cutoff, and event set, export includes both ancestors of a cited claim and in-scope incoming challenges, revisions, withdrawals, and replication failures known to that snapshot. An export may be partial, but must label missing events or unavailable payloads; `no observed challenge in snapshot S` is not `unchallenged everywhere`. A view records the exact snapshot identifier and deterministic policy version. Differences between two views can then be attributed to differing input coverage, policy, or unavailable artifacts, rather than collapsed into a popularity score. This is a proposed interoperability requirement, not a proved guarantee against unseen or withheld events.

More precisely, let $S$ be the finite event set of one declared problem snapshot and $R$ the export roots. Starting from $R$, repeatedly add available targets of outgoing references and events in $S$ with a `challenges`, `revises`, `withdraws` or `reproduces` edge into the retained set. Iterate to a fixed point; referenced identifiers absent from $S$ enter a separate missing list. Include successful and unsuccessful replications alike. This definition preserves disputes about cited ancestors, not only direct objections to the export root. Completeness is relative to the supplied set $S$, not all events that exist elsewhere. Capacity-limited implementations must support explicit, resumable partial export rather than silently truncating objections.

Receipts require explicit semantics: `observed header`, `stored bytes at time t`, `promised inclusion in named scoped snapshot by deadline d`, or `promised retention under stated access and duration`. Only incompatible signed commitments to the *same* named scope can constitute cryptographic evidence of equivocation. Different local subsets are legitimate; a failed download alone is not proof of malicious censorship. Scope of v1 is public, appropriately licensed research. Private ideas and restricted datasets need a separate disclosure and access-control design.

A first test should compare the same event schema and discovery interface atop CRL, multi-remote signed Git, and nanopublications, rather than comparing structured CRL to an unstructured chat. Inject a later challenge pointing into a previously exported claim, a hidden challenge at a dominant index, vanished payloads, and a flood of valid but irrelevant events. Evaluate whether independent clients reconstruct the declared snapshot and retain known dissent, along with discovery recall, latency, storage, verification cost, and human review effort. If the existing substrates implement the same behavior more simply, the contribution should be the research-event interchange and dispute-preserving export convention, not a new network.

The local `crl/0.1-agent-key-demo` example implements only Ed25519 signatures, canonical event bodies, duplicate elimination and the fixed-point export rule. It generates temporary keys and signs an intentionally false claim, a counterexample and a revision; it is an interchange example, not a scientific result. Focused tests check copied-key impersonation, tampering after digest recomputation, property-order invariance, later disputes of ancestors and explicit missing references. The snapshot manifest identifies the supplied event set, not a globally witnessed cutoff. No WebAuthn owner binding, delegation verifier, revocation service, storage network or comparative trial is implemented. Passing these checks establishes local behavior on the tested inputs, not public-network security or research effectiveness.

## 10. Conclusion

The proposed contribution is an agent-native, publicly citable research lineage whose references carry explicit scientific relationships and whose migrations do not silently wash away known objections. The first milestone is an interoperable, adversarially tested application protocol, not a universal blockchain or a claim to have surpassed existing research institutions.

## References

[1] S. Shilina, “DeScAI: the convergence of decentralized science and artificial intelligence,” *Frontiers in Blockchain* 8, 1657050 (2025). https://doi.org/10.3389/fbloc.2025.1657050

[2] W. Dogah, “Traxia: A Framework for Verifiable, Agent-Native Scientific Publishing,” arXiv:2606.08256v1 (2026). https://arxiv.org/abs/2606.08256

[3] J. Liu et al., “The Last Human-Written Paper: Agent-Native Research Artifacts,” arXiv:2604.24658v3 (2026). https://arxiv.org/abs/2604.24658

[4] P. Koellinger, C. Roessler, and O. Ugot, “Claims: A Bittensor Subnet for Machine-Readable Scientific Evidence,” White Paper v1 (2026). https://claims111.ai/whitepaper

[5] T. Kuhn et al., “Decentralized provenance-aware publishing with nanopublications,” *PeerJ Computer Science* 2, e78 (2016). https://doi.org/10.7717/peerj-cs.78

[6] Z. Guo et al., “Clarus: Coordinating Autonomous Research Agents toward Web-Scale Scientific Collaboration,” arXiv:2606.30246v1 (2026). https://arxiv.org/abs/2606.30246v1

[7] J. Luo, “XScientist: A Git-Like Research Protocol for Long-Running Autonomous Scientific Discovery,” arXiv:2607.12301v2 (2026). https://arxiv.org/abs/2607.12301v2

[8] D. Pratt, “Symposium: Trust via Auditable Records for Communities of AI Scientist Agents,” arXiv:2608.19511v1 (2026). https://arxiv.org/abs/2608.19511v1

[9] Y. Huang et al., “Large Knowledge Model: A Knowledge Foundation for Agentic Science at Scale,” arXiv:2609.27297v2 (2026). https://arxiv.org/abs/2609.27297v2

[10] N. Tomašev et al., “Agentic Economies for Autonomous Scientific Discovery,” arXiv:2609.31562v1 (2026). https://arxiv.org/abs/2609.31562v1

[11] J. Gottweis et al., “Accelerating scientific discovery with Co-Scientist,” *Nature* (2026). https://doi.org/10.1038/s41586-026-10644-y

[12] J. R. Douceur, “The Sybil Attack,” *Peer-to-Peer Systems*, pp. 251-260 (2002). https://doi.org/10.1007/3-540-45748-8_24

[13] W3C, *Web Authentication: An API for Accessing Public Key Credentials, Level 3*. https://www.w3.org/TR/webauthn-3/ (accessed 2 October 2026).

[14] Apple, “About the security of passkeys” (2024). https://support.apple.com/en-us/102195 (accessed 2 October 2026).

[15] A. Rundgren, B. Jordan, and S. Erdtman, *JSON Canonicalization Scheme (JCS)*, RFC 8785 (2020). https://www.rfc-editor.org/rfc/rfc8785

[16] E. Ostrom, “Beyond Markets and States: Polycentric Governance of Complex Economic Systems,” *American Economic Review* 100(3), 641-672 (2010). https://doi.org/10.1257/aer.100.3.641; accompanying Nobel lecture (2009): https://www.nobelprize.org/uploads/2018/06/ostrom_lecture.pdf

[17] Clay Mathematics Institute, *Rules for the Millennium Prize Problems*. https://www.claymath.org/millennium-problems/rules/ (accessed 2 October 2026).
