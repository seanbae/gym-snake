# gym-snake

1) Clone the repo:
```
$ git clone git@github.com:SeanBae/gym-snake.git
```

2) `cd` into `gym-snake` and run:
```
$ pip install -e .
```

3) This should run total 100 instances of the `snake-v0` environment for 1000 timesteps, rendering the environment at each step. By default, you should see a window pop up rendering the classic Snake problem:
```python
import gym
import gym_snake

env = gym.make('snake-v0')

for i in range(100):
    env.reset()
    for t in range(1000):
        env.render()
        observation, reward, done, info = env.step(env.action_space.sample())
        if done:
            print('episode {} finished after {} timesteps'.format(i, t))
            break


```
