# Review Management System - Quick Start

## 🚀 Quick Launch (Development)

### 1. Backend (Terminal 1)
```bash
# Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
# Backend running at http://localhost:5000
```

### 2. Frontend (Terminal 2)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start React app
npm start
# Frontend running at http://localhost:3000
```

### 3. Create Test Account
Open the app, register with any email/password:
- Email: test@example.com
- Password: test123456

---

## 📊 Demo Data

### Add a Branch (Admin Only)
1. Login as admin
2. Go to "Branches"
3. Click "Add Branch"
4. Fill in details:
   - Name: Downtown Restaurant
   - Location: New York, NY
   - Branch Code: NYC-001

### Submit a Review
1. Go to "Collect Review"
2. Select branch
3. Rate 1-5 stars
4. Write feedback
5. Submit

### View Dashboard
- See metrics: Total reviews, Avg rating, Response rate
- View sentiment distribution (pie chart)
- Check branch performance

---

## 🔧 Key Features Implemented

### ✅ Core Features
- User authentication with JWT
- Multi-branch management
- Centralized review dashboard
- Sentiment analysis (positive/neutral/negative)
- Review categorization
- Response management
- Analytics with trends

### ✅ API Endpoints
- Authentication (Register/Login)
- CRUD operations for reviews
- Branch management
- Template creation
- Analytics dashboards

### ✅ Frontend Components
- Login/Register pages
- Dashboard with metrics
- Reviews list with filtering
- Analytics charts
- Branch management
- Reply templates
- Mobile-responsive design

---

## 📁 Project Structure

```
review-management-system/
├── app.py                      # Flask backend
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── .env.example               # Environment template
│
├── frontend/
│   ├── App.jsx                # Main React component
│   ├── App.css                # Styling
│   ├── package.json           # React dependencies
│   ├── .env.example          # Frontend config
│   └── public/
│       └── index.html         # HTML entry point
│
└── DEPLOYMENT_GUIDE.md        # Complete deployment docs
```

---

## 🗄️ Database Models

### Users
- email, password_hash, full_name, role (admin/manager/staff)
- branch_id, is_active

### Branches
- name, location, branch_code, manager_id

### Reviews
- branch_id, rating (1-5), title, content, source
- category, sentiment, customer_info
- staff_id, response_text, responded_by, is_escalated

### ReplyTemplates
- name, template_text, category, sentiment_type

### Analytics
- branch_id, date, metrics (avg_rating, sentiment counts, response_rate)

---

## 🔐 Authentication

Using JWT (JSON Web Tokens)
- Login generates access token
- Valid for 30 days
- Send in Authorization header: `Bearer <token>`

---

## 📈 Analytics Features

### Dashboard Metrics
- Total reviews received
- Average rating across all branches
- Response rate percentage
- Sentiment distribution pie chart
- Branch-wise performance comparison

### Trend Analysis
- Last 7/30/90 days view
- Review count trends
- Sentiment trends over time
- Average rating trends

---

## 🎨 UI/UX Features

- Clean, modern dashboard
- Mobile-responsive design
- Color-coded sentiment (🟢 positive, 🟡 neutral, 🔴 negative)
- Real-time filters and search
- Smooth animations and transitions
- Intuitive navigation

---

## 🚀 Rendering on Render.com

### Deploy Backend
1. Push code to GitHub
2. Create Web Service on Render
3. Connect GitHub repo
4. Set environment variables:
   ```
   DATABASE_URL=postgresql://...
   JWT_SECRET_KEY=your-secret
   FLASK_ENV=production
   ```
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`

### Deploy Frontend
1. Create Static Site on Render
2. Connect GitHub repo (frontend directory)
3. Build command: `npm install && npm run build`
4. Publish directory: `build`
5. Set environment:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com/api
   ```

---

## 🐛 Common Issues & Solutions

### Port 5000 already in use
```bash
lsof -i :5000  # Find process
kill -9 <PID>  # Kill process
```

### Module not found error
```bash
pip install -r requirements.txt
```

### CORS errors
- Check backend URL in .env
- Verify frontend and backend are on same network

### Database errors
```bash
# Reset database
rm review_system.db
python app.py  # Recreates database
```

---

## 📚 API Testing

### Test with cURL
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","full_name":"Test"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'

# Get Reviews
curl -X GET http://localhost:5000/api/reviews \
  -H "Authorization: Bearer <token>"
```

---

## 🎯 Next Steps

1. ✅ Setup local environment
2. ✅ Create test accounts
3. ✅ Add sample branches
4. ✅ Submit test reviews
5. ✅ View analytics
6. → Deploy to Render
7. → Setup PostgreSQL database
8. → Configure domain
9. → Enable HTTPS
10. → Monitor in production

---

## 📞 Support

For issues:
1. Check DEPLOYMENT_GUIDE.md
2. Review Flask/React documentation
3. Check Render documentation
4. Review error messages in terminal

---

## 🎉 You're All Set!

Your Review Management System is ready to use!

Start with: `python app.py` and `npm start`
