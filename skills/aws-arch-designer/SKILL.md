---
name: aws-arch-designer
description: AWS 架构设计说明书生成器。将零散的客户材料（会议记录、需求列表、代码片段等）转化为结构化、符合 AWS Best Practice 的《架构设计说明书》。支持 Web 应用、AI/ML（GenAI、RAG、Agentic）、大数据（批处理、实时流、数据湖）等多种架构类型。使用场景：(1) 客户提供零散需求材料需要整理；(2) 需要进行 AWS 架构设计；(3) 需要生成标准化的架构设计文档；(4) 需要基于 AWS Well-Architected Framework 进行架构评估；(5) AI/ML 项目架构设计；(6) 大数据平台架构设计。
---

# AWS 架构设计说明书生成器

将零散的客户材料自动转化为结构化、可审计、符合 AWS Best Practice 的《架构设计说明书》。

## 核心能力

- **多模态材料解析**: 直接处理 Word、Excel、PDF、Markdown、图片等任意格式材料
- **批量上传支持**: 支持用户将材料集中在一个目录，批量扫描上传
- **智能追问**: 自动识别缺失信息并主动追问（P0 关键信息）
- **架构决策**: 基于 AWS Well-Architected Framework 进行服务选型
- **多场景支持**: Web 应用、AI/ML、大数据、SaaS、混合云
- **标准化输出**: 生成完整的架构设计说明书

## 工作流程

此 Skill 遵循严格的 **6 步流程**，**不可跳过或合并**：

### 步骤 0: 案例学习文件识别与分析（可选但推荐）

**功能**: 自动识别和分析案例学习文件（多模态直接处理）

**何时触发**:
- 用户上传包含"案例"、"case study"、"项目背景"、"痛点"、"解决方案"等关键词的文档
- 无需脚本检测，LLM 直接理解

**支持的案例文件格式**（任意格式）:
- 📄 Word (docx)、PDF
- 🖼️ 包含架构图的图片（PNG/JPG）
- 📊 Excel（包含项目数据、成本预算表）
- 📝 Markdown 或纯文本

**执行任务（LLM 多模态直接处理）:**

1. **自动检测案例文件**（无需脚本）:
   LLM 理解文件内容，识别是否为案例学习文件
   - 文件名模式识别（case study、案例、迁移方案等）
   - 内容关键词识别（背景、痛点、解决方案、收益等）
   - 自动判定文件是否为案例学习文件

2. **结构化信息提取**（多模态理解）:
   从任意格式的案例文件中提取：
   - **项目背景**: 行业、公司规模、现状基础设施
   - **痛点分析**: 问题描述、影响、严重程度
   - **AWS 解决方案**: 服务组合、架构模式、配置
   - **关键指标**: 可用性、性能、流量、数据量
   - **预期收益**: 成本节省、性能提升、业务影响
   - **经验教训**: 关键经验和最佳实践
   - **架构图**: 理解文件中的架构图（PDF 中的图片、独立图片文件等）

3. **与新项目进行相关性匹配**（LLM 理解能力）:
   计算相关性分数（0-100）：
   - 行业相似性 (30 分)
   - 公司规模相似性 (20 分)
   - 痛点相似性 (30 分)
   - 功能需求相似性 (20 分)

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
    "company_scale": "公司规模",
    "source_file": "电商平台迁移案例.pdf"
  },
  "pain_points": [...],
  "aws_solution": {...},
  "key_metrics": {...},
  "expected_benefits": {...},
  "lessons_learned": [...],
  "architecture_diagram": {
    "detected": true,
    "description": "架构图描述..."
  },
  "match_with_new_project": {
    "relevance_score": 85,
    "relevance_level": "high",
    "reusable_services": [...],
    "recommendations": [...]
  }
}
```

**关键原则**:
- ✅ 多模态直接理解，无需脚本
- ✅ 支持任意格式文件（Word/PDF/图片/Excel）
- ✅ 相似案例可加速架构决策
- ✅ 从案例中提取验证过的最佳实践
- ✅ 吸取案例的经验教训规避风险
- ❌ 不要盲目复制，需要考虑新项目的特殊约束

---

### 步骤 1: Material Parser (多模态材料解析)

**目标**: 通过多模态模型从用户提交的任意格式材料中提取结构化需求信息

**支持的输入材料格式（无需预处理脚本，LLM 直接处理）:**

**文本类**:
- 会议记录（散乱的讨论要点）
- 需求列表（箭头式要点、编号列表）
- 代码片段（推断技术栈）
- Markdown 和纯文本

**文档类**:
- Word (docx): 提取文本、表格、嵌入的图片和架构图
- Excel (xlsx): 提取数据、图表、注释（如资源清单、成本预算）
- PDF: 提取文本和图片（包括架构图）

**图片类**:
- PNG、JPEG、JPG、GIF、WebP、SVG、BMP
- 架构图、流程图、截图等

**混合形式**:
- 用户可在一个目录中放置多个不同格式的文件
- Skill 支持批量扫描上传（用户一次上传整个目录或多个文件）

**批量上传目录结构示例**:
```
/项目名称/
├── 需求说明.md                 # Markdown
├── 会议记录.txt               # 纯文本
├── 业务需求.docx              # Word 文档
├── 现有资源表.xlsx             # Excel 表格
├── 架构参考图.png              # 架构图（可选）
├── 案例_电商平台迁移.pdf       # 案例学习文件（可选）
└── 其他材料/
    ├── 流程图.jpg
    ├── 数据模型.pdf
    └── ...
