# server.py
# Clean MCP server for deployment (HTTP transport) and use in Claude Code / MCP Inspector.

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import os
import json
import requests

# -----------------------------------------------------------------------------
# Server
# -----------------------------------------------------------------------------
mcp = FastMCP("churnandburn")


# -----------------------------------------------------------------------------
# Tools
# -----------------------------------------------------------------------------
@mcp.tool()
def PredictChurn(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Predicts whether one or more employees will churn.

    Args:
        data: A list of employee attribute dicts, e.g.:
              [
                {
                  "YearsAtCompany": 10,
                  "EmployeeSatisfaction": 0.99,
                  "Position": "Non-Manager",
                  "Salary": 5.0
                }
              ]

    Returns:
        dict: {"results": [...]} with one result per input item.
              Each result is the upstream model's JSON response or {"error": "..."}.
    """
    model_url = os.environ.get("MODEL_API_URL", "http://127.0.0.1:8000/predict")
    api_key = os.environ.get("MODEL_API_KEY", "")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Basic input validation
    if not isinstance(data, list) or len(data) == 0:
        return {"results": [{"error": "Input must be a non-empty list of dicts."}]}

    results: List[Dict[str, Any]] = []

    for i, payload in enumerate(data):
        if not isinstance(payload, dict):
            results.append({"error": f"Item {i} is not an object/dict."})
            continue

        try:
            resp = requests.post(
                model_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=20,
            )
            resp.raise_for_status()
            try:
                results.append(resp.json())
            except ValueError:
                results.append(
                    {
                        "error": "Upstream returned non-JSON response.",
                        "status": resp.status_code,
                        "text_preview": resp.text[:500],
                    }
                )
        except requests.RequestException as e:
            results.append({"error": f"Request failed: {e}"})

    return {"results": results}


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Run as a remote/hosted MCP server over HTTP (for Sevalla).
    # Connect with: https://<your-domain>/mcp from Claude Code or MCP Inspector.
    port = int(os.environ.get("PORT", "8080"))
    mcp.run(transport="http", host="0.0.0.0", port=port, path="/mcp")
