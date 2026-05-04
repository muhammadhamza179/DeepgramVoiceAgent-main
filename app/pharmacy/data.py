"""Mock pharmacy databases.

Contains in-memory storage for drug inventory and orders.
In a production environment, these would be replaced with a real database.
"""

# Simple in-memory storage for orders
ORDERS_DB = {"orders": {}, "next_id": 1}

# Drug inventory database
DRUG_DB = {
    "aspirin": {
        "name": "Acetylsalicylic Acid",
        "price": 5.99,
        "description": "Non-steroidal anti-inflammatory drug for pain relief and fever reduction",
        "quantity": 30
    },
    "ibuprofen": {
        "name": "Ibuprofen",
        "price": 7.99,
        "description": "Anti-inflammatory medication for pain and inflammation management",
        "quantity": 20
    },
    "acetaminophen": {
        "name": "Acetaminophen",
        "price": 6.99,
        "description": "Analgesic and antipyretic medication for pain and fever control",
        "quantity": 25
    },
    "metformin": {
        "name": "Metformin Hydrochloride",
        "price": 12.50,
        "description": "Biguanide antidiabetic medication for type 2 diabetes management",
        "quantity": 60
    },
    "lisinopril": {
        "name": "Lisinopril",
        "price": 8.75,
        "description": "ACE inhibitor for hypertension and heart failure treatment",
        "quantity": 30
    },
    "atorvastatin": {
        "name": "Atorvastatin Calcium",
        "price": 15.25,
        "description": "HMG-CoA reductase inhibitor for cholesterol management",
        "quantity": 30
    },
    "omeprazole": {
        "name": "Omeprazole",
        "price": 11.99,
        "description": "Proton pump inhibitor for acid reflux and ulcer treatment",
        "quantity": 28
    },
    "amlodipine": {
        "name": "Amlodipine Besylate",
        "price": 9.50,
        "description": "Calcium channel blocker for hypertension and angina",
        "quantity": 30
    },
    "metoprolol": {
        "name": "Metoprolol Tartrate",
        "price": 7.25,
        "description": "Beta-blocker for hypertension and heart rhythm disorders",
        "quantity": 30
    },
    "sertraline": {
        "name": "Sertraline Hydrochloride",
        "price": 13.75,
        "description": "Selective serotonin reuptake inhibitor for depression and anxiety",
        "quantity": 30
    }
}
