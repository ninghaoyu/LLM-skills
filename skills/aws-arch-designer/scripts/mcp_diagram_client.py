#!/usr/bin/env python3
"""
AWS Diagram MCP Server Client

功能:
- 与 awslabs-aws-diagram-mcp-server 进行通信
- 将架构蓝图转换为 AWS 架构图
- 处理 MCP 服务的调用和响应

作者: AWS Architecture Designer Skill
版本: 1.0
"""

import json
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiagramFormat(Enum):
    """架构图输出格式"""
    PNG = "PNG"
    SVG = "SVG"
    PDF = "PDF"


class DiagramStyle(Enum):
    """架构图样式"""
    AWS_STANDARD = "aws_standard"
    AWS_DETAILED = "aws_detailed"
    MINIMAL = "minimal"


@dataclass
class MCPDiagramRequest:
    """MCP 架构图生成请求"""
    blueprint: Dict
    format: DiagramFormat = DiagramFormat.PNG
    style: DiagramStyle = DiagramStyle.AWS_STANDARD
    title: str = ""
    include_legend: bool = True
    include_annotations: bool = True


class MCPDiagramClient:
    """MCP 架构图客户端"""

    # MCP Server 配置
    MCP_SERVER_NAME = "awslabs-aws-diagram-mcp-server"
    DEFAULT_TIMEOUT = 30  # 秒

    def __init__(self):
        self.server_name = self.MCP_SERVER_NAME
        self.timeout = self.DEFAULT_TIMEOUT
        self.is_connected = False

    def connect(self) -> bool:
        """
        连接到 MCP Server

        Returns:
            是否连接成功
        """
        logger.info(f"Attempting to connect to {self.server_name}")
        try:
            # 在实际实现中,这里会进行真实的 MCP 连接
            # 目前为示意代码
            self.is_connected = True
            logger.info(f"Connected to {self.server_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {str(e)}")
            return False

    def validate_blueprint(self, blueprint: Dict) -> tuple[bool, list[str]]:
        """
        验证架构蓝图格式

        Args:
            blueprint: 架构蓝图

        Returns:
            (是否有效, 错误列表)
        """
        logger.info("Validating blueprint format")
        errors = []

        # 检查必需字段
        required_fields = ["pattern_name", "services", "connections", "network_config"]
        for field in required_fields:
            if field not in blueprint:
                errors.append(f"Missing required field: {field}")

        # 检查服务列表
        if "services" in blueprint:
            if not isinstance(blueprint["services"], list):
                errors.append("'services' must be a list")
            else:
                for i, service in enumerate(blueprint["services"]):
                    if "name" not in service or "type" not in service:
                        errors.append(f"Service {i} missing 'name' or 'type'")

        # 检查连接列表
        if "connections" in blueprint:
            if not isinstance(blueprint["connections"], list):
                errors.append("'connections' must be a list")
            else:
                service_names = {s["name"] for s in blueprint.get("services", [])}
                for i, conn in enumerate(blueprint["connections"]):
                    if "from_service" not in conn or "to_service" not in conn:
                        errors.append(f"Connection {i} missing 'from_service' or 'to_service'")
                    else:
                        if conn.get("from_service") not in service_names:
                            errors.append(
                                f"Connection {i}: unknown from_service '{conn.get('from_service')}'"
                            )
                        if conn.get("to_service") not in service_names:
                            errors.append(
                                f"Connection {i}: unknown to_service '{conn.get('to_service')}'"
                            )

        if errors:
            logger.warning(f"Blueprint validation failed with {len(errors)} errors")
        else:
            logger.info("Blueprint validation passed")

        return len(errors) == 0, errors

    def generate_diagram(
        self,
        blueprint: Dict,
        format: DiagramFormat = DiagramFormat.PNG,
        style: DiagramStyle = DiagramStyle.AWS_STANDARD,
        title: str = ""
    ) -> Dict:
        """
        调用 MCP Server 生成架构图

        Args:
            blueprint: 架构蓝图
            format: 输出格式
            style: 架构图样式
            title: 架构图标题

        Returns:
            生成结果
        """
        logger.info("Generating architecture diagram via MCP")

        # 1. 验证蓝图
        is_valid, errors = self.validate_blueprint(blueprint)
        if not is_valid:
            logger.error(f"Blueprint validation failed: {errors}")
            return {
                "status": "error",
                "error": "Blueprint validation failed",
                "details": errors
            }

        # 2. 准备请求
        request = self._prepare_request(blueprint, format, style, title)

        # 3. 调用 MCP Server
        try:
            response = self._call_mcp_server(request)
            logger.info("MCP server call completed")
            return response
        except Exception as e:
            logger.error(f"MCP server call failed: {str(e)}")
            return {
                "status": "error",
                "error": "MCP server call failed",
                "details": str(e)
            }

    def _prepare_request(
        self,
        blueprint: Dict,
        format: DiagramFormat,
        style: DiagramStyle,
        title: str
    ) -> MCPDiagramRequest:
        """准备 MCP 请求"""
        return MCPDiagramRequest(
            blueprint=blueprint,
            format=format,
            style=style,
            title=title or blueprint.get("pattern_name", "AWS Architecture")
        )

    def _call_mcp_server(self, request: MCPDiagramRequest) -> Dict:
        """
        调用 MCP Server

        在实际实现中,这里会进行真实的 MCP RPC 调用。
        目前为模拟实现。

        Args:
            request: MCP 请求

        Returns:
            MCP 响应
        """
        logger.info(f"Calling MCP server with format={request.format.value}, style={request.style.value}")

        # 模拟 MCP 响应
        # 在实际实现中,这里会调用真实的 MCP 接口
        mock_response = {
            "status": "success",
            "diagram_file": f"/tmp/aws_architecture_diagram.{request.format.value.lower()}",
            "diagram_format": request.format.value,
            "title": request.title,
            "services_detected": [
                {
                    "name": s["name"],
                    "type": s["type"],
                    "multi_az": s.get("multi_az", False)
                }
                for s in request.blueprint.get("services", [])
            ],
            "connections_detected": [
                {
                    "from": c["from_service"],
                    "to": c["to_service"],
                    "label": c["label"],
                    "protocol": c.get("protocol", "")
                }
                for c in request.blueprint.get("connections", [])
            ],
            "metadata": {
                "generation_time_ms": 2500,
                "version": "1.0"
            }
        }

        logger.info("MCP server response received")
        return mock_response

    def disconnect(self):
        """断开与 MCP Server 的连接"""
        logger.info(f"Disconnecting from {self.server_name}")
        self.is_connected = False