```

**执行任务（LLM 多模态直接处理，无需脚本）:**

1. **扫描和理解所有文件**:
   - 📄 **Word**: 提取文本、表格、嵌入图片
   - 📊 **Excel**: 提取数据、图表、注释
   - 📕 **PDF**: 提取文本和图片（包括架构图）
   - 🖼️ **图片**: 理解架构图、流程图、截图
   - 📝 **文本**: 理解会议记录、需求说明

2. **自动检测案例学习文件**（无需脚本）:
   LLM 识别文件内容中的关键词，如果检测到：
   - 案例、case study、项目背景、现状痛点、AWS 解决方案、预期收益
   - 自动触发步骤 0 的案例分析流程

3. **提取 5 大关键要素**（多模态直接理解）:
   - **功能需求**: 从文本、图表、代码中提取业务功能
   - **非功能需求**: 从需求和注释中识别可用性、性能、延迟、扩展性、RTO/RPO
   - **合规性要求**: 从文档中识别等保、GDPR、数据本地化等
   - **预算限制**: 从 Excel 或说明中提取预算数据
   - **预估流量**: 从数据表和需求中推断 DAU、QPS、数据量、峰值倍数

4. **识别项目类型**（无需脚本函数）:
   LLM 理解全部内容后自动分类：
   - AI/ML 项目：GenAI、RAG、Agentic
   - 大数据项目：批处理、实时流、数据湖
   - 传统应用：Web、SaaS、混合云

5. **理解用户提供的架构图**（多模态能力）:
   如果用户上传了架构图（PNG/JPG/PDF 中的图片）：
   - 识别 AWS 服务图标和组件
   - 理解数据流和连接关系
   - 提取关键配置（Multi-AZ、扩展策略等）
   - 验证架构与文字需求的匹配度

6. **标注缺失信息**（无需脚本）:
   LLM 自动识别 P0 关键信息的缺失：
   - RTO/RPO、可用性要求、预估流量、AWS 区域

7. **生成追问列表**（无需脚本）:
   LLM 基于缺失的 P0 信息生成追问：
   - 提供选项或参考值（如: "RTO < 4h, RPO < 1h"）
   - 一次最多 3-5 个问题
   - 使用易于理解的语言

8. **输出结构化 JSON**:
   ```json
   {
     "input_files": ["需求说明.md", "会议记录.txt", "业务需求.docx", "现有资源表.xlsx", "架构参考图.png"],
     "project_type": "Web-Application",
     "business_goals": [...],
     "functional_requirements": [...],
     "non_functional_requirements": {...},
     "traffic_estimation": {...},
     "constraints": {...},
     "assumptions": [...],
     "open_questions": [...],
     "generated_questions_for_user": [...],
     "detected_architecture_diagram": {
       "exists": true,
       "source_file": "架构参考图.png",
       "description": "用户提供的架构图显示了 Web 三层架构..."
     },
     "detected_case_study": {
       "exists": false,
       "message": "未检测到案例学习文件"
     }
   }
   ```

**关键原则**:
- ✅ **多模态优先**: 直接使用 LLM 的多模态能力处理所有格式（无需脚本）
- ✅ **批量处理**: 支持用户一次上传多个文件或整个目录
- ✅ **无脚本依赖**: 不需要 `material_parser.py`、`case_study_analyzer.py` 等预处理脚本
- ✅ **自动检测**: 自动识别案例文件、架构图等特殊内容
- ✅ **优先提取**: 优先提取明确信息，不确定的标注为"待确认"
- ❌ **不脑补**: 不要"脑补"未明确的强约束
- ❌ **不假设**: 对于不确定信息应主动追问或标注假设

**如果有追问问题**: 向用户展示问题并等待回答，然后合并回答到结构化数据中。

---

### 步骤 2: Architecture Diagram Generation (架构图处理与验证)

**目标**: 正确处理架构图，绝不自作主张重新设计架构

**前置条件**: 步骤 1 已完成，所有 P0 信息已确认

**关键原则 - 必须严格遵守**:
- 🚫 **如果用户提供了架构图，绝对不要自行设计架构和生成架构图**
- ✅ 只能理解、验证和描述用户提供的架构图
- ✅ 只有在用户明确未提供架构图时，才能调用 MCP Server 生成新的架构图
- ✅ 基于用户的架构图进行架构设计和决策

**判断逻辑**（必须严格按以下顺序执行）:

```
检查用户是否提供了架构图
    ↓
