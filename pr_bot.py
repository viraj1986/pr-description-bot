import os
import sys
import requests
import google.generativeai as genai

# --- Config ---
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
REPO = os.environ["GITHUB_REPOSITORY"]          # e.g. "virajvagal/pr-description-bot"
PR_NUMBER = int(os.environ["PR_NUMBER"])
PR_BODY = os.environ.get("PR_BODY", "").strip()

GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_pr_diff():
    """Fetch the code diff for this PR from GitHub."""
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}"
    headers_diff = {**HEADERS, "Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=headers_diff)
    response.raise_for_status()
    return response.text

def generate_description(diff: str) -> str:
    """Send diff to Gemini and get back a structured PR description."""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-3.6-flash")  # free tier

    # Trim diff if too large (Gemini has a context limit)
    if len(diff) > 30000:
        diff = diff[:30000] + "\n\n[diff truncated for length]"

    prompt = f"""You are a helpful engineering assistant. 
Analyze the following code diff and write a clear, concise pull request description.

Return ONLY the markdown description in this exact format — no extra commentary:

## What changed
[1-3 sentences describing what this PR does]

## Why
[1-2 sentences explaining the reason or problem it solves]

## Testing
[bullet list of how this was or should be tested]

## Checklist
- [ ] Tests added or updated
- [ ] Documentation updated if needed
- [ ] No breaking changes (or breaking changes documented)

---
CODE DIFF:
{diff}
"""

    response = model.generate_content(prompt)
    return response.text

def post_comment(body: str):
    """Post the generated description as a comment on the PR."""
    url = f"{GITHUB_API}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    payload = {
        "body": f"🤖 **AI-generated PR description** (review and copy to description if accurate)\n\n{body}"
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    print(f"✅ Comment posted: {response.json()['html_url']}")

def main():
    # Only run if PR description is empty
    if PR_BODY:
        print("PR already has a description — skipping.")
        sys.exit(0)

    print(f"PR #{PR_NUMBER} has no description. Generating one...")

    diff = get_pr_diff()
    if not diff.strip():
        print("No diff found — skipping.")
        sys.exit(0)

    description = generate_description(diff)
    post_comment(description)

if __name__ == "__main__":
    main()