# Automated Internship Pipeline

A fully self-hosted, automated pipeline that fetches job listings, scores them using Google's Gemini AI, generates tailored PDF resumes using a custom LaTeX microservice, and automatically emails your application!

## 🚀 Architecture
The system consists of two primary Docker containers orchestrated via `docker-compose`:
1. **n8n Automation Engine**: The core logic driver, securely storing credentials via Postgres and mapping an external `.env` file for API keys.
2. **Custom LaTeX API (Alpine)**: A lightweight FastAPI microservice that completely bypasses aggressive OS/network restrictions. It receives raw LaTeX strings and compiles them into professional `.pdf` documents using `pdflatex`.

## ⚙️ Features
* **Job Sourcing**: Continuously scrapes RapidAPI (JSearch / LinkedIn) for role-specific internship postings.
* **AI Scoring**: Passes job descriptions linearly to a Gemini 1.5 Flash Chat Model, rigorously grading role-fit and returning strict JSON outputs.
* **PDF Compilation**: Converts the placeholder string (or your dynamically tailored resume) directly into an `application/pdf` binary.
* **Automated Outreach**: Fully circumvents corporate/institutional SSO blocks via a direct SMTP connection through Google App Passwords to deploy applications instantly.

## 🛠️ How to Run Locally
1. Clone this repository.
2. Initialize your `.env` file with your RapidAPI, Gemini, and Local n8n Basic Auth environment variables.
3. Boot the architecture:
   ```bash
   docker-compose up -d --build
   ```
4. Access `http://localhost:5678`.
5. Import `internship_workflow.json`.
6. Configure the **Send Email** node with your SMTP App Password.
7. Click **Test Workflow** to launch the pipeline!
