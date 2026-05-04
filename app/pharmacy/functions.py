"""Pharmacy business logic functions.

Implements all pharmacy operations: drug information retrieval, order placement,
and order lookup. These functions are called by the Deepgram agent via the
function dispatcher.
"""

from .data import ORDERS_DB, DRUG_DB


def get_drug_info(drug_name):
    """Get drug information.
    
    Args:
        drug_name: Name of the drug to look up (case-insensitive).
        
    Returns:
        Dictionary containing drug information or error message.
    """
    drug = DRUG_DB.get(drug_name.lower())
    if drug:
        return {
            "name": drug["name"],
            "description": drug["description"],
            "price": drug["price"],
            "quantity": drug["quantity"]
        }
    return {"error": f"Drug '{drug_name}' not found"}


def place_order(customer_name, drug_name):
    """Place a simple order with predefined quantity.
    
    Args:
        customer_name: Full name of the customer placing the order.
        drug_name: Name of the drug to order (case-insensitive).
        
    Returns:
        Dictionary containing order confirmation or error message.
    """
    drug = DRUG_DB.get(drug_name.lower())
    if not drug:
        return {"error": f"Drug '{drug_name}' not found"}

    order_id = ORDERS_DB["next_id"]
    ORDERS_DB["next_id"] += 1

    order = {
        "id": order_id,
        "customer": customer_name,
        "drug": drug["name"],
        "quantity": drug["quantity"],
        "total": drug["price"],
        "status": "pending"
    }
    ORDERS_DB["orders"][order_id] = order

    return {
        "order_id": order_id,
        "message": f"Order {order_id} placed: {drug['quantity']} {drug['name']} for ${order['total']:.2f}",
        "total": order['total'],
        "quantity": drug['quantity']
    }


def lookup_order(order_id):
    """Look up an order by ID.
    
    Args:
        order_id: The order ID to look up.
        
    Returns:
        Dictionary containing order details or error message.
    """
    order = ORDERS_DB["orders"].get(int(order_id))
    if order:
        return {
            "order_id": order_id,
            "customer": order["customer"],
            "drug": order["drug"],
            "quantity": order["quantity"],
            "total": order["total"],
            "status": order["status"]
        }
    return {"error": f"Order {order_id} not found"}


# Function mapping dictionary - used by the function dispatcher
FUNCTION_MAP = {
    'get_drug_info': get_drug_info,
    'place_order': place_order,
    'lookup_order': lookup_order
}
