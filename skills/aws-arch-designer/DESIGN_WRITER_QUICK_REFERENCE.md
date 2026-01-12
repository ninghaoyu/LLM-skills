# Design Writer 快速参考指南

## 🎯 核心要求

### 必须做的事

✅ **生成 Markdown 文件**
- 文件名: `{PROJECT_NAME}_架构设计说明书_v1.0.md`
- 例如: `电商平台_架构设计说明书_v1.0.md`

✅ **使用模板**
- 基础: `templates/design_doc_template.md`
- 严格遵循所有 11 个章节顺序
- 填充所有 40+ 个占位符

✅ **完整的 11 个章节**
```
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
```

✅ **每个设计决策包含**
- 设计选择的具体内容
- **选择理由 (Why)** - 为什么选这个
- **权衡 (Trade-off)** - 优势 vs 劣势
- 【假设】或【待确认】标注

### 禁止做的事

❌ **不要仅输出文本**
- 必须生成实际的 `.md` 文件

❌ **不要改变模板结构**
- 不要跳过章节
- 不要改变章节顺序
- 不要合并章节

❌ **不要留下占位符**
- 检查: 没有 `{PLACEHOLDER}` 残留
- 所有 40+ 个占位符都要填充

❌ **不要引入新需求**
- 只用步骤 1 中出现过的需求
- 不要自行添加 AWS 服务或配置

---

## 📋 占位符速查表

### 基本信息
- `{PROJECT_NAME}` ← 项目名称（步骤 1）
- `{DATE}` ← 当前日期（系统）

### 背景和目标（来自步骤 1）
- `{PROJECT_BACKGROUND}` - 项目背景
- `{BUSINESS_GOALS}` - 业务目标
- `{SUCCESS_CRITERIA}` - 成功标准

### 设计原则（来自步骤 3 WAF）
- `{OPERATIONAL_EXCELLENCE_PRINCIPLE}` - 卓越运营
- `{SECURITY_PRINCIPLE}` - 安全性
- `{RELIABILITY_PRINCIPLE}` - 可靠性
- `{PERFORMANCE_PRINCIPLE}` - 性能效率
- `{COST_PRINCIPLE}` - 成本优化
- `{SUSTAINABILITY_PRINCIPLE}` - 可持续性

### 架构概述（来自步骤 2, 3）
- `{ARCHITECTURE_STYLE}` - 架构模式
- `{CORE_COMPONENTS}` - 核心组件
- `{ARCHITECTURE_DIAGRAM_DESCRIPTION}` - 架构图描述

### 网络层（来自步骤 3）
- `{VPC_DESIGN}` - VPC 设计
- `{SUBNET_PLANNING}` - 子网规划
- `{ROUTING_AND_GATEWAYS}` - 路由和网关

### 计算层（来自步骤 3）
- `{COMPUTE_SERVICE_CHOICE}` - 计算服务
- `{COMPUTE_WHY}` - 选择理由
- `{COMPUTE_PROS}` - 优势
- `{COMPUTE_CONS}` - 劣势
- `{COMPUTE_ALTERNATIVES}` - 替代方案
- `{SCALING_STRATEGY}` - 扩展策略

### 数据库和存储（来自步骤 3）
- `{DATABASE_CHOICE}` - 数据库服务
- `{DATABASE_WHY}` - 选择理由
- `{DATABASE_PROS}` - 优势
- `{DATABASE_CONS}` - 劣势
- `{DATABASE_ALTERNATIVES}` - 替代方案
- `{S3_DESIGN}` - S3 配置
- `{BACKUP_STRATEGY}` - 备份策略

### 安全合规（来自步骤 3, 1）
- `{IAM_DESIGN}` - IAM 设计
- `{NETWORK_SECURITY}` - 网络安全
- `{ENCRYPTION_IN_TRANSIT}` - 传输加密
- `{ENCRYPTION_AT_REST}` - 静态加密
- `{COMPLIANCE}` - 合规性

### 高可用和灾备（来自步骤 3, 1）
- `{MULTI_AZ_DEPLOYMENT}` - Multi-AZ 部署
- `{RTO}` - 恢复时间目标
- `{RPO}` - 恢复点目标
- `{DISASTER_RECOVERY}` - 灾备方案

### 运维监控（来自步骤 3）
- `{LOG_AGGREGATION}` - 日志聚合
- `{MONITORING_ALERTING}` - 监控告警
- `{AUTOMATION}` - 自动化运维

### 成本分析（来自步骤 3）
- `{COST_ESTIMATION}` - 成本估算
- `{SCALABILITY_ANALYSIS}` - 扩展性分析
- `{COST_OPTIMIZATION}` - 成本优化

