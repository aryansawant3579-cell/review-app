# 📊 Review Management System

A comprehensive, centralized review management platform for multi-branch businesses. Aggregates reviews from multiple sources, provides sentiment analysis, and enables efficient response management.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-green)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Features

### Core Features
- ✅ **Centralized Dashboard**: View all reviews from multiple sources in one place
- ✅ **Multi-Source Integration**: Google, Zomato, internal forms, WhatsApp
- ✅ **Review Collection**: Mobile-friendly form with QR code support
- ✅ **Sentiment Analysis**: Automatic classification as positive/neutral/negative
- ✅ **Auto-Categorization**: Food, Service, Staff, Cleanliness, Ambience
- ✅ **Response Management**: Predefined templates and AI-assisted suggestions
- ✅ **Analytics Dashboard**: Branch-wise and staff-wise performance insights
- ✅ **Real-time Updates**: Live review synchronization across branches

### Advanced Features
- 🔐 **JWT Authentication**: Secure user sessions with role-based access control
- 📊 **Trend Analysis**: Monitor sentiment and rating trends over time
- 🚨 **Escalation System**: Automatic flagging of negative reviews
- 👥 **Multi-User Support**: Admin, Manager, and Staff roles
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🔄 **Bulk Operations**: Manage multiple reviews simultaneously

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React)                       │
│         Dashboard | Reviews | Analytics | Settings      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────┐
│               API Gateway (Flask)                        │
│  Auth | Reviews | Branches | Templates | Analytics      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Database (PostgreSQL)                   │
│  Users | Branches | Reviews | Templates | Analytics     │
└─────────────────────────────────────────────────────────┘
```

## 📋 API Endpoints

### Authentication
```
POST   /api/auth/register        Register new user
POST   /api/auth/login           User login
```

### Branches
```
GET    /api/branches             Get all branches
POST   /api/branches             Create new branch
```

### Reviews
```
GET    /api/reviews              Get reviews with filters
POST   /api/reviews              Submit new review
GET    /api/reviews/<id>         Get review details
POST   /api/reviews/<id>/respond Respond to review
POST   /api/reviews/<id>/escalate Escalate review
```

### Templates
```
GET    /api/templates            Get all templates
POST   /api/templates            Create new template
```

### Analytics
```
GET    /api/analytics/dashboard  Dashboard metrics
GET    /api/analytics/trends     Trend data
```

## 📦 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email VARCHAR(120) UNIQUE,
  password_hash VARCHAR(255),
  full_name VARCHAR(120),
  role VARCHAR(50),  -- 'admin', 'manager', 'staff'
  branch_id INTEGER,
  is_active BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Reviews Table
```sql
CREATE TABLE reviews (
  id INTEGER PRIMARY KEY,
  branch_id INTEGER,
  rating INTEGER,  -- 1-5
  title VARCHAR(255),
  content TEXT,
  source VARCHAR(50),  -- 'google', 'zomato', 'internal'
  category VARCHAR(100),  -- 'food', 'service', 'staff', etc.
  sentiment VARCHAR(50),  -- 'positive', 'neutral', 'negative'
  customer_name VARCHAR(120),
  customer_email VARCHAR(120),
  customer_phone VARCHAR(20),
  staff_id INTEGER,
  is_responded BOOLEAN,
  response_text TEXT,
  responded_by INTEGER,
  responded_at TIMESTAMP,
  is_escalated BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Branches Table
```sql
CREATE TABLE branches (
  id INTEGER PRIMARY KEY,
  name VARCHAR(120),
  location VARCHAR(255),
  branch_code VARCHAR(50) UNIQUE,
  manager_id INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- Git
- PostgreSQL 13+ (for production) or SQLite (for development)

### Development Setup

**1. Clone the repository**
```bash
git clone <repository-url>
cd review-management-system
```

**2. Backend Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run Flask server
python app.py
# Server running at http://localhost:5000
```

**3. Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Keep default values for local development

# Start React app
npm start
# App running at http://localhost:3000
```

**4. Create Test Account**
- Open http://localhost:3000
- Click "Register"
- Create account with any email/password
- Login and explore the dashboard

## 🌐 Deployment to Render

### Backend Deployment

1. **Create PostgreSQL Database on Render**
   - Go to Render Dashboard
   - New → PostgreSQL
   - Note the connection string

2. **Deploy Flask Backend**
   - New → Web Service
   - Connect GitHub repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Environment variables:
     ```
     DATABASE_URL=postgresql://...
     JWT_SECRET_KEY=your-secret-key
     FLASK_ENV=production
     ```

3. **Deploy React Frontend**
   - New → Static Site
   - Connect GitHub (frontend directory)
   - Build command: `npm install && npm run build`
   - Publish directory: `build`
   - Environment:
     ```
     REACT_APP_API_URL=https://your-backend-url/api
     ```

## 📊 Sample Data

```bash
# Create admin user
python -c "
from app import app, db, User
with app.app_context():
    user = User(
        email='admin@example.com',
        full_name='Administrator',
        role='admin'
    )
    user.set_password('admin123')
    db.session.add(user)
    db.session.commit()
    print('Admin user created!')
"
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing
- **Role-Based Access Control**: Admin, Manager, Staff roles
- **CORS Protection**: Cross-origin request handling
- **Environment Variables**: Sensitive data in .env files
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📈 Analytics

The system provides comprehensive analytics including:

### Dashboard Metrics
- Total reviews received
- Average rating (1-5)
- Response rate (percentage)
- Sentiment distribution (positive/neutral/negative)
- Branch-wise performance comparison

### Trend Analysis
- 7, 30, or 90-day trends
- Review volume trends
- Sentiment trends over time
- Rating trends

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask 3.0 |
| Frontend | React 18.2 |
| Database | PostgreSQL 15+ |
| Authentication | JWT |
| Charts | Recharts |
| Icons | Lucide React |
| ORM | SQLAlchemy |
| Styling | CSS3 |
| Hosting | Render |

## 📚 Project Structure

```
review-management-system/
│
├── app.py                          # Flask main application
├── requirements.txt                # Python dependencies
├── Procfile                        # Render deployment config
├── .env.example                    # Environment template
│
├── frontend/
│   ├── App.jsx                     # Main React component
│   ├── App.css                     # Styling
│   ├── package.json                # Node dependencies
│   ├── .env.example               # Frontend config
│   └── public/
│       ├── index.html             # HTML entry
│       └── favicon.ico
│
├── DEPLOYMENT_GUIDE.md             # Detailed deployment docs
├── QUICKSTART.md                   # Quick start guide
└── README.md                       # This file
```

## 🔧 Configuration

### Environment Variables (Backend)

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# JWT
JWT_SECRET_KEY=your-secret-key-change-this

# Server
SERVER_NAME=localhost:5000
```

### Environment Variables (Frontend)

```bash
# API Configuration
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Database Connection Error
- Check DATABASE_URL format
- Verify database is running
- Check user credentials

### CORS Errors
- Update CORS configuration in Flask
- Verify backend and frontend URLs

### Module Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Node Modules Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📝 API Examples

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "pass123",
    "full_name": "User Name",
    "role": "staff"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "pass123"
  }'
