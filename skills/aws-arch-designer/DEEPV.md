# AWS 架构设计说明书生成器 Skill 需求文档

## 一、Skill 定位与目标

### 1.1 核心目标
将非结构化或半结构化的客户材料,自动转化为结构化、可审计、符合 AWS Best Practice 的《架构设计说明书》。

### 1.2 角色定位
**SA 的"一级设计助理"**,而非决策者。协助 SA 快速完成架构设计文档,但不替代 SA 做最终责任判断。

### 1.3 输入材料特征

**材料形态(可能非常零散):**
- 会议记录(散乱的讨论要点)
- 简单需求列表(箭头式要点)
- 代码片段(现有系统实现参考)
- 客户需求说明(Word / Markdown / 文本)
- 现有系统描述(迁移项目适用)
- 现有资源收集表(Excel表格,迁移项目适用)
- 合规、安全、地域约束
- 成本、性能、可用性目标
- 指定 AWS 区域(Global / China)

**Skill 必须具备的能力:**
- ✅ **信息清洗**: 从零散材料中提取结构化信息
- ✅ **关键要素识别**: 自动识别功能需求、非功能需求、合规性要求、预算限制、预估流量
- ✅ **主动交互**: 当关键信息缺失时,主动追问用户(如 RTO/RPO、峰值流量、合规要求)

### 1.4 输出产物
一份标准化的《AWS 架构设计说明书》,包含:
- 架构目标与设计原则
- 总体架构说明
  - 文字版架构图说明
- 关键组件设计(VPC、Compute、Storage、Network、Security、Ops)
- 安全与合规设计
- 高可用与灾备设计
- 成本与扩展性说明
- 风险、假设与待确认事项


### 1.5 明确不做的事(边界)
- ❌ 不自动"脑补"客户未给出的强约束
- ❌ 不直接输出 IaC 代码(Terraform / CloudFormation 由其他 Skill 负责)
- ❌ 不替代 SA 做最终判断和审批
- ❌ 不过度设计(在需求不明确时,选择最简方案)

---

## 二、技术架构设计

### 2.1 整体流程(4-Step Pipeline)

这是一个**多步骤 Skill**,而非单一 Prompt。

```
┌────────────────────────┐
│  用户输入零散材料        │
│ (会议记录/需求列表/代码) │
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
│ - 标注缺失信息                 │
│ - 主动追问(RTO/RPO/峰值等)     │
│ - 输出结构化 JSON              │
└──────┬────────────────────────┘
       ↓ (结构化数据)
┌──────────────────────────────┐
│ ② Architecture Decisioning    │ ← LLM + WAF + Rules
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
│ ③ Design Writer           │ ← LLM
│ - 按固定模板生成说明书       │
│ - 强制章节完整性            │
│ - 输出 Markdown 文档        │
└──────┬────────────────────┘
       ↓
┌──────────────────────────┐
│ ④ Design Reviewer         │ ← LLM (Critic Role)
│ - AWS Best Practice 检查   │
│ - 自相矛盾检查              │
│ - 缺失章节检查              │
│ - 输出问题清单与修订建议     │
└──────────────────────────┘
```

### 2.2 关键原则
- **结构化优先**: 所有步骤基于结构化数据,不依赖自然语言传递
- **模式化设计**: 使用预定义架构模式,避免 LLM 自由发挥
- **强制检查**: Reviewer 环节必须执行,确保输出质量

---

## 三、核心数据结构

### 3.1 Material Parser 工作流程

#### 3.1.1 关键要素提取清单

**必须提取的 5 大要素:**

| 要素类别 | 具体内容 | 缺失时的处理策略 |
|---------|---------|----------------|
| **功能需求** | 系统需要实现的业务功能 | 基于上下文推断,并标注假设 |
| **非功能需求** | 可用性、性能、延迟、扩展性 | **主动追问**,不可假设 |
| **合规性要求** | 等保、GDPR、SOC2、行业特殊要求 | **主动追问**,默认标注为"未确认" |
| **预算限制** | 月度/年度预算上限 | 标注为"未提供",不影响架构设计 |
| **预估流量** | DAU、QPS、数据量、峰值倍数 | **主动追问**,影响服务选型 |

#### 3.1.2 主动交互机制

**触发追问的条件:**

当以下关键信息缺失时,Skill **必须**主动提问:

```python
CRITICAL_QUESTIONS = {
    "RTO/RPO": "您对系统的恢复时间目标(RTO)和恢复点目标(RPO)有要求吗?例如: RTO < 1h, RPO < 15min",
    "峰值流量": "请问系统的峰值流量大约是日常流量的多少倍?例如: 2-3倍",
    "合规要求": "是否有明确的合规性要求?例如: 等保二级、GDPR、数据本地化等",
    "可用性要求": "对系统可用性有明确要求吗?例如: 99.9%、99.95%、99.99%",
    "数据敏感度": "系统处理的数据是否包含敏感信息(个人信息、金融数据等)?",
    "区域限制": "是否有明确的 AWS 区域要求?例如: 必须使用中国区、必须在欧盟境内等"
}
```

**追问策略:**
- 一次最多追问 **3-5 个问题**,避免用户疲劳
- 提供**选项或参考值**,降低用户理解成本
- 对于非关键信息(如预算),可标注"未提供"并继续

#### 3.1.3 输出结构

```json
{
  "business_goals": [
    "支持 Web 访问",
    "日活 10 万用户"
  ],
  "functional_requirements": [
    "用户注册与登录",
    "订单管理",
    "支付功能"
  ],
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
  "assumptions": [
    "用户未明确峰值流量,假设为日常流量的 3 倍"
  ],
  "open_questions": [
    "是否需要多 Region 灾备?",
    "是否需要跨境数据传输?"
  ],
  "user_interaction_log": [
    {
      "question": "对系统可用性有明确要求吗?",
      "answer": "99.9%",
      "timestamp": "2026-01-06 10:30:00"
    }
  ]
}
```

**字段说明:**
- `functional_requirements`: 功能需求列表(新增)
- `traffic_estimation`: 流量估算数据(新增)
- `business_goals`: 业务目标列表
- `non_functional_requirements`: 非功能需求(可用性、性能、扩展性)
- `constraints`: 硬约束(地域、合规、网络、预算)
- `assumptions`: 当信息不足时做出的假设(需明确标注)
- `open_questions`: 需要客户进一步确认的问题
- `user_interaction_log`: 交互记录(用于追溯和审计)

### 3.2 Material Parser 实施细节

#### 3.2.1 信息清洗与识别规则

**零散材料处理流程:**

```python
# 伪代码示例
def parse_raw_material(raw_input):
    """处理零散输入材料"""

    # 1. 识别材料类型
    material_type = detect_material_type(raw_input)
    # 类型: meeting_notes / requirement_list / code_snippet / mixed

    # 2. 提取关键要素
    extracted = {
        "functional_requirements": extract_features(raw_input),
        "non_functional": extract_nfr(raw_input),
        "compliance": extract_compliance(raw_input),
        "budget": extract_budget(raw_input),
        "traffic": extract_traffic(raw_input)
    }

    # 3. 识别缺失字段
    missing_fields = identify_missing_critical_fields(extracted)

    # 4. 生成追问列表
    questions = generate_questions(missing_fields)

    # 5. 与用户交互
    answers = interact_with_user(questions)

    # 6. 合并信息
    final_output = merge_and_structure(extracted, answers)

    return final_output
```

**信息提取模式匹配表:**

| 输入特征 | 可能包含的信息 | 提取策略 |
|---------|--------------|---------|
| 包含"用户量"、"DAU"、"QPS" | 流量估算 | 正则提取数值,单位标准化 |
| 包含"等保"、"GDPR"、"合规" | 合规要求 | 关键词匹配 |
| 包含"可用性"、"SLA"、"99.x%" | 可用性要求 | 提取百分比 |
| 包含"成本"、"预算"、"万元" | 预算限制 | 提取金额和周期 |
| 包含代码片段 | 技术栈信息 | 推断语言和框架 |
| 包含"会议"、"讨论"关键词 | 会议记录 | 提取决策项和待办 |

#### 3.2.2 追问优先级矩阵

