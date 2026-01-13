# 使用示例汇总

本文档包含 AWS 架构设计说明书生成器的详细使用示例。更多基础内容请参考 [SKILL.md](./SKILL.md)。

---

## 示例 1: 电商平台迁移云

### 场景
客户提供散乱的会议记录，需要整理成架构设计说明书。

### 用户输入

```
会议主题: XX电商平台云迁移讨论
参会人员: 张三(CTO)、李四(架构师)、王五(运维)

关键讨论点:
- 现有系统用 Java Spring Boot, MySQL 数据库
- 日活大概 5-10 万，高峰期会翻倍
- 希望迁到云上，减少运维成本
- 数据不能出境，必须在中国
- 老板要求 99.9% 可用性
- 预算还没定，先出个方案

待确认:
- 是否需要容器化? (李四倾向于先用虚拟机)
- 备份策略怎么做?
```

### 步骤 1 输出（Material Parser）

```json
{
  "input_type": "meeting_notes",
  "project_type": "Web-Application",
  "business_goals": ["云迁移", "降低运维成本"],
  "functional_requirements": ["电商平台", "用户访问", "订单处理"],
  "non_functional_requirements": {
    "availability": "99.9%"
  },
  "traffic_estimation": {
    "dau": "50,000 - 100,000",
    "peak_multiplier": "2x"
  },
  "constraints": {
    "region": "AWS China",
    "tech_stack": "Java Spring Boot + MySQL",
    "data_residency": "数据不得出境"
  },
  "generated_questions_for_user": [
    "请问对系统的 RTO 和 RPO 有明确要求吗？例如: RTO < 4h, RPO < 1h",
    "高峰期的 QPS 大约是多少？例如: 500 QPS",
    "当前数据库的数据量大约有多大？例如: 100 GB"
  ],
  "user_provided_diagram": false
}
```

### 步骤 2 输出（架构图生成）

```json
{
  "diagram_source": "auto_generated",
  "diagram_file": "/tmp/architecture.png",
  "detected_services": ["ALB", "EC2", "RDS", "S3"],
  "diagram_text_description": "Web 三层架构，跨两个可用区部署..."
}
```

### 步骤 3 输出（架构决策）

```json
{
  "architecture_pattern": "Web 三层架构",
  "selected_services": {
    "compute": "EC2 Auto Scaling Group",
    "load_balancer": "Application Load Balancer",
    "database": "RDS for MySQL Multi-AZ",
    "storage": "S3",
    "cache": "ElastiCache Redis (可选)"
  },
  "architecture_decisions": {
    "database": {
      "recommendation": "RDS for MySQL",
      "reason": "完全托管，Multi-AZ 实现高可用，成本友好，满足 99.9% 可用性要求",
      "pros": [
        "完全托管，自动备份和补丁",
        "Multi-AZ 部署，自动故障转移",
        "成本相对较低"
      ],
      "cons": [
        "性能不如 Aurora",
        "扩展能力有限（最大 64 TiB）"
      ],
      "alternative": "若未来流量增长 10 倍以上，建议迁移至 Aurora"
    }
  },
  "waf_assessment": {
    "operational_excellence": "✅ CloudWatch Logs + Systems Manager",
    "security": "✅ IAM + KMS + TLS",
    "reliability": "✅ Multi-AZ + Auto Scaling",
    "performance": "✅ ElastiCache",
    "cost": "✅ Auto Scaling + RI",
    "sustainability": "⚠️ 建议考虑 Graviton 实例"
  }
}
```

### 最终输出（设计说明书）

生成 `电商平台迁移_架构设计说明书_v1.0.md`（11 个章节）

---

## 示例 2: AI 知识库问答系统（RAG）

### 场景
客户需要构建企业知识库 Q&A 系统。

### 用户输入

```
需求：开发企业知识库问答系统
- 用户可以上传公司文档（PDF、Word）
- 用户提问，系统根据文档内容回答
- 需要支持中文
- 预计 1000 个文档，每天 500 次查询
- 响应延迟需要 < 2 秒
```

### 步骤 1 输出

```json
{
  "project_type": "AI/ML-RAG",
  "business_goals": ["知识库自助服务", "降低人工客服成本"],
  "functional_requirements": [
    "文档上传和索引",
    "语义搜索和问答",
    "中文支持",
    "引用来源显示"
  ],
  "non_functional_requirements": {
    "latency": "< 2s",
    "availability": "99.9%",
    "concurrent_users": "100+"
  },
  "traffic_estimation": {
    "documents": "1000",
    "daily_queries": "500",
    "peak_qps": "20"
  },
  "generated_questions_for_user": [
    "文档中是否包含敏感信息（个人隐私、财务数据）？",
    "是否需要保留用户的查询日志用于改进？"
  ]
}
```

### 步骤 3 输出

