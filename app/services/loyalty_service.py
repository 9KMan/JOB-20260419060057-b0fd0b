from datetime import datetime
from app.models import Visit, Reward

VISITS_PER_REWARD = 10

class LoyaltyService:
    def __init__(self, visits_per_reward: int = VISITS_PER_REWARD):
        self.visits_per_reward = visits_per_reward

    def record_visit(self, db, customer):
        visit = Visit(customer_id=customer.id)
        db.add(visit)

        customer.total_visits += 1
        db.commit()
        db.refresh(visit)

        reward_granted = False
        if customer.total_visits % self.visits_per_reward == 0:
            reward = Reward(customer_id=customer.id, visit_id=visit.id)
            db.add(reward)
            db.commit()
            db.refresh(reward)
            reward_granted = True

        return visit, reward_granted

    def get_loyalty_status(self, customer):
        current_visits = customer.total_visits
        visits_since_last_reward = current_visits % self.visits_per_reward
        visits_until_reward = self.visits_per_reward - visits_since_last_reward

        return {
            "current_visits": current_visits,
            "visits_until_reward": visits_until_reward,
            "total_rewards_earned": current_visits // self.visits_per_reward,
            "next_reward_at": visits_until_reward == 0
        }