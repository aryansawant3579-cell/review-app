import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Star, MessageSquare, TrendingUp, Users, AlertCircle, Check, Eye, Send } from 'lucide-react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// ============ MAIN APP ============

function App() {
  const [currentPage, setCurrentPage] = useState('login');
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => {
    const t = localStorage.getItem('token');
    return (t && t !== 'undefined' && t !== 'null') ? t : null;
  });

  useEffect(() => {
    if (token) {
      setCurrentPage('dashboard');
    }
  }, [token]);

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    setCurrentPage('login');
  };

  const onAuthError = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setCurrentPage('login');
  };

  const isCollectReviewRoute = window.location.pathname === '/collect-review';

  if (isCollectReviewRoute) {
    return (
      <div className="app">
        <ReviewCollectionForm />
      </div>
    );
  }

  return (
    <div className="app">
      {currentPage === 'login' && !token && (
        <LoginPage setToken={setToken} setUser={setUser} setCurrentPage={setCurrentPage} />
      )}
      {token && (
        <>
          <Navbar user={user} onLogout={handleLogout} setCurrentPage={setCurrentPage} />
          <div className="main-content">
            {currentPage === 'dashboard' && <Dashboard token={token} user={user} onAuthError={onAuthError} />}
            {currentPage === 'reviews' && <ReviewsPage token={token} user={user} onAuthError={onAuthError} />}
            {currentPage === 'analytics' && <AnalyticsPage token={token} user={user} onAuthError={onAuthError} />}
            {currentPage === 'branches' && <BranchesPage token={token} user={user} onAuthError={onAuthError} />}
            {currentPage === 'templates' && <TemplatesPage token={token} user={user} onAuthError={onAuthError} />}
          </div>
        </>
      )}
    </div>
  );
}

// ============ NAVBAR ============

function Navbar({ user, onLogout, setCurrentPage }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h1 className="logo">📊 Review Management System</h1>
        <div className="nav-menu">
          <button onClick={() => setCurrentPage('dashboard')} className="nav-button">Dashboard</button>
          <button onClick={() => setCurrentPage('reviews')} className="nav-button">Reviews</button>
          <button onClick={() => setCurrentPage('analytics')} className="nav-button">Analytics</button>
          <button onClick={() => setCurrentPage('branches')} className="nav-button">Branches</button>
          <button onClick={() => setCurrentPage('templates')} className="nav-button">Templates</button>
        </div>
        <div className="user-section">
          <span className="user-name">{user?.full_name}</span>
          <button onClick={onLogout} className="logout-button">Logout</button>
        </div>
      </div>
    </nav>
  );
}

// ============ LOGIN PAGE ============

function LoginPage({ setToken, setUser, setCurrentPage }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [fullName, setFullName] = useState('');
  const [registerRole, setRegisterRole] = useState('staff');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = isRegister ? '/auth/register' : '/auth/login';
      const payload = isRegister
        ? { email, password, full_name: fullName, role: registerRole }
        : { email, password };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || 'Authentication failed');
        return;
      }

      setToken(data.access_token);
      setUser(data.user);
      localStorage.setItem('token', data.access_token);
      setCurrentPage('dashboard');
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>{isRegister ? 'Create Account' : 'Login'}</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          {isRegister && (
            <>
              <input
                type="text"
                placeholder="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
              <select
                value={registerRole}
                onChange={(e) => setRegisterRole(e.target.value)}
                className="role-select"
              >
                <option value="staff">Staff Member</option>
                <option value="owner">Owner</option>
              </select>
            </>
          )}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : isRegister ? 'Register' : 'Login'}
          </button>
        </form>
        <p className="toggle-auth">
          {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button type="button" onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? 'Login' : 'Register'}
          </button>
        </p>
      </div>
    </div>
  );
}

// ============ DASHBOARD PAGE ============

