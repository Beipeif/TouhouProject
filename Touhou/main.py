from stable_baselines3 import PPO
import gymnasium as gym
from gymnasium.envs.registration import register

import KeyboardAction
import time


print(KeyboardAction.reset_key())
time.sleep(1)

env_name = 'TouhouEnvs'

register(
    id=f"{env_name}",
    entry_point=f"{env_name}:CustomEnv",
    reward_threshold=80000,
)

print(gym.spec(f"{env_name}"))


env = gym.make(f"{env_name}")

model = PPO(
    policy = 'MlpPolicy',
    env = env,
    n_steps = 512,
    batch_size = 32,
    n_epochs = 10824,
    gamma = 0.999,
    gae_lambda = 0.98,
    ent_coef = 0.01,
    device = 'cuda',
    verbose=1)

'''
print("_____OBSERVATION SPACE_____ \n")
print("Observation Space Shape", env.observation_space.shape)
print("Sample observation", env.observation_space.sample()) # Get a random observation
print("\n _____ACTION SPACE_____ \n"zx)
print("Action Space Shape", env.action_space.shape)
print("Action Space Sample", env.action_space.sample()) # Tazke a random action
'''

model.learn(total_timesteps=10)
# Save the model
model_name = f"{env_name}"
model.save(model_name)

'''
model = PPO.load("Touhous")


obs = vec_env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)

#Model Load
'''

'''
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

     
eval_env = Monitor(gym.make('TouhouEnvs'))
mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=10, deterministic=True)
print(f"mean_reward={mean_reward:.2f} +/- {std_reward}")
'''