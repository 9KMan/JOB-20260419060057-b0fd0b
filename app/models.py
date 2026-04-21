from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    total_visits = Column(Integer, default=0)
    total_rewards = Column(Integer, default=0)

    visits = relationship("Visit", back_populates="customer", order_by="desc(Visit.created_at)")

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "name": self.name,
            "total_visits": self.total_visits,
            "total_rewards": self.total_rewards,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_reward = Column(Boolean, default=False)
    notes = Column(String(500), nullable=True)

    customer = relationship("Customer", back_populates="visits")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_reward": self.is_reward,
            "notes": self.notes,
        }

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    redeemed = Column(Boolean, default=False)
    redeemed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "visit_id": self.visit_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "redeemed": self.redeemed,
            "redeemed_at": self.redeemed_at.isoformat() if self.redeemed_at else None,
        }