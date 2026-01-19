# AWS 架构设计说明书生成器 Skill 需求文档

## 一、Skill 定位与目标

### 1.1 核心目标
将非结构化或半结构化的客户材料，自动转化为结构化、可审计、符合 AWS Best Practice 的《架构设计说明书》。

### 1.2 角色定位
**SA 的"一级设计助理"**，而非决策者。协助 SA 快速完成架构设计文档，但不替代 SA 做最终责任判断。

### 1.3 输入材料特征

**支持的材料格式（多模态直接处理）:**
- 📄 **文本类**: 会议记录、需求列表、Markdown、纯文本
- 📊 **文档类**: Word (docx)、Excel (xlsx)、PDF
- 🖼️ **图片类**: PNG、JPEG、JPG、GIF、WebP、SVG、BMP
- 📋 **案例学习文件**: 包含项目背景、痛点、解决方案、架构图、收益分析

**使用方式:**
- ✅ **批量上传**: 用户可将所有材料集中放入某一目录
- ✅ **单一上传**: 支持单个或多个文件同时上传
- ✅ **混合格式**: 同时上传不同格式的文件（PDF + Excel + 图片等）

**Skill 处理能力:**
- ✅ **多模态理解**: LLM 直接处理所有格式文件（无需专用脚本）
- ✅ **自动检测案例文件**: 识别是否为案例学习文件（无需用户标记）
- ✅ **关键要素提取**: 自动识别功能需求、非功能需求、合规要求、预算、流量等
- ✅ **主动追问**: 当关键信息缺失时主动追问（RTO/RPO、峰值流量、合规要求）

**架构图处理:**
- 📸 **用户提供的架构图**: LLM 用视觉能力直接理解和验证
- 🎨 **自动生成**: 若无架构图，通过 MCP 调用 `awslabs-aws-diagram-mcp-server` 自动生成

### 1.4 输出产物
一份标准化的《AWS 架构设计说明书》，包含:
- 架构目标与设计原则
- 总体架构说明（含架构图）
- 关键组件设计（VPC、Compute、Storage、Network、Security、Ops）
- 安全与合规设计
- 高可用与灾备设计
- 成本与扩展性说明
- 风险、假设与待确认事项

### 1.5 明确不做的事（边界）
- ❌ 不自动"脑补"客户未给出的强约束
- ❌ 不直接输出 IaC 代码（Terraform / CloudFormation 由其他 Skill 负责）
- ❌ 不替代 SA 做最终判断和审批
- ❌ 不过度设计（在需求不明确时，选择最简方案）

---

## 二、技术架构设计

### 2.1 整体流程（5-Step Pipeline）

这是一个**多步骤 Skill**，而非单一 Prompt。

```
┌────────────────────────┐
│  用户输入零散材料        │
│ (会议记录/需求列表/代码) │
│ (可能含有架构图,可能无)   │
└──────┬─────────────────┘
       ↓
┌──────────────────────────────┐
│ ① Material Parser             │ ← LLM + Interactive
│ - 清洗零散信息                  │
│ - 提取关键要素:                 │
│   • 功能需求                   │
│   • 非功能需求                 │
│   • 合规性要求                 │
│   • 预算限制                   │
│   • 预估流量                   │
│ - 检测用户是否提供架构图         │
│ - 检测是否为案例学习文件         │
│ - 标注缺失信息                 │
│ - 主动追问(RTO/RPO/峰值等)     │
│ - 输出结构化 JSON              │
└──────┬────────────────────────┘
       ↓ (结构化数据)
┌──────────────────────────────┐
│ ② Architecture Diagram Gen    │ ← MCP + AWS Diagram Server
│ - 检查是否有用户提供的架构图     │
│ - 若无提供:                   │
│   • 基于结构化需求调用 MCP      │
│   • 使用 aws-diagram-mcp-server │
│   • 自动生成架构图              │
│ - 若有提供:                   │
│   • 验证架构图与需求的匹配度    │
│   • 识别架构图中的 AWS 服务     │
│ - 输出架构图(PNG/SVG) + 描述   │
└──────┬────────────────────────┘
       ↓ (架构图 + 需求数据)
┌──────────────────────────────┐
│ ③ Architecture Decisioning    │ ← LLM + WAF + Rules
│ - 服务选型决策树                │
│   • 需求 → 候选服务列表          │
│   • 约束筛选                   │
│   • 对比评估                   │
│ - AWS Well-Architected 检查   │
│   • 六大支柱强制评估            │
│   • 最佳实践验证                │
│ - 匹配架构模式                 │
│ - Region / China 特判          │
│ - 生成设计蓝图 + 决策理由       │
└──────┬────────────────────────┘
       ↓ (设计蓝图 + WAF 评估)
┌──────────────────────────┐
│ ④ Design Writer           │ ← LLM + Writing Standards
│ - 按固定模板生成说明书       │
│ - 强制章节完整性            │
│ - 整合架构图信息            │
│ - 遵循写作标准              │
│ - 输出 Markdown 文档        │
└──────┬────────────────────┘
       ↓
┌──────────────────────────┐
│ ⑤ Design Reviewer         │ ← LLM (Critic Role)
│ - AWS Best Practice 检查   │
│ - 自相矛盾检查              │
│ - 缺失章节检查              │
│ - 架构图与文档一致性检查     │
│ - 运维监控完整性检查         │
│ - 输出问题清单与修订建议     │
└──────────────────────────┘
```

