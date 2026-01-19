# CHANGELOG - AWS 架构设计说明书生成器

本文档记录 AWS 架构设计说明书生成器 Skill 的完整版本历史。

---

## v1.8 (2026-01-18) - 结构优化版 ✨

**核心改进**:
- ✅ **重新编排流程顺序** - 步骤 2（架构决策）和步骤 3（架构图处理）互换，逻辑更严谨
  - 原顺序: Material Parser → Diagram → Decisioning
  - 新顺序: Material Parser → Decisioning → Diagram Processing
  - **理由**: 必须先做架构决策，才能生成架构蓝图，才能绘制架构图
- ✅ **新增流程图可视化** - ASCII 流程图，快速理解整体流程
- ✅ **新增决策点检查** - 步骤 1 → 2 之间增加 P0 问题检查点
- ✅ **精简模板选择说明** - 从 2 处合并为 1 处（步骤 4）
- ✅ **强化禁止事项** - 表格化 + emoji 标记，更加醒目
- ✅ **移除冗余版本历史** - 保留最近 2 版，详细历史移到 CHANGELOG.md
- ✅ **减少 25% 冗余内容** - 精简重复说明，提升逻辑严谨性

**文件变更**:
- 修改: `SKILL.md` (642 行，优化前 750 行)
- 新增: `CHANGELOG.md` (本文档)

**改进细节**:
- 步骤 0: 标题改为"案例学习文件识别与分析"（更准确）
- 步骤 1: 增加"检测用户架构图"任务
- 决策点检查: 新增表格化检查清单
- 步骤 2: 强化 WAF 检查说明，增加项目特定检查
- 步骤 3: 拆分为"情况 1"和"情况 2"，逻辑更清晰
- 步骤 4: 模板选择规则表格化
- 步骤 5: 增加 WAF 六大支柱复审
- 核心原则: 改为表格化 5 条铁律
- 禁止事项: 分类为 AI/ML、大数据、通用三大类，表格化呈现

---

## v1.7 (2026-01-13) - 精简优化版

**核心改进**:
- ✅ SKILL.md 精简为 950 行（原 1534 行，减少 38%）
- ✅ 分离出 4 个专题文档
  - `DESIGN_WRITER_GUIDE.md` - 步骤 4 的详细实施指南
  - `EXAMPLES.md` - 4 个完整使用示例
  - `OPTIMIZATION_GUIDE.md` - 脚本优化和实施建议
  - `BEST_PRACTICES.md` - 最佳实践和检查清单
- ✅ 保留完整的功能和细节（通过链接访问）
- ✅ 提升可读性和快速上手体验
- ✅ 创建原始备份 (`SKILL.md.backup`)

**文件变更**:
- 修改: `SKILL.md`
- 新增: `DESIGN_WRITER_GUIDE.md`
- 新增: `EXAMPLES.md`
- 新增: `OPTIMIZATION_GUIDE.md`
- 新增: `BEST_PRACTICES.md`
- 新增: `SKILL.md.backup`

---

## v1.6 (2026-01-12) - 运维监控强化版 ⭐⭐

**重要更新: 运维监控完整性 + AI Agentic 与 RAG 关系澄清**

**关键改进**:

### 1. 运维、监控与可观测性能力强化

- ✅ 在 WAF 检查清单中新增"卓越运营"完整章节
  - 日志聚合与管理（采样策略、脱敏、保留期）
  - 监控与告警（指标定义、告警阈值、分级响应）
  - 分布式追踪与性能诊断（X-Ray 集成）
  - 仪表盘与可视化要求
  - 成本监控与异常检测
  - 自动化运维与 On-Call 体系
- ✅ AI/ML 项目特有监控指标（Token 使用、推理延迟、幻觉率、数据漂移）
- ✅ 大数据项目特有监控指标（ETL 成功率、消费延迟、数据质量、存储成本）
- ✅ Design Reviewer 阶段新增"运维监控与可观测性检查"（5.4 章节）
  - 日志、监控、告警、追踪、仪表盘、自动化的完整检查清单
  - AI/ML 和大数据项目的特定监控要求

### 2. AI Agentic 与 RAG 关系澄清

- ✅ **关键认识**: RAG 是可选的知识库增强，不是 Agentic 必需组件
- ✅ 修改架构模式选择决策树
  - 纯 Agentic (无 RAG): API 编排、流程自动化、任务执行
  - Agentic + RAG: 知识库增强的任务系统（可选）
  - 纯 RAG: 知识库问答、文档检索（无任务编排）
- ✅ 更新模式对比表（新增"是否包含 RAG"列）
- ✅ 更新架构模式速查表（明确关键词区分）
- ✅ 更新 AI Agentic 模板
  - 第 8 章改为"仅当需要 RAG 增强时"
  - 新增 8.1 节判断标准（什么时候需要 RAG）
  - 新增 8.5 节 RAG 与 Agent 的 3 种集成方式（工具型、上下文型、混合型）
  - 关键提醒：RAG 是可选增强，不是必须部分

### 3. 禁止事项强化

