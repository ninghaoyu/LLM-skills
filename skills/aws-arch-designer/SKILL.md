---
name: aws-arch-designer
description: AWS 架构设计说明书生成器。将零散的客户材料（会议记录、需求列表、代码片段等）转化为结构化、符合 AWS Best Practice 的《架构设计说明书》。支持 Web 应用、AI/ML（GenAI、RAG、Agentic）、大数据（批处理、实时流、数据湖）等多种架构类型。使用场景：(1) 客户提供零散需求材料需要整理；(2) 需要进行 AWS 架构设计；(3) 需要生成标准化的架构设计文档；(4) 需要基于 AWS Well-Architected Framework 进行架构评估；(5) AI/ML 项目架构设计；(6) 大数据平台架构设计。
---

# AWS 架构设计说明书生成器

将零散的客户材料自动转化为结构化、可审计、符合 AWS Best Practice 的《架构设计说明书》。

## 核心能力

- **材料解析**: 处理会议记录、需求列表、代码片段等零散材料
- **智能追问**: 自动识别缺失信息并主动追问
- **架构决策**: 基于 AWS Well-Architected Framework 进行服务选型
- **多场景支持**: Web 应用、AI/ML、大数据、SaaS、混合云
- **标准化输出**: 生成完整的架构设计说明书

## 工作流程

此 Skill 遵循严格的 **5 步流程**，**不可跳过或合并**：

### 步骤 0: 案例学习文件识别（可选但推荐）

**功能**: 自动识别和参考案例学习文件

**何时触发**:
- 用户提供包含"案例"、"case study"、"项目背景"、"痛点"、"解决方案"等关键词的文档

**执行任务**:

1. **自动检测案例文件**:
   使用 `scripts/case_study_analyzer.py` 中的 `CaseStudyDetector`
   - 文件名模式识别（case study、案例、迁移方案等）
   - 内容关键词识别（20+ 中英文关键词）
   - 自动判定文件是否为案例学习文件

2. **结构化信息提取**:
   从案例文件中提取：
   - **项目背景**: 行业、公司规模、现状基础设施
   - **痛点分析**: 问题描述、影响、严重程度
   - **AWS 解决方案**: 服务组合、架构模式、配置
   - **关键指标**: 可用性、性能、流量、数据量
   - **预期收益**: 成本节省、性能提升、业务影响
   - **经验教训**: 关键经验和最佳实践
   - **架构图**: 自动检测（Markdown 和 HTML 格式）

3. **与新项目进行相关性匹配**:
   使用 `CaseStudyMatcher` 计算相关性分数（0-100）
   - 行业相似性 (30 分)
   - 公司规模相似性 (20 分)
   - 痛点相似性 (30 分)
   - 功能需求相似性 (20 分)
   - 架构模式一致性 (bonus 10 分)

   相关性等级：
   - **High (≥70)**: 强烈推荐参考，可直接采用案例的架构模式
   - **Medium (40-69)**: 部分参考价值，某些服务和经验可复用
   - **Low (<40)**: 参考价值有限

4. **提取可复用资源**:
   - 验证过的 AWS 服务组合
   - 成本基线数据
   - 关键经验教训
   - 风险规避建议

**输出结构**:
```json
{
  "is_case_study": true,
  "case_study_metadata": {
    "title": "项目标题",
    "industry": "行业",
    "company_scale": "公司规模"
  },
  "pain_points": [...],
  "aws_solution": {...},
  "key_metrics": {...},
  "expected_benefits": {...},
  "lessons_learned": [...],
  "match_with_new_project": {
    "relevance_score": 85,
    "relevance_level": "high",
    "reusable_services": [...],
    "recommendations": [...]
  }
}
```

**关键原则**:
- ✅ 相似案例可加速架构决策
- ✅ 从案例中提取验证过的最佳实践
- ✅ 吸取案例的经验教训规避风险
- ✅ 基于案例的成本数据进行预算规划
- ❌ 不要盲目复制，需要考虑新项目的特殊约束

---

### 步骤 1: Material Parser (材料解析)

**目标**: 从零散材料中提取结构化需求信息，检测是否为案例学习文件

