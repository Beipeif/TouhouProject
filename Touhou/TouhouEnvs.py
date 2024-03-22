import time
from typing import Optional, Union
from PIL import Image
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import utils
import ddddocr
import KeyboardAction
import win32gui
import os

red_pixel = (484, 112, 80, 19)
blue_pixel = (482, 128, 95, 20)
reward_pixel = (490, 82, 140, 16)


class CustomEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):

    metadata = {
        "render_modes": ["human", "rgb_array"],
    }

    def __init__(self, render_mode: Optional[str] = None):
        self.screen_width = 420
        self.screen_height = 460
        self.actionDimension = 7
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.fps = 3
        self.imgz = (
            self.x1 + 20, self.y1 + 50,
            self.screen_width, self.screen_height
        )

        act_low, act_high, act_shape, self.act_dtype = (
            (0, 1, (7, 1), np.float32)
        )
        self.action_space = spaces.Box(
            low=act_low, high=act_high, shape=act_shape, dtype=self.act_dtype
        )
        self.key = (0x48, 0x50, 0x4D, 0x4B, 0x2C, 0x2D, 0x2A)  # up/down/left/right/z/x/shift

        _low, _high, _obs_dtype = (
            (0, 255, np.uint8)
        )
        _shape = (self.screen_height, self.fps * self.screen_width, 3)
        self.observation_space = spaces.Box(
            low=_low, high=_high, shape=_shape, dtype=_obs_dtype
        )
        "设置ObsType"
        self.render_mode = render_mode
        self.steps_beyond_terminated = None
        self.state = None
        self.episode_step = 0

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        # Note that if you use custom reset bounds, it may lead to out-of-bound
        # state/observations.
        self.episode_step = 0
        (x1, y1, x2, y2), handle = KeyboardAction.get_window_pos(
            '东方永夜抄 ～  Imperishable Night. ver 1.00d'
        )
        "The substitution of 'self.*' to '*' will lead to the missing of handle"
        " win32gui.SendMessage(handle, win32con.WM_SYS_COMMAND, win32con.SC_RESTORE, 0) # 还原最小化窗口"
        handles = win32gui.SetForegroundWindow(handle)
        print(handles)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        "使窗口显示在最前面"
        KeyboardAction.restart_key()
        time.sleep(2)
        low, high = utils.maybe_parse_reset_bounds(
            options, -0.05, 0.05  # default low
        )  # default high
        self.state = self.np_random.uniform(low=low, high=high, size=(4,))
        self.steps_beyond_terminated = None
        KeyboardAction.pause()
        return KeyboardAction.getimage3(self.imgz), {}

    def step(self, action):
        assert self.action_space.contains(action), f"{action!r} ({type(action)}) invalid"
        "给定action输入，采用step将action导入envs"
        "action ActType -> tuple[ObsType, Float, bool, bool, dict[str, Any]]"
        KeyboardAction.pause()

        self.imgz = (
            self.x1 + 20, self.y1 + 50,
            self.screen_width, self.screen_height
        )
        "take actions and collect imgs"
        action = [1 if j > 0.5 else 0 for j in action]
        get_imgz = KeyboardAction.activate(action, self.key, self.imgz)

        for i in range(7):
            KeyboardAction.ReleaseKey(self.key[i])

        KeyboardAction.pause()

        self.episode_step += 1

        blue_star_number = self.blue_star()
        red_star_number = self.red_star()
        rew_number = self.reward_number()

        "奖励函数设置"
        rew_number = 1e7 * red_star_number + 2e6 * blue_star_number + rew_number - 8e6
        print(
            f'step={self.episode_step}, rew={rew_number}, redstar={red_star_number}, bluestar={blue_star_number}, action={action}'
        )
        terminated = False
        truncated = False

        if red_star_number == 0 and self.episode_step >= 5:
            print('terminated')
            KeyboardAction.pause()
            #KeyboardAction.reset_key()
            terminated = True
            "死亡判定"

        return get_imgz, rew_number, terminated, truncated, {}

    def close(self):
        pass

    def red_star(self):
        red_star_img = KeyboardAction.getimage(
            self.x1 + red_pixel[0], self.y1 + red_pixel[1], red_pixel[2], red_pixel[3]
        )
        red_star_img = Image.fromarray(red_star_img.astype('uint8')).convert('RGB')
        red_star_img.save('./red_test_temp.jpg')
        with open("red_test_temp.jpg", 'rb') as f:
            rb_img = f.read()
        red_star_number = ddddocr.DdddOcr(old=False, det=False, show_ad=False).classification(rb_img)
        red_star_number = red_star_number.replace(' ', '')
        f.close()
        #print(red_star_number)
        #print(len(red_star_number))
        #os.remove('./red_test_temp.jpg')
        return len(red_star_number)

    def blue_star(self):
        blue_star_img = KeyboardAction.getimage(
            self.x1 + blue_pixel[0], self.y1 + blue_pixel[1], blue_pixel[2], blue_pixel[3]
        )
        blue_star_img = Image.fromarray(blue_star_img.astype('uint8')).convert('RGB')
        blue_star_img.save('./blue_test_temp.jpg')
        with open("blue_test_temp.jpg", 'rb') as f:
            rb_img = f.read()
        blue_star_number = ddddocr.DdddOcr(old=False, det=False, show_ad=False).classification(rb_img)
        blue_star_number = blue_star_number.replace(' ', '')
        f.close()
        #print(blue_star_number)
        #print(len(blue_star_number))
        #os.remove('./blue_test_temp.jpg')
        return len(blue_star_number)

    def reward_number(self):
        reward_img = KeyboardAction.getimage(
            self.x1 + reward_pixel[0], self.y1 + reward_pixel[1], reward_pixel[2], reward_pixel[3]
        )
        reward_img = Image.fromarray(reward_img.astype('uint8')).convert('RGB')
        reward_img.save('./temp.jpg')
        with open("temp.jpg", 'rb') as f:
            rb_img = f.read()
        rew_number = ddddocr.DdddOcr(old=False, det=False, show_ad=False).classification(rb_img)
        rew_number = rew_number.replace('o', '0')
        rew_number = rew_number.replace('s', '8')
        rew_number = rew_number.replace('L', '')
        rew_number = rew_number.replace('y', '')
        rew_number = rew_number.replace('Z', '4')
        rew_number = rew_number.replace('t', '1')
        rew_number = rew_number.replace('场', '311')
        f.close()
        #print(rew_number)
        #print(int(rew_number))
        #os.remove('./temp.jpg')
        return int(rew_number)

