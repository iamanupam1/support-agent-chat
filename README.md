# Support Agent Project

An autonomous customer support agent for an e-commerce platform, built with AI-powered chat capabilities. This project provides a comprehensive support system that can handle order inquiries, customer information, product searches, support ticket management, and more through a conversational interface.

## Features

- **AI-Powered Chat**: Uses Groq's LLM for intelligent, context-aware responses
- **Order Management**: Check order status, view order details, search orders
- **Customer Support**: Access customer information, order history, and support tickets
- **Product Queries**: Search products by category, price, or name
- **Analytics**: Get sales analytics and insights
- **Ticket Management**: Create, update, and search support tickets
- **Refund Processing**: Initiate refunds for eligible orders
- **Memory System**: Maintains conversation history across sessions
- **Dual Interfaces**: Streamlit web UI and FastAPI REST API

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI**: Groq API
- **Containerization**: Docker & Docker Compose
- **Other**: Pydantic for data validation, httpx for HTTP requests

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Groq API key (sign up at [groq.com](https://groq.com))

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd support_agent_project
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   DATABASE_URL=your_database_url_here
   ```

3. **Start the database**:
   ```bash
   docker-compose up -d
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database schema and seed data**:
   ```bash
   ./scripts/setup_db.sh
   ```

## Quick Start

After completing the installation steps above, you can start the application:

1. **Start the FastAPI backend**:
   ```bash
   uvicorn --app-dir src main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Streamlit frontend** (in a separate terminal):
   ```bash
   PYTHONPATH=. streamlit run frontend/app.py
   ```

The application will be available at:
- **Streamlit UI**: `http://localhost:8501`
- **FastAPI API**: `http://localhost:8000`

## Usage

### Running the Streamlit App

To run the web interface for chatting with the support agent:

```bash
PYTHONPATH=. streamlit run frontend/app.py
```

This will start the web interface at `http://localhost:8501` where you can chat with the support agent.

### Running the FastAPI Backend

To run the API server:

```bash
uvicorn --app-dir src main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- **POST /chat**: Send a chat message to the agent
  - Request body: `{"session_id": "string", "customer_id": "string", "message": "string"}`
  - Response: `{"reply": "string"}`

## Database Schema

The application uses PostgreSQL with the following tables:

- **customers**: Customer information (customer_id, name, email, phone, created_at)
- **products**: Product catalog (product_id, name, description, price, category, created_at)
- **orders**: Order records (order_id, customer_id, status, total_amount, created_at)
- **order_items**: Order line items (id, order_id, product_id, quantity, unit_price)
- **tickets**: Support tickets (ticket_id, customer_id, order_id, issue, status, created_at)

## Project Structure

```
support_agent_project/
├── frontend/
│   └── app.py              # Streamlit web interface
├── scripts/
│   └── setup_db.sh         # Database setup script
├── src/
│   ├── agent.py            # AI agent logic with Groq integration
│   ├── database.py         # Database connection and session management
│   ├── main.py             # FastAPI application entry point
│   ├── memory.py           # Conversation memory management
│   ├── models.py           # SQLAlchemy data models
│   ├── routes.py           # API route definitions
│   ├── seed_data.py        # Database seeding script
│   └── tools.py            # Database query tools for the agent
├── tests/                  # Unit and integration tests
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── docker-compose.yml      # Docker Compose configuration
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
