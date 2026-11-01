# pr-description-bot
GitHub Action that auto-generates PR descriptions using Gemini AI
Open a PR with no description — the bot fills it in within 30 seconds.

## Demo
![PR Description Bot in action](demo.png)

## How it works

1. Developer opens a PR with a blank description
2. GitHub Action triggers automatically  
3. Bot fetches the code diff via GitHub API
4. Sends diff to Gemini 2.0 Flash
5. Gemini returns a structured description
6. Bot updates the PR description field directly

## Setup

1. Fork this repo
2. Add your Gemini API key to repo secrets:
   Settings → Secrets and variables → Actions → New repository secret
   Name: GEMINI_API_KEY
3. Open any PR with a blank description

## Stack
Python · Gemini 2.0 Flash · GitHub Actions · GitHub API

## Cost
$0 — GitHub Actions free tier + Gemini free tier