### 2.2 关键原则
- **结构化优先**: 所有步骤基于结构化数据，不依赖自然语言传递
- **模式化设计**: 使用预定义架构模式，避免 LLM 自由发挥
- **强制检查**: Reviewer 环节必须执行，确保输出质量
- **架构图驱动**: 优先使用用户提供的架构图；若无提供则主动绘制，确保视觉化表示
- **写作标准**: 严格遵循写作标准，确保文档专业、丰满、精准

---

## 三、步骤详细设计

### 步骤 1: Material Parser（需求提取）

#### 3.1 核心任务
从零散、非结构化的客户材料中提取关键信息，输出结构化 JSON。

#### 3.2 关键要素提取（5 大要素）

| 要素类别 | 具体内容 | 缺失时的处理策略 |
|---------|---------|----------------|
| **功能需求** | 系统需要实现的业务功能 | 基于上下文推断，并标注假设 |
| **非功能需求** | 可用性、性能、延迟、扩展性、RTO/RPO | **主动追问**，不可假设 |
| **合规性要求** | 等保、GDPR、SOC2、行业特殊要求 | **主动追问**，默认标注为"未确认" |
| **预算限制** | 月度/年度预算上限 | 标注为"未提供"，不影响架构设计 |
| **预估流量** | DAU、QPS、数据量、峰值倍数 | **主动追问**，影响服务选型 |

#### 3.3 主动交互机制

**P0 关键问题（必须追问）:**
- RTO/RPO 目标（影响灾备设计）
- 可用性要求（影响 Multi-AZ 决策）
- 预估流量/QPS（影响扩展策略）
- AWS 区域（影响服务可用性）

**追问策略:**
- 一次最多追问 **3-5 个问题**，避免用户疲劳
- 提供**选项或参考值**，降低用户理解成本
- 对于非关键信息（如预算），可标注"未提供"并继续

#### 3.4 案例学习文件处理

**案例文件识别:**
- 检测文件名关键词：案例、case study、迁移方案等
- 检测内容关键词：项目背景、痛点、解决方案、收益等

**提取信息:**
- 项目背景（行业、规模、现状）
- 痛点分析
- AWS 解决方案（服务组合、架构模式）
- 关键指标（可用性、性能、成本）
- 预期收益
- 经验教训

**关联匹配:**
- 计算案例与新项目的相关性（行业、规模、痛点、功能）
- 提取可复用的服务和经验
- 作为新项目的参考基线

#### 3.5 输出结构

```json
{
  "business_goals": ["业务目标1", "业务目标2"],
  "functional_requirements": ["功能需求1", "功能需求2"],
  "non_functional_requirements": {
    "availability": "99.9%",
    "latency": "<200ms",
    "scalability": "水平扩展",
    "rto": "< 4h",
    "rpo": "< 1h"
  },
  "traffic_estimation": {
    "daily_active_users": "100,000",
    "peak_qps": "500",
    "data_volume": "500 GB",
    "peak_multiplier": "3x"
  },
  "constraints": {
    "region": "AWS China",
    "compliance": ["等保二级"],
    "network": "需要私网访问本地 IDC",
    "budget": "未提供"
  },
  "assumptions": ["假设1", "假设2"],
  "open_questions": ["待确认问题1", "待确认问题2"]
}
```

