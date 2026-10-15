VYRON Instagram Webhook

A minimal Python server for receiving Meta Instagram webhook events.

What it does

- Verifies Meta's webhook callback.
- Checks incoming event signatures.
- Logs safe event summaries without logging message text or secrets.

This server does not automatically publish Instagram posts or reply to DMs.

Render deployment

Create a new Web Service in Render and connect the "navinmsbcom-ui/Vyron" GitHub repository.

Use these settings:

- Branch: "main"
- Root Directory: "webhook"
- Runtime: Python 3
- Build Command: "pip install -r requirements.txt"
- Start Command: "gunicorn app:app --bind 0.0.0.0:$PORT"

Choose the Free instance option if available. Free services may sleep when idle.

Environment variables

In Render's Environment settings, add:

- "META_VERIFY_TOKEN" — a random verification string you create.
- "META_APP_SECRET" — the App Secret from your Meta developer app.

Never publish either secret in GitHub or share them in messages.

Connect Meta

After deployment, your service URL will look similar to:

"https://your-service-name.onrender.com"

Check that the homepage displays "ok".

In Meta's webhook configuration, use this callback URL:

"https://your-service-name.onrender.com/webhook"

Enter the exact same verification string configured as "META_VERIFY_TOKEN", then verify and save.

Important

A successful deployment does not guarantee Meta verification or production access. Test the callback with Meta before relying on it. Further Instagram API permissions and implementation are required for automated messages, comment replies, and publishing.
