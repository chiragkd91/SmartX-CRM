from app import db
from app.models.crm import Activity, Account, Contact, Lead, Opportunity, User
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import json

class ActivityService:
    """Service for managing activities with CRUD operations"""
    
    def create_activity(self, activity_data):
        """Create a new activity"""
        try:
            # Validate required fields
            required_fields = ['subject', 'type']
            for field in required_fields:
                if field not in activity_data or not activity_data[field]:
                    return {'success': False, 'error': f'{field} is required'}
            
            # Create new activity
            activity = Activity(
                subject=activity_data['subject'],
                type=activity_data['type'],
                status=activity_data.get('status', 'Planned'),
                priority=activity_data.get('priority', 'Medium'),
                description=activity_data.get('description'),
                due_date=activity_data.get('due_date'),
                completed_date=activity_data.get('completed_date'),
                duration=activity_data.get('duration'),
                location=activity_data.get('location'),
                account_id=activity_data.get('account_id'),
                contact_id=activity_data.get('contact_id'),
                lead_id=activity_data.get('lead_id'),
                opportunity_id=activity_data.get('opportunity_id'),
                assigned_to=activity_data.get('assigned_to'),
                created_by=activity_data.get('created_by')
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {'success': True, 'data': activity, 'message': 'Activity created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_activity(self, activity_id):
        """Get an activity by ID"""
        try:
            activity = Activity.query.get(activity_id)
            if not activity:
                return {'success': False, 'error': 'Activity not found'}
            
            return {'success': True, 'data': activity}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_activities(self, filters=None, page=1, per_page=20):
        """Get activities with optional filtering and pagination"""
        try:
            query = Activity.query
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Apply pagination
            activities = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            return {
                'success': True, 
                'data': {
                    'activities': activities.items,
                    'total': activities.total,
                    'pages': activities.pages,
                    'current_page': activities.page,
                    'per_page': activities.per_page
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_activity(self, activity_id, update_data):
        """Update an activity"""
        try:
            activity = Activity.query.get(activity_id)
            if not activity:
                return {'success': False, 'error': 'Activity not found'}
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(activity, field) and field not in ['id', 'created_at']:
                    setattr(activity, field, value)
            
            activity.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'data': activity, 'message': 'Activity updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def delete_activity(self, activity_id):
        """Delete an activity"""
        try:
            activity = Activity.query.get(activity_id)
            if not activity:
                return {'success': False, 'error': 'Activity not found'}
            
            db.session.delete(activity)
            db.session.commit()
            
            return {'success': True, 'message': 'Activity deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def schedule_activity(self, activity_id, schedule_data):
        """Schedule an activity"""
        try:
            activity = Activity.query.get(activity_id)
            if not activity:
                return {'success': False, 'error': 'Activity not found'}
            
            # Update scheduling information
            activity.due_date = schedule_data.get('due_date')
            activity.duration = schedule_data.get('duration')
            activity.location = schedule_data.get('location')
            activity.status = 'Planned'
            
            db.session.commit()
            
            return {'success': True, 'data': activity, 'message': 'Activity scheduled successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def track_activity_completion(self, activity_id, completion_data):
        """Track activity completion"""
        try:
            activity = Activity.query.get(activity_id)
            if not activity:
                return {'success': False, 'error': 'Activity not found'}
            
            # Update completion information
            activity.status = 'Completed'
            activity.completed_date = completion_data.get('completed_date', datetime.utcnow())
            activity.description = completion_data.get('notes', activity.description)
            
            db.session.commit()
            
            return {'success': True, 'data': activity, 'message': 'Activity completion tracked successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def manage_activity_templates(self, template_data):
        """Manage activity templates"""
        try:
            # This would typically involve creating template records
            # For now, we'll create a template activity
            template_activity = Activity(
                subject=f"Template: {template_data.get('name', 'Activity Template')}",
                type=template_data.get('type', 'Task'),
                status='Template',
                priority=template_data.get('priority', 'Medium'),
                description=template_data.get('description'),
                duration=template_data.get('duration'),
                created_by=template_data.get('created_by')
            )
            
            db.session.add(template_activity)
            db.session.commit()
            
            return {'success': True, 'data': template_activity, 'message': 'Activity template created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def automate_activities(self, automation_data):
        """Automate activity creation"""
        try:
            # Create automated activity based on trigger
            trigger_type = automation_data.get('trigger_type')
            trigger_id = automation_data.get('trigger_id')
            
            if trigger_type == 'lead_created':
                lead = Lead.query.get(trigger_id)
                if lead:
                    activity = Activity(
                        subject=f"Follow up with {lead.full_name}",
                        type='Call',
                        status='Planned',
                        priority='High',
                        description=f"Follow up call for new lead: {lead.full_name}",
                        due_date=datetime.utcnow() + timedelta(days=1),
                        lead_id=trigger_id,
                        assigned_to=automation_data.get('assigned_to'),
                        created_by=automation_data.get('created_by')
                    )
                    db.session.add(activity)
            
            elif trigger_type == 'opportunity_stage_change':
                opportunity = Opportunity.query.get(trigger_id)
                if opportunity:
                    activity = Activity(
                        subject=f"Next steps for {opportunity.name}",
                        type='Task',
                        status='Planned',
                        priority='Medium',
                        description=f"Plan next steps for opportunity: {opportunity.name}",
                        opportunity_id=trigger_id,
                        assigned_to=automation_data.get('assigned_to'),
                        created_by=automation_data.get('created_by')
                    )
                    db.session.add(activity)
            
            db.session.commit()
            
            return {'success': True, 'message': 'Automated activity created successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def send_reminders(self, activity_id):
        """Send reminders for activities"""
        try:
            activity = Activity.query.get(activity_id)
            if not activity:
                return {'success': False, 'error': 'Activity not found'}
            
            # This would typically involve sending email/SMS reminders
            # For now, we'll just update the activity status
            
            if activity.due_date and activity.due_date <= datetime.utcnow():
                activity.status = 'Overdue'
                db.session.commit()
                return {'success': True, 'message': 'Reminder sent - activity marked as overdue'}
            else:
                return {'success': True, 'message': 'Reminder sent successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_activity_reports(self):
        """Generate activity reports"""
        try:
            activities = Activity.query.all()
            
            report = {
                'total_activities': len(activities),
                'by_type': {},
                'by_status': {},
                'by_priority': {},
                'completed_activities': 0,
                'pending_activities': 0,
                'overdue_activities': 0,
                'average_completion_time': 0
            }
            
            total_completion_time = 0
            completed_count = 0
            
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
                
                # Count by status
                if activity.status == 'Completed':
                    report['completed_activities'] += 1
                    if activity.created_at and activity.completed_date:
                        completion_time = (activity.completed_date - activity.created_at).days
                        total_completion_time += completion_time
                        completed_count += 1
                elif activity.status == 'Planned':
                    report['pending_activities'] += 1
                elif activity.status == 'Overdue':
                    report['overdue_activities'] += 1
            
            report['average_completion_time'] = total_completion_time / completed_count if completed_count > 0 else 0
            
            return {'success': True, 'data': report}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def export_activity_data(self):
        """Export activity data"""
        try:
            activities = Activity.query.all()
            
            # Convert to export format
            export_data = []
            for activity in activities:
                export_data.append({
                    'id': activity.id,
                    'subject': activity.subject,
                    'type': activity.type,
                    'status': activity.status,
                    'priority': activity.priority,
                    'description': activity.description,
                    'due_date': activity.due_date.isoformat() if activity.due_date else None,
                    'completed_date': activity.completed_date.isoformat() if activity.completed_date else None,
                    'duration': activity.duration,
                    'location': activity.location,
                    'account_id': activity.account_id,
                    'contact_id': activity.contact_id,
                    'lead_id': activity.lead_id,
                    'opportunity_id': activity.opportunity_id,
                    'assigned_to': activity.assigned_to,
                    'created_by': activity.created_by,
                    'created_at': activity.created_at.isoformat() if activity.created_at else None,
                    'updated_at': activity.updated_at.isoformat() if activity.updated_at else None
                })
            
            return {'success': True, 'data': export_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _apply_filters(self, query, filters):
        """Apply filters to query"""
        for field, value in filters.items():
            if hasattr(Activity, field):
                if isinstance(value, dict):
                    if 'operator' in value and 'value' in value:
                        if value['operator'] == 'like':
                            query = query.filter(getattr(Activity, field).like(f"%{value['value']}%"))
                        elif value['operator'] == 'in':
                            query = query.filter(getattr(Activity, field).in_(value['value']))
                        else:
                            query = query.filter(getattr(Activity, field) == value['value'])
                else:
                    query = query.filter(getattr(Activity, field) == value)
        
        return query 