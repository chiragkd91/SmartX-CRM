from app import db
from app.models.crm import Lead, Activity, Opportunity, User
from app.models.crm_business_processes import LeadScoring, Campaign
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import json

class LeadService:
    """Service for managing leads with CRUD operations"""
    
    def create_lead(self, lead_data):
        """Create a new lead"""
        try:
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email']
            for field in required_fields:
                if field not in lead_data or not lead_data[field]:
                    return {'success': False, 'error': f'{field} is required'}
            
            # Check if email already exists
            existing_lead = Lead.query.filter_by(email=lead_data['email']).first()
            if existing_lead:
                return {'success': False, 'error': 'Lead with this email already exists'}
            
            # Create new lead
            lead = Lead(
                first_name=lead_data['first_name'],
                last_name=lead_data['last_name'],
                email=lead_data['email'],
                phone=lead_data.get('phone'),
                company=lead_data.get('company'),
                job_title=lead_data.get('job_title'),
                industry=lead_data.get('industry'),
                source=lead_data.get('source', 'Manual'),
                status=lead_data.get('status', 'New'),
                budget=lead_data.get('budget'),
                timeline=lead_data.get('timeline'),
                notes=lead_data.get('notes'),
                assigned_to=lead_data.get('assigned_to')
            )
            
            db.session.add(lead)
            db.session.commit()
            
            # Auto-score the lead if scoring rules exist
            self.score_lead(lead.id)
            
            return {'success': True, 'data': lead, 'message': 'Lead created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_lead(self, lead_id):
        """Get a lead by ID"""
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            return {'success': True, 'data': lead}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_leads(self, filters=None, page=1, per_page=20):
        """Get leads with optional filtering and pagination"""
        try:
            query = Lead.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Apply pagination
            leads = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            return {
                'success': True, 
                'data': {
                    'leads': leads.items,
                    'total': leads.total,
                    'pages': leads.pages,
                    'current_page': leads.page,
                    'per_page': leads.per_page
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_lead(self, lead_id, update_data):
        """Update a lead"""
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(lead, field) and field not in ['id', 'created_at']:
                    setattr(lead, field, value)
            
            lead.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'data': lead, 'message': 'Lead updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def delete_lead(self, lead_id):
        """Delete a lead"""
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            db.session.delete(lead)
            db.session.commit()
            
            return {'success': True, 'message': 'Lead deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def qualify_lead(self, lead_id, qualification_data):
        """Qualify a lead"""
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            # Update qualification fields
            lead.status = qualification_data.get('status', 'Qualified')
            lead.score = qualification_data.get('score', lead.score)
            lead.notes = qualification_data.get('notes', lead.notes)
            lead.updated_at = datetime.utcnow()
            
            # Create qualification activity
            activity = Activity(
                subject=f"Lead Qualified: {lead.full_name}",
                type='Task',
                status='Completed',
                description=f"Lead qualified with score: {lead.score}",
                lead_id=lead_id,
                created_by=qualification_data.get('user_id')
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {'success': True, 'data': lead, 'message': 'Lead qualified successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def score_lead(self, lead_id):
        """Score a lead based on scoring rules"""
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            # Get active scoring rules
            scoring_rules = LeadScoring.query.filter_by(is_active=True).all()
            
            total_score = 0
            for rule in scoring_rules:
                if rule.criteria:
                    criteria = rule.criteria
                    rule_score = self._calculate_rule_score(lead, criteria)
                    total_score += rule_score
            
            lead.score = total_score
            db.session.commit()
            
            return {'success': True, 'data': {'score': total_score}}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def nurture_lead(self, lead_id, nurturing_data):
        """Nurture a lead with automated activities"""
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            # Create nurturing activity
            activity = Activity(
                subject=f"Nurturing: {nurturing_data.get('subject', 'Lead Nurturing')}",
                type=nurturing_data.get('type', 'Email'),
                status='Planned',
                description=nurturing_data.get('description'),
                due_date=datetime.utcnow() + timedelta(days=nurturing_data.get('delay_days', 1)),
                lead_id=lead_id,
                created_by=nurturing_data.get('user_id')
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {'success': True, 'data': activity, 'message': 'Lead nurturing activity created'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def convert_lead(self, lead_id, conversion_data):
        """Convert a lead to opportunity/account/contact"""
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            # Update lead status
            lead.status = 'Converted'
            lead.updated_at = datetime.utcnow()
            
            # Create opportunity if specified
            opportunity = None
            if conversion_data.get('create_opportunity'):
                opportunity = Opportunity(
                    name=conversion_data.get('opportunity_name', f"Opportunity from {lead.full_name}"),
                    lead_id=lead_id,
                    stage='Prospecting',
                    amount=conversion_data.get('amount'),
                    expected_close_date=conversion_data.get('expected_close_date'),
                    description=conversion_data.get('description'),
                    assigned_to=conversion_data.get('assigned_to')
                )
                db.session.add(opportunity)
            
            # Create conversion activity
            activity = Activity(
                subject=f"Lead Converted: {lead.full_name}",
                type='Task',
                status='Completed',
                description=f"Lead converted to opportunity: {opportunity.name if opportunity else 'N/A'}",
                lead_id=lead_id,
                opportunity_id=opportunity.id if opportunity else None,
                created_by=conversion_data.get('user_id')
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {
                'success': True, 
                'data': {
                    'lead': lead,
                    'opportunity': opportunity
                },
                'message': 'Lead converted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def import_leads(self, file_data):
        """Import leads from file"""
        try:
            # This would typically handle CSV/Excel file parsing
            # For now, we'll assume file_data is a list of dictionaries
            imported_count = 0
            errors = []
            
            for row in file_data:
                try:
                    result = self.create_lead(row)
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
    
    def export_leads(self, filters=None):
        """Export leads to file"""
        try:
            query = Lead.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            leads = query.all()
            
            # Convert to export format
            export_data = []
            for lead in leads:
                export_data.append({
                    'id': lead.id,
                    'first_name': lead.first_name,
                    'last_name': lead.last_name,
                    'email': lead.email,
                    'phone': lead.phone,
                    'company': lead.company,
                    'job_title': lead.job_title,
                    'industry': lead.industry,
                    'source': lead.source,
                    'status': lead.status,
                    'score': lead.score,
                    'budget': float(lead.budget) if lead.budget else None,
                    'timeline': lead.timeline,
                    'notes': lead.notes,
                    'created_at': lead.created_at.isoformat() if lead.created_at else None,
                    'updated_at': lead.updated_at.isoformat() if lead.updated_at else None
                })
            
            return {'success': True, 'data': export_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_lead_reports(self):
        """Generate lead reports"""
        try:
            leads = Lead.query.all()
            
            report = {
                'total_leads': len(leads),
                'by_status': {},
                'by_source': {},
                'by_industry': {},
                'by_score_range': {
                    '0-25': 0,
                    '26-50': 0,
                    '51-75': 0,
                    '76-100': 0
                },
                'conversion_rate': 0,
                'average_score': 0
            }
            
            converted_count = 0
            total_score = 0
            
            for lead in leads:
                # By status
                status = lead.status
                if status not in report['by_status']:
                    report['by_status'][status] = 0
                report['by_status'][status] += 1
                
                # By source
                source = lead.source or 'Unknown'
                if source not in report['by_source']:
                    report['by_source'][source] = 0
                report['by_source'][source] += 1
                
                # By industry
                industry = lead.industry or 'Unknown'
                if industry not in report['by_industry']:
                    report['by_industry'][industry] = 0
                report['by_industry'][industry] += 1
                
                # By score range
                score = lead.score or 0
                if score <= 25:
                    report['by_score_range']['0-25'] += 1
                elif score <= 50:
                    report['by_score_range']['26-50'] += 1
                elif score <= 75:
                    report['by_score_range']['51-75'] += 1
                else:
                    report['by_score_range']['76-100'] += 1
                
                # Conversion count
                if lead.status == 'Converted':
                    converted_count += 1
                
                total_score += score
            
            report['conversion_rate'] = (converted_count / len(leads) * 100) if leads else 0
            report['average_score'] = (total_score / len(leads)) if leads else 0
            
            return {'success': True, 'data': report}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _calculate_rule_score(self, lead, criteria):
        """Calculate score based on scoring criteria"""
        score = 0
        
        for criterion in criteria:
            field = criterion.get('field')
            operator = criterion.get('operator')
            value = criterion.get('value')
            points = criterion.get('points', 0)
            
            if hasattr(lead, field):
                field_value = getattr(lead, field)
                
                if operator == 'equals' and field_value == value:
                    score += points
                elif operator == 'contains' and value in str(field_value):
                    score += points
                elif operator == 'greater_than' and field_value > value:
                    score += points
                elif operator == 'less_than' and field_value < value:
                    score += points
        
        return score
    
    def _apply_filters(self, query, filters):
        """Apply filters to query"""
        for field, value in filters.items():
            if hasattr(Lead, field):
                if isinstance(value, dict):
                    if 'operator' in value and 'value' in value:
                        if value['operator'] == 'like':
                            query = query.filter(getattr(Lead, field).like(f"%{value['value']}%"))
                        elif value['operator'] == 'in':
                            query = query.filter(getattr(Lead, field).in_(value['value']))
                        else:
                            query = query.filter(getattr(Lead, field) == value['value'])
                else:
                    query = query.filter(getattr(Lead, field) == value)
        
        return query 