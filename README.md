# TouhouProject
Artificial Idiot wrote for Cirno for STG Touhou Games

python == 3.10.13

Modules Needed
1. pyautogui
2. gymnasium
3. ddddocr
4. stable_baselines3
5. pywin32
6. pytorch

This is an AI (artificial idiot) Enviroments for Touhou Project(Imperishable Night in MyCard platform https://ygobbs.com/).
In this code, PPO algorithm with online_training are aplied.
Notably, in this verision, the number of red stars, blue stars and the scores are all detected by ddddorc to quantify their influence.
And then these three parameters are concluded to calculated the rewards.

However, at the time cirno チルノ running this code, she came up the problem of the lack of computing resource.
Thus, the next version in developing will invert the online_training policy to a offline one.
Any suggestions or adopt of this AI will be seriously considerated and authorized.
Looking forward to your advises on improving this Artificial Idiot.


Thanks for your reading.

Reference: https://zhuanlan.zhihu.com/p/344924619.