- ❌ **禁止盲目为所有 Agentic 项目添加 RAG**
- ❌ 只在确实需要知识库检索时才包含 RAG
- ✅ 基于实际需求进行决策（见 8.1 判断标准）

**新增文件更新**:
- `references/waf_checklist.md`: 完整运维监控检查清单
- `templates/design_doc_template_ai_agentic.md`: 明确 RAG 可选性

**关键学习要点**:
- Agentic AI 的核心是**任务编排与自主推理**，RAG 是**可选的知识库补充**
- 架构模式应该基于**业务需求**，而非假设需要 RAG
- 运维与监控是系统稳定性的**关键支撑**，不仅仅是告警

---

## v1.5 (2026-01-07) - 案例学习支持 ⭐⭐

**重大更新: 案例学习文件支持与参考**

**新增功能**:

### 1. 案例学习文件检测与识别

- ✅ 支持文件名模式识别 (case study, 案例, 迁移方案等)
- ✅ 支持内容关键词识别
- ✅ 自动判定文件是否为案例学习文件

### 2. 结构化信息提取（从案例文件中）

- ✅ **项目背景**: 行业、公司规模、现状基础设施
- ✅ **痛点分析**: 问题描述、影响、严重程度
- ✅ **AWS 解决方案**: 服务组合、架构模式、配置
- ✅ **关键指标**: 可用性、性能、流量、数据量等
- ✅ **预期收益**: 成本节省、性能提升、业务影响
- ✅ **经验教训**: 关键经验和最佳实践
- ✅ **架构图**: 自动检测（Markdown 和 HTML 格式）

### 3. 新项目与案例的关联匹配

- ✅ 相关性分数计算（0-100）
- ✅ 多维度匹配（行业、规模、痛点、功能）
- ✅ 相关性等级判定（高/中/低）
- ✅ 可复用服务提取

### 4. 参考加速决策流程

- ✅ 从案例中快速参考架构模式
- ✅ 提取验证过的服务组合
- ✅ 基于案例的成本基线预测
- ✅ 吸取经验教训规避风险

**新增实现文件**:
- `scripts/case_study_analyzer.py`: 案例学习分析引擎（850+ 行）
  - `CaseStudyDetector`: 案例检测器
    - `detect()`: 通过文件名和内容检测
    - 支持 20+ 种案例关键词（中文和英文）
  - `CaseStudyExtractor`: 信息提取器
    - `_extract_background()`: 背景信息提取
    - `_extract_pain_points()`: 痛点提取
    - `_extract_aws_solution()`: 方案提取
    - `_extract_key_metrics()`: 指标提取
    - `_extract_benefits()`: 收益提取
    - `_extract_lessons()`: 经验提取
    - `_detect_diagram()`: 架构图检测
  - `CaseStudyMatcher`: 匹配和关联器
    - `calculate_relevance()`: 相关性评分
    - `extract_reusable_services()`: 可复用服务提取
  - `CaseStudyAnalyzer`: 主分析器
    - `analyze()`: 完整分析流程
    - `match_with_project()`: 与新项目匹配

**新增设计文档**:
- 第 3.0 节: 案例学习文件处理（Case Study Analysis）
  - 案例文件识别规则
  - 结构化提取信息
  - 与新项目的关联机制
- 第 3.2.4 节: 基于案例学习文件的架构设计完整示例

**关键改进**:
- 参考加速: 相似项目可直接参考已验证的案例
- 成本基线: 基于案例的成本数据预测新项目
- 风险规避: 吸取案例的经验教训
- 自动化匹配: 智能关联相关案例
- 完整信息链: 从案例中提取背景、方案、结果的全链路

---

## v1.4 (2026-01-07) - 架构图生成能力 ⭐⭐

**重大更新: 架构图自动生成能力**

**新增功能**:

### 1. 整体流程升级

- ✅ 整体流程升级为 **5-Step Pipeline**，新增架构图生成步骤
- ✅ 用户架构图检测与识别能力（Vision/OCR）
- ✅ 架构蓝图自动构建（基于架构决策）
- ✅ MCP Server 集成: `awslabs-aws-diagram-mcp-server`
- ✅ 架构图与需求的一致性检查
- ✅ 架构图文字描述自动生成

### 2. 两种处理路径

- **Case 1: 用户提供架构图**
  - 识别验证 → 文字描述 → 一致性检查
- **Case 2: 用户无架构图**
  - 蓝图构建 → MCP 生成 → 文字描述 → 一致性检查

**新增实现文件**:
- `scripts/diagram_generator.py`: 架构图生成核心模块
  - `DiagramGenerator`: 主生成器
  - `BlueprintBuilder`: 蓝图构建器
  - `DiagramValidator`: 一致性验证器
  - `DiagramDescriptionGenerator`: 文字描述生成器
- `scripts/mcp_diagram_client.py`: MCP Server 集成模块
  - `MCPDiagramClient`: MCP 客户端
  - `DiagramGenerationOrchestrator`: 编排器
  - 完整的蓝图验证和请求处理

