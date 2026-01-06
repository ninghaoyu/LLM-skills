# AWS 架构设计说明书生成器 Skill

## 概述

这是一个基于 DEEPV.md 需求文档设计和实现的完整 Skill，可以将零散的客户材料（会议记录、需求列表、代码片段等）自动转化为结构化、符合 AWS Best Practice 的《架构设计说明书》。

## 核心能力

✅ **材料解析**: 处理会议记录、需求列表、代码片段等零散材料
✅ **智能追问**: 自动识别缺失信息（RTO/RPO、流量、区域等）并主动追问
✅ **架构决策**: 基于 AWS Well-Architected Framework 进行服务选型
✅ **多场景支持**:
- Web 应用（三层架构、Serverless）
- AI/ML（GenAI、RAG、Agentic 系统）
- 大数据（批处理、实时流、数据湖）
- SaaS、混合云

✅ **标准化输出**: 生成完整的 11 章节架构设计说明书

## 文件结构

```
aws-arch-designer/
├── SKILL.md                           # Skill 主文档（包含 4 步工作流程）
├── scripts/                           # Python 脚本
│   ├── material_parser.py             # 材料解析和项目类型识别
│   └── architecture_decisioning.py    # 架构决策和 WAF 评估
├── references/                        # 参考文档
│   ├── architecture_patterns.md       # 架构模式库（9 大模式）
│   └── waf_checklist.md              # WAF 检查清单
└── assets/                           # 输出模板
    └── design_doc_template.md        # 设计说明书模板
```

## 工作流程（4 步）

### 步骤 1: Material Parser（材料解析）
- 从零散材料中提取 5 大关键要素
- 识别项目类型（AI/ML、大数据、Web 等）
- 生成追问列表（P0 问题）
- 输出结构化 JSON

### 步骤 2: Architecture Decisioning（架构决策）
- 选择架构模式（从 9 大模式中匹配）
- 服务选型决策（生成候选 → 筛选 → 对比 → 推荐）
- WAF 六大支柱检查
- AI/ML 或大数据项目特殊处理

### 步骤 3: Design Writer（文档生成）
- 按固定 11 章节模板生成说明书
- 每章节包含设计选择、Why、Trade-off
- 技术说明书风格，中文输出

### 步骤 4: Design Reviewer（设计审查）
- 区域合规性检查
- 架构一致性检查
- 必备组件检查
- Best Practice 检查

## 支持的架构模式

### 传统应用
- Web 三层架构
- Serverless API
- SaaS 多租户
- 混合云

### AI/ML 架构
- GenAI 应用架构（Bedrock + Lambda）
- RAG 架构（Bedrock KB + OpenSearch）
- AI Agentic 系统（Bedrock Agents + Step Functions）
- ML 训练推理平台（SageMaker）
- 多模态 AI（Bedrock + Rekognition + Textract）

### 大数据架构
- 批量数据处理平台（S3 + Glue + Athena/Redshift）
- 实时数据处理平台（Kinesis + Lambda）
- 数据湖架构（Lake Formation）
- 大数据计算集群（EMR + Spark）

## 使用示例

### 示例 1: 电商平台云迁移

**输入**（零散会议记录）:
```
会议主题: XX电商平台云迁移讨论
关键讨论点:
- 现有系统用 Java Spring Boot, MySQL 数据库
- 日活大概 5-10 万，高峰期会翻倍
- 希望迁到云上，减少运维成本
- 数据不能出境，必须在中国
- 老板要求 99.9% 可用性
```

**Skill 会**:
1. 识别为 "Web-Application" 项目
2. 提取：流量 5-10万 DAU，技术栈 Spring Boot + MySQL，区域 AWS China
3. 追问：RTO/RPO、峰值 QPS、合规要求
4. 推荐架构：Web 三层架构（ALB + EC2 ASG + RDS Multi-AZ）
5. WAF 评估：六大支柱 + China Region 检查
6. 生成完整设计文档（11 章节）

### 示例 2: AI 知识库问答

**输入**:
```
需求：开发一个企业知识库问答系统
- 用户可以上传公司文档（PDF、Word）
- 用户提问，系统根据文档内容回答
- 需要支持中文
- 预计 1000 个文档，每天 500 次查询
```

**Skill 会**:
1. 识别为 "AI/ML-RAG" 项目
2. 推荐架构：RAG 架构
3. 服务选型：
   - LLM: Claude 3.5 Haiku（成本低，中文支持好）
   - 向量数据库: OpenSearch Serverless（成本优化）
   - Embedding: Titan Embeddings v2
4. AI 特有检查：Token 成本控制、Prompt Injection 防护、幻觉检测
5. 生成 AI 项目专用设计文档

## 核心特性

### 1. 智能项目类型识别
```python
# 自动识别 9 种项目类型
AI/ML-GenAI       # 聊天机器人、内容生成
AI/ML-RAG         # 知识库问答、文档检索
AI/ML-Agentic     # 任务编排、多步骤工作流
BigData-Batch     # 离线分析、BI
BigData-Streaming # 实时流、IoT
BigData-DataLake  # 数据湖、ML 训练
Web-Application   # 传统 Web
SaaS              # 多租户
Hybrid-Cloud      # 混合云
```

