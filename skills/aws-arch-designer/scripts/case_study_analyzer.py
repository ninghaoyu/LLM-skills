#!/usr/bin/env python3
"""
案例学习文件分析器

功能:
- 检测和识别案例学习文件
- 提取案例文件中的关键信息(背景、痛点、方案、架构图、收益)
- 建立新项目与案例的关联,进行相关性匹配
- 从案例中提取可复用的架构和经验

作者: AWS Architecture Designer Skill
版本: 1.0
"""

import json
import logging
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Industry(Enum):
    """行业分类"""
    ECOMMERCE = "ecommerce"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    MANUFACTURING = "manufacturing"
    MEDIA = "media"
    TELECOM = "telecom"
    TRAVEL = "travel"
    OTHER = "other"


class CompanyScale(Enum):
    """公司规模"""
    STARTUP = "startup"  # < 50 员工
    SMALL = "small"  # 50-250 员工
    MEDIUM = "medium"  # 250-1000 员工
    LARGE = "large"  # > 1000 员工


@dataclass
class ProjectBackground:
    """项目背景信息"""
    title: str
    description: str
    industry: str
    company_scale: str
    current_infrastructure: str
    team_size: Optional[str] = None
    annual_users: Optional[str] = None
    daily_active_users: Optional[str] = None


@dataclass
class PainPoint:
    """痛点信息"""
    title: str
    description: str
    impact: str
    severity: str = "medium"  # high, medium, low


@dataclass
class AWSService:
    """AWS 服务信息"""
    name: str
    role: str
    configuration: Dict = None
    justification: str = ""

    def __post_init__(self):
        if self.configuration is None:
            self.configuration = {}


@dataclass
class AWSolution:
    """AWS 解决方案"""
    architecture_pattern: str
    services: List[AWSService]
    overview: str
    key_highlights: List[str] = None

    def __post_init__(self):
        if self.key_highlights is None:
            self.key_highlights = []


@dataclass
class Benefit:
    """收益信息"""
    category: str  # cost_savings, performance, scalability, reliability
    metric: str
    baseline: Optional[str]
    target: Optional[str]
    improvement_percentage: Optional[float]
    business_impact: str


@dataclass
class CaseStudy:
    """完整的案例学习信息"""
    metadata: Dict
    background: ProjectBackground
    pain_points: List[PainPoint]
    aws_solution: AWSolution
    key_metrics: Dict
    expected_benefits: List[Benefit]
    lessons_learned: List[str]
    architecture_diagram: Optional[Dict] = None
    references: Optional[Dict] = None


class CaseStudyDetector:
    """案例学习文件检测器"""

    # 案例相关的关键词
    CASE_STUDY_KEYWORDS = {
        "chinese": [
            "案例", "项目背景", "痛点", "解决方案", "架构图",
            "收益", "经验", "最佳实践", "迁移", "云化"
        ],
        "english": [
            "case study", "project overview", "background", "challenge",
            "painpoint", "solution", "architecture", "benefit",
            "lessons learned", "migration", "aws solution"
        ]
    }

    # 案例文件的标准文件名模式
    CASE_STUDY_FILENAME_PATTERNS = [
        r".*case\s*study.*",
        r".*案例.*",
        r".*项目.*架构.*",
        r".*迁移.*方案.*",
        r".*解决.*方案.*"
    ]

    @staticmethod
    def detect(filename: str, content: str) -> bool:
        """
        检测是否为案例学习文件

        Args:
            filename: 文件名
            content: 文件内容

        Returns:
            是否为案例学习文件
        """
        logger.info(f"Detecting case study file: {filename}")

        # 1. 检查文件名
        filename_lower = filename.lower()
        for pattern in CaseStudyDetector.CASE_STUDY_FILENAME_PATTERNS:
            if re.match(pattern, filename_lower):
                logger.info("Matched filename pattern, detected as case study")
                return True

        # 2. 检查内容关键词
        content_lower = content.lower()
        keyword_count = 0

        all_keywords = (
            CaseStudyDetector.CASE_STUDY_KEYWORDS["chinese"] +
            CaseStudyDetector.CASE_STUDY_KEYWORDS["english"]
        )

        for keyword in all_keywords:
            if keyword in content_lower:
                keyword_count += 1

        # 如果包含 3 个或以上关键词,判定为案例学习文件
        if keyword_count >= 3:
            logger.info(f"Found {keyword_count} case study keywords, detected as case study")
            return True

        return False


