import rawpy
import imageio
import numpy as np
import cv2
import os

INPUT_DIR = "input"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def apply_kodak_gold_200_emulation(rgb_img):
    # 1. Simulate Kodak Gold tone curve (lift shadows, roll off highlights)
    def tone_curve(channel, gamma=0.9):
        lut = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)]).astype("uint8")
        return cv2.LUT(channel, lut)

    b, g, r = cv2.split(rgb_img)
    r = tone_curve(r, 0.95)
    g = tone_curve(g, 0.9)
    b = tone_curve(b, 0.85)

    # 2. Shift color: add slight warmth (bias red, reduce blue)
    r = cv2.add(r, 5)
    b = cv2.subtract(b, 5)

    # 3. Combine channels back
    styled = cv2.merge((b, g, r))
    return styled

def convert_nef_to_tiff_jpg(nef_path):
    base = os.path.splitext(os.path.basename(nef_path))[0]
    tiff_path = os.path.join(OUTPUT_DIR, f"{base}_kodakgold200.tiff")
    jpg_path = os.path.join(OUTPUT_DIR, f"{base}_kodakgold200.jpg")

    print(f"Processing {nef_path}...")

    with rawpy.imread(nef_path) as raw:
        rgb = raw.postprocess(output_bps=8)  # 8-bit for OpenCV compatibility

    styled = apply_kodak_gold_200_emulation(rgb)

    imageio.imwrite(tiff_path, styled)
    imageio.imwrite(jpg_path, styled)
    print(f"Saved TIFF → {tiff_path}")
    print(f"Saved JPG  → {jpg_path}")

def main():
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".nef"):
            convert_nef_to_tiff_jpg(os.path.join(INPUT_DIR, file))

if __name__ == "__main__":
    main()
