# 🚀 RENDER.COM DEPLOYMENT GUIDE

## Complete Step-by-Step Instructions to Deploy Your Leave Tracker

---

## ✅ WHAT YOU NEED

1. **GitHub Account** (free) - to store code
2. **Render.com Account** (free) - to host app
3. **Your Outlook Password** - for email notifications

**Time Required:** 15-20 minutes

---

## 📋 STEP-BY-STEP PROCESS

### **PHASE 1: PREPARE YOUR CODE**

#### Step 1: Download & Extract Files

1. Download `leave-tracker-complete.tar.gz` from above
2. Extract to a folder:
   ```bash
   tar -xzf leave-tracker-complete.tar.gz
   cd leave-tracker
   ```

#### Step 2: Test Locally (Optional but Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Set password (temporary for testing)
export SMTP_PASSWORD="your-password"

# Run app
python app.py
```

Open browser: http://localhost:5000
Login with: ObeidH@adx.ae

**If it works locally, it will work on Render!**

---

### **PHASE 2: PUSH TO GITHUB**

#### Step 3: Create GitHub Repository

1. **Go to GitHub.com**
2. **Login** (or create free account)
3. **Click "New Repository"** (green button, top right)
4. **Repository settings:**
   - Name: `leave-tracker`
   - Description: `ADX Team Leave Management System`
   - Visibility: **Private** (recommended) or Public
   - **DO NOT** initialize with README
5. **Click "Create Repository"**

#### Step 4: Push Code to GitHub

**In your terminal (inside leave-tracker folder):**

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Leave Tracker App"

# Connect to GitHub (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/leave-tracker.git

# Push code
git branch -M main
git push -u origin main
```

**Enter your GitHub credentials when prompted**

✅ **Your code is now on GitHub!**

---

### **PHASE 3: DEPLOY TO RENDER**

#### Step 5: Create Render Account

1. **Go to:** https://render.com
2. **Click "Get Started for Free"**
3. **Sign up with GitHub** (easiest option)
4. **Authorize Render** to access your GitHub

✅ **You're in Render Dashboard!**

#### Step 6: Create New Web Service

1. **Click "New +"** (top right)
2. **Select "Web Service"**
3. **Connect Repository:**
   - You'll see your GitHub repositories
   - Find and **select "leave-tracker"**
   - Click **"Connect"**

#### Step 7: Configure Web Service

**Fill in these settings:**

| Setting | Value |
|---------|-------|
| **Name** | `adx-leave-tracker` (or any name you want) |
| **Region** | Choose closest to UAE (e.g., Singapore, Frankfurt) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python init_db.py` |
| **Start Command** | `python app.py` |
| **Instance Type** | **Free** |

**Scroll down to Environment Variables section...**

#### Step 8: Add Environment Variables

Click **"Add Environment Variable"** button and add:

**Variable 1:**
- Key: `SMTP_PASSWORD`
- Value: `your-outlook-password-here`

**Variable 2:**
- Key: `SECRET_KEY`
- Value: `adx-leave-tracker-secret-2026` (or any random string)

**Variable 3:**
- Key: `PORT`
- Value: `10000`

#### Step 9: Deploy!

1. **Click "Create Web Service"** (bottom of page)
2. **Wait 2-3 minutes** for deployment
3. Watch the logs (you'll see build progress)

**You'll see:**
```
Building...
Installing dependencies...
Initializing database...
Database initialized successfully!
Starting application...
Your service is live!
```

✅ **YOUR APP IS LIVE!** 🎉

---

### **PHASE 4: ACCESS YOUR APP**

#### Step 10: Get Your URL

Render will give you a URL like:
```
https://adx-leave-tracker.onrender.com
```

**Copy this URL - this is your app!**

#### Step 11: Test Your App

1. **Open your URL** in browser
2. **Login with:** ObeidH@adx.ae
3. **You should see your dashboard!**

---

### **PHASE 5: SHARE WITH TEAM**

#### Step 12: Test Email Notifications

1. Submit a leave request
2. Check your email (ObeidH@adx.ae)
3. You should receive notification!

If emails work ✅ everything is working!

#### Step 13: Add to Microsoft Teams

1. **Open Microsoft Teams**
2. **Go to your team channel**
3. **Click "+" tab** at top
4. **Choose "Website"**
5. **Enter:**
   - Name: `Leave Tracker`
   - URL: `https://adx-leave-tracker.onrender.com`
6. **Save**

✅ **Team can now access from Teams!**

#### Step 14: Announce to Team

**Send email to team:**