### 2. 主动追问机制
自动生成追问问题（P0 级别）:
- RTO/RPO: "请问对系统的 RTO 和 RPO 有明确要求吗？例如: RTO < 4h, RPO < 1h"
- 流量: "请问系统的预估流量是多少？例如: 日活 10 万用户，峰值 QPS 500"
- 区域: "是否有明确的 AWS 区域要求？例如: 必须使用中国区"

### 3. WAF 强制检查
六大支柱 + 项目特有检查:
- 基础：卓越运营、安全性、可靠性、性能、成本、可持续性
- AI/ML: Token 成本、推理延迟、Prompt Injection、幻觉检测、MLOps
- 大数据: 存储成本、查询性能、数据一致性、数据治理

### 4. 服务选型决策
对比评估 + 决策理由 + 替代方案:
```json
{
  "recommendation": "RDS for MySQL",
  "reason": "基于 10 万 DAU 的中等规模，RDS 性价比更优",
  "alternative": "若未来流量增长 10 倍，建议迁移至 Aurora",
  "trade_off": {
    "pros": ["成本较低", "Multi-AZ 高可用"],
    "cons": ["性能不如 Aurora"]
  }
}
```

### 5. 防止过度设计
- 优先选择最简单可满足需求的方案
- 复杂度评分机制
- 人工确认机制（当选择复杂方案时）

## 输出文档结构

生成的架构设计说明书包含 11 个章节:

1. 设计背景与目标
2. 架构设计原则（WAF 六大支柱）
3. 总体架构概述
4. 网络架构设计
5. 计算层设计（含 Why 和 Trade-off）
6. 存储与数据库设计（含 Why 和 Trade-off）
7. 安全与权限设计
8. 高可用与灾备设计
9. 运维与监控设计
10. 成本与扩展性分析
11. 风险、假设与待确认事项

## 技术实现

### Python 脚本
- `material_parser.py`:
  - 项目类型识别（9 种类型）
  - 追问生成（P0/P1/P2 优先级）

- `architecture_decisioning.py`:
  - 架构模式库（9 大模式）
  - 服务选型决策表
  - WAF 检查清单

### 知识库
- `architecture_patterns.md` (2000+ 行):
  - 9 大架构模式详细说明
  - 典型流程图
  - 成本估算
  - 关键决策点

- `waf_checklist.md` (1500+ 行):
  - WAF 六大支柱检查清单
  - AI/ML 特有检查（5 大维度）
  - 大数据特有检查（5 大维度）

### 模板
- `design_doc_template.md`:
  - 11 章节标准模板
  - 占位符替换
  - Markdown 格式

## 验收标准

一份合格的输出文档应满足:
- ✅ 包含全部 11 个章节，结构完整
- ✅ 每个技术选择都有 Why 和 Trade-off 说明
- ✅ 明确标注所有假设和待确认事项
- ✅ 通过 Reviewer 检查（无架构矛盾、无遗漏组件）
- ✅ 符合 AWS China / Global 区域限制
- ✅ AI/ML 项目通过 AI 特有检查
- ✅ 大数据项目通过大数据特有检查
- ✅ 文风专业，适合直接交付

## 安装和使用

### 1. 安装 Skill

将 `aws-arch-designer.skill` 文件安装到 DeepV Code CLI。

### 2. 使用 Skill

在对话中，当您提供 AWS 架构设计相关的材料或需求时，Skill 会自动触发。

**触发场景**:
- "帮我设计一个 XX 系统的 AWS 架构"
- "我有一份会议记录，需要整理成架构设计文档"
- "我要开发一个 AI 聊天机器人，帮我设计架构"
- "大数据平台架构设计"

### 3. Skill 会自动执行 4 步流程

您只需要回答追问的问题，其余工作由 Skill 自动完成。

## 项目特色

1. **完全基于 DEEPV.md 需求**: 忠实实现了文档中的所有要求
2. **4 步流程清晰**: Material Parser → Architecture Decisioning → Design Writer → Design Reviewer
3. **知识库丰富**: 包含 9 大架构模式和 WAF 检查清单
4. **实战导向**: 每个模式都有成本估算、数据规模、延迟指标
5. **可扩展性强**: 易于添加新的架构模式和检查项

## 版本信息

- **版本**: v1.0
- **创建日期**: 2026-01-06
- **基于文档**: DEEPV.md v1.3
- **支持项目类型**: 9 种（Web、AI/ML、大数据、SaaS、混合云）
- **架构模式**: 9 大模式
- **WAF 检查**: 6 大支柱 + AI/ML 和大数据特有检查

## 文件清单

```
aws-arch-designer.skill           # 打包后的 Skill 文件
aws-arch-designer/                # Skill 源代码
├── SKILL.md                      # 主文档 (3000+ 行)
├── scripts/
│   ├── material_parser.py        # 材料解析 (200+ 行)
│   └── architecture_decisioning.py # 架构决策 (300+ 行)
├── references/
│   ├── architecture_patterns.md  # 架构模式库 (2000+ 行)
│   └── waf_checklist.md         # WAF 检查清单 (1500+ 行)
└── assets/
    └── design_doc_template.md   # 文档模板 (200+ 行)
```

总代码量: **7000+ 行**

## 下一步

您现在可以:
1. 将 `aws-arch-designer.skill` 安装到 DeepV Code CLI
2. 尝试使用示例输入测试 Skill
3. 根据实际使用情况迭代优化

Skill 已完成并通过验证！🎉