---

### 步骤 2: Architecture Diagram Generation（架构图生成）

#### 3.6 两种处理路径

**Case 1: 用户提供了架构图（图片/PDF）**

处理流程:
1. 使用 Vision/OCR 识别架构图内容
2. 提取 AWS 服务和连接关系
3. 生成文字描述
4. 验证与需求的匹配度

输出结构:
```json
{
  "architecture_diagram_source": "user_provided",
  "detected_services": ["EC2", "RDS", "S3", "ALB"],
  "detected_relationships": [
    {"source": "ALB", "target": "EC2", "type": "forward_traffic"}
  ],
  "diagram_text_description": "用户提供的架构图展示了一个三层架构...",
  "compatibility_check": {
    "matches_requirements": true,
    "notes": "架构图与需求基本匹配，但未明确显示备份策略"
  }
}
```

**Case 2: 用户未提供架构图**

处理流程:
1. 基于步骤 3 的架构决策结果构建**架构蓝图**（服务列表 + 连接关系）
2. 调用 MCP Server: `awslabs-aws-diagram-mcp-server`
3. 传入架构蓝图（JSON 格式）
4. 生成 PNG/SVG 架构图文件
5. 生成文字描述
6. 整合到设计文档

输出结构:
```json
{
  "architecture_diagram_source": "auto_generated",
  "generation_method": "awslabs-aws-diagram-mcp-server",
  "diagram_file": "architecture_diagram.png",
  "diagram_services": ["EC2", "RDS", "S3", "ALB"],
  "diagram_text_description": "生成的架构图展示了一个标准的三层 Web 应用...",
  "assumptions": ["假设 EC2 实例部署在 Multi-AZ"]
}
```

#### 3.7 架构图一致性检查

**检查项:**
- [ ] 服务完整性：架构图是否包含所有确定的服务？
- [ ] 设计原则一致性：是否体现 Multi-AZ、负载均衡、备份等？
- [ ] 需求满足性：是否支持可用性、流量规模要求？

---

### 步骤 3: Architecture Decisioning（架构决策）⭐ 最关键

#### 3.8 核心任务

1. **服务选型决策树**
   - 需求 → 候选服务列表
   - 基于约束筛选（Region/合规/预算）
   - 候选服务对比评估（Pros/Cons/成本）
   - 输出推荐 + 替代方案 + Why + Trade-off

2. **AWS Well-Architected Framework 强制检查**
   - 六大支柱逐一评估
   - 确保设计符合最佳实践
   - 识别潜在风险

#### 3.9 WAF 六大支柱检查

##### 1️⃣ 卓越运营 (Operational Excellence)
- [ ] 是否定义了运维流程和标准？
- [ ] 是否使用 IaC（CloudFormation/Terraform）？
- [ ] 是否配置了日志聚合（CloudWatch Logs）？
- [ ] 是否配置了自动化运维（Systems Manager）？
- [ ] 是否建立了变更管理流程？

**检查点:**
- CloudWatch Logs 日志聚合
- EventBridge 自动化响应
- Systems Manager 补丁管理
- IaC 代码管理

##### 2️⃣ 安全性 (Security)
- [ ] 是否遵循最小权限原则（IAM）？
- [ ] 是否启用静态数据加密（KMS）？
- [ ] 是否启用传输加密（TLS）？
- [ ] 是否配置网络隔离（VPC/Security Group）？
- [ ] 是否启用审计日志（CloudTrail）？

**检查点:**
- IAM 角色（禁止使用 Root）
- KMS 密钥管理
- WAF 防护（若有公网暴露）
- MFA 多因素认证
- VPC Flow Logs

##### 3️⃣ 可靠性 (Reliability)
- [ ] 是否实现 Multi-AZ 部署？
- [ ] 是否配置自动故障转移？
- [ ] 是否定义了 RTO/RPO？
- [ ] 是否配置了备份策略？
- [ ] 是否进行了容量规划？

**检查点:**
- RDS Multi-AZ / Aurora Replicas
- Auto Scaling 组配置
- 备份策略（AWS Backup / Snapshot）
- Route 53 健康检查

