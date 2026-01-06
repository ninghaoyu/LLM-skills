#!/usr/bin/env python3
"""
Material Parser - 从零散材料中提取结构化需求信息
"""

import json
import sys
from typing import Dict, List, Any

def parse_material(raw_input: str) -> Dict[str, Any]:
    """
    解析原始输入材料，提取关键要素

    Args:
        raw_input: 原始输入材料（会议记录、需求列表等）

    Returns:
        结构化的需求数据
    """
    # 这个函数由 LLM 实际执行，这里只是结构定义
    # LLM 会根据 SKILL.md 中的 Prompt 来执行实际的解析

    result = {
        "business_goals": [],
        "functional_requirements": [],
        "non_functional_requirements": {},
        "traffic_estimation": {},
        "constraints": {},
        "assumptions": [],
        "open_questions": [],
        "generated_questions_for_user": []
    }

    return result

def identify_project_type(requirements: Dict[str, Any]) -> str:
    """
    识别项目类型

    Returns:
        项目类型: "AI/ML", "Big Data", "Web Application", "Hybrid", "SaaS", etc.
    """
    # 检查关键词
    business_goals = " ".join(requirements.get("business_goals", []))
    functional_reqs = " ".join(requirements.get("functional_requirements", []))
    all_text = (business_goals + " " + functional_reqs).lower()

    # AI/ML 项目识别
    ai_keywords = ["llm", "生成式", "ai", "机器学习", "模型", "chatbot", "聊天", "知识库", "agent", "agentic"]
    if any(keyword in all_text for keyword in ai_keywords):
        if "知识库" in all_text or "文档检索" in all_text:
            return "AI/ML-RAG"
        elif "agent" in all_text or "任务编排" in all_text:
            return "AI/ML-Agentic"
        else:
            return "AI/ML-GenAI"

    # 大数据项目识别
    bigdata_keywords = ["大数据", "数据分析", "bi", "数据湖", "etl", "实时流", "kinesis", "spark", "hadoop"]
    if any(keyword in all_text for keyword in bigdata_keywords):
        if "实时" in all_text or "流数据" in all_text:
            return "BigData-Streaming"
        elif "数据湖" in all_text:
            return "BigData-DataLake"
        else:
            return "BigData-Batch"

    # 传统应用识别
    if "web" in all_text or "api" in all_text or "电商" in all_text:
        return "Web-Application"

    if "saas" in all_text or "多租户" in all_text:
        return "SaaS"

    if "混合云" in all_text or "专线" in all_text or "idc" in all_text:
        return "Hybrid-Cloud"

    return "Unknown"

def generate_clarification_questions(requirements: Dict[str, Any]) -> List[str]:
    """
    生成需要向用户追问的问题

    Returns:
        问题列表
    """
    questions = []

    nfr = requirements.get("non_functional_requirements", {})
    traffic = requirements.get("traffic_estimation", {})
    constraints = requirements.get("constraints", {})

    # P0 问题
    if not nfr.get("rto") or not nfr.get("rpo"):
        questions.append("请问对系统的 RTO(恢复时间目标)和 RPO(恢复点目标)有明确要求吗？例如: RTO < 4h, RPO < 1h")

    if not nfr.get("availability"):
        questions.append("对系统可用性有明确要求吗？例如: 99.9%、99.95%、99.99%")

    if not traffic.get("peak_qps") and not traffic.get("daily_active_users"):
        questions.append("请问系统的预估流量是多少？例如: 日活 10 万用户，峰值 QPS 500")

    if not constraints.get("region"):
        questions.append("是否有明确的 AWS 区域要求？例如: 必须使用中国区、必须在欧盟境内等")

    # P1 问题
    if not constraints.get("compliance"):
        questions.append("是否有明确的合规性要求？例如: 等保二级、GDPR、数据本地化等")

    if not traffic.get("peak_multiplier"):
        questions.append("请问系统的峰值流量大约是日常流量的多少倍？例如: 2-3倍")

    return questions[:5]  # 最多返回 5 个问题

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python material_parser.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        raw_input = f.read()

    result = parse_material(raw_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))
