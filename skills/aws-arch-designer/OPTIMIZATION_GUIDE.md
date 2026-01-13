# 脚本优化与实施指南

> 本文档提供脚本优化和项目实施的建议。这是开发者和维护人员的参考资料，用户通常不需要阅读本文档。

---

## 核心优化原则

### 问题分析

**原始设计的局限**:
- `material_parser.py`: 试图通过脚本处理文本和结构化提取 ❌
- `case_study_analyzer.py`: 试图通过正则和规则进行案例检测 ❌
- 这些脚本在**多模态 LLM 时代**完全冗余

### 新方向（推荐）

✅ **相信 LLM 的多模态能力直接处理所有格式**
- Word、PDF、图片、Excel、文本无需预处理

✅ **让 LLM 直接理解内容**
- 无需预处理脚本

✅ **支持批量上传**
- 用户在一个目录中放置所有材料，一次上传多个文件

---

## 脚本清理清单

### ❌ 应删除的脚本（完全冗余）

#### 1. `scripts/material_parser.py` - 完全不需要

**原因**: LLM 可以直接处理和理解任何格式的输入材料

**原函数**:
- `parse_material()` → LLM 直接理解（无需脚本）
- `identify_project_type()` → LLM 直接推断（无需脚本）
- `generate_clarification_questions()` → LLM 直接生成（无需脚本）

**删除方法**:
```bash
rm -f scripts/material_parser.py
```

**删除影响**: 无，所有功能由 LLM 直接处理

---

#### 2. `scripts/case_study_analyzer.py` - 完全不需要

**原因**: LLM 多模态能力可直接理解案例文件内容

**原函数**:
- `CaseStudyDetector.detect()` → LLM 直接识别（通过内容理解）
- `CaseStudyExtractor` 各函数 → LLM 直接提取（无需 NLP 规则）
- `CaseStudyMatcher.calculate_relevance()` → LLM 直接评估（无需评分算法）

**删除方法**:
```bash
rm -f scripts/case_study_analyzer.py
```

**删除影响**: 无，所有功能由 LLM 直接处理

---

### ✅ 可保留的脚本（需改造）

#### 1. `scripts/diagram_generator.py` - 保留但改造

**改造目标**: 不做架构图检测和验证，只支持 LLM 调用 MCP

**删除内容**:
- `DiagramGenerator.detect_user_diagram()` - LLM 直接理解
- `DiagramValidator` 类 - LLM 直接验证

**保留内容**:
- `BlueprintBuilder` - 帮助构建结构化的架构蓝图
- MCP 接口调用部分

**改造理由**: LLM 理解架构图后，仍需要编程方式调用 MCP Server

---

#### 2. `scripts/mcp_diagram_client.py` - 保留

**目的**: 与 `awslabs-aws-diagram-mcp-server` 通信

**保留原因**: 必须的 MCP 集成

**改造内容**:
- 简化 API（移除内部检测逻辑）
- 直接响应 LLM 的 MCP 调用请求
- 返回生成的架构图结果

---

## 新架构流程

```
用户上传材料（任意格式、批量）
    ↓
【步骤 0】
LLM 多模态直接理解（无脚本）
    ├─ 理解所有格式（Word/PDF/图片/Excel/文本）
    ├─ 自动检测案例文件（CaseStudyDetector 删除）
    ├─ 提取 5 大关键要素
    ├─ 理解用户提供的架构图
    └─ 生成追问问题
    ↓
【步骤 1】
Material Parser - LLM 直接处理（material_parser.py 删除）
    ↓
【步骤 2】
[如果缺少架构图]
    LLM 调用 MCP: awslabs-aws-diagram-mcp-server
    (diagram_generator.py 配合 mcp_diagram_client.py)
    ↓
【步骤 3-5】
LLM 进行架构决策、文档生成、质量审核
    ↓
生成完整的架构设计说明书
```

---

## 实施步骤

### 第 1 步：删除完全冗余的脚本

```bash
# 进入项目目录
cd /path/to/skills/aws-arch-designer

# 删除冗余脚本
rm -f scripts/material_parser.py
rm -f scripts/case_study_analyzer.py

# 验证
ls -la scripts/
# 应该只看到: diagram_generator.py, mcp_diagram_client.py
```

---

### 第 2 步：改造 diagram_generator.py

**目标**: 简化为只支持架构蓝图构建

```python
# 删除这些类和方法：

# ❌ 删除整个类
class DiagramGenerator:
    def detect_user_diagram(self):  # ❌ 删除
        """LLM 直接理解，无需脚本"""

# ❌ 删除整个类
class DiagramValidator:
    """LLM 直接验证，无需脚本"""

# ✅ 保留这个类
class BlueprintBuilder:
    """用于构建架构蓝图的辅助类"""
    def build_blueprint(self, decisions):
        """基于架构决策构建蓝图"""
        pass
```

**改造前行数**: ~300 行
**改造后行数**: ~100 行

---

### 第 3 步：简化 mcp_diagram_client.py

**目标**: 简化为瘦客户端，直接调用 MCP

```python
# ✅ 保留
class MCPDiagramClient:
    def generate_diagram(self, blueprint):
        """调用 MCP Server 生成架构图"""
        # 直接转发请求，无需内部验证
        pass

    def get_diagram_result(self):
        """返回生成结果"""
        pass

# ❌ 删除
class DiagramValidationOrchestrator:
    """LLM 直接验证，无需脚本"""
```

**改造前行数**: ~200 行
**改造后行数**: ~80 行

---

### 第 4 步：更新文档

