# -*- coding: utf-8 -*-
"""
Slider-crank mechanism animation
曲柄滑块机构运动动画
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle


# 1. Mechanism parameters, mm
r = 40.0
l = 120.0

if l <= r:
    raise ValueError(
        "Connecting rod length must be greater than crank radius."
    )


# 2. Crank angles
theta = np.linspace(0, 2 * np.pi, 181)


# 3. Create figure
fig, ax = plt.subplots(figsize=(10, 5))

ax.set_xlim(-60, 190)
ax.set_ylim(-70, 70)
ax.set_aspect("equal")
ax.set_xlabel("Horizontal Position (mm)")
ax.set_ylabel("Vertical Position (mm)")
ax.set_title("Slider-Crank Mechanism Animation")
ax.grid(True, linestyle="--", alpha=0.5)

# Crank rotation path
crank_circle = plt.Circle(
    (0, 0),
    r,
    fill=False,
    linestyle="--",
    color="gray"
)
ax.add_patch(crank_circle)

# Fixed pivot
ax.plot(0, 0, "ko", markersize=8)

# Moving components
crank_line, = ax.plot(
    [],
    [],
    color="blue",
    linewidth=4,
    label="Crank"
)

rod_line, = ax.plot(
    [],
    [],
    color="orange",
    linewidth=4,
    label="Connecting Rod"
)

crank_pin, = ax.plot([], [], "ko", markersize=7)

slider = Rectangle(
    (0, -10),
    24,
    20,
    facecolor="red",
    edgecolor="black"
)
ax.add_patch(slider)

angle_text = ax.text(
    0.03,
    0.92,
    "",
    transform=ax.transAxes,
    fontsize=11
)

ax.legend(loc="upper right")


# 4. Animation update function
def update(frame):
    angle = theta[frame]

    crank_x = r * np.cos(angle)
    crank_y = r * np.sin(angle)

    slider_x = (
        crank_x
        + np.sqrt(l**2 - crank_y**2)
    )

    crank_line.set_data(
        [0, crank_x],
        [0, crank_y]
    )

    rod_line.set_data(
        [crank_x, slider_x],
        [crank_y, 0]
    )

    crank_pin.set_data(
        [crank_x],
        [crank_y]
    )

    slider.set_x(slider_x - 12)

    angle_text.set_text(
        "Crank angle: %.0f degree"
        % np.rad2deg(angle)
    )

    return (
        crank_line,
        rod_line,
        crank_pin,
        slider,
        angle_text
    )


# 5. Generate and save GIF
animation = FuncAnimation(
    fig,
    update,
    frames=len(theta),
    interval=40,
    blit=True
)

print("Generating animation, please wait...")

writer = PillowWriter(fps=25)
animation.save(
    "slider_crank_animation.gif",
    writer=writer,
    dpi=120
)

print("Animation saved: slider_crank_animation.gif")

plt.show()