Yes（用户提供了架构图）
    ↓
【情况 1】
┌─────────────────────────────────────────────────────────┐
│ ✅ DO: 理解、验证、描述用户的架构图                        │
│ ❌ DO NOT: 设计新的架构，生成替代的架构图                  │
│ ❌ DO NOT: 质疑用户的架构设计，除非有明确的技术错误        │
└─────────────────────────────────────────────────────────┘
    ↓
No（用户未提供架构图）
    ↓
【情况 2】
┌─────────────────────────────────────────────────────────┐
│ ✅ DO: 基于需求进行架构设计，调用 MCP Server 生成架构图    │
│ ✅ DO: 进行 WAF 和最佳实践评估                             │
└─────────────────────────────────────────────────────────┘
```

---

#### 情况 1: 用户提供了架构图（PNG/PDF/JPEG）

**执行任务**:

1. **识别架构图**:
   LLM 直接理解用户上传的架构图
   - 识别图片中的 AWS 服务图标和组件
   - 理解数据流和服务间的连接关系
   - 识别关键配置（Multi-AZ、扩展策略等）

2. **生成架构图文字描述**:
   LLM 基于用户的架构图生成 Markdown 描述
   - 清晰描述架构中的每个组件
   - 说明服务间的连接和数据流
   - 注释关键的配置和决策点
   - 用于后续的 Design Writer 阶段

3. **验证架构图与需求的匹配度**:
   进行一致性检查（**仅限验证，不做修改或建议替换**）：
   - ✅ **服务覆盖检查**: 架构中是否包含了满足功能需求的服务？
   - ✅ **非功能需求检查**: 架构是否满足可用性、性能、扩展性需求？
   - ✅ **连接有效性检查**: 服务间的连接是否合理？
   - ⚠️ **告警而非阻断**: 如果发现潜在问题，仅以**建议**的形式反馈，不强制修改

4. **输出**:
```json
{
  "diagram_source": "user_provided",
  "diagram_file": "user_architecture.png",
  "detected_services": ["ALB", "EC2", "RDS", "S3"],
  "diagram_text_description": "架构图文字描述...",
  "consistency_check": {
    "service_coverage": "✅ Pass",
    "nfr_satisfaction": "✅ Pass",
    "connection_validity": "✅ Pass",
    "warnings": [],
    "improvement_suggestions": []  // 可选改进建议，非强制
  }
}
```

**严格禁止**:
- ❌ 不要说"我会为你设计一个更好的架构"
- ❌ 不要生成替代的架构图
- ❌ 不要修改用户的架构设计
- ❌ 不要批评用户的架构选择（除非有明确的技术错误）
- ❌ 不要自作主张调用 MCP Server 生成新的架构图
- ❌ 不要忽视用户的架构而强行进行 WAF 重新评估和重新设计

**应该说的话**:
- ✅ "您的架构图显示了一个 Web 三层架构..."
- ✅ "基于您提供的架构，这些服务组合可以满足..."
- ✅ "您的架构设计考虑了 Multi-AZ 部署，这很好"
- ✅ "一个可选的改进是...（如果用户感兴趣）"

---

#### 情况 2: 用户未提供架构图

**执行任务**:

1. **构建架构蓝图**:
   LLM 基于步骤 1 的结构化需求和步骤 3 的架构决策，构建架构蓝图
   - 计算层服务（EC2、Lambda、Fargate 等）
   - 数据库服务（RDS、DynamoDB、Aurora 等）
   - 缓存服务（ElastiCache 等）
   - 存储服务（S3 等）
   - 负载均衡（ALB、NLB 等）
   - 服务间连接关系

2. **调用 MCP Server 生成架构图**:
   使用 `scripts/mcp_diagram_client.py` 与 `awslabs-aws-diagram-mcp-server` 通信
   - 传入架构蓝图
   - 返回 PNG/SVG 格式的架构图

3. **生成架构图文字描述**:
   LLM 基于自动生成的架构图生成 Markdown 描述
   - 清晰描述架构中的每个组件
   - 说明服务间的连接和数据流
   - 注释关键的配置和决策点

4. **进行一致性验证**:
   验证生成的架构是否满足之前的 WAF 评估结果
   - 检查所有关键服务是否包含
   - 检查 Multi-AZ 部署是否正确配置
   - 检查连接关系是否合理

5. **降级方案**:
   如果 MCP Server 不可用，使用纯文本描述架构而不强制生成图片

**输出**:
```json
{
  "diagram_source": "auto_generated",
  "diagram_file": "/tmp/architecture.png",
  "diagram_format": "PNG",
  "services": [...],
  "connections": [...],
  "diagram_text_description": "架构图文字描述...",
  "consistency_check": {
    "waf_alignment": "✅ Pass",
    "service_completeness": "✅ Pass",
    "connection_validity": "✅ Pass",
    "issues": []
  }
}
```

---

**关键原则 - 必须遵守**:
- ✅ 用户提供架构图 → 尊重、验证、描述
- ✅ 用户未提供架构图 → 进行架构设计、生成架构图
- ✅ 架构图和设计文档必须保持一致
- ❌ 绝对不要自作主张地替换用户的架构图
- ❌ 绝对不要在用户已提供架构图的情况下自行重新设计

---

### 步骤 3: Architecture Decisioning (架构决策)

**目标**: 基于结构化需求和用户提供的架构图（或自行设计的架构），进行服务选型和 WAF 评估

**前置条件**: 步骤 1 已完成，且所有 P0 问题已得到回答，步骤 2 已处理架构图

**重要说明**:
- 如果用户提供了架构图 → 基于用户的架构图进行决策和 WAF 评估
- 如果用户未提供架构图 → 基于需求自行设计架构并进行评估

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

**目标**: 按固定模板生成架构设计说明书并输出为 Markdown 文件

**前置条件**: 步骤 3 已完成，所有服务选型和 WAF 评估已完成

**CRITICAL - 必须执行**:
- ✅ 使用 `templates/design_doc_template.md` 作为基础模板
- ✅ 填充所有占位符（`{PLACEHOLDER_NAME}`）
- ✅ **生成完整的 Markdown 文件**（不仅仅是文本响应）
- ✅ 文件命名规则: `{PROJECT_NAME}_架构设计说明书_v1.0.md`
- ✅ 将文件保存到项目目录或返回给用户下载

**执行任务**:

#### 4.1 模板映射

基于步骤 1、2、3 的输出结果，填充以下占位符：

| 占位符 | 数据源 | 填充内容 |
|-------|--------|---------|
| `{PROJECT_NAME}` | 步骤 1 | 项目名称 |
| `{DATE}` | 系统 | 当前日期 |
| `{PROJECT_BACKGROUND}` | 步骤 1 | 项目背景和业务需求 |
| `{BUSINESS_GOALS}` | 步骤 1 | 业务目标列表 |
| `{SUCCESS_CRITERIA}` | 步骤 1 | 成功标准和关键指标 |
| `{OPERATIONAL_EXCELLENCE_PRINCIPLE}` | 步骤 3 WAF | 卓越运营设计说明 |
| `{SECURITY_PRINCIPLE}` | 步骤 3 WAF | 安全性设计说明 |
| `{RELIABILITY_PRINCIPLE}` | 步骤 3 WAF | 可靠性设计说明 |
| `{PERFORMANCE_PRINCIPLE}` | 步骤 3 WAF | 性能效率设计说明 |
| `{COST_PRINCIPLE}` | 步骤 3 WAF | 成本优化设计说明 |
| `{SUSTAINABILITY_PRINCIPLE}` | 步骤 3 WAF | 可持续性设计说明 |
| `{PROJECT_SPECIFIC_PRINCIPLES}` | 步骤 1 | 项目特定的设计原则 |
| `{ARCHITECTURE_STYLE}` | 步骤 3 | 选择的架构模式（如 Web 三层架构、RAG 架构） |
| `{CORE_COMPONENTS}` | 步骤 3 | 核心 AWS 服务及其作用 |
| `{ARCHITECTURE_DIAGRAM_DESCRIPTION}` | 步骤 2 | 架构图的文字描述 |
| `{VPC_DESIGN}` | 步骤 3 | VPC 设计和配置 |
| `{SUBNET_PLANNING}` | 步骤 3 | 子网规划（公有、私有、数据库层） |
| `{ROUTING_AND_GATEWAYS}` | 步骤 3 | 路由表和网关配置 |
| `{HYBRID_CLOUD_CONNECTION}` | 步骤 1 | 混合云连接方案（若适用） |
| `{COMPUTE_SERVICE_CHOICE}` | 步骤 3 | 选择的计算服务及原因 |
| `{COMPUTE_WHY}` | 步骤 3 | 计算服务选择理由 |
| `{COMPUTE_PROS}` | 步骤 3 | 选择方案的优势 |
| `{COMPUTE_CONS}` | 步骤 3 | 选择方案的劣势 |
| `{COMPUTE_ALTERNATIVES}` | 步骤 3 | 替代方案及升级路径 |
| `{SCALING_STRATEGY}` | 步骤 3 | Auto Scaling、负载均衡等扩展策略 |
| `{CONTAINER_FUNCTION_DESIGN}` | 步骤 3 | 容器或函数设计（若适用） |
| `{DATABASE_CHOICE}` | 步骤 3 | 选择的数据库服务 |
| `{DATABASE_WHY}` | 步骤 3 | 数据库选择理由 |
| `{DATABASE_PROS}` | 步骤 3 | 数据库方案的优势 |
| `{DATABASE_CONS}` | 步骤 3 | 数据库方案的劣势 |
| `{DATABASE_ALTERNATIVES}` | 步骤 3 | 替代数据库方案 |
| `{S3_DESIGN}` | 步骤 3 | S3 配置、分区策略、生命周期 |
| `{BACKUP_STRATEGY}` | 步骤 3 | 备份策略和恢复流程 |
| `{IAM_DESIGN}` | 步骤 3 | IAM 角色和权限策略 |
| `{NETWORK_SECURITY}` | 步骤 3 | Security Group、NACL、WAF 配置 |
| `{ENCRYPTION_IN_TRANSIT}` | 步骤 3 | TLS、VPN 等传输加密配置 |
| `{ENCRYPTION_AT_REST}` | 步骤 3 | KMS、服务端加密等静态加密配置 |
| `{COMPLIANCE}` | 步骤 1 | 合规性要求（等保、GDPR 等）及实现方案 |
| `{MULTI_AZ_DEPLOYMENT}` | 步骤 3 | Multi-AZ 部署说明 |
| `{RTO}` | 步骤 1 | 恢复时间目标 |
| `{RPO}` | 步骤 1 | 恢复点目标 |
| `{DISASTER_RECOVERY}` | 步骤 3 | 灾备方案（备份、故障转移、跨 Region） |
| `{LOG_AGGREGATION}` | 步骤 3 | CloudWatch Logs 和日志保留策略 |
| `{MONITORING_ALERTING}` | 步骤 3 | CloudWatch Alarms、SNS 通知配置 |
| `{AUTOMATION}` | 步骤 3 | Systems Manager、EventBridge、Lambda 自动化 |
| `{COST_ESTIMATION}` | 步骤 3 | 成本估算表（月度/年度预估） |
| `{SCALABILITY_ANALYSIS}` | 步骤 3 | 扩展性分析和成长规划 |
| `{COST_OPTIMIZATION}` | 步骤 3 | RI、Savings Plans、Spot、Auto Scaling 优化 |
| `{TECHNICAL_RISKS}` | 步骤 1 + 步骤 3 | 技术风险和缓解策略 |
| `{ASSUMPTIONS}` | 步骤 1 | 基于假设的内容清单 |
| `{OPEN_QUESTIONS}` | 步骤 1 | 待客户确认的问题 |
| `{SERVICE_LIST}` | 步骤 3 | 完整的 AWS 服务清单和配置参数 |

#### 4.2 章节要求（严格按顺序，不可合并或跳过）

每个章节必须包含：
- **设计选择的具体内容** - 清晰说明选了什么服务和配置
- **选择理由（Why）** - 为什么选择这个方案而不是其他
- **权衡说明（Trade-off）** - 这个方案的优势和劣势
- **基于假设的内容标注** - 若信息不足，明确标注 `【假设】` 或 `【待确认】`

**11 个章节清单**:
1. ✅ 设计背景与目标
2. ✅ 架构设计原则
3. ✅ 总体架构概述
4. ✅ 网络架构设计
5. ✅ 计算层设计
6. ✅ 存储与数据库设计
7. ✅ 安全与权限设计
8. ✅ 高可用与灾备设计
9. ✅ 运维与监控设计
10. ✅ 成本与扩展性分析
11. ✅ 风险、假设与待确认事项

#### 4.3 文风和格式要求

**文风**:
- 技术说明书风格，避免营销语言
- 适合直接交付客户或进入方案评审
- 客观中立，不做过度承诺

**格式**:
- 使用 Markdown 语法
- 章节编号清晰（## 表示一级章节，### 表示二级章节）
- 代码块使用 ```json、```yaml 标注
- 表格使用 Markdown 表格格式
- 列表使用 - 或数字编号

**示例章节格式**:
```markdown
## 5. 计算层设计