class DiagramGenerationOrchestrator:
    """架构图生成编排器"""

    def __init__(self):
        self.mcp_client = MCPDiagramClient()

    def generate_from_blueprint(
        self,
        blueprint: Dict,
        requirements: Dict = None
    ) -> Dict:
        """
        从架构蓝图生成完整的架构图信息

        Args:
            blueprint: 架构蓝图
            requirements: 业务需求(用于配置)

        Returns:
            完整的架构图信息
        """
        logger.info("Starting diagram generation orchestration")

        # 1. 连接到 MCP Server
        if not self.mcp_client.connect():
            logger.error("Failed to connect to MCP server, falling back to text-only")
            return self._generate_text_only(blueprint)

        try:
            # 2. 生成架构图
            diagram_result = self.mcp_client.generate_diagram(
                blueprint,
                format=DiagramFormat.PNG,
                style=DiagramStyle.AWS_STANDARD,
                title=blueprint.get("pattern_name", "AWS Architecture")
            )

            if diagram_result.get("status") != "success":
                logger.warning("MCP diagram generation failed, using text-only output")
                return self._generate_text_only(blueprint)

            # 3. 整合结果
            result = {
                "diagram_source": "auto_generated",
                "mcp_server_used": True,
                "diagram_file": diagram_result.get("diagram_file"),
                "diagram_format": diagram_result.get("diagram_format"),
                "services": diagram_result.get("services_detected", []),
                "connections": diagram_result.get("connections_detected", []),
                "metadata": diagram_result.get("metadata", {}),
                "generated_successfully": True
            }

            logger.info("Diagram generation completed successfully")
            return result

        except Exception as e:
            logger.error(f"Diagram generation failed: {str(e)}")
            return self._generate_text_only(blueprint)
        finally:
            self.mcp_client.disconnect()

    def _generate_text_only(self, blueprint: Dict) -> Dict:
        """
        生成纯文本格式的架构信息(降级方案)

        Args:
            blueprint: 架构蓝图

        Returns:
            文本格式的架构信息
        """
        logger.info("Generating text-only architecture description (fallback)")

        return {
            "diagram_source": "auto_generated",
            "mcp_server_used": False,
            "format": "text",
            "architecture_description": self._build_text_description(blueprint),
            "services": [
                {
                    "name": s["name"],
                    "type": s["type"],
                    "multi_az": s.get("multi_az", False)
                }
                for s in blueprint.get("services", [])
            ],
            "connections": [
                {
                    "from": c["from_service"],
                    "to": c["to_service"],
                    "label": c["label"]
                }
                for c in blueprint.get("connections", [])
            ],
            "generated_successfully": True,
            "notes": "Diagram generation via MCP server failed. Text-only description provided."
        }

    def _build_text_description(self, blueprint: Dict) -> str:
        """构建文本描述"""
        desc = f"## {blueprint.get('pattern_name', 'AWS Architecture')}\n\n"

        # 服务列表
        desc += "### Services:\n"
        for service in blueprint.get("services", []):
            multi_az = " (Multi-AZ)" if service.get("multi_az") else ""
            desc += f"- {service['name']}: {service['type']}{multi_az}\n"

        # 连接关系
        desc += "\n### Connections:\n"
        for conn in blueprint.get("connections", []):
            desc += f"- {conn['from_service']} -> {conn['to_service']}: {conn['label']}\n"

        # 网络配置
        desc += "\n### Network Configuration:\n"
        network = blueprint.get("network_config", {})
        desc += f"- VPC CIDR: {network.get('vpc_cidr', 'N/A')}\n"
        desc += f"- Multi-AZ: {'Yes' if network.get('multi_az') else 'No'}\n"

        return desc


