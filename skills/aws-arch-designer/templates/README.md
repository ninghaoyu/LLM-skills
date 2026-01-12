# AWS 架构设计说明书模板库

本目录包含用于生成 AWS 架构设计说明书的标准化模板。

## 📋 可用模板

### 1. 通用模板 (推荐用于大多数项目)

**文件**: `design_doc_template.md`

- **适用项目类型**:
  - Web 应用
  - AI/ML-RAG
  - AI/ML-GenAI
  - 大数据分析 (批处理、流处理、数据湖)
  - 云迁移项目
  - SaaS 多租户
  - 混合云

- **特点**:
  - 11 个标准章节
  - 49 个结构化占位符
  - 遵循 AWS Well-Architected Framework 六大支柱
  - 包含服务选型、网络、计算、存储、安全、高可用、成本等完整设计

- **输出格式**: `{PROJECT_NAME}_架构设计说明书_v1.0.md`

- **章节清单**:
  1. 设计背景与目标
  2. 架构设计原则
  3. 总体架构概述
  4. 网络架构设计
  5. 计算层设计
  6. 存储与数据库设计
  7. 安全与权限设计
  8. 高可用与灾备设计
  9. 运维与监控设计
  10. 成本与扩展性分析
  11. 风险、假设与待确认事项

---

### 2. AI Agentic 专用模板 (用于 Agent 相关项目)

**文件**: `design_doc_template_ai_agentic.md`

- **适用项目类型**:
  - 🤖 AI/ML-Agentic (Bedrock Agents、LangGraph、Agent 框架)
  - 多 Agent 系统
  - Agent + RAG 混合架构
  - 企业 AI 代理应用

- **特点**:
  - 14 个精心设计的章节 (比通用模板多 3 个)
  - 40+ 个 Agentic AI 特定占位符
  - 融合 AWS Agentic AI 实践要求的 6 大核心能力
  - 专注于 Agent 编排、LLM 推理、工具集成、幻觉防护、负责任 AI
  - 包含能力评估矩阵和 4 阶段实施路线图

- **核心优势**:
  - ✨ 详细的 LLM 选择和 Token 成本控制
  - ✨ Agent 编排与工具集成 (MCP、RESTful API、AWS SDK)
  - ✨ 状态管理和多 Agent 协调设计
  - ✨ Bedrock Guardrails、Prompt 注入防护、幻觉检测
  - ✨ 人类在循环 (HITL) 机制
  - ✨ Agent 特定的监控指标 (成功率、推理延迟、Token 使用率)
  - ✨ Agentic AI 能力评估矩阵 (附录 A)
  - ✨ 项目实施路线图 (4 阶段) (附录 B)

- **输出格式**: `{PROJECT_NAME}_Agentic_架构设计说明书_v1.0.md`

- **章节清单** (14 个):
  1. 设计背景与目标
  2. **AI Agentic 架构设计原则** ⭐
  3. **总体架构概述** (强化 Agent、LLM、工具角色)
  4. 网络架构设计
  5. **推理与 LLM 部署设计** ⭐
  6. **Agent 编排与工具设计** ⭐
  7. **状态管理与记忆设计** ⭐
  8. **向量存储与知识库设计** ⭐
  9. 计算层设计 (Agent 运行环境)
  10. **安全与负责任 AI 设计** (强化)
  11. 高可用与灾备设计
  12. **运维、监控与可观测性设计** (强化)
  13. **成本与性能优化** (强化 Token 成本)
  14. 风险、假设与待确认事项
  - 附录 A: **Agentic AI 能力评估矩阵** ⭐
  - 附录 B: **项目实施路线图** ⭐

---

## 🎯 模板选择指南

### 何时使用通用模板?

✅ 使用 `design_doc_template.md` 当:
- Web 应用、电商、内容管理等传统应用
- RAG 应用 (但不涉及 Agent)
- GenAI 应用 (文本生成、翻译等)
- 大数据分析平台 (离线、实时、数据湖)
- 云迁移项目
- SaaS 多租户应用

### 何时使用 AI Agentic 专用模板?

✅ 使用 `design_doc_template_ai_agentic.md` 当:
- Bedrock Agents 应用
- LangGraph 或其他 Agent 框架应用
- 多 Agent 系统
- Agent + RAG 混合
- Agent + Tool Chain 集成
- 任何涉及"自主 Agent"决策和执行的项目

### 快速判断标准

