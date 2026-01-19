# References 参考文档目录

本目录包含所有参考类文档，供 LLM 在执行各个步骤时查阅。

---

## 📚 文档列表

### 1️⃣ 架构模式参考
**文件**: [architecture_patterns.md](./architecture_patterns.md)
**用途**: 预定义的架构模式库（Web 三层、Serverless、大数据、AI/ML 等）
**使用时机**: 步骤 2 Architecture Decisioning

---

### 2️⃣ WAF 检查清单
**文件**: [waf_checklist.md](./waf_checklist.md)
**用途**: AWS Well-Architected Framework 六大支柱检查清单
**使用时机**:
- 步骤 2 Architecture Decisioning（设计时）
- 步骤 5 Design Reviewer（审查时）

---

### 3️⃣ Agentic AI 实践要求
**文件**: [agentic_ai_practice_requirements.md](./agentic_ai_practice_requirements.md)
**用途**: AI Agentic 项目的特殊要求和实践标准
**使用时机**:
- 步骤 2 Architecture Decisioning（AI/ML-Agentic 项目）
- 步骤 4 Design Writer（填充 AI Agentic 模板时）
- 步骤 5 Design Reviewer（审查 AI 项目时）

---

### 4️⃣ 写作标准参考手册 ⭐
**文件**: [WRITING_STANDARDS.md](./WRITING_STANDARDS.md)
**用途**: 架构设计说明书的写作标准、规范和检查清单
**使用时机**:
- ⭐⭐⭐ 步骤 4 Design Writer（生成前预习、填充时参考、生成后质检）
- ⭐ 步骤 5 Design Reviewer（质量验证）

**关键内容**:
- 5 个黄金标准（专业性、丰满性、量化性、逻辑性、精简性）
- 7 大写作规范（技术决策表达、避免啰嗦、量化数据等）
- 质量检查清单（章节级 + 文档级）
- 常见错误与纠正
- 快速自检方法

---

### 5️⃣ 写作标准使用指南
**文件**: [WHEN_TO_USE_WRITING_STANDARDS.md](./WHEN_TO_USE_WRITING_STANDARDS.md)
**用途**: 详细说明何时参考 WRITING_STANDARDS.md
**使用时机**: 首次使用时阅读

**关键内容**:
- 5 个详细使用场景
- 完整使用流程示例
- 快速参考索引（按阶段、问题、章节）
- 与其他文档的关系图

---

### 6️⃣ 写作标准使用总结
**文件**: [WRITING_STANDARDS_USAGE_SUMMARY.md](./WRITING_STANDARDS_USAGE_SUMMARY.md)
**用途**: WRITING_STANDARDS.md 使用场景的总结报告
**使用时机**: 查看使用频率统计和流程可视化

---

### 7️⃣ 写作标准整合总结
**文件**: [WRITING_STANDARDS_INTEGRATION_SUMMARY.md](./WRITING_STANDARDS_INTEGRATION_SUMMARY.md)
**用途**: 写作标准在 SKILL.md 中的整合记录
**使用时机**: 了解写作标准是如何被整合到工作流程中的

---

## 📊 使用频率统计

| 参考文档 | 使用频率 | 主要用途 |
|---------|---------|---------|
| **WRITING_STANDARDS.md** | 每个项目 | 步骤 4 写作质量控制 ⭐⭐⭐ |
| **waf_checklist.md** | 每个项目 | 步骤 2/5 架构质量检查 ⭐⭐⭐ |
| **architecture_patterns.md** | 每个项目 | 步骤 2 架构模式选择 ⭐⭐⭐ |
| **agentic_ai_practice_requirements.md** | AI/ML 项目 | 步骤 2/4/5 AI 项目特殊要求 ⭐⭐ |
| **WHEN_TO_USE_WRITING_STANDARDS.md** | 首次使用 | 了解写作标准使用场景 ⭐ |

---

## 🔍 快速查找

### 按步骤查找

| 步骤 | 需要参考的文档 |
|-----|--------------|
| **步骤 2: Architecture Decisioning** | architecture_patterns.md, waf_checklist.md, agentic_ai_practice_requirements.md (AI 项目) |
| **步骤 4: Design Writer** | WRITING_STANDARDS.md ⭐⭐⭐ |
| **步骤 5: Design Reviewer** | waf_checklist.md, WRITING_STANDARDS.md, agentic_ai_practice_requirements.md (AI 项目) |

---

### 按项目类型查找

| 项目类型 | 需要参考的文档 |
|---------|--------------|
| **传统 Web 应用** | architecture_patterns.md, waf_checklist.md, WRITING_STANDARDS.md |
| **大数据项目** | architecture_patterns.md, waf_checklist.md, WRITING_STANDARDS.md |
| **AI/ML 项目** | architecture_patterns.md, waf_checklist.md, agentic_ai_practice_requirements.md, WRITING_STANDARDS.md |

---

## 📝 维护说明

### 新增参考文档时
1. ✅ 将文件放入 `references/` 目录
2. ✅ 在本 README.md 中添加文档说明
3. ✅ 在 SKILL.md 相应步骤中添加引用
4. ✅ 更新使用频率统计表

### 文档命名规范
- **架构相关**: `architecture_*.md`
- **检查清单**: `*_checklist.md`
- **实践要求**: `*_requirements.md`
- **标准规范**: `*_STANDARDS.md`（全大写）
- **使用指南**: `WHEN_TO_USE_*.md`

---

## ✅ 目录完整性检查

- [x] architecture_patterns.md
- [x] waf_checklist.md
- [x] agentic_ai_practice_requirements.md
- [x] WRITING_STANDARDS.md
- [x] WHEN_TO_USE_WRITING_STANDARDS.md
- [x] WRITING_STANDARDS_USAGE_SUMMARY.md
- [x] WRITING_STANDARDS_INTEGRATION_SUMMARY.md
- [x] README.md（本文件）

---

**最后更新**: 2026-01-18
**维护者**: AWS 架构设计 Skill 团队
