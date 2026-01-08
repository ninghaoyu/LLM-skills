# AWS 架构设计 Skill 安装指南

## 快速安装

### 方式 1: 从 Marketplace 安装（推荐）

1. 在 Claude 中使用以下命令：
   ```
   /install aws-arch-designer
   ```

2. 或者手动配置：
   - 点击 Settings → Plugins/Skills
   - 选择 "Add from Marketplace"
   - 搜索 "AWS 架构设计说明书生成器"
   - 点击 Install

### 方式 2: 从 GitHub 克隆安装

```bash
# 克隆仓库
git clone https://github.com/ninghaoyu/LLM-skills.git

# 进入 Skill 目录
cd LLM-skills/skills/aws-arch-designer

# 按照 SKILL.md 的说明使用该 Skill
```

## Marketplace 元数据

项目根目录下的 `.claude-plugin/marketplace.json` 包含了完整的 Skill 元数据：

```json
{
  "version": "1.0.0",
  "skills": [
    {
      "id": "aws-arch-designer",
      "name": "AWS 架构设计说明书生成器",
      "version": "1.0.0",
      "author": "ninghaoyu",
      "repository": {
        "type": "git",
        "url": "https://github.com/ninghaoyu/LLM-skills.git",
        "directory": "skills/aws-arch-designer"
      }
    }
  ]
}
```

## Skill 概览

### 📋 基本信息
- **ID**: `aws-arch-designer`
- **名称**: AWS 架构设计说明书生成器
- **版本**: 1.0.0
- **作者**: ninghaoyu
- **许可**: MIT
- **仓库**: https://github.com/ninghaoyu/LLM-skills.git

### 🎯 核心能力

1. **多模态材料解析**
   - 支持 Word、Excel、PDF、Markdown、图片等任意格式
   - LLM 直接处理，零预处理脚本

2. **批量上传支持**
   - 将材料集中在一个目录
   - 一次上传整个目录或多个混合格式文件

3. **智能追问**
   - 自动识别缺失的关键信息
   - 主动追问 RTO/RPO、峰值流量、合规要求等

4. **架构决策**
   - 基于 AWS Well-Architected Framework
   - 自动选择合适的架构模式

5. **多场景支持**
   - Web 应用、AI/ML、大数据、SaaS、混合云
   - 13 种预定义架构模式

6. **标准化输出**
   - 生成 11 章节完整架构设计说明书
   - Markdown 格式，可直接交付客户

7. **架构图生成**
   - 识别用户提供的架构图
   - 自动生成 AWS 标准架构图

8. **案例学习分析**
   - 识别案例学习文件
   - 支持与新项目的相关性匹配

### 📊 支持的架构模式（13 种）

#### 传统应用
- Web 三层架构
- Serverless API
- SaaS 多租户
- 混合云 / 专线

#### 大数据
- 批量数据处理平台
- 实时数据处理平台
- 数据湖架构
- 大数据计算集群

#### AI/ML
- GenAI 应用架构
- RAG 架构
- AI Agentic 系统架构
- ML 训练与推理平台
- 多模态 AI 架构

### 🔌 支持的 AWS 服务

**计算**: EC2, Lambda, ECS, EKS, Fargate

**数据库**: RDS, Aurora, DynamoDB, ElastiCache, Redshift

**存储**: S3, EBS, EFS

**网络**: VPC, ALB, NLB, CloudFront, Route 53

**AI/ML**: Amazon Bedrock, SageMaker, Rekognition, Textract

**大数据**: Athena, Glue, EMR, Kinesis, Lake Formation

### 🌍 支持的地域
- AWS Global
- AWS China

### 📚 文件结构

```
skills/aws-arch-designer/
├── SKILL.md                           # Skill 主文档（包含完整工作流）
├── DEEPV.md                           # 需求文档（2600+ 行详细规范）
├── README.md                          # 项目说明
├── SKILL_TEST_CASES.md                # 测试用例
├── references/
│   ├── architecture_patterns.md       # 架构模式库
│   └── waf_checklist.md              # WAF 检查清单
└── assets/
    └── design_doc_template.md        # 设计说明书模板
```

### 🔧 系统要求

