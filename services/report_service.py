#!/usr/bin/env python3
"""
Report Service
Generates financial reports and analytics

TODO: Complete the report generation methods
"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from models.transaction import Transaction
from models.category import Category
from services.transaction_service import TransactionService
from utils.formatters import format_currency, format_date

class ReportService:
    """
    Service class for generating financial reports
    """
    
    @staticmethod
    def generate_balance_report():
        """
        Generate a balance report showing current financial status
        
        Returns:
            str: Formatted balance report
        """
        print("📊 Generating Balance Report...")
        
        # TODO: Get transaction summary
        summary = TransactionService.get_transaction_summary()
        
        income = summary.get('total_income', Decimal('0'))
        expenses = summary.get('total_expenses', Decimal('0'))
        balance = income - expenses
        
        report = []
        report.append("\n" + "=" * 50)
        report.append("💰 PERSONAL BUDGET BALANCE REPORT")
        report.append("=" * 50)
        
        # TODO: Add balance information to report
        # Format currency amounts nicely
        # Show income, expenses, and net balance
        
        report.append(f"\n💵 Total Income:   {format_currency(income)}")
        report.append(f"💸 Total Expenses: {format_currency(expenses)}")
        report.append(f"📊 Net Balance:    {format_currency(balance)}")
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_category_report(transaction_type='expense', top_n=10):
        """
        Generate a report showing spending/income by category
        
        Args:
            transaction_type (str): 'income' or 'expense'
            top_n (int): Number of top categories to show
            
        Returns:
            str: Formatted category report
        """
        print(f"🏷️  Generating {transaction_type.title()} by Category Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📋 {transaction_type.upper()} BY CATEGORY REPORT")
        report.append("=" * 50)
        
        # TODO: Get category spending data
        category_data = TransactionService.get_spending_by_category(transaction_type)
        
        # TODO: Sort categories by amount (highest first)
        # Show top N categories with percentages
        
        category_data = sorted(category_data, key=lambda x: x['total'], reverse=True)

        total = sum(c['total'] for c in category_data) or Decimal('1')

        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📋 {transaction_type.upper()} BY CATEGORY REPORT")
        report.append("=" * 50)

        for cat in category_data[:top_n]:
            percent = (cat['total'] / total) * 100
            report.append(
                f"{cat['category_name']:<20} "
                f"{format_currency(cat['total']):>10} "
                f"({percent:.1f}%)"
            )
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_monthly_report(year=None, month=None):
        """
        Generate a monthly financial report
        
        Args:
            year (int, optional): Year (default: current)
            month (int, optional): Month (default: current)
            
        Returns:
            str: Formatted monthly report
        """
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
            
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        print(f"📅 Generating {month_names[month-1]} {year} Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📅 MONTHLY REPORT - {month_names[month-1].upper()} {year}")
        report.append("=" * 50)
        
        # TODO: Get monthly data
        # monthly_data = TransactionService.get_monthly_summary(year, month)
        
        # TODO: Add monthly statistics
        # - Total income for month
        # - Total expenses for month
        # - Net change
        # - Number of transactions
        # - Average transaction size
        # - Top spending categories

        monthly_data = TransactionService.get_monthly_summary(year, month)

        income = monthly_data.get('income', Decimal('0'))
        expenses = monthly_data.get('expenses', Decimal('0'))
        count = monthly_data.get('count', 0)

        net = income - expenses
        avg = (income + expenses) / count if count else Decimal('0')

        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📅 MONTHLY REPORT - {month}/{year}")
        report.append("=" * 50)

        report.append(f"\n💵 Income:        {format_currency(income)}")
        report.append(f"💸 Expenses:      {format_currency(expenses)}")
        report.append(f"📊 Net Change:    {format_currency(net)}")
        report.append(f"🔢 Transactions:  {count}")
        report.append(f"📈 Avg Size:      {format_currency(avg)}")
        
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_trend_report(days=30):
        """
        Generate a trend report for recent activity
        
        Args:
            days (int): Number of days to analyze
            
        Returns:
            str: Formatted trend report
        """
        print(f"📈 Generating {days}-Day Trend Report...")
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📈 FINANCIAL TREND REPORT ({days} DAYS)")
        report.append("=" * 50)
        report.append(f"Period: {format_date(start_date)} to {format_date(end_date)}")
        report.append("")
        
        # TODO: Get transactions for date range
        # Use Transaction.get_by_date_range()
        transactions = Transaction.get_by_date_range(start_date, end_date)

        # TODO: Calculate trends
        # - Daily average spending
        # - Most active spending days
        # - Trend direction (spending increasing/decreasing)
        
        total = sum(t.amount for t in transactions)
        avg = total / len(transactions) if transactions else Decimal('0')

        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📈 TREND REPORT ({days} DAYS)")
        report.append("=" * 50)

        report.append(f"Period: {format_date(start_date)} → {format_date(end_date)}")
        report.append(f"Total Activity: {format_currency(total)}")
        report.append(f"Daily Avg: {format_currency(avg)}")
        report.append(f"Transactions: {len(transactions)}")
        
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_summary_dashboard():
        """
        Generate a comprehensive dashboard with key metrics
        
        Returns:
            str: Formatted dashboard
        """
        print("📊 Generating Financial Dashboard...")
        
        summary = TransactionService.get_transaction_summary()
        balance = summary['total_income'] - summary['total_expenses']

        # Extra data
        expense_categories = TransactionService.get_spending_by_category('expense')
        recent_transactions = Transaction.get_by_date_range(
            date.today() - timedelta(days=7),
            date.today()
    )
        
        health = ReportService.generate_budget_health_score()

        dashboard = []
        dashboard.append("\n" + "=" * 60)
        dashboard.append("📊 PERSONAL BUDGET TRACKER DASHBOARD")
        dashboard.append("=" * 60)
        
        # TODO: Get comprehensive data
        # summary = TransactionService.get_transaction_summary()
        # expense_categories = TransactionService.get_spending_by_category('expense')
        # income_categories = TransactionService.get_spending_by_category('income')

        # 1. Balance Overview
        dashboard.append("\n💰 BALANCE OVERVIEW")
        dashboard.append(f"   Balance:  {format_currency(balance)}")
        dashboard.append(f"   Income:   {format_currency(summary['total_income'])}")
        dashboard.append(f"   Expenses: {format_currency(summary['total_expenses'])}")

    # 2. Recent Activity
        dashboard.append("\n🕒 RECENT ACTIVITY (7 DAYS)")
        if recent_transactions:
            for t in recent_transactions[:5]:
                dashboard.append(f"   {t}")
        else:
            dashboard.append("   No recent transactions")

    # 3. Top Categories
        dashboard.append("\n🏷️ TOP SPENDING CATEGORIES")
        sorted_categories = sorted(
            expense_categories,
            key=lambda x: x['total'],
            reverse=True
        )

        for cat in sorted_categories[:3]:
          dashboard.append(
            f"   {cat['category_name']}: {format_currency(cat['total'])}"
        )

    # 4. Health Score
        dashboard.append("\n📊 BUDGET HEALTH")
        dashboard.append(f"   Score: {health['score']} ({health['grade']})")

        dashboard.append(f"\n💰 Balance: {format_currency(balance)}")
        dashboard.append(f"💵 Income:  {format_currency(summary['total_income'])}")
        dashboard.append(f"💸 Expenses:{format_currency(summary['total_expenses'])}")
        
        # TODO: Create dashboard sections:
        # 1. Current Balance Overview
        # 2. Recent Activity (last 7 days)
        # 3. Top Spending Categories
        # 4. Budget Health Indicators
        
        dashboard.append("\n📝 QUICK ACTIONS:")
        dashboard.append("   1. Add New Transaction")
        dashboard.append("   2. View Recent Transactions")
        dashboard.append("   3. Generate Detailed Reports")
        dashboard.append("   4. Manage Categories")
        
        dashboard.append("\nGenerated: " + format_date(date.today()))
        dashboard.append("=" * 60)
        
        return "\n".join(dashboard)
    
    @staticmethod
    def generate_budget_health_score():
        """
        Calculate and return a budget health score (0-100)
        
        Returns:
            dict: Health score and breakdown
        """
        # TODO: Implement budget health calculation
        # Consider factors like:
        # - Income vs expenses ratio
        # - Savings rate (if income > expenses)
        # - Spending consistency
        # - Emergency fund equivalent
        
        summary = TransactionService.get_transaction_summary()

        income = summary.get('total_income', Decimal('0'))
        expenses = summary.get('total_expenses', Decimal('0'))
        
        health_data = {
            'score': 0,  # 0-100
            'grade': 'F',  # A, B, C, D, F
            'factors': {
                'income_stability': 0,
                'expense_control': 0,
                'savings_rate': 0,
                'budget_balance': 0
            },
            'recommendations': []
        }
        
        # TODO: Calculate actual score based on financial data
        if income == 0:
            health_data['recommendations'].append("Increase income sources")
            return health_data

        savings_rate = (income - expenses) / income
        expense_ratio = expenses / income

        # Scoring logic
        score = 0

        # Savings rate (40 pts)
        if savings_rate >= 0.2:
            score += 40
        elif savings_rate >= 0.1:
            score += 25
        elif savings_rate > 0:
            score += 10

        # Expense control (30 pts)
        if expense_ratio < 0.7:
            score += 30
        elif expense_ratio < 0.9:
            score += 20
        else:
            score += 5

        # Basic balance (30 pts)
        if income > expenses:
            score += 30

        # Grade
        if score >= 90:
            grade = 'A'
        elif score >= 75:
            grade = 'B'
        elif score >= 60:
            grade = 'C'
        elif score >= 50:
            grade = 'D'
        else:
            grade = 'F'

        # Recommendations
        if expenses > income:
            health_data['recommendations'].append("Reduce expenses")
        if savings_rate < 0.1:
            health_data['recommendations'].append("Increase savings rate")

        health_data['score'] = score
        health_data['grade'] = grade
        health_data['factors'] = {
            'savings_rate': float(savings_rate),
            'expense_ratio': float(expense_ratio)
        }

        return health_data
    
    @staticmethod
    def export_report_to_file(report_content, filename):
        """
        Export report content to a text file
        
        Args:
            report_content (str): Report content
            filename (str): Output filename
            
        Returns:
            bool: True if successful
        """
        try:
            # TODO: Write report to file
            # Use context managers for file operations
            
            with open(filename, 'w') as f:
                f.write(report_content)
        
            print(f"✅ Report exported to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
            return False

def main():
    """
    Test the ReportService
    """
    print("📈 Testing Report Service")
    print("=" * 30)
    
    # Test dashboard generation
    dashboard = ReportService.generate_summary_dashboard()
    print(dashboard)
    
    # Test balance report
    balance_report = ReportService.generate_balance_report()
    print(balance_report)
    
    print("\n💡 Complete the TODO sections to see full reports!")

if __name__ == "__main__":
    main()