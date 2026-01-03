# FASTEST DEPLOYMENT - 2 OPTIONS

## OPTION 1: ngrok (30 SECONDS - Temporary Demo)

**What is it?** Creates a public URL for your local server (already running!)

### Quick Setup:

```bash
# Download ngrok
# Go to: https://ngrok.com/download
# Or install with chocolatey:
choco install ngrok

# Run (while your app.py is running)
ngrok http 5000
```

**You'll get**: `https://abc123.ngrok.io` → Your live API!

✅ **Pros**: 30 seconds, no signup, no CC
❌ **Cons**: URL changes on restart, not permanent

---

## OPTION 2: Replit (3 MINUTES - Permanent & Free)

**What is it?** Online IDE with free hosting, NO credit card

### Steps:

1. Go to: https://replit.com/new/python
2. Click **"Import from GitHub"**
3. Paste: `https://github.com/dushyanth96/academicerp-backend`
4. Click **"Import"**
5. Replit auto-detects Flask
6. Click **"Secrets"** (🔒 icon, left sidebar)
7. Add all env vars as secrets:
   - SUPABASE_URL
   - SUPABASE_KEY
   - SUPABASE_JWT_SECRET
   - GEMINI_API_KEY
   - DATABASE_URL
8. Click **"Run"** button (top)

**You'll get**: `https://academicerp-backend.yourname.repl.co`

✅ **Pros**: Permanent, free, no CC, auto-redeploy on GitHub push
❌ **Cons**: Sleeps after inactivity (10-15 min), slower cold starts

---

## OPTION 3: Render (Workaround for 2 Env Var Limit)

**Solution**: Store all secrets in ONE variable as JSON:

1. Create a `.env.render` file:

```json
{
  "SUPABASE_URL": "...",
  "SUPABASE_KEY": "...",
  "SUPABASE_JWT_SECRET": "...",
  "GEMINI_API_KEY": "...",
  "DATABASE_URL": "..."
}
```

2. In Render, add 1 variable:

   - Key: `APP_SECRETS`
   - Value: (paste the entire JSON)

3. Update `config.py` to parse JSON on startup

---

## MY RECOMMENDATION FOR 5 MIN DEADLINE:

**Use ngrok NOW for demo** → Then migrate to Replit for permanent

```bash
# Terminal 1 (keep running)
python app.py

# Terminal 2 (new terminal)
ngrok http 5000
```

Copy the ngrok URL and you're LIVE! 🚀