```json
{
  "architecture_pattern": "RAG 架构",
  "selected_services": {
    "knowledge_base": "Bedrock Knowledge Bases",
    "vector_db": "OpenSearch Serverless",
    "llm": "Claude 3.5 Haiku",
    "api_gateway": "API Gateway",
    "compute": "Lambda",
    "storage": "S3"
  },
  "ai_specific": {
    "model_choice": "Claude 3.5 Haiku",
    "model_reason": "成本低（$0.0008/1K input），中文支持好，足以满足知识库问答需求",
    "cost_estimate": "$0.0008/1K input tokens + $0.0016/1K output tokens",
    "monthly_estimated_cost": "$50-100（假设平均 Query 长度 200 tokens，Response 150 tokens）",
    "vector_db": "OpenSearch Serverless",
    "vector_db_reason": "无需运维，按查询付费，成本优化",
    "embedding_model": "Titan Embeddings v2",
    "knowledge_base_strategy": "自动向量化，支持多文档格式"
  }
}
```

### 最终输出

生成 `企业知识库_RAG_架构设计说明书_v1.0.md`（11 个章节）

---

## 示例 3: AI 客服代理系统（Agentic）

### 场景
客户需要构建智能客服系统，支持多个工具集成和自主决策。

### 用户输入

```
需求：AI 客服代理系统
- Agent 能自主判断是否需要调用工具
- 集成订单查询、退货流程、账单系统 3 个工具
- 支持人类接管和人工审核
- 月均 10,000 次对话，峰值 50 QPS
- 对话历史保留 30 天用于审计
- 需要检测并防止幻觉回答（特别是关于订单、账户的信息）
```

### 步骤 1 输出

```json
{
  "project_type": "AI/ML-Agentic",
  "business_goals": ["自动化客服", "降低成本", "提升用户体验"],
  "functional_requirements": [
    "自然语言对话",
    "多工具集成",
    "人类接管机制",
    "故障降级"
  ],
  "tool_requirements": [
    {
      "name": "订单查询工具",
      "type": "REST API",
      "endpoint": "/api/orders",
      "required_params": ["order_id", "customer_id"]
    },
    {
      "name": "退货流程工具",
      "type": "REST API",
      "endpoint": "/api/returns",
      "required_params": ["order_id", "reason"]
    },
    {
      "name": "账单系统工具",
      "type": "REST API",
      "endpoint": "/api/billing",
      "required_params": ["customer_id"]
    }
  ],
  "non_functional_requirements": {
    "availability": "99.95%",
    "latency": "< 3s",
    "concurrent_users": "100+",
    "peak_qps": "50"
  },
  "compliance": {
    "audit_log_retention": "30 days",
    "pii_protection": "required"
  },
  "hallucination_risk": "HIGH (订单、账户、价格信息)",
  "human_in_loop": {
    "required": true,
    "trigger_scenarios": [
      "高置信度降级",
      "工具调用失败",
      "多轮无法解决",
      "敏感信息查询"
    ]
  }
}
```

### 步骤 3 输出

```json
{
  "architecture_pattern": "AI Agentic 系统架构",
  "selected_services": {
    "agent_orchestrator": "Bedrock Agents",
    "llm": "Claude 3.5 Sonnet",
    "action_groups": [
      "订单查询 (Lambda 1)",
      "退货流程 (Lambda 2)",
      "账单查询 (Lambda 3)"
    ],
    "state_storage": "DynamoDB",
    "session_management": "ElastiCache Redis",
    "audit_log": "CloudWatch Logs + S3",
    "human_handoff": "SNS + Lambda 通知"
  },
  "ai_specific": {
    "model_choice": "Claude 3.5 Sonnet",
    "model_reason": "强大的推理能力，支持复杂的工具选择逻辑，适合 Agentic AI",
    "estimated_monthly_cost": "$500-800（月均 10K 对话）",
    "cost_breakdown": {
      "agent_api_calls": "$100-150",
      "llm_tokens": "$300-400",
      "tool_invocations": "$50-100",
      "storage_and_logs": "$50"
    },
    "token_cost_control": [
      "使用 Prompt 缓存减少重复 token",
      "限制单次对话历史到最近 10 轮",
      "工具响应自动摘要而非完整返回",
      "按用户/会话维度监控 Token 使用"
    ]
  },
  "agent_orchestration": {
    "orchestrator": "Bedrock Agents",
    "reasoning_type": "Agentic reasoning",
    "action_groups": 3,
    "tool_selection_logic": "Agent 自主判断是否需要调用工具",
    "error_handling": {
      "tool_failure": "重试 1 次，失败则降级到人工",
      "network_timeout": "3s 超时自动降级",
      "invalid_response": "验证工具响应格式，失败则通知人工"
    }
  },
  "hallucination_mitigation": {
    "detection_strategy": "Fact checking + Guardrails",
    "high_risk_queries": [
      "订单信息（总是调用订单查询工具验证）",
      "价格信息（总是调用账单系统验证）",
      "账户状态（总是调用账户系统验证）"
    ],
    "confidence_scoring": "Agent 输出置信度评分，< 0.7 自动升级人工",
    "bedrock_guardrails": "启用 Guardrails 检测潜在幻觉内容"
  },
  "human_in_loop": {
    "trigger_scenarios": [
      "Agent 置信度 < 0.7",
      "工具调用失败",
      "多轮（> 5 轮）未解决",
      "敏感信息查询"
    ],
    "handoff_process": "通过 SNS 通知人工客服，DynamoDB 保存会话状态",
    "escalation_time": "< 30s 内通知人工"
  },
  "monitoring": {
    "agent_success_rate": "监控每个工具的调用成功率",
    "inference_latency": "监控 Agent 推理延迟（目标 < 2s）",
    "token_usage": "按 Agent/会话/用户维度监控",
    "hallucination_rate": "统计被检测出的幻觉内容比例",
    "human_escalation_rate": "监控需要人工接管的比例"
  }
}
```

