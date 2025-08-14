#!/usr/bin/env python3
"""
Simple test client for the MCP server to demonstrate churn prediction functionality.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_churn_prediction():
    # Server parameters for connecting to our MCP server
    server_params = StdioServerParameters(
        command="python", 
        args=["server.py"],
        env=None,
    )
    
    print("🚀 Connecting to MCP server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("✅ Connected to MCP server")
            
            # List available tools
            tools = await session.list_tools()
            print(f"📋 Available tools: {[tool.name for tool in tools.tools]}")
            
            # Test case 1: High-risk employee (low satisfaction, new, low pay)
            high_risk_employee = {
                "YearsAtCompany": 1,
                "EmployeeSatisfaction": 0.01,
                "Position": "Non-Manager", 
                "Salary": 2.0
            }
            
            print(f"\n🔍 Testing high-risk employee: {high_risk_employee}")
            
            result1 = await session.call_tool(
                "PredictChurn", 
                {"data": [high_risk_employee]}
            )
            print(f"📊 Prediction result: {result1.content[0].text}")
            
            # Test case 2: Low-risk employee (high satisfaction, experienced, good pay)  
            low_risk_employee = {
                "YearsAtCompany": 8,
                "EmployeeSatisfaction": 0.92,
                "Position": "Manager",
                "Salary": 7.5
            }
            
            print(f"\n🔍 Testing low-risk employee: {low_risk_employee}")
            
            result2 = await session.call_tool(
                "PredictChurn",
                {"data": [low_risk_employee]}
            )
            print(f"📊 Prediction result: {result2.content[0].text}")
            
            # Test case 3: Batch prediction
            batch_employees = [high_risk_employee, low_risk_employee]
            
            print(f"\n🔍 Testing batch prediction with {len(batch_employees)} employees")
            
            result3 = await session.call_tool(
                "PredictChurn",
                {"data": batch_employees}
            )
            print(f"📊 Batch prediction results: {result3.content[0].text}")

if __name__ == "__main__":
    print("🤖 MCP Churn Prediction Test Client")
    print("=" * 50)
    asyncio.run(test_churn_prediction())