### 风险和假设（来自步骤 1, 3）
- `{TECHNICAL_RISKS}` - 技术风险
- `{ASSUMPTIONS}` - 假设列表
- `{OPEN_QUESTIONS}` - 待确认问题
- `{SERVICE_LIST}` - 服务清单

---

## 📝 章节内容模板

### 标准格式示例

```markdown
## 5. 计算层设计

### 5.1 计算服务选择

选择 **Amazon EC2 Auto Scaling Group** 作为计算层的主要计算服务。

**选择理由 (Why)**:
- 应用基于 Java Spring Boot，EC2 提供最小迁移成本
- 需要对操作系统级别的完整控制，支持自定义部署
- 团队已有 EC2 运维经验，学习曲线低

**权衡 (Trade-off)**:
- ✅ 优势:
  - 灵活性高，支持任意操作系统和中间件定制
  - 性价比相对较好，按实际需求扩展
  - Auto Scaling 支持自动负载均衡
- ❌ 劣势:
  - 需要维护操作系统补丁和安全更新
  - 相比 Lambda，部署和管理复杂度更高
  - 即使无流量也需要保持最小实例
- 💡 替代方案:
  - ECS Fargate: 若希望容器化但减少基础设施管理，可考虑升级
  - Lambda: 若应用改造为无状态微服务，成本更优

### 5.2 扩展策略

{SCALING_STRATEGY}

【假设】假设应用无状态或使用分布式会话管理，支持水平扩展
```

---

## ✅ 验证清单

生成文件后，检查以下项目：

### 文件检查
- [ ] 文件名正确: `{PROJECT_NAME}_架构设计说明书_v1.0.md`
- [ ] 文件格式: Markdown (`.md`)
- [ ] 文件可以打开和查看

### 内容完整性
- [ ] 有 11 个主要章节（##）
- [ ] 没有 `{PLACEHOLDER}` 字符残留
- [ ] 所有占位符都已填充

### 结构检查
```bash
# 检查章节数
grep "^## [0-9]" 文件.md | wc -l
# 应该返回 11

# 检查占位符残留
grep "{[A-Z_]*}" 文件.md
# 应该返回空
```

### 内容质量
- [ ] 每个设计决策都有 Why 和 Trade-off
- [ ] 所有假设都标注了【假设】或【待确认】
- [ ] 中文表述清晰，没有语法错误
- [ ] Markdown 格式正确（## ### ``` | 等）

---

## 🔍 常见问题

### Q: 如果某个占位符找不到数据怎么办？
**A**:
```
【待确认】此部分信息未在需求中明确，建议与客户确认...
```

或者在文档末尾的"待确认事项"中添加问题。

### Q: 可以改变章节顺序吗？
**A**: **不可以**。必须严格按照以下顺序：
1. 设计背景 → 2. 设计原则 → 3. 总体架构 → 4. 网络 → 5. 计算 → 6. 存储 → 7. 安全 → 8. 高可用 → 9. 运维 → 10. 成本 → 11. 风险

### Q: 可以删除某些章节吗？
**A**: **不可以**。所有 11 个章节必须包含，即使内容很少也要有该章节。

### Q: 文件保存到哪里？
**A**: 通常保存到项目根目录或用户指定的目录。文件名必须是 `{PROJECT_NAME}_架构设计说明书_v1.0.md`。

### Q: Markdown 格式有要求吗？
**A**: 是的，参考本指南的"章节内容模板"部分：
- 一级标题: `## 数字. 标题`
- 二级标题: `### 数字.数字 标题`
- 列表: `-` 或 `1.`
- 代码块: ``` 三引号
- 表格: Markdown 表格格式

---

## 📚 相关文件

- `templates/design_doc_template.md` - 完整的 Markdown 模板
- `SKILL.md` - 步骤 4 Design Writer 的完整实现指导
- `DESIGN_WRITER_FIX.md` - 问题根因和解决方案详细说明

---

## 🚀 使用流程

1. **准备数据**
   - 步骤 1: 提取的需求数据 ✓
   - 步骤 2: 架构图描述 ✓
   - 步骤 3: 架构决策和 WAF 评估 ✓

2. **生成文档**
   - 打开模板: `templates/design_doc_template.md`
   - 填充占位符: 根据上面的占位符速查表
   - 生成 Markdown 文件

3. **验证输出**
   - 使用上面的验证清单
   - 检查文件格式和内容完整性
   - 确认没有占位符残留

4. **交付**
   - 文件名: `{PROJECT_NAME}_架构设计说明书_v1.0.md`
   - 格式: Markdown (.md)
   - 内容: 完整的 11 个章节，所有占位符已填充

---

**最后更新**: 2026-01-12
**相关提交**: 26bcd77, d8f5ef5