| 要求 | 说明 |
|-----|------|
| **最小 Token** | 8,000 tokens |
| **推荐 Token** | 32,000 tokens |
| **支持的模型** | Claude 3.5 Sonnet<br/>Claude 3 Opus<br/>Claude 3 Sonnet |
| **执行时间** | 10-15 分钟（取决于材料复杂度） |
| **并发模式** | 顺序执行（Sequential） |

### 💡 使用场景

1. **材料整理**: 客户提供零散需求材料需要整理和结构化
2. **架构设计**: 需要进行 AWS 架构设计和规划
3. **文档生成**: 需要生成标准化的架构设计文档
4. **架构评估**: 基于 AWS Well-Architected Framework 进行评估
5. **AI/ML 项目**: GenAI、RAG、Agentic 系统架构设计
6. **大数据平台**: 批处理、实时流、数据湖架构设计
7. **SaaS 应用**: 多租户应用设计
8. **混合云方案**: 混合云和专线架构设计

## 工作流程（5 步）

### 步骤 0: 案例学习文件识别（可选）
- 自动识别案例学习文件
- 进行相关性匹配
- 提取可复用资源

### 步骤 1: 多模态材料解析与主动追问
- 处理任意格式文件
- 提取 5 大关键要素
- 识别项目类型
- 主动追问缺失信息

### 步骤 2: 架构图生成与验证
- 识别或生成架构图
- 一致性验证
- 生成文字描述

### 步骤 3: 架构决策与 WAF 评估
- 选择架构模式
- 进行服务选型
- 执行 WAF 六大支柱检查
- AI/ML 和大数据项目特殊处理

### 步骤 4: 架构设计说明书生成
- 11 章节标准模板
- 完整的设计说明书
- Markdown 格式

### 步骤 5: 设计评审与优化建议
- 最终设计评审
- 问题清单
- 修订建议

## 输入格式

支持的输入文件格式：
- 📝 **文本**: text/plain, text/markdown
- 📄 **文档**: PDF, DOCX, XLSX
- 🖼️ **图片**: PNG, JPEG, GIF, WebP, SVG, BMP

## 输出格式

生成的输出格式：
- 📝 Markdown（架构设计说明书）
- 📊 JSON（结构化数据）

## 集成

### MCP 服务集成
- **AWS Diagram MCP Server**: 用于自动生成 AWS 架构图

## 版本历史

### v1.0.0（2026-01-08）
- 完整重构：迁移到 LLM 原生多模态处理
- 删除所有脚本依赖（3200+ 行代码删除）
- 支持任意文件格式（Word、Excel、PDF、图片）
- 支持批量上传和混合格式
- 完全由 LLM 驱动，零维护成本
- 新增架构图生成和验证能力
- 新增案例学习文件分析和相关性匹配
- 扩展支持 13 种架构模式
- 支持 AWS 全球和中国区域

## 常见问题

### Q1: 这个 Skill 需要脚本吗？
**A**: 不需要。该 Skill 完全由 LLM 的多模态能力驱动，零脚本依赖。所有文件处理、架构决策、文档生成都由 LLM 直接执行。

### Q2: 支持哪些文件格式？
**A**: 支持任意格式，包括 Word、Excel、PDF、Markdown、图片（PNG、JPG、GIF、WebP、SVG、BMP）。

### Q3: 生成一份完整的设计说明书需要多长时间？
**A**: 通常需要 10-15 分钟，取决于材料复杂度和追问回合数。

### Q4: 支持中文吗？
**A**: 完全支持中文。所有文档、说明书都可以用中文生成。

### Q5: 可以用于中国 AWS 区域吗？
**A**: 可以。Skill 特别针对 AWS China 区域进行了优化，会自动检查服务可用性。

### Q6: 生成的架构图是什么格式？
**A**: 通过 AWS Diagram MCP Server 生成 PNG 或 SVG 格式的标准 AWS 架构图。

## 许可

MIT License - 详见仓库中的 LICENSE 文件

## 联系方式

如有问题或建议，请在 GitHub 上提交 Issue:
https://github.com/ninghaoyu/LLM-skills/issues

## 关键词

aws, 架构设计, 云计算, AI/ML, 大数据, 多模态, 文档生成, 架构图, Well-Architected, 系统设计

---

**Happy Architecture Designing! 🚀**
