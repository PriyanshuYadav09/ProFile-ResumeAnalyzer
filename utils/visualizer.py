import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw

def create_radar_chart(qualities_dict):
    if not qualities_dict:
        st.warning("No qualities found to generate radar chart.")
        return

    categories = list(qualities_dict.keys())
    values = list(qualities_dict.values())

    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    values += values[:1]  # close the radar loop
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(2, 2), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'b-', linewidth=2)
    ax.fill(angles, values, 'skyblue', alpha=0.4)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticks([])
    ax.set_title("Personality Traits Radar", size=10, pad=10)
    st.pyplot(fig)

def draw_tone_slider(polarity):
    img = Image.new("RGB", (300, 20), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    cursor_x = int(np.interp(polarity, [-1, 1], [0, img.width]))
    for x in range(img.width):
        r = int(np.interp(x, [0, img.width], [255, 0]))
        g = int(np.interp(x, [0, img.width], [0, 255]))
        b = 0
        draw.line([(x, 0), (x, 20)], fill=(r, g, b))
    draw.line([(cursor_x, 0), (cursor_x, 20)], fill="black", width=3)
    return img

