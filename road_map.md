You're tackling a sophisticated and rewarding problem: **style matching via parameter estimation** for **film emulation**, using **scanned negatives and digital reference pairs**. The goal is to learn a model (or parameter mapping) that **translates digital images into film-like renderings**, grounded in actual paired observations.

---

## 🛣️ **Roadmap for Film Emulation via Style Parameter Estimation**

We'll break this into 5 key phases:

---

### **1. Data Collection & Preprocessing**

#### 📸 1.1. Image Pair Acquisition

* Capture **the same scene** using:

  * Digital camera (raw or processed to linear TIFF)
  * Film camera (scan negatives at high quality, 16-bit preferred)
* Use tripod or register frames carefully to minimize alignment issues.

#### 🧹 1.2. Preprocessing

* Align image pairs using:

  * Feature-based methods (e.g. SIFT, ORB)
  * Homography warping (OpenCV)
* Normalize:

  * Film scans to linear tone scale (remove scanner curve if possible)
  * Digital images to linear RGB or XYZ
* Optional: **mask out sky, specular highlights, and deep shadows** (regions with unpredictable scanner response)

#### 💡 1.3. Color Space Conversion

* Convert both images to perceptually meaningful space (e.g., **Lab**, **LCH**, or **OKLab**)

---

### **2. Feature Matching & Region Mapping**

#### 🧭 2.1. Feature Mapping

* Use matched keypoints to identify **corresponding regions** (not pixel-perfect)
* Optionally use clustering to group color areas (e.g., foliage, skin, concrete)

#### 🧪 2.2. Extract Color Statistics

* For each region:

  * Extract RGB or Lab means, stds, histograms
  * Calculate chroma, hue angle in LCH/OKLab
* Optional: extract tonal curve via fitting (logit or spline)

---

### **3. Parameter Estimation Model Design**

#### 🎛️ 3.1. Define Style Parameters

Candidate parameter set (to be learned):

| Type               | Parameters                          |
| ------------------ | ----------------------------------- |
| Tone Curve         | Contrast, black/white point, spline |
| Color Grading      | Hue shift, saturation curve         |
| WB/Color Cast      | RGB gains, temperature/tint         |
| Grain/Texture      | (optional) synthetic grain strength |
| Curves per channel | R/G/B or Lab A/B curves             |

#### 🤖 3.2. Choose Model Type

Options include:

* **Parametric fit**: Linear or polynomial mapping from digital → film
* **ML Regression**: Learn mapping (e.g., RandomForest, MLP)
* **Neural model** (for later): CNN/VAE that estimates style vectors

Train on region-level or global color statistics:

```text
Input:  [Digital RGB or Lab features]
Output: [Estimated tone curve points, hue shifts, saturation scales, etc.]
```

---

### **4. Training & Validation**

#### 🧠 4.1. Loss Functions

* **Color loss**: L1/L2 between predicted vs. film Lab values
* **Tone curve loss**: Compare predicted vs. actual tonal shape
* **Perceptual loss**: (Optional) using VGG features for image similarity
* **Regularization**: Smoothness of estimated curves

#### 🧪 4.2. Evaluation Metrics

* ΔE (CIE76 or CIE2000)
* Histogram distance (e.g., Earth Mover’s Distance)
* Human visual preference (if available)

---

### **5. Rendering Pipeline & Style Reproduction**

#### 🛠️ 5.1. Build the Parameterized Rendering Engine

Use estimated parameters to emulate the film style:

* Apply tone curve to linear RGB
* Adjust hue/saturation based on learned shift maps
* Introduce color cast or simulate white balance
* (Optional) Add grain, halation, bloom based on film stock characteristics

#### 🧪 5.2. Validate with Holdout Scenes

* Apply learned parameters to unseen digital images.
* Compare against actual film-scanned images (if available).
* Use both perceptual + statistical comparison.

#### 🎨 5.3. Save Style Preset

Export estimated parameters in usable form:

* JSON with tone curve, color shifts, etc.
* LUT or Hald CLUT format
* Plugin-friendly format (Lightroom, Capture One, RawTherapee)

---

## ✅ Deliverables

| Item                         | Description                                       |
| ---------------------------- | ------------------------------------------------- |
| Matched image pair dataset   | Registered TIFF pairs of film/digital             |
| Feature map + region samples | Masks or clusters for stable color comparison     |
| Parameter model              | Estimation function or ML model                   |
| Rendering pipeline           | Function to apply parameters to digital input     |
| Emulation result             | Emulated film-style output from raw digital input |

---

## 📌 Optional Enhancements

* Support **different film stocks** as separate styles
* Build **interactive UI** to visualize tone & color curve differences
* Allow **manual override or fine-tuning** of parameters
* Create **exportable LUTs** or camera profiles (ICC/DCP)

---

Would you like a Python starter template for region matching and color stat extraction?
