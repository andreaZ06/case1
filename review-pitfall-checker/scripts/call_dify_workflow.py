"""Dify Workflow 调用脚本。

当前使用 Dify Workflow by ID 接口：
POST /workflows/{workflow_id}/run

密钥只从环境变量或 .env 读取，避免把敏感信息写进代码。
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import requests


DEFAULT_API_BASE_URL = "https://api.dify.ai/v1"


class DifyWorkflowError(RuntimeError):
    """Dify Workflow 调用失败时抛出的业务异常。"""


def load_dotenv_file(env_path: str | Path = ".env") -> None:
    """轻量读取 .env 文件；已有环境变量优先，不会被覆盖。"""

    path = Path(env_path)
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_dify_config(env_path: str | Path = ".env") -> dict[str, str]:
    """读取 Dify 配置，缺少关键配置时给出清晰错误。"""

    load_dotenv_file(env_path)
    api_key = os.getenv("DIFY_API_KEY", "").strip()
    workflow_id = os.getenv("WORKFLOW_ID", "").strip()
    api_base_url = os.getenv("DIFY_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")

    missing = [
        name
        for name, value in (("DIFY_API_KEY", api_key), ("WORKFLOW_ID", workflow_id))
        if not value
    ]
    if missing:
        raise DifyWorkflowError(f"缺少 Dify 配置: {', '.join(missing)}")

    return {
        "api_key": api_key,
        "workflow_id": workflow_id,
        "api_base_url": api_base_url,
    }


def parse_workflow_outputs(response_json: dict[str, Any]) -> list[dict[str, Any]]:
    """从 Dify 响应中提取统一的分析结果列表。"""

    data = response_json.get("data", {})
    outputs = data.get("outputs") or response_json.get("outputs") or {}

    raw_result = (
        outputs.get("results")
        or outputs.get("result")
        or outputs.get("analysis_results")
        or []
    )

    if isinstance(raw_result, str):
        try:
            raw_result = json.loads(raw_result)
        except json.JSONDecodeError as exc:
            raise DifyWorkflowError("Dify 输出不是合法 JSON") from exc

    if isinstance(raw_result, dict):
        raw_result = [raw_result]

    if not isinstance(raw_result, list):
        raise DifyWorkflowError("Dify 输出格式不符合预期，期望列表或对象")

    parsed: list[dict[str, Any]] = []
    for item in raw_result:
        if not isinstance(item, dict):
            continue
        parsed.append(
            {
                "review_id": item.get("review_id", ""),
                "risk_level": item.get("risk_level", ""),
                "impact_on_user": item.get("impact_on_user", ""),
                "matched_scenario": item.get("matched_scenario", ""),
                "reason": item.get("reason", ""),
            }
        )

    return parsed


def run_dify_workflow(
    reviews: list[dict[str, Any]],
    user_scenario: str,
    product_id: str = "",
    env_path: str | Path = ".env",
    timeout_seconds: int = 60,
    max_retries: int = 3,
) -> list[dict[str, Any]]:
    """调用 Dify Workflow，带超时、重试和错误处理。"""

    config = get_dify_config(env_path)
    url = f"{config['api_base_url']}/workflows/{config['workflow_id']}/run"
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {
            "product_id": product_id,
            "reviews": reviews,
            "user_scenario": user_scenario,
        },
        "response_mode": "blocking",
        "user": "review-pitfall-checker",
    }

    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                url, headers=headers, json=payload, timeout=timeout_seconds
            )
            response.raise_for_status()
            return parse_workflow_outputs(response.json())
        except (requests.RequestException, ValueError, DifyWorkflowError) as exc:
            last_error = exc
            if attempt == max_retries:
                break
            time.sleep(min(2**attempt, 8))

    raise DifyWorkflowError(f"Dify Workflow 调用失败: {last_error}") from last_error
