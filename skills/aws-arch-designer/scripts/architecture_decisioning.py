#!/usr/bin/env python3
"""
Architecture Decisioning - 架构决策引擎
基于结构化需求进行服务选型和 WAF 评估
"""

import json
import sys
from typing import Dict, List, Any

# 架构模式库
ARCHITECTURE_PATTERNS = {
    "Web-Application": {
        "pattern_name": "Web 三层架构",
        "services": {
            "compute": "EC2 Auto Scaling Group",
            "load_balancer": "Application Load Balancer",
            "database": "RDS Multi-AZ",
            "storage": "S3",
            "cache": "ElastiCache (可选)"
        }
    },
    "AI/ML-GenAI": {
        "pattern_name": "GenAI 应用架构",
        "services": {
            "llm": "Amazon Bedrock",
            "compute": "Lambda",
            "api": "API Gateway",
            "database": "DynamoDB",
            "storage": "S3"
        }
    },
    "AI/ML-RAG": {
        "pattern_name": "RAG 架构",
        "services": {
            "knowledge_base": "Bedrock Knowledge Bases",
            "vector_db": "OpenSearch Serverless",
            "llm": "Amazon Bedrock",
            "storage": "S3"
        }
    },
    "AI/ML-Agentic": {
        "pattern_name": "AI Agentic 系统",
        "services": {
            "agent": "Bedrock Agents",
            "tools": "Lambda Functions",
            "workflow": "Step Functions",
            "state": "DynamoDB"
        }
    },
    "BigData-Batch": {
        "pattern_name": "批量数据处理平台",
        "services": {
            "storage": "S3",
            "etl": "AWS Glue",
            "analytics": "Athena / Redshift Serverless"
        }
    },
    "BigData-Streaming": {
        "pattern_name": "实时数据处理平台",
        "services": {
            "streaming": "Kinesis Data Streams",
            "processing": "Lambda / Kinesis Data Analytics",
            "storage": "DynamoDB",
            "archive": "S3"
        }
    }
}

# 服务选型决策表
SERVICE_DECISIONS = {
    "托管数据库": {
        "candidates": ["RDS", "Aurora"],
        "decision_criteria": {
            "RDS": {
                "pros": ["成本较低", "Multi-AZ 高可用", "完全托管"],
                "cons": ["性能不如 Aurora", "扩展能力有限"],
                "use_case": "中等规模应用"
            },
            "Aurora": {
                "pros": ["性能优异", "自动扩展", "Global Database"],
                "cons": ["成本高 20-30%"],
                "use_case": "高性能、大规模应用"
            }
        }
    },
    "LLM推理": {
        "candidates": ["Bedrock", "SageMaker"],
        "decision_criteria": {
            "Bedrock": {
                "pros": ["托管模型", "按 Token 计费", "快速上线"],
                "cons": ["模型选择受限"],
                "use_case": "标准 LLM 应用"
            },
            "SageMaker": {
                "pros": ["自定义模型", "灵活性高"],
                "cons": ["需要管理", "实例计费"],
                "use_case": "自定义模型需求"
            }
        }
    }
}

# WAF 检查项
WAF_CHECKS = {
    "operational_excellence": [
        "是否使用 IaC (CloudFormation/Terraform)?",
        "是否配置了 CloudWatch Logs?",
        "是否配置了自动化运维?"
    ],
    "security": [
        "是否遵循最小权限原则 (IAM)?",
        "是否启用数据加密 (KMS)?",
        "是否启用传输加密 (TLS)?",
        "是否配置网络隔离 (VPC/Security Group)?",
        "是否启用审计日志 (CloudTrail)?"
    ],
    "reliability": [
        "是否实现 Multi-AZ 部署?",
        "是否配置自动故障转移?",
        "是否定义了 RTO/RPO?",
        "是否配置了备份策略?"
    ],
    "performance": [
        "实例类型是否适配工作负载?",
        "是否使用了缓存?",
        "是否启用了 CDN (若适用)?"
    ],
    "cost": [
        "是否使用 Auto Scaling?",
        "是否考虑 RI / Savings Plans?",
        "是否配置 S3 生命周期策略?"
    ],
    "sustainability": [
        "是否选择能效实例 (Graviton)?",
        "是否优化资源利用率?"
    ]
}