# 示例使用
if __name__ == "__main__":
    # 示例架构蓝图
    sample_blueprint = {
        "pattern_name": "Web 三层架构",
        "services": [
            {
                "name": "ALB",
                "type": "Application Load Balancer",
                "multi_az": True
            },
            {
                "name": "EC2-ASG",
                "type": "EC2 Auto Scaling Group",
                "multi_az": True,
                "config": {"instance_type": "t3.medium"}
            },
            {
                "name": "RDS",
                "type": "RDS for MySQL",
                "multi_az": True,
                "config": {"storage": "200GB"}
            },
            {
                "name": "S3",
                "type": "Amazon S3",
                "config": {"versioning": True}
            }
        ],
        "connections": [
            {
                "from_service": "ALB",
                "to_service": "EC2-ASG",
                "label": "Forward Traffic",
                "protocol": "TCP 80/443"
            },
            {
                "from_service": "EC2-ASG",
                "to_service": "RDS",
                "label": "SQL Query",
                "protocol": "TCP 3306"
            },
            {
                "from_service": "EC2-ASG",
                "to_service": "S3",
                "label": "Object Store",
                "protocol": "HTTPS"
            }
        ],
        "network_config": {
            "vpc_cidr": "10.0.0.0/16",
            "multi_az": True,
            "subnets": [
                {"name": "Public-1a", "tier": "public", "cidr": "10.0.1.0/24"},
                {"name": "Public-1b", "tier": "public", "cidr": "10.0.2.0/24"},
                {"name": "Private-1a", "tier": "private", "cidr": "10.0.11.0/24"},
                {"name": "Private-1b", "tier": "private", "cidr": "10.0.12.0/24"}
            ]
        }
    }

    orchestrator = DiagramGenerationOrchestrator()
    result = orchestrator.generate_from_blueprint(sample_blueprint)

    print(json.dumps(result, indent=2, ensure_ascii=False))