```

### Submit Review
```bash
curl -X POST http://localhost:5000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "branch_id": 1,
    "rating": 5,
    "title": "Great Experience",
    "content": "Amazing service and food!",
    "source": "internal",
    "customer_name": "John Doe",
    "customer_email": "john@example.com"
  }'
```

### Get Reviews with Filter
```bash
curl -X GET "http://localhost:5000/api/reviews?branch_id=1&sentiment=positive" \
  -H "Authorization: Bearer <token>"
```

## 🚀 Performance Optimization

### Database
- Implement indexing on frequently queried fields
- Use pagination for large datasets
- Cache analytics results

### Frontend
- Code splitting and lazy loading
- Image optimization
- Service workers for offline mode

### Backend
- Implement caching (Redis)
- Use task queues (Celery) for heavy operations
- Rate limiting for API endpoints

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop browsers (1920x1080+)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

Review collection form is optimized for mobile touch interactions.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the DEPLOYMENT_GUIDE.md
- Review Flask documentation: https://flask.palletsprojects.com/
- React documentation: https://react.dev/
- Render documentation: https://docs.render.com/

## 🎉 Acknowledgments

- Built with Flask and React
- Charts powered by Recharts
- Icons from Lucide React
- Deployed on Render

---

**Ready to get started?** Follow the [Quick Start](#-quick-start) guide above!

**Need detailed setup?** Check out [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Questions?** Check [QUICKSTART.md](QUICKSTART.md) for common issues
