# AWS Well-Architected Framework 检查清单

本文档包含 WAF 六大支柱的详细检查清单，以及 AI/ML 和大数据项目的特殊检查项。

## 目录

1. [WAF 六大支柱](#waf-六大支柱)
2. [AI/ML 特有检查](#aiml-特有检查)
3. [大数据特有检查](#大数据特有检查)

---

## WAF 六大支柱

### 1️⃣ 卓越运营 (Operational Excellence)

**核心问题**:
- [ ] 是否定义了运维流程和标准?
- [ ] 是否使用 IaC (Infrastructure as Code)?
- [ ] 是否配置了自动化运维工具?
- [ ] 是否建立了变更管理流程?

**检查点**:
- **日志聚合**: CloudWatch Logs
- **自动化响应**: EventBridge
- **补丁管理**: Systems Manager
- **IaC**: CloudFormation / Terraform

**最佳实践**:
- 所有基础设施使用 IaC 定义
- 集中式日志聚合到 CloudWatch 或 S3
- 自动化常规运维任务

---

### 2️⃣ 安全性 (Security)

**核心问题**:
- [ ] 是否遵循最小权限原则 (IAM)?
- [ ] 是否启用静态数据加密?
- [ ] 是否启用传输加密 (TLS)?
- [ ] 是否配置网络隔离 (VPC/Security Group)?
- [ ] 是否启用审计日志 (CloudTrail)?

**检查点**:
- **IAM 角色**: 禁止使用 Root 账户，使用细粒度权限
- **KMS 加密**: S3、RDS、EBS 静态加密
- **WAF 防护**: 公网暴露的应用
- **MFA**: 管理员账户强制 MFA
- **VPC Flow Logs**: 网络流量审计
- **CloudTrail**: 所有 API 调用审计

**最佳实践**:
- 默认拒绝，显式允许
- 定期轮换密钥和凭证
- 使用 AWS Secrets Manager 管理敏感信息

---

### 3️⃣ 可靠性 (Reliability)

**核心问题**:
- [ ] 是否实现 Multi-AZ 部署?
- [ ] 是否配置自动故障转移?
- [ ] 是否定义了 RTO/RPO?
- [ ] 是否配置了备份策略?
- [ ] 是否进行了容量规划?

**检查点**:
- **Multi-AZ**: RDS Multi-AZ / Aurora Replicas
- **Auto Scaling**: 动态调整容量
- **备份策略**: AWS Backup / Snapshot
- **健康检查**: Route 53 / ALB
- **RTO/RPO**: 明确恢复目标

**最佳实践**:
- 生产环境必须 Multi-AZ
- 定期测试灾备流程
- 监控关键指标并设置告警

---

### 4️⃣ 性能效率 (Performance Efficiency)

**核心问题**:
- [ ] 是否选择了适合工作负载的实例类型?
- [ ] 是否使用了缓存机制?
- [ ] 是否启用了 CDN (若适用)?
- [ ] 是否优化了数据库查询?

**检查点**:
- **实例类型**: 计算优化 / 内存优化 / 通用
- **缓存**: ElastiCache / DAX
- **CDN**: CloudFront
- **性能洞察**: RDS Performance Insights

**实例类型选择**:
| 工作负载 | 推荐实例 | 说明 |
|---------|---------|-----|
| Web 应用 | t3, m5 | 通用型 |
| 计算密集 | c5, c6i | 高 CPU |
| 内存密集 | r5, r6i | 高内存 |
| 机器学习 | p3, g4dn | GPU |

**最佳实践**:
- 使用缓存减少数据库负载
- 启用 CloudFront 减少延迟
- 定期审查和优化资源配置

---

### 5️⃣ 成本优化 (Cost Optimization)

**核心问题**:
- [ ] 是否使用了 Auto Scaling 避免资源浪费?
- [ ] 是否考虑了 Reserved Instance / Savings Plans?
- [ ] 是否配置了 S3 生命周期策略?
- [ ] 是否启用了成本监控 (Cost Explorer)?

**检查点**:
- **Auto Scaling**: 按需扩展
- **S3 Lifecycle**: Standard → IA → Glacier
- **Spot Instances**: 非关键工作负载
- **Cost Explorer**: 成本分析
- **Budgets**: 成本告警

**成本优化策略**:
1. **计算**:
   - RI / Savings Plans (1年/3年承诺)
   - Spot Instances (最高 90% 折扣)
   - Auto Scaling (避免过度配置)

2. **存储**:
   - S3 Intelligent-Tiering
   - 删除未使用的快照和卷
   - 压缩和去重

3. **网络**:
   - 使用 VPC Endpoints 减少数据传输费
   - CloudFront 缓存减少回源

**最佳实践**:
- 定期审查资源使用情况
- 删除未使用的资源
- 使用 Cost Anomaly Detection

---

### 6️⃣ 可持续性 (Sustainability)

**核心问题**:
- [ ] 是否选择了能效更高的实例类型 (Graviton)?
- [ ] 是否优化了资源利用率?
- [ ] 是否选择了绿色能源的 Region?

**检查点**:
- **Graviton 实例**: ARM 架构，能效更高
- **Serverless**: 按需计费，无闲置资源
- **自动关闭**: 开发/测试环境非工作时间关闭

**Graviton 实例优势**:
- 性能提升 40%
- 价格降低 20%
- 能耗降低 60%

**最佳实践**:
- 优先使用 Serverless 服务
- 开发环境使用 Lambda / Fargate
- 选择可再生能源比例高的 Region

---

## AI/ML 特有检查

### 🤖 AI Cost Optimization

**Token 成本控制**:
- [ ] 是否设置单次请求 Token 上限?
- [ ] 是否使用 Prompt 缓存减少重复调用?
- [ ] 是否根据任务选择合适的模型?

**推理成本优化**:
- [ ] SageMaker Endpoint 是否使用 Auto Scaling?
- [ ] 是否考虑 Serverless Inference (不定期流量)?
- [ ] 训练是否使用 Spot Instances?

**向量数据库成本**:
- [ ] 是否选择 OpenSearch Serverless 而非常驻集群?
- [ ] 是否配置 Index 生命周期策略?

**成本对比**:
| 模型 | Input Token 成本 | Output Token 成本 | 适用场景 |
|-----|-----------------|-------------------|---------|
| Claude 3.5 Sonnet | $0.003/1K | $0.015/1K | 复杂推理 |
| Claude 3.5 Haiku | $0.0008/1K | $0.0016/1K | 简单任务 |
| Llama 3.1 70B | $0.00065/1K | $0.00065/1K | 成本敏感 |
| Titan Text | $0.0002/1K | $0.0006/1K | 低成本 |

---

### 🤖 AI Performance

**推理延迟**:
- [ ] 是否满足业务 SLA (如 <500ms)?
- [ ] 是否使用缓存 (Redis) 减少重复推理?
- [ ] 是否配置 Provisioned Throughput (高并发)?

**模型选择**:
- [ ] 模型大小是否匹配任务复杂度 (避免大材小用)?
- [ ] 是否测试过多个模型的性能/成本比?

**批处理优化**:
- [ ] 批量推理是否使用 Batch Transform?
- [ ] 是否合并多个请求减少 API 调用?

---

### 🤖 AI Security

**数据隐私**:
- [ ] 训练数据是否加密存储 (S3 + KMS)?
- [ ] 是否使用 VPC Endpoints 避免公网传输?
- [ ] Bedrock 是否选择不记录数据的模型?

**Prompt Injection 防护**:
- [ ] 是否对用户输入进行过滤和验证?
- [ ] 是否限制 System Prompt 不被覆盖?

**模型访问控制**:
- [ ] 是否使用 IAM 细粒度控制模型调用权限?
- [ ] 是否启用 CloudTrail 审计 API 调用?

**Prompt Injection 防护示例**:
```python
def validate_input(user_input):
    # 检查危险关键词
    dangerous_keywords = ["ignore previous", "system prompt", "override"]
    if any(keyword in user_input.lower() for keyword in dangerous_keywords):
        return False, "输入包含不安全内容"

    # 长度限制
    if len(user_input) > 4000:
        return False, "输入过长"

    return True, "输入安全"
```

---

### 🤖 AI Reliability

**降级策略**:
- [ ] 当主模型不可用时，是否有备用模型?
- [ ] 是否设置超时和重试机制?

**幻觉检测**:
- [ ] 是否对 LLM 输出进行验证 (如 Guardrails)?
- [ ] 是否结合 RAG 提供事实依据?

**版本管理**:
- [ ] 模型是否版本化 (SageMaker Model Registry)?
- [ ] 是否支持 A/B 测试和回滚?

---

### 🤖 MLOps

**监控与可观测性**:
- [ ] 是否监控模型性能指标 (准确率、延迟、成本)?
- [ ] 是否配置 SageMaker Model Monitor (数据漂移检测)?
- [ ] 是否记录 Prompt/Response 用于调试?

**持续优化**:
- [ ] 是否建立模型重训练流程?
- [ ] 是否收集用户反馈优化 Prompt?

---

## 大数据特有检查

### 📊 Big Data Cost

**存储成本**:
- [ ] S3 是否配置生命周期策略 (Standard → IA → Glacier)?
- [ ] 是否使用 S3 Intelligent-Tiering 自动优化?
- [ ] 是否删除/归档过期数据?

**计算成本**:
- [ ] EMR 是否使用临时集群 (用后即删)?
- [ ] 是否使用 Spot Instances (非关键任务)?
- [ ] Redshift 是否使用 Reserved Instances / Serverless?

**数据传输成本**:
- [ ] 是否使用 VPC Endpoints 避免公网流量费?
- [ ] 跨 Region 复制是否必要?

**成本优化策略**:
- EMR 临时集群 vs 常驻集群: 节省 70%+
- Spot Instances: 最高 90% 折扣
- Redshift Serverless: 按查询计费，避免闲置成本

---

### 📊 Big Data Performance

**查询性能**:
- [ ] S3 数据是否合理分区 (按日期/地区)?
- [ ] 是否使用列式存储 (Parquet/ORC)?
- [ ] Athena 查询是否优化 (避免 SELECT *)?

**数据处理性能**:
- [ ] EMR 实例类型是否适配工作负载 (计算 vs 内存)?
- [ ] Glue Job 是否配置合理的 DPU 数量?
- [ ] Kinesis Shard 数量是否满足吞吐量?

**并发控制**:
- [ ] Redshift 并发扩展是否启用?
- [ ] Athena 查询是否限制并发数?

**查询优化示例**:
```sql
-- ❌ 差的查询 (全表扫描)
SELECT * FROM logs WHERE date = '2024-01-15';

-- ✅ 好的查询 (分区过滤)
SELECT user_id, event_type, timestamp
FROM logs
WHERE year='2024' AND month='01' AND day='15';
```

---

### 📊 Big Data Reliability

**数据一致性**:
- [ ] 是否处理重复数据 (去重逻辑)?
- [ ] 流处理是否支持 Exactly-Once 语义?

**容错机制**:
- [ ] EMR 是否配置自动恢复?
- [ ] Glue Job 是否支持 Bookmark (断点续传)?
- [ ] 是否配置死信队列 (DLQ)?

**数据质量**:
- [ ] 是否配置 Glue Data Quality 检查?
- [ ] 是否验证数据 Schema?

---

### 📊 Big Data Security

**数据加密**:
- [ ] S3 是否启用服务端加密 (SSE-S3/SSE-KMS)?
- [ ] Redshift 是否启用加密?
- [ ] Kinesis 是否启用传输加密?

**访问控制**:
- [ ] 是否使用 Lake Formation 细粒度权限?
- [ ] 是否遵循最小权限原则 (IAM)?
- [ ] 是否启用 S3 Bucket Policy 限制访问?

**数据脱敏**:
- [ ] 敏感数据是否脱敏处理?
- [ ] 是否使用 Glue DataBrew 进行数据清洗?

---

### 📊 Data Governance

**监控与告警**:
- [ ] 是否监控 ETL Job 失败率?
- [ ] 是否配置 Kinesis 数据积压告警?
- [ ] Redshift 查询性能是否监控?

**数据治理**:
- [ ] 是否建立数据目录 (Glue Catalog)?
- [ ] 是否定义数据保留策略?
- [ ] 是否记录数据血缘关系?

**自动化**:
- [ ] ETL 是否使用调度工具 (Step Functions / MWAA)?
- [ ] 是否自动化数据质量检查?