| 关键词 | 使用模板 |
|-------|---------|
| **"Agent"、"代理"、"自主"** | AI Agentic 专用 ⭐ |
| **"Bedrock Agents"、"LangGraph"** | AI Agentic 专用 ⭐ |
| **"工具调用"、"Tool Chain"、"MCP"** | AI Agentic 专用 ⭐ |
| **"多步推理"、"复杂决策"** | AI Agentic 专用 ⭐ |
| **"RAG"、"知识库"** (纯检索，无 Agent) | 通用模板 |
| **"文本生成"、"翻译"、"摘要"** | 通用模板 |
| **"Web 应用"、"电商"、"API"** | 通用模板 |
| **"数据分析"、"ETL"、"数据湖"** | 通用模板 |

---

## 📝 模板使用流程

### 通用模板使用流程

```
1. Design Writer 步骤 4.0: 项目类型识别
   └─ 如果是 AI/ML-Agentic
      └─ 使用 AI Agentic 专用模板 ❌

   └─ 其他所有类型
      └─ 使用通用模板 ✅

2. 打开 design_doc_template.md
3. 填充 49 个占位符 (按数据源)
4. 检查 11 个章节完整性
5. 验证清单 (8 项检查)
6. 输出: {PROJECT_NAME}_架构设计说明书_v1.0.md
```

### AI Agentic 专用模板使用流程

```
1. Design Writer 步骤 4.0: 项目类型识别
   └─ 如果是 AI/ML-Agentic ✅
      └─ 使用 AI Agentic 专用模板

2. 打开 design_doc_template_ai_agentic.md
3. 填充 40+ 个 Agentic 占位符 (优先级顺序)
   - 推理与 LLM (Token 成本最优先)
   - Agent 编排与工具 (MCP/API 集成)
   - 状态管理和幻觉防护
   - 监控和成本
4. 检查 14 个章节完整性
   - 特别注意第 5-8 章 (Agentic 核心)
   - 特别注意第 10、12、13 章 (强化部分)
5. 完成两个附录
   - 附录 A: Agentic AI 能力评估矩阵
   - 附录 B: 4 阶段实施路线图
6. 验证清单 (18 项详细检查)
7. 输出: {PROJECT_NAME}_Agentic_架构设计说明书_v1.0.md
```

---

## 🔍 占位符对比

### 通用模板占位符

**总计**: 49 个占位符

主要类别:
- 项目基本信息: 4 个
- WAF 原则: 6 个
- 架构设计: 8 个
- 计算存储: 13 个
- 网络安全: 8 个
- 高可用成本: 6 个

### AI Agentic 专用模板占位符

**总计**: 40+ 个占位符 (部分与通用模板共用)

新增/特化类别:
- Agentic 原则: 4 个
- LLM 部署: 8 个
- Agent 编排: 7 个
- 工具集成: 5 个
- 状态管理: 4 个
- 安全防护: 6 个
- 成本优化: 4 个
- 附录内容: 多个

---

## ✅ 验证清单对比

### 通用模板验证清单 (8 项)

- [ ] 11 个章节完整
- [ ] 所有占位符填充
- [ ] Why 和 Trade-off 完整
- [ ] 假设明确标注
- [ ] 格式符合 Markdown
- [ ] 文件名符合规则
- [ ] 中文语言正确
- [ ] 使用正确的模板文件

### AI Agentic 专用模板验证清单 (18 项)

**章节检查** (8 项):
- [ ] 14 个章节完整
- [ ] 第 2 章: AI Agentic 架构设计原则
- [ ] 第 5 章: 推理与 LLM 部署设计 + Token 成本
- [ ] 第 6 章: Agent 编排与工具设计 + MCP
- [ ] 第 7 章: 状态管理与记忆设计
- [ ] 第 8 章: 向量存储与知识库设计
- [ ] 第 10 章: 安全与负责任 AI + Guardrails + 幻觉检测 + HITL
- [ ] 第 12 章: 运维监控 + Agent 特定指标

**附录检查** (2 项):
- [ ] 附录 A: Agentic AI 能力评估矩阵完整
- [ ] 附录 B: 4 阶段项目实施路线图

**内容检查** (6 项):
- [ ] Token 成本分析清晰
- [ ] Guardrails、幻觉检测、HITL 方案明确
- [ ] 所有占位符填充，无 {PLACEHOLDER} 残留
- [ ] Why 和 Trade-off 完整
- [ ] 假设明确标注
- [ ] Markdown 格式和文件名正确