**输入材料可能是**:
- 会议记录（散乱的讨论要点）
- 简单需求列表（箭头式要点）
- 代码片段（现有系统实现参考）
- Word/Excel 文档
- 混合形式的文本
- **案例学习文件**（包含背景、痛点、方案、架构图、收益）
- **架构图**（用户上传的 PNG/PDF/JPEG）

**执行任务**:

1. **提取 5 大关键要素**:
   - 功能需求：系统需要实现的业务功能
   - 非功能需求：可用性、性能、延迟、扩展性、RTO/RPO
   - 合规性要求：等保、GDPR、数据本地化等
   - 预算限制：月度/年度预算上限
   - 预估流量：DAU、QPS、数据量、峰值倍数

2. **检测案例学习文件**:
   使用 `scripts/case_study_analyzer.py` 中的 `CaseStudyDetector`
   - 如果检测到案例文件，触发步骤 0 的案例分析流程
   - 提取案例中的关键信息用于参考和决策

3. **识别项目类型**:
   使用 `scripts/material_parser.py` 中的 `identify_project_type()` 函数
   - AI/ML 项目：GenAI、RAG、Agentic
   - 大数据项目：批处理、实时流、数据湖
   - 传统应用：Web、SaaS、混合云

4. **标注缺失信息**:
   识别 P0 关键信息（RTO/RPO、可用性、流量、区域）

5. **生成追问列表**:
   使用 `scripts/material_parser.py` 中的 `generate_clarification_questions()` 函数
   - 提供选项或参考值（如: "RTO < 4h, RPO < 1h"）
   - 一次最多 3-5 个问题
   - 使用易于理解的语言

6. **输出结构化 JSON**:
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

**关键原则**:
- ❌ 不要"脑补"未明确的强约束
- ✅ 优先提取明确信息，不确定的标注为"待确认"
- ✅ 对于代码片段，推断技术栈但不假设架构模式
- ✅ 对于会议记录，区分"已决策"和"待讨论"
- ✅ 生成的追问问题必须具体、可操作

**如果有追问问题**: 向用户展示问题并等待回答，然后合并回答到结构化数据中。

---

### 步骤 2: Architecture Diagram Generation (架构图生成与验证)

**目标**: 获取或生成架构图，并验证其与需求的匹配度

**前置条件**: 步骤 1 已完成，所有 P0 信息已确认

**处理两种情况**:

#### 情况 1: 用户提供了架构图（PNG/PDF/JPEG）

**执行任务**:

1. **检测和识别架构图**:
   使用 `scripts/diagram_generator.py` 中的 `DiagramGenerator.detect_user_diagram()`
   - 识别图片中的 AWS 服务图标
   - 提取架构图中的数据流和连接关系
   - 识别关键配置（Multi-AZ、Auto Scaling 等）

2. **生成架构图文字描述**:
   使用 `DiagramDescriptionGenerator.generate_from_blueprint()`
   - 生成 Markdown 格式的架构描述
   - 用于后续的 Design Writer 阶段

3. **验证架构图与需求的匹配度**:
   使用 `DiagramValidator` 进行一致性检查：
   - ✅ **服务完整性检查**: 架构图中的服务是否包含所有关键服务
   - ✅ **Multi-AZ 部署检查**: 生产环境是否明确 Multi-AZ 配置
   - ✅ **连接关系检查**: 服务间连接是否有效和正确
   - ✅ **配置一致性检查**: 关键参数是否与需求匹配

4. **输出**:
```json
{
  "diagram_source": "user_provided",
  "detected_services": ["ALB", "EC2", "RDS", "S3"],
  "diagram_text_description": "架构图文字描述...",
  "consistency_check": {
    "service_completeness": "✅ Pass",
    "multi_az_deployment": "✅ Pass",
    "connection_validity": "✅ Pass",
    "issues": []
  }
}
```

#### 情况 2: 用户未提供架构图

**执行任务**:

1. **构建架构蓝图**:
   使用 `scripts/diagram_generator.py` 中的 `BlueprintBuilder`
   基于步骤 1 的结构化需求构建蓝图，包括：
   - 计算层服务（EC2、Lambda、Fargate 等）
   - 数据库服务（RDS、DynamoDB、Aurora 等）
   - 缓存服务（ElastiCache 等）
   - 存储服务（S3 等）
   - 负载均衡（ALB、NLB 等）
   - 服务间连接关系