**P0 - 必须追问(阻塞设计):**
- RTO/RPO(影响灾备设计)
- 可用性要求(影响 Multi-AZ 决策)
- 预估流量/QPS(影响扩展策略)
- AWS 区域(影响服务可用性)

**P1 - 强烈建议追问(影响成本和安全):**
- 合规性要求(影响架构复杂度)
- 数据敏感度(影响加密和访问控制)
- 峰值流量倍数(影响 Auto Scaling 配置)

**P2 - 可选追问(优化项):**
- 预算限制(用于成本优化)
- 运维团队技能(影响技术栈选择)
- 现有基础设施(混合云场景)

#### 3.2.3 示例: 从会议记录到结构化数据

**输入材料(零散会议记录):**
```
会议主题: XX电商平台云迁移讨论
参会人员: 张三(CTO)、李四(架构师)、王五(运维)

关键讨论点:
- 现有系统用 Java Spring Boot,MySQL 数据库
- 日活大概 5-10 万,高峰期会翻倍
- 希望迁到云上,减少运维成本
- 数据不能出境,必须在中国
- 老板要求 99.9% 可用性
- 预算还没定,先出个方案

待确认:
- 是否需要容器化? (李四倾向于先用虚拟机)
- 备份策略怎么做?
```

**Material Parser 处理流程:**

```json
{
  "extracted_info": {
    "functional_requirements": ["电商平台", "用户访问", "订单处理"],
    "tech_stack": {
      "language": "Java",
      "framework": "Spring Boot",
      "database": "MySQL"
    },
    "traffic": {
      "dau": "50,000 - 100,000",
      "peak_multiplier": "2x"
    },
    "constraints": {
      "region": "AWS China",
      "data_residency": "数据不得出境"
    },
    "non_functional": {
      "availability": "99.9%"
    }
  },
  "missing_critical_fields": ["RTO/RPO", "QPS", "数据量", "合规要求"],
  "generated_questions": [
    "请问对系统的 RTO(恢复时间目标)和 RPO(恢复点目标)有明确要求吗? 例如: RTO < 4h, RPO < 1h",
    "高峰期的 QPS(每秒请求数)大约是多少? 例如: 500 QPS",
    "当前数据库的数据量大约有多大? 例如: 100 GB",
    "除了数据不出境,是否还有其他合规要求? 例如: 等保二级"
  ]
}
```

**用户回答后的最终输出:**
```json
{
  "business_goals": ["云迁移", "降低运维成本", "提升可用性"],
  "functional_requirements": ["电商平台", "用户访问", "订单处理"],
  "non_functional_requirements": {
    "availability": "99.9%",
    "rto": "< 4h",
    "rpo": "< 1h"
  },
  "traffic_estimation": {
    "dau": "50,000 - 100,000",
    "peak_qps": "500",
    "data_volume": "200 GB",
    "peak_multiplier": "2x"
  },
  "constraints": {
    "region": "AWS China",
    "compliance": ["等保二级", "数据不得出境"],
    "tech_stack": "Java Spring Boot + MySQL",
    "budget": "未提供"
  },
  "assumptions": [
    "基于 Spring Boot,推荐使用 EC2 而非容器化(降低迁移成本)"
  ],
  "open_questions": [
    "是否需要 Redis 缓存来降低数据库压力?",
    "是否需要 CDN 加速静态资源?"
  ]
}
```

### 3.3 Architecture Decisioning - 架构决策引擎

**这是整个 Skill 最关键的"思考"步骤**,负责将结构化需求映射为具体的 AWS 架构设计。

#### 3.3.1 核心任务

1. **服务选型 (Service Selection)**
   - 将需求映射到具体 AWS 服务
   - 进行服务间的对比与权衡
   - 输出选择理由和替代方案

2. **AWS Well-Architected Framework 检查**
   - 强制基于 WAF 六大支柱进行推理
   - 确保设计符合最佳实践
   - 识别潜在的架构风险

#### 3.3.2 服务选型决策树

**决策流程:**

```
需求分类
    ↓
服务候选列表生成
    ↓
基于约束条件筛选
    ↓
WAF 六大支柱评估
    ↓
最终推荐 + 替代方案
```

**通用服务决策表:**

| 需求类型 | 关键约束 | 候选服务 | 决策依据 |
|---------|---------|---------|---------|
| 托管数据库 | 高可用、低运维 | RDS vs Aurora | Aurora: 性能更优但成本更高;<br>RDS: 成本友好,满足大部分场景 |
| 无服务器计算 | 按需扩展、无需管理 | Lambda vs Fargate | Lambda: 事件驱动、短任务;<br>Fargate: 长任务、容器化应用 |
| 对象存储 | 大规模、低成本 | S3 (唯一选择) | 标准/IA/Glacier 根据访问频率选择 |
| 缓存 | 低延迟读取 | ElastiCache Redis vs Memcached | Redis: 持久化、复杂数据结构;<br>Memcached: 简单缓存 |
| 负载均衡 | HTTP/HTTPS 流量 | ALB vs NLB | ALB: 7 层、支持路径路由;<br>NLB: 4 层、超高性能 |

**AI/ML 项目服务决策表:**

| 需求类型 | 关键约束 | 候选服务 | 决策依据 |
|---------|---------|---------|---------|
| **LLM 推理** | 成本、性能、功能 | Bedrock vs SageMaker | Bedrock: 托管模型、按 Token 计费、快速上线;<br>SageMaker: 自定义模型、实例计费、灵活性高 |
| **模型选择** | 任务类型、成本 | Claude 3.5 vs Llama 3 vs Titan | Claude: 推理能力强、多模态;<br>Llama: 开源、成本低;<br>Titan: AWS 原生、低成本 |
| **向量数据库** | 规模、性能、成本 | OpenSearch Serverless vs Kendra vs pgvector | OpenSearch: 灵活、成本优化;<br>Kendra: 开箱即用、企业级;<br>pgvector: 混合查询 |
| **知识库** | 文档类型、规模 | Bedrock KB vs Kendra | Bedrock KB: 自动向量化、简单;<br>Kendra: 企业搜索、复杂文档 |
| **Agent 框架** | 复杂度、集成 | Bedrock Agents vs LangChain (Lambda) | Bedrock Agents: 托管、集成度高;<br>LangChain: 灵活、社区生态 |
| **模型部署** | 流量、延迟 | SageMaker Real-time vs Serverless vs Batch | Real-time: 低延迟、稳定流量;<br>Serverless: 不定期流量;<br>Batch: 批量推理 |

**大数据项目服务决策表:**

| 需求类型 | 关键约束 | 候选服务 | 决策依据 |
|---------|---------|---------|---------|
| **离线分析** | 数据量、查询频率 | Athena vs Redshift | Athena: 即席查询、按查询付费、TB 级;<br>Redshift: 频繁查询、预留实例、PB 级 |
| **ETL 处理** | 复杂度、运维 | Glue vs EMR | Glue: Serverless、简单 ETL、自动扩展;<br>EMR: 复杂逻辑、Spark/Hadoop 生态 |
| **实时流** | 吞吐量、生态 | Kinesis vs MSK (Kafka) | Kinesis: 托管、AWS 集成、简单;<br>MSK: Kafka 生态、高吞吐、复杂 |
| **流处理** | 逻辑复杂度 | Lambda vs Kinesis Data Analytics (Flink) | Lambda: 简单转换、事件驱动;<br>Flink: 复杂窗口、状态计算 |
| **数据仓库** | 规模、并发 | Redshift vs Redshift Serverless | Redshift: 大规模、稳定负载、成本优化;<br>Serverless: 不定期查询、自动扩展 |
| **数据湖查询** | 数据格式、性能 | Athena vs Redshift Spectrum | Athena: 标准 SQL、按查询付费;<br>Spectrum: Redshift 集成、复杂查询 |

#### 3.3.3 AWS Well-Architected Framework 强制检查

**六大支柱评估矩阵:**

每个架构设计必须显式回答以下问题:

##### 1️⃣ 卓越运营 (Operational Excellence)
- [ ] 是否定义了运维流程和标准?
- [ ] 是否使用 IaC(Infrastructure as Code)?
- [ ] 是否配置了自动化运维工具(Systems Manager)?
- [ ] 是否建立了变更管理流程?