class CaseStudyExtractor:
    """案例学习信息提取器"""

    def __init__(self):
        self.detector = CaseStudyDetector()

    def extract(self, content: str) -> CaseStudy:
        """
        从案例文件中提取结构化信息

        Args:
            content: 文件内容(Markdown / 纯文本)

        Returns:
            CaseStudy 对象
        """
        logger.info("Extracting case study information")

        case_study = CaseStudy(
            metadata=self._extract_metadata(content),
            background=self._extract_background(content),
            pain_points=self._extract_pain_points(content),
            aws_solution=self._extract_aws_solution(content),
            key_metrics=self._extract_key_metrics(content),
            expected_benefits=self._extract_benefits(content),
            lessons_learned=self._extract_lessons(content),
            architecture_diagram=self._detect_diagram(content)
        )

        logger.info(f"Extraction completed: {len(case_study.pain_points)} pain points, "
                   f"{len(case_study.aws_solution.services)} AWS services")

        return case_study

    def _extract_metadata(self, content: str) -> Dict:
        """提取元数据"""
        metadata = {
            "title": "",
            "industry": "unknown",
            "company_scale": "unknown"
        }

        # 尝试从第一行或标题提取标题
        lines = content.split('\n')
        for line in lines[:5]:
            if line.startswith('#'):
                metadata["title"] = line.replace('#', '').strip()
                break

        return metadata

    def _extract_background(self, content: str) -> ProjectBackground:
        """提取项目背景"""
        # 从内容中提取背景信息(简化实现)
        lines = content.split('\n')
        description = ""
        for i, line in enumerate(lines):
            if "背景" in line or "background" in line.lower():
                # 收集后续的几行作为背景描述
                description = '\n'.join(lines[i+1:i+5])
                break

        return ProjectBackground(
            title="",
            description=description,
            industry="unknown",
            company_scale="unknown",
            current_infrastructure=""
        )

    def _extract_pain_points(self, content: str) -> List[PainPoint]:
        """提取痛点"""
        pain_points = []
        lines = content.split('\n')

        # 查找"痛点"、"问题"、"challenge"相关的部分
        in_pain_point_section = False
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ["痛点", "problem", "challenge"]):
                in_pain_point_section = True
                continue

            if in_pain_point_section:
                # 尝试识别列表项
                if line.strip().startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                    pain_text = line.lstrip('-*•0123456789. ').strip()
                    if pain_text:
                        pain_points.append(PainPoint(
                            title=pain_text.split(':')[0],
                            description=pain_text,
                            impact="unknown",
                            severity="medium"
                        ))

                # 如果遇到新的章节,停止收集
                if line.startswith('##') and "痛点" not in line:
                    break

        return pain_points

    def _extract_aws_solution(self, content: str) -> AWSolution:
        """提取 AWS 解决方案"""
        services = []
        lines = content.split('\n')

        # 查找 AWS 服务相关的部分
        aws_service_keywords = {
            "ec2": "计算层",
            "rds": "数据库",
            "s3": "存储",
            "lambda": "计算",
            "dynamodb": "数据库",
            "alb": "负载均衡",
            "nlb": "负载均衡",
            "elasticache": "缓存",
            "cloudfront": "CDN",
            "cloudwatch": "监控",
            "kinesis": "流数据"
        }

        for line in lines:
            line_lower = line.lower()
            for service_key, role in aws_service_keywords.items():
                if service_key in line_lower:
                    # 提取服务名称和相关配置
                    match = re.search(r'(Amazon\s+|AWS\s+)?[\w\s]+', line)
                    if match:
                        service_name = match.group(0).strip()
                        services.append(AWSService(
                            name=service_name,
                            role=role
                        ))

        # 识别架构模式
        architecture_pattern = "Unknown"
        if "三层" in content or "three-tier" in content.lower():
            architecture_pattern = "Web 三层架构"
        elif "微服务" in content or "microservice" in content.lower():
            architecture_pattern = "微服务架构"
        elif "serverless" in content.lower():
            architecture_pattern = "Serverless 架构"

        return AWSolution(
            architecture_pattern=architecture_pattern,
            services=services,
            overview="",
            key_highlights=[]
        )

    def _extract_key_metrics(self, content: str) -> Dict:
        """提取关键指标"""
        metrics = {}

        # 数字提取正则
        number_patterns = {
            "可用性|availability": "availability",
            "qps|请求|request": "qps",
            "延迟|latency": "latency",
            "用户|user|dau|mau": "users",
            "数据|data|volume": "data_volume",
            "成本|cost|价格": "cost"
        }

        for line in content.split('\n'):
            for pattern, key in number_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    # 尝试提取数字
                    numbers = re.findall(r'[\d.]+\s*(%|k|m|b|gb|tb|%)?', line, re.IGNORECASE)
                    if numbers:
                        metrics[key] = numbers[0]

        return metrics

    def _extract_benefits(self, content: str) -> List[Benefit]:
        """提取预期收益"""
        benefits = []
        lines = content.split('\n')

        # 查找收益部分
        in_benefit_section = False
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ["收益", "benefit", "improvement"]):
                in_benefit_section = True
                continue

            if in_benefit_section:
                if line.strip().startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                    benefit_text = line.lstrip('-*•0123456789. ').strip()
                    if benefit_text:
                        # 尝试提取百分比
                        percentage_match = re.search(r'(\d+)%', benefit_text)
                        percentage = float(percentage_match.group(1)) if percentage_match else None

                        benefits.append(Benefit(
                            category="general",
                            metric=benefit_text.split(':')[0],
                            baseline=None,
                            target=None,
                            improvement_percentage=percentage,
                            business_impact=benefit_text
                        ))

                if line.startswith('##') and "收益" not in line:
                    break

        return benefits

    def _extract_lessons(self, content: str) -> List[str]:
        """提取经验教训"""
        lessons = []
        lines = content.split('\n')

        # 查找经验部分
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ["经验", "lesson", "best practice"]):
                # 收集后续列表
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip().startswith(('-', '*', '•')) or re.match(r'^\d+\.', lines[j]):
                        lesson_text = lines[j].lstrip('-*•0123456789. ').strip()
                        if lesson_text:
                            lessons.append(lesson_text)
                    elif lines[j].startswith('##'):
                        break

        return lessons

    def _detect_diagram(self, content: str) -> Optional[Dict]:
        """检测是否包含架构图"""
        # 查找图片引用(Markdown 格式)
        image_patterns = [
            r'!\[.*?\]\((.*?)\)',  # Markdown 格式
            r'<img.*?src=["\']([^"\']+)["\']',  # HTML 格式
        ]

        for pattern in image_patterns:
            match = re.search(pattern, content)
            if match:
                return {
                    "detected": True,
                    "file_path": match.group(1),
                    "format": "unknown"
                }

        return {"detected": False, "file_path": None}


