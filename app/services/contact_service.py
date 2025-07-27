from app import db
from app.models.crm import Contact, Account, Activity, Opportunity, User
from datetime import datetime
from sqlalchemy import func, and_, or_
import json

class ContactService:
    """Service for managing contacts with CRUD operations"""
    
    def create_contact(self, contact_data):
        """Create a new contact"""
        try:
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email']
            for field in required_fields:
                if field not in contact_data or not contact_data[field]:
                    return {'success': False, 'error': f'{field} is required'}
            
            # Check if email already exists
            existing_contact = Contact.query.filter_by(email=contact_data['email']).first()
            if existing_contact:
                return {'success': False, 'error': 'Contact with this email already exists'}
            
            # Create new contact
            contact = Contact(
                first_name=contact_data['first_name'],
                last_name=contact_data['last_name'],
                email=contact_data['email'],
                phone=contact_data.get('phone'),
                mobile=contact_data.get('mobile'),
                job_title=contact_data.get('job_title'),
                department=contact_data.get('department'),
                account_id=contact_data.get('account_id'),
                lead_source=contact_data.get('lead_source'),
                status=contact_data.get('status', 'Active'),
                preferred_contact_method=contact_data.get('preferred_contact_method'),
                notes=contact_data.get('notes'),
                assigned_to=contact_data.get('assigned_to')
            )
            
            db.session.add(contact)
            db.session.commit()
            
            return {'success': True, 'data': contact, 'message': 'Contact created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_contact(self, contact_id):
        """Get a contact by ID"""
        try:
            contact = Contact.query.get(contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}
            
            return {'success': True, 'data': contact}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_contacts(self, filters=None, page=1, per_page=20):
        """Get contacts with optional filtering and pagination"""
        try:
            query = Contact.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Apply pagination
            contacts = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            return {
                'success': True, 
                'data': {
                    'contacts': contacts.items,
                    'total': contacts.total,
                    'pages': contacts.pages,
                    'current_page': contacts.page,
                    'per_page': contacts.per_page
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_contact(self, contact_id, update_data):
        """Update a contact"""
        try:
            contact = Contact.query.get(contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(contact, field) and field not in ['id', 'created_at']:
                    setattr(contact, field, value)
            
            contact.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'data': contact, 'message': 'Contact updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def delete_contact(self, contact_id):
        """Delete a contact"""
        try:
            contact = Contact.query.get(contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}
            
            db.session.delete(contact)
            db.session.commit()
            
            return {'success': True, 'message': 'Contact deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def manage_contact_relationships(self, contact_id, relationship_data):
        """Manage contact relationships"""
        try:
            contact = Contact.query.get(contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}
            
            # Update relationship data
            current_notes = contact.notes or ""
            relationship_notes = f"\nRelationship Update: {relationship_data.get('description', '')}"
            contact.notes = current_notes + relationship_notes
            
            db.session.commit()
            
            return {'success': True, 'data': contact, 'message': 'Contact relationships updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def track_communication_preferences(self, contact_id, preferences_data):
        """Track communication preferences"""
        try:
            contact = Contact.query.get(contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}
            
            # Update communication preferences
            contact.preferred_contact_method = preferences_data.get('preferred_contact_method', contact.preferred_contact_method)
            
            # Add preferences to notes
            current_notes = contact.notes or ""
            preference_notes = f"\nCommunication Preferences: {preferences_data.get('description', '')}"
            contact.notes = current_notes + preference_notes
            
            db.session.commit()
            
            return {'success': True, 'data': contact, 'message': 'Communication preferences updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def segment_contacts(self, segmentation_criteria):
        """Segment contacts based on criteria"""
        try:
            query = Contact.query
            
            # Apply segmentation criteria
            if 'account_id' in segmentation_criteria:
                query = query.filter(Contact.account_id == segmentation_criteria['account_id'])
            
            if 'status' in segmentation_criteria:
                query = query.filter(Contact.status == segmentation_criteria['status'])
            
            if 'job_title' in segmentation_criteria:
                query = query.filter(Contact.job_title.like(f"%{segmentation_criteria['job_title']}%"))
            
            if 'department' in segmentation_criteria:
                query = query.filter(Contact.department == segmentation_criteria['department'])
            
            contacts = query.all()
            
            return {'success': True, 'data': contacts, 'count': len(contacts)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def import_contacts(self, file_data):
        """Import contacts from file"""
        try:
            imported_count = 0
            errors = []
            
            for row in file_data:
                try:
                    result = self.create_contact(row)
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
    
    def export_contacts(self, filters=None):
        """Export contacts to file"""
        try:
            query = Contact.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            contacts = query.all()
            
            # Convert to export format
            export_data = []
            for contact in contacts:
                export_data.append({
                    'id': contact.id,
                    'first_name': contact.first_name,
                    'last_name': contact.last_name,
                    'email': contact.email,
                    'phone': contact.phone,
                    'mobile': contact.mobile,
                    'job_title': contact.job_title,
                    'department': contact.department,
                    'account_id': contact.account_id,
                    'lead_source': contact.lead_source,
                    'status': contact.status,
                    'preferred_contact_method': contact.preferred_contact_method,
                    'notes': contact.notes,
                    'created_at': contact.created_at.isoformat() if contact.created_at else None,
                    'updated_at': contact.updated_at.isoformat() if contact.updated_at else None
                })
            
            return {'success': True, 'data': export_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_contact_reports(self):
        """Generate contact reports"""
        try:
            contacts = Contact.query.all()
            
            report = {
                'total_contacts': len(contacts),
                'by_status': {},
                'by_department': {},
                'by_job_title': {},
                'by_account': {},
                'by_lead_source': {}
            }
            
            for contact in contacts:
                # By status
                status = contact.status
                if status not in report['by_status']:
                    report['by_status'][status] = 0
                report['by_status'][status] += 1
                
                # By department
                department = contact.department or 'Unknown'
                if department not in report['by_department']:
                    report['by_department'][department] = 0
                report['by_department'][department] += 1
                
                # By job title
                job_title = contact.job_title or 'Unknown'
                if job_title not in report['by_job_title']:
                    report['by_job_title'][job_title] = 0
                report['by_job_title'][job_title] += 1
                
                # By account
                account_name = contact.account.name if contact.account else 'Unassigned'
                if account_name not in report['by_account']:
                    report['by_account'][account_name] = 0
                report['by_account'][account_name] += 1
                
                # By lead source
                lead_source = contact.lead_source or 'Unknown'
                if lead_source not in report['by_lead_source']:
                    report['by_lead_source'][lead_source] = 0
                report['by_lead_source'][lead_source] += 1
            
            return {'success': True, 'data': report}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _apply_filters(self, query, filters):
        """Apply filters to query"""
        for field, value in filters.items():
            if hasattr(Contact, field):
                if isinstance(value, dict):
                    if 'operator' in value and 'value' in value:
                        if value['operator'] == 'like':
                            query = query.filter(getattr(Contact, field).like(f"%{value['value']}%"))
                        elif value['operator'] == 'in':
                            query = query.filter(getattr(Contact, field).in_(value['value']))
                        else:
                            query = query.filter(getattr(Contact, field) == value['value'])
                else:
                    query = query.filter(getattr(Contact, field) == value)
        
        return query 