### 5.1 计算服务选择

选择 **Amazon EC2 Auto Scaling Group** 作为计算层。

**选择理由 (Why)**:
- 现有应用基于 Spring Boot，迁移成本最低
- 需要完整的操作系统控制，定制化部署
- 团队已有 EC2 运维经验

**权衡 (Trade-off)**:
- ✅ 优势:
  - 灵活性高，支持任意定制
  - 成本相对较低（与容器化相比）
  - Auto Scaling 支持自动扩展
- ❌ 劣势:
  - 需要维护操作系统和补丁
  - 对比 Lambda，冷启动更慢
- 💡 替代方案:
  - ECS Fargate: 若想减少 OS 管理工作，可考虑容器化
  - Lambda: 若应用改造为无状态微服务
```

#### 4.4 禁止事项

- ❌ 不要引入步骤 1 中未出现的强约束
- ❌ 不要使用 AWS China 不可用的服务（若 region = China）
- ❌ 不要过度设计（无需求不上 EKS / Multi-Region）
- ❌ **不要仅输出文本响应，必须生成实际的 Markdown 文件**
- ❌ 不要偏离模板结构，改变章节顺序或合并章节

#### 4.5 生成和输出文件

**文件命名规则**:
```
{PROJECT_NAME}_架构设计说明书_v1.0.md