##### 4️⃣ 性能效率 (Performance Efficiency)
- [ ] 是否选择了适合工作负载的实例类型？
- [ ] 是否使用了缓存机制？
- [ ] 是否启用了 CDN（若适用）？
- [ ] 是否优化了数据库查询？

**检查点:**
- 实例类型选择（计算优化/内存优化/通用）
- ElastiCache / DAX 缓存
- CloudFront CDN
- RDS 性能洞察

##### 5️⃣ 成本优化 (Cost Optimization)
- [ ] 是否使用了 Auto Scaling 避免资源浪费？
- [ ] 是否考虑了 Reserved Instance / Savings Plans？
- [ ] 是否配置了 S3 生命周期策略？
- [ ] 是否启用了成本监控（Cost Explorer）？

**检查点:**
- Auto Scaling 策略
- S3 Intelligent-Tiering / Glacier
- Spot Instances（非关键工作负载）
- 成本告警（Budgets）

##### 6️⃣ 可持续性 (Sustainability)
- [ ] 是否选择了能效更高的实例类型（Graviton）？
- [ ] 是否优化了资源利用率？
- [ ] 是否选择了绿色能源的 Region？

**检查点:**
- Graviton 实例（ARM 架构）
- Serverless 优先（按需计费）
- 自动关闭开发/测试环境

#### 3.10 AI/ML 项目的特殊 WAF 检查

**额外检查维度:**

**1. AI 成本优化**
- [ ] Token 成本控制（单次请求 Token 上限、Prompt 缓存）
- [ ] 推理成本优化（SageMaker Auto Scaling、Serverless Inference）
- [ ] 向量数据库成本（OpenSearch Serverless、Index 生命周期）

**2. AI 性能效率**
- [ ] 推理延迟（满足业务 SLA、缓存、Provisioned Throughput）
- [ ] 模型选择（模型大小匹配任务复杂度）
- [ ] 批处理优化（Batch Transform、合并请求）

**3. AI 安全性**
- [ ] 数据隐私（训练数据加密、VPC Endpoints、不记录数据）
- [ ] Prompt Injection 防护（输入过滤、System Prompt 保护）
- [ ] 模型访问控制（IAM 细粒度权限、CloudTrail 审计）

**4. AI 可靠性**
- [ ] 降级策略（备用模型、超时重试）
- [ ] 幻觉检测（Guardrails、RAG 事实依据）
- [ ] 版本管理（Model Registry、A/B 测试）

**5. MLOps（卓越运营）**
- [ ] 监控（性能指标、数据漂移、Prompt/Response 日志）
- [ ] 持续优化（模型重训练、用户反馈）

#### 3.11 大数据项目的特殊 WAF 检查

**额外检查维度:**

**1. 大数据成本优化**
- [ ] 存储成本（S3 生命周期、Intelligent-Tiering、过期数据删除）
- [ ] 计算成本（EMR 临时集群、Spot Instances、Redshift RI）
- [ ] 数据传输成本（VPC Endpoints、跨 Region 复制必要性）

**2. 大数据性能效率**
- [ ] 查询性能（S3 分区、列式存储、Athena 优化）
- [ ] 数据处理性能（EMR 实例类型、Glue DPU、Kinesis Shard）
- [ ] 并发控制（Redshift 并发扩展、Athena 并发限制）

**3. 大数据可靠性**
- [ ] 数据一致性（去重逻辑、Exactly-Once 语义）
- [ ] 容错机制（EMR 自动恢复、Glue Bookmark、死信队列）
- [ ] 数据质量（Glue Data Quality、Schema 验证）

**4. 大数据安全性**
- [ ] 数据加密（S3/Redshift/Kinesis 加密）
- [ ] 访问控制（Lake Formation 细粒度权限、最小权限）
- [ ] 数据脱敏（敏感数据处理、Glue DataBrew）

**5. 数据治理（卓越运营）**
- [ ] 监控（ETL Job 失败率、数据积压、查询性能）
- [ ] 数据治理（Glue Catalog、保留策略、数据血缘）
- [ ] 自动化（调度工具、数据质量检查）

#### 3.12 架构模式库（13 个预定义模式）

