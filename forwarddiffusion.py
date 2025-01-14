from PIL import Image

import math
import matplotlib.pyplot as plt
import numpy as np

TOTAL_TIME_STEPS = 100
COSINE_OFFSET = 0.008 # Offset prevents noise from getting too small near t=0
alpha_bar_noise_schedule = [
    # Cosine schedule from https://arxiv.org/pdf/2102.09672
    math.cos((t/TOTAL_TIME_STEPS + COSINE_OFFSET) / (1 + COSINE_OFFSET) * math.pi/2)**2
    for t in range(TOTAL_TIME_STEPS)
]
print(alpha_bar_noise_schedule)

def noise_image(img, time_step):
    noise = np.random.normal(size=(original_img.shape))
    img = math.sqrt(alpha_bar_noise_schedule[time_step]) * original_img + \
        math.sqrt(1-alpha_bar_noise_schedule[time_step]) * noise
    # Clip within RGB bounds. According to https://arxiv.org/pdf/2102.09672, there
    # are "singularities" near t=T if you let values get too close to 1, so we
    # clip at 0.999. Don't ask me what singularities are.
    return img.clip(min=0, max=0.999)

original_img = np.asarray(Image.open('anakin_sand.jpg')) / 256
ROW_LENGTH = 10
fig, ax = plt.subplots(ncols=ROW_LENGTH, nrows=TOTAL_TIME_STEPS // ROW_LENGTH)
ax = ax.flatten()
for i in range(TOTAL_TIME_STEPS):
    img = noise_image(original_img, i)
    ax[i].imshow(img)
    ax[i].set_axis_off()
plt.show()