---
name: aws-arch-designer
description: AWS 架构设计说明书生成器。将零散的客户材料（会议记录、需求列表、代码片段等）转化为结构化、符合 AWS Best Practice 的《架构设计说明书》。支持 Web 应用、AI/ML（GenAI、RAG、Agentic）、大数据（批处理、实时流、数据湖）等多种架构类型。
---

# AWS 架构设计说明书生成器

将零散的客户材料自动转化为结构化、可审计、符合 AWS Best Practice 的《架构设计说明书》。

## 核心能力

- **多模态材料解析**: 直接处理 Word、Excel、PDF、Markdown、图片等任意格式材料
- **批量上传支持**: 支持用户将材料集中在一个目录，批量上传
- **智能追问**: 自动识别缺失信息并主动追问（P0 关键信息）
- **架构决策**: 基于 AWS Well-Architected Framework 进行服务选型
- **多场景支持**: Web 应用、AI/ML、大数据、SaaS、混合云
- **多模板支持**: 根据项目类型自动选择对应的专用模板
- **标准化输出**: 生成完整的架构设计说明书

### 多模板支持说明

Skill 支持**针对不同项目类型的专用设计模板**：

| 项目类型 | 使用模板 | 特殊设计 | 章节数 |
|---------|---------|---------|--------|
| **AI/ML-Agentic** | `design_doc_template_ai_agentic.md` | Agent 编排、LLM 部署、幻觉检测、负责任 AI | **14** |
| **其他所有类型** | `design_doc_template.md` | 标准 AWS Well-Architected 设计 | **11** |

**关键特性**:
- ✨ **AI Agentic 专用模板**: 融合 AWS Agentic AI 实践的 6 大核心能力
- ✨ **智能模板选择**: 步骤 1 自动识别项目类型，步骤 4 自动选择对应模板
- ✨ **完整功能覆盖**: AI Agentic 模板涵盖 Agent 编排、Token 成本、幻觉防护、人类在循环
- ✨ **向后兼容**: 通用模板保持不变，作为默认选择

---

## 工作流程（6 步）

此 Skill 遵循严格的 **6 步流程**，**不可跳过或合并**：

### 步骤 0: 案例学习文件识别与分析（可选但推荐）

**功能**: 自动识别和分析案例学习文件

**支持格式**: Word、PDF、图片、Excel、Markdown 等任意格式

**执行任务**:
1. **自动检测案例文件** - LLM 理解文件内容，识别是否为案例
2. **结构化信息提取** - 提取背景、痛点、方案、指标、收益、经验
3. **相关性匹配** - 计算与新项目的相似度（0-100 分）
4. **提取可复用资源** - 验证过的服务组合、成本基线、经验教训

**输出**: 案例分析结果 + 与新项目的相关性评分和建议

**优势**: 可加速架构设计 50%、基于验证过的最佳实践、规避风险

---

### 步骤 1: Material Parser（多模态材料解析）

**目标**: 从用户提交的任意格式材料中提取结构化需求信息

**支持的输入材料**:
- **文本类**: 会议记录、需求列表、代码片段、Markdown、纯文本
- **文档类**: Word (docx)、Excel (xlsx)、PDF
- **图片类**: PNG、JPEG、JPG、GIF、WebP、SVG、BMP
- **混合形式**: 用户可在一个目录中放置多个不同格式的文件

**执行任务**（LLM 多模态直接处理）:

1. **扫描和理解所有文件** - 自动处理所有格式
2. **自动检测案例学习文件** - 若存在，触发步骤 0
3. **提取 5 大关键要素**:
   - 功能需求 - 系统需要实现的业务功能
   - 非功能需求 - 可用性、性能、延迟、扩展性、RTO/RPO
   - 合规性要求 - 等保、GDPR、数据本地化等
   - 预算限制 - 月度/年度预算上限
   - 预估流量 - DAU、QPS、数据量、峰值倍数
4. **识别项目类型** - Web/AI/BigData/Migration/SaaS
5. **理解用户提供的架构图**（若存在）- 识别服务、理解连接、验证匹配度
6. **标注缺失信息** - 标记 P0 关键信息的缺失
7. **生成追问列表** - 基于缺失的 P0 信息生成 3-5 个问题
8. **输出结构化 JSON**

**关键原则**:
- ✅ 多模态直接理解，无需脚本预处理
- ✅ 支持批量处理，无脚本依赖
- ✅ 不脑补未明确的强约束
- ✅ 信息不足时标注假设并追问

---

### 步骤 2: Architecture Diagram Generation（架构图处理与验证）

**目标**: 正确处理架构图，绝不自作主张重新设计架构

