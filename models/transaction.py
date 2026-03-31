#!/usr/bin/env python3
"""
Transaction Model
Handles transaction data operations and validation

TODO: Complete the Transaction class with CRUD operations
"""

from datetime import date, datetime
from decimal import Decimal
from database.connection import DatabaseConnection

class Transaction:
    """
    Represents a financial transaction (income or expense)
    """
    
    def __init__(self, amount=None, description=None, transaction_date=None, 
                 category_id=None, transaction_type=None, transaction_id=None):
        """
        Initialize a transaction
        
        Args:
            amount (Decimal): Transaction amount
            description (str): Transaction description
            transaction_date (date): Date of transaction
            category_id (int): Category ID
            transaction_type (str): 'income' or 'expense'
            transaction_id (int): Database ID (for existing transactions)
        """
        self.id = transaction_id
        self.amount = amount
        self.description = description
        self.transaction_date = transaction_date
        self.category_id = category_id
        self.type = transaction_type
        self.db = DatabaseConnection()
    
    def save(self):
        """
        Save transaction to database (INSERT or UPDATE)
        
        Returns:
            bool: True if successful, False otherwise
        """
        # TODO: Implement save method
        # If self.id exists, UPDATE existing transaction
        # If self.id is None, INSERT new transaction
        
        if not self.validate():
            return False
            
        if not self.db.connect():
            return False        
        try:
            if self.id:
                # TODO: UPDATE existing transaction
                # Write SQL UPDATE query
                # Use self.db.execute_update() with parameters
                query = """
                UPDATE transactions
                SET amount = %s,
                    description = %s,
                    transaction_date = %s,
                    category_id = %s,
                    type = %s
                WHERE id = %s
                """
                return self.db.execute_update(query, (
                    self.amount,
                    self.description,
                    self.transaction_date,
                    self.category_id,
                    self.type,
                    self.id
                ))
            else:
                # TODO: INSERT new transaction
                # Write SQL INSERT query with RETURNING id
                # Use self.db.execute_query() to get the new ID
                # Set self.id to the returned ID
                query = """
            INSERT INTO transactions (amount, description, transaction_date, category_id, type)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """
            result = self.db.execute_query(query, (
                self.amount,
                self.description,
                self.transaction_date,
                self.category_id,
                self.type
            ))

            if result:
                self.id = result[0]['id']
                return True
            return False
                
        except Exception as e:
            print(f"❌ Error saving transaction: {e}")
            return False
        finally:
            self.db.disconnect()
        
        return True
    
    def delete(self):
        """
        Delete transaction from database
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.id:
            print("❌ Cannot delete transaction without ID")
            return False
            
        # TODO: Implement delete method
        # Write SQL DELETE query
        # Use self.db.execute_update()
        
        if not self.db.connect():
            return False

        try:
            query = "DELETE FROM transactions WHERE id = %s"
            return self.db.execute_update(query, (self.id,))
        finally:
            self.db.disconnect()
    
    def validate(self):
        """
        Validate transaction data
        
        Returns:
            bool: True if valid, False otherwise
        """
        # TODO: Implement validation
        # Check that:
        # - amount is positive Decimal or float
        # - description is not empty
        # - transaction_date is a valid date
        # - type is 'income' or 'expense'
        # - category_id exists in database (optional check)
        
        
        if self.amount is None:
            print("❌ Amount is required")
            return False

        try:
            self.amount = Decimal(self.amount)
            if self.amount <= 0:
                print("❌ Amount must be positive")
                return False
        except:
            print("❌ Invalid amount")
            return False

        if not self.description or not self.description.strip():
            print("❌ Description cannot be empty")
            return False

        if not isinstance(self.transaction_date, date):
            print("❌ Invalid date")
            return False

        if self.type not in ['income', 'expense']:
            print("❌ Type must be 'income' or 'expense'")
            return False

        return True   
     
    @staticmethod
    def get_all():
        """
        Get all transactions from database
        
        Returns:
            list: List of Transaction objects
        """
        db = DatabaseConnection()
        if not db.connect():
            return []

        # TODO: Write SQL query to get all transactions
        # JOIN with categories to get category name
        # Order by transaction_date DESC
        
        query = """
        SELECT t.id, t.amount, t.description, t.transaction_date,
            t.type, t.category_id, c.name AS category_name
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        ORDER BY t.transaction_date DESC
        """
        
        results = db.execute_query(query)
        db.disconnect()
        
        transactions = []
        # TODO: Convert database results to Transaction objects
        # Loop through results and create Transaction instances
        for row in results:
            transactions.append(Transaction(
                amount=row['amount'],
                description=row['description'],
                transaction_date=row['transaction_date'],
                category_id=row['category_id'],
                transaction_type=row['type'],
                transaction_id=row['id']
            ))
        return transactions
    
    @staticmethod
    def get_by_id(transaction_id):
        """
        Get transaction by ID
        
        Args:
            transaction_id (int): Transaction ID
            
        Returns:
            Transaction: Transaction object or None if not found
        """
        # TODO: Implement get_by_id
        # Similar to get_all() but with WHERE clause
        
        db = DatabaseConnection()
        if not db.connect():
            return None

        query = """
        SELECT id, amount, description, transaction_date, category_id, type
        FROM transactions
        WHERE id = %s
        """

        result = db.execute_query(query, (transaction_id,))
        db.disconnect()

        if result:
            row = result[0]
            return Transaction(
                amount=row['amount'],
                description=row['description'],
                transaction_date=row['transaction_date'],
                category_id=row['category_id'],
                transaction_type=row['type'],
                transaction_id=row['id']
            )

        return None
    
    @staticmethod
    def get_by_type(transaction_type):
        """
        Get transactions by type (income or expense)
        
        Args:
            transaction_type (str): 'income' or 'expense'
            
        Returns:
            list: List of Transaction objects
        """
        # TODO: Implement filtering by type
        # Similar to get_all() but with WHERE type = %s
        
        db = DatabaseConnection()
        if not db.connect():
            return []

        query = """
        SELECT id, amount, description, transaction_date, category_id, type
        FROM transactions
        WHERE type = %s
        ORDER BY transaction_date DESC
        """

        results = db.execute_query(query, (transaction_type,))
        db.disconnect()

        return [
            Transaction(
                amount=row['amount'],
                description=row['description'],
                transaction_date=row['transaction_date'],
                category_id=row['category_id'],
                transaction_type=row['type'],
                transaction_id=row['id']
            )
            for row in results
        ]
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        """
        Get transactions within date range
        
        Args:
            start_date (date): Start date
            end_date (date): End date
            
        Returns:
            list: List of Transaction objects
        """
        # TODO: Implement date range filtering
        # Similar to get_all() but with WHERE transaction_date BETWEEN %s AND %s
        
        db = DatabaseConnection()
        if not db.connect():
            return []

        query = """
        SELECT id, amount, description, transaction_date, category_id, type
        FROM transactions
        WHERE transaction_date BETWEEN %s AND %s
        ORDER BY transaction_date DESC
        """

        results = db.execute_query(query, (start_date, end_date))
        db.disconnect()

        return [
        Transaction(
            amount=row['amount'],
            description=row['description'],
            transaction_date=row['transaction_date'],
            category_id=row['category_id'],
            transaction_type=row['type'],
            transaction_id=row['id']
            )
            for row in results
        ]
    
    def __str__(self):
        """
        String representation of transaction
        """
        return f"{self.type.title()}: ${self.amount} - {self.description} ({self.transaction_date})"
    
    def __repr__(self):
        """
        Developer-friendly representation
        """
        return f"Transaction(id={self.id}, amount={self.amount}, type='{self.type}', date='{self.transaction_date}')"

def main():
    """
    Test the Transaction model
    """
    print("💰 Testing Transaction Model")
    print("=" * 30)
    
    # Test creating a new transaction
    transaction = Transaction(
        amount=Decimal('25.50'),
        description="Coffee and pastry",
        transaction_date=date.today(),
        category_id=4,  # Food category from seed data
        transaction_type="expense"
    )
    
    print(f"Created transaction: {transaction}")
    
    # Test validation (when implemented)
    if transaction.validate():
        print("✅ Transaction is valid")
    else:
        print("❌ Transaction validation failed")
    
    # Test getting all transactions  
    print("\n📋 All transactions:")
    all_transactions = Transaction.get_all()
    for t in all_transactions[:5]:  # Show first 5
        print(f"  {t}")
    
    print(f"\n📊 Found {len(all_transactions)} total transactions")

if __name__ == "__main__":
    main()