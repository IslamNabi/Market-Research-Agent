from config import client

class Planner:
    def create_plan(self, goal):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # You can change model here
            messages=[
                {"role": "system", "content": "You are a market research planner that creates step-by-step research plans."},
                {"role": "user", "content": f"Create a detailed 5 steps plan for this market research goal: {goal}"}
            ],
            temperature=0.7
        )
        return resp.choices[0].message.content