示例:
- 电商平台_架构设计说明书_v1.0.md
- 企业知识库_架构设计说明书_v1.0.md
- AI聊天机器人_架构设计说明书_v1.0.md
```

**输出方式**:
1. 生成完整的 Markdown 文件内容
2. 保存为文件（若有文件系统访问权限）
3. 或将完整的 Markdown 内容返回给用户，用户可复制保存

**验证清单**:
- [ ] 所有 11 个章节都已包含
- [ ] 所有占位符都已填充，没有 `{PLACEHOLDER}` 残留
- [ ] 每个技术选择都有 Why 和 Trade-off
- [ ] 假设和待确认事项都已明确标注
- [ ] 格式符合 Markdown 规范
- [ ] 文件名符合规则
- [ ] 中文语言使用正确

**输出**:
- 🎯 **必须输出完整的 Markdown 文件**
- 文件名: `{PROJECT_NAME}_架构设计说明书_v1.0.md`
- 格式: 严格按照 `templates/design_doc_template.md` 模板
- 内容: 填充所有占位符，11 个章节完整

#### 4.6 Design Writer Prompt 模板

当执行步骤 4 时，使用以下 Prompt 指导 LLM 生成文档：

```markdown
你是一名资深 AWS 解决方案架构师，需要基于已完成的架构决策，
生成标准化的《AWS 架构设计说明书》。

