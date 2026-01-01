"""
Leave Tracker Web Application
Main Flask application with routes and business logic
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaves.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class TeamMember(db.Model):
    """Team member information"""
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    stream = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(20), nullable=False)  # UAE, India
    role = db.Column(db.String(20), default='member')  # member, scrum_master
    annual_entitlement = db.Column(db.Integer, default=22)
    sick_entitlement = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    leave_requests = db.relationship('LeaveRequest', 
                                 foreign_keys='LeaveRequest.employee_id',
                                 backref='employee', 
                                 lazy=True)
    approved_leaves = db.relationship('LeaveRequest',
                                 foreign_keys='LeaveRequest.approved_by',
                                 backref='approver',
                                 lazy=True)
    
    def __repr__(self):
        return f'<TeamMember {self.name} - {self.stream}>'
    
    def get_balance(self, leave_type):
        """Calculate remaining leave balance"""
        if leave_type == 'Annual':
            entitlement = self.annual_entitlement
        else:
            entitlement = self.sick_entitlement
        
        # Sum approved leaves of this type
        approved_leaves = LeaveRequest.query.filter_by(
            employee_id=self.id,
            leave_type=leave_type,
            status='Approved'
        ).all()
        
        used_days = sum(leave.working_days for leave in approved_leaves)
        return entitlement - used_days
    
    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'stream': self.stream,
            'location': self.location,
            'role': self.role,
            'annual_balance': self.get_balance('Annual'),
            'sick_balance': self.get_balance('Sick')
        }


class Holiday(db.Model):
    """Public holidays by location"""
    __tablename__ = 'holidays'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(20), nullable=False)  # UAE, India, Both
    color = db.Column(db.String(7), default='#4CAF50')  # Hex color for calendar
    
    def __repr__(self):
        return f'<Holiday {self.name} - {self.date} - {self.location}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d'),
            'location': self.location,
            'color': self.color
        }


class LeaveRequest(db.Model):
    """Leave requests from team members"""
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('team_members.id'), nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)  # Annual, Sick
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    working_days = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    reason = db.Column(db.Text)
    rejection_reason = db.Column(db.Text)
    override_used = db.Column(db.Boolean, default=False)
    override_reason = db.Column(db.Text)
    approved_by = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<LeaveRequest {self.id} - {self.employee.name} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_name': self.employee.name,
            'employee_email': self.employee.email,
            'stream': self.employee.stream,
            'location': self.employee.location,
            'leave_type': self.leave_type,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'working_days': self.working_days,
            'status': self.status,
            'reason': self.reason,
            'submitted_at': self.submitted_at.strftime('%Y-%m-%d %H:%M'),
            'override_used': self.override_used
        }


class Configuration(db.Model):
    """System configuration settings"""
    __tablename__ = 'configuration'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Config {self.key}={self.value}>'


class Sprint(db.Model):
    """Sprint information for capacity planning"""
    __tablename__ = 'sprints'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Sprint {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'is_active': self.is_active
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_working_days(start_date, end_date, location):
    """
    Calculate working days between two dates
    Excludes weekends (Sat-Sun) and location-specific holidays
    """
    if start_date > end_date:
        return 0
    
    working_days = 0
    current_date = start_date
    
    # Get holidays for this location
    holidays = Holiday.query.filter(
        (Holiday.location == location) | (Holiday.location == 'Both')
    ).all()
    holiday_dates = set(h.date for h in holidays)
    
    while current_date <= end_date:
        # Skip weekends (Saturday=5, Sunday=6)
        if current_date.weekday() not in [5, 6]:
            # Skip holidays
            if current_date not in holiday_dates:
                working_days += 1
        current_date += timedelta(days=1)
    
    return working_days


def check_overlap(employee_id, start_date, end_date, exclude_request_id=None):
    """
    Check if leave request overlaps with approved leaves from same stream
    Returns (has_overlap, overlapping_employee_name, overlapping_dates)
    """
    employee = TeamMember.query.get(employee_id)
    if not employee:
        return False, None, None
    
    # Get all approved leaves from same stream (excluding this employee)
    query = db.session.query(LeaveRequest).join(TeamMember).filter(
        TeamMember.stream == employee.stream,
        TeamMember.id != employee_id,
        LeaveRequest.status == 'Approved',
        LeaveRequest.start_date <= end_date,
        LeaveRequest.end_date >= start_date
    )
    
    if exclude_request_id:
        query = query.filter(LeaveRequest.id != exclude_request_id)
    
    overlapping = query.first()
    
    if overlapping:
        return True, overlapping.employee.name, (overlapping.start_date, overlapping.end_date)
    
    return False, None, None


def check_sufficient_balance(employee_id, leave_type, required_days):
    """
    Check if employee has sufficient balance for leave request
    Returns (sufficient, current_balance, remaining_balance)
    """
    employee = TeamMember.query.get(employee_id)
    if not employee:
        return False, 0, 0
    
    current_balance = employee.get_balance(leave_type)
    remaining = current_balance - required_days
    
    return remaining >= 0, current_balance, remaining


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def scrum_master_required(f):
    """Decorator to require scrum master role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = TeamMember.query.get(session['user_id'])
        if not user or user.role != 'scrum_master':
            flash('Access denied. Scrum Master role required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Landing page - redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        # Find user by email
        user = TeamMember.query.filter_by(email=email, is_active=True).first()
        
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email not found or account inactive', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    user = TeamMember.query.get(session['user_id'])
    
    # Get user's leave statistics
    annual_balance = user.get_balance('Annual')
    sick_balance = user.get_balance('Sick')
    
    # Get pending leaves
    pending_leaves = LeaveRequest.query.filter_by(
        employee_id=user.id,
        status='Pending'
    ).count()
    
    # Get upcoming approved leaves
    upcoming_leaves = LeaveRequest.query.filter_by(
        employee_id=user.id,
        status='Approved'
    ).filter(
        LeaveRequest.start_date >= datetime.now().date()
    ).order_by(LeaveRequest.start_date).limit(5).all()
    
    # Get active sprint
    active_sprint = Sprint.query.filter_by(is_active=True).first()
    
    return render_template('dashboard.html',
                         user=user,
                         annual_balance=annual_balance,
                         sick_balance=sick_balance,
                         pending_leaves=pending_leaves,
                         upcoming_leaves=upcoming_leaves,
                         active_sprint=active_sprint)


@app.route('/calendar')
@login_required
def calendar_view():
    """Calendar view"""
    user = TeamMember.query.get(session['user_id'])
    return render_template('calendar.html', user=user)


@app.route('/leave/request', methods=['GET', 'POST'])
@login_required
def leave_request():
    """Leave request form"""
    user = TeamMember.query.get(session['user_id'])
    
    if request.method == 'POST':
        return submit_leave_request()
    
    annual_balance = user.get_balance('Annual')
    sick_balance = user.get_balance('Sick')
    today = datetime.now().date().strftime('%Y-%m-%d')
    
    return render_template('leave_request.html',
                         user=user,
                         annual_balance=annual_balance,
                         sick_balance=sick_balance,
                         today=today)


@app.route('/leave/submit', methods=['POST'])
@login_required
def submit_leave_request():
    """Submit leave request"""
    # EMAIL NOTIFICATIONS DISABLED - All email imports removed
    
    user = TeamMember.query.get(session['user_id'])
    
    leave_type = request.form.get('leave_type')
    start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
    reason = request.form.get('reason', '')
    
    # Calculate working days
    working_days = calculate_working_days(start_date, end_date, user.location)
    
    # Check sufficient balance
    sufficient, current_balance, remaining = check_sufficient_balance(user.id, leave_type, working_days)
    
    if not sufficient:
        # EMAIL NOTIFICATION DISABLED
        # from email_service import notify_insufficient_balance
        # notify_insufficient_balance(
        #     user.email, user.name, leave_type,
        #     working_days, current_balance, abs(remaining)
        # )
        flash(f'Insufficient {leave_type} leave balance. You need {abs(remaining)} more days.', 'error')
        return redirect(url_for('leave_request'))
    
    # Check overlap
    has_overlap, overlapping_name, overlapping_dates = check_overlap(user.id, start_date, end_date)
    
    if has_overlap:
        # EMAIL NOTIFICATION DISABLED
        # from email_service import notify_overlap_blocked
        # notify_overlap_blocked(
        #     user.email, user.name, overlapping_name,
        #     overlapping_dates, start_date, end_date
        # )
        flash(f'Cannot submit: {overlapping_name} from your stream already has approved leave during this period.', 'error')
        return redirect(url_for('leave_request'))
    
    # Create leave request
    leave_req = LeaveRequest(
        employee_id=user.id,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        working_days=working_days,
        reason=reason,
        status='Pending'
    )
    
    db.session.add(leave_req)
    db.session.commit()
    
    # EMAIL NOTIFICATIONS DISABLED - Team will notify Scrum Masters directly
    # from email_service import notify_new_leave_request
    # notify_new_leave_request(
    #     user.name, user.email, user.stream, leave_type,
    #     start_date.strftime('%d %b %Y'),
    #     end_date.strftime('%d %b %Y'),
    #     working_days, reason, leave_req.id
    # )
    
    flash('Leave request submitted successfully! Please notify your Scrum Master to review.', 'success')
    return redirect(url_for('my_leaves'))


@app.route('/leave/my-leaves')
@login_required
def my_leaves():
    """View user's leaves"""
    user = TeamMember.query.get(session['user_id'])
    leaves = LeaveRequest.query.filter_by(employee_id=user.id).order_by(LeaveRequest.submitted_at.desc()).all()
    
    return render_template('my_leaves.html', user=user, leaves=leaves)


@app.route('/leave/team-leaves')
@login_required
def team_leaves():
    """View all team leaves"""
    user = TeamMember.query.get(session['user_id'])
    leaves = LeaveRequest.query.join(TeamMember).order_by(LeaveRequest.submitted_at.desc()).all()
    
    return render_template('team_leaves.html', user=user, leaves=leaves)


@app.route('/admin')
@login_required
@scrum_master_required
def admin_panel():
    """Admin panel for Scrum Masters"""
    user = TeamMember.query.get(session['user_id'])
    pending_leaves = LeaveRequest.query.filter_by(status='Pending').order_by(LeaveRequest.submitted_at).all()
    
    return render_template('admin.html', user=user, pending_leaves=pending_leaves)


@app.route('/admin/team')
@login_required
@scrum_master_required
def team_management():
    """Manage team members"""
    user = TeamMember.query.get(session['user_id'])
    team_members = TeamMember.query.filter_by(is_active=True).order_by(TeamMember.stream, TeamMember.name).all()
    
    return render_template('team_management.html', user=user, team_members=team_members)


@app.route('/admin/holidays')
@login_required
@scrum_master_required
def holiday_management():
    """Manage holidays"""
    user = TeamMember.query.get(session['user_id'])
    holidays = Holiday.query.order_by(Holiday.date).all()
    
    return render_template('holiday_management.html', user=user, holidays=holidays)


@app.route('/admin/sprint-capacity')
@login_required
@scrum_master_required
def sprint_capacity():
    """Sprint capacity planning"""
    user = TeamMember.query.get(session['user_id'])
    sprints = Sprint.query.order_by(Sprint.start_date.desc()).all()
    
    return render_template('sprint_capacity.html', user=user, sprints=sprints)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/calculate-working-days', methods=['POST'])
@login_required
def api_calculate_working_days():
    """API endpoint to calculate working days"""
    data = request.get_json()
    
    try:
        start = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        location = data['location']
        
        working_days = calculate_working_days(start, end, location)
        
        return jsonify({
            'working_days': working_days,
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/check-overlap', methods=['POST'])
@login_required
def api_check_overlap():
    """API endpoint to check for overlapping leaves"""
    data = request.get_json()
    
    try:
        employee_id = data['employee_id']
        start = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        has_overlap, name, dates = check_overlap(employee_id, start, end)
        
        return jsonify({
            'has_overlap': has_overlap,
            'employee_name': name,
            'dates': [d.strftime('%Y-%m-%d') for d in dates] if dates else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/calendar/events')
@login_required
def api_calendar_events():
    """Get all calendar events (holidays + leaves)"""
    events = []
    
    # Add holidays
    holidays = Holiday.query.all()
    for holiday in holidays:
        color = '#2196F3' if holiday.location == 'UAE' else '#FF9800' if holiday.location == 'India' else '#4CAF50'
        events.append({
            'title': f"🎉 {holiday.name}",
            'start': holiday.date.strftime('%Y-%m-%d'),
            'color': color,
            'type': 'holiday',
            'location': holiday.location
        })
    
    # Add approved leaves
    leaves = LeaveRequest.query.filter_by(status='Approved').all()
    for leave in leaves:
        events.append({
            'title': f"{leave.employee.name} - {leave.leave_type}",
            'start': leave.start_date.strftime('%Y-%m-%d'),
            'end': (leave.end_date + timedelta(days=1)).strftime('%Y-%m-%d'),  # FullCalendar exclusive end
            'color': '#F44336',
            'type': 'leave',
            'employee_name': leave.employee.name,
            'employee_email': leave.employee.email,
            'employee_location': leave.employee.location,
            'stream': leave.employee.stream,
            'leave_type': leave.leave_type,
            'working_days': leave.working_days,
            'status': leave.status
        })
    
    return jsonify({'events': events})


@app.route('/api/admin/approve/<int:leave_id>', methods=['POST'])
@login_required
@scrum_master_required
def api_admin_approve(leave_id):
    """Approve leave request"""
    # EMAIL NOTIFICATIONS DISABLED
    # from email_service import notify_leave_approved
    
    leave_req = LeaveRequest.query.get_or_404(leave_id)
    user = TeamMember.query.get(session['user_id'])
    
    leave_req.status = 'Approved'
    leave_req.approved_by = user.id
    leave_req.approved_at = datetime.utcnow()
    
    db.session.commit()
    
    # Calculate remaining balance
    remaining = leave_req.employee.get_balance(leave_req.leave_type)
    
    # EMAIL NOTIFICATION DISABLED - Employee will check their "My Leaves" page
    # notify_leave_approved(
    #     leave_req.employee.email,
    #     leave_req.employee.name,
    #     leave_req.leave_type,
    #     leave_req.start_date.strftime('%d %b %Y'),
    #     leave_req.end_date.strftime('%d %b %Y'),
    #     leave_req.working_days,
    #     remaining
    # )
    
    return jsonify({'success': True})


@app.route('/api/admin/reject/<int:leave_id>', methods=['POST'])
@login_required
@scrum_master_required
def api_admin_reject(leave_id):
    """Reject leave request"""
    # EMAIL NOTIFICATIONS DISABLED
    # from email_service import notify_leave_rejected
    
    data = request.get_json()
    leave_req = LeaveRequest.query.get_or_404(leave_id)
    
    leave_req.status = 'Rejected'
    leave_req.rejection_reason = data.get('reason', '')
    
    db.session.commit()
    
    # EMAIL NOTIFICATION DISABLED - Employee will check their "My Leaves" page
    # notify_leave_rejected(
    #     leave_req.employee.email,
    #     leave_req.employee.name,
    #     leave_req.leave_type,
    #     leave_req.start_date.strftime('%d %b %Y'),
    #     leave_req.end_date.strftime('%d %b %Y'),
    #     leave_req.rejection_reason
    # )
    
    return jsonify({'success': True})


@app.route('/api/admin/override/<int:leave_id>', methods=['POST'])
@login_required
@scrum_master_required
def api_admin_override(leave_id):
    """Approve leave with manager override"""
    # EMAIL NOTIFICATIONS DISABLED
    # from email_service import notify_manager_override, notify_leave_approved
    
    data = request.get_json()
    leave_req = LeaveRequest.query.get_or_404(leave_id)
    user = TeamMember.query.get(session['user_id'])
    
    leave_req.status = 'Approved'
    leave_req.approved_by = user.id
    leave_req.approved_at = datetime.utcnow()
    leave_req.override_used = True
    leave_req.override_reason = data.get('reason', '')
    
    db.session.commit()
    
    # EMAIL NOTIFICATIONS DISABLED
    # leave_details = f"{leave_req.leave_type} from {leave_req.start_date.strftime('%d %b')} to {leave_req.end_date.strftime('%d %b %Y')} ({leave_req.working_days} days)"
    # notify_manager_override(
    #     leave_req.employee.name,
    #     leave_req.employee.email,
    #     leave_req.override_reason,
    #     leave_details,
    #     user.name
    # )
    
    # remaining = leave_req.employee.get_balance(leave_req.leave_type)
    # notify_leave_approved(
    #     leave_req.employee.email,
    #     leave_req.employee.name,
    #     leave_req.leave_type,
    #     leave_req.start_date.strftime('%d %b %Y'),
    #     leave_req.end_date.strftime('%d %b %Y'),
    #     leave_req.working_days,
    #     remaining
    # )
    
    return jsonify({'success': True})


@app.route('/api/leave/cancel/<int:leave_id>', methods=['POST'])
@login_required
def api_cancel_leave(leave_id):
    """Cancel pending leave request"""
    leave_req = LeaveRequest.query.get_or_404(leave_id)
    
    # Check ownership
    if leave_req.employee_id != session['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    # Can only cancel pending requests
    if leave_req.status != 'Pending':
        return jsonify({'success': False, 'error': 'Can only cancel pending requests'}), 400
    
    db.session.delete(leave_req)
    db.session.commit()
    
    return jsonify({'success': True})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Get port from environment variable (Render uses PORT)
    import os
    port = int(os.environ.get('PORT', 5000))
    
    # Run app
    app.run(debug=False, host='0.0.0.0', port=port)