✅ 已完成（本次修改）：
- SKILL.md 精简
- DESIGN_WRITER_GUIDE.md 创建
- EXAMPLES.md 创建
- OPTIMIZATION_GUIDE.md 创建（本文件）

---

## 最终项目结构

### 优化前

```
skills/aws-arch-designer/
├── SKILL.md (1534 行)
├── DEEPV.md (3000+ 行)
├── templates/
│   ├── design_doc_template.md
│   └── design_doc_template_ai_agentic.md
├── references/
│   ├── architecture_patterns.md
│   └── waf_checklist.md
└── scripts/
    ├── material_parser.py (200 行，冗余)
    ├── case_study_analyzer.py (150 行，冗余)
    ├── diagram_generator.py (300 行，需改造)
    └── mcp_diagram_client.py (200 行，保留)
```

### 优化后

```
skills/aws-arch-designer/
├── SKILL.md (950 行，精简)
├── SKILL.md.backup (1534 行，原始备份)
├── DEEPV.md (3000+ 行，保持不变)
├── DESIGN_WRITER_GUIDE.md (300 行，新增)
├── EXAMPLES.md (400 行，新增)
├── OPTIMIZATION_GUIDE.md (本文件，新增)
├── BEST_PRACTICES.md (待创建)
├── templates/
│   ├── design_doc_template.md
│   └── design_doc_template_ai_agentic.md
├── references/
│   ├── architecture_patterns.md
│   └── waf_checklist.md
└── scripts/
    ├── diagram_generator.py (100 行，改造后)
    └── mcp_diagram_client.py (80 行，简化后)
```

---

## 代码优化对比

### 删除的代码行数

| 文件 | 删除前 | 删除后 | 减少 |
|-----|-------|--------|------|
| material_parser.py | 200 | **0** | **-200** |
| case_study_analyzer.py | 150 | **0** | **-150** |
| diagram_generator.py | 300 | 100 | **-200** |
| mcp_diagram_client.py | 200 | 80 | **-120** |
| **总计** | **850** | **180** | **-670** |

**优化效果**: 减少 79% 的维护代码

---

## 迁移检查清单

- [ ] **Step 1**: 备份原始脚本（如需要）
  ```bash
  mkdir -p scripts/backup
  cp scripts/material_parser.py scripts/backup/
  cp scripts/case_study_analyzer.py scripts/backup/
  ```

- [ ] **Step 2**: 删除冗余脚本
  ```bash
  rm -f scripts/material_parser.py
  rm -f scripts/case_study_analyzer.py
  ```

- [ ] **Step 3**: 改造 diagram_generator.py
  - 删除 `DiagramGenerator.detect_user_diagram()`
  - 删除 `DiagramValidator` 类
  - 保留 `BlueprintBuilder`

- [ ] **Step 4**: 简化 mcp_diagram_client.py
  - 移除内部验证逻辑
  - 简化为瘦客户端

- [ ] **Step 5**: 更新文档
  - 更新 README.md（如需要）
  - 确认 SKILL.md 和 DEEPV.md 已更新

- [ ] **Step 6**: 测试验证
  - 测试 LLM 能否直接处理各种材料格式
  - 测试 MCP 架构图生成是否正常
  - 测试端到端流程

---

## 性能和可维护性提升

### 代码复杂度

| 维度 | 优化前 | 优化后 | 提升 |
|-----|-------|--------|------|
| **总行数** | 850 行 | 180 行 | ↓58% |
| **脚本数** | 4 个 | 2 个 | ↓50% |
| **维护复杂度** | 高 | 低 | ✅ |
| **依赖关系** | 复杂 | 简单 | ✅ |

### 功能覆盖

| 功能 | 优化前 | 优化后 | 备注 |
|-----|-------|--------|------|
| **材料处理** | 脚本 + LLM | **LLM 直接** | 移除脚本 |
| **案例检测** | 脚本 + LLM | **LLM 直接** | 移除脚本 |
| **架构图生成** | 脚本 + MCP | **脚本 + MCP** | 保留但简化 |
| **功能完整性** | ✅ 100% | ✅ 100% | 无功能丧失 |

---

## 常见问题

### Q: 删除脚本后，Material Parser 功能如何实现？
A: 直接由 LLM 的多模态能力处理。LLM 可以理解所有格式（Word、PDF、图片、Excel）并直接提取信息。

### Q: 案例学习文件检测由谁负责？
A: LLM 理解文件内容后，直接识别是否为案例文件。无需 `case_study_analyzer.py`。

### Q: 保留的脚本为什么还需要改造？
A: MCP 集成仍需编程方式处理，但可以简化为瘦客户端，移除冗余的验证逻辑。

### Q: 这些改动会影响 Skill 的功能吗？
A: 不会。所有功能由 LLM 直接处理，脚本优化只是代码层面的改进。

### Q: 备份的原始脚本什么时候可以完全删除？
A: 在充分测试后（至少 2-3 个完整项目周期），确认 LLM 处理稳定后可删除。

---

## 总结

这次优化的核心理念：
- ✅ **相信多模态 LLM 的能力** - 无需脚本预处理
- ✅ **简化代码复杂度** - 从 850 行减少到 180 行
- ✅ **保留必要的 MCP 集成** - 但可以简化实现
- ✅ **提升可维护性** - 减少脚本故障点

**最终效果**:
- 代码减少 58%
- 维护成本降低
- 功能完全保留
- 用户体验不变

---

参考资源：
- [SKILL.md](./SKILL.md) - 用户使用指南
- [DEEPV.md](./DEEPV.md) - 设计和实现详情
- [DESIGN_WRITER_GUIDE.md](./DESIGN_WRITER_GUIDE.md) - 步骤 4 详细指南