【输入数据】
- 步骤 1 提取的需求数据（项目背景、业务目标、非功能需求、流量估算、约束条件等）
- 步骤 2 生成或识别的架构图
- 步骤 3 完成的架构决策和 WAF 评估结果

【执行任务】

1. **使用模板**
   打开 `templates/design_doc_template.md` 作为基础模板

2. **填充占位符**
   根据输入数据填充所有 {PLACEHOLDER} 占位符
   - 必须逐一填充，不留空白
   - 使用数据驱动的内容，不使用虚拟或假设的数据

3. **生成完整的 Markdown 文档**
   - 严格按照 11 个章节顺序
   - 每个章节包含 Why、Trade-off、假设标注
   - 使用清晰的 Markdown 格式（##、###、```、表格、列表）

4. **输出文件**
   文件名: {PROJECT_NAME}_架构设计说明书_v1.0.md
   示例: 电商平台_架构设计说明书_v1.0.md

5. **验证清单**
   - [ ] 所有 11 个章节完整
   - [ ] 没有 {PLACEHOLDER} 残留
   - [ ] 每个决策都有 Why 和 Trade-off
   - [ ] 假设明确标注【假设】
   - [ ] Markdown 格式正确
   - [ ] 文件名符合规则

【关键原则】
- ✅ 遵循模板结构，不要改变章节顺序或合并
- ✅ 填充所有占位符，确保完整性
- ✅ 输出实际的 Markdown 文件，不仅仅是文本响应
- ✅ 技术说明书风格，避免营销语言
- ✅ 每个技术选择都要有明确的理由
- ❌ 不要跳过任何章节
- ❌ 不要引入未在步骤 1 中出现的需求
- ❌ 不要改变模板的基本结构
```

---

### 步骤 5: Design Reviewer (设计审查)

**目标**: 检查架构设计的完整性和正确性

**前置条件**: 步骤 4 已完成，设计文档已生成

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
  ],
  "user_provided_diagram": false
}
```

**步骤 2 输出**（架构图处理）:
```json
{
  "diagram_source": "auto_generated",
  "diagram_file": "/tmp/architecture.png",
  "detected_services": ["ALB", "EC2", "RDS", "S3"],
  "diagram_text_description": "基于需求生成的 Web 三层架构图..."
}
```

**步骤 3 输出**（架构决策）:
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

### 示例 1b: 用户提供了架构图的电商平台迁移

**用户输入**:
```
需求：电商平台云迁移
附件：我已经设计了一个架构，请基于我的架构进行评估和文档化
[用户上传了 architecture.png]
```

**步骤 1 输出**: （与示例 1 相同）