**检查点:**
- CloudWatch Logs 日志聚合
- EventBridge 自动化响应
- Systems Manager 补丁管理
- CloudFormation/Terraform IaC

##### 2️⃣ 安全性 (Security)
- [ ] 是否遵循最小权限原则(IAM)?
- [ ] 是否启用静态数据加密?
- [ ] 是否启用传输加密(TLS)?
- [ ] 是否配置网络隔离(VPC/Security Group)?
- [ ] 是否启用审计日志(CloudTrail)?

**检查点:**
- IAM 角色(禁止使用 Root)
- KMS 密钥管理
- WAF 防护(若有公网暴露)
- MFA 多因素认证
- VPC Flow Logs

##### 3️⃣ 可靠性 (Reliability)
- [ ] 是否实现 Multi-AZ 部署?
- [ ] 是否配置自动故障转移?
- [ ] 是否定义了 RTO/RPO?
- [ ] 是否配置了备份策略?
- [ ] 是否进行了容量规划?

**检查点:**
- RDS Multi-AZ / Aurora Replicas
- Auto Scaling 组配置
- 备份策略(AWS Backup / Snapshot)
- Route 53 健康检查

##### 4️⃣ 性能效率 (Performance Efficiency)
- [ ] 是否选择了适合工作负载的实例类型?
- [ ] 是否使用了缓存机制?
- [ ] 是否启用了 CDN(若适用)?
- [ ] 是否优化了数据库查询?

**检查点:**
- 实例类型选择(计算优化/内存优化/通用)
- ElastiCache / DAX 缓存
- CloudFront CDN
- RDS 性能洞察

##### 5️⃣ 成本优化 (Cost Optimization)
- [ ] 是否使用了 Auto Scaling 避免资源浪费?
- [ ] 是否考虑了 Reserved Instance / Savings Plans?
- [ ] 是否配置了 S3 生命周期策略?
- [ ] 是否启用了成本监控(Cost Explorer)?

**检查点:**
- Auto Scaling 策略
- S3 Intelligent-Tiering / Glacier
- Spot Instances(非关键工作负载)
- 成本告警(Budgets)

##### 6️⃣ 可持续性 (Sustainability)
- [ ] 是否选择了能效更高的实例类型(Graviton)?
- [ ] 是否优化了资源利用率?
- [ ] 是否选择了绿色能源的 Region?

**检查点:**
- Graviton 实例(ARM 架构)
- Serverless 优先(按需计费)
- 自动关闭开发/测试环境

---

#### 3.3.3.1 AI/ML 项目的特殊 WAF 检查

**AI/ML 项目在 WAF 六大支柱基础上,需额外考虑以下维度:**

##### 🤖 AI 特有检查点

**1. 成本优化 (AI Cost Optimization)**
- [ ] **Token 成本控制**
  - 是否设置单次请求 Token 上限?
  - 是否使用 Prompt 缓存减少重复调用?
  - 是否根据任务选择合适的模型(Claude vs Llama vs Titan)?
- [ ] **推理成本优化**
  - SageMaker Endpoint 是否使用 Auto Scaling?
  - 是否考虑 Serverless Inference(不定期流量)?
  - 训练是否使用 Spot Instances?
- [ ] **向量数据库成本**
  - 是否选择 OpenSearch Serverless 而非常驻集群?
  - 是否配置 Index 生命周期策略?

**2. 性能效率 (AI Performance)**
- [ ] **推理延迟**
  - 是否满足业务 SLA(如 <500ms)?
  - 是否使用缓存(Redis)减少重复推理?
  - 是否配置 Provisioned Throughput(高并发)?
- [ ] **模型选择**
  - 模型大小是否匹配任务复杂度(避免大材小用)?
  - 是否测试过多个模型的性能/成本比?
- [ ] **批处理优化**
  - 批量推理是否使用 Batch Transform?
  - 是否合并多个请求减少 API 调用?

**3. 安全性 (AI Security)**
- [ ] **数据隐私**
  - 训练数据是否加密存储(S3 + KMS)?
  - 是否使用 VPC Endpoints 避免公网传输?
  - Bedrock 是否选择不记录数据的模型?
- [ ] **Prompt Injection 防护**
  - 是否对用户输入进行过滤和验证?
  - 是否限制 System Prompt 不被覆盖?
- [ ] **模型访问控制**
  - 是否使用 IAM 细粒度控制模型调用权限?
  - 是否启用 CloudTrail 审计 API 调用?

**4. 可靠性 (AI Reliability)**
- [ ] **降级策略**
  - 当主模型不可用时,是否有备用模型?
  - 是否设置超时和重试机制?
- [ ] **幻觉检测**
  - 是否对 LLM 输出进行验证(如 Guardrails)?
  - 是否结合 RAG 提供事实依据?
- [ ] **版本管理**
  - 模型是否版本化(SageMaker Model Registry)?
  - 是否支持 A/B 测试和回滚?

**5. 卓越运营 (AI Operations - MLOps)**
- [ ] **监控与可观测性**
  - 是否监控模型性能指标(准确率、延迟、成本)?
  - 是否配置 SageMaker Model Monitor(数据漂移检测)?
  - 是否记录 Prompt/Response 用于调试?
- [ ] **持续优化**
  - 是否建立模型重训练流程?
  - 是否收集用户反馈优化 Prompt?

---

#### 3.3.3.2 大数据项目的特殊 WAF 检查

**大数据项目在 WAF 六大支柱基础上,需额外考虑以下维度:**

##### 📊 大数据特有检查点

**1. 成本优化 (Big Data Cost)**
- [ ] **存储成本**
  - S3 是否配置生命周期策略(Standard → IA → Glacier)?
  - 是否使用 S3 Intelligent-Tiering 自动优化?
  - 是否删除/归档过期数据?
- [ ] **计算成本**
  - EMR 是否使用临时集群(用后即删)?
  - 是否使用 Spot Instances(非关键任务)?
  - Redshift 是否使用 Reserved Instances / Serverless?
- [ ] **数据传输成本**
  - 是否使用 VPC Endpoints 避免公网流量费?
  - 跨 Region 复制是否必要?

**2. 性能效率 (Big Data Performance)**
- [ ] **查询性能**
  - S3 数据是否合理分区(按日期/地区)?
  - 是否使用列式存储(Parquet/ORC)?
  - Athena 查询是否优化(避免 SELECT *)?
- [ ] **数据处理性能**
  - EMR 实例类型是否适配工作负载(计算 vs 内存)?
  - Glue Job 是否配置合理的 DPU 数量?
  - Kinesis Shard 数量是否满足吞吐量?
- [ ] **并发控制**
  - Redshift 并发扩展是否启用?
  - Athena 查询是否限制并发数?

**3. 可靠性 (Big Data Reliability)**
- [ ] **数据一致性**
  - 是否处理重复数据(去重逻辑)?
  - 流处理是否支持 Exactly-Once 语义?
- [ ] **容错机制**
  - EMR 是否配置自动恢复?
  - Glue Job 是否支持 Bookmark(断点续传)?
  - 是否配置死信队列(DLQ)?
- [ ] **数据质量**
  - 是否配置 Glue Data Quality 检查?
  - 是否验证数据 Schema?

**4. 安全性 (Big Data Security)**
- [ ] **数据加密**
  - S3 是否启用服务端加密(SSE-S3/SSE-KMS)?
  - Redshift 是否启用加密?
  - Kinesis 是否启用传输加密?
- [ ] **访问控制**
  - 是否使用 Lake Formation 细粒度权限?
  - 是否遵循最小权限原则(IAM)?
  - 是否启用 S3 Bucket Policy 限制访问?
- [ ] **数据脱敏**
  - 敏感数据是否脱敏处理?
  - 是否使用 Glue DataBrew 进行数据清洗?

**5. 卓越运营 (Big Data Operations)**
- [ ] **监控与告警**
  - 是否监控 ETL Job 失败率?
  - 是否配置 Kinesis 数据积压告警?
  - Redshift 查询性能是否监控?
- [ ] **数据治理**
  - 是否建立数据目录(Glue Catalog)?
  - 是否定义数据保留策略?
  - 是否记录数据血缘关系?