2. **调用 MCP Server 生成架构图**:
   使用 `scripts/mcp_diagram_client.py` 中的 `MCPDiagramClient`
   - 连接到 `awslabs-aws-diagram-mcp-server`
   - 传入架构蓝图
   - 返回 PNG/SVG 格式的架构图

3. **生成架构图文字描述**:
   与情况 1 相同

4. **进行一致性验证**:
   与情况 1 相同的 4 项检查

5. **降级方案**:
   如果 MCP Server 不可用，使用纯文本描述架构而不生成图片

**输出**:
```json
{
  "diagram_source": "auto_generated",
  "diagram_file": "/tmp/architecture.png",
  "diagram_format": "PNG",
  "services": [...],
  "connections": [...],
  "diagram_text_description": "架构图文字描述...",
  "consistency_check": {...}
}
```

**关键原则**:
- ✅ 所有设计最终都应有对应的架构图表示
- ✅ 架构图和设计文档必须保持一致
- ✅ 检查清单必须全部通过
- ❌ 如果一致性检查失败，返回步骤 1 重新分析需求

---

### 步骤 4: Architecture Decisioning (架构决策)

**目标**: 基于结构化需求进行服务选型和 WAF 评估

**前置条件**: 步骤 1 已完成，且所有 P0 问题已得到回答，架构图已处理

**执行任务**:

#### 任务 3.1: 选择架构模式

根据项目类型从 `references/architecture_patterns.md` 中选择匹配的架构模式。

**决策逻辑**:
```python
if project_type.startswith("AI/ML"):
    if "知识库" in requirements or "文档检索" in requirements:
        pattern = "RAG 架构"
    elif "agent" in requirements or "任务编排" in requirements:
        pattern = "AI Agentic 系统"
    else:
        pattern = "GenAI 应用架构"
elif project_type.startswith("BigData"):
    if "实时" in requirements or "流数据" in requirements:
        pattern = "实时数据处理平台"
    elif "数据湖" in requirements:
        pattern = "数据湖架构"
    else:
        pattern = "批量数据处理平台"
else:
    pattern = "Web 三层架构"
```

#### 任务 3.2: 服务选型决策

对于每个需求维度（计算、存储、数据库、网络、缓存等），执行以下步骤：

1. **生成候选服务列表**
   - 基于需求类型，列出所有可能的 AWS 服务
   - 例如："托管数据库" → [RDS, Aurora, DynamoDB]

2. **基于约束条件筛选**
   - Region 约束（China / Global）
   - 合规要求
   - 预算限制
   - 技术栈兼容性

3. **候选服务对比评估**
   - 列出每个候选服务的优势（Pros）和劣势（Cons）
   - 说明适用场景
   - 估算成本差异

4. **输出最终推荐**
   - 选择 1 个主推方案
   - 提供 1-2 个替代方案
   - 写明决策理由（Why）
   - 说明权衡（Trade-off）