**步骤 2 输出**（架构图处理）:
```json
{
  "diagram_source": "user_provided",
  "diagram_file": "architecture.png",
  "detected_services": ["ALB", "EC2", "RDS", "ElastiCache", "S3"],
  "diagram_text_description": "用户提供的架构图展示了一个 Web 三层架构...",
  "consistency_check": {
    "service_coverage": "✅ Pass - 所有关键服务都已包含",
    "nfr_satisfaction": "✅ Pass - 支持 99.9% 可用性",
    "connection_validity": "✅ Pass",
    "warnings": [],
    "improvement_suggestions": [
      "可选：考虑添加 CloudFront CDN 加速静态资源"
    ]
  }
}
```

**步骤 3 输出**（基于用户架构的决策）:
```json
{
  "architecture_pattern": "Web 三层架构（基于用户提供）",
  "selected_services": {
    "compute": "EC2 Auto Scaling Group",
    "load_balancer": "Application Load Balancer",
    "database": "RDS for MySQL Multi-AZ",
    "cache": "ElastiCache Redis",
    "storage": "S3"
  },
  "decision_basis": "基于用户提供的架构图进行决策和 WAF 评估"
}
```

**最终输出**: 基于用户架构的完整设计说明书

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
  ],
  "user_provided_diagram": false
}
```

**步骤 2 输出**（架构图生成）:
```json
{
  "diagram_source": "auto_generated",
  "diagram_file": "/tmp/rag_architecture.png",
  "services": ["Bedrock KB", "OpenSearch Serverless", "Lambda", "S3"],
  "diagram_text_description": "自动生成的 RAG 架构图..."
}
```

**步骤 3 输出**（架构决策）:
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
  },
  "user_provided_diagram": false
}
```

**后续步骤**:
- 步骤 2: 基于案例中的架构图或生成相似架构图
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

1. **严格遵循 6 步流程**: 不可跳过或合并步骤
   - 步骤 0: 案例学习文件识别（可选但推荐）
   - 步骤 1: Material Parser（需求清洗）
   - 步骤 2: Architecture Diagram Generation（架构图处理与验证）
   - 步骤 3: Architecture Decisioning（架构决策）
   - 步骤 4: Design Writer（文档生成）
   - 步骤 5: Design Reviewer（质量审核）

2. **尊重用户的架构图**（CRITICAL）:
   - ✅ **如果用户提供了架构图**: 严格遵守用户的架构设计，进行验证和描述，绝不自作主张重新设计
   - ❌ **禁止行为**:
     - 不要说"我会为你设计一个更好的架构"
     - 不要生成替代的架构图
     - 不要在已有用户架构的情况下调用 MCP Server 生成新的架构图
     - 不要强行进行 WAF 重新评估和重新设计
   - ✅ **应该做的**:
     - 理解、验证、描述用户的架构图
     - 基于用户的架构进行 WAF 评估
     - 提供可选的改进建议（非强制）

3. **主动追问**: 发现缺失的 P0 信息必须追问
   - RTO/RPO、可用性要求、流量估算、AWS 区域

4. **案例参考**: 优先识别和参考相关案例
   - 相似案例可加速决策 50%
   - 吸取经验教训规避风险
   - 基于案例的成本数据进行预算规划

5. **架构图验证**: 架构图与设计文档必须一致
   - 服务完整性检查
   - Multi-AZ 部署检查
   - 连接关系有效性检查
   - 如果检查失败，返回步骤 1 重新分析

6. **WAF 检查是强制的**: 不可跳过任何支柱的评估
   - 特别注意 AI/ML 和大数据项目的特殊要求

7. **防止过度设计**: 优先选择最简单可满足需求的方案
   - 无需求不上 EKS、Service Mesh、Multi-Region

8. **记录所有决策理由**: 每个技术选择都要有 Why 和 Trade-off
   - 包括架构模式选择、服务选型、配置决策

8. **明确标注假设**: 所有基于假设的内容必须标注
   - 特别是在信息不足的情况下

9. **架构图一致性**: 确保所有设计都有对应的可视化表示
   - 用户提供的图 → 验证和标注
   - 自动生成的图 → MCP Server 集成
   - 降级方案 → 纯文本描述

---

## 脚本优化指南 - 多模态处理改进

### 核心优化原则

**原始设计的问题**:
- `material_parser.py`: 试图通过脚本处理文本和结构化提取 ❌
- `case_study_analyzer.py`: 试图通过正则和规则进行案例检测 ❌
- 这些脚本在多模态 LLM 时代**完全冗余**

**新方向**:
✅ **相信 LLM 的多模态能力直接处理所有格式** - Word、PDF、图片、Excel、文本
✅ **让 LLM 直接理解内容** - 无需预处理脚本
✅ **支持批量上传** - 用户在一个目录中放置所有材料，一次上传多个文件

### 脚本清理清单

#### ❌ 应删除的脚本（完全冗余）

