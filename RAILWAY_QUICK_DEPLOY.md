# URGENT: Railway Deployment (5 Min Guide)

## Why Railway Instead of Render?
✅ **Unlimited environment variables** on free tier
✅ **$5 free credit/month** (more than Render)
✅ **Faster deployments**
✅ **Auto-detects everything** from GitHub

## Quick Deploy (2 Minutes)

### 1. Sign Up & Deploy
I've opened Railway.app in your browser.

1. **Click "Login with GitHub"** (top right)
2. **Authorize Railway**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose**: `academicerp-backend`
6. **Click "Deploy"**

### 2. Add Environment Variables (1 Minute)
After deployment starts:

1. Click **"Variables"** tab
2. Click **"+ New Variable"** and add ALL of these:

**CRITICAL - Copy these from your .env:**
```
SUPABASE_URL=https://qpfrpoucwoavofxtwlcm.supabase.co
SUPABASE_KEY=<your-key>
SUPABASE_JWT_SECRET=<your-secret>
GEMINI_API_KEY=<your-key>
DATABASE_URL=<your-db-url>
```

3. Railway will **auto-redeploy** when you save

### 3. Get Your URL (30 Seconds)
1. Click **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Generate Domain"**
4. Copy your URL: `https://academicerp-backend-production.up.railway.app`

## Test It
```bash
# Replace with your Railway URL
curl https://your-url.up.railway.app/health
```

## Important Notes
- ✅ Railway has **NO 2-variable limit**
- ✅ **$5 free credit/month** (enough for small apps)
- ✅ **Auto-redeploys** on GitHub push
- ✅ **Better logs** than Render

## Alternative: Vercel (If Railway fails)
```bash
npm i -g vercel
vercel
# Follow prompts, add env vars in dashboard
```

## Alternative: Fly.io (Most generous free tier)
```bash
# Install Fly CLI
iwr https://fly.io/install.ps1 -useb | iex

# Deploy
fly launch
fly secrets set SUPABASE_URL=...
# (Repeat for all vars)
```

---

**TL;DR: Use Railway - it's the fastest with no limits!**