**示例输出格式**:
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
    }
  ],
  "recommendation": "Amazon RDS for MySQL",
  "reason": "基于 10 万 DAU 的中等规模，RDS 性价比更优",
  "alternative": "若未来流量增长 10 倍，建议迁移至 Aurora"
}
```

#### 任务 3.3: AWS Well-Architected Framework 检查

**CRITICAL**: 必须对每个架构设计逐一进行 WAF 六大支柱检查。

使用 `references/waf_checklist.md` 中的检查清单。

**六大支柱**:
1. 卓越运营（Operational Excellence）
2. 安全性（Security）
3. 可靠性（Reliability）
4. 性能效率（Performance Efficiency）
5. 成本优化（Cost Optimization）
6. 可持续性（Sustainability）

**对于每个支柱**，输出:
```json
{
  "operational_excellence": {
    "score": "✅ 符合" | "⚠️ 部分符合" | "❌ 不符合",
    "evidence": ["使用 CloudWatch Logs 聚合日志", "..."],
    "improvements": ["建议建立变更管理流程"]
  }
}
```

#### 任务 3.4: AI/ML 与大数据项目特殊处理

**如果项目类型为 AI/ML**:

1. **额外 WAF 检查**（参考 `references/waf_checklist.md` AI 章节）:
   - AI Cost: Token 成本、推理成本、向量数据库成本
   - AI Performance: 推理延迟、模型选择、批处理优化
   - AI Security: 数据隐私、Prompt Injection 防护
   - AI Reliability: 降级策略、幻觉检测、版本管理
   - MLOps: 监控、持续优化

2. **关键决策**:
   - 模型选择（Bedrock vs SageMaker，Claude vs Llama）
   - 向量数据库选择（OpenSearch vs Kendra vs pgvector）
   - 部署方式（Real-time vs Serverless vs Batch）
   - 成本控制策略（Token 限制、缓存、模型降级）

3. **输出额外字段**:
   ```json
   {
     "ai_specific": {
       "model_choice": "Claude 3.5 Sonnet",
       "model_reason": "推理能力强，支持多模态",
       "cost_estimate": "$0.003/1K input tokens",
       "vector_db": "OpenSearch Serverless",
       "embedding_model": "Titan Embeddings v2"
     }
   }
   ```

**如果项目类型为大数据**:

1. **额外 WAF 检查**（参考 `references/waf_checklist.md` 大数据章节）:
   - Big Data Cost: 存储成本、计算成本、数据传输成本
   - Big Data Performance: 查询性能、数据处理性能
   - Big Data Reliability: 数据一致性、容错机制
   - Big Data Security: 数据加密、访问控制
   - Data Governance: 监控、数据治理、自动化

2. **关键决策**:
   - 离线 vs 实时（Athena vs Kinesis）
   - ETL 工具（Glue vs EMR）
   - 数据仓库（Redshift vs Redshift Serverless）
   - 数据格式（Parquet vs ORC）
   - 分区策略（日期/地区/业务维度）

3. **输出额外字段**:
   ```json
   {
     "bigdata_specific": {
       "processing_mode": "批处理 + 实时流",
       "etl_tool": "AWS Glue",
       "data_warehouse": "Redshift Serverless",
       "storage_format": "Parquet",
       "partition_strategy": "按日期分区 (year/month/day)"
     }
   }
   ```

#### 任务 3.5: Region / China 特判

- 若 `region = "AWS China"`，检查是否使用了不可用服务
- 输出服务可用性检查结果

**完整输出格式**:
```json
{
  "project_type": "AI/ML-RAG" | "BigData-Streaming" | "Web-Application",
  "architecture_pattern": "RAG 架构",
  "selected_services": {...},
  "architecture_decisions": {
    "compute": {...},
    "database": {...},
    "storage": {...}
  },
  "waf_assessment": {...},
  "region_compliance": {
    "region": "AWS China",
    "warnings": []
  },
  "ai_specific": {...},       // 仅 AI/ML 项目
  "bigdata_specific": {...}   // 仅大数据项目
}
```

**关键原则**:
- ✅ 每个服务选择必须通过 WAF 检查
- ✅ AI/ML 项目必须通过 AI 特有检查点
- ✅ 大数据项目必须通过大数据特有检查点
- ✅ 必须提供决策理由和替代方案
- ❌ 禁止跳过 WAF 评估
- ❌ 禁止过度设计（无需求不上 EKS/Multi-Region）
- ❌ AI 项目禁止忽略成本控制（Token 限制）
- ❌ 大数据项目禁止忽略数据分区和存储优化

---

### 步骤 4: Design Writer (文档生成)

**目标**: 按固定模板生成架构设计说明书

**前置条件**: 步骤 2 已完成，架构图已获取或生成，所有服务选型和 WAF 评估已完成

**执行任务**:

使用 `assets/design_doc_template.md` 作为基础模板。

**章节要求（严格按顺序，不可合并或跳过）**:

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

**每一章节必须包含**:
- 设计选择的具体内容
- 选择理由（Why）
- 权衡说明（Trade-off）
- 若信息不足，基于步骤 1 中的假设并**明确标注**

**文风要求**:
- 技术说明书风格，避免营销语言
- 适合直接交付客户或进入方案评审
- 使用 Markdown 格式
- 语言：中文

**禁止事项**:
- ❌ 引入步骤 1 中未出现的强约束
- ❌ 使用 AWS China 不可用的服务（若 region = China）
- ❌ 过度设计（无需求不上 EKS / Multi-Region）

**输出**: 完整的 Markdown 文档，章节编号清晰（使用 ##、###）

---

### 步骤 5: Design Reviewer (设计审查)

**目标**: 检查架构设计的完整性和正确性

**前置条件**: 步骤 3 已完成，设计文档已生成

**执行任务**:

#### 4.1 区域合规性检查
- [ ] 若 `region = "AWS China"`，是否使用了 China 不可用的服务？
- [ ] 若 `region = "Global"`，是否考虑数据合规性（GDPR / 数据本地化）？

#### 4.2 架构一致性检查
- [ ] 是否存在矛盾设计？
  - 例如：没有 NAT Gateway 却声称可以访问公网
  - 例如：RDS 单 AZ 部署却宣称高可用
- [ ] 是否出现过度设计？
  - 例如：小流量场景使用 EKS、Service Mesh
  - 例如：无明确需求却引入 Multi-Region

#### 4.3 必备组件检查
- [ ] 是否遗漏 **IAM** 角色设计？
- [ ] 是否遗漏 **CloudWatch Logs** 日志方案？
- [ ] 是否遗漏 **Backup** 备份策略？
- [ ] 是否明确 **RTO / RPO**？
- [ ] 是否考虑 **成本估算**？

#### 4.4 Best Practice 检查
- [ ] 是否使用 Multi-AZ 部署（生产环境）？
- [ ] 是否启用加密（传输 + 静态）？
- [ ] 是否启用 MFA（管理员账户）？
- [ ] 是否配置告警（CPU / Memory / Disk / Error Rate）？

**输出**: 问题清单与修订建议

如果发现问题，返回步骤 3 进行修订。

---

## 使用示例

### 示例 1: 电商平台迁移云

**用户输入**（零散会议记录）:
```
会议主题: XX电商平台云迁移讨论
关键讨论点:
- 现有系统用 Java Spring Boot, MySQL 数据库
- 日活大概 5-10 万，高峰期会翻倍
- 希望迁到云上，减少运维成本
- 数据不能出境，必须在中国
- 老板要求 99.9% 可用性
```

**步骤 1 输出**:
```json
{
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
    "tech_stack": "Java Spring Boot + MySQL"
  },
  "generated_questions_for_user": [
    "请问对系统的 RTO 和 RPO 有明确要求吗？例如: RTO < 4h, RPO < 1h",
    "高峰期的 QPS 大约是多少？例如: 500 QPS"
  ]
}
```

**步骤 2 输出**:
```json
{
  "architecture_pattern": "Web 三层架构",
  "selected_services": {
    "compute": "EC2 Auto Scaling Group",
    "load_balancer": "Application Load Balancer",
    "database": "RDS for MySQL Multi-AZ"
  },
  "architecture_decisions": {
    "database": {
      "recommendation": "RDS for MySQL",
      "reason": "成本友好，满足 99.9% 可用性要求",
      "alternative": "若未来流量增长 10 倍，建议迁移至 Aurora"
    }
  }
}
```

**最终输出**: 完整的架构设计说明书（11 个章节）

---

### 示例 2: AI 聊天机器人

**用户输入**:
```
需求：开发一个企业知识库问答系统
- 用户可以上传公司文档（PDF、Word）
- 用户提问，系统根据文档内容回答
- 需要支持中文
- 预计 1000 个文档，每天 500 次查询
```

**步骤 1 输出**:
```json
{
  "project_type": "AI/ML-RAG",
  "functional_requirements": [
    "文档上传",
    "知识库问答",
    "中文支持"
  ],
  "traffic_estimation": {
    "documents": "1000",
    "daily_queries": "500"
  },
  "generated_questions_for_user": [
    "对响应延迟有要求吗？例如: <2秒",
    "每月的 AI 成本预算是多少？"
  ]
}
```

**步骤 2 输出**:
```json
{
  "architecture_pattern": "RAG 架构",
  "selected_services": {
    "knowledge_base": "Bedrock Knowledge Bases",
    "vector_db": "OpenSearch Serverless",
    "llm": "Claude 3.5 Haiku"
  },
  "ai_specific": {
    "model_choice": "Claude 3.5 Haiku",
    "model_reason": "成本低，适合简单问答，中文支持好",
    "cost_estimate": "$0.0008/1K input + $0.0016/1K output",
    "vector_db": "OpenSearch Serverless",
    "embedding_model": "Titan Embeddings v2"
  }
}
```

**最终输出**: 针对 RAG 架构的完整设计说明书

---

### 示例 3: 基于案例学习的快速设计

**用户输入**（包含案例文件 + 新项目需求）:
```
案例文件: 电商平台云迁移案例.md
新需求: 我们的电商平台与案例中的项目类似，
想基于案例的设计进行定制化调整
```

**步骤 0 输出**（案例分析）:
```json
{
  "is_case_study": true,
  "case_study_metadata": {
    "title": "电商平台云迁移案例",
    "industry": "电商"
  },
  "pain_points": [
    "高运维成本(年150万)",
    "扩展困难(高峰流量翻倍)",
    "可用性低(仅95%)"
  ],
  "aws_solution": {
    "pattern": "Web 三层架构",
    "services": ["ALB", "EC2 ASG", "RDS MySQL", "S3", "ElastiCache"]
  },
  "expected_benefits": {
    "cost_savings": "60万/年(40%)",
    "performance": "响应时间提升70%"
  },
  "match_with_new_project": {
    "relevance_score": 85,
    "relevance_level": "high",
    "reusable_services": [
      {"name": "EC2 ASG", "role": "计算"},
      {"name": "RDS MySQL", "role": "数据库"},
      {"name": "ALB", "role": "负载均衡"}
    ],
    "recommendations": [
      "强烈推荐采用相同的 Web 三层架构",
      "建议同样考虑 Multi-AZ 部署提升可用性",
      "重点关注数据库迁移和缓存策略"
    ]
  }
}
```

**步骤 1 输出**（需求提取）:
```json
{
  "project_type": "Web-Application",
  "business_goals": ["云迁移", "成本优化"],
  "functional_requirements": ["电商平台", "订单处理"],
  "non_functional_requirements": {
    "availability": "99.9%",
    "rto": "< 4h"
  },
  "case_study_reference": {
    "is_referenced": true,
    "similarity_score": 85,
    "suggested_architecture": "Web 三层架构",
    "suggested_services": ["EC2 ASG", "RDS", "ALB"]
  }
}
```

**后续步骤**:
- 步骤 2: 使用案例中的架构图或生成相似架构图
- 步骤 3: 基于案例的服务组合进行决策（减少分析时间）
- 步骤 4: 生成针对新项目的定制化设计文档
- 步骤 5: 验证设计的完整性和合规性

**优势**:
- 减少 50% 的架构设计时间
- 基于验证过的最佳实践规避风险
- 更准确的成本预算和时间规划

---

## 参考资料

详细的架构模式和检查清单请参考：

- **架构模式库**: `references/architecture_patterns.md`
- **WAF 检查清单**: `references/waf_checklist.md`

---

## 重要提示

1. **严格遵循 5 步流程**: 不可跳过或合并步骤
   - 步骤 0: 案例学习文件识别（可选但推荐）
   - 步骤 1: Material Parser（需求清洗）
   - 步骤 2: Architecture Diagram Generation（架构图）
   - 步骤 3: Architecture Decisioning（架构决策）
   - 步骤 4: Design Writer（文档生成）
   - 步骤 5: Design Reviewer（质量审核）

2. **主动追问**: 发现缺失的 P0 信息必须追问
   - RTO/RPO、可用性要求、流量估算、AWS 区域

3. **案例参考**: 优先识别和参考相关案例
   - 相似案例可加速决策 50%
   - 吸取经验教训规避风险
   - 基于案例的成本数据进行预算规划

4. **架构图验证**: 架构图与设计文档必须一致
   - 服务完整性检查
   - Multi-AZ 部署检查
   - 连接关系有效性检查
   - 如果检查失败，返回步骤 1 重新分析

5. **WAF 检查是强制的**: 不可跳过任何支柱的评估
   - 特别注意 AI/ML 和大数据项目的特殊要求

6. **防止过度设计**: 优先选择最简单可满足需求的方案
   - 无需求不上 EKS、Service Mesh、Multi-Region

7. **记录所有决策理由**: 每个技术选择都要有 Why 和 Trade-off
   - 包括架构模式选择、服务选型、配置决策

8. **明确标注假设**: 所有基于假设的内容必须标注
   - 特别是在信息不足的情况下

9. **架构图一致性**: 确保所有设计都有对应的可视化表示
   - 用户提供的图 → 验证和标注
   - 自动生成的图 → MCP Server 集成
   - 降级方案 → 纯文本描述