**特殊要求** (2 项):
- [ ] 文件名包含 "Agentic" 标记
- [ ] 使用 AI Agentic 专用模板

---

## 📖 占位符填充指南

### 通用模板占位符示例

```markdown
{PROJECT_NAME} = "电商平台迁移"
{DATE} = "2026-01-12"
{BUSINESS_GOALS} =
  - 降低运维成本 30%
  - 支持日活 10 万用户
  - 99.9% 可用性

{COMPUTE_SERVICE_CHOICE} = "EC2 Auto Scaling Group"
{COMPUTE_WHY} =
  - 现有 Spring Boot 应用，迁移成本最低
  - 团队熟悉 EC2 运维

{COMPUTE_PROS} =
  - 灵活性高
  - 成本相对较低

{COMPUTE_CONS} =
  - 需要维护操作系统

{COMPUTE_ALTERNATIVES} =
  - ECS Fargate: 若想减少 OS 管理工作
  - Lambda: 若应用改造为无状态微服务
```

### AI Agentic 专用模板占位符示例

```markdown
{LLM_MODEL_CHOICE} = "Claude 3.5 Sonnet"
{LLM_CHOICE_WHY} =
  - 推理能力强，适合复杂决策
  - 支持中文，处理国内应用
  - Token 成本相对较低

{TOKEN_COST_CONTROL_STRATEGY} =
  1. Prompt 缓存: 减少重复调用 30%
  2. 上下文管理: 控制 Token 窗口
  3. 模型降级: 简单任务使用 Haiku

{AGENT_ORCHESTRATOR_CHOICE} = "Bedrock Agents"
{AGENT_ORCHESTRATOR_WHY} =
  - 完全托管，无需运维
  - 与 Bedrock 无缝集成
  - 支持 OpenAPI/Lambda 工具

{ACTION_GROUPS_DESIGN} =
  | Group | Function | Service | Latency |
  |-------|----------|---------|---------|
  | API Call | 查询数据库 | Lambda/RDS | <200ms |
  | Tool Call | 调用工具 | Lambda | <500ms |

{HALLUCINATION_DETECTION} =
  1. 事实检查: 与 RAG 知识库对比
  2. 置信度标记: 输出包含置信度评分
  3. 人类审核: 高风险决策上报到 HITL
```

---

## 🚀 快速开始

### 为通用模板项目

1. 复制 `design_doc_template.md`
2. 替换 49 个占位符
3. 检查 11 个章节
4. 执行 8 项验证清单
5. 保存输出文件

### 为 AI Agentic 项目

1. 复制 `design_doc_template_ai_agentic.md`
2. 优先填充 LLM 和 Agent 相关占位符
3. 完成 Token 成本控制、幻觉防护、HITL 等关键章节
4. 完成两个附录 (能力评估矩阵、实施路线图)
5. 执行 18 项详细验证清单
6. 保存输出文件

---

## 📞 常见问题

### Q: 我的项目涉及 Agent + RAG，应该用哪个模板?

**A**: 使用 **AI Agentic 专用模板**
- 如果 Agent 是核心 (执行工具、多步推理)
- Agent 使用 RAG 作为知识源，这是常见的混合架构

如果只是 RAG (纯检索，无 Agent 决策)，使用通用模板。

---

### Q: 通用模板和 AI Agentic 模板可以混用吗?

**A**: **强烈禁止** ❌

- 不要在 AI Agentic 项目中用通用模板
- 不要在其他项目中用 AI Agentic 专用模板
- 选择正确的模板是关键，影响文档的完整性和质量

---

### Q: 如何添加新的项目特定占位符?

**A**:
1. 在对应模板中添加新占位符 `{YOUR_PLACEHOLDER}`
2. 在模板映射表中记录新占位符及其数据源
3. 更新验证清单
4. 在使用文档中说明

建议先与团队讨论，确保新占位符的通用性。

---

### Q: 可以自己创建新模板吗?

**A**: 可以，但建议:
1. 从现有模板复制
2. 确保包含必要的架构设计内容
3. 记录模板的适用项目类型
4. 创建对应的验证清单

---

## 📚 参考资源

- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- AWS Agentic AI: https://aws.amazon.com/blogs/machine-learning/agentic-ai/
- Bedrock Agents: https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- LangGraph: https://langchain-ai.github.io/langgraph/

---

**最后更新**: 2026-01-12
**维护者**: AWS 架构设计 Skill 团队
