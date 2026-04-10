from typing import Optional, List, Dict, Any
from src.database import SessionLocal
from src.models import Customer, Product, Order, OrderItem, SupportTicket
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import and_, or_, func
from datetime import datetime
import uuid

class Tools:

    def get_order_status(self, order_id: str) -> str:
        """Get the status of a specific order by order_id"""
        db = SessionLocal()
        try:
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if not order:
                return "Order not found"
            return f"Order {order.order_id} | Status: {order.status} | Amount: ${order.total_amount}"
        finally:
            db.close()

    def get_order_details(self, order_id: str) -> str:
        """Get detailed information about an order including items"""
        db = SessionLocal()
        try:
            order = db.query(Order).options(
                joinedload(Order.customer),
                joinedload(Order.items).joinedload(OrderItem.product)
            ).filter(Order.order_id == order_id).first()

            if not order:
                return "Order not found"

            details = f"Order {order.order_id}\n"
            details += f"Customer: {order.customer.name} ({order.customer.email})\n"
            details += f"Status: {order.status}\n"
            details += f"Total Amount: ${order.total_amount}\n"
            details += f"Items:\n"

            for item in order.items:
                details += f"  - {item.product.name} (x{item.quantity}) @ ${item.unit_price} each\n"

            return details
        finally:
            db.close()

    def search_orders(self, customer_id: Optional[str] = None, status: Optional[str] = None,
                     min_amount: Optional[float] = None, max_amount: Optional[float] = None) -> str:
        """Search orders by various criteria"""
        db = SessionLocal()
        try:
            query = db.query(Order).options(joinedload(Order.customer))

            filters = []
            if customer_id:
                filters.append(Order.customer_id == customer_id)
            if status:
                filters.append(Order.status == status)
            if min_amount:
                filters.append(Order.total_amount >= min_amount)
            if max_amount:
                filters.append(Order.total_amount <= max_amount)

            if filters:
                query = query.filter(and_(*filters))

            orders = query.all()

            if not orders:
                return "No orders found matching criteria"

            result = f"Found {len(orders)} orders:\n"
            for order in orders:
                result += f"- {order.order_id}: {order.customer.name}, Status: {order.status}, Amount: ${order.total_amount}\n"

            return result
        finally:
            db.close()

    def get_customer_info(self, customer_id: str) -> str:
        """Get detailed information about a customer"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            if not customer:
                return "Customer not found"

            # Get order count and total spent
            orders = db.query(Order).filter(Order.customer_id == customer_id).all()
            order_count = len(orders)
            total_spent = sum(order.total_amount for order in orders)

            # Get ticket count
            tickets = db.query(SupportTicket).filter(SupportTicket.customer_id == customer_id).all()
            ticket_count = len(tickets)

            return f"Customer {customer.customer_id}\n" \
                   f"Name: {customer.name}\n" \
                   f"Email: {customer.email}\n" \
                   f"Phone: {customer.phone}\n" \
                   f"Orders: {order_count}\n" \
                   f"Total Spent: ${total_spent}\n" \
                   f"Support Tickets: {ticket_count}"
        finally:
            db.close()

    def search_products(self, category: Optional[str] = None, min_price: Optional[float] = None,
                       max_price: Optional[float] = None, name_contains: Optional[str] = None) -> str:
        """Search products by various criteria"""
        db = SessionLocal()
        try:
            query = db.query(Product)

            filters = []
            if category:
                filters.append(Product.category == category)
            if min_price:
                filters.append(Product.price >= min_price)
            if max_price:
                filters.append(Product.price <= max_price)
            if name_contains:
                filters.append(Product.name.ilike(f"%{name_contains}%"))

            if filters:
                query = query.filter(and_(*filters))

            products = query.all()

            if not products:
                return "No products found matching criteria"

            result = f"Found {len(products)} products:\n"
            for product in products:
                result += f"- {product.product_id}: {product.name} - ${product.price} ({product.category})\n"
                result += f"  {product.description}\n"

            return result
        finally:
            db.close()

    def get_ticket_details(self, ticket_id: str) -> str:
        """Get detailed information about a support ticket"""
        db = SessionLocal()
        try:
            ticket = db.query(SupportTicket).options(
                joinedload(SupportTicket.customer),
                joinedload(SupportTicket.order)
            ).filter(SupportTicket.ticket_id == ticket_id).first()

            if not ticket:
                return "Ticket not found"

            details = f"Ticket {ticket.ticket_id}\n"
            details += f"Customer: {ticket.customer.name} ({ticket.customer.email})\n"
            details += f"Order: {ticket.order_id}\n"
            details += f"Issue: {ticket.issue}\n"
            details += f"Status: {ticket.status}\n"
            details += f"Created: {ticket.created_at}\n"

            return details
        finally:
            db.close()

    def search_tickets(self, customer_id: Optional[str] = None, order_id: Optional[str] = None,
                      status: Optional[str] = None, issue_contains: Optional[str] = None) -> str:
        """Search support tickets by various criteria"""
        db = SessionLocal()
        try:
            query = db.query(SupportTicket).options(joinedload(SupportTicket.customer))

            filters = []
            if customer_id:
                filters.append(SupportTicket.customer_id == customer_id)
            if order_id:
                filters.append(SupportTicket.order_id == order_id)
            if status:
                filters.append(SupportTicket.status == status)
            if issue_contains:
                filters.append(SupportTicket.issue.ilike(f"%{issue_contains}%"))

            if filters:
                query = query.filter(and_(*filters))

            tickets = query.all()

            if not tickets:
                return "No tickets found matching criteria"

            result = f"Found {len(tickets)} tickets:\n"
            for ticket in tickets:
                result += f"- {ticket.ticket_id}: {ticket.customer.name}, {ticket.issue} ({ticket.status})\n"

            return result
        finally:
            db.close()

    def get_customer_orders_summary(self, customer_id: str) -> str:
        """Get a summary of all orders for a customer"""
        db = SessionLocal()
        try:
            orders = db.query(Order).options(
                joinedload(Order.items).joinedload(OrderItem.product)
            ).filter(Order.customer_id == customer_id).all()

            if not orders:
                return "No orders found for this customer"

            result = f"Customer {customer_id} - Order Summary:\n"
            total_spent = 0

            for order in orders:
                result += f"\nOrder {order.order_id} ({order.status}) - ${order.total_amount}\n"
                total_spent += order.total_amount
                for item in order.items:
                    result += f"  - {item.product.name} (x{item.quantity})\n"

            result += f"\nTotal spent: ${total_spent}"
            return result
        finally:
            db.close()

    def get_sales_analytics(self) -> str:
        """Get basic sales analytics"""
        db = SessionLocal()
        try:
            # Total orders and revenue
            total_orders = db.query(func.count(Order.order_id)).scalar()
            total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0

            # Orders by status
            status_counts = db.query(Order.status, func.count(Order.order_id)).group_by(Order.status).all()

            # Top products
            top_products = db.query(
                Product.name,
                func.sum(OrderItem.quantity).label('total_quantity')
            ).join(OrderItem).group_by(Product.product_id, Product.name).order_by(
                func.sum(OrderItem.quantity).desc()
            ).limit(5).all()

            result = f"Sales Analytics:\n"
            result += f"Total Orders: {total_orders}\n"
            result += f"Total Revenue: ${total_revenue:.2f}\n\n"
            result += "Orders by Status:\n"
            for status, count in status_counts:
                result += f"  {status}: {count}\n"

            result += "\nTop Products by Quantity Sold:\n"
            for name, qty in top_products:
                result += f"  {name}: {qty}\n"

            return result
        finally:
            db.close()

    def initiate_refund(self, order_id: str, reason: str) -> str:
        """Initiate a refund for an order"""
        db = SessionLocal()
        try:
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if not order:
                return "Order not found"

            if order.status in ["delivered", "cancelled"]:
                order.status = "REFUND_INITIATED"
                db.commit()
                return f"Refund initiated for {order_id}. Reason: {reason}"

            return f"Refund not allowed. Current status: {order.status}"
        finally:
            db.close()

    def create_ticket(self, customer_id: str, order_id: str, issue: str) -> str:
        """Create a new support ticket"""
        db = SessionLocal()
        try:
            ticket = SupportTicket(
                ticket_id=str(uuid.uuid4()),
                customer_id=customer_id,
                order_id=order_id,
                issue=issue,
                status="open",
                created_at=datetime.utcnow()
            )
            db.add(ticket)
            db.commit()
            return f"Ticket created: {ticket.ticket_id}"
        finally:
            db.close()

    def update_ticket_status(self, ticket_id: str, new_status: str) -> str:
        """Update the status of a support ticket"""
        db = SessionLocal()
        try:
            ticket = db.query(SupportTicket).filter(SupportTicket.ticket_id == ticket_id).first()
            if not ticket:
                return "Ticket not found"

            valid_statuses = ["open", "in_progress", "resolved", "closed"]
            if new_status not in valid_statuses:
                return f"Invalid status. Valid statuses: {', '.join(valid_statuses)}"

            ticket.status = new_status
            db.commit()
            return f"Ticket {ticket_id} status updated to {new_status}"
        finally:
            db.close()

    def insert_mock_data(self, data_type: str, data: Dict[str, Any]) -> str:
        """Insert mock data into the database"""
        db = SessionLocal()
        try:
            if data_type == "customer":
                customer = Customer(**data)
                db.add(customer)
            elif data_type == "product":
                product = Product(**data)
                db.add(product)
            elif data_type == "order":
                order = Order(**data)
                db.add(order)
            elif data_type == "order_item":
                item = OrderItem(**data)
                db.add(item)
            elif data_type == "ticket":
                ticket = SupportTicket(**data)
                db.add(ticket)
            else:
                return f"Unknown data type: {data_type}"

            db.commit()
            return f"Mock {data_type} data inserted successfully"
        except Exception as e:
            db.rollback()
            return f"Error inserting data: {str(e)}"
        finally:
            db.close()

    def general_query(self, query_type: str, **kwargs) -> str:
        """General query tool for complex data retrieval"""
        db = SessionLocal()
        try:
            if query_type == "customer_orders_with_items":
                customer_id = kwargs.get("customer_id")
                orders = db.query(Order).options(
                    joinedload(Order.items).joinedload(OrderItem.product)
                ).filter(Order.customer_id == customer_id).all()

                result = f"Orders for customer {customer_id}:\n"
                for order in orders:
                    result += f"\nOrder {order.order_id} ({order.status}):\n"
                    for item in order.items:
                        result += f"  - {item.product.name} x{item.quantity} @ ${item.unit_price}\n"
                return result

            elif query_type == "product_sales":
                product_id = kwargs.get("product_id")
                sales = db.query(
                    func.sum(OrderItem.quantity).label('total_sold'),
                    func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue')
                ).filter(OrderItem.product_id == product_id).first()

                if sales.total_sold:
                    return f"Product {product_id}: {sales.total_sold} sold, Revenue: ${sales.total_revenue:.2f}"
                return f"No sales data for product {product_id}"

            elif query_type == "recent_tickets":
                limit = kwargs.get("limit", 10)
                tickets = db.query(SupportTicket).options(
                    joinedload(SupportTicket.customer)
                ).order_by(SupportTicket.created_at.desc()).limit(limit).all()

                result = f"Recent {len(tickets)} tickets:\n"
                for ticket in tickets:
                    result += f"- {ticket.ticket_id}: {ticket.customer.name} - {ticket.issue} ({ticket.status})\n"
                return result

            else:
                return f"Unknown query type: {query_type}"
        finally:
            db.close()
