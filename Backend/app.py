from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime, timedelta
from functools import wraps
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration - use absolute path so app and seed scripts share the same DB
_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review_system.db').replace('\\', '/')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{_db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# ============ DATABASE MODELS ============

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='staff')  # admin, manager, staff
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    branch = db.relationship('Branch', foreign_keys=[branch_id], backref='staff_members')
    reviews_responded = db.relationship('Review', backref='responder', foreign_keys='Review.responded_by')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'branch_id': self.branch_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class Branch(db.Model):
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    branch_code = db.Column(db.String(50), unique=True, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    manager = db.relationship('User', foreign_keys=[manager_id])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='branch', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'branch_code': self.branch_code,
            'manager_id': self.manager_id,
            'created_at': self.created_at.isoformat()
        }


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50), nullable=False)  # google, zomato, internal, whatsapp
    category = db.Column(db.String(100))  # food, service, staff, cleanliness, ambience
    sentiment = db.Column(db.String(50))  # positive, neutral, negative
    customer_name = db.Column(db.String(120))
    customer_email = db.Column(db.String(120))
    customer_phone = db.Column(db.String(20))
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_responded = db.Column(db.Boolean, default=False)
    response_text = db.Column(db.Text)
    responded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    responded_at = db.Column(db.DateTime)
    is_escalated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    staff = db.relationship('User', foreign_keys=[staff_id], backref='reviews_tagged')
    
    def to_dict(self):
        return {
            'id': self.id,
            'branch_id': self.branch_id,
            'branch_name': self.branch.name if self.branch else None,
            'rating': self.rating,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'category': self.category,
            'sentiment': self.sentiment,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'staff_id': self.staff_id,
            'staff_name': self.staff.full_name if self.staff else None,
            'is_responded': self.is_responded,
            'response_text': self.response_text,
            'responded_by': self.responded_by,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'is_escalated': self.is_escalated,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ReplyTemplate(db.Model):
    __tablename__ = 'reply_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    template_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    sentiment_type = db.Column(db.String(50))  # positive, neutral, negative
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'template_text': self.template_text,
            'category': self.category,
            'sentiment_type': self.sentiment_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_reviews = db.Column(db.Integer, default=0)
    avg_rating = db.Column(db.Float, default=0.0)
    positive_count = db.Column(db.Integer, default=0)
    neutral_count = db.Column(db.Integer, default=0)
    negative_count = db.Column(db.Integer, default=0)
    response_rate = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    branch = db.relationship('Branch')
    
    def to_dict(self):
        return {
            'id': self.id,
            'branch_id': self.branch_id,
            'date': self.date.isoformat(),
            'total_reviews': self.total_reviews,
            'avg_rating': self.avg_rating,
            'positive_count': self.positive_count,
            'neutral_count': self.neutral_count,
            'negative_count': self.negative_count,
            'response_rate': self.response_rate
        }


# ============ AUTHENTICATION ROUTES ============

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists'}), 400
        
        role = data.get('role', 'staff')
        if role not in ('staff', 'owner'):
            role = 'staff'
        
        user = User(
            email=data['email'],
            full_name=data.get('full_name', ''),
            role=role,
            branch_id=data.get('branch_id')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing credentials'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'message': 'User account is inactive'}), 403
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# ============ BRANCH ROUTES ============

@app.route('/api/branches', methods=['GET'])
@jwt_required()
def get_branches():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if user.role in ('admin', 'owner'):
            branches = Branch.query.all()
        else:
            branches = Branch.query.filter_by(manager_id=current_user_id).all()
        
        return jsonify([branch.to_dict() for branch in branches]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/public/branches', methods=['GET'])
def get_public_branches():
    try:
        branches = Branch.query.all()
        return jsonify([{'id': b.id, 'name': b.name, 'location': b.location} for b in branches]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/branches', methods=['POST'])
@jwt_required()
def create_branch():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if user.role not in ('admin', 'owner'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if Branch.query.filter_by(branch_code=data['branch_code']).first():
            return jsonify({'message': 'Branch code already exists'}), 400
        
        branch = Branch(
            name=data['name'],
            location=data['location'],
            branch_code=data['branch_code'],
            manager_id=data.get('manager_id')
        )
        
        db.session.add(branch)
        db.session.commit()
        
        return jsonify({
            'message': 'Branch created successfully',
            'branch': branch.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


# ============ REVIEW ROUTES ============

@app.route('/api/reviews', methods=['GET'])
@jwt_required()
def get_reviews():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        branch_id = request.args.get('branch_id', type=int)
        sentiment = request.args.get('sentiment')
        category = request.args.get('category')
        source = request.args.get('source')
        
        query = Review.query

        # Access control: which branches this user can see
        if user.role in ('admin', 'owner'):
            # Admins can see all reviews
            pass
        elif user.role == 'manager':
            # Managers see reviews for branches they manage
            manager_branch_ids = db.session.query(Branch.id).filter_by(manager_id=current_user_id).all()
            manager_branch_ids = [b[0] for b in manager_branch_ids]
            if manager_branch_ids:
                query = query.filter(Review.branch_id.in_(manager_branch_ids))
            else:
                query = query.filter(False)
        else:
            # Staff and other roles: prefer their assigned branch, otherwise fall back to all
            if user.branch_id:
                query = query.filter_by(branch_id=user.branch_id)
        
        if branch_id:
            query = query.filter_by(branch_id=branch_id)
        if sentiment:
            query = query.filter_by(sentiment=sentiment)
        if category:
            query = query.filter_by(category=category)
        if source:
            query = query.filter_by(source=source)
        
        reviews = query.order_by(Review.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/reviews', methods=['POST'])
def create_review():
    try:
        data = request.get_json()
        
        review = Review(
            branch_id=data['branch_id'],
            rating=data['rating'],
            title=data.get('title'),
            content=data['content'],
            source=data.get('source', 'internal'),
            category=data.get('category'),
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            customer_phone=data.get('customer_phone'),
            staff_id=data.get('staff_id')
        )
        
        # Sentiment analysis (simple rule-based)
        review.sentiment = analyze_sentiment(data['rating'], data['content'])
        
        db.session.add(review)
        db.session.commit()
        
        # Update analytics
        update_analytics(data['branch_id'])
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/reviews/<int:review_id>', methods=['GET'])
@jwt_required()
def get_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)
        return jsonify(review.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/reviews/<int:review_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_review(review_id):
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        review = Review.query.get_or_404(review_id)
        review.response_text = data['response_text']
        review.is_responded = True
        review.responded_by = current_user_id
        review.responded_at = datetime.utcnow()
        
        db.session.commit()
        
        # Update analytics
        update_analytics(review.branch_id)
        
        return jsonify({
            'message': 'Response added successfully',
            'review': review.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/reviews/<int:review_id>/escalate', methods=['POST'])
@jwt_required()
def escalate_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)
        review.is_escalated = True
        db.session.commit()
        
        return jsonify({
            'message': 'Review escalated successfully',
            'review': review.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


# ============ REPLY TEMPLATE ROUTES ============

@app.route('/api/templates', methods=['GET'])
@jwt_required()
def get_templates():
    try:
        templates = ReplyTemplate.query.filter_by(is_active=True).all()
        return jsonify([template.to_dict() for template in templates]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/templates', methods=['POST'])
@jwt_required()
def create_template():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        template = ReplyTemplate(
            name=data['name'],
            template_text=data['template_text'],
            category=data.get('category'),
            sentiment_type=data.get('sentiment_type'),
            created_by=current_user_id
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            'message': 'Template created successfully',
            'template': template.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


# ============ ANALYTICS ROUTES ============

@app.route('/api/analytics/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        # Determine which branches this user can see
        if user.role in ('admin', 'owner'):
            branch_ids = [b[0] for b in db.session.query(Branch.id).all()]
        elif user.role == 'manager':
            branch_ids = [b[0] for b in db.session.query(Branch.id).filter_by(manager_id=current_user_id).all()]
        else:
            # Staff and other roles: prefer their assigned branch, otherwise show all
            if user.branch_id:
                branch_ids = [user.branch_id]
            else:
                branch_ids = [b[0] for b in db.session.query(Branch.id).all()]

        reviews_query = Review.query
        if branch_ids:
            reviews_query = reviews_query.filter(Review.branch_id.in_(branch_ids))
        reviews = reviews_query.all()
        
        total_reviews = len(reviews)
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        responded = sum(1 for r in reviews if r.is_responded)
        response_rate = (responded / total_reviews * 100) if total_reviews > 0 else 0
        
        sentiments = {
            'positive': sum(1 for r in reviews if r.sentiment == 'positive'),
            'neutral': sum(1 for r in reviews if r.sentiment == 'neutral'),
            'negative': sum(1 for r in reviews if r.sentiment == 'negative')
        }
        
        # Branch-wise ratings
        branch_ratings = {}
        for review in reviews:
            if review.branch_id not in branch_ratings:
                branch_ratings[review.branch_id] = []
            branch_ratings[review.branch_id].append(review.rating)
        
        branch_stats = []
        for branch_id in branch_ids:
            branch = Branch.query.get(branch_id)
            ratings = branch_ratings.get(branch_id, [])
            avg = sum(ratings) / len(ratings) if ratings else 0
            branch_stats.append({
                'branch_id': branch_id,
                'branch_name': branch.name,
                'avg_rating': round(avg, 2),
                'total_reviews': len(ratings)
            })
        
        return jsonify({
            'total_reviews': total_reviews,
            'avg_rating': round(avg_rating, 2),
            'response_rate': round(response_rate, 2),
            'sentiments': sentiments,
            'branch_stats': branch_stats
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/analytics/trends', methods=['GET'])
@jwt_required()
def get_trends():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        days = request.args.get('days', 30, type=int)

        # Determine which branches this user can see
        if user.role in ('admin', 'owner'):
            branch_ids = [b[0] for b in db.session.query(Branch.id).all()]
        elif user.role == 'manager':
            branch_ids = [b[0] for b in db.session.query(Branch.id).filter_by(manager_id=current_user_id).all()]
        else:
            # Staff and other roles: prefer their assigned branch, otherwise show all
            if user.branch_id:
                branch_ids = [user.branch_id]
            else:
                branch_ids = [b[0] for b in db.session.query(Branch.id).all()]

        start_date = datetime.utcnow() - timedelta(days=days)
        reviews_query = Review.query.filter(Review.created_at >= start_date)
        if branch_ids:
            reviews_query = reviews_query.filter(Review.branch_id.in_(branch_ids))
        reviews = reviews_query.all()
        
        # Group by date
        trends = {}
        for review in reviews:
            date = review.created_at.date().isoformat()
            if date not in trends:
                trends[date] = {
                    'total': 0,
                    'avg_rating': 0,
                    'positive': 0,
                    'neutral': 0,
                    'negative': 0
                }
            trends[date]['total'] += 1
            trends[date]['positive'] += 1 if review.sentiment == 'positive' else 0
            trends[date]['neutral'] += 1 if review.sentiment == 'neutral' else 0
            trends[date]['negative'] += 1 if review.sentiment == 'negative' else 0
        
        # Calculate average ratings
        for date, data in trends.items():
            date_reviews = [r for r in reviews if r.created_at.date().isoformat() == date]
            data['avg_rating'] = sum(r.rating for r in date_reviews) / len(date_reviews) if date_reviews else 0
        
        return jsonify(trends), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# ============ HELPER FUNCTIONS ============

def analyze_sentiment(rating, content):
    """Simple sentiment analysis based on rating and keywords"""
    positive_keywords = ['excellent', 'great', 'good', 'amazing', 'wonderful', 'fantastic', 'love', 'perfect']
    negative_keywords = ['bad', 'poor', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disgusting']
    
    content_lower = content.lower()
    
    positive_count = sum(1 for keyword in positive_keywords if keyword in content_lower)
    negative_count = sum(1 for keyword in negative_keywords if keyword in content_lower)
    
    if rating >= 4:
        return 'positive'
    elif rating <= 2:
        return 'negative'
    else:
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'


def update_analytics(branch_id):
    """Update analytics for a branch"""
    try:
        today = datetime.utcnow().date()
        
        reviews = Review.query.filter_by(branch_id=branch_id).filter(
            db.func.date(Review.created_at) == today
        ).all()
        
        if reviews:
            total = len(reviews)
            avg_rating = sum(r.rating for r in reviews) / total
            responded = sum(1 for r in reviews if r.is_responded)
            response_rate = (responded / total * 100) if total > 0 else 0
            positive = sum(1 for r in reviews if r.sentiment == 'positive')
            neutral = sum(1 for r in reviews if r.sentiment == 'neutral')
            negative = sum(1 for r in reviews if r.sentiment == 'negative')
            
            analytics = Analytics.query.filter_by(
                branch_id=branch_id,
                date=today
            ).first()
            
            if analytics:
                analytics.total_reviews = total
                analytics.avg_rating = avg_rating
                analytics.response_rate = response_rate
                analytics.positive_count = positive
                analytics.neutral_count = neutral
                analytics.negative_count = negative
            else:
                analytics = Analytics(
                    branch_id=branch_id,
                    date=today,
                    total_reviews=total,
                    avg_rating=avg_rating,
                    response_rate=response_rate,
                    positive_count=positive,
                    neutral_count=neutral,
                    negative_count=negative
                )
                db.session.add(analytics)
            
            db.session.commit()
    except Exception as e:
        print(f"Error updating analytics: {e}")
        db.session.rollback()


# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