### 最终输出

生成 `AI客服代理_Agentic_架构设计说明书_v1.0.md`（14 个章节，包括附录）

**关键差异**:
- ✨ 第 5 章：推理与 LLM 部署（Token 成本控制、模型选择理由）
- ✨ 第 6 章：Agent 编排与工具设计（3 个工具集成、错误处理、MCP 协议）
- ✨ 第 7 章：状态管理与记忆设计（会话管理、对话历史长度限制）
- ✨ 第 10 章：安全与负责任 AI（幻觉检测策略、Guardrails 配置、HITL 流程）
- ✨ 第 12 章：运维监控（Agent 成功率、推理延迟、幻觉率、人工接管率）
- 📎 附录 A：Agentic AI 能力评估矩阵
- 📎 附录 B：4 阶段实施路线图（开发→测试→上线→优化）

---

## 示例 4: 基于案例学习的快速设计

### 场景
用户上传了一份案例学习文件（电商平台迁移），希望基于类似案例快速设计新项目。

### 用户输入

```
案例文件: 电商平台云迁移案例.md
新需求: 我们的电商平台规模和技术栈与案例类似，
想基于案例的设计进行定制化调整
```

### 步骤 0 输出（案例分析）

```json
{
  "is_case_study": true,
  "case_study_metadata": {
    "title": "电商平台云迁移案例",
    "industry": "电商",
    "company_scale": "中型（日均 10 万用户）",
    "source_file": "电商平台迁移案例.md"
  },
  "pain_points": [
    "高运维成本: 5 人团队年度成本 150 万",
    "扩展困难: 高峰期流量翻倍无法快速扩展",
    "可用性低: 单点故障导致宕机，可用性仅 95%",
    "迁移风险: 技术栈不清，依赖关系复杂"
  ],
  "aws_solution": {
    "pattern": "Web 三层架构",
    "services": [
      {"name": "ALB", "role": "负载均衡"},
      {"name": "EC2 ASG", "role": "计算"},
      {"name": "RDS MySQL Multi-AZ", "role": "数据库"},
      {"name": "ElastiCache Redis", "role": "缓存"},
      {"name": "S3", "role": "存储"}
    ]
  },
  "expected_benefits": {
    "cost_savings": {
      "amount": "60万/年",
      "percentage": "40%",
      "baseline": "150万 → 90万"
    },
    "performance": {
      "response_time_improvement": "1.5s → 200ms (70% 提升)",
      "peak_qps_increase": "300 → 500 (67% 提升)"
    }
  },
  "match_with_new_project": {
    "relevance_score": 85,
    "relevance_level": "high",
    "reusable_services": [
      {"name": "EC2 ASG", "recommendation": "直接采用"},
      {"name": "RDS MySQL Multi-AZ", "recommendation": "直接采用"},
      {"name": "ALB", "recommendation": "直接采用"}
    ],
    "recommendations": [
      "强烈推荐采用相同的 Web 三层架构",
      "建议同样考虑 Multi-AZ 部署提升可用性",
      "重点关注数据库迁移和缓存策略"
    ]
  }
}
```

### 优化效果

- ✅ **减少 50% 的架构设计时间** - 直接基于验证过的案例
- ✅ **更准确的成本预算** - 基于案例的实际数据
- ✅ **降低风险** - 吸取案例的经验教训
- ✅ **加快决策** - 避免重复评估已验证的方案

---

## 总结

这些示例展示了不同场景下 AWS 架构设计说明书生成器的应用：

| 示例 | 项目类型 | 关键特点 | 输出模板 |
|-----|---------|---------|---------|
| 示例 1 | Web 应用 | 基础迁移、会议记录、追问确认 | 11 章 |
| 示例 2 | RAG 系统 | AI/LLM、向量存储、成本分析 | 11 章 |
| 示例 3 | Agentic | 复杂 Agent、多工具、幻觉检测、HITL | **14 章** |
| 示例 4 | 案例参考 | 快速决策、成本基线、经验教训 | 11 章 |

关键学习：
- 根据**项目类型**选择对应模板
- **充分进行 Material Parser** 确保所有 P0 信息已确认
- **AI Agentic 项目**需要额外关注 Token 成本、幻觉检测、人类在循环
- **案例学习**可加速 50% 的设计时间

更多细节请参考 [SKILL.md](./SKILL.md) 或 [DESIGN_WRITER_GUIDE.md](./DESIGN_WRITER_GUIDE.md)。
