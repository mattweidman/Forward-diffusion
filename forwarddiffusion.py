from PIL import Image

import math
import matplotlib.pyplot as plt
import numpy as np

TOTAL_TIME_STEPS = 10
cosine_offset = 1e-4 # Offset prevents noise from getting too small near t=0
alpha_bar_noise_schedule = [
    # Cosine schedule from https://arxiv.org/pdf/2102.09672
    math.cos((t/TOTAL_TIME_STEPS + cosine_offset) / (1 + cosine_offset) * math.pi/2)**2
    for t in range(TOTAL_TIME_STEPS)
]
print(alpha_bar_noise_schedule)

original_img = np.asarray(Image.open('anakin_sand.jpg')) / 256
fig, ax = plt.subplots(ncols=TOTAL_TIME_STEPS)
ax = ax.flatten()
for i in range(TOTAL_TIME_STEPS):
    noise = np.random.normal(size=(original_img.shape))
    img = math.sqrt(alpha_bar_noise_schedule[i]) * original_img + \
        math.sqrt(1-alpha_bar_noise_schedule[i]) * noise
    # Clip within RGB bounds. According to https://arxiv.org/pdf/2102.09672, there
    # are "singularities" near t=T if you let values get too close to 1, so we
    # clip at 0.999. Don't ask me what singularities are.
    img = img.clip(min=0, max=0.999)
    ax[i].imshow(img)
plt.show()