- [ ] **自动化**
  - ETL 是否使用调度工具(Step Functions / MWAA)?
  - 是否自动化数据质量检查?

#### 3.3.4 服务选型示例

**场景: 需要托管关系型数据库**

```json
{
  "requirement": "托管关系型数据库,MySQL 兼容,需要高可用",
  "candidates": [
    {
      "service": "Amazon RDS for MySQL",
      "pros": [
        "完全托管,自动备份",
        "Multi-AZ 部署实现高可用",
        "成本相对较低"
      ],
      "cons": [
        "性能不如 Aurora",
        "扩展能力有限(最大 64 TiB)"
      ],
      "waf_assessment": {
        "operational_excellence": "✅ 自动补丁管理",
        "security": "✅ 支持 KMS 加密",
        "reliability": "✅ Multi-AZ 自动故障转移",
        "performance": "⚠️ 读副本扩展有限",
        "cost": "✅ 按需实例 + RI 优化",
        "sustainability": "⚠️ 标准实例,非 Graviton"
      },
      "recommended_for": "成本敏感、中等规模的 Web 应用"
    },
    {
      "service": "Amazon Aurora MySQL",
      "pros": [
        "性能是 RDS 的 5 倍",
        "自动扩展存储(最大 128 TiB)",
        "支持 Global Database(跨 Region)"
      ],
      "cons": [
        "成本比 RDS 高 20-30%",
        "复杂度稍高"
      ],
      "waf_assessment": {
        "operational_excellence": "✅ 自动补丁 + Backtrack",
        "security": "✅ KMS 加密 + IAM 认证",
        "reliability": "✅✅ 6 副本跨 3 AZ",
        "performance": "✅✅ 高性能 + 读副本",
        "cost": "⚠️ 成本较高",
        "sustainability": "⚠️ 标准实例"
      },
      "recommended_for": "高性能要求、大规模应用、需要 Global 部署"
    }
  ],
  "final_recommendation": {
    "choice": "Amazon RDS for MySQL",
    "reason": "基于需求分析,客户流量为 10 万 DAU,属于中等规模。RDS Multi-AZ 可满足高可用要求,成本更优。若未来流量增长 10 倍以上,建议迁移至 Aurora。",
    "alternative": "若预算允许或性能要求极高,可直接选择 Aurora"
  }
}
```

#### 3.3.5 架构模式库

**模式定义结构:**

```json
{
  "pattern_name": "Three-Tier Web Application",
  "applicable_when": ["Web 应用", "需要数据库", "中等并发"],
  "default_services": {
    "compute": ["EC2 Auto Scaling Group"],
    "load_balancer": ["Application Load Balancer"],
    "database": ["RDS Multi-AZ"],
    "storage": ["S3"],
    "cache": ["ElastiCache (可选)"]
  },
  "network": {
    "vpc": "Multi-AZ VPC",
    "subnet_tiers": ["Public", "Private", "Database"]
  },
  "waf_compliance": {
    "operational_excellence": "CloudWatch + Systems Manager",
    "security": "IAM + Security Groups + KMS",
    "reliability": "Multi-AZ + Auto Scaling",
    "performance": "ElastiCache + CloudFront(可选)",
    "cost": "Auto Scaling + RI",
    "sustainability": "Auto Scaling 优化资源利用率"
  }
}
```

**内置模式库:**

#### 传统应用架构

1. **Web 三层架构**
   - **核心服务**: ALB + EC2 ASG + RDS Multi-AZ
   - **适用场景**: 传统 Web 应用、中等并发
   - **流量规模**: 10 万 - 100 万 DAU

2. **Serverless API**
   - **核心服务**: API Gateway + Lambda + DynamoDB
   - **适用场景**: 轻量级 API、按需扩展
   - **流量规模**: 不定期流量、事件驱动

3. **SaaS 多租户**
   - **核心服务**: 租户隔离策略 + 资源池设计
   - **适用场景**: SaaS 应用、多租户管理
   - **关键考虑**: 数据隔离、计费、资源配额

4. **混合云 / 专线**
   - **核心服务**: Direct Connect + VPN + Transit Gateway
   - **适用场景**: 本地 IDC + 云混合部署
   - **关键考虑**: 网络延迟、数据传输成本

#### 大数据与分析架构

5. **批量数据处理平台 (Batch Data Pipeline)**
   - **核心服务**: S3 + AWS Glue + Athena / Redshift
   - **适用场景**: 离线数据分析、ETL、BI 报表
   - **数据规模**: TB - PB 级
   - **处理模式**: 定时批处理、T+1 数据
   - **典型流程**:
     ```
     数据源 → S3 (Data Lake) → Glue ETL →
     Athena (即席查询) / Redshift (数据仓库) → QuickSight (BI)
     ```
   - **关键决策**:
     - Athena vs Redshift: 查询频率和复杂度
     - Glue vs EMR: 数据转换复杂度
     - S3 分区策略: 查询性能优化

6. **实时数据处理平台 (Real-time Streaming)**
   - **核心服务**: Kinesis Data Streams + Kinesis Data Analytics + Lambda + DynamoDB
   - **适用场景**: IoT 数据、日志分析、实时监控、金融交易
   - **数据规模**: 百万级 TPS
   - **处理延迟**: 毫秒 - 秒级
   - **典型流程**:
     ```
     数据源 → Kinesis Data Streams →
     Kinesis Data Analytics (实时分析) / Lambda (处理) →
     DynamoDB (存储) / S3 (归档) / CloudWatch (监控)
     ```
   - **关键决策**:
     - Kinesis vs Kafka (MSK): 运维复杂度、生态兼容性
     - Lambda vs Flink (KDA): 处理逻辑复杂度
     - 数据保留策略: 成本 vs 合规要求

7. **数据湖架构 (Data Lake)**
   - **核心服务**: S3 + Lake Formation + Glue Catalog + Athena + Redshift Spectrum
   - **适用场景**: 多源异构数据、数据科学、ML 训练
   - **数据规模**: PB - EB 级
   - **架构层次**:
     - Raw Zone (S3): 原始数据
     - Curated Zone (S3 + Glue): 清洗后数据
     - Analytics Zone (Athena/Redshift): 分析层
   - **关键决策**:
     - 数据分区策略: 年/月/日
     - 数据格式: Parquet / ORC (列式存储优化查询)
     - 访问控制: Lake Formation 细粒度权限

8. **大数据计算集群 (Big Data Cluster)**
   - **核心服务**: EMR (Hadoop/Spark) + S3 + Glue Catalog
   - **适用场景**: 复杂 ETL、机器学习训练、图计算
   - **数据规模**: TB - PB 级
   - **计算模式**: 批处理 + 交互式查询
   - **关键决策**:
     - EMR vs Glue: 作业复杂度和定制需求
     - Spot Instances: 成本优化(非关键任务)
     - 集群生命周期: 常驻 vs 临时集群

#### AI/ML 与 Agentic 架构

9. **GenAI 应用架构 (Generative AI Application)**
   - **核心服务**: Amazon Bedrock + Lambda + API Gateway + DynamoDB + S3
   - **适用场景**: 聊天机器人、内容生成、文档摘要、代码辅助
   - **典型流程**:
     ```
     用户请求 → API Gateway → Lambda (业务逻辑) →
     Bedrock (LLM 推理) → DynamoDB (会话存储) →
     S3 (文档/知识库) → 用户响应
     ```
   - **关键决策**:
     - 模型选择: Claude / Llama / Titan (性能 vs 成本 vs 功能)
     - Prompt 缓存: 降低成本
     - 上下文管理: DynamoDB vs RDS
     - 成本控制: Token 限制、Rate Limiting

10. **RAG 架构 (Retrieval-Augmented Generation)**
    - **核心服务**: Bedrock Knowledge Bases + OpenSearch Serverless / Kendra + S3 + Lambda
    - **适用场景**: 企业知识库问答、文档检索、客服助手
    - **典型流程**:
      ```
      文档上传 → S3 → Bedrock Knowledge Base (自动向量化) →
      OpenSearch Serverless (向量存储) →
      用户查询 → 向量检索 → 相关文档 → Bedrock (生成答案)
      ```
    - **关键决策**:
      - 向量数据库选择:
        - OpenSearch Serverless: 成本优化、无需运维
        - Kendra: 开箱即用、企业级搜索
        - Aurora pgvector: 结构化+向量混合查询
      - Embedding 模型: Titan Embeddings vs 第三方
      - 检索策略: Top-K、相似度阈值