class CaseStudyMatcher:
    """案例与新项目的匹配器"""

    @staticmethod
    def calculate_relevance(
        new_project: Dict,
        case_study: CaseStudy
    ) -> Tuple[float, List[str]]:
        """
        计算案例与新项目的相关性

        Args:
            new_project: 新项目信息
            case_study: 案例学习信息

        Returns:
            (相关性分数 0-100, 匹配理由列表)
        """
        logger.info("Calculating case study relevance")

        score = 0
        reasons = []

        # 1. 行业相似性 (30 分)
        if (new_project.get("industry") and
            new_project.get("industry").lower() in case_study.background.industry.lower()):
            score += 30
            reasons.append("行业相同或相似")

        # 2. 规模相似性 (20 分)
        project_scale = new_project.get("company_scale", "").lower()
        case_scale = case_study.background.company_scale.lower()
        if project_scale and case_scale and project_scale == case_scale:
            score += 20
            reasons.append("公司规模相近")

        # 3. 痛点相似性 (30 分)
        project_pain_points = set(str(p).lower() for p in new_project.get("pain_points", []))
        case_pain_points = set(p.title.lower() for p in case_study.pain_points)

        matching_pain_points = len(project_pain_points & case_pain_points)
        score += min(30, matching_pain_points * 10)
        if matching_pain_points > 0:
            reasons.append(f"共有 {matching_pain_points} 个相同或相似的痛点")

        # 4. 功能需求相似性 (20 分)
        project_features = set(str(f).lower() for f in new_project.get("functional_requirements", []))
        case_services = set(s.name.lower() for s in case_study.aws_solution.services)

        matching_features = len(project_features & case_services)
        score += min(20, matching_features * 5)
        if matching_features > 0:
            reasons.append(f"案例中的 {matching_features} 个 AWS 服务可复用")

        # 5. 架构模式相似性 (extra bonus)
        if "architecture_pattern" in new_project:
            if case_study.aws_solution.architecture_pattern.lower() in new_project.get("architecture_pattern", "").lower():
                score += 10
                reasons.append("架构模式一致")

        logger.info(f"Relevance score: {score}/100")
        return min(100, score), reasons

    @staticmethod
    def extract_reusable_services(case_study: CaseStudy) -> List[Dict]:
        """
        从案例中提取可复用的 AWS 服务组合

        Args:
            case_study: 案例学习信息

        Returns:
            可复用服务列表
        """
        reusable_services = []

        for service in case_study.aws_solution.services:
            reusable_services.append({
                "name": service.name,
                "role": service.role,
                "configuration": service.configuration,
                "source_case": case_study.metadata.get("title", "Unknown"),
                "validated": True
            })

        return reusable_services


