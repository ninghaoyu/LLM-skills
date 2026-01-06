# AWS 架构模式库

本文档包含各类 AWS 架构模式的详细信息。

## 目录

1. [传统应用架构](#传统应用架构)
2. [AI/ML 架构](#aiml-架构)
3. [大数据架构](#大数据架构)

---

## 传统应用架构

### Web 三层架构

**核心服务**: ALB + EC2 ASG + RDS Multi-AZ

**适用场景**: 传统 Web 应用、中等并发

**典型流程**:
```
用户 → Route 53 → CloudFront (可选) → ALB →
EC2 Auto Scaling Group (应用层) →
ElastiCache (可选缓存) → RDS Multi-AZ (数据层)
```

**关键决策**:
- EC2 实例类型: t3 (通用) vs c5 (计算优化) vs r5 (内存优化)
- RDS vs Aurora: 成本 vs 性能
- 缓存策略: ElastiCache Redis vs Memcached

**WAF 合规**:
- 卓越运营: CloudWatch + Systems Manager
- 安全性: IAM + Security Groups + KMS
- 可靠性: Multi-AZ + Auto Scaling
- 性能: ElastiCache + CloudFront
- 成本: Auto Scaling + RI
- 可持续性: Auto Scaling 优化资源利用率

---

## AI/ML 架构

### GenAI 应用架构

**核心服务**: Amazon Bedrock + Lambda + API Gateway + DynamoDB + S3

**适用场景**: 聊天机器人、内容生成、文档摘要、代码辅助

**典型流程**:
```
用户请求 → API Gateway → Lambda (业务逻辑) →
Bedrock (LLM 推理) → DynamoDB (会话存储) →
S3 (文档/知识库) → 用户响应
```

**关键决策**:
- **模型选择**:
  - Claude 3.5 Sonnet: 推理能力强、多模态、$0.003/1K input tokens
  - Llama 3.1: 开源、成本低、$0.00065/1K input tokens
  - Titan Text: AWS 原生、低成本、$0.0002/1K input tokens

- **成本控制**:
  - 设置单次请求 Token 上限 (如 4000 tokens)
  - 使用 Prompt 缓存减少重复调用
  - 根据任务复杂度选择模型

- **上下文管理**:
  - DynamoDB: 会话历史、用户偏好
  - S3: 长期存储、文档归档

**AI 特有 WAF 检查**:
- AI Cost: Token 限制、缓存策略
- AI Performance: 推理延迟 <500ms
- AI Security: Prompt Injection 防护、输入验证
- AI Reliability: 降级策略、幻觉检测

---

### RAG 架构

**核心服务**: Bedrock Knowledge Bases + OpenSearch Serverless + S3

**适用场景**: 企业知识库问答、文档检索、客服助手

**典型流程**:
```
文档上传 → S3 → Bedrock Knowledge Base (自动向量化) →
OpenSearch Serverless (向量存储) →
用户查询 → 向量检索 → 相关文档 → Bedrock (生成答案)
```

**关键决策**:
- **向量数据库选择**:
  - OpenSearch Serverless: 成本优化、无需运维、$0.24/OCU-hour
  - Kendra: 开箱即用、企业级搜索、$810/月起
  - Aurora pgvector: 结构化+向量混合查询

- **Embedding 模型**:
  - Titan Embeddings G1: $0.0001/1K tokens
  - Cohere Embed: 多语言支持

- **检索策略**:
  - Top-K: 返回最相关的 K 个文档 (如 K=5)
  - 相似度阈值: 过滤低相关性结果 (如 >0.7)

**成本估算**:
- OpenSearch Serverless: 2 OCU × $0.24/hour × 730 hours = $350/月
- Bedrock KB 向量化: $0.0001/1K tokens
- Bedrock 推理: Claude 3.5 Haiku $0.0008/1K input + $0.0016/1K output

---

### AI Agentic 系统架构

**核心服务**: Bedrock Agents + Lambda (Tools) + Step Functions + DynamoDB + EventBridge

**适用场景**: 自主任务执行、多步骤工作流、API 编排

**架构组件**:
- **Agent Orchestrator**: Bedrock Agents (任务规划、推理)
- **Action Groups**: Lambda Functions (工具调用)
- **Memory**: DynamoDB (会话状态、历史记录)
- **Workflow**: Step Functions (复杂多步骤编排)
- **Event-Driven**: EventBridge (异步任务触发)

**典型流程**:
```
用户意图 → Bedrock Agent (规划) →
选择 Action Group → Lambda (执行工具) →
外部 API / 数据库查询 →
Agent (综合结果) → 用户响应
```

**关键决策**:
- **Agent vs Lambda 编排**: 任务复杂度、动态性
- **工具设计**: RESTful API / SDK 封装
- **状态管理**: DynamoDB TTL 策略
- **错误处理**: 重试机制、降级策略

**示例 Action Group**:
```python
# Lambda Function - 查询天气工具
def lambda_handler(event, context):
    city = event['parameters']['city']
    weather_data = get_weather_api(city)
    return {
        'response': {
            'temperature': weather_data['temp'],
            'condition': weather_data['condition']
        }
    }
```

---

## 大数据架构

### 批量数据处理平台

**核心服务**: S3 + AWS Glue + Athena / Redshift

**适用场景**: 离线数据分析、ETL、BI 报表

**数据规模**: TB - PB 级

**典型流程**:
```
数据源 → S3 (Data Lake) → Glue ETL →
Athena (即席查询) / Redshift (数据仓库) → QuickSight (BI)
```

**关键决策**:
- **Athena vs Redshift**:
  - Athena: 即席查询、按查询付费、$5/TB扫描
  - Redshift: 频繁查询、预留实例、$0.25/hour起

- **Glue vs EMR**:
  - Glue: Serverless、简单 ETL、$0.44/DPU-hour
  - EMR: 复杂逻辑、Spark/Hadoop、更灵活

- **S3 分区策略**:
  - 按日期: `year=2024/month=01/day=15/`
  - 查询性能优化: 减少扫描数据量

**数据格式**:
- Parquet: 列式存储、压缩率高、查询性能优
- ORC: 类似 Parquet，Hive 生态
- CSV/JSON: 原始格式，易读但性能差

**成本优化**:
- S3 Intelligent-Tiering: 自动迁移到低成本存储
- Glue Job Bookmark: 避免重复处理
- Athena 分区: 减少扫描数据量

---

### 实时数据处理平台

**核心服务**: Kinesis Data Streams + Lambda + DynamoDB

**适用场景**: IoT 数据、日志分析、实时监控、金融交易

**数据规模**: 百万级 TPS

**处理延迟**: 毫秒 - 秒级

**典型流程**:
```
数据源 → Kinesis Data Streams →
Lambda (实时处理) / Kinesis Data Analytics (流分析) →
DynamoDB (存储) / S3 (归档) / CloudWatch (监控)
```

**关键决策**:
- **Kinesis vs MSK (Kafka)**:
  - Kinesis: 托管、AWS 集成、简单、$0.015/shard-hour
  - MSK: Kafka 生态、高吞吐、$0.21/hour起

- **Lambda vs Flink (KDA)**:
  - Lambda: 简单转换、事件驱动、$0.20/1M请求
  - Flink: 复杂窗口、状态计算、$0.11/KPU-hour

- **数据保留策略**:
  - Kinesis: 1-365 天
  - 成本 vs 合规要求

**Shard 容量规划**:
- 1 Shard = 1 MB/s 写入 或 2 MB/s 读取
- 示例: 100 MB/s 写入 → 100 Shards

**成本估算**:
- Kinesis: 10 Shards × $0.015/hour × 730 hours = $109/月
- Lambda: 1000 万次 × $0.20/1M = $2/月
- DynamoDB: 按需计费 或 预留容量

---

### 数据湖架构

**核心服务**: S3 + Lake Formation + Glue Catalog + Athena + Redshift Spectrum

**适用场景**: 多源异构数据、数据科学、ML 训练

**数据规模**: PB - EB 级

**架构层次**:
1. **Raw Zone (S3)**: 原始数据
   - 格式: 任意 (JSON, CSV, Parquet, etc.)
   - 保留策略: 根据合规要求

2. **Curated Zone (S3 + Glue)**: 清洗后数据
   - 格式: Parquet (列式存储)
   - 分区: 按日期/业务维度
   - 数据质量: Glue Data Quality

3. **Analytics Zone (Athena/Redshift)**: 分析层
   - 即席查询: Athena
   - 复杂查询: Redshift Spectrum

**关键决策**:
- **数据分区策略**: year/month/day
- **数据格式**: Parquet / ORC (列式存储优化查询)
- **访问控制**: Lake Formation 细粒度权限

**Lake Formation 优势**:
- 集中式权限管理
- 列级别访问控制
- 数据目录管理

**成本估算**:
- S3 存储: $0.023/GB-month (Standard)
- Athena 查询: $5/TB 扫描
- Lake Formation: 免费