11. **AI Agentic 系统架构 (Multi-Agent System)**
    - **核心服务**: Bedrock Agents + Lambda (Tools) + DynamoDB + Step Functions + EventBridge
    - **适用场景**: 自主任务执行、多步骤工作流、API 编排
    - **架构组件**:
      - **Agent Orchestrator**: Bedrock Agents (任务规划、推理)
      - **Action Groups**: Lambda Functions (工具调用)
      - **Memory**: DynamoDB (会话状态、历史记录)
      - **Workflow**: Step Functions (复杂多步骤编排)
      - **Event-Driven**: EventBridge (异步任务触发)
    - **典型流程**:
      ```
      用户意图 → Bedrock Agent (规划) →
      选择 Action Group → Lambda (执行工具) →
      外部 API / 数据库查询 →
      Agent (综合结果) → 用户响应
      ```
    - **关键决策**:
      - Agent vs Lambda 编排: 任务复杂度、动态性
      - 工具设计: RESTful API / SDK 封装
      - 状态管理: DynamoDB TTL 策略
      - 错误处理: 重试机制、降级策略

12. **ML 训练与推理平台 (MLOps)**
    - **核心服务**: SageMaker + S3 + ECR + Model Registry + Endpoints
    - **适用场景**: 自定义模型训练、模型部署、A/B 测试
    - **架构层次**:
      - **数据准备**: SageMaker Data Wrangler + S3
      - **模型训练**: SageMaker Training Jobs (Spot Instances)
      - **模型注册**: SageMaker Model Registry
      - **模型部署**: SageMaker Endpoints (Real-time / Serverless / Batch)
      - **监控**: SageMaker Model Monitor + CloudWatch
    - **典型流程**:
      ```
      数据准备 → 特征工程 → 模型训练 →
      模型评估 → 模型注册 → 部署到 Endpoint →
      在线推理 / 批量推理 → 监控 → 重训练
      ```
    - **关键决策**:
      - 实例类型: GPU (训练) vs CPU (推理)
      - Endpoint 类型:
        - Real-time: 低延迟要求
        - Serverless: 不定期流量
        - Batch Transform: 批量推理
      - Auto Scaling: 基于调用量动态扩展
      - 成本优化: Spot Instances (训练)、Serverless (推理)

13. **多模态 AI 架构 (Multimodal AI)**
    - **核心服务**: Bedrock (Multimodal Models) + Rekognition + Textract + Transcribe + S3
    - **适用场景**: 图像识别、文档理解、语音转文字、视频分析
    - **典型流程**:
      ```
      多模态输入 (图片/PDF/音频/视频) → S3 →
      预处理 (Textract/Rekognition/Transcribe) →
      结构化数据 → Bedrock (多模态推理) →
      DynamoDB (结果存储) → 应用层
      ```
    - **关键决策**:
      - 专用服务 vs 通用 LLM:
        - Rekognition: 标准图像识别
        - Bedrock Claude 3: 自定义图像理解
      - 数据格式转换: 异步处理 vs 实时
      - 成本优化: 批量处理 vs 实时推理

#### 架构模式选择决策树

```python
def select_architecture_pattern(requirements):
    """根据需求选择架构模式"""

    # 1. AI/ML 项目识别
    if has_ai_ml_requirements(requirements):
        if "LLM" in requirements or "生成式 AI" in requirements:
            if "知识库" in requirements or "文档检索" in requirements:
                return "RAG 架构"
            elif "任务编排" in requirements or "多步骤" in requirements:
                return "AI Agentic 系统架构"
            else:
                return "GenAI 应用架构"

        elif "图像" in requirements or "视频" in requirements or "语音" in requirements:
            return "多模态 AI 架构"

        elif "自定义模型" in requirements or "模型训练" in requirements:
            return "ML 训练与推理平台"

    # 2. 大数据项目识别
    if has_bigdata_requirements(requirements):
        data_volume = requirements.get("data_volume")
        processing_mode = requirements.get("processing_mode")

        if processing_mode == "实时" or "流数据" in requirements:
            return "实时数据处理平台"

        elif data_volume in ["PB", "EB"] and "数据湖" in requirements:
            return "数据湖架构"

        elif "复杂 ETL" in requirements or "Spark" in requirements:
            return "大数据计算集群"

        else:
            return "批量数据处理平台"

    # 3. 传统应用识别
    if "Web 应用" in requirements:
        return "Web 三层架构"

    elif "API" in requirements and "Serverless" in requirements:
        return "Serverless API"

    elif "混合云" in requirements or "专线" in requirements:
        return "混合云 / 专线"

    else:
        return "需要进一步明确需求"
```

**关键原则:**
- ✅ 使用模式库 + WAF 评估选择服务
- ✅ 每个服务选择必须通过 WAF 六大支柱检查
- ✅ **AI/ML 项目额外考虑**: 模型成本、Token 限制、推理延迟
- ✅ **大数据项目额外考虑**: 数据分区、存储成本、查询性能
- ❌ 禁止让 LLM "自由选择"服务(易导致过度设计)
- ❌ 禁止跳过 WAF 评估直接输出方案

---

## 四、Design Writer - 输出文档模板

### 4.1 固定章节结构(不可删减、不可合并)

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
- 架构风格(如三层架构、Serverless 等)
- 核心组件概览
- 架构图文字描述

## 4. 网络架构设计
- VPC 设计
- 子网规划
- 路由与网关
- 混合云连接(如适用)

## 5. 计算层设计
- 计算服务选择(EC2 / Lambda / ECS / EKS)
- 扩展策略
- 容器 / 函数设计(如适用)

## 6. 存储与数据库设计
- 数据库选型(RDS / DynamoDB / Aurora)
- 对象存储(S3)
- 数据备份策略

## 7. 安全与权限设计
- IAM 角色与策略
- 网络安全(Security Group / NACL / WAF)
- 数据加密(传输 / 静态)
- 合规性(等保 / SOC2 等)

## 8. 高可用与灾备设计
- 多 AZ 部署
- RTO / RPO 目标
- 灾备方案(Backup / Snapshot / 跨 Region)

## 9. 运维与监控设计
- 日志聚合(CloudWatch Logs / S3)
- 监控告警(CloudWatch Alarms)
- 自动化运维(Systems Manager / EventBridge)

## 10. 成本与扩展性分析
- 成本估算
- 扩展性分析
- 成本优化建议(RI / Savings Plans / Spot)

## 11. 风险、假设与待确认事项
- 技术风险
- 假设列表
- 待客户确认的问题
```

### 4.2 每章节要求
- ✅ 明确说明**设计选择**
- ✅ 简要解释**为什么这样设计**(Why)
- ✅ 说明**权衡取舍**(Trade-off)
- ✅ 若信息不足,基于**假设**并明确标注

### 4.3 文风要求
- 技术说明书风格,不要营销或宣传语言
- 使用 Markdown 格式
- 语言:中文
- 适合直接交付客户或进入方案评审

---

## 五、Design Reviewer - 检查清单

### 5.1 区域合规性检查
- [ ] 若 `region = "AWS China"`,是否使用了 China 不可用的服务?
  - 例如:AWS Batch、Amazon Chime、某些 AI 服务
- [ ] 若 `region = "Global"`,是否考虑数据合规性(GDPR / 数据本地化)?

### 5.2 架构一致性检查
- [ ] 是否存在矛盾设计?
  - 例如:没有 NAT Gateway 却声称可以访问公网
  - 例如:RDS 单 AZ 部署却宣称高可用
- [ ] 是否出现过度设计?
  - 例如:小流量场景使用 EKS、Service Mesh
  - 例如:无明确需求却引入 Multi-Region

### 5.3 必备组件检查
- [ ] 是否遗漏 **IAM** 角色设计?
- [ ] 是否遗漏 **CloudWatch Logs** 日志方案?
- [ ] 是否遗漏 **Backup** 备份策略?
- [ ] 是否明确 **RTO / RPO**?
- [ ] 是否考虑 **成本估算**?

### 5.4 Best Practice 检查
- [ ] 是否使用 Multi-AZ 部署(生产环境)?
- [ ] 是否启用加密(传输 + 静态)?
- [ ] 是否启用 MFA(管理员账户)?
- [ ] 是否配置告警(CPU / Memory / Disk / Error Rate)?

---

## 六、实施指南与优化建议

### 6.1 Architecture Decisioning 执行要点

#### 6.1.1 防止过度设计

**常见问题:**
- LLM 倾向于使用复杂方案(EKS、Service Mesh、Multi-Region)
- LLM 倾向于"想当然"地添加未被要求的功能

**解决方案:**

1. **在 Decisioning 阶段添加约束 Prompt:**
   > "在没有明确需求时,选择能满足需求的**最简单方案**。
   > 例如:优先 EC2 + Auto Scaling,而非 EKS;优先单 Region,而非 Multi-Region。"

2. **引入人工确认机制:**
   - 当选择"复杂方案"时,输出决策理由并请求人工确认
   - 例如:"检测到您选择了 EKS,是否确认需要容器编排?简单场景建议使用 EC2。"

3. **复杂度评分机制:**
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

   # 若总分 > 10,触发人工确认
   if total_complexity_score > 10:
       request_confirmation("架构复杂度较高,是否确认?")
   ```

