# 模板快速参考卡

## 🎯 快速判断: 选择哪个模板?

### 关键词检查清单

看到以下关键词? → **使用 AI Agentic 专用模板** ⭐

- ✅ **"Agent"、"代理"、"自主系统"**
- ✅ **"Bedrock Agents"**
- ✅ **"LangGraph"**
- ✅ **"工具调用"、"Tool Call"**
- ✅ **"MCP"、"Model Context Protocol"**
- ✅ **"多步推理"、"Reasoning"**
- ✅ **"幻觉"、"Hallucination"**
- ✅ **"人类在循环"、"HITL"**
- ✅ **"Token 成本"**
- ✅ **"Prompt 注入防护"**

### 反面特征: 使用通用模板

看到以下? → **使用通用模板** (保持原样)

- ✅ Web 应用、电商
- ✅ 纯 RAG (无 Agent 决策)
- ✅ 文本生成、翻译、摘要
- ✅ 大数据分析、ETL
- ✅ 云迁移
- ✅ SaaS 应用

---

## 📊 模板对比一览表

| 特性 | 通用模板 | AI Agentic |
|-----|---------|-----------|
| **章节数** | 11 | **14** |
| **占位符** | 49 | **40+** |
| **验证项** | 8 | **18** |
| **Agent 设计** | ❌ | ✅ |
| **Token 成本** | ❌ | ✅ |
| **幻觉检测** | ❌ | ✅ |
| **能力矩阵** | ❌ | ✅ |
| **路线图** | ❌ | ✅ |
| **适用范围** | 10+ 类型 | Agentic 专用 |

---

## 🚀 快速开始

### 3 步使用 AI Agentic 模板

```
1️⃣ 打开 design_doc_template_ai_agentic.md

2️⃣ 按优先级填充:
   ① LLM 部分 (Token 成本最优先!)
   ② Agent 编排与工具 (MCP 集成)
   ③ 安全性 (Guardrails、幻觉检测、HITL)
   ④ 其他章节

3️⃣ 执行 18 项验证清单
   ✓ 14 个章节完整
   ✓ 两个附录完整
   ✓ 所有占位符填充
```

### 3 步使用通用模板

```
1️⃣ 打开 design_doc_template.md

2️⃣ 按顺序填充 49 个占位符

3️⃣ 执行 8 项验证清单
   ✓ 11 个章节完整
   ✓ 所有占位符填充
```

---

## 📝 核心章节对比

### 通用模板 (11 章)

1. 设计背景与目标
2. 架构设计原则
3. 总体架构概述
4. 网络架构设计
5. **计算层设计**
6. 存储与数据库设计
7. 安全与权限设计
8. 高可用与灾备设计
9. 运维与监控设计
10. 成本与扩展性分析
11. 风险、假设与待确认事项

### AI Agentic 专用模板 (14 章)

1. 设计背景与目标
2. **⭐ AI Agentic 架构设计原则**
3. **⭐ 总体架构概述** (加强 Agent、LLM、工具)
4. 网络架构设计
5. **⭐ 推理与 LLM 部署设计**
6. **⭐ Agent 编排与工具设计**
7. **⭐ 状态管理与记忆设计**
8. **⭐ 向量存储与知识库设计**
9. 计算层设计 (Agent 运行环境)
10. **⭐ 安全与负责任 AI 设计**
11. 高可用与灾备设计
12. **⭐ 运维、监控与可观测性设计**
13. **⭐ 成本与性能优化**
14. 风险、假设与待确认事项

**⭐ = Agentic AI 新增或强化章节**

---

## ✅ AI Agentic 模板关键检查点

生成 AI Agentic 设计文档时必须验证:

### 推理与 LLM (第 5 章)
- [ ] LLM 模型选择明确
- [ ] Token 成本控制策略清晰
- [ ] 部署方案 (Bedrock/SageMaker 选择) 合理

### Agent 编排与工具 (第 6 章)
- [ ] Agent Orchestrator 选择 (Bedrock Agents/LangGraph/自定义)
- [ ] Action Groups 设计完整
- [ ] 工具集成协议 (MCP/API/Lambda) 明确
- [ ] 错误处理和重试机制定义清晰

### 安全与负责任 AI (第 10 章)
- [ ] Bedrock Guardrails 配置
- [ ] Prompt 注入防护方案
- [ ] 幻觉检测机制
- [ ] 人类在循环 (HITL) 机制
- [ ] 数据隐私和脱敏策略

### 两个附录 (A & B)
- [ ] 附录 A: Agentic AI 能力评估矩阵 (6 大能力)
- [ ] 附录 B: 4 阶段项目实施路线图

---

## 💡 常见填充示例

### AI Agentic 项目 - LLM 选择

```
{LLM_MODEL_CHOICE} = Claude 3.5 Sonnet

{LLM_CHOICE_WHY} =
- 推理能力强，支持复杂多步决策
- Token 成本相对较低 ($0.0008/1K input)
- 支持中文，适合国内应用

{TOKEN_COST_CONTROL_STRATEGY} =
1. Prompt 缓存: 减少重复调用成本 30%
2. 上下文管理: 控制 Token 窗口在 4K
3. 模型降级: 简单任务使用 Haiku 模型
```

### AI Agentic 项目 - Agent 编排

```
{AGENT_ORCHESTRATOR_CHOICE} = Bedrock Agents

{ACTION_GROUPS_DESIGN} =
| Action Group | Function | 延迟 |
|---|---|---|
| DatabaseQuery | 查询 RDS 数据 | <200ms |
| APICall | 调用外部 API | <500ms |
| Calculation | 进行复杂计算 | <100ms |
```

### AI Agentic 项目 - 幻觉防护

```
{HALLUCINATION_DETECTION} =
1. 事实检查: 与 RAG 知识库对比
   - 相关性评分 > 0.8
   - 置信度评分 > 0.7

2. 人类在循环: 高风险决策上报
   - 金融交易
   - 医疗建议
   - 法律意见
```

---

## 🔗 相关资源

### 文档
- 📖 **完整指南**: `README.md`
- 📊 **更新总结**: `TEMPLATE_UPDATES_SUMMARY.md`
- 📋 **实施完成**: `IMPLEMENTATION_COMPLETE.md`

### 模板
- 📄 **通用模板**: `design_doc_template.md` (11 章)
- 🤖 **AI Agentic 专用**: `design_doc_template_ai_agentic.md` (14 章)

### SKILL 文档
- 🎯 **步骤 4.0**: 模板选择说明
- 🔍 **步骤 4.1**: 占位符映射
- 📝 **步骤 4.6**: Prompt 模板

---

## ⚡ 速记表

| 需求 | 模板 | 章节 | 占位符 | 验证项 |
|-----|-----|-----|--------|--------|
| Web/数据/迁移 | 通用 | 11 | 49 | 8 |
| **AI Agentic** | **Agentic** | **14** | **40+** | **18** |

---

**最后更新**: 2026-01-12
**版本**: v1.0