**传统应用架构（4 个）:**
1. **Web 三层架构** - ALB + EC2 ASG + RDS Multi-AZ
2. **Serverless API** - API Gateway + Lambda + DynamoDB
3. **SaaS 多租户** - 租户隔离策略 + 资源池设计
4. **混合云/专线** - Direct Connect + VPN + Transit Gateway

**大数据与分析架构（4 个）:**
5. **批量数据处理平台** - S3 + Glue + Athena/Redshift
6. **实时数据处理平台** - Kinesis + Lambda + DynamoDB
7. **数据湖架构** - S3 + Lake Formation + Glue Catalog
8. **大数据计算集群** - EMR (Hadoop/Spark) + S3

**AI/ML 与 Agentic 架构（5 个）:**
9. **GenAI 应用架构** - Bedrock + Lambda + DynamoDB
10. **RAG 架构** - Bedrock KB + OpenSearch Serverless（知识库问答）
11. **AI Agentic 系统架构** - Bedrock Agents + Lambda + Step Functions（任务编排）
12. **ML 训练与推理平台** - SageMaker + S3 + ECR
13. **多模态 AI 架构** - Bedrock + Rekognition + Textract

**关键原则:**
- ✅ RAG 是**可选的知识库增强**，不是 Agentic 必需组件
- ✅ 只在需要文档检索/语义搜索时才用 RAG
- ✅ 纯任务编排/API 自动化的 Agent 不需要 RAG
- ❌ 禁止盲目为所有 Agentic 项目加入 RAG

#### 3.13 架构模式选择决策树

```
需求关键词 → 推荐架构模式

【传统应用】
"电商"、"Web"、"API" → Web 三层架构 / Serverless API
"本地 IDC + 云" → 混合云
"容器"、"微服务" → 容器化应用

【大数据】
"大数据"、"分析"、"BI" → 批量数据处理 / 数据湖
"实时"、"流数据"、"IoT" → 实时数据处理

【AI/ML】
"聊天机器人"、"内容生成"（无文档） → GenAI 应用
"知识库"、"文档检索"、"语义搜索" → RAG 架构
"任务编排"、"多步骤"、"工作流"、"API 自动化" → AI Agentic（不需要 RAG）
"任务编排" + "知识库" → AI Agentic + RAG
"自定义模型"、"训练" → ML 训练推理
"图像识别"、"OCR"、"语音处理" → 多模态 AI
```

#### 3.14 服务选型示例

**场景: 托管关系型数据库**

```json
{
  "decision_item": "数据库选型",
  "candidates": [
    {
      "service": "Amazon RDS for MySQL",
      "pros": ["完全托管", "成本较低", "Multi-AZ 高可用"],
      "cons": ["性能不如 Aurora", "扩展能力有限"],
      "cost_estimate": "$200-500/月",
      "use_case": "中等规模 Web 应用"
    },
    {
      "service": "Amazon Aurora MySQL",
      "pros": ["性能优异", "自动扩展", "Global Database"],
      "cons": ["成本高 20-30%"],
      "cost_estimate": "$300-700/月",
      "use_case": "高性能、大规模应用"
    }
  ],
  "recommendation": "Amazon RDS for MySQL",
  "reason": "基于 10 万 DAU 的中等规模，RDS 性价比更优，满足 99.9% 可用性要求",
  "alternative": "若未来流量增长 10 倍，建议迁移至 Aurora"
}
```

#### 3.15 防止过度设计

**复杂度评分机制:**
```python
COMPLEXITY_SCORE = {
    "EC2": 1,
    "ECS Fargate": 2,
    "EKS": 4,
    "RDS": 1,
    "Aurora": 2,
    "Single Region": 1,
    "Multi-Region": 4
}

# 若总分 > 10，触发人工确认
if total_complexity_score > 10:
    request_confirmation("架构复杂度较高，是否确认？")
```

**原则:**
- 优先 EC2 + Auto Scaling，而非 EKS
- 优先单 Region，而非 Multi-Region
- 选择能满足需求的**最简单方案**

---

### 步骤 4: Design Writer（文档生成）

#### 3.16 固定章节结构（11 章，不可删减/合并）

