from src.database import engine, Base
from src.models import Customer, Product, Order, OrderItem, SupportTicket
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Drop all tables and recreate
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Dummy data for Customers
customers_data = [
    {"customer_id": "CUST001", "name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"},
    {"customer_id": "CUST002", "name": "Jane Smith", "email": "jane@example.com", "phone": "098-765-4321"},
    {"customer_id": "CUST003", "name": "Bob Johnson", "email": "bob@example.com", "phone": "555-123-4567"},
]

# Dummy data for Products
products_data = [
    {"product_id": "PROD001", "name": "Laptop", "description": "High-performance laptop", "price": 1200.00, "category": "Electronics"},
    {"product_id": "PROD002", "name": "Mouse", "description": "Wireless mouse", "price": 25.00, "category": "Electronics"},
    {"product_id": "PROD003", "name": "Keyboard", "description": "Mechanical keyboard", "price": 80.00, "category": "Electronics"},
    {"product_id": "PROD004", "name": "Book", "description": "Programming book", "price": 45.00, "category": "Books"},
    {"product_id": "PROD005", "name": "Headphones", "description": "Noise-cancelling headphones", "price": 150.00, "category": "Electronics"},
]

# Dummy data for Orders
orders_data = [
    {"order_id": "ORD001", "customer_id": "CUST001", "status": "shipped", "total_amount": 150.00},
    {"order_id": "ORD002", "customer_id": "CUST002", "status": "pending", "total_amount": 200.50},
    {"order_id": "ORD003", "customer_id": "CUST001", "status": "delivered", "total_amount": 75.25},
    {"order_id": "ORD004", "customer_id": "CUST003", "status": "cancelled", "total_amount": 300.00},
    {"order_id": "ORD005", "customer_id": "CUST002", "status": "shipped", "total_amount": 120.75},
]

# Dummy data for OrderItems
order_items_data = [
    {"order_id": "ORD001", "product_id": "PROD002", "quantity": 2, "unit_price": 25.00},
    {"order_id": "ORD001", "product_id": "PROD003", "quantity": 1, "unit_price": 80.00},
    {"order_id": "ORD001", "product_id": "PROD004", "quantity": 1, "unit_price": 45.00},
    {"order_id": "ORD002", "product_id": "PROD001", "quantity": 1, "unit_price": 1200.00},
    {"order_id": "ORD002", "product_id": "PROD005", "quantity": 1, "unit_price": 150.00},
    {"order_id": "ORD003", "product_id": "PROD002", "quantity": 3, "unit_price": 25.00},
    {"order_id": "ORD004", "product_id": "PROD001", "quantity": 1, "unit_price": 1200.00},
    {"order_id": "ORD005", "product_id": "PROD003", "quantity": 1, "unit_price": 80.00},
    {"order_id": "ORD005", "product_id": "PROD004", "quantity": 1, "unit_price": 45.00},
]

# Dummy data for SupportTickets
tickets_data = [
    {"ticket_id": "TICK001", "customer_id": "CUST001", "order_id": "ORD001", "issue": "Wrong item received", "status": "open"},
    {"ticket_id": "TICK002", "customer_id": "CUST002", "order_id": "ORD002", "issue": "Delayed delivery", "status": "in_progress"},
    {"ticket_id": "TICK003", "customer_id": "CUST001", "order_id": "ORD003", "issue": "Refund request", "status": "closed"},
    {"ticket_id": "TICK004", "customer_id": "CUST003", "order_id": "ORD004", "issue": "Cancellation issue", "status": "open"},
    {"ticket_id": "TICK005", "customer_id": "CUST002", "order_id": "ORD005", "issue": "Damaged product", "status": "resolved"},
]

# Insert dummy customers
for customer_data in customers_data:
    customer = Customer(**customer_data)
    session.add(customer)

# Insert dummy products
for product_data in products_data:
    product = Product(**product_data)
    session.add(product)

# Insert dummy orders
for order_data in orders_data:
    order = Order(**order_data)
    session.add(order)

# Insert dummy order items
for item_data in order_items_data:
    item = OrderItem(**item_data)
    session.add(item)

# Insert dummy tickets
for ticket_data in tickets_data:
    ticket = SupportTicket(**ticket_data)
    session.add(ticket)

# Commit the changes
session.commit()

# Close the session
session.close()

print("Dummy data inserted successfully!")