**新增设计文档**:
- 第 2-A 节: Architecture Diagram Generation 详细设计
- 第 6.4 节: 架构图生成执行要点
  - MCP Server 集成工作流
  - 架构蓝图构建规则
  - MCP 响应处理
  - Design Reviewer 阶段的架构图检查

**关键改进**:
- 视觉化架构表示: 所有设计都包含生成的或用户提供的架构图
- 自动一致性检查: 架构图与文档的内容验证
- 降级方案: MCP Server 不可用时的文本描述备选
- 完整的检查流程: 从架构图检测到文档集成的全链路

---

## v1.3 (2026-01-06) - 大数据与 AI/ML 架构 ⭐⭐

**重大更新: 大数据与 AI/ML 架构设计能力**

**新增架构模式（9 个）**:

### 大数据架构
- 批量数据处理平台 (S3 + Glue + Athena/Redshift)
- 实时数据处理平台 (Kinesis + Lambda + DynamoDB)
- 数据湖架构 (Lake Formation + S3 + Glue)
- 大数据计算集群 (EMR + Spark)

### AI/ML 架构
- GenAI 应用架构 (Bedrock + Lambda)
- RAG 架构 (Bedrock KB + OpenSearch)
- AI Agentic 系统 (Bedrock Agents + Step Functions)
- ML 训练推理平台 (SageMaker)
- 多模态 AI 架构 (Bedrock + Rekognition + Textract)

**新增服务选型决策**:
- **AI/ML 服务决策表**: LLM 推理、模型选择、向量数据库、Agent 框架、模型部署
- **大数据服务决策表**: 离线分析、ETL、实时流、流处理、数据仓库、数据湖查询

**新增特殊 WAF 检查**:
- **AI 特有检查点**: Token 成本控制、推理性能优化、Prompt Security、幻觉检测、MLOps
- **大数据特有检查点**: 存储成本优化、查询性能、数据一致性、数据治理、自动化

**其他更新**:
- 架构模式选择决策树（Python 伪代码）
- Architecture Decisioning Prompt 增加 AI/大数据特殊处理（任务 5）
- 附录增加架构模式速查表和服务选型速查表（5 个速查表）

**文件变更**:
- 修改: `DEEPV.md` (新增第 A.2-A.5 节)
- 修改: `references/architecture_patterns.md` (新增 9 个模式)
- 修改: Architecture Decisioning Prompt (新增 AI/大数据处理)

---

## v1.2 (2026-01-06) - 架构决策引擎 ⭐

**核心更新: Architecture Decisioning（架构决策引擎）**

**新增功能**:
- ✅ 服务选型决策树和对比评估流程
- ✅ AWS Well-Architected Framework 六大支柱强制检查机制
- ✅ 服务选型完整示例（RDS vs Aurora 对比）
- ✅ Architecture Decisioning Prompt 模板
- ✅ WAF 检查强制执行流程和阻断级别定义
- ✅ 复杂度评分机制防止过度设计

**优化改进**:
- 验收标准增加架构决策质量和可追溯性要求
- 流程图标注 WAF 评估环节

**文件变更**:
- 修改: `DEEPV.md` (新增第 3.3 节 - 架构决策引擎)
- 新增: Architecture Decisioning Prompt (Prompt 模板)
- 修改: 第 6 节 - 实施指南（WAF 强制执行）

---

## v1.1 (2026-01-06) - Material Parser 增强

**新增功能**:
- ✅ Material Parser 对零散材料的处理能力
- ✅ 5 大关键要素提取清单（功能需求、非功能需求、合规性、预算、流量）
- ✅ 主动交互机制和追问优先级矩阵
- ✅ 从会议记录到结构化数据的完整示例
- ✅ Material Parser Prompt 模板

**文件变更**:
- 修改: `DEEPV.md` (新增第 3.1-3.2 节)
- 新增: Material Parser Prompt (Prompt 模板)

---

## v1.0 (初始版本)

**初始功能**:
- ✅ 基础架构设计 Skill 需求定义
- ✅ 6 步工作流程设计
- ✅ 多模态材料解析能力
- ✅ 架构决策框架
- ✅ 文档生成和审查机制

**文件创建**:
- `SKILL.md` - 主文档
- `DEEPV.md` - 深层设计
- `templates/design_doc_template.md` - 通用模板
- `references/architecture_patterns.md` - 架构模式库
- `references/waf_checklist.md` - WAF 检查清单

---

## 版本编号规则

- **v1.x** - 主版本号：重大功能更新、架构调整
- **v1.x.y** - 次版本号：功能增强、新增模板
- **v1.x.y.z** - 修订版本号：Bug 修复、文档更新

---

## 相关文档

- [SKILL.md](./SKILL.md) - 主文档（精简版，快速上手）
- [DEEPV.md](./DEEPV.md) - 深层设计（完整版，技术细节）
- [EXAMPLES.md](./EXAMPLES.md) - 使用示例
- [BEST_PRACTICES.md](./BEST_PRACTICES.md) - 最佳实践
- [OPTIMIZATION_GUIDE.md](./OPTIMIZATION_GUIDE.md) - 优化指南

---

**最后更新**: 2026-01-18
