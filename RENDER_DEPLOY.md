# Render Deployment - Quick Reference

## Your GitHub Repository

✅ **Pushed to**: https://github.com/dushyanth96/academicerp-backend.git

## Deploy to Render (Step-by-Step)

### 1. Create Web Service

I've opened Render Dashboard in your browser.

1. Click **"New +"** (top right)
2. Select **"Blueprint"** (recommended - uses render.yaml)
   - OR select **"Web Service"** for manual setup

### 2. Connect Repository

1. Click **"Connect a repository"**
2. Authorize GitHub if needed
3. Search for: `academicerp-backend`
4. Click **"Connect"**

### 3. Configure (Blueprint will auto-fill from render.yaml)

- **Name**: `academicerp-backend`
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: Free (or upgrade for better performance)

### 4. Set Environment Variables

Click **"Environment"** tab and add:

| Key                   | Value                                      | Where to find  |
| --------------------- | ------------------------------------------ | -------------- |
| `SUPABASE_URL`        | `https://qpfrpoucwoavofxtwlcm.supabase.co` | Your .env file |
| `SUPABASE_KEY`        | Your anon key                              | Your .env file |
| `SUPABASE_JWT_SECRET` | Your JWT secret                            | Your .env file |
| `GEMINI_API_KEY`      | Your Gemini key                            | Your .env file |
| `DATABASE_URL`        | Your Supabase DB URL                       | Your .env file |

### 5. Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes first time)
3. Watch the logs for any errors

## After Deployment

### Your Live URL

Render will assign you a URL like: `https://academicerp-backend.onrender.com`

### Test Endpoints

- Health check: `https://your-url.onrender.com/health`
- API docs: `https://your-url.onrender.com/api/docs`
- Login: `https://your-url.onrender.com/api/auth/verify-token`

### Update Frontend

Once deployed, update your frontend's API base URL to point to:
`https://your-url.onrender.com/api`

## Important Notes

⚠️ **Free Tier Limitations:**

- Spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month free (enough for 1 service)

✅ **Auto-Deploy Enabled:**
Any push to `main` branch will automatically redeploy

## Troubleshooting

If deployment fails:

1. Check Render logs for error messages
2. Verify all environment variables are set
3. Ensure `requirements.txt` is up to date
4. Check that `gunicorn` is in requirements.txt

## Future Updates

To update your deployed app:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect the push and redeploy within minutes.
