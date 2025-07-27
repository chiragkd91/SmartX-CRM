from app import db
from app.models.crm import Account, Contact, Opportunity, Activity, Territory, User
from datetime import datetime
from sqlalchemy import func, and_, or_
import json

class AccountService:
    """Service for managing accounts with CRUD operations"""
    
    def create_account(self, account_data):
        """Create a new account"""
        try:
            # Validate required fields
            if 'name' not in account_data or not account_data['name']:
                return {'success': False, 'error': 'Account name is required'}
            
            # Check if account name already exists
            existing_account = Account.query.filter_by(name=account_data['name']).first()
            if existing_account:
                return {'success': False, 'error': 'Account with this name already exists'}
            
            # Create new account
            account = Account(
                name=account_data['name'],
                industry=account_data.get('industry'),
                website=account_data.get('website'),
                phone=account_data.get('phone'),
                email=account_data.get('email'),
                address=account_data.get('address'),
                city=account_data.get('city'),
                state=account_data.get('state'),
                country=account_data.get('country'),
                postal_code=account_data.get('postal_code'),
                annual_revenue=account_data.get('annual_revenue'),
                employee_count=account_data.get('employee_count'),
                status=account_data.get('status', 'Active'),
                type=account_data.get('type'),
                parent_account_id=account_data.get('parent_account_id'),
                territory_id=account_data.get('territory_id'),
                assigned_to=account_data.get('assigned_to')
            )
            
            db.session.add(account)
            db.session.commit()
            
            return {'success': True, 'data': account, 'message': 'Account created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_account(self, account_id):
        """Get an account by ID"""
        try:
            account = Account.query.get(account_id)
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            return {'success': True, 'data': account}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_accounts(self, filters=None, page=1, per_page=20):
        """Get accounts with optional filtering and pagination"""
        try:
            query = Account.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Apply pagination
            accounts = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            return {
                'success': True, 
                'data': {
                    'accounts': accounts.items,
                    'total': accounts.total,
                    'pages': accounts.pages,
                    'current_page': accounts.page,
                    'per_page': accounts.per_page
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_account(self, account_id, update_data):
        """Update an account"""
        try:
            account = Account.query.get(account_id)
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(account, field) and field not in ['id', 'created_at']:
                    setattr(account, field, value)
            
            account.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'data': account, 'message': 'Account updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def delete_account(self, account_id):
        """Delete an account"""
        try:
            account = Account.query.get(account_id)
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            db.session.delete(account)
            db.session.commit()
            
            return {'success': True, 'message': 'Account deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def manage_account_hierarchy(self, account_id, hierarchy_data):
        """Manage account hierarchy"""
        try:
            account = Account.query.get(account_id)
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            # Update parent account
            if 'parent_account_id' in hierarchy_data:
                account.parent_account_id = hierarchy_data['parent_account_id']
            
            # Update child accounts
            if 'child_account_ids' in hierarchy_data:
                for child_id in hierarchy_data['child_account_ids']:
                    child_account = Account.query.get(child_id)
                    if child_account:
                        child_account.parent_account_id = account_id
            
            db.session.commit()
            
            return {'success': True, 'data': account, 'message': 'Account hierarchy updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def track_account_relationships(self, account_id, relationship_data):
        """Track account relationships"""
        try:
            account = Account.query.get(account_id)
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            # This would typically involve creating relationship records
            # For now, we'll just update the account with relationship notes
            
            current_notes = account.notes or ""
            relationship_notes = f"\nRelationship Update: {relationship_data.get('description', '')}"
            account.notes = current_notes + relationship_notes
            
            db.session.commit()
            
            return {'success': True, 'data': account, 'message': 'Account relationships updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def manage_account_territories(self, account_id, territory_data):
        """Manage account territories"""
        try:
            account = Account.query.get(account_id)
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            # Update territory assignment
            if 'territory_id' in territory_data:
                account.territory_id = territory_data['territory_id']
            
            db.session.commit()
            
            return {'success': True, 'data': account, 'message': 'Account territory updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def import_accounts(self, file_data):
        """Import accounts from file"""
        try:
            imported_count = 0
            errors = []
            
            for row in file_data:
                try:
                    result = self.create_account(row)
                    if result['success']:
                        imported_count += 1
                    else:
                        errors.append(f"Row {row}: {result['error']}")
                except Exception as e:
                    errors.append(f"Row {row}: {str(e)}")
            
            return {
                'success': True,
                'data': {
                    'imported_count': imported_count,
                    'error_count': len(errors),
                    'errors': errors
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def export_accounts(self, filters=None):
        """Export accounts to file"""
        try:
            query = Account.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            accounts = query.all()
            
            # Convert to export format
            export_data = []
            for account in accounts:
                export_data.append({
                    'id': account.id,
                    'name': account.name,
                    'industry': account.industry,
                    'website': account.website,
                    'phone': account.phone,
                    'email': account.email,
                    'address': account.address,
                    'city': account.city,
                    'state': account.state,
                    'country': account.country,
                    'postal_code': account.postal_code,
                    'annual_revenue': float(account.annual_revenue) if account.annual_revenue else None,
                    'employee_count': account.employee_count,
                    'status': account.status,
                    'type': account.type,
                    'parent_account_id': account.parent_account_id,
                    'territory_id': account.territory_id,
                    'created_at': account.created_at.isoformat() if account.created_at else None,
                    'updated_at': account.updated_at.isoformat() if account.updated_at else None
                })
            
            return {'success': True, 'data': export_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_account_reports(self):
        """Generate account reports"""
        try:
            accounts = Account.query.all()
            
            report = {
                'total_accounts': len(accounts),
                'by_industry': {},
                'by_status': {},
                'by_type': {},
                'by_territory': {},
                'total_revenue': 0,
                'average_revenue': 0
            }
            
            total_revenue = 0
            accounts_with_revenue = 0
            
            for account in accounts:
                # By industry
                industry = account.industry or 'Unknown'
                if industry not in report['by_industry']:
                    report['by_industry'][industry] = 0
                report['by_industry'][industry] += 1
                
                # By status
                status = account.status
                if status not in report['by_status']:
                    report['by_status'][status] = 0
                report['by_status'][status] += 1
                
                # By type
                account_type = account.type or 'Unknown'
                if account_type not in report['by_type']:
                    report['by_type'][account_type] = 0
                report['by_type'][account_type] += 1
                
                # By territory
                territory = account.territory.name if account.territory else 'Unassigned'
                if territory not in report['by_territory']:
                    report['by_territory'][territory] = 0
                report['by_territory'][territory] += 1
                
                # Revenue calculations
                if account.annual_revenue:
                    total_revenue += float(account.annual_revenue)
                    accounts_with_revenue += 1
            
            report['total_revenue'] = total_revenue
            report['average_revenue'] = total_revenue / accounts_with_revenue if accounts_with_revenue > 0 else 0
            
            return {'success': True, 'data': report}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _apply_filters(self, query, filters):
        """Apply filters to query"""
        for field, value in filters.items():
            if hasattr(Account, field):
                if isinstance(value, dict):
                    if 'operator' in value and 'value' in value:
                        if value['operator'] == 'like':
                            query = query.filter(getattr(Account, field).like(f"%{value['value']}%"))
                        elif value['operator'] == 'in':
                            query = query.filter(getattr(Account, field).in_(value['value']))
                        else:
                            query = query.filter(getattr(Account, field) == value['value'])
                else:
                    query = query.filter(getattr(Account, field) == value)
        
        return query 