1. **`scripts/material_parser.py`** - 完全不需要
   - **原因**: LLM 可以直接处理和理解任何格式的输入材料
   - **原函数用途**:
     - `parse_material()` → LLM 直接理解（无需脚本）
     - `identify_project_type()` → LLM 直接推断（无需脚本）
     - `generate_clarification_questions()` → LLM 直接生成（无需脚本）
   - **删除方法**: 直接删除整个文件

2. **`scripts/case_study_analyzer.py`** - 完全不需要
   - **原因**: LLM 多模态能力可直接理解案例文件内容
   - **原函数用途**:
     - `CaseStudyDetector.detect()` → LLM 直接识别（通过内容理解）
     - `CaseStudyExtractor` 各函数 → LLM 直接提取（无需 NLP 规则）
     - `CaseStudyMatcher.calculate_relevance()` → LLM 直接评估（无需评分算法）
   - **删除方法**: 直接删除整个文件

#### ✅ 可保留的脚本（需要改造）

1. **`scripts/diagram_generator.py`** - 保留但改造
   - **改造目标**: 不做架构图检测和验证，只支持 LLM 调用 MCP
   - **改造内容**:
     - 删除 `DiagramGenerator.detect_user_diagram()` - LLM 直接理解
     - 删除 `DiagramValidator` 类 - LLM 直接验证
     - 保留 `BlueprintBuilder` - 帮助构建结构化的架构蓝图
     - 保留与 MCP 的接口调用部分

2. **`scripts/mcp_diagram_client.py`** - 保留
   - **目的**: 与 `awslabs-aws-diagram-mcp-server` 通信
   - **保留原因**: 必须的 MCP 集成
   - **改造内容**:
     - 简化 API（移除内部检测逻辑）
     - 直接响应 LLM 的 MCP 调用请求
     - 返回生成的架构图结果

### 新架构流程

```
用户上传材料（任意格式、批量）
    ↓
LLM 多模态直接理解（无脚本）
    ├─ 理解所有格式（Word/PDF/图片/Excel/文本）
    ├─ 自动检测案例文件
    ├─ 提取 5 大关键要素
    ├─ 理解用户提供的架构图
    └─ 生成追问问题
    ↓
[如果缺少架构图]
    LLM 调用 MCP: awslabs-aws-diagram-mcp-server
    (diagram_generator.py 和 mcp_diagram_client.py 配合)
    ↓
生成完整的架构设计说明书
```

### 实施步骤

#### 第 1 步: 删除完全冗余的脚本
```bash
rm -f scripts/material_parser.py
rm -f scripts/case_study_analyzer.py
```

#### 第 2 步: 改造 diagram_generator.py
删除以下类和方法：
- `DiagramGenerator.detect_user_diagram()`
- `DiagramValidator` 整个类
- 所有与内部检测相关的代码

保留：
- `BlueprintBuilder` - LLM 调用来构建蓝图
- `DiagramDescriptionGenerator` - 生成文字描述

#### 第 3 步: 简化 mcp_diagram_client.py
- 移除内部验证逻辑
- 简化为直接调用 MCP 的瘦客户端
- 返回原始 MCP 结果

#### 第 4 步: 更新 SKILL.md 和 DEEPV.md
- ✅ 已完成（本次修改）
- 强调多模态处理
- 移除对脚本的引用

### 最终项目结构

```
skills/aws-arch-designer/
├── SKILL.md                    # 修改完成 ✅
├── DEEPV.md                    # 修改完成 ✅
├── README.md
├── SKILL_TEST_CASES.md
├── assets/
│   └── design_doc_template.md
├── references/
│   ├── architecture_patterns.md
│   └── waf_checklist.md
└── scripts/
    ├── diagram_generator.py      # 保留（改造）
    └── mcp_diagram_client.py      # 保留（保持不变或简化）

    ❌ 已删除:
    - material_parser.py
    - case_study_analyzer.py
```

### 关键改动总结

| 方面 | 原设计 | 新设计 |
|-----|--------|--------|
| **材料处理** | 脚本 → 正则匹配 | **LLM 多模态** → 直接理解 |
| **案例检测** | 脚本 → 关键词匹配 | **LLM** → 内容理解 |
| **上传方式** | 单文件处理 | **批量上传** → 支持目录和多个文件 |
| **架构图理解** | 脚本 vision API | **LLM 直接** → 多模态能力 |
| **代码行数** | ~2000 行脚本 | **~0 行脚本**（全部 LLM）+ 小型 MCP 客户端 |

### 使用建议

1. **先更新文档** ✅ (已完成 SKILL.md 和 DEEPV.md)
2. **立即删除**: `material_parser.py` 和 `case_study_analyzer.py`
3. **渐进改造**: 逐步简化 `diagram_generator.py` 和 `mcp_diagram_client.py`
4. **测试验证**: 确保 LLM 能直接处理各种材料格式