class CaseStudyAnalyzer:
    """案例学习分析主类"""

    def __init__(self):
        self.detector = CaseStudyDetector()
        self.extractor = CaseStudyExtractor()
        self.matcher = CaseStudyMatcher()

    def analyze(self, filename: str, content: str) -> Dict:
        """
        完整分析案例学习文件

        Args:
            filename: 文件名
            content: 文件内容

        Returns:
            分析结果
        """
        logger.info(f"Starting case study analysis: {filename}")

        # 1. 检测
        is_case_study = self.detector.detect(filename, content)
        if not is_case_study:
            logger.warning("Not detected as case study")
            return {"is_case_study": False, "message": "File is not a case study"}

        # 2. 提取
        case_study = self.extractor.extract(content)

        # 3. 输出结果
        result = {
            "is_case_study": True,
            "case_study_metadata": asdict(case_study.metadata),
            "project_background": asdict(case_study.background),
            "pain_points": [asdict(p) for p in case_study.pain_points],
            "aws_solution": {
                "pattern": case_study.aws_solution.architecture_pattern,
                "services": [asdict(s) for s in case_study.aws_solution.services],
                "highlights": case_study.aws_solution.key_highlights
            },
            "key_metrics": case_study.key_metrics,
            "expected_benefits": [asdict(b) for b in case_study.expected_benefits],
            "lessons_learned": case_study.lessons_learned,
            "architecture_diagram": case_study.architecture_diagram
        }

        logger.info("Case study analysis completed")
        return result

    def match_with_project(self, case_study: Dict, new_project: Dict) -> Dict:
        """
        将案例与新项目进行匹配

        Args:
            case_study: 案例学习信息
            new_project: 新项目信息

        Returns:
            匹配结果
        """
        logger.info("Matching case study with new project")

        # 重建 CaseStudy 对象(简化版)
        relevance_score, reasons = self.matcher.calculate_relevance(
            new_project,
            case_study
        )

        # 提取可复用的服务
        reusable_services = self.matcher.extract_reusable_services(case_study)

        return {
            "relevance_score": relevance_score,
            "relevance_level": "high" if relevance_score >= 70 else "medium" if relevance_score >= 40 else "low",
            "matching_reasons": reasons,
            "reusable_services": reusable_services,
            "recommendations": self._generate_recommendations(relevance_score, case_study)
        }

    def _generate_recommendations(self, relevance_score: float, case_study: Dict) -> List[str]:
        """生成建议"""
        recommendations = []

        if relevance_score >= 70:
            recommendations.append("该案例与当前项目高度相关,强烈建议采用类似的架构")
            recommendations.append(f"直接参考案例的 AWS 服务组合可加快设计速度")

        if relevance_score >= 40:
            recommendations.append("该案例提供了有价值的参考,部分服务和经验可复用")

        # 添加经验教训建议
        if "lessons_learned" in case_study and case_study["lessons_learned"]:
            recommendations.append("重点关注案例提供的关键经验教训,规避潜在风险")

        return recommendations


# 示例使用
if __name__ == "__main__":
    sample_case_study = """
# 电商平台云迁移案例

## 项目背景
XX 公司是一家在线电商平台,日均用户 10 万,目前部署在自建数据中心。

## 痛点
- 高运维成本: 年度成本 150 万
- 扩展困难: 高峰期流量翻倍
- 可用性低: 仅 95%
- 迁移风险高

## AWS 解决方案
基于 Web 三层架构:
- EC2 Auto Scaling Group (t3.medium)
- RDS for MySQL Multi-AZ
- Application Load Balancer
- Amazon S3
- ElastiCache Redis
- CloudWatch

## 关键指标
- 可用性: 99.9%
- 响应时间: <200ms
- 峰值 QPS: 500
- 成本节省: 40%(年省 60 万)

## 经验教训
1. 提前进行应用改造
2. 数据库迁移是关键路径
3. Multi-AZ 虽增加成本但提升可用性
4. 缓存策略对性能至关重要
"""

    analyzer = CaseStudyAnalyzer()
    result = analyzer.analyze("case_study.md", sample_case_study)
    print(json.dumps(result, indent=2, ensure_ascii=False))
