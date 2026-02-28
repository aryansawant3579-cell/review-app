# Review Management System - Complete Setup Guide

## Project Overview
A centralized review management system for multi-branch businesses with review aggregation, analytics, and sentiment analysis.

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (Render) or SQLite (local)
- **Frontend**: React with Recharts
- **Authentication**: JWT
- **Hosting**: Render

---

## LOCAL SETUP (Development)

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git
- PostgreSQL (optional, can use SQLite for development)

### Backend Setup

1. **Clone and navigate to project**
   ```bash
   cd review-management-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Create initial admin user** (optional)
   ```python
   python
   >>> from app import app, db, User
   >>> with app.app_context():
   ...     user = User(email='admin@example.com', full_name='Admin', role='admin')
   ...     user.set_password('password123')
   ...     db.session.add(user)
   ...     db.session.commit()
   ```

7. **Run Flask server**
   ```bash
   python app.py
   # Server will run on http://localhost:5000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Setup environment**
   ```bash
   cp .env.example .env
   # Keep default values for local development
   ```

4. **Run React app**
   ```bash
   npm start
   # App will open on http://localhost:3000
   ```

---

## RENDER DEPLOYMENT GUIDE

### Prerequisites
- Render account (https://render.com)
- GitHub repository with code
- PostgreSQL database on Render

### Step 1: Create PostgreSQL Database on Render

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: review-management-db
   - **Database**: review_management
   - **User**: postgres (or custom)
   - **Region**: Choose closest region
   - **Version**: 15+
4. Create and note the connection string

### Step 2: Deploy Flask Backend

1. **Create Backend Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: review-management-api
     - **Environment**: Python 3.11
     - **Build Command**: 
       ```bash
       pip install -r requirements.txt
       ```
     - **Start Command**: 
       ```bash
       gunicorn app:app
       ```
     - **Region**: Same as database
     - **Plan**: Free or Starter

2. **Set Environment Variables** (in Render Dashboard)
   ```
   DATABASE_URL=postgresql://user:password@host:5432/review_management
   JWT_SECRET_KEY=your-strong-random-secret-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

3. **Enable Auto-Deploy**
   - Settings → Auto-Deploy → Enable
   - Choose branch (main/master)

4. **Important Files to Ensure**
   - `requirements.txt` - All dependencies
   - `app.py` - Main Flask application
   - `Procfile` (optional, but recommended):
     ```
     web: gunicorn app:app
     ```

### Step 3: Deploy React Frontend

1. **Build React App Locally**
   ```bash
   cd frontend
   npm run build
   ```

2. **Create Frontend Service on Render**
   - Click "New +" → "Static Site"
   - Connect GitHub repository
   - Configure:
     - **Name**: review-management-dashboard
     - **Build Command**: 
       ```bash
       cd frontend && npm install && npm run build
       ```
     - **Publish Directory**: `frontend/build`
     - **Environment Variables**:
       ```
       REACT_APP_API_URL=https://review-management-api.onrender.com/api
       ```

3. **Add Redirects** (for React Router)
   - Create `frontend/public/_redirects`:
     ```
     /* /index.html 200
     ```

### Step 4: Connect Frontend to Backend

1. Update React environment:
   ```
   REACT_APP_API_URL=https://[your-backend-url]/api
   ```

2. Update Flask CORS configuration (in `app.py`):
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": ["https://[your-frontend-url]"],
           "methods": ["GET", "POST", "PUT", "DELETE"],
           "allow_headers": ["Content-Type", "Authorization"]
       }
   })
   ```

### Step 5: Database Migration on Render

After deploying backend, run migrations:

1. **SSH into Backend Service**
   - Go to Service → Logs → Console
   - Run:
     ```bash
     flask db upgrade
     ```

2. Or use one-off script:
   - Create script in Render's console
   - Execute migration commands

---

## API ENDPOINTS

### Authentication
```
POST   /api/auth/register     - Register new user
POST   /api/auth/login        - Login user
```

### Branches
```
GET    /api/branches          - Get all branches (user specific)
POST   /api/branches          - Create new branch (admin only)
```

### Reviews
```
GET    /api/reviews           - Get all reviews (paginated)
POST   /api/reviews           - Submit new review
GET    /api/reviews/<id>      - Get single review
POST   /api/reviews/<id>/respond      - Respond to review
POST   /api/reviews/<id>/escalate     - Escalate review
```

### Templates
```
GET    /api/templates         - Get all templates
POST   /api/templates         - Create new template
```

### Analytics
```
GET    /api/analytics/dashboard   - Get dashboard metrics
GET    /api/analytics/trends      - Get trend data
```

---

## DEFAULT TEST CREDENTIALS

After setup, use these to test:
```
Email: admin@example.com
Password: password123
```

---

## FEATURE CHECKLIST

### MVP Features ✅
- [x] Centralized Review Dashboard
- [x] Multi-source review aggregation
- [x] Review Categorization
- [x] Response Management
- [x] Analytics & Reporting
- [x] Sentiment Analysis
- [x] Branch-wise Performance

### Bonus Features (Ready to Implement)
- [ ] Deep sentiment insights (use OpenAI API)
- [ ] Escalation workflow alerts
- [ ] WhatsApp/SMS notifications
- [ ] Competitor benchmarking
- [ ] CSAT tracking

---

## SCALING RECOMMENDATIONS

1. **Database Optimization**
   - Add indexes on frequently queried fields
   - Implement caching with Redis
   - Archive old reviews

2. **Backend Performance**
   - Add task queue (Celery) for heavy operations
   - Implement rate limiting
   - Add API versioning

3. **Frontend Optimization**
   - Code splitting and lazy loading
   - Image optimization
   - Service workers for offline mode

4. **Infrastructure**
   - Use CDN for static assets
   - Implement auto-scaling
   - Add monitoring (Sentry, New Relic)

---

## TROUBLESHOOTING

### Database Connection Error
```
Solution: Check DATABASE_URL in environment variables
Format: postgresql://user:password@host:5432/dbname
```

### CORS Errors
```
Solution: Update CORS configuration in Flask to match frontend URL
```

### JWT Errors
```
Solution: Ensure JWT_SECRET_KEY is set in environment
Change to new key: secrets.token_urlsafe(32)
```

### Frontend Not Loading
```
Solution: Check REACT_APP_API_URL in environment
Verify backend service is running and accessible
```

---

## DATABASE SCHEMA

### Users Table
- id, email, password_hash, full_name, role, branch_id, is_active, timestamps

### Branches Table
- id, name, location, branch_code, manager_id, timestamps

### Reviews Table
- id, branch_id, rating, title, content, source, category, sentiment
- customer_name, customer_email, customer_phone, staff_id
- is_responded, response_text, responded_by, responded_at, is_escalated, timestamps

### ReplyTemplates Table
- id, name, template_text, category, sentiment_type, created_by, is_active, created_at

### Analytics Table
- id, branch_id, date, total_reviews, avg_rating, positive/neutral/negative_count, response_rate, created_at

---

## SECURITY BEST PRACTICES

1. Change JWT_SECRET_KEY in production
2. Use HTTPS only
3. Implement rate limiting
4. Add input validation
5. Use prepared statements (already using SQLAlchemy ORM)
6. Regular security audits
7. Keep dependencies updated

---

## SUPPORT & DOCUMENTATION

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- React: https://react.dev/
- Render: https://docs.render.com/

---

## VERSION HISTORY

v1.0.0 - Initial MVP Release
- Core review management
- Multi-source aggregation
- Analytics dashboard
- JWT authentication
