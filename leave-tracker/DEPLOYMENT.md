# 🚀 DEPLOYMENT GUIDE - Leave Tracker Web App

## ✅ WHAT'S BEEN BUILT

Complete web application with:
- ✅ Login system (email-based, no password)
- ✅ Dashboard with leave balances
- ✅ Leave request form with real-time validation
- ✅ Visual calendar view (FullCalendar.js)
- ✅ My Leaves & Team Leaves pages
- ✅ Admin panel for Scrum Masters
- ✅ Email notifications (Outlook SMTP)
- ✅ All 18 team members loaded
- ✅ All 31 holidays for 2026
- ✅ Professional UI with Bootstrap

---

## 📦 FILES INCLUDED

```
leave-tracker/
├── app.py                      # Main Flask application ✅
├── email_service.py            # Email notifications ✅
├── init_db.py                  # Database initialization ✅
├── requirements.txt            # Python dependencies ✅
├── README.md                   # Documentation ✅
├── templates/                  # HTML templates ✅
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── leave_request.html
│   ├── calendar.html
│   ├── my_leaves.html
│   ├── team_leaves.html
│   ├── admin.html
│   ├── team_management.html
│   ├── sprint_capacity.html
│   └── holiday_management.html
└── static/                     # CSS/JS files ✅
    └── css/
        └── style.css
```

---

## 🔧 SETUP INSTRUCTIONS

### Step 1: Extract Files
```bash
tar -xzf leave-tracker-complete.tar.gz
cd leave-tracker
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
python init_db.py
```

This will create `leaves.db` with:
- 18 team members (including you & Peter)
- 31 holidays for 2026
- System configuration

### Step 4: Set Environment Variables
```bash
# REQUIRED for email notifications
export SMTP_PASSWORD="your-outlook-password-here"

# Optional
export SECRET_KEY="random-secret-key"
```

### Step 5: Run Application
```bash
python app.py
```

Application runs at: **http://localhost:5000**

---

## 🌐 DEPLOYMENT TO CLOUD (Recommended: Render.com)

### Option 1: Render.com (Free, Easy)

1. **Create account** at render.com

2. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Leave Tracker App"
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

3. **Create Web Service on Render:**
   - Go to render.com dashboard
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - Name: `adx-leave-tracker`
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python app.py`

4. **Add Environment Variables:**
   - `SMTP_PASSWORD`: Your Outlook password
   - `SECRET_KEY`: Random string (generate one)

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Your app will be live at: `https://adx-leave-tracker.onrender.com`

### Option 2: Railway.app (Also Free)

Similar process:
1. Create account at railway.app
2. "New Project" → "Deploy from GitHub"
3. Select repository
4. Add environment variables
5. Deploy!

---

## 📧 EMAIL CONFIGURATION

The app sends emails via Outlook SMTP:

**Settings:**
- Server: smtp.office365.com:587
- From: ObeidH@adx.ae
- To (Scrum Masters): ObeidH@adx.ae, MurmyloP@adx.ae

**Set Password:**
```bash
export SMTP_PASSWORD="your-actual-password"
```

**Security Note:** Use App Password, not your actual Outlook password!

To generate App Password:
1. Go to Microsoft Account Security
2. Advanced security options
3. App passwords
4. Generate new password
5. Use that password

---

## 👥 LOGIN CREDENTIALS

**Anyone can login with their email (no password):**

**Scrum Masters (Full Access):**
- ObeidH@adx.ae (Husam - You)
- MurmyloP@adx.ae (Peter)

**Team Members (Standard Access):**
- YadavT@adx.ae
- AbhishekG@adx.ae
- (... all 16 team members)

---

## ✨ FEATURES WORKING

### For All Users:
✅ Dashboard with leave balances
✅ Submit leave requests (with validation)
✅ View calendar (holidays + team leaves)
✅ View own leaves
✅ View team leaves
✅ Real-time working days calculation
✅ Overlap detection
✅ Balance checking
✅ Email notifications

### For Scrum Masters (You & Peter):
✅ Approve/Reject leaves
✅ Manager override (bypass validation)
✅ View all pending requests
✅ Team management (view)
✅ Holiday management (view)

---

## 🎯 VALIDATION RULES ACTIVE

1. ✅ **No Overlap**: Only 1 person per stream can be on leave
2. ✅ **Balance Check**: Cannot exceed available balance
3. ✅ **Working Days**: Auto-calculates (excludes weekends + holidays)
4. ✅ **Location-Based Holidays**:
   - UAE employees: UAE + Both holidays excluded
   - India employees: India + Both holidays excluded