#### 6.1.2 WAF 检查强制执行

**关键原则: WAF 检查是 MANDATORY,不可跳过。**

**执行流程:**

```python
def architecture_decisioning(requirements):
    # 1. 服务选型
    services = service_selection(requirements)

    # 2. WAF 检查(强制)
    waf_result = perform_waf_assessment(services)

    # 3. 检查是否通过
    if waf_result.has_critical_issues():
        raise ArchitectureError("WAF 检查未通过,存在关键问题")

    # 4. 输出设计蓝图
    return generate_blueprint(services, waf_result)
```

**WAF 检查清单自动化:**

| 支柱 | 自动检查项 | 不通过的处理 |
|-----|----------|------------|
| 卓越运营 | CloudWatch Logs 是否配置? | 警告 + 建议 |
| 安全性 | IAM/KMS/TLS 是否启用? | **阻断**,必须修复 |
| 可靠性 | Multi-AZ 是否部署?(生产) | **阻断**,必须修复 |
| 性能效率 | 实例类型是否合理? | 警告 + 建议 |
| 成本优化 | Auto Scaling 是否配置? | 警告 + 建议 |
| 可持续性 | Graviton 是否考虑? | 提示(可选) |

**阻断级别:**
- 🔴 **Critical(阻断)**: 安全性、可靠性问题,必须修复才能继续
- 🟡 **Warning(警告)**: 非关键问题,记录到文档的"改进建议"
- 🟢 **Info(提示)**: 优化建议,不影响输出

### 6.2 强制输出 Why 和 Trade-off
在 Design Writer 的 Prompt 中强制要求:
- 每个技术选型必须写明**选择理由(Why)**
- 每个重要决策必须说明**权衡(Trade-off)**

**示例:**
```markdown
### 5.1 计算服务选择:EC2 Auto Scaling

**选择理由(Why):**
- 应用为传统 Web 框架(Spring Boot),迁移成本低
- 需要保持对运行时环境的完全控制
- 团队熟悉 EC2 运维

**权衡(Trade-off):**
- ✅ 优势:灵活性高,可深度定制
- ❌ 劣势:需要管理操作系统和补丁
- 💡 替代方案:若希望减少运维负担,可考虑 ECS Fargate
```

### 6.3 China Region 特判逻辑
**硬编码规则库:**
```json
{
  "china_unavailable_services": [
    "AWS Batch",
    "Amazon Chime",
    "Amazon Comprehend",
    "Amazon Forecast"
  ],
  "china_service_mapping": {
    "Route 53": "需使用 ICP 备案域名",
    "CloudFront": "需使用中国境内加速服务(如 CloudFront China)"
  }
}
```

在 Reviewer 阶段强制检查,若违反则拒绝输出。

---

## 七、推荐 Prompt 模板

### 7.1 Material Parser Prompt

```markdown
你是一名 AWS 解决方案架构师的助手,负责从零散、非结构化的客户材料中提取关键信息。

【输入】
用户提供的材料可能是:
- 会议记录(散乱的讨论要点)
- 简单需求列表(箭头式要点)
- 代码片段(现有系统实现)
- Word/Excel 文档
- 混合形式的文本

【你的任务】
1. **信息清洗与提取**
   从输入材料中提取以下 5 大关键要素:
   - 功能需求: 系统需要实现的业务功能
   - 非功能需求: 可用性、性能、延迟、扩展性、RTO/RPO
   - 合规性要求: 等保、GDPR、数据本地化等
   - 预算限制: 月度/年度预算上限
   - 预估流量: DAU、QPS、数据量、峰值倍数

2. **识别缺失信息**
   对于以下 **P0 关键信息**,如果缺失则必须标注:
   - RTO/RPO(恢复时间/恢复点目标)
   - 可用性要求(如 99.9%)
   - 预估流量/QPS
   - AWS 区域(Global / China)

3. **生成追问列表**
   对于缺失的 P0 信息,生成具体的追问问题:
   - 提供选项或参考值(如: "RTO < 4h, RPO < 1h")
   - 一次最多 3-5 个问题
   - 使用易于理解的语言

4. **输出结构化 JSON**
   按照以下格式输出:
   ```json
   {
     "business_goals": [...],
     "functional_requirements": [...],
     "non_functional_requirements": {...},
     "traffic_estimation": {...},
     "constraints": {...},
     "assumptions": [...],
     "open_questions": [...],
     "generated_questions_for_user": [...]
   }
   ```

【关键原则】
- ❌ 不要"脑补"未明确的强约束
- ✅ 优先提取明确信息,不确定的标注为"待确认"
- ✅ 对于代码片段,推断技术栈但不假设架构模式
- ✅ 对于会议记录,区分"已决策"和"待讨论"
- ✅ 生成的追问问题必须具体、可操作

【示例输出】
见文档第 3.2.3 节完整示例。
```

---

### 7.2 Architecture Decisioning Prompt

```markdown
你是一名资深 AWS 解决方案架构师,负责基于结构化需求数据进行架构决策。

【输入】
- Material Parser 输出的结构化需求 JSON
- 包含: 业务目标、功能/非功能需求、流量估算、约束条件

【你的任务】

#### 任务 1: 服务选型决策

对于每个需求维度(计算、存储、数据库、网络、缓存等),执行以下步骤:

1. **生成候选服务列表**
   - 基于需求类型,列出所有可能的 AWS 服务
   - 例如: "托管数据库" → [RDS, Aurora, DynamoDB]

2. **基于约束条件筛选**
   - Region 约束(China / Global)
   - 合规要求
   - 预算限制
   - 技术栈兼容性

3. **候选服务对比评估**
   - 列出每个候选服务的 优势(Pros) 和 劣势(Cons)
   - 说明适用场景
   - 估算成本差异

4. **输出最终推荐**
   - 选择 1 个主推方案
   - 提供 1-2 个替代方案
   - 写明决策理由(Why)
   - 说明权衡(Trade-off)

**示例格式:**
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
  "reason": "基于 10 万 DAU 的中等规模,RDS 性价比更优,满足 99.9% 可用性要求",
  "alternative": "若未来流量增长 10 倍,建议迁移至 Aurora"
}
```

#### 任务 2: AWS Well-Architected Framework 检查

**CRITICAL: 你必须对每个架构设计逐一进行 WAF 六大支柱检查。**

对于每个支柱,回答以下问题:

##### 1️⃣ 卓越运营 (Operational Excellence)
- [ ] 是否定义了运维流程和标准?
- [ ] 是否使用 IaC(CloudFormation/Terraform)?
- [ ] 是否配置了日志聚合(CloudWatch Logs)?
- [ ] 是否配置了自动化运维(Systems Manager)?

