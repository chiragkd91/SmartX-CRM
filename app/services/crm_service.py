from app import db
from app.models.crm import Lead, Account, Contact, Opportunity, Activity, Quote, User
from app.models.crm_business_processes import Campaign, Workflow, AutomationRule
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import json

class CRMService:
    """Main CRM service for handling core CRM operations"""
    
    def get_crm_stats(self):
        """Get overall CRM statistics"""
        try:
            stats = {
                'total_leads': Lead.query.count(),
                'total_accounts': Account.query.count(),
                'total_contacts': Contact.query.count(),
                'total_opportunities': Opportunity.query.count(),
                'total_activities': Activity.query.count(),
                'total_quotes': Quote.query.count(),
                'active_leads': Lead.query.filter(Lead.status.in_(['New', 'Qualified', 'Nurturing'])).count(),
                'won_opportunities': Opportunity.query.filter(Opportunity.stage == 'Closed Won').count(),
                'pending_activities': Activity.query.filter(Activity.status == 'Planned').count()
            }
            return {'success': True, 'data': stats}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_sales_pipeline(self):
        """Get sales pipeline data"""
        try:
            pipeline = db.session.query(
                Opportunity.stage,
                func.count(Opportunity.id).label('count'),
                func.sum(Opportunity.amount).label('total_amount')
            ).group_by(Opportunity.stage).all()
            
            pipeline_data = []
            for stage, count, amount in pipeline:
                pipeline_data.append({
                    'stage': stage,
                    'count': count,
                    'amount': float(amount) if amount else 0
                })
            
            return {'success': True, 'data': pipeline_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_lead_conversion_rate(self, days=30):
        """Calculate lead conversion rate"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            total_leads = Lead.query.filter(Lead.created_at >= start_date).count()
            converted_leads = Lead.query.filter(
                and_(
                    Lead.created_at >= start_date,
                    Lead.status == 'Converted'
                )
            ).count()
            
            conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
            
            return {
                'success': True,
                'data': {
                    'total_leads': total_leads,
                    'converted_leads': converted_leads,
                    'conversion_rate': round(conversion_rate, 2)
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_customer_lifetime_value(self):
        """Calculate customer lifetime value"""
        try:
            # Get all won opportunities
            won_opportunities = Opportunity.query.filter(
                Opportunity.stage == 'Closed Won'
            ).all()
            
            total_revenue = sum(float(opp.amount) for opp in won_opportunities if opp.amount)
            customer_count = len(set(opp.account_id for opp in won_opportunities if opp.account_id))
            
            clv = total_revenue / customer_count if customer_count > 0 else 0
            
            return {
                'success': True,
                'data': {
                    'total_revenue': total_revenue,
                    'customer_count': customer_count,
                    'clv': round(clv, 2)
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_sales_forecast(self, months=3):
        """Generate sales forecast"""
        try:
            end_date = datetime.utcnow() + timedelta(days=months*30)
            
            # Get opportunities closing in the next X months
            forecast_opportunities = Opportunity.query.filter(
                and_(
                    Opportunity.expected_close_date <= end_date,
                    Opportunity.stage.in_(['Prospecting', 'Qualification', 'Proposal', 'Negotiation'])
                )
            ).all()
            
            forecast_amount = sum(float(opp.amount * opp.probability / 100) for opp in forecast_opportunities if opp.amount)
            
            return {
                'success': True,
                'data': {
                    'forecast_amount': round(forecast_amount, 2),
                    'opportunity_count': len(forecast_opportunities),
                    'forecast_period': f'{months} months'
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_activity_summary(self, days=7):
        """Get activity summary for the last X days"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            activities = Activity.query.filter(Activity.created_at >= start_date).all()
            
            activity_summary = {
                'total_activities': len(activities),
                'completed_activities': len([a for a in activities if a.status == 'Completed']),
                'pending_activities': len([a for a in activities if a.status == 'Planned']),
                'by_type': {}
            }
            
            # Group by activity type
            for activity in activities:
                activity_type = activity.type
                if activity_type not in activity_summary['by_type']:
                    activity_summary['by_type'][activity_type] = 0
                activity_summary['by_type'][activity_type] += 1
            
            return {'success': True, 'data': activity_summary}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_crm_reports(self, report_type='all'):
        """Generate CRM reports"""
        try:
            reports = {}
            
            if report_type in ['all', 'leads']:
                reports['leads'] = self._generate_lead_report()
            
            if report_type in ['all', 'opportunities']:
                reports['opportunities'] = self._generate_opportunity_report()
            
            if report_type in ['all', 'activities']:
                reports['activities'] = self._generate_activity_report()
            
            if report_type in ['all', 'sales']:
                reports['sales'] = self._generate_sales_report()
            
            return {'success': True, 'data': reports}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def export_crm_data(self, data_type, filters=None):
        """Export CRM data"""
        try:
            if data_type == 'leads':
                query = Lead.query
            elif data_type == 'accounts':
                query = Account.query
            elif data_type == 'contacts':
                query = Contact.query
            elif data_type == 'opportunities':
                query = Opportunity.query
            elif data_type == 'activities':
                query = Activity.query
            else:
                return {'success': False, 'error': 'Invalid data type'}
            
            # Apply filters if provided
            if filters:
                query = self._apply_filters(query, filters)
            
            data = query.all()
            
            # Convert to dictionary format
            export_data = []
            for item in data:
                export_data.append(item.__dict__)
            
            return {'success': True, 'data': export_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _generate_lead_report(self):
        """Generate lead report"""
        leads = Lead.query.all()
        
        report = {
            'total_leads': len(leads),
            'by_status': {},
            'by_source': {},
            'by_industry': {},
            'conversion_rate': 0
        }
        
        converted_count = 0
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
            
            # Conversion count
            if lead.status == 'Converted':
                converted_count += 1
        
        report['conversion_rate'] = (converted_count / len(leads) * 100) if leads else 0
        
        return report
    
    def _generate_opportunity_report(self):
        """Generate opportunity report"""
        opportunities = Opportunity.query.all()
        
        report = {
            'total_opportunities': len(opportunities),
            'by_stage': {},
            'total_pipeline_value': 0,
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
            
            # Won/Lost values
            if opp.stage == 'Closed Won' and opp.amount:
                report['won_value'] += float(opp.amount)
            elif opp.stage == 'Closed Lost' and opp.amount:
                report['lost_value'] += float(opp.amount)
        
        return report
    
    def _generate_activity_report(self):
        """Generate activity report"""
        activities = Activity.query.all()
        
        report = {
            'total_activities': len(activities),
            'by_type': {},
            'by_status': {},
            'by_priority': {}
        }
        
        for activity in activities:
            # By type
            activity_type = activity.type
            if activity_type not in report['by_type']:
                report['by_type'][activity_type] = 0
            report['by_type'][activity_type] += 1
            
            # By status
            status = activity.status
            if status not in report['by_status']:
                report['by_status'][status] = 0
            report['by_status'][status] += 1
            
            # By priority
            priority = activity.priority
            if priority not in report['by_priority']:
                report['by_priority'][priority] = 0
            report['by_priority'][priority] += 1
        
        return report
    
    def _generate_sales_report(self):
        """Generate sales report"""
        opportunities = Opportunity.query.filter(
            Opportunity.stage == 'Closed Won'
        ).all()
        
        report = {
            'total_sales': len(opportunities),
            'total_revenue': 0,
            'average_deal_size': 0,
            'by_month': {}
        }
        
        for opp in opportunities:
            if opp.amount:
                amount = float(opp.amount)
                report['total_revenue'] += amount
                
                # By month
                if opp.actual_close_date:
                    month_key = opp.actual_close_date.strftime('%Y-%m')
                    if month_key not in report['by_month']:
                        report['by_month'][month_key] = {'count': 0, 'revenue': 0}
                    report['by_month'][month_key]['count'] += 1
                    report['by_month'][month_key]['revenue'] += amount
        
        report['average_deal_size'] = report['total_revenue'] / len(opportunities) if opportunities else 0
        
        return report
    
    def _apply_filters(self, query, filters):
        """Apply filters to query"""
        for field, value in filters.items():
            if hasattr(query.column_descriptions[0]['type'], field):
                if isinstance(value, dict):
                    if 'operator' in value and 'value' in value:
                        if value['operator'] == 'like':
                            query = query.filter(getattr(query.column_descriptions[0]['type'], field).like(f"%{value['value']}%"))
                        elif value['operator'] == 'in':
                            query = query.filter(getattr(query.column_descriptions[0]['type'], field).in_(value['value']))
                        else:
                            query = query.filter(getattr(query.column_descriptions[0]['type'], field) == value['value'])
                else:
                    query = query.filter(getattr(query.column_descriptions[0]['type'], field) == value)
        
        return query 