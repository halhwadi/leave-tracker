# Leave Tracker Web Application

Professional leave management system for ADX Team with calendar view and sprint capacity planning.

**⚠️ NOTE: Email notifications are DISABLED in this version for security/simplicity. Team members notify Scrum Masters directly via Teams/Slack.**

## Features

✅ **Leave Management**
- Submit annual and sick leave requests
- Real-time balance checking
- Overlap detection (same stream)
- Location-based holiday calculation (UAE/India)

✅ **No Email Notifications** (Simplified Version)
- Team notifies Scrum Masters directly (Teams/Slack)
- Employees check "My Leaves" page for status updates
- Simpler deployment, no IT security concerns

✅ **Calendar View**
- Visual monthly calendar
- Color-coded holidays (UAE blue, India orange, Both green)
- Team leaves displayed
- Click day for details

✅ **Sprint Capacity Planning**
- Calculate team availability
- Include holidays + vacations
- Per-stream capacity tracking

✅ **Admin Panel** (Scrum Masters only)
- Approve/reject leaves
- Override validations (with reason)
- Manage team members
- Manage holidays
- Configure leave policies

## Team

**18 Members across 8 Streams:**
- CRM (3), EIP (2), Website (2), Mobile (2)
- QA (3), Sitecore (1), DevOps (1), BA (2)

**Scrum Masters:**
- Husam Alhwadi (ObeidH@adx.ae)
- Peter Murmylo (MurmyloP@adx.ae)

## Technology Stack

- **Backend:** Python Flask
- **Database:** SQLite
- **Email:** Outlook SMTP (smtp.office365.com)
- **Frontend:** HTML/CSS/JavaScript + Bootstrap
- **Calendar:** FullCalendar.js

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Required
export SECRET_KEY="your-secret-key"

# Optional (has defaults)
export PORT="5000"
```

**Note:** No SMTP_PASSWORD needed - email notifications disabled!

### 3. Initialize Database

```bash
python init_db.py
```

This creates the database and loads:
- 18 team members
- 31 holidays for 2026 (UAE/India/Both)
- System configuration

### 4. Run Application

```bash
python app.py
```

Application will be available at: `http://localhost:5000`

## Login

Use any team member email to login:
- `ObeidH@adx.ae` (Scrum Master - Full access)
- `MurmyloP@adx.ae` (Scrum Master - Full access)
- Any team member email (Standard access)

**No password required** - email-based authentication.

## File Structure

```
leave-tracker/
├── app.py                  # Main Flask application
├── email_service.py        # Email notification service
├── init_db.py             # Database initialization
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates (to be created)
│   ├── login.html
│   ├── dashboard.html
│   ├── calendar.html
│   ├── leave_request.html
│   ├── admin.html
│   └── team_management.html
├── static/                # CSS/JS files (to be created)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── calendar.js
└── data/
    └── leaves.db          # SQLite database (created after init)
```

## Deployment Options

### Option 1: Render.com (Free, Recommended)

1. Create account at render.com
2. Connect GitHub repository
3. Create New Web Service
4. Set environment variables:
   - `SMTP_PASSWORD`: Your Outlook password
5. Deploy!

URL will be: `https://your-app-name.onrender.com`

### Option 2: Railway.app (Free)

1. Create account at railway.app
2. New Project → Deploy from GitHub
3. Add environment variables
4. Deploy!

### Option 3: Docker (Your Company Server)

```bash
# Build Docker image
docker build -t leave-tracker .

# Run container
docker run -d -p 5000:5000 \
  -e SMTP_PASSWORD="your-password" \
  -v $(pwd)/data:/app/data \
  leave-tracker
```

## Email Configuration

The app sends emails via Outlook SMTP:

- **Server:** smtp.office365.com:587
- **From:** ObeidH@adx.ae
- **To (Scrum Masters):** ObeidH@adx.ae, MurmyloP@adx.ae

**Set password:**
```bash
export SMTP_PASSWORD="your-outlook-password"
```

## Leave Policies

**Entitlements:**
- Annual Leave: 22 working days/year
- Sick Leave: 10 working days/year

**Validations:**
- No overlap: Only 1 person per stream can be on leave at same time
- Balance check: Cannot exceed available balance
- Both can be overridden by Scrum Masters with reason

**Working Days Calculation:**
- Excludes weekends (Saturday-Sunday)
- Excludes location-based holidays
- UAE employees: UAE + Both holidays excluded
- India employees: India + Both holidays excluded

## Holidays 2026

**31 Holidays:**
- 9 holidays for Both locations
- 17 holidays for India only
- 4 holidays for UAE only

All loaded automatically during database initialization.

## Support

For issues or questions:
- Contact: Husam Alhwadi (ObeidH@adx.ae)
- Or: Peter Murmylo (MurmyloP@adx.ae)

## Next Steps

After basic app is running, we'll add:
1. HTML templates (login, dashboard, calendar, etc.)
2. CSS styling (professional UI)
3. JavaScript for calendar view
4. Additional admin features
5. Reports and analytics
6. Export to Excel

---

**Status:** ✅ Core backend complete - Ready for frontend development