function Dashboard({ token, user, onAuthError }) {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    const fetchDashboard = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/analytics/dashboard`, {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        if (response.status === 401 || response.status === 422) {
          onAuthError?.();
          return;
        }
        const data = await response.json();
        setDashboard(data);
      } catch (err) {
        console.error('Error fetching dashboard:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, [token]);

  if (!token) return <div className="loading">Loading...</div>;

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <h2>Dashboard Overview</h2>

      <div className="metrics-grid">
        <MetricCard
          icon={<MessageSquare />}
          label="Total Reviews"
          value={dashboard?.total_reviews || 0}
          color="#3498db"
        />
        <MetricCard
          icon={<Star />}
          label="Average Rating"
          value={dashboard?.avg_rating || 0}
          color="#f39c12"
        />
        <MetricCard
          icon={<Check />}
          label="Response Rate"
          value={`${dashboard?.response_rate || 0}%`}
          color="#27ae60"
        />
        <MetricCard
          icon={<TrendingUp />}
          label="Positive Reviews"
          value={dashboard?.sentiments?.positive || 0}
          color="#2ecc71"
        />
      </div>

      <div className="dashboard-charts">
        <div className="chart-container">
          <h3>Sentiment Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Positive', value: dashboard?.sentiments?.positive || 0 },
                  { name: 'Neutral', value: dashboard?.sentiments?.neutral || 0 },
                  { name: 'Negative', value: dashboard?.sentiments?.negative || 0 },
                ]}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                <Cell fill="#2ecc71" />
                <Cell fill="#f39c12" />
                <Cell fill="#e74c3c" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h3>Branch Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dashboard?.branch_stats || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="branch_name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="avg_rating" fill="#3498db" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

// ============ REVIEWS PAGE ============

function ReviewsPage({ token, user, onAuthError }) {
  const [reviews, setReviews] = useState([]);
  const [filters, setFilters] = useState({
    sentiment: '',
    category: '',
    source: '',
    branchId: '',
  });
  const [selectedReview, setSelectedReview] = useState(null);
  const [responseText, setResponseText] = useState('');
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchReviews();
  }, [filters, page]);

  const fetchReviews = async () => {
    try {
      const params = new URLSearchParams({
        page,
        per_page: 10,
        ...Object.fromEntries(Object.entries(filters).filter(([, v]) => v)),
      });

      const response = await fetch(`${API_BASE_URL}/reviews?${params}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.status === 401 || response.status === 422) {
        onAuthError?.();
        return;
      }
      const data = await response.json();
      setReviews(Array.isArray(data.reviews) ? data.reviews : []);
      setTotalPages(data.pages || 1);
    } catch (err) {
      console.error('Error fetching reviews:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRespond = async () => {
    if (!responseText.trim()) return;

    try {
      const response = await fetch(`${API_BASE_URL}/reviews/${selectedReview.id}/respond`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ response_text: responseText }),
      });

      if (response.ok) {
        setResponseText('');
        setSelectedReview(null);
        fetchReviews();
      }
    } catch (err) {
      console.error('Error responding to review:', err);
    }
  };

  const handleEscalate = async (reviewId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/reviews/${reviewId}/escalate`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        fetchReviews();
      }
    } catch (err) {
      console.error('Error escalating review:', err);
    }
  };

  return (
    <div className="reviews-page">
      <h2>All Reviews</h2>

      <div className="filters">
        <select
          value={filters.sentiment}
          onChange={(e) => setFilters({ ...filters, sentiment: e.target.value, page: 1 })}
          className="filter-select"
        >
          <option value="">All Sentiments</option>
          <option value="positive">Positive</option>
          <option value="neutral">Neutral</option>
          <option value="negative">Negative</option>
        </select>

        <select
          value={filters.category}
          onChange={(e) => setFilters({ ...filters, category: e.target.value, page: 1 })}
          className="filter-select"
        >
          <option value="">All Categories</option>
          <option value="food">Food</option>
          <option value="service">Service</option>
          <option value="staff">Staff</option>
          <option value="cleanliness">Cleanliness</option>
          <option value="ambience">Ambience</option>
        </select>

        <select
          value={filters.source}
          onChange={(e) => setFilters({ ...filters, source: e.target.value, page: 1 })}
          className="filter-select"
        >
          <option value="">All Sources</option>
          <option value="google">Google</option>
          <option value="zomato">Zomato</option>
          <option value="internal">Internal</option>
          <option value="whatsapp">WhatsApp</option>
        </select>
      </div>

      <div className="reviews-list">
        {loading ? (
          <div className="loading">Loading reviews...</div>
        ) : reviews.length === 0 ? (
          <div className="no-reviews">No reviews found</div>
        ) : (
          reviews.map((review) => (
            <div key={review.id} className={`review-card sentiment-${review.sentiment}`}>
              <div className="review-header">
                <div className="review-info">
                  <h4>{review.title || 'Untitled Review'}</h4>
                  <p className="review-meta">
                    {review.customer_name} • {review.branch_name} • {review.source}
                  </p>
                </div>
                <div className="rating-badge">⭐ {review.rating}/5</div>
              </div>

              <p className="review-content">{review.content}</p>

              <div className="review-tags">
                <span className={`sentiment-tag ${review.sentiment}`}>{review.sentiment}</span>
                {review.category && <span className="category-tag">{review.category}</span>}
                {review.staff_name && <span className="staff-tag">👤 {review.staff_name}</span>}
              </div>

              {review.is_responded ? (
                <div className="review-response">
                  <strong>Response:</strong> {review.response_text}
                </div>
              ) : (
                <button
                  onClick={() => setSelectedReview(review)}
                  className="respond-button"
                >
                  <Send size={16} /> Respond
                </button>
              )}

              {!review.is_escalated && review.sentiment === 'negative' && (
                <button
                  onClick={() => handleEscalate(review.id)}
                  className="escalate-button"
                >
                  <AlertCircle size={16} /> Escalate
                </button>
              )}

              {review.is_escalated && <span className="escalated-badge">🚨 Escalated</span>}

              <div className="review-date">
                {new Date(review.created_at).toLocaleDateString()}
              </div>
            </div>
          ))
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button onClick={() => setPage(Math.max(1, page - 1))} disabled={page === 1}>
            Previous
          </button>
          <span>Page {page} of {totalPages}</span>
          <button onClick={() => setPage(Math.min(totalPages, page + 1))} disabled={page === totalPages}>
            Next
          </button>
        </div>
      )}

      {selectedReview && (
        <ReviewResponseModal
          review={selectedReview}
          responseText={responseText}
          setResponseText={setResponseText}
          onSubmit={handleRespond}
          onClose={() => setSelectedReview(null)}
        />
      )}
    </div>
  );
}

// ============ ANALYTICS PAGE ============

function AnalyticsPage({ token, user, onAuthError }) {
  const [trends, setTrends] = useState([]);
  const [days, setDays] = useState(30);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrends();
  }, [days]);

  const fetchTrends = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/analytics/trends?days=${days}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.status === 401 || response.status === 422) {
        onAuthError?.();
        return;
      }
      const data = await response.json();
      const chartData = Object.entries(data).map(([date, stats]) => ({
        date,
        ...stats,
      }));
      setTrends(chartData);
    } catch (err) {
      console.error('Error fetching trends:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analytics-page">
      <h2>Analytics & Reports</h2>

      <div className="analytics-controls">
        <label>
          Time Period:
          <select value={days} onChange={(e) => setDays(Number(e.target.value))}>
            <option value={7}>Last 7 Days</option>
            <option value={30}>Last 30 Days</option>
            <option value={90}>Last 90 Days</option>
          </select>
        </label>
      </div>

      {loading ? (
        <div className="loading">Loading analytics...</div>
      ) : (
        <div className="analytics-charts">
          <div className="chart-container">
            <h3>Review Trends</h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="total" stroke="#3498db" name="Total Reviews" />
                <Line type="monotone" dataKey="avg_rating" stroke="#f39c12" name="Avg Rating" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-container">
            <h3>Sentiment Trends</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="positive" fill="#2ecc71" name="Positive" />
                <Bar dataKey="neutral" fill="#f39c12" name="Neutral" />
                <Bar dataKey="negative" fill="#e74c3c" name="Negative" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

// ============ BRANCHES PAGE ============

function BranchesPage({ token, user, onAuthError }) {
  const [branches, setBranches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', location: '', branch_code: '' });

  useEffect(() => {
    fetchBranches();
  }, []);

  const fetchBranches = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/branches`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.status === 401 || response.status === 422) {
        onAuthError?.();
        return;
      }
      const data = await response.json();
      setBranches(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching branches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBranch = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/branches`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setFormData({ name: '', location: '', branch_code: '' });
        setShowForm(false);
        fetchBranches();
      }
    } catch (err) {
      console.error('Error creating branch:', err);
    }
  };

  return (
    <div className="branches-page">
      <h2>Branches</h2>

      {(user?.role === 'admin' || user?.role === 'owner') && (
        <button onClick={() => setShowForm(!showForm)} className="primary-button">
          {showForm ? 'Cancel' : 'Add Branch'}
        </button>
      )}

      {showForm && (
        <form onSubmit={handleCreateBranch} className="branch-form">
          <input
            type="text"
            placeholder="Branch Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Location"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Branch Code"
            value={formData.branch_code}
            onChange={(e) => setFormData({ ...formData, branch_code: e.target.value })}
            required
          />
          <button type="submit">Create Branch</button>
        </form>
      )}

      <div className="branches-grid">
        {loading ? (
          <div className="loading">Loading branches...</div>
        ) : (
          branches.map((branch) => (
            <div key={branch.id} className="branch-card">
              <h3>{branch.name}</h3>
              <p>📍 {branch.location}</p>
              <p>Code: {branch.branch_code}</p>
              <div style={{ marginTop: '1rem', borderTop: '1px solid #eee', paddingTop: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <p style={{ fontSize: '0.8rem', color: '#666', marginBottom: '0.5rem', fontWeight: 'bold' }}>Scan to leave a review</p>
                <img
                  src={`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(window.location.origin + '/collect-review?branch_id=' + branch.id)}`}
                  alt={`QR Code for ${branch.name}`}
                  width="100"
                  height="100"
                  style={{ borderRadius: '8px', border: '1px solid #eee', padding: '4px', background: 'white' }}
                />
                <a
                  href={`/collect-review?branch_id=${branch.id}`}
                  target="_blank"
                  rel="noreferrer"
                  style={{ fontSize: '0.8rem', marginTop: '0.5rem', color: '#3498db', textDecoration: 'none' }}
                >
                  Direct Link
                </a>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

// ============ TEMPLATES PAGE ============

function TemplatesPage({ token, user, onAuthError }) {
  const [templates, setTemplates] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    template_text: '',
    category: '',
    sentiment_type: '',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/templates`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.status === 401 || response.status === 422) {
        onAuthError?.();
        return;
      }
      const data = await response.json();
      setTemplates(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching templates:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/templates`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setFormData({
          name: '',
          template_text: '',
          category: '',
          sentiment_type: '',
        });
        setShowForm(false);
        fetchTemplates();
      }
    } catch (err) {
      console.error('Error creating template:', err);
    }
  };

  return (
    <div className="templates-page">
      <h2>Reply Templates</h2>

      <button onClick={() => setShowForm(!showForm)} className="primary-button">
        {showForm ? 'Cancel' : 'Add Template'}
      </button>

      {showForm && (
        <form onSubmit={handleCreateTemplate} className="template-form">
          <input
            type="text"
            placeholder="Template Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          <textarea
            placeholder="Template Text"
            value={formData.template_text}
            onChange={(e) => setFormData({ ...formData, template_text: e.target.value })}
            required
            rows="4"
          />
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
          >
            <option value="">Select Category</option>
            <option value="food">Food</option>
            <option value="service">Service</option>
            <option value="staff">Staff</option>
            <option value="cleanliness">Cleanliness</option>
            <option value="ambience">Ambience</option>
          </select>
          <select
            value={formData.sentiment_type}
            onChange={(e) => setFormData({ ...formData, sentiment_type: e.target.value })}
          >
            <option value="">Select Sentiment Type</option>
            <option value="positive">Positive</option>
            <option value="neutral">Neutral</option>
            <option value="negative">Negative</option>
          </select>
          <button type="submit">Create Template</button>
        </form>
      )}

      <div className="templates-grid">
        {loading ? (
          <div className="loading">Loading templates...</div>
        ) : (
          templates.map((template) => (
            <div key={template.id} className="template-card">
              <h3>{template.name}</h3>
              <p className="template-text">{template.template_text}</p>
              <div className="template-meta">
                {template.category && <span className="meta-tag">{template.category}</span>}
                {template.sentiment_type && <span className="meta-tag">{template.sentiment_type}</span>}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

// ============ REVIEW COLLECTION FORM ============

function ReviewCollectionForm() {
  const urlParams = new URLSearchParams(window.location.search);
  const initialBranchId = urlParams.get('branch_id') || '';

  const [branches, setBranches] = useState([]);
  const [formData, setFormData] = useState({
    branch_id: initialBranchId ? Number(initialBranchId) : '',
    rating: 5,
    title: '',
    content: '',
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    category: '',
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBranches();
  }, []);

  const fetchBranches = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/public/branches`);
      if (!response.ok) {
        console.error('Failed to fetch public branches');
        return;
      }
      const data = await response.json();
      setBranches(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching branches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, source: 'internal' }),
      });

      if (response.ok) {
        setSubmitted(true);
        setFormData({
          branch_id: '',
          rating: 5,
          title: '',
          content: '',
          customer_name: '',
          customer_email: '',
          customer_phone: '',
          category: '',
        });
        setTimeout(() => setSubmitted(false), 5000);
      }
    } catch (err) {
      console.error('Error submitting review:', err);
    }
  };

  return (
    <div className="review-collection">
      <div className="collection-card">
        <h2>📝 Share Your Feedback</h2>
        <p className="collection-subtitle">Help us improve your experience</p>

        {submitted && <div className="success-message">✅ Thank you for your feedback!</div>}

        <form onSubmit={handleSubmit}>
          {loading ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              <select
                value={formData.branch_id}
                onChange={(e) => setFormData({ ...formData, branch_id: Number(e.target.value) })}
                required
              >
                <option value="">Select Branch</option>
                {branches.map((branch) => (
                  <option key={branch.id} value={branch.id}>
                    {branch.name}
                  </option>
                ))}
              </select>

              <div className="rating-selector">
                <label>How would you rate your experience?</label>
                <div className="stars">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      className={`star ${formData.rating >= star ? 'active' : ''}`}
                      onClick={() => setFormData({ ...formData, rating: star })}
                    >
                      ⭐
                    </button>
                  ))}
                </div>
              </div>

              <input
                type="text"
                placeholder="Review Title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              />

              <textarea
                placeholder="Tell us about your experience..."
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                required
                rows="4"
              />

              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              >
                <option value="">Select Category (Optional)</option>
                <option value="food">Food Quality</option>
                <option value="service">Service</option>
                <option value="staff">Staff Behavior</option>
                <option value="cleanliness">Cleanliness</option>
                <option value="ambience">Ambience</option>
              </select>

              <input
                type="text"
                placeholder="Your Name"
                value={formData.customer_name}
                onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
              />

              <input
                type="email"
                placeholder="Your Email"
                value={formData.customer_email}
                onChange={(e) => setFormData({ ...formData, customer_email: e.target.value })}
              />

              <input
                type="tel"
                placeholder="Your Phone (Optional)"
                value={formData.customer_phone}
                onChange={(e) => setFormData({ ...formData, customer_phone: e.target.value })}
              />

              <button type="submit" className="submit-button">Submit Review</button>
            </>
          )}
        </form>
      </div>
    </div>
  );
}

// ============ HELPER COMPONENTS ============

function MetricCard({ icon, label, value, color }) {
  return (
    <div className="metric-card" style={{ borderLeftColor: color }}>
      <div className="metric-icon" style={{ color }}>
        {icon}
      </div>
      <div className="metric-content">
        <p className="metric-label">{label}</p>
        <p className="metric-value">{value}</p>
      </div>
    </div>
  );
}

function ReviewResponseModal({ review, responseText, setResponseText, onSubmit, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h3>Respond to Review</h3>
        <p className="review-preview">"{review.content}"</p>
        <textarea
          value={responseText}
          onChange={(e) => setResponseText(e.target.value)}
          placeholder="Write your response here..."
          rows="4"
        />
        <div className="modal-buttons">
          <button onClick={onClose} className="cancel-button">Cancel</button>
          <button onClick={onSubmit} className="submit-button">Send Response</button>
        </div>
      </div>
    </div>
  );
}

export default App;
