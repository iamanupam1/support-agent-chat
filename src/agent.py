from groq import Groq
from src.tools import Tools
import json
from dotenv import load_dotenv
import os

load_dotenv()

tools = Tools()

SYSTEM_PROMPT = """
You are an advanced autonomous customer support agent for an e-commerce platform with comprehensive access to order, customer, product, and support data.

Available tools:
- get_order_status: Get the status of a specific order by order_id
- get_order_details: Get detailed information about an order including all items
- search_orders: Search orders by customer, status, amount range
- get_customer_info: Get detailed customer information including order history summary
- search_products: Search products by category, price range, name
- get_ticket_details: Get detailed information about a specific support ticket
- search_tickets: Search support tickets by customer, order, status, issue keywords
- get_customer_orders_summary: Get complete order history with items for a customer
- get_sales_analytics: Get sales analytics including totals, status breakdowns, top products
- initiate_refund: Initiate a refund for an order (requires order_id and reason)
- create_ticket: Create a support ticket (requires customer_id, order_id, issue)
- update_ticket_status: Update the status of a support ticket
- insert_mock_data: Insert mock data into the database for testing
- general_query: Perform complex queries like customer orders with items, product sales, recent tickets

Rules:
- Use the most appropriate tool for each query to provide comprehensive answers
- For order-related questions, use get_order_details to show items
- For customer questions, use get_customer_info or get_customer_orders_summary
- For product questions, use search_products
- For analytics, use get_sales_analytics
- For ticket management, use appropriate ticket tools
- Always check order status before initiating refunds
- Only initiate refund if order is delivered or cancelled
- Create tickets for unresolved issues
- Use search tools for broad queries
- Respond helpfully and comprehensively using available data

Do not attempt to call functions in your response text. Use the tool calling mechanism only when ready.
"""

class Agent:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.tools = Tools()

    def run(self, customer_id, message, history):
        messages = history + [{"role": "user", "content": message}]

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_order_status",
                        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_order_details",
                        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_orders",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "customer_id": {"type": ["string", "null"]},
                                "status": {"type": ["string", "null"]},
                                "min_amount": {"type": ["number", "null"]},
                                "max_amount": {"type": ["number", "null"]}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_customer_info",
                        "parameters": {"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_products",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "category": {"type": ["string", "null"]},
                                "min_price": {"type": ["number", "null"]},
                                "max_price": {"type": ["number", "null"]},
                                "name_contains": {"type": ["string", "null"]}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_ticket_details",
                        "parameters": {"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_tickets",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "customer_id": {"type": ["string", "null"]},
                                "order_id": {"type": ["string", "null"]},
                                "status": {"type": ["string", "null"]},
                                "issue_contains": {"type": ["string", "null"]}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_customer_orders_summary",
                        "parameters": {"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_sales_analytics",
                        "parameters": {"type": "object", "properties": {}}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "initiate_refund",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "order_id": {"type": "string"},
                                "reason": {"type": "string"}
                            },
                            "required": ["order_id", "reason"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "create_ticket",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "customer_id": {"type": "string"},
                                "order_id": {"type": "string"},
                                "issue": {"type": "string"}
                            },
                            "required": ["customer_id", "order_id", "issue"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_ticket_status",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "ticket_id": {"type": "string"},
                                "new_status": {"type": "string"}
                            },
                            "required": ["ticket_id", "new_status"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "insert_mock_data",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "data_type": {"type": "string"},
                                "data": {"type": "object"}
                            },
                            "required": ["data_type", "data"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "general_query",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query_type": {"type": "string"}
                            },
                            "required": ["query_type"],
                            "additionalProperties": True
                        }
                    }
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            result = getattr(self.tools, name)(**args)

            messages.append(msg)
            messages.append({"role": "tool", "content": result, "tool_call_id": tool_call.id})

            final = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )

            return final.choices[0].message.content

        return msg.content
