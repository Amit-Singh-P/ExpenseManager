import requests
from decimal import Decimal
from django.core.cache import cache

def get_countries_with_currencies():
    """Fetch countries and their currencies from REST Countries API"""
    cache_key = 'countries_currencies'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        response = requests.get('https://restcountries.com/v3.1/all?fields=name,currencies', timeout=10)
        response.raise_for_status()
        data = response.json()
        
        countries = []
        for country in data:
            if 'currencies' in country and country['currencies']:
                currency_code = list(country['currencies'].keys())[0]
                country_name = country['name']['common']
                countries.append({
                    'name': country_name,
                    'currency': currency_code
                })
        
        countries.sort(key=lambda x: x['name'])
        cache.set(cache_key, countries, 86400)  # Cache for 24 hours
        return countries
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return []

def convert_currency(amount, from_currency, to_currency):
    """Convert currency using exchange rate API"""
    if from_currency == to_currency:
        return amount
    
    cache_key = f'exchange_rate_{from_currency}_{to_currency}'
    cached_rate = cache.get(cache_key)
    
    if cached_rate:
        return Decimal(str(amount)) * Decimal(str(cached_rate))
    
    try:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_currency}', timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if to_currency in data['rates']:
            rate = data['rates'][to_currency]
            cache.set(cache_key, rate, 3600)  # Cache for 1 hour
            return Decimal(str(amount)) * Decimal(str(rate))
    except Exception as e:
        print(f"Currency conversion error: {e}")
    
    return amount

def get_applicable_approval_rule(company, amount):
    """Get the applicable approval rule for an expense"""
    from .models import ApprovalRule
    
    rules = ApprovalRule.objects.filter(
        company=company,
        is_active=True
    ).order_by('-min_amount')
    
    for rule in rules:
        if rule.min_amount is None or amount >= rule.min_amount:
            if rule.max_amount is None or amount <= rule.max_amount:
                return rule
    
    return None

def process_approval_workflow(expense):
    """Process the approval workflow for an expense"""
    from .models import ExpenseApproval, ApprovalStep
    
    rule = get_applicable_approval_rule(expense.company, expense.converted_amount or expense.amount)
    
    if not rule:
        expense.status = 'approved'
        expense.save()
        return
    
    # Get approval steps
    steps = rule.steps.all().order_by('step_number')
    
    if rule.is_manager_approver and expense.employee.manager:
        # First approval is by manager
        ExpenseApproval.objects.create(
            expense=expense,
            approver=expense.employee.manager,
            step_number=0,
            status='pending'
        )
        expense.current_approver = expense.employee.manager
        expense.current_step = 0
    elif steps.exists():
        # Start with first step in the rule
        first_step = steps.first()
        approver = first_step.approver or get_approver_by_role(expense.company, first_step.approver_role)
        
        if approver:
            ExpenseApproval.objects.create(
                expense=expense,
                approver=approver,
                step_number=1,
                status='pending'
            )
            expense.current_approver = approver
            expense.current_step = 1
    
    expense.status = 'in_progress'
    expense.save()

def get_approver_by_role(company, role):
    """Get an approver by role"""
    from .models import User
    users = User.objects.filter(company=company, role=role)
    return users.first() if users.exists() else None