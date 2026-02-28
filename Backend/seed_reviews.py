import random
from datetime import datetime, timedelta

from app import app, db, User, Branch, Review


def infer_sentiment_from_rating(rating: int) -> str:
    if rating >= 4:
        return "positive"
    if rating <= 2:
        return "negative"
    return "neutral"


def generate_sample_text(rating: int, category: str) -> tuple[str, str]:
    positive_phrases = [
        "Amazing experience",
        "Great service",
        "Loved the ambience",
        "Delicious food",
        "Highly recommended",
    ]
    neutral_phrases = [
        "Decent overall",
        "Average experience",
        "Nothing special",
        "Okay visit",
        "Could be better",
    ]
    negative_phrases = [
        "Very disappointing",
        "Poor service",
        "Bad experience",
        "Not satisfied",
        "Would not recommend",
    ]

    if rating >= 4:
        title = random.choice(positive_phrases)
    elif rating <= 2:
        title = random.choice(negative_phrases)
    else:
        title = random.choice(neutral_phrases)

    category_phrases = {
        "food": [
            "The dishes were flavorful and served hot.",
            "Portions were generous and presentation was nice.",
            "Food quality was inconsistent compared to previous visits.",
            "Some items on the menu were unavailable.",
        ],
        "service": [
            "Staff were attentive and friendly throughout.",
            "Service was a bit slow during peak hours.",
            "Requests were handled politely and efficiently.",
            "It was difficult to get the staff's attention.",
        ],
        "staff": [
            "The team was professional and courteous.",
            "Staff seemed overwhelmed but tried their best.",
            "Some staff members were not very welcoming.",
            "The manager personally checked on our table.",
        ],
        "cleanliness": [
            "The place was clean and well maintained.",
            "Washrooms could be cleaned more frequently.",
            "Tables were cleared quickly between customers.",
            "Saw some trash left around the corner tables.",
        ],
        "ambience": [
            "The music and lighting created a great vibe.",
            "Ambience was okay but a bit too noisy.",
            "Seating was comfortable and spacious.",
            "The place felt a little cramped during rush hours.",
        ],
    }

    sentences = category_phrases.get(category, category_phrases["service"])
    content = f"{title}. {random.choice(sentences)}"
    return title, content


def seed_database(num_branches: int = 5, reviews_per_branch: int = 200) -> None:
    """Populate the database with branches, users (admin/manager/staff), and lots of reviews."""
    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # Create branches if none exist
        if Branch.query.count() == 0:
            branch_locations = [
                "Downtown",
                "Uptown",
                "City Center",
                "Mall Road",
                "Tech Park",
                "Airport",
                "Suburban Plaza",
            ]

            for i in range(num_branches):
                branch = Branch(
                    name=f"Branch {i + 1}",
                    location=random.choice(branch_locations),
                    branch_code=f"BR{i + 1:03}",
                )
                db.session.add(branch)

            db.session.commit()

        branches = Branch.query.all()

        # Create admin + manager + staff users if there are no users yet
        if User.query.count() == 0:
            # Admin user (can see all reviews)
            admin_email = "admin@example.com"
            admin = User(
                email=admin_email,
                full_name="Admin User",
                role="admin",
            )
            admin.set_password("password123")
            db.session.add(admin)

            for branch in branches:
                # Manager for each branch (used by backend filter on manager_id)
                manager_email = f"manager{branch.id}@example.com"
                manager = User(
                    email=manager_email,
                    full_name=f"Branch {branch.id} Manager",
                    role="manager",
                    branch_id=branch.id,
                )
                manager.set_password("password123")
                db.session.add(manager)
                db.session.flush()  # ensure manager.id is available
                branch.manager_id = manager.id

                # Extra staff user for the branch
                staff_email = f"staff{branch.id}@example.com"
                staff_user = User(
                    email=staff_email,
                    full_name=f"Staff Member {branch.id}",
                    role="staff",
                    branch_id=branch.id,
                )
                staff_user.set_password("password123")
                db.session.add(staff_user)

            db.session.commit()

        users = User.query.all()

        # Only seed reviews if none exist to avoid duplicates
        if Review.query.count() > 0:
            print("Reviews already exist. Skipping review seeding.")
            return

        categories = ["food", "service", "staff", "cleanliness", "ambience"]
        sources = ["google", "zomato", "internal", "whatsapp"]

        print(
            f"Creating {reviews_per_branch} reviews for each of "
            f"{len(branches)} branches..."
        )

        for branch in branches:
            for _ in range(reviews_per_branch):
                rating = random.randint(1, 5)
                category = random.choice(categories)
                sentiment = infer_sentiment_from_rating(rating)
                title, content = generate_sample_text(rating, category)

                created_offset_days = random.randint(0, 180)
                created_at = datetime.utcnow() - timedelta(days=created_offset_days)

                customer_id = random.randint(1000, 9999)
                staff = random.choice(users)

                review = Review(
                    branch_id=branch.id,
                    rating=rating,
                    title=title,
                    content=content,
                    source=random.choice(sources),
                    category=category,
                    sentiment=sentiment,
                    customer_name=f"Customer {customer_id}",
                    customer_email=f"customer{customer_id}@example.com",
                    customer_phone=f"+91-9{random.randint(100000000, 999999999)}",
                    staff_id=staff.id,
                    is_responded=random.choice([True, False]),
                    created_at=created_at,
                    updated_at=created_at,
                )

                db.session.add(review)

        db.session.commit()
        print("Database seeding complete.")


if __name__ == "__main__":
    seed_database()