```markdown
# AWS 架构设计说明书

## 1. 设计背景与目标
- 项目背景
- 业务目标
- 成功标准

## 2. 架构设计原则
- 适用的 AWS Well-Architected 原则
- 项目特定的设计原则

## 3. 总体架构概述
- 架构风格（如三层架构、Serverless 等）
- 核心组件概览
- 架构图文字描述

## 4. 网络架构设计
- VPC 设计
- 子网规划
- 路由与网关
- 混合云连接（如适用）

## 5. 计算层设计
- 计算服务选择（EC2 / Lambda / ECS / EKS）
- 扩展策略
- 容器 / 函数设计（如适用）

## 6. 存储与数据库设计
- 数据库选型（RDS / DynamoDB / Aurora）
- 对象存储（S3）
- 数据备份策略

## 7. 安全与权限设计
- IAM 角色与策略
- 网络安全（Security Group / NACL / WAF）
- 数据加密（传输 / 静态）
- 合规性（等保 / SOC2 等）

## 8. 高可用与灾备设计
- 多 AZ 部署
- RTO / RPO 目标
- 灾备方案（Backup / Snapshot / 跨 Region）

## 9. 运维与监控设计
- 日志聚合（CloudWatch Logs / S3）
- 监控告警（CloudWatch Alarms）
- 自动化运维（Systems Manager / EventBridge）

## 10. 成本与扩展性分析
- 成本估算
- 扩展性分析
- 成本优化建议（RI / Savings Plans / Spot）

## 11. 风险、假设与待确认事项
- 技术风险
- 假设列表
- 待客户确认的问题
```

#### 3.17 写作要求

**每章节必须包含:**
- ✅ 设计选择的具体内容
- ✅ 选择理由（Why）
- ✅ 权衡说明（Trade-off）
- ✅ 若信息不足，基于假设并**明确标注**

**写作标准:**
- 📝 参考 `references/WRITING_STANDARDS.md`
- 语言专业、丰满、精准
- 每个技术决策包含 4 要素：决策内容、理由、权衡、指标
- 避免过度啰嗦，直击要点
- 使用准确的 AWS 术语

**文风要求:**
- 技术说明书风格，避免营销语言
- 适合直接交付客户或进入方案评审
- 使用 Markdown 格式
- 语言：中文

---

### 步骤 5: Design Reviewer（质量审查）

#### 3.18 检查清单

**5.1 区域合规性检查**
- [ ] 若 `region = "AWS China"`，是否使用了 China 不可用的服务？
- [ ] 若 `region = "Global"`，是否考虑数据合规性（GDPR / 数据本地化）？

**5.2 架构一致性检查**
- [ ] 是否存在矛盾设计？（如：没有 NAT Gateway 却声称可访问公网）
- [ ] 是否出现过度设计？（如：小流量场景使用 EKS）

**5.3 必备组件检查**
- [ ] 是否遗漏 **IAM** 角色设计？
- [ ] 是否遗漏 **CloudWatch Logs** 日志方案？
- [ ] 是否遗漏 **Backup** 备份策略？
- [ ] 是否明确 **RTO / RPO**？
- [ ] 是否考虑 **成本估算**？
- [ ] 是否完整设计 **监控与可观测性体系**？

**5.4 运维监控与可观测性检查**

**日志聚合与管理:**
- [ ] 是否明确日志保留期（应用日志 30-90 天、审计日志 1-3 年）？
- [ ] 是否配置了日志脱敏（不记录敏感信息）？
- [ ] 是否设置了日志采样率（避免日志爆炸）？

**监控与告警:**
- [ ] 是否定义了系统级监控指标（CPU、内存、磁盘、网络）？
- [ ] 是否定义了应用级监控指标（错误率、延迟、吞吐量）？
- [ ] 是否定义了业务级监控指标（DAU、转化率、关键功能可用性）？
- [ ] 是否定义了**告警阈值和优先级**（Critical/High/Medium/Low）？
- [ ] 是否配置了多渠道通知（邮件、Slack、SMS）？
- [ ] 是否实施了**告警聚合**（防止告警风暴）？
- [ ] 是否有**告警升级机制**（无响应自动升级）？

**分布式追踪与性能诊断:**
- [ ] 是否启用了 X-Ray 或类似追踪工具？
- [ ] 是否追踪了跨服务调用链路？

**仪表盘与可视化:**
- [ ] 是否有运维监控仪表盘（系统健康、告警状态）？
- [ ] 是否有业务仪表盘（KPI、收入、用户行为）？
- [ ] 是否有成本仪表盘（按服务成本、预测趋势）？

