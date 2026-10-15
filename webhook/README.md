VYRON Instagram Webhook

A minimal Python Flask server for receiving Meta Instagram webhook events.

Features

- Verifies Meta's webhook callback.
- Validates incoming event signatures.
- Logs event summaries without exposing message text or secrets.

This server does not publish Instagram posts or automatically reply to DMs or comments.

Render deployment

Create a Render Web Service connected to "navinmsbcom-ui/Vyron".

- Branch: "main"
- Root Directory: "webhook"
- Runtime: Python 3
- Build Command: "pip install -r requirements.txt"
- Start Command: "gunicorn app:app --bind 0.0.0.0:$PORT"
- Instance Type: Free, if available

Environment variables

Set these in Render's Environment settings:

- "META_VERIFY_TOKEN" — a private verification string you create.
- "META_APP_SECRET" — your Meta developer app's App Secret.

Never put these secrets in GitHub or share them in chat.

Meta callback

After successful deployment, your callback URL will be:

"https://YOUR-RENDER-SERVICE-URL/webhook"

Replace the placeholder with your actual Render service URL. Use the same verification string configured as "META_VERIFY_TOKEN" when verifying the callback in Meta.

Important

A successful deployment does not guarantee Meta verification or production API access. Test the callback with Meta before relying on it. Additional permissions and implementation are required for automated messaging, comment replies, and publishing.
