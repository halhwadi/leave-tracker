# ✅ RENDER DEPLOYMENT - QUICK CHECKLIST

## 🎯 YOUR MISSION: Get Leave Tracker Live in 20 Minutes

---

## BEFORE YOU START

**You Need:**
- [ ] GitHub account (create at github.com if you don't have)
- [ ] Your Outlook email password (or App Password - recommended)
- [ ] 20 minutes of time

---

## STEP 1: PREPARE CODE (2 minutes)

- [ ] Download `leave-tracker-complete.tar.gz`
- [ ] Extract files: `tar -xzf leave-tracker-complete.tar.gz`
- [ ] Open terminal in `leave-tracker` folder

---

## STEP 2: GITHUB (5 minutes)

- [ ] Go to github.com
- [ ] Create new repository: "leave-tracker"
- [ ] Make it Private ✅
- [ ] DO NOT initialize with README
- [ ] Copy the repository URL

**In terminal:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_URL_HERE
git branch -M main
git push -u origin main
```

- [ ] Enter GitHub username/password when prompted
- [ ] Verify code is on GitHub (refresh your repo page)

---

## STEP 3: RENDER.COM (10 minutes)

### Create Account
- [ ] Go to render.com
- [ ] Sign up with GitHub (easiest!)
- [ ] Authorize Render

### Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Select your "leave-tracker" repository
- [ ] Click "Connect"

### Configure Settings
- [ ] Name: `adx-leave-tracker`
- [ ] Region: Singapore or Frankfurt (closest to UAE)
- [ ] Branch: `main`
- [ ] Build Command: `pip install -r requirements.txt && python init_db.py`
- [ ] Start Command: `python app.py`
- [ ] Instance Type: **Free** ✅

### Add Environment Variables
Click "Add Environment Variable" for each:

**Variable 1:**
- [ ] Key: `SMTP_PASSWORD`
- [ ] Value: Your Outlook password

**Variable 2:**
- [ ] Key: `SECRET_KEY`
- [ ] Value: `adx-secret-2026`

**Variable 3:**
- [ ] Key: `PORT`
- [ ] Value: `10000`

### Deploy
- [ ] Click "Create Web Service"
- [ ] Wait 2-3 minutes
- [ ] Watch logs (should see "Database initialized!")
- [ ] Wait for "Your service is live!"

---

## STEP 4: TEST (3 minutes)

- [ ] Copy your Render URL (looks like: https://adx-leave-tracker.onrender.com)
- [ ] Open URL in browser
- [ ] Login with: `ObeidH@adx.ae`
- [ ] You should see dashboard with your name!
- [ ] Check balance shows: 22 annual, 10 sick
- [ ] Click "Request Leave" - form should load
- [ ] Click "Calendar" - should show holidays

✅ **IT WORKS!**

---

## STEP 5: TEST EMAIL (2 minutes)

- [ ] Submit a test leave request
- [ ] Wait 30 seconds
- [ ] Check your email (ObeidH@adx.ae)
- [ ] Should receive "New Leave Request" notification

✅ **EMAILS WORKING!**

---

## STEP 6: ADD TO TEAMS (2 minutes)

- [ ] Open Microsoft Teams
- [ ] Go to your team channel
- [ ] Click "+" to add tab
- [ ] Choose "Website"
- [ ] Name: `Leave Tracker`
- [ ] URL: Your Render URL
- [ ] Save

✅ **IN TEAMS!**

---

## STEP 7: SHARE WITH TEAM (2 minutes)

**Send this email:**

```
Subject: 🎉 Leave Tracker Now Live!

Team,

Our new Leave Tracker is live!

🔗 Link: [YOUR_RENDER_URL]
📧 Login: Your @adx.ae email (no password)

Features:
✅ Submit leave requests
✅ View team calendar
✅ Check your balance
✅ Email notifications

Also in Teams: [Channel] → Leave Tracker tab

Please submit 2026 vacation plans by [DATE].

Questions → Husam or Peter
```

- [ ] Copy template above
- [ ] Replace [YOUR_RENDER_URL] with actual URL
- [ ] Send to team
- [ ] Pin message for visibility

✅ **TEAM NOTIFIED!**

---

## 🎉 YOU'RE DONE!

**Completed:**
- [x] Code on GitHub
- [x] App deployed to Render
- [x] Testing passed
- [x] Emails working
- [x] Added to Teams
- [x] Team notified

---

## 🆘 TROUBLESHOOTING

**Issue: Build fails in Render**
→ Check logs, usually missing file issue
→ Solution: Re-push to GitHub

**Issue: Can't login**
→ Try lowercase: `obeidh@adx.ae`
→ Check database initialized (see logs)

**Issue: No email received**
→ Check spam folder
→ Verify SMTP_PASSWORD is correct
→ Use App Password (not regular password)

**Issue: App sleeping (slow first load)**
→ Normal on free tier
→ App wakes in 30 seconds
→ Upgrade to $7/month for always-on

---

## 📊 WHAT'S NEXT?

**This Week:**
- [ ] Test with Peter (MurmyloP@adx.ae)
- [ ] Test approve/reject workflow
- [ ] Verify all team members can login
- [ ] Monitor for issues

**Next Week:**
- [ ] Collect team feedback
- [ ] Train team on features
- [ ] Set deadline for 2026 vacation planning

**Future:**
- [ ] Add sprint capacity view
- [ ] Export to Excel feature
- [ ] Reports for management

---

## 🔗 USEFUL LINKS

- Your App: [YOUR_RENDER_URL]
- Render Dashboard: https://dashboard.render.com
- GitHub Repo: https://github.com/YOUR_USERNAME/leave-tracker
- Full Docs: RENDER_DEPLOYMENT.md

---

**Time to Complete:** ~20 minutes
**Cost:** $0 (FREE!)
**Result:** Professional leave tracking system ✅

**You did it! 🚀**
