from PIL import Image

import math
import matplotlib.pyplot as plt
import numpy as np

TOTAL_TIME_STEPS = 10
MIN_NOISE = 0
MAX_NOISE = 1
noise_schedule = [
    # TODO: Switch to a cosine noise schedule as in https://arxiv.org/pdf/2102.09672
    (1-t/(TOTAL_TIME_STEPS-1)) * MIN_NOISE + (t/(TOTAL_TIME_STEPS-1)) * MAX_NOISE
    for t in range(TOTAL_TIME_STEPS)
]
print(noise_schedule)

last_alpha_bar = 1
alpha_bar_noise_schedule = []
for beta in noise_schedule:
    last_alpha_bar = last_alpha_bar * (1 - beta)
    alpha_bar_noise_schedule.append(last_alpha_bar)
print(alpha_bar_noise_schedule)

original_img = np.asarray(Image.open('anakin_sand.jpg')) / 256
fig, ax = plt.subplots(ncols=TOTAL_TIME_STEPS)
ax = ax.flatten()
for i in range(TOTAL_TIME_STEPS):
    noise = np.random.normal(size=(original_img.shape))
    img = math.sqrt(alpha_bar_noise_schedule[i]) * original_img + \
        math.sqrt(1-alpha_bar_noise_schedule[i]) * noise
    ax[i].imshow(img)
plt.show()