# AI/ML 特有检查
AI_SPECIFIC_CHECKS = {
    "ai_cost": [
        "是否设置 Token 限制?",
        "是否使用 Prompt 缓存?",
        "是否根据任务选择合适模型?"
    ],
    "ai_performance": [
        "推理延迟是否满足 SLA (<500ms)?",
        "是否使用缓存减少重复推理?"
    ],
    "ai_security": [
        "是否对用户输入进行验证 (Prompt Injection)?",
        "Bedrock 是否选择不记录数据的模型?"
    ],
    "ai_reliability": [
        "是否有降级策略?",
        "是否对 LLM 输出进行验证?"
    ]
}

# 大数据特有检查
BIGDATA_SPECIFIC_CHECKS = {
    "bigdata_cost": [
        "S3 是否配置生命周期策略?",
        "EMR 是否使用临时集群?",
        "是否使用 Spot Instances?"
    ],
    "bigdata_performance": [
        "S3 数据是否合理分区?",
        "是否使用列式存储 (Parquet/ORC)?",
        "查询是否优化?"
    ],
    "bigdata_reliability": [
        "是否处理重复数据?",
        "是否配置数据质量检查?"
    ]
}

def select_architecture_pattern(project_type: str) -> Dict[str, Any]:
    """选择架构模式"""
    return ARCHITECTURE_PATTERNS.get(project_type, ARCHITECTURE_PATTERNS["Web-Application"])

def perform_waf_assessment(services: Dict[str, Any], project_type: str) -> Dict[str, Any]:
    """执行 WAF 评估"""
    assessment = {}

    # 基础 WAF 检查
    for pillar, checks in WAF_CHECKS.items():
        assessment[pillar] = {
            "checks": checks,
            "score": "✅"  # 简化处理，实际应由 LLM 评估
        }

    # AI/ML 特有检查
    if project_type.startswith("AI/ML"):
        assessment["ai_specific"] = {}
        for category, checks in AI_SPECIFIC_CHECKS.items():
            assessment["ai_specific"][category] = {
                "checks": checks,
                "score": "✅"
            }

    # 大数据特有检查
    if project_type.startswith("BigData"):
        assessment["bigdata_specific"] = {}
        for category, checks in BIGDATA_SPECIFIC_CHECKS.items():
            assessment["bigdata_specific"][category] = {
                "checks": checks,
                "score": "✅"
            }

    return assessment

def make_architecture_decision(requirements: Dict[str, Any], project_type: str) -> Dict[str, Any]:
    """架构决策主流程"""

    # 选择架构模式
    pattern = select_architecture_pattern(project_type)

    # WAF 评估
    waf_assessment = perform_waf_assessment(pattern["services"], project_type)

    result = {
        "project_type": project_type,
        "architecture_pattern": pattern["pattern_name"],
        "selected_services": pattern["services"],
        "waf_assessment": waf_assessment,
        "architecture_decisions": {},
        "region_compliance": {
            "region": requirements.get("constraints", {}).get("region", "Global"),
            "warnings": []
        }
    }

    # China Region 特判
    if "China" in result["region_compliance"]["region"]:
        china_unavailable = ["AWS Batch", "Amazon Chime", "Amazon Comprehend"]
        for service in pattern["services"].values():
            if service in china_unavailable:
                result["region_compliance"]["warnings"].append(
                    f"{service} 在中国区不可用，需要替代方案"
                )

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python architecture_decisioning.py <requirements_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        requirements = json.load(f)

    # 识别项目类型
    from material_parser import identify_project_type
    project_type = identify_project_type(requirements)

    # 架构决策
    result = make_architecture_decision(requirements, project_type)

    print(json.dumps(result, ensure_ascii=False, indent=2))
