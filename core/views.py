from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from .models import User, Company, ContactMessage
from .forms import RegistrationForm, LoginForm, UserForm, CompanyForm, ContactForm
import json


def index(request):
    """Landing page view"""
    return render(request, 'index.html')


def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            currency = data.get('country')
            
            # Check if user exists
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Username or email already exists!'
                })
            
            # Create admin user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='admin',
                first_name=username
            )
            
            # Create company
            company = Company.objects.create(
                name=f"{username}'s Company",
                currency=currency,
                admin=user
            )
            
            # Login user
            login(request, user)
            
            return JsonResponse({
                'success': True,
                'message': 'Registration successful!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'role': user.role,
                    'name': user.get_full_name() or user.username
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid credentials'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out successfully'})


def contact_view(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
            
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We will get back to you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def dashboard_view(request):
    """Admin dashboard view"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('index')
    
    try:
        company = Company.objects.get(admin=request.user)
    except Company.DoesNotExist:
        # Create company if doesn't exist
        company = Company.objects.create(
            name=f"{request.user.username}'s Company",
            currency='USD',
            admin=request.user
        )
    
    context = {
        'company': company,
        'total_employees': User.objects.filter(role='employee').count(),
        'total_managers': User.objects.filter(role='manager').count(),
        'total_users': User.objects.count(),
        'recent_users': User.objects.all()[:5]
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def get_company_data(request):
    """Get company data as JSON"""
    try:
        company = Company.objects.get(admin=request.user)
        return JsonResponse({
            'success': True,
            'company': {
                'name': company.name,
                'currency': company.currency,
                'address': company.address or '',
                'phone': company.phone or ''
            }
        })
    except Company.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Company not found'
        })


@login_required
def get_users_data(request):
    """Get all users data as JSON"""
    users = User.objects.all().select_related('manager')
    users_data = []
    
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.get_full_name() or user.username,
            'role': user.role,
            'managerId': user.manager.id if user.manager else None,
            'managerName': user.manager.get_full_name() if user.manager else None,
            'teamSize': user.get_team_size()
        })
    
    return JsonResponse({
        'success': True,
        'users': users_data
    })


@login_required
def get_dashboard_stats(request):
    """Get dashboard statistics"""
    return JsonResponse({
        'success': True,
        'stats': {
            'employees': User.objects.filter(role='employee').count(),
            'managers': User.objects.filter(role='manager').count(),
            'total': User.objects.count()
        }
    })


@login_required
def create_user(request):
    """Create new user (employee or manager)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Check if email exists
            if User.objects.filter(email=data.get('email')).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Email already exists'
                })
            
            # Create user
            user = User.objects.create_user(
                username=data.get('email').split('@')[0],
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('name').split()[0],
                last_name=' '.join(data.get('name').split()[1:]) if len(data.get('name').split()) > 1 else '',
                role=data.get('role')
            )
            
            # Set manager if provided
            if data.get('managerId'):
                user.manager = User.objects.get(id=data.get('managerId'))
                user.save()
            
            return JsonResponse({
                'success': True,
                'message': f"{data.get('role').capitalize()} created successfully",
                'user': {
                    'id': user.id,
                    'name': user.get_full_name(),
                    'email': user.email,
                    'role': user.role
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def update_user(request, user_id):
    """Update existing user"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, id=user_id)
            
            # Update user fields
            user.first_name = data.get('name').split()[0]
            user.last_name = ' '.join(data.get('name').split()[1:]) if len(data.get('name').split()) > 1 else ''
            user.email = data.get('email')
            user.role = data.get('role')
            
            if data.get('password'):
                user.set_password(data.get('password'))
            
            if data.get('managerId'):
                user.manager = User.objects.get(id=data.get('managerId'))
            else:
                user.manager = None
            
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'User updated successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def delete_user(request, user_id):
    """Delete user"""
    if request.method == 'DELETE':
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Don't allow deleting own account
            if user.id == request.user.id:
                return JsonResponse({
                    'success': False,
                    'message': 'Cannot delete your own account'
                })
            
            user.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'User deleted successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def update_company(request):
    """Update company settings"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company = Company.objects.get(admin=request.user)
            
            company.name = data.get('name')
            company.currency = data.get('currency')
            company.address = data.get('address', '')
            company.phone = data.get('phone', '')
            company.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Company settings updated successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})