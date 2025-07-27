from app import db
from app.models.crm import Opportunity, Account, Contact, Lead, Activity, Quote
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import json

class OpportunityService:
    """Service for managing opportunities with CRUD operations"""
    
    def create_opportunity(self, opportunity_data):
        """Create a new opportunity"""
        try:
            # Validate required fields
            if 'name' not in opportunity_data or not opportunity_data['name']:
                return {'success': False, 'error': 'Opportunity name is required'}
            
            # Create new opportunity
            opportunity = Opportunity(
                name=opportunity_data['name'],
                account_id=opportunity_data.get('account_id'),
                contact_id=opportunity_data.get('contact_id'),
                lead_id=opportunity_data.get('lead_id'),
                stage=opportunity_data.get('stage', 'Prospecting'),
                amount=opportunity_data.get('amount'),
                probability=opportunity_data.get('probability', 0),
                expected_close_date=opportunity_data.get('expected_close_date'),
                actual_close_date=opportunity_data.get('actual_close_date'),
                type=opportunity_data.get('type'),
                source=opportunity_data.get('source'),
                description=opportunity_data.get('description'),
                notes=opportunity_data.get('notes'),
                assigned_to=opportunity_data.get('assigned_to')
            )
            
            db.session.add(opportunity)
            db.session.commit()
            
            return {'success': True, 'data': opportunity, 'message': 'Opportunity created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_opportunity(self, opportunity_id):
        """Get an opportunity by ID"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            return {'success': True, 'data': opportunity}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_opportunities(self, filters=None, page=1, per_page=20):
        """Get opportunities with optional filtering and pagination"""
        try:
            query = Opportunity.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Apply pagination
            opportunities = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            return {
                'success': True, 
                'data': {
                    'opportunities': opportunities.items,
                    'total': opportunities.total,
                    'pages': opportunities.pages,
                    'current_page': opportunities.page,
                    'per_page': opportunities.per_page
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_opportunity(self, opportunity_id, update_data):
        """Update an opportunity"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(opportunity, field) and field not in ['id', 'created_at']:
                    setattr(opportunity, field, value)
            
            opportunity.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'data': opportunity, 'message': 'Opportunity updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def delete_opportunity(self, opportunity_id):
        """Delete an opportunity"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            db.session.delete(opportunity)
            db.session.commit()
            
            return {'success': True, 'message': 'Opportunity deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def manage_sales_pipeline(self, opportunity_id, stage_data):
        """Manage sales pipeline stage transitions"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            # Update stage
            old_stage = opportunity.stage
            opportunity.stage = stage_data.get('stage', opportunity.stage)
            opportunity.probability = stage_data.get('probability', opportunity.probability)
            
            # Create stage transition activity
            activity = Activity(
                subject=f"Stage Change: {old_stage} → {opportunity.stage}",
                type='Task',
                status='Completed',
                description=f"Opportunity moved from {old_stage} to {opportunity.stage}",
                opportunity_id=opportunity_id,
                created_by=stage_data.get('user_id')
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {'success': True, 'data': opportunity, 'message': 'Sales pipeline updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def calculate_probability(self, opportunity_id):
        """Calculate opportunity probability based on stage"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            # Stage-based probability calculation
            stage_probabilities = {
                'Prospecting': 10,
                'Qualification': 25,
                'Proposal': 50,
                'Negotiation': 75,
                'Closed Won': 100,
                'Closed Lost': 0
            }
            
            probability = stage_probabilities.get(opportunity.stage, 0)
            opportunity.probability = probability
            
            db.session.commit()
            
            return {'success': True, 'data': {'probability': probability}}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def generate_quotes(self, opportunity_id, quote_data):
        """Generate quotes for an opportunity"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            # Create quote
            quote = Quote(
                quote_number=quote_data.get('quote_number'),
                opportunity_id=opportunity_id,
                status=quote_data.get('status', 'Draft'),
                valid_until=quote_data.get('valid_until'),
                total_amount=quote_data.get('total_amount'),
                tax_amount=quote_data.get('tax_amount', 0),
                discount_amount=quote_data.get('discount_amount', 0),
                grand_total=quote_data.get('grand_total'),
                notes=quote_data.get('notes'),
                terms_conditions=quote_data.get('terms_conditions'),
                created_by=quote_data.get('user_id')
            )
            
            db.session.add(quote)
            db.session.commit()
            
            return {'success': True, 'data': quote, 'message': 'Quote generated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def create_proposals(self, opportunity_id, proposal_data):
        """Create proposals for an opportunity"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            # Create proposal activity
            activity = Activity(
                subject=f"Proposal Created: {proposal_data.get('title', 'Proposal')}",
                type='Task',
                status='Completed',
                description=proposal_data.get('description'),
                opportunity_id=opportunity_id,
                created_by=proposal_data.get('user_id')
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {'success': True, 'data': activity, 'message': 'Proposal created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def manage_contracts(self, opportunity_id, contract_data):
        """Manage contracts for an opportunity"""
        try:
            opportunity = Opportunity.query.get(opportunity_id)
            if not opportunity:
                return {'success': False, 'error': 'Opportunity not found'}
            
            # Create contract activity
            activity = Activity(
                subject=f"Contract: {contract_data.get('title', 'Contract Management')}",
                type='Task',
                status='Planned',
                description=contract_data.get('description'),
                opportunity_id=opportunity_id,
                created_by=contract_data.get('user_id')
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {'success': True, 'data': activity, 'message': 'Contract management activity created'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def forecast_sales(self, forecast_data):
        """Generate sales forecast"""
        try:
            # Get opportunities closing in the forecast period
            start_date = forecast_data.get('start_date', datetime.utcnow())
            end_date = forecast_data.get('end_date', datetime.utcnow() + timedelta(days=90))
            
            opportunities = Opportunity.query.filter(
                and_(
                    Opportunity.expected_close_date >= start_date,
                    Opportunity.expected_close_date <= end_date,
                    Opportunity.stage.in_(['Prospecting', 'Qualification', 'Proposal', 'Negotiation'])
                )
            ).all()
            
            forecast_amount = 0
            for opp in opportunities:
                if opp.amount and opp.probability:
                    forecast_amount += float(opp.amount) * opp.probability / 100
            
            return {
                'success': True,
                'data': {
                    'forecast_amount': round(forecast_amount, 2),
                    'opportunity_count': len(opportunities),
                    'start_date': start_date,
                    'end_date': end_date
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_opportunity_reports(self):
        """Generate opportunity reports"""
        try:
            opportunities = Opportunity.query.all()
            
            report = {
                'total_opportunities': len(opportunities),
                'by_stage': {},
                'by_type': {},
                'by_source': {},
                'total_pipeline_value': 0,
                'weighted_pipeline_value': 0,
                'won_value': 0,
                'lost_value': 0
            }
            
            for opp in opportunities:
                # By stage
                stage = opp.stage
                if stage not in report['by_stage']:
                    report['by_stage'][stage] = {'count': 0, 'value': 0}
                report['by_stage'][stage]['count'] += 1
                if opp.amount:
                    report['by_stage'][stage]['value'] += float(opp.amount)
                    report['total_pipeline_value'] += float(opp.amount)
                    report['weighted_pipeline_value'] += float(opp.amount) * (opp.probability or 0) / 100
                
                # By type
                opp_type = opp.type or 'Unknown'
                if opp_type not in report['by_type']:
                    report['by_type'][opp_type] = 0
                report['by_type'][opp_type] += 1
                
                # By source
                source = opp.source or 'Unknown'
                if source not in report['by_source']:
                    report['by_source'][source] = 0
                report['by_source'][source] += 1
                
                # Won/Lost values
                if opp.stage == 'Closed Won' and opp.amount:
                    report['won_value'] += float(opp.amount)
                elif opp.stage == 'Closed Lost' and opp.amount:
                    report['lost_value'] += float(opp.amount)
            
            return {'success': True, 'data': report}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _apply_filters(self, query, filters):
        """Apply filters to query"""
        for field, value in filters.items():
            if hasattr(Opportunity, field):
                if isinstance(value, dict):
                    if 'operator' in value and 'value' in value:
                        if value['operator'] == 'like':
                            query = query.filter(getattr(Opportunity, field).like(f"%{value['value']}%"))
                        elif value['operator'] == 'in':
                            query = query.filter(getattr(Opportunity, field).in_(value['value']))
                        else:
                            query = query.filter(getattr(Opportunity, field) == value['value'])
                else:
                    query = query.filter(getattr(Opportunity, field) == value)
        
        return query 