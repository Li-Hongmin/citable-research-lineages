# CRL 文献与实现地图

检索与原始来源核验日期：2026-10-02。范围是开放 AI 科研协作、可迁移研究对象、争议记录、身份授权和公共治理；不是自主科研能力的全面综述。本地文献缓存与检索矩阵未随本仓库发布；下文公开链接提供核对入口。

## 决策与概念关系

本轮需要决定：是否需要新链或新网络；如何保护参与者身份；CRL 相对已有系统还能提出什么可检验的贡献。区分这些路径的直接观测，是已有协议的对象与导出规则、实际凭证作用域，以及同一快照在不同实现上的导出结果。

```text
公共参与与协作组织
  Polymath / DeScAI / Clarus
        |
        +-- 人与 agent 身份 --> WebAuthn + 有限委托
        |                       Sybil: 密钥数 != 独立参与者数
        |
        +-- 资源与治理 -------> Ostrom / Agentic Economies
        |
        +-- 可迁移科研对象 ---> Ara / XScientist
        |
        +-- 发布与保存 -------> nanopublications / Symposium / Git
        |
        +-- 主张与证据发现 ---> LKM / Claims
                                |
                                +-- CRL 待测: 已知 incoming dispute 随成果迁移
```

这张图连接机制，不表示所有项目实现了同一标准，也不把概念提案、原型和实证能力混成一个排行榜。每个分支已能支持当前选型；暂不继续扩展不会改变这一选择的文献。

## 核心文献

“相关段落已读”仅指用于下述判断的原文部分，不表示逐页阅读全文。“摘要已读”只支持摘要中的窄主张，不能支持未检查的实现细节。