**AI/ML 特有监控（AI 项目必检）:**
- [ ] 是否监控 **Token 使用量**？
- [ ] 是否监控 **推理延迟**（平均/P95/P99）？
- [ ] 是否监控 **模型成功率** 和 **幻觉率**？
- [ ] 是否记录 **Prompt 和 Completion**（用于调试）？
- [ ] 是否进行 **数据漂移检测**（SageMaker Model Monitor）？

**大数据特有监控（大数据项目必检）:**
- [ ] 是否监控 **ETL Job 成功率** 和 **执行时间**？
- [ ] 是否监控 **数据延迟**（进入 vs 处理完毕）？
- [ ] 是否监控 **数据质量**（完整性、准确性、一致性）？
- [ ] 是否配置 **消费延迟告警**（Kinesis/Kafka）？
- [ ] 是否监控 **存储使用率** 和 **成本趋势**？

**自动化运维:**
- [ ] 是否有自动化补丁管理策略？
- [ ] 是否支持快速回滚（< 5 分钟）？
- [ ] 是否有自动化故障转移机制？
- [ ] 是否建立了 **On-Call 轮换体系**（24/7 支持）？

**5.5 Best Practice 检查**
- [ ] 是否使用 Multi-AZ 部署（生产环境）？
- [ ] 是否启用加密（传输 + 静态）？
- [ ] 是否启用 MFA（管理员账户）？
- [ ] 是否配置告警（CPU / Memory / Disk / Error Rate）？

**5.6 架构图检查**
- [ ] 架构图是否存在？
- [ ] 架构图中的服务是否与设计文档一致？
- [ ] 架构图是否体现了 Multi-AZ/Multi-Region 部署？
- [ ] 关键组件（备份、灾备、监控）是否在架构图中标注？

---

## 四、验收标准

### 4.1 文档完整性
- ✅ 包含全部 11 个章节，结构完整
- ✅ 每个技术选择都有 Why 和 Trade-off 说明
- ✅ 明确标注所有假设和待确认事项
- ✅ 文风专业，适合直接交付

### 4.2 架构决策质量
- ✅ **所有服务选择都经过 WAF 六大支柱评估**
- ✅ 每个服务选型都有候选对比和决策理由
- ✅ 提供了替代方案和升级路径
- ✅ 没有出现过度设计（复杂度评分合理）

### 4.3 技术合规性
- ✅ 通过 Reviewer 检查（无架构矛盾、无遗漏组件）
- ✅ 符合 AWS China / Global 区域限制
- ✅ 满足合规性要求（等保、GDPR 等）
- ✅ 安全性和可靠性检查通过（无 Critical 级别问题）

### 4.4 可追溯性
- ✅ 记录了 Material Parser 的交互历史
- ✅ 记录了 Architecture Decisioning 的决策过程
- ✅ WAF 评估结果可追溯

---

## 五、参考文档结构

### 5.1 references/ 目录

```
references/
├── README.md                              - 参考文档索引
├── architecture_patterns.md               - 架构模式库
├── waf_checklist.md                       - WAF 检查清单
├── agentic_ai_practice_requirements.md    - AI Agentic 实践要求
├── WRITING_STANDARDS.md                   - 写作标准（步骤 4 必读）
├── WHEN_TO_USE_WRITING_STANDARDS.md       - 写作标准使用指南
├── WRITING_STANDARDS_USAGE_SUMMARY.md     - 写作标准使用总结
└── WRITING_STANDARDS_INTEGRATION_SUMMARY.md - 写作标准整合总结
```

### 5.2 使用时机

| 参考文档 | 使用频率 | 主要用途 |
|---------|---------|---------|
| **WRITING_STANDARDS.md** | 每个项目 | 步骤 4 写作质量控制 ⭐⭐⭐ |
| **waf_checklist.md** | 每个项目 | 步骤 3/5 架构质量检查 ⭐⭐⭐ |
| **architecture_patterns.md** | 每个项目 | 步骤 3 架构模式选择 ⭐⭐⭐ |
| **agentic_ai_practice_requirements.md** | AI/ML 项目 | 步骤 3/4/5 AI 项目特殊要求 ⭐⭐ |

---

## 六、关键原则总结

