# webhook-repo

Flask webhook receiver for the TechStaX GitHub Integration Assessment.

## Features
- **POST /webhook** — Receives GitHub Actions events (Push, PR, Merge) and stores in MongoDB
- **GET /events** — Returns all stored events as JSON
- **GET /** — Minimal UI that auto-polls MongoDB every 15 seconds

## Project Structure
```
webhook-repo/
├── app.py              # Flask application (routes and logic)
├── database.py         # MongoDB connection and helpers
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── templates/
│   └── index.html      # UI – polls /events every 15 seconds
└── static/
    └── style.css       # Clean, minimal UI styles
```

## Setup & Run

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/<your-username>/webhook-repo.git
cd webhook-repo
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
copy .env.example .env
# Edit .env with your MongoDB URI
```

### 3. Start MongoDB
Make sure MongoDB is running locally or update `MONGO_URI` in `.env` to point to your MongoDB Atlas cluster.

### 4. Run the Flask App
```bash
python app.py
```
App runs at: `http://localhost:5000`

### 5. Expose to Internet (for GitHub Webhooks)
Use [ngrok](https://ngrok.com/) to expose your local server:
```bash
ngrok http 5000
```
Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.dev`) and set it as the `WEBHOOK_URL` secret in your `action-repo`.

## Webhook Payload Format (received from action-repo)
```json
{
  "request_id": "<commit_sha or PR-<number>>",
  "author": "<github_username>",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "<source_branch>",
  "to_branch": "<target_branch>",
  "timestamp": "<DD Month YYYY - HH:MM AM/PM UTC>"
}
```

## MongoDB Schema
| Field        | Type     | Details                        |
|-------------|----------|--------------------------------|
| `id`         | ObjectID | MongoDB default                |
| `request_id` | string   | Git commit hash or PR ID      |
| `author`     | string   | GitHub username                |
| `action`     | string   | PUSH / PULL_REQUEST / MERGE    |
| `from_branch`| string   | Source branch                  |
| `to_branch`  | string   | Destination branch             |
| `timestamp`  | string   | UTC formatted datetime string  |

## UI Display Formats
- **PUSH:** `{author} pushed to {to_branch} on {timestamp}`
- **PULL_REQUEST:** `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **MERGE:** `{author} merged branch {from_branch} to {to_branch} on {timestamp}`

## Related Repository
- **action-repo**: Dummy repo that triggers GitHub Actions webhook events.
