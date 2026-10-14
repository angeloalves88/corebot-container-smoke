#!/usr/bin/env python3
"""Bot smoke do contrato Corebot Container (COREBOT_CONTRACT_VERSION=1)."""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    input_file = Path(os.environ.get("COREBOT_INPUT_FILE", "/corebot/input/input.json"))
    output_dir = Path(os.environ.get("COREBOT_OUTPUT_DIR", "/corebot/output"))

    if not input_file.is_file():
        print(f"ENVIRONMENT_ERROR: input ausente em {input_file}", file=sys.stderr, flush=True)
        return 4

    payload = json.loads(input_file.read_text(encoding="utf-8"))
    task_id = payload.get("task_id") or os.environ.get("COREBOT_TASK_ID")
    bot = payload.get("bot") or {}
    params = payload.get("parameters") or {}

    print(
        json.dumps(
            {
                "level": "info",
                "message": "smoke iniciado",
                "task_id": task_id,
                "bot": bot.get("name"),
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "uid": os.getuid() if hasattr(os, "getuid") else None,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    result = {
        "ok": True,
        "summary": f"smoke ok task={task_id}",
        "task_id": task_id,
        "bot": bot,
        "parameters": params,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps({"level": "info", "message": "smoke concluido", "summary": result["summary"]}),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