**输出示例:**
```json
{
  "operational_excellence": {
    "score": "✅ 符合",
    "evidence": [
      "使用 CloudWatch Logs 聚合日志",
      "配置 Systems Manager 自动补丁",
      "推荐使用 Terraform 进行 IaC"
    ],
    "improvements": [
      "建议建立变更管理流程"
    ]
  }
}
```

##### 2️⃣ 安全性 (Security)
- [ ] 是否遵循最小权限原则(IAM)?
- [ ] 是否启用静态数据加密(KMS)?
- [ ] 是否启用传输加密(TLS)?
- [ ] 是否配置网络隔离(VPC/SG)?
- [ ] 是否启用审计日志(CloudTrail)?

##### 3️⃣ 可靠性 (Reliability)
- [ ] 是否实现 Multi-AZ 部署?
- [ ] 是否配置自动故障转移?
- [ ] 是否定义了 RTO/RPO?
- [ ] 是否配置了备份策略?

##### 4️⃣ 性能效率 (Performance Efficiency)
- [ ] 实例类型是否适配工作负载?
- [ ] 是否使用了缓存(ElastiCache/CloudFront)?
- [ ] 是否优化了数据库查询?

##### 5️⃣ 成本优化 (Cost Optimization)
- [ ] 是否使用 Auto Scaling 避免浪费?
- [ ] 是否考虑 RI / Savings Plans?
- [ ] 是否配置 S3 生命周期策略?

##### 6️⃣ 可持续性 (Sustainability)
- [ ] 是否选择能效实例(Graviton)?
- [ ] 是否优化资源利用率?

**WAF 评估输出格式:**
```json
{
  "waf_assessment": {
    "operational_excellence": {"score": "✅", "evidence": [...], "improvements": [...]},
    "security": {"score": "✅", "evidence": [...], "improvements": [...]},
    "reliability": {"score": "⚠️", "evidence": [...], "improvements": ["需明确 RTO/RPO"]},
    "performance": {"score": "✅", "evidence": [...], "improvements": [...]},
    "cost": {"score": "✅", "evidence": [...], "improvements": [...]},
    "sustainability": {"score": "⚠️", "evidence": [...], "improvements": ["建议使用 Graviton"]}
  }
}
```

#### 任务 3: 架构模式匹配

从预定义模式库中选择最匹配的架构模式:
- Web 三层架构
- Serverless API
- 数据分析平台
- SaaS 多租户
- 混合云 / 专线

输出选择的模式及理由。

#### 任务 4: Region / China 特判

- 若 region = "AWS China",检查是否使用了不可用服务
- 输出服务可用性检查结果

#### 任务 5: AI/ML 与大数据项目的特殊处理

**如果项目类型为 AI/ML:**

1. **额外 WAF 检查**
   - AI Cost Optimization: Token 成本、推理成本、向量数据库成本
   - AI Performance: 推理延迟、模型选择、批处理优化
   - AI Security: 数据隐私、Prompt Injection 防护、访问控制
   - AI Reliability: 降级策略、幻觉检测、版本管理
   - MLOps: 监控、持续优化

2. **关键决策**
   - 模型选择(Bedrock vs SageMaker,Claude vs Llama)
   - 向量数据库选择(OpenSearch vs Kendra vs pgvector)
   - 部署方式(Real-time vs Serverless vs Batch)
   - 成本控制策略(Token 限制、缓存、模型降级)

3. **输出额外字段**
   ```json
   {
     "ai_specific": {
       "model_choice": "Claude 3.5 Sonnet",
       "model_reason": "推理能力强,支持多模态,适合复杂任务",
       "cost_estimate": "$0.003/1K input tokens + $0.015/1K output tokens",
       "vector_db": "OpenSearch Serverless",
       "embedding_model": "Titan Embeddings v2"
     }
   }
   ```

**如果项目类型为大数据:**

1. **额外 WAF 检查**
   - Big Data Cost: 存储成本、计算成本、数据传输成本
   - Big Data Performance: 查询性能、数据处理性能、并发控制
   - Big Data Reliability: 数据一致性、容错机制、数据质量
   - Big Data Security: 数据加密、访问控制、数据脱敏
   - Data Governance: 监控、数据治理、自动化

2. **关键决策**
   - 离线 vs 实时(Athena vs Kinesis)
   - ETL 工具(Glue vs EMR)
   - 数据仓库(Redshift vs Redshift Serverless)
   - 数据格式(Parquet vs ORC)
   - 分区策略(日期/地区/业务维度)

3. **输出额外字段**
   ```json
   {
     "bigdata_specific": {
       "processing_mode": "批处理 + 实时流",
       "etl_tool": "AWS Glue",
       "data_warehouse": "Redshift Serverless",
       "storage_format": "Parquet (列式存储)",
       "partition_strategy": "按日期分区 (year/month/day)",
       "estimated_data_volume": "1 TB/day,年增长 50%"
     }
   }
   ```

【输出格式】
```json
{
  "project_type": "AI/ML" | "Big Data" | "Web Application" | "...",
  "architecture_decisions": {
    "compute": {...},
    "database": {...},
    "storage": {...},
    "network": {...},
    "cache": {...}
  },
  "waf_assessment": {...},
  "architecture_pattern": "RAG 架构" | "实时数据处理平台" | "...",
  "pattern_reason": "企业知识库问答,需要文档检索和生成式 AI",
  "region_compliance": {
    "region": "AWS China",
    "unavailable_services": [],
    "warnings": []
  },
  "ai_specific": {...},  // 仅 AI/ML 项目
  "bigdata_specific": {...}  // 仅大数据项目
}
```

【关键原则】
- ✅ 每个服务选择必须通过 WAF 检查
- ✅ **AI/ML 项目必须通过 AI 特有检查点**
- ✅ **大数据项目必须通过大数据特有检查点**
- ✅ 必须提供决策理由和替代方案
- ✅ 优先选择最简单可满足需求的方案
- ❌ 禁止跳过 WAF 评估
- ❌ 禁止过度设计(无需求不上 EKS/Multi-Region)
- ❌ 禁止"脑补"未明确的需求
- ❌ **AI 项目禁止忽略成本控制(Token 限制、模型选择)**
- ❌ **大数据项目禁止忽略数据分区和存储优化**
```

---

### 7.3 Design Writer Prompt

```markdown
你是一名资深 AWS 解决方案架构师(SA),需要基于已解析的结构化需求数据,
编写一份《AWS 架构设计说明书》。

【输入】
- 业务目标、非功能需求、约束条件、假设、未确认事项(已结构化为 JSON)
- 已完成的架构设计蓝图(服务选型已确定)

【编写要求】
1. **严格按照以下章节顺序输出,不得合并或跳过:**
   1) 设计背景与目标
   2) 架构设计原则
   3) 总体架构概述
   4) 网络架构设计
   5) 计算层设计
   6) 存储与数据库设计
   7) 安全与权限设计
   8) 高可用与灾备设计
   9) 运维与监控设计
   10) 成本与扩展性分析
   11) 风险、假设与待确认事项

2. **每一章节必须包含:**
   - 设计选择的具体内容
   - 选择理由(Why)
   - 权衡说明(Trade-off)
   - 若信息不足,基于输入中的假设并**明确标注**

3. **禁止事项:**
   - ❌ 引入输入中未出现的强约束
   - ❌ 使用 AWS China 不可用的服务(若 region = China)
   - ❌ 过度设计(无需求不上 EKS / Multi-Region)

4. **文风要求:**
   - 技术说明书风格,避免营销语言
   - 适合直接交付客户或进入方案评审
   - 使用 Markdown 格式
   - 语言:中文