### 6.1 核心原则
1. **结构化优先** - 所有步骤基于结构化数据，不依赖自然语言传递
2. **模式化设计** - 使用预定义架构模式，避免 LLM 自由发挥
3. **强制检查** - WAF 检查是 MANDATORY，不可跳过
4. **防止过度设计** - 优先最简方案（EC2 优于 EKS，单 Region 优于 Multi-Region）
5. **架构图驱动** - 所有设计都包含架构图（用户提供或自动生成）
6. **写作标准** - 严格遵循写作标准，确保文档专业、丰满、精准

### 6.2 禁止事项
- ❌ 禁止跳过 WAF 评估
- ❌ 禁止过度设计（无需求不上 EKS/Multi-Region）
- ❌ 禁止"脑补"未明确的需求
- ❌ 禁止盲目为所有 Agentic 项目加入 RAG
- ❌ AI 项目禁止忽略成本控制（Token 限制、模型选择）
- ❌ 大数据项目禁止忽略数据分区和存储优化

### 6.3 关键认识
- ✅ RAG 是**可选的知识库增强**，不是 Agentic 必需组件
- ✅ 只在需要文档检索/语义搜索时才用 RAG
- ✅ 纯任务编排/API 自动化的 Agent 不需要 RAG
- ✅ 运维与监控是系统稳定性的**关键支撑**，不仅仅是告警
- ✅ Agentic AI 的核心是**任务编排与自主推理**，RAG 是**可选的知识库补充**

---

## 七、后续扩展方向

### 7.1 已实现功能
- ✅ 架构图自动生成（MCP Server 集成）
- ✅ 用户架构图识别和验证（Vision/OCR）
- ✅ 案例学习文件检测和关联匹配
- ✅ 写作标准参考手册

### 7.2 未来增强
- 🔄 IaC 代码生成 Skill（Terraform / CloudFormation）
- 🔄 成本计算 Skill（AWS Pricing API 集成）
- 🔄 架构图版本管理和历史对比
- 🔄 案例库管理和分类
- 🔄 知识库增强（WAF Lens、行业 Compliance）
- 🔄 交互式设计对比（方案 A vs 方案 B）

---

**文档版本:** v1.7
**最后更新:** 2026-01-18
**维护者:** AWS 架构设计 Skill 团队

## 版本历史

### v1.7 (2026-01-18)
- ✅ 重新组织文档结构，提高可读性
- ✅ 清理冗余内容，聚焦核心需求
- ✅ 统一参考文档管理（references/ 目录）
- ✅ 修复绝对路径问题，确保跨用户可移植性
- ✅ 精简版本历史，保留关键更新记录

### v1.6 (2026-01-12)
⭐⭐ **重要更新: 运维监控完整性 + AI Agentic 与 RAG 关系澄清**
- ✅ 运维、监控与可观测性能力强化
- ✅ AI Agentic 与 RAG 关系澄清
- ✅ 禁止盲目为所有 Agentic 项目添加 RAG

### v1.5 (2026-01-07)
⭐⭐ **重大更新: 案例学习文件支持与参考**
- ✅ 案例学习文件检测与识别
- ✅ 结构化信息提取
- ✅ 新项目与案例的关联匹配
- ✅ 参考加速决策流程

### v1.4 (2026-01-07)
⭐⭐ **重大更新: 架构图自动生成能力**
- ✅ 整体流程升级为 5-Step Pipeline
- ✅ MCP Server 集成（aws-diagram-mcp-server）
- ✅ 架构图一致性检查

### v1.3 (2026-01-06)
⭐⭐ **重大更新: 大数据与 AI/ML 架构设计能力**
- ✅ 新增 9 个架构模式
- ✅ AI/ML 和大数据服务选型决策表
- ✅ 特殊 WAF 检查（AI 和大数据）

### v1.2 (2026-01-06)
⭐ **核心更新: Architecture Decisioning（架构决策引擎）**
- ✅ 服务选型决策树
- ✅ WAF 六大支柱强制检查
- ✅ 复杂度评分机制防止过度设计

### v1.1 (2026-01-06)
- ✅ Material Parser 处理能力
- ✅ 5 大关键要素提取清单
- ✅ 主动交互机制

### v1.0 (初始版本)
- 基础架构设计 Skill 需求定义