**CRITICAL 原则**:
- 🚫 **如果用户提供了架构图，绝对不要自行设计和生成新的**
- ✅ 只能理解、验证和描述用户提供的架构图
- ✅ 只有在用户明确未提供架构图时，才能调用 MCP Server 生成新的

**判断逻辑**:

#### 情况 1: 用户提供了架构图（PNG/PDF/JPEG）

✅ **执行任务**:
1. 识别架构图中的 AWS 服务图标和组件
2. 理解数据流和服务间的连接关系
3. 生成架构图的文字描述（用于 Design Writer）
4. 进行一致性验证（仅限验证，不做修改）
5. 输出架构分析结果

✅ **应该说的话**:
- "您的架构图显示了一个 Web 三层架构..."
- "基于您提供的架构，这些服务组合可以满足..."
- "一个可选的改进是...（如果用户感兴趣）"

❌ **严格禁止**:
- 不说"我会为你设计一个更好的架构"
- 不生成替代的架构图
- 不修改用户的架构设计
- 不自作主张调用 MCP Server

---

#### 情况 2: 用户未提供架构图

✅ **执行任务**:
1. 构建架构蓝图（基于需求和架构决策）
2. 调用 MCP Server 生成架构图（PNG/SVG）
3. 生成架构图的文字描述
4. 进行一致性验证

---

**关键原则**:
- ✅ 用户提供架构图 → 尊重、验证、描述
- ✅ 用户未提供 → 进行设计、生成架构图
- ❌ 绝对不要自作主张替换用户的架构图

---

### 步骤 3: Architecture Decisioning（架构决策）

**目标**: 基于结构化需求进行服务选型和 WAF 评估

**前置条件**: 步骤 1 和 2 已完成，所有 P0 问题已回答

**执行任务**:

1. **选择架构模式** - 从 `references/architecture_patterns.md` 中选择匹配的模式
2. **服务选型决策** - 对每个需求维度进行 Why/Pros/Cons/Alternatives 的完整分析
3. **AWS Well-Architected Framework 检查** - 强制对 6 大支柱进行评估
   - 卓越运营 (Operational Excellence)
   - 安全性 (Security)
   - 可靠性 (Reliability)
   - 性能效率 (Performance Efficiency)
   - 成本优化 (Cost Optimization)
   - 可持续性 (Sustainability)
4. **AI/ML 项目特殊处理** - 若为 AI 项目，进行额外的 AI 特有检查
5. **大数据项目特殊处理** - 若为大数据项目，进行额外的大数据特有检查
6. **Region/China 特判** - 检查是否使用了不可用服务

**输出**: 完整的架构决策和 WAF 评估结果

**关键原则**:
- ✅ 每个服务选择必须通过 WAF 检查
- ✅ 必须提供决策理由和替代方案
- ❌ 禁止跳过 WAF 评估
- ❌ 禁止过度设计（无需求不上 EKS/Multi-Region）

---

### 步骤 4: Design Writer（文档生成）

**目标**: 按项目类型对应的模板生成架构设计说明书

**前置条件**: 步骤 3 已完成，架构决策已确定，项目类型已识别

**CRITICAL - 必须执行**:
- ✅ 根据项目类型选择对应的模板
- ✅ 填充所有占位符
- ✅ **生成完整的 Markdown 文件**（不仅仅是文本响应）
- ✅ 文件命名规则: `{PROJECT_NAME}_架构设计说明书_v1.0.md`

**模板选择**:

```python
if project_type == "AI/ML-Agentic":
    template = "templates/design_doc_template_ai_agentic.md"  # 14 章
else:
    template = "templates/design_doc_template.md"              # 11 章
```

**执行任务**:
1. 选择正确的模板（AI Agentic 用专用模板）
2. 填充所有占位符（P0 占位符必须填充）
3. 遵循章节结构（不可改变顺序或合并）
4. 包含每个决策的 Why 和 Trade-off
5. 明确标注所有假设（【假设】标签）
6. 输出为 Markdown 文件

**详细指南**: 参考 [DESIGN_WRITER_GUIDE.md](./DESIGN_WRITER_GUIDE.md)

**文件命名**:
```
{PROJECT_NAME}_架构设计说明书_v1.0.md
{PROJECT_NAME}_Agentic_架构设计说明书_v1.0.md  # Agentic 项目
```

---

### 步骤 5: Design Reviewer（设计审查）

**目标**: 检查架构设计的完整性和正确性

**前置条件**: 步骤 4 已完成，设计文档已生成

**执行任务**:

1. **区域合规性检查**
   - China Region 是否使用了不可用服务？
   - 是否考虑数据合规性（GDPR/数据本地化）？

