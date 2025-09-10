# breakia
Breakia is a simple AI experiment designed to play a Breakout-style game built in Python with Pygame.
This project was my very first attempt at both Python and reinforcement learning, so you’ll find that all variables and comments are still written in French.

What libs: 
- Pygame
- Random
- Numpy

How it works:
- The AI is trained with a Q-Learning algorithm.
- The environment is a Breakout clone built in Pygame, simplified and broken down into several parts to reduce the number of possible cases.
- At each step, the AI chooses an action (move left, move right, or stay still).
- It receives a reward based on the outcome (e.g., hitting the ball vs. losing a life).
- Over time, it updates its Q-table to maximize rewards and improve performance.

Features:
- Basic Q-Learning implementation
- Simple Pygame environment (Breakout clone)
- Educational project to understand how reinforcement learning works in games

Notes:
- This is my first real Python project, so the code may not be perfect.
- All variables and comments are currently in French.
- The AI works surprisingly well given its simplicity.

Future Improvements:
- Clean up and translate the code to English
- Add visualizations of the training process
- Experiment with other RL algorithms (e.g., Deep Q-Networks)

Here, I tried to create a graph showing the evolution of my AI over nearly 5000 games. It’s not very clear, but you can see that the AI progresses quite quickly, even though the games are extremely random :
<img width="1200" height="600" alt="graph_ai_1" src="https://github.com/user-attachments/assets/10c0c417-549a-4f95-811d-5af443845eeb" />
