# AI E-commerce Intelligence Platform

## Vision
Build the world's best e-commerce intelligence platform by scraping real-time product, price, and review data from across the web, using LLMs to generate unique insights and trends, and exposing this data via a scalable API and dashboard. Monetize via paid API access.

## Architecture
- **Scraper**: Python (Scrapy/Playwright) for e-commerce data collection
- **LLM Pipeline**: OpenAI API for summarization and trend detection
- **Backend**: FastAPI (Python) for API endpoints and business logic
- **Frontend**: Next.js (React) dashboard for users
- **Database**: PostgreSQL (hosted, e.g., Supabase)
- **Payments**: Stripe for API key purchase and management

## Features
- Real-time product, price, and review scraping
- LLM-powered trend and sentiment analysis
- API endpoints for products, trends, and reviews
- Dashboard for onboarding, API key management, and demo
- Stripe integration for monetization

## Setup
1. **Clone the repo**
2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables** (see `.env.example`)
5. **Run the backend**
   ```bash
   uvicorn api.main:app --reload
   ```
6. **Run the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Next Steps
- Build scraper and LLM pipeline
- Implement FastAPI backend
- Scaffold Next.js frontend
- Integrate Stripe for payments