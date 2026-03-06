import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Taller figure to accommodate larger text inside boxes
fig, ax = plt.subplots(figsize=(18, 6))
ax.set_xlim(0, 18)
ax.set_ylim(0, 6)
ax.axis('off')
fig.patch.set_facecolor('white')

YELLOW_BOX = '#B8BF6A'
CYAN_BG    = '#A8E6E6'
BLUE_BOX   = '#8888CC'
TEXT_DARK  = '#222222'

def rbox(ax, x, y, w, h, color, lw=3, ec='#555555', zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.12",
                                facecolor=color, edgecolor=ec,
                                linewidth=lw, zorder=zorder))

def arrow(ax, x1, y1, x2, y2, label='', label_dy=0.28):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=3.0))
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 + label_dy
        ax.text(mx, my, label, fontsize=28, fontstyle='italic',
                ha='center', va='bottom', color=TEXT_DARK)

# ─── Encoder box ───
rbox(ax, 0.8, 1.0, 3.8, 4.0, YELLOW_BOX)
ax.text(2.7, 3.3, 'Encoder', fontsize=40, fontweight='bold',
        ha='center', va='center', color=TEXT_DARK, zorder=5)
ax.text(2.7, 2.1, '(NN)', fontsize=34,
        ha='center', va='center', color=TEXT_DARK, zorder=5)

# ─── Latent Space box ───
rbox(ax, 6.6, 1.0, 4.8, 4.0, CYAN_BG)
ax.text(9.0, 3.6, 'Latent Space', fontsize=36, fontweight='bold',
        ha='center', va='center', color=TEXT_DARK, zorder=5)
ax.text(9.0, 2.7, r'$z \sim \mathcal{N}(\mu, \sigma)$', fontsize=32,
        ha='center', va='center', color=TEXT_DARK, zorder=5)
ax.text(9.0, 1.75, 'Sampling', fontsize=28,
        ha='center', va='center', color='#444444', zorder=5)

# ─── Decoder box ───
rbox(ax, 13.4, 1.0, 3.8, 4.0, BLUE_BOX)
ax.text(15.3, 3.3, 'Decoder', fontsize=40, fontweight='bold',
        ha='center', va='center', color='white', zorder=5)
ax.text(15.3, 2.1, '(NN)', fontsize=34,
        ha='center', va='center', color='white', zorder=5)

# ─── Arrows ───
arrow(ax, 0.0, 3.0, 0.8, 3.0)
ax.text(-0.1, 3.0, '$x$', fontsize=36, fontstyle='italic',
        ha='right', va='center', color=TEXT_DARK)

arrow(ax, 4.6, 3.0, 6.6, 3.0, label='$\\mu,\\, \\sigma$')
arrow(ax, 11.4, 3.0, 13.4, 3.0, label='$z$')

arrow(ax, 17.2, 3.0, 17.9, 3.0)
ax.text(18.0, 3.0, "$x'$", fontsize=36, fontstyle='italic',
        ha='left', va='center', color=TEXT_DARK)

plt.tight_layout(pad=0.3)
plt.savefig('/home/ubuntu/upload/VAE_diagram.png', dpi=180,
            bbox_inches='tight', facecolor='white')
print("Saved: /home/ubuntu/upload/VAE_diagram.png")
