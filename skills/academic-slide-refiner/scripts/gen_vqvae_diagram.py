import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Wider canvas to give more room between NN and Quantization
fig, ax = plt.subplots(figsize=(20, 6))
ax.set_xlim(0, 20)
ax.set_ylim(0, 6)
ax.axis('off')
fig.patch.set_facecolor('white')

YELLOW_BG  = '#E8EDA0'
NN_BOX     = '#B8BF6A'
QUANT_BOX  = '#7DC87D'
CYAN_BG    = '#A8E6E6'
BLUE_BOX   = '#8888CC'
TEXT_DARK  = '#222222'
RED_TEXT   = '#CC0000'

def solid_box(ax, x, y, w, h, color, lw=3, ec='#555555', zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.08",
                                facecolor=color, edgecolor=ec,
                                linewidth=lw, zorder=zorder))

def dashed_box(ax, x, y, w, h, color, lw=2.5, ec='#666666', zorder=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.08",
                                facecolor=color, edgecolor=ec,
                                linewidth=lw, linestyle='--', zorder=zorder))

def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=2.5))

# ─── Layout coordinates ───────────────────────────────────────────
# Encoder outer box: x=0.8 to x=11.0
# NN inner box:       x=1.4 to x=4.0  (width 2.6)
# gap for label:      x=4.0 to x=6.6  (2.6 wide — enough for "Feature\nEmbedding z")
# Quantization box:   x=6.6 to x=10.2 (width 3.6)
# Encoder label at bottom
# Latent Space box:   x=11.4 to x=15.4
# Decoder box:        x=15.8 to x=18.0

# ─── Outer Encoder box ───
solid_box(ax, 0.8, 0.8, 10.2, 4.4, YELLOW_BG, lw=3, ec='#888800')

# ─── NN inner box ───
dashed_box(ax, 1.4, 1.8, 2.6, 2.4, NN_BOX, ec='#666666')
ax.text(2.7, 3.1, 'NN', fontsize=40, fontweight='bold',
        ha='center', va='center', color=TEXT_DARK, zorder=6)

# ─── Arrow: NN → Quantization with "Feature Embedding z" label above ───
arrow(ax, 4.0, 3.0, 6.6, 3.0)
ax.text(5.3, 3.55, 'Feature', fontsize=24, fontstyle='italic',
        ha='center', va='bottom', color=TEXT_DARK)
ax.text(5.3, 3.0, 'Embedding z', fontsize=24, fontstyle='italic',
        ha='center', va='bottom', color=TEXT_DARK)

# ─── Quantization inner box ───
dashed_box(ax, 6.6, 1.8, 3.6, 2.4, QUANT_BOX, ec='#666666')
ax.text(8.4, 3.1, 'Quantization', fontsize=30, fontweight='bold',
        ha='center', va='center', color=TEXT_DARK, zorder=6)

# ─── Encoder label ───
ax.text(5.9, 1.0, 'Encoder', fontsize=36, fontweight='bold',
        ha='center', va='center', color=TEXT_DARK, zorder=5)

# ─── Arrow: Quantization → Latent Space ───
arrow(ax, 11.0, 3.0, 11.4, 3.0)

# ─── Latent Space / Quantized Embedding z' box ───
solid_box(ax, 11.4, 0.8, 4.0, 4.4, CYAN_BG, lw=3, ec='#5599AA')
ax.text(13.4, 3.5, 'Quantized', fontsize=30, fontweight='bold',
        ha='center', va='center', color=TEXT_DARK, zorder=5)
ax.text(13.4, 2.75, "Embedding z'", fontsize=28,
        ha='center', va='center', color=TEXT_DARK, zorder=5)
ax.text(13.4, 1.8, 'Latent Space', fontsize=28, fontstyle='italic',
        ha='center', va='center', color=RED_TEXT, fontweight='bold', zorder=5)

# ─── Arrow: Latent Space → Decoder ───
arrow(ax, 15.4, 3.0, 15.8, 3.0)

# ─── Decoder box ───
solid_box(ax, 15.8, 1.2, 2.4, 3.6, BLUE_BOX, lw=3, ec='#555599')
ax.text(17.0, 3.2, 'Decoder', fontsize=30, fontweight='bold',
        ha='center', va='center', color='white', zorder=5)
ax.text(17.0, 2.2, '(NN)', fontsize=26,
        ha='center', va='center', color='white', zorder=5)

# ─── x → NN ───
arrow(ax, 0.0, 3.0, 1.4, 3.0)
ax.text(-0.1, 3.0, '$x$', fontsize=36, fontstyle='italic',
        ha='right', va='center', color=TEXT_DARK)

# ─── Decoder → x' ───
arrow(ax, 18.2, 3.0, 19.0, 3.0)
ax.text(19.1, 3.0, "$x'$", fontsize=36, fontstyle='italic',
        ha='left', va='center', color=TEXT_DARK)

# ─── Codebook arrow (upward into Quantization) ───
ax.annotate('', xy=(8.4, 1.8), xytext=(8.4, 0.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=2.5))
ax.text(8.4, 0.22, 'Codebook', fontsize=28,
        ha='center', va='center', color=TEXT_DARK)

plt.tight_layout(pad=0.3)
plt.savefig('/home/ubuntu/upload/VQVAE_redrawn.png', dpi=180,
            bbox_inches='tight', facecolor='white')
print("Saved: /home/ubuntu/upload/VQVAE_redrawn.png")
