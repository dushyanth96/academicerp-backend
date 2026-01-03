# GitHub Push Instructions

## 1. Create GitHub Repository

I've opened GitHub in your browser. Create a new repository with:

- **Name**: `academicerp-backend` (or your preferred name)
- **Visibility**: Private (recommended) or Public
- **DO NOT** initialize with README, .gitignore, or license (we already have these)

## 2. Push to GitHub

After creating the repository, run these commands:

```bash
# Add GitHub remote (replace YOUR_USERNAME and REPO_NAME with actual values)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push code
git push -u origin main
```

## 3. Deploy to Render

### Option A: Automatic Deployment (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml` and configure everything
5. Set environment variables in Render Dashboard:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_JWT_SECRET`
   - `GEMINI_API_KEY`
   - `DATABASE_URL`
6. Click "Create Web Service"

### Option B: Manual Blueprint

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will use `render.yaml` automatically
5. Set environment variables as above

## 4. Verify Deployment

After deployment completes:

- Check the Render logs for any errors
- Test the API: `https://your-app.onrender.com/health`
- Access Swagger docs: `https://your-app.onrender.com/api/docs`

## Important Notes

- `.env` file is NOT pushed to GitHub (excluded by .gitignore)
- All secrets must be configured in Render's environment variables
- Render free tier may spin down after inactivity (first request will be slower)

## Updating Your Deployment

Any future changes:

```bash
git add .
git commit -m "Your commit message"
git push
```

Render will automatically redeploy on push to main branch.