| 工作与版本 | 直接相关的机制 | 阅读层级与边界 | 对 CRL 的影响 |
|---|---|---|---|
| [Symposium, 2608.19511v1](https://arxiv.org/abs/2608.19511v1) | 异构 agents 共用不可变科研历史，反驳及更正新增记录 | PDF 的对象、论证和实现说明相关段落；示例 community 为 synthetic | 不能把持久研究记录或分离接受政策称为首创；比较其发布对象与 incoming dispute 导出 |
| [XScientist, 2607.12301v2](https://arxiv.org/abs/2607.12301v2) | local-first、typed/content-addressed 研究状态、失败分支、可继续的 ARA 导出 | 原文研究对象及相关工作段落；没有运行其系统 | 可迁移研究状态已经存在；需比较多作者输入、快照边界和后来的反驳 |
| [Clarus, 2606.30246v1](https://arxiv.org/abs/2606.30246v1) | project-agent-resource、开放网络身份与发现、资源权限 | 原文 §2.4、§3.4、§4.5 等相关段落 | 开放 agent 科研合作不是空白；CRL 应定义较薄的交换语义而非重新建设全栈 |
| [Agentic Economies, 2609.31562v1](https://arxiv.org/abs/2609.31562v1) | 资源、credit、国际协作、双用途与制度问题 | 原文治理与限制段落；概念性判断，不是安全部署试验 | 责任主体与资源许可不能只用签名或投票替代 |
| [LKM, 2609.27297v2](https://arxiv.org/abs/2609.27297v2) | 可寻址主张、支持与反对证据的检索 | 摘要及原文 Limitations；100 篇提取检查测 hallucination，未测 omission | 检索提升不证明反驳没有遗漏；争议发现 recall 要单独测 |
| [Federation Is Nearly Free, 2608.25215v1](https://arxiv.org/abs/2608.25215v1) | 蛋白质表征流程中的 federation、harness、模型与提示消融 | 摘要已读，限定任务 | 工具 federation 成本结果不能外推为开放科研网络有效性 |
| [Traxia, 2606.08256v1](https://arxiv.org/abs/2606.08256v1) | agent 身份、签名发表、复现、信誉、四层审稿 | 原文 §6.1、§8；最终 human arbiter accept/reject；架构提案 | 接受决定不是记录交换；不把其架构描述写成已经获得实证的保证 |
| [Ara, 2604.24658v3](https://arxiv.org/abs/2604.24658v3) | 主张、证据、代码、探索轨迹及机器可执行包 | 原文 §2、§5 等相关段落；实验结果未独立复现 | 复用结构化研究材料；结构通过不等于发现正确 |
| [Co-Scientist, Nature 2026](https://doi.org/10.1038/s41586-026-10644-y)，[原预印本](https://arxiv.org/abs/2502.18864) | Gemini 多 agent 生成、批评、演化假设；特定生物医学验证 | 正式发表元数据与摘要；主文和两份补充文件已在库 | 是能力与工作流参照，不是公众多运营者交换协议 |
| [DeScAI, 2025](https://doi.org/10.3389/fbloc.2025.1657050) | 去中心化科学与 AI 的理论综合 | 摘要已读，概念框架 | 不能把 DeSci + agents 组合当作新概念 |
| [Nanopublications, 2016](https://doi.org/10.7717/peerj-cs.78) | provenance-aware RDF 单元、分布式发布与取回；底层发布和上层服务分离 | PDF 的架构与服务分层相关段落 | 直接发布基线；验证争议导出规则是否可作为已有网络的应用约定 |
| [Gowers & Nielsen, 2009](https://doi.org/10.1038/461879a) | 协作数学的历史检索入口 | 仅核验元数据；出版商页面受限，检出的作者 PDF 返回 404 | 不以未取得的正文支持具体组织成效判断 |
| [Ostrom, 2010](https://doi.org/10.1257/aer.100.3.641) | 多中心、相互作用的治理机构 | 已读同题 [2009 Nobel lecture](https://www.nobelprize.org/uploads/2018/06/ostrom_lecture.pdf) 的相关段落；不是 AER 出版版本 | 为分离节点、问题与公益项目责任提供背景，不是 AI 网络实验依据 |
| [Douceur, 2002](https://doi.org/10.1007/3-540-45748-8_24) | Sybil 身份倍增与独立性假设 | Microsoft Research 作者稿摘要及论证相关段落 | 多个公钥、passkeys 或模型不自动意味着多个独立的人 |

另保留论文原有 [Claims white paper](https://claims111.ai/whitepaper) 作为相邻项目；本轮只核验官方摘要与 PDF 入口，未将其全文贡献提升为已核验的研究结论。

## 标准与已有开发

| 原始来源 | 本轮可采用的内容 | 不应宣称的内容 |
|---|---|---|
| [Apple passkey security](https://support.apple.com/en-us/102195) 与 [WebAuthn](https://www.w3.org/TR/webauthn-3/) | 公私钥、RP/origin 绑定、challenge、用户验证；Apple E2EE 同步与恢复 | Apple 专有身份标准；任意域名可直接使用旧凭证；永不泄露或全失后无条件恢复 |
| [Bitcoin BIP-32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) 与 [钱包安全](https://bitcoin.org/en/secure-your-wallet) | 私钥控制、公钥可分发、seed 派生及钱包备份、硬件钱包和多签 | 上链自动保护私钥，或自动恢复被盗身份 |
| [Bitcoin BIP-3](https://github.com/bitcoin/bips/blob/master/bip-0003.md) | 提案记录不等于采用共识 | 单个文档维护者拥有协议采用或科学真理的最终裁决权 |
| [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) | 用维护的 JCS 库取得确定性签名输入 | 自写 JSON 规范化与密码算法 |
| [Nostr NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md) | 签名事件及 relay 模型的参考 | CRL Ed25519/JCS 示例与 Nostr secp256k1/Schnorr wire format 兼容 |
| [Symposium 开源实现](https://github.com/ndexbio/symposium) | README、规范入口及 synthetic 示例已查；现有发布基础设施候选 | 本轮已完成部署或跨系统兼容测试 |
| [XScientist 实现](https://github.com/smileformylove/XScientist) | README 区分 alpha、发布版与 main 未发布能力 | 将 main 中所有功能当作发布版功能；本轮已运行它 |

## 设计判断与待测假设

**原始来源直接支持的事实：**开放协作架构、可迁移研究材料和记录/接受分层已有前例。通行密钥与钱包都用公私钥，但 WebAuthn 的凭证作用域和交互与传统钱包不同。密钥数不是独立参与者数。

**本项目的设计判断：**第一版不用原生币或强制区块链；人使用平台无关 WebAuthn，agent 使用独立短期工作密钥；研究材料沿用已有存储与传输。节点可以管理成本和安全范围，但不能把本地选择伪装成全网科学结论。贡献签名、原创性、署名与法律权利分开处理。

**尚待检验的假设：**相对于使用同一结构化 schema 的 Git、nanopublications、XScientist/Symposium 接口，固定快照内的 incoming dispute 闭包能减少迁移时漏掉反驳，且不会使发现和人工筛选成本不可接受。以后来反驳、缺失材料和噪声事件做小规模对照，测争议保留、发现 recall、耗时与审议负担。若基线更简单且效果相同，CRL 应成为交换约定，不必另建网络。

身份选型的下一项直接实验是：真实浏览器注册、明确授权一个 agent、撤销后拒绝新提交；同时检查错误 origin 和重复 challenge。当前 `crl_events.py` 只验证工作公钥控制、内容完整性与给定快照的导出规则，没有 owner 绑定，也不证明科学成果或现实网络安全。

## 本地获取边界

矩阵收录 14 条研究记录，12 条缓存了摘要；可用的参考文献列表与部分前向引用也已缓存。前向图仅含 nanopublication 记录的一个 OpenAlex 检索页，不是完整引文图。

当前有 12 份论文主文/作者稿，另有 1 份相关 Nobel lecture。不能把 lecture 算作 AER 正式全文。Gowers/Nielsen 的合法全文本轮未取得：出版商页面需要进一步访问条件，Brave 检出的作者地址 `https://michaelnielsen.org/papers/mcm.pdf` 返回 404。它仍保留为元数据记录。

Co-Scientist 的主文与两份补充文件复用已有库文件。其他已取得主文不等于已完整取得补充材料；PeerJ 的补充查询未成功解析，未声称补充覆盖完整。所有上述读取层级均与下载状态分开，不把下载、验签或测试通过当成科学成功。

论文库记录已缓存，`exports/research-library.bib` 已刷新；导出器跳过了一些既有的非标准 BibTeX 类型记录，因此不是全库无遗漏导出。未为此修改与本项目无关的记录。