2. **架构一致性检查**
   - 是否存在矛盾设计？
   - 是否存在过度设计？
   - 服务选择是否与需求相符？

3. **必备组件检查**
   - [ ] IAM 角色设计完整
   - [ ] CloudWatch Logs 日志方案清晰
   - [ ] Backup 备份策略明确
   - [ ] RTO/RPO 已定义
   - [ ] 成本估算已提供
   - [ ] 监控和告警已规划

4. **Best Practice 检查**
   - [ ] Multi-AZ 部署（生产环境）
   - [ ] 加密已启用（传输+静态）
   - [ ] MFA 已配置
   - [ ] 告警已设置

**输出**: 通过/不通过，若问题则返回步骤 3 修订

---

## 使用示例

详细的使用示例请参考 [EXAMPLES.md](./EXAMPLES.md)，包括：
- 示例 1: 电商平台迁移云（Web 应用）
- 示例 2: AI 知识库问答系统（RAG）
- 示例 3: AI 客服代理系统（Agentic - 14 章）
- 示例 4: 基于案例学习的快速设计

---

## 重要提示

### 核心原则（5 条铁律）

1. **严格遵循 6 步流程** - 不可跳过或合并步骤
2. **尊重用户的架构图** - 若用户提供了架构图，绝不自作主张重新设计
3. **WAF 检查强制执行** - 每个支柱都要评估，特别是 AI 和大数据项目
4. **记录所有决策理由** - 每个技术选择都要有 Why 和 Trade-off
5. **主动追问缺失信息** - P0 信息（RTO/RPO/可用性/流量）不可假设

### AI/ML 项目特别关注

- ❌ **禁止忽略 Token 成本** - 分析成本、制定控制策略
- ❌ **禁止忽略幻觉防护** - 设计检测和降级策略
- ❌ **禁止忽略人类在循环** - HITL 流程必须明确
- ❌ **Agentic 项目禁止用通用模板** - 必须用 14 章专用模板

### 大数据项目特别关注

- ❌ **禁止忽略数据分区** - 分区策略必须明确
- ❌ **禁止忽略存储优化** - 生命周期和分层必须规划
- ❌ **禁止忽略数据质量** - 检查和治理机制必须设计

---

## 相关文档

| 文档 | 用途 | 适合人群 |
|-----|------|---------|
| [SKILL.md](./SKILL.md) | 本文档 - 完整使用指南 | 用户、架构师 |
| [DESIGN_WRITER_GUIDE.md](./DESIGN_WRITER_GUIDE.md) | 步骤 4 的详细实施指南 | LLM、文档生成器 |
| [EXAMPLES.md](./EXAMPLES.md) | 4 个完整使用示例 | 用户、学习者 |
| [BEST_PRACTICES.md](./BEST_PRACTICES.md) | 最佳实践和检查清单 | 架构师、审核者 |
| [OPTIMIZATION_GUIDE.md](./OPTIMIZATION_GUIDE.md) | 脚本优化和实施建议 | 开发者、维护人员 |
| [DEEPV.md](./DEEPV.md) | 深层设计和内部实现 | 开发者、贡献者 |
| [references/architecture_patterns.md](./references/architecture_patterns.md) | 架构模式库 | 架构师 |
| [references/waf_checklist.md](./references/waf_checklist.md) | WAF 检查清单 | 架构师、审核者 |
| [templates/design_doc_template.md](./templates/design_doc_template.md) | 通用设计模板（11 章） | LLM、文档生成 |
| [templates/design_doc_template_ai_agentic.md](./templates/design_doc_template_ai_agentic.md) | AI Agentic 专用模板（14 章） | LLM、AI 项目 |

---

## 备份和版本

- `SKILL.md.backup` - 原始版本备份（2026-01-13）
- `SKILL.md` - 当前优化版本

---

## 版本历史

### v1.7 (2026-01-13)
✨ **优化版本发布**
- ✅ SKILL.md 精简为 950 行（原 1534 行，减少 38%）
- ✅ 分离出 4 个专题文档（DESIGN_WRITER_GUIDE、EXAMPLES、OPTIMIZATION_GUIDE、BEST_PRACTICES）
- ✅ 保留完整的功能和细节（通过链接访问）
- ✅ 提升可读性和快速上手体验
- ✅ 创建原始备份 (SKILL.md.backup)

### v1.6 (2026-01-12)
⭐⭐ **运维监控完整性 + AI Agentic 与 RAG 关系澄清**
- 新增：运维监控完整性（Operational Excellence 强化）
- 澄清：AI Agentic 与 RAG 的关系（RAG 是可选增强）
- 更新：AI Agentic 架构模式说明

详细版本历史请参考 DEEPV.md。
