"""
Database Initialization Script
Loads team members and holidays into the database
"""

from app import app, db, TeamMember, Holiday, Configuration
from datetime import datetime

def init_database():
    """Initialize database with team members and holidays"""
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Clear existing data (for fresh start)
        print("Clearing existing data...")
        TeamMember.query.delete()
        Holiday.query.delete()
        Configuration.query.delete()
        
        # ====================================================================
        # TEAM MEMBERS
        # ====================================================================
        print("\nAdding team members...")
        
        team_members = [
            # Scrum Masters
            {'name': 'Husam Alhwadi', 'email': 'ObeidH@adx.ae', 'stream': 'Scrum', 'location': 'UAE', 'role': 'scrum_master'},
            {'name': 'Peter Murmylo', 'email': 'MurmyloP@adx.ae', 'stream': 'Scrum', 'location': 'UAE', 'role': 'scrum_master'},
            
            # CRM Team
            {'name': 'Tarun Yadav', 'email': 'YadavT@adx.ae', 'stream': 'CRM', 'location': 'UAE', 'role': 'member'},
            {'name': 'Gunjesh Abhishek', 'email': 'AbhishekG@adx.ae', 'stream': 'CRM', 'location': 'India', 'role': 'member'},
            {'name': 'Anusha Aidam', 'email': 'AidamA@adx.ae', 'stream': 'CRM', 'location': 'India', 'role': 'member'},
            
            # EIP Team
            {'name': 'Ravi Rai', 'email': 'RaiR@adx.ae', 'stream': 'EIP', 'location': 'India', 'role': 'member'},
            {'name': 'Prasad Kale', 'email': 'KaleP@adx.ae', 'stream': 'EIP', 'location': 'India', 'role': 'member'},
            
            # Website Team
            {'name': 'Gopal Sharma', 'email': 'SharmaG@adx.ae', 'stream': 'Website', 'location': 'India', 'role': 'member'},
            {'name': 'Anil Parmar', 'email': 'ParmarA@adx.ae', 'stream': 'Website', 'location': 'India', 'role': 'member'},
            
            # Mobile Team
            {'name': 'Belal Obaid', 'email': 'ObaidB@adx.ae', 'stream': 'Mobile', 'location': 'UAE', 'role': 'member'},
            {'name': 'Sarat Chandra', 'email': 'ChandraS@adx.ae', 'stream': 'Mobile', 'location': 'India', 'role': 'member'},
            
            # QA Team
            {'name': 'Gaurav Arora', 'email': 'AroraG@adx.ae', 'stream': 'QA', 'location': 'India', 'role': 'member'},
            {'name': 'Siddharth Nashine', 'email': 'NashineS@adx.ae', 'stream': 'QA', 'location': 'UAE', 'role': 'member'},
            {'name': 'Chodavarapu Dorababu', 'email': 'DorababuC@adx.ae', 'stream': 'QA', 'location': 'India', 'role': 'member'},
            
            # Sitecore Team
            {'name': 'Roopal Anand', 'email': 'AnandR@adx.ae', 'stream': 'Sitecore', 'location': 'India', 'role': 'member'},
            
            # DevOps Team
            {'name': 'Lakshay Jain', 'email': 'JainL@adx.ae', 'stream': 'Devops', 'location': 'India', 'role': 'member'},
            
            # BA Team
            {'name': 'Anant Sharma', 'email': 'SharmaA@adx.ae', 'stream': 'BA', 'location': 'UAE', 'role': 'member'},
            {'name': 'Saket Upadhyay', 'email': 'UpadhyayS@adx.ae', 'stream': 'BA', 'location': 'UAE', 'role': 'member'},
        ]
        
        for member_data in team_members:
            member = TeamMember(
                name=member_data['name'],
                email=member_data['email'].lower(),
                stream=member_data['stream'],
                location=member_data['location'],
                role=member_data['role'],
                annual_entitlement=22,
                sick_entitlement=10,
                is_active=True
            )
            db.session.add(member)
            print(f"  ✓ Added: {member.name} ({member.stream} - {member.location})")
        
        # ====================================================================
        # HOLIDAYS 2026
        # ====================================================================
        print("\nAdding holidays for 2026...")
        
        holidays = [
            # Both Locations
            {'name': 'New Year', 'date': '2026-01-01', 'location': 'Both', 'color': '#4CAF50'},
            {'name': 'Eid Al Fitr', 'date': '2026-03-20', 'location': 'Both', 'color': '#8BC34A'},
            {'name': 'Eid Al Fitr Holiday', 'date': '2026-03-21', 'location': 'Both', 'color': '#8BC34A'},
            {'name': 'Eid Al Fitr Holiday', 'date': '2026-03-22', 'location': 'Both', 'color': '#8BC34A'},
            {'name': 'Eid Al Adha', 'date': '2026-05-27', 'location': 'Both', 'color': '#8BC34A'},
            {'name': 'Eid Al Adha Holiday', 'date': '2026-05-28', 'location': 'Both', 'color': '#8BC34A'},
            {'name': 'Eid Al Adha Holiday', 'date': '2026-05-29', 'location': 'Both', 'color': '#8BC34A'},
            {'name': 'Islamic New Year', 'date': '2026-06-16', 'location': 'Both', 'color': '#8BC34A'},
            {'name': 'Prophet Birthday', 'date': '2026-08-25', 'location': 'Both', 'color': '#8BC34A'},
            
            # India Only
            {'name': 'Makar Sankranti / Pongal', 'date': '2026-01-14', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Republic Day', 'date': '2026-01-26', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Maha Shivaratri', 'date': '2026-02-15', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Holi', 'date': '2026-03-04', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Ugadi / Gudi Padwa', 'date': '2026-03-19', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Ram Navami', 'date': '2026-03-26', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Mahavir Jayanti', 'date': '2026-03-31', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Good Friday', 'date': '2026-04-03', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Buddha Purnima', 'date': '2026-05-01', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Muharram / Ashura', 'date': '2026-06-26', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Independence Day', 'date': '2026-08-15', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Janmashtami', 'date': '2026-09-04', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Mahatma Gandhi Jayanti', 'date': '2026-10-02', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Dussehra', 'date': '2026-10-20', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Diwali / Deepavali', 'date': '2026-11-08', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Guru Nanak Jayanti', 'date': '2026-11-24', 'location': 'India', 'color': '#FF9800'},
            {'name': 'Christmas Day', 'date': '2026-12-25', 'location': 'India', 'color': '#FF9800'},
            
            # UAE Only
            {'name': 'Al Israa & Al Miraj', 'date': '2026-01-15', 'location': 'UAE', 'color': '#2196F3'},
            {'name': 'Arafat Day', 'date': '2026-05-26', 'location': 'UAE', 'color': '#2196F3'},
            {'name': 'National Day (UAE)', 'date': '2026-12-02', 'location': 'UAE', 'color': '#2196F3'},
            {'name': 'National Day Holiday (UAE)', 'date': '2026-12-03', 'location': 'UAE', 'color': '#2196F3'},
        ]
        
        for holiday_data in holidays:
            holiday = Holiday(
                name=holiday_data['name'],
                date=datetime.strptime(holiday_data['date'], '%Y-%m-%d').date(),
                location=holiday_data['location'],
                color=holiday_data['color']
            )
            db.session.add(holiday)
            print(f"  ✓ Added: {holiday.name} ({holiday.date}) - {holiday.location}")
        
        # ====================================================================
        # SYSTEM CONFIGURATION
        # ====================================================================
        print("\nAdding system configuration...")
        
        configs = [
            {'key': 'annual_leave_days', 'value': '22', 'description': 'Annual leave entitlement in working days'},
            {'key': 'sick_leave_days', 'value': '10', 'description': 'Sick leave entitlement in working days'},
            {'key': 'allow_overlap', 'value': 'false', 'description': 'Allow overlapping leaves in same stream'},
            {'key': 'allow_negative_balance', 'value': 'false', 'description': 'Allow negative leave balance'},
            {'key': 'smtp_configured', 'value': 'true', 'description': 'SMTP email configured'},
        ]
        
        for config_data in configs:
            config = Configuration(
                key=config_data['key'],
                value=config_data['value'],
                description=config_data['description']
            )
            db.session.add(config)
            print(f"  ✓ Config: {config.key} = {config.value}")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*70)
        print("✅ DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*70)
        print(f"\nTeam Members: {TeamMember.query.count()}")
        print(f"  - Scrum Masters: {TeamMember.query.filter_by(role='scrum_master').count()}")
        print(f"  - Team Members: {TeamMember.query.filter_by(role='member').count()}")
        print(f"\nHolidays: {Holiday.query.count()}")
        print(f"  - UAE: {Holiday.query.filter_by(location='UAE').count()}")
        print(f"  - India: {Holiday.query.filter_by(location='India').count()}")
        print(f"  - Both: {Holiday.query.filter_by(location='Both').count()}")
        print(f"\nStreams:")
        streams = db.session.query(TeamMember.stream, db.func.count(TeamMember.id)).filter(
            TeamMember.role == 'member'
        ).group_by(TeamMember.stream).all()
        for stream, count in streams:
            print(f"  - {stream}: {count} members")
        print("\n" + "="*70)


if __name__ == '__main__':
    init_database()