【输出格式】
- Markdown 文档
- 章节编号清晰(使用 ##、###)
- 代码块使用 ``` 标注
```

---

## 八、验收标准

### 8.1 文档完整性
- ✅ 包含全部 11 个章节,结构完整
- ✅ 每个技术选择都有 Why 和 Trade-off 说明
- ✅ 明确标注所有假设和待确认事项
- ✅ 文风专业,适合直接交付

### 8.2 架构决策质量
- ✅ **所有服务选择都经过 WAF 六大支柱评估**
- ✅ 每个服务选型都有候选对比和决策理由
- ✅ 提供了替代方案和升级路径
- ✅ 没有出现过度设计(复杂度评分合理)

### 8.3 技术合规性
- ✅ 通过 Reviewer 检查(无架构矛盾、无遗漏组件)
- ✅ 符合 AWS China / Global 区域限制
- ✅ 满足合规性要求(等保、GDPR 等)
- ✅ 安全性和可靠性检查通过(无 Critical 级别问题)

### 8.4 可追溯性
- ✅ 记录了 Material Parser 的交互历史
- ✅ 记录了 Architecture Decisioning 的决策过程
- ✅ WAF 评估结果可追溯

---

## 九、后续扩展方向

### 9.1 与其他 Skill 的集成
- **架构图生成 Skill**: 基于文字描述自动生成 Draw.io / Lucidchart 架构图
- **IaC 代码生成 Skill**: 将设计说明书转为 Terraform / CloudFormation 代码
- **成本计算 Skill**: 基于服务选型自动调用 AWS Pricing API 生成详细成本报告

### 9.2 知识库增强
- 集成 AWS Well-Architected Framework Lens 库
- 集成行业 Compliance 要求库(金融、医疗、政务)
- 集成 AWS 服务配额(Service Quotas)检查

### 9.3 交互式优化
- 支持多轮对话,逐步细化设计
- 支持"设计对比"功能(方案 A vs 方案 B)

---

## 附录:常见架构模式参考

### A.1 传统应用架构

| 模式名称 | 适用场景 | 核心服务 | 典型规模 |
|---------|---------|---------|---------|
| Web 三层架构 | 传统 Web 应用 | ALB + EC2 ASG + RDS Multi-AZ | 10 万 - 100 万 DAU |
| Serverless API | 轻量级 API | API Gateway + Lambda + DynamoDB | 不定期流量 |
| SaaS 多租户 | SaaS 应用 | 租户隔离 + 资源池 | 多租户管理 |
| 混合云 | 本地 IDC + 云 | Direct Connect + VPN + Transit Gateway | 混合部署 |
| 容器化应用 | 微服务架构 | ECS Fargate / EKS | 复杂微服务 |

### A.2 大数据架构

| 模式名称 | 适用场景 | 核心服务 | 数据规模 | 延迟 |
|---------|---------|---------|---------|------|
| 批量数据处理 | 离线分析、BI | S3 + Glue + Athena/Redshift | TB - PB | T+1 |
| 实时数据处理 | IoT、日志分析 | Kinesis + Lambda + DynamoDB | 百万 TPS | 毫秒 - 秒 |
| 数据湖 | 多源数据、ML | S3 + Lake Formation + Glue | PB - EB | 按需 |
| 大数据计算 | 复杂 ETL、图计算 | EMR + S3 + Glue Catalog | TB - PB | 分钟 - 小时 |

### A.3 AI/ML 架构

| 模式名称 | 适用场景 | 核心服务 | 典型应用 | 成本模型 |
|---------|---------|---------|---------|---------|
| GenAI 应用 | 聊天、内容生成 | Bedrock + Lambda + DynamoDB | ChatBot、摘要 | 按 Token |
| RAG 架构 | 知识库问答 | Bedrock KB + OpenSearch + S3 | 文档检索 | Token + 存储 |
| AI Agentic | 自主任务执行 | Bedrock Agents + Lambda + Step Functions | API 编排 | Token + 调用 |
| ML 训练推理 | 自定义模型 | SageMaker + S3 + ECR | 推荐系统 | 实例计费 |
| 多模态 AI | 图像、语音、文档 | Bedrock + Rekognition + Textract | OCR、识别 | 按请求 |

### A.4 架构模式选择速查表

```
用户需求关键词 → 推荐架构模式

"电商"、"Web"、"API" → Web 三层架构 / Serverless API
"大数据"、"分析"、"BI" → 批量数据处理 / 数据湖
"实时"、"流数据"、"IoT" → 实时数据处理
"聊天机器人"、"内容生成" → GenAI 应用
"知识库"、"文档检索" → RAG 架构
"任务编排"、"多步骤" → AI Agentic
"自定义模型"、"训练" → ML 训练推理
"图像识别"、"OCR" → 多模态 AI
"本地 IDC + 云" → 混合云
"容器"、"微服务" → 容器化应用
```

### A.5 服务选型速查表

#### AI/ML 服务选型

| 需求 | 首选方案 | 替代方案 | 关键考虑 |
|-----|---------|---------|---------|
| 聊天机器人 | Bedrock (Claude) | SageMaker (自定义) | 成本 vs 定制化 |
| 文档检索 | Bedrock KB | Kendra | 简单 vs 企业级 |
| 向量存储 | OpenSearch Serverless | pgvector | 成本 vs 混合查询 |
| 任务编排 | Bedrock Agents | LangChain (Lambda) | 托管 vs 灵活性 |
| 模型训练 | SageMaker Training | EMR (Spark ML) | 易用 vs 复杂度 |
| 实时推理 | SageMaker Real-time | Lambda (小模型) | 延迟 vs 成本 |
| 批量推理 | SageMaker Batch | Lambda (异步) | 数据量 vs 简单 |

#### 大数据服务选型

| 需求 | 首选方案 | 替代方案 | 关键考虑 |
|-----|---------|---------|---------|
| 即席查询 | Athena | Redshift Spectrum | 查询频率 |
| 数据仓库 | Redshift Serverless | Redshift | 负载稳定性 |
| ETL | Glue | EMR | 复杂度 |
| 实时流 | Kinesis | MSK (Kafka) | 生态兼容性 |
| 流处理 | Kinesis Analytics | Lambda | 逻辑复杂度 |
| 数据湖管理 | Lake Formation | 手动配置 | 治理需求 |

---

**文档版本:** v1.2
**最后更新:** 2026-01-06

## 版本历史

### v1.3 (2026-01-06)
⭐⭐ **重大更新: 大数据与 AI/ML 架构设计能力**

**新增架构模式 (9 个):**
- 批量数据处理平台 (S3 + Glue + Athena/Redshift)
- 实时数据处理平台 (Kinesis + Lambda + DynamoDB)
- 数据湖架构 (Lake Formation + S3 + Glue)
- 大数据计算集群 (EMR + Spark)
- GenAI 应用架构 (Bedrock + Lambda)
- RAG 架构 (Bedrock KB + OpenSearch)
- AI Agentic 系统 (Bedrock Agents + Step Functions)
- ML 训练推理平台 (SageMaker)
- 多模态 AI 架构 (Bedrock + Rekognition + Textract)

**新增服务选型决策:**
- AI/ML 服务决策表: LLM 推理、模型选择、向量数据库、Agent 框架、模型部署
- 大数据服务决策表: 离线分析、ETL、实时流、流处理、数据仓库、数据湖查询

**新增特殊 WAF 检查:**
- AI 特有检查点: Token 成本控制、推理性能优化、Prompt Security、幻觉检测、MLOps
- 大数据特有检查点: 存储成本优化、查询性能、数据一致性、数据治理、自动化

**其他更新:**
- 架构模式选择决策树 (Python 伪代码)
- Architecture Decisioning Prompt 增加 AI/大数据特殊处理 (任务 5)
- 附录增加架构模式速查表和服务选型速查表 (5 个速查表)

### v1.2 (2026-01-06)
⭐ **核心更新: Architecture Decisioning(架构决策引擎)**
- 新增: 服务选型决策树和对比评估流程
- 新增: AWS Well-Architected Framework 六大支柱强制检查机制
- 新增: 服务选型完整示例(RDS vs Aurora 对比)
- 新增: Architecture Decisioning Prompt 模板
- 新增: WAF 检查强制执行流程和阻断级别定义
- 新增: 复杂度评分机制防止过度设计
- 优化: 验收标准增加架构决策质量和可追溯性要求
- 更新: 流程图标注 WAF 评估环节

### v1.1 (2026-01-06)
- 新增: Material Parser 对零散材料的处理能力
- 新增: 5 大关键要素提取清单(功能需求、非功能需求、合规性、预算、流量)
- 新增: 主动交互机制和追问优先级矩阵
- 新增: 从会议记录到结构化数据的完整示例
- 新增: Material Parser Prompt 模板

### v1.0 (初始版本)
- 基础架构设计 Skill 需求定义