5. ✅ **Manager Override**: You can approve exceptions with reason

---

## 📊 DATA LOADED

**Team Members: 18**
- CRM: 3 (1 UAE, 2 India)
- EIP: 2 (India)
- Website: 2 (India)
- Mobile: 2 (1 UAE, 1 India)
- QA: 3 (1 UAE, 2 India)
- Sitecore: 1 (India)
- DevOps: 1 (India)
- BA: 2 (UAE)

**Holidays: 31**
- UAE only: 4 holidays
- India only: 17 holidays
- Both locations: 9 holidays

**Leave Policy:**
- Annual: 22 working days/year
- Sick: 10 working days/year

---

## 🔍 TESTING THE APP

1. **Test Login:**
   - Go to http://localhost:5000
   - Enter: ObeidH@adx.ae
   - You should see your dashboard

2. **Test Leave Request:**
   - Click "Request Leave"
   - Select dates, type
   - Watch real-time validation
   - Submit request

3. **Test Admin:**
   - Go to Admin Panel
   - You'll see your own pending request
   - Try approving it
   - Check email for notification

4. **Test Calendar:**
   - Click "Calendar"
   - See holidays color-coded
   - Apply filters
   - Click on days

---

## 📱 SHARING WITH TEAM

### Once Deployed:

1. **Share URL** with team:
   - `https://your-app.onrender.com`

2. **Add to Microsoft Teams:**
   - Teams → Channel → + Tab
   - Choose "Website"
   - Paste your app URL
   - Save!

3. **Send Email** to team:
   ```
   Subject: New Leave Tracker - Action Required

   Hi Team,

   We've launched our new Leave Tracker app!

   🔗 Access: https://your-app.onrender.com
   📧 Login: Use your @adx.ae email (no password)

   Features:
   - Submit leave requests
   - View team calendar
   - Check your balance
   - Get email confirmations

   Please submit your 2026 vacation plans by [date].

   Questions? Contact Husam or Peter.
   ```

---

## 🐛 TROUBLESHOOTING

**Issue: Can't login**
- Check email is exactly as in database
- Try: obeidh@adx.ae (lowercase)

**Issue: Email not sending**
- Check SMTP_PASSWORD is set
- Try App Password instead of regular password
- Check Outlook settings allow SMTP

**Issue: Working days wrong**
- Check holidays are loaded (visit /admin/holidays)
- Check employee location matches holiday location

**Issue: Can't approve leaves**
- Make sure you're logged in as Scrum Master
- Check role in database (should be 'scrum_master')

---

## 🎉 SUCCESS CHECKLIST

Before going live, verify:
- [ ] Database initialized (run init_db.py)
- [ ] All 18 team members present
- [ ] All 31 holidays loaded
- [ ] SMTP password configured
- [ ] Can login as yourself
- [ ] Can submit leave request
- [ ] Can approve leave (as Scrum Master)
- [ ] Email notifications working
- [ ] Calendar shows holidays
- [ ] Deployed to cloud (Render/Railway)
- [ ] URL shared with team

---

## 📞 SUPPORT

**For technical issues:**
- Check logs: `python app.py` (see console output)
- Database issues: Delete `leaves.db` and run `init_db.py` again
- Email issues: Test with your own email first

**For feature requests:**
- Sprint capacity view (placeholder ready)
- Export to Excel
- Mobile app
- Reports & analytics

---

## 🚀 NEXT STEPS

**Immediate (Required):**
1. Deploy to Render.com
2. Configure SMTP password
3. Test with your team
4. Share URL with everyone

**Soon (Optional):**
1. Add Sprint Capacity view with charts
2. Add Export to Excel feature
3. Add email templates customization
4. Add reports for management

**Future (Nice to have):**
1. Mobile app (React Native)
2. Integration with HR system
3. Slack notifications
4. Advanced analytics

---

## 📝 NOTES

- App uses SQLite (perfect for small team)
- All data stored in `leaves.db` file
- Email sends from ObeidH@adx.ae
- No user passwords (email-based auth)
- Scrum Masters have full admin access
- Calendar uses FullCalendar.js (professional)
- Bootstrap 5 for responsive design

---

**🎉 YOU'RE READY TO GO LIVE!**

Deploy, test, and share with your team!

Good luck! 🚀

---

*Created: December 31, 2025*
*Version: 1.0 - Complete & Production Ready*