```
Subject: 🎉 New Leave Tracker System - Now Live!

Hi Team,

Our new Leave Tracker is now live!

🔗 Access: https://adx-leave-tracker.onrender.com
📧 Login: Use your @adx.ae email (no password needed)

What you can do:
✅ Submit annual & sick leave requests
✅ View team calendar with holidays
✅ Check your leave balance
✅ Get email confirmations

Please submit your 2026 vacation plans by [DATE].

Also available in Microsoft Teams under [Channel Name] → Leave Tracker tab

Questions? Contact Husam or Peter.

Happy leave planning! 🌴
```

---

## 🔧 TROUBLESHOOTING

### **Issue: Build Failed**

**Check logs in Render dashboard**

Common fixes:
- Make sure `requirements.txt` exists
- Check `runtime.txt` has `python-3.11.0`

### **Issue: App Not Loading**

- Wait 2-3 minutes after first deploy (Render takes time)
- Check logs for errors
- Restart service in Render dashboard

### **Issue: Emails Not Sending**

1. **Check SMTP_PASSWORD is correct**
2. **Use App Password, not regular password:**
   - Go to: https://account.microsoft.com
   - Security → Advanced security options
   - App passwords → Generate new
   - Use that password in Render

3. **Test SMTP manually:**
   - In Render dashboard → Shell
   - Run: `python`
   - Test email service

### **Issue: Database Not Initialized**

- Check build logs, should see "Database initialized successfully!"
- If missing, manually run in Render Shell:
  ```bash
  python init_db.py
  ```

### **Issue: Can't Login**

- Email must be exact: `ObeidH@adx.ae` (case-sensitive)
- Try lowercase: `obeidh@adx.ae`
- Check database has users (Render Shell → `python init_db.py`)

---

## 📊 RENDER FREE TIER LIMITS

**What you get FREE:**
✅ 750 hours/month (enough for 24/7 for small team)
✅ 512 MB RAM
✅ SSL certificate (HTTPS)
✅ Custom domains
✅ Automatic deploys from GitHub
✅ No credit card required

**Limitations:**
⚠️ App sleeps after 15 mins of inactivity (wakes up in ~30 seconds on first visit)
⚠️ Free tier services may restart occasionally

**For production (paid, $7/month):**
- App never sleeps
- More resources
- Faster performance

---

## 🔄 UPDATING YOUR APP

**To make changes later:**

1. Edit code locally
2. Commit changes:
   ```bash
   git add .
   git commit -m "Updated feature X"
   git push
   ```
3. **Render auto-deploys!** (sees GitHub push)
4. Wait 2-3 minutes
5. Changes are live!

---

## 🎯 POST-DEPLOYMENT CHECKLIST

After deploying, verify:

- [ ] App URL loads correctly
- [ ] Can login as ObeidH@adx.ae
- [ ] Dashboard shows correct balance (22 annual, 10 sick)
- [ ] Can submit leave request
- [ ] Validation works (try invalid dates)
- [ ] Calendar shows holidays
- [ ] Can view team leaves
- [ ] Email notification received (check spam!)
- [ ] Can approve leave (as Scrum Master)
- [ ] Peter can login as MurmyloP@adx.ae
- [ ] Added to Microsoft Teams
- [ ] URL shared with team

---

## 📈 MONITORING YOUR APP

**Render Dashboard shows:**
- Deployment logs
- Application logs
- Metrics (CPU, Memory, Requests)
- Uptime status

**Check regularly:**
- Logs for errors
- Email delivery
- User activity

---

## 💡 PRO TIPS

1. **Bookmark your Render dashboard**
2. **Keep GitHub repo private** (contains team data)
3. **Use App Password** for SMTP (not regular password)
4. **Check logs weekly** for issues
5. **Backup database** occasionally:
   - Render Shell → Download `leaves.db`
6. **Test before big announcements**

---

## 🆘 NEED HELP?

**Render Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com

**For this app:**
- Check logs in Render dashboard
- Review DEPLOYMENT.md
- Test locally first

---

## 🎉 SUMMARY - YOU'RE DONE!

**What you accomplished:**

✅ Created GitHub repository
✅ Pushed code to GitHub
✅ Created Render account
✅ Deployed web app
✅ Got public URL
✅ Configured email notifications
✅ Added to Microsoft Teams
✅ Shared with team

**Your app is now:**
- 🌐 Live on the internet
- 🔒 Secure (HTTPS)
- 📧 Sending email notifications
- 👥 Accessible to your team
- 🔄 Auto-updating from GitHub
- 💰 Free (Render free tier)

---

**Congratulations! Your Leave Tracker is LIVE! 🚀**

*Any issues? Check logs and troubleshooting section above.*

---

**Next Steps:**
1. Test all features
2. Train your team
3. Start tracking leaves!

**Happy Leave Planning! 🌴**
