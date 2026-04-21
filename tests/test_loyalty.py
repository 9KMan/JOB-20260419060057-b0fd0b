import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Customer, Visit, Reward
from app.services.loyalty_service import LoyaltyService

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def loyalty_service():
    return LoyaltyService(visits_per_reward=10)

@pytest.fixture
def customer(db):
    c = Customer(phone="+966501234567", name="Test Customer")
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

def test_first_visit_no_reward(db, customer, loyalty_service):
    visit, reward = loyalty_service.record_visit(db, customer)
    assert reward is False
    assert customer.total_visits == 1
    assert visit.is_reward is False

def test_tenth_visit_grants_reward(db, customer, loyalty_service):
    for i in range(9):
        loyalty_service.record_visit(db, customer)
    assert customer.total_visits == 9

    visit, reward = loyalty_service.record_visit(db, customer)
    assert reward is True
    assert customer.total_visits == 10

    rewards = db.query(Reward).filter_by(customer_id=customer.id).all()
    assert len(rewards) == 1
    assert rewards[0].redeemed is False

def test_eleventh_visit_no_reward(db, customer, loyalty_service):
    for i in range(10):
        loyalty_service.record_visit(db, customer)

    visit, reward = loyalty_service.record_visit(db, customer)
    assert reward is False
    assert customer.total_visits == 11

def test_loyalty_status(db, customer, loyalty_service):
    loyalty_service.record_visit(db, customer)
    status = loyalty_service.get_loyalty_status(customer)

    assert status["current_visits"] == 1
    assert status["visits_until_reward"] == 9
    assert status["total_rewards_earned"] == 0

def test_loyalty_status_near_reward(db, customer, loyalty_service):
    for i in range(9):
        loyalty_service.record_visit(db, customer)

    status = loyalty_service.get_loyalty_status(customer)
    assert status["visits_until_reward"] == 1
    assert status["total_rewards_earned"] == 0

def test_multiple_rewards(db, customer, loyalty_service):
    for i in range(20):
        loyalty_service.record_visit(db, customer)

    rewards = db.query(Reward).filter_by(customer_id=customer.id).all()
    assert len(rewards) == 2
    assert customer.total_rewards == 0

def test_visit_notes(db, customer, loyalty_service):
    visit, reward = loyalty_service.record_visit(db, customer)
    visit.notes = "Full wash + vacuum"
    db.commit()

    saved_visit = db.query(Visit).filter_by(id=visit.id).first()
    assert saved_visit.notes == "Full wash + vacuum"