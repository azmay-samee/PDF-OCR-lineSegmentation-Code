# import numpy as np
# import os
# import csv
# from image_processor import ImageProcessor
# import cv2
# import pandas as pd
# from tensorflow.python.keras.models import load_model
# class ConnectedComponentLabeler:
#  def __init__(self, imgProcessor, img_name, binary_image):
#         self.binary = (binary_image == 255).astype(np.uint16)
#         self.labels = np.uint16(256)
#         self.imgProcessorClass = imgProcessor
#         self.name = os.path.splitext(img_name)[0]
#         self.cc_matrix = []
#         self.nameImg = self.name

#  def _dfs(self, i, j):
#         stack = [(i, j)]
#         points = []
#         directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
#         while stack:
#             x, y = stack.pop()
#             if self.binary[x, y] != 0:
#                 continue
#             self.binary[x, y] = self.labels
#             points.append((x, y))
#             for dx, dy in directions:
#                 nx, ny = x+dx, y+dy
#                 if 0 <= nx < self.binary.shape[0] and 0 <= ny < self.binary.shape[1]:
#                     if self.binary[nx, ny] == 0:
#                         stack.append((nx, ny))
#         return points

#  def extract_components(self, output_dir):
#         for i in range(self.binary.shape[0]):
#             for j in range(self.binary.shape[1]):
#                 if self.binary[i, j] == 0:
#                     points = self._dfs(i, j)
#                     self._save_component(points, output_dir, self.labels)
#                     self.labels += 1
#                     self.nameImg = self.name

#  def _save_component(self, points, output_dir, label_id):
#         if not points:
#             return

#         top = min(p[0] for p in points)
#         bottom = max(p[0] for p in points)
#         left = min(p[1] for p in points)
#         right = max(p[1] for p in points)
#         width = right - left + 1
#         height = bottom - top + 1

#         cc_matrix = np.full((height, width), 255, dtype=np.uint16)
#         for x, y in points:
#             cc_matrix[x - top, y - left] = 0

#         nameImg = f'{self.name}_CC{label_id}_Top{top}_Bottom{bottom}_Left{left}_Right{right}.jpg'
#         handler = self.imgProcessorClass()
#         handler.writeImg(output_dir, nameImg, cc_matrix)
 
#  def separation(self,output_dir):
#     model_path = r"D:\FYP\Data\line_segmentation\lemon\cc_classifier.h5"

# # Load model once (not inside the loop)
#     model = load_model(model_path)

#     for file in os.listdir(output_dir):
#         if file.endswith(".jpg"):
#             img_path = os.path.join(output_dir, file)

#         # 1) Load image and preprocess
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#             if img is None:
#                 raise ValueError("Image not found:", img_path)

#             img_resized = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)
#             img_norm    = img_resized.astype("float32") / 255.0
#             img_input   = img_norm[np.newaxis, ..., np.newaxis]  # shape = (1, 32, 32, 1)

#         # 2) Predict
#             pred = model.predict(img_input)[0][0]
#             label = 1 if pred >= 0.5 else 0

#         # 3) Decide class and output directory
#             if label == 1:
#                 print(f"Prediction: MAIN-BODY (score = {pred:.3f})")
#                 save_path = os.path.join(output_dir, "main_body")
#             else:
#                 print(f"Prediction: DIACRITIC (score = {pred:.3f})")
#                 save_path = os.path.join(output_dir, "diacritics")

#         # 4) Create folder (if not exists) and save the file
#             os.makedirs(save_path, exist_ok=True)
#             cv2.imwrite(os.path.join(save_path, file), img)


import os
import cv2
import numpy as np
import pandas as pd
from skimage.filters import threshold_sauvola
from skimage import img_as_ubyte
import shutil
from datetime import datetime

class ConnectedComponentLabeler:
    def __init__(self, imgProcessor, img_name, binary_image):
        self.binary = (binary_image == 255).astype(np.uint16)
        self.labels = np.uint16(256)
        self.imgProcessorClass = imgProcessor
        self.name = os.path.splitext(img_name)[0]
        self.cc_matrix = []
        self.nameImg = self.name

    def _dfs(self, i, j):
        stack = [(i, j)]
        points = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        while stack:
            x, y = stack.pop()
            if self.binary[x, y] != 0:
                continue
            self.binary[x, y] = self.labels
            points.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.binary.shape[0] and 0 <= ny < self.binary.shape[1]:
                    if self.binary[nx, ny] == 0:
                        stack.append((nx, ny))
        return points

    def extract_components(self, output_dir):
        for i in range(self.binary.shape[0]):
            for j in range(self.binary.shape[1]):
                if self.binary[i, j] == 0:
                    points = self._dfs(i, j)
                    self._save_component(points, output_dir, self.labels)
                    self.labels += 1
                    self.nameImg = self.name

    def _save_component(self, points, output_dir, label_id):
        if not points:
            return

        top = min(p[0] for p in points)
        bottom = max(p[0] for p in points)
        left = min(p[1] for p in points)
        right = max(p[1] for p in points)
        width = right - left + 1
        height = bottom - top + 1

        self.cc_matrix = np.full((height, width), 255, dtype=np.uint16)
        for x, y in points:
            self.cc_matrix[x - top, y - left] = 0

        nameImg = f'{self.name}_CC{label_id}_Top{top}_Bottom{bottom}_Left{left}_Right{right}.jpg'
        handler = self.imgProcessorClass()
        handler.writeImg(output_dir, nameImg, self.cc_matrix)

    # =============================================================
    # ========== RULE-BASED SEPARATION FUNCTION ===================
    # =============================================================
    def separation(self, output_dir):
        main_body_dir = os.path.join(output_dir, "main_body")
        diacritics_dir = os.path.join(output_dir, "diacritics")
        excel_output = os.path.join(output_dir, "cc_features_classification.xlsx")
        log_file = os.path.join(output_dir, "classification_log.txt")

        os.makedirs(main_body_dir, exist_ok=True)
        os.makedirs(diacritics_dir, exist_ok=True)

        # Initialize log file
        with open(log_file, "w", encoding="utf-8") as log:
            log.write(f"=== Classification Debug Log ===\n")
            log.write(f"Timestamp: {datetime.now()}\n")
            log.write("=" * 60 + "\n\n")

        def log_message(msg):
            print(msg)
            with open(log_file, "a", encoding="utf-8") as log:
                log.write(msg + "\n")

        # --- Helper: Binarization ---
        def preprocess_and_binarize(img):
            thresh = threshold_sauvola(img, window_size=25, k=0.2)
            binary = img > thresh
            binary = img_as_ubyte(binary)
            binary = cv2.bitwise_not(binary)
            return binary

        # --- Helper: Extract features ---
        def extract_cc_features(file_path):
            feats = []
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                log_message(f"⚠️ Error reading image: {file_path}")
                return feats

            img_bin = preprocess_and_binarize(img)
            name = os.path.splitext(os.path.basename(file_path))[0]
            parts = name.split('_')
            try:
                top = int(parts[4].replace('Top', ''))
                bottom = int(parts[5].replace('Bottom', ''))
                left = int(parts[6].replace('Left', ''))
                right = int(parts[7].replace('Right', ''))
            except Exception:
                log_message(f"⚠️ Filename format issue: {name}")
                return feats

            height = bottom - top + 1
            width = right - left + 1
            area = height * width
            black_pix = np.sum(img_bin == 255)
            black_ratio = black_pix / area if area != 0 else 0
            aspect_ratio = height / width if width != 0 else 0
            compactness = black_pix / ((height + width) ** 2) if (height + width) != 0 else 0

            feats.append({
                "height": height,
                "width": width,
                "area": area,
                "black_pixels": black_pix,
                "black_density": black_ratio,
                "aspect_ratio": aspect_ratio,
                "compactness": compactness
            })
            return feats

        # --- Helper: Stats ---
        def compute_global_stats(all_feats):
            heights = np.array([f["height"] for f in all_feats])
            areas = np.array([f["area"] for f in all_feats])
            densities = np.array([f["black_density"] for f in all_feats])
            aspects = np.array([f["aspect_ratio"] for f in all_feats])
            compact = np.array([f["compactness"] for f in all_feats])
            stats = {
                "median_height": np.median(heights),
                "median_area": np.median(areas),
                "median_density": np.median(densities),
                "median_aspect": np.median(aspects),
                "median_compact": np.median(compact),
                "aspect_p5": np.percentile(aspects, 5),
                "aspect_p95": np.percentile(aspects, 95)
            }
            log_message(f"✅ Global Stats Computed:\n"
                        f"  Median Height: {stats['median_height']:.2f}\n"
                        f"  Median Area: {stats['median_area']:.2f}\n"
                        f"  Median Density: {stats['median_density']:.4f}\n"
                        f"  Median Aspect: {stats['median_aspect']:.4f}\n")
            return stats

        # --- Helper: Black pixel percentage ---
        def black_pixel_percentage(black_pixels, area):
            return (black_pixels / area) * 100 if area else 0.0

        # --- Helper: Rule-based classification ---
        def is_diacritic_by_rules(f, stats, fname):
            h, area = f["height"], f["area"]
            dens, aspect = f["black_density"], f["aspect_ratio"]
            black_pix_perc = black_pixel_percentage(f["black_pixels"], area)
            msg_header = f"\n[{fname}] Height={h}, Area={area}, Black%={black_pix_perc:.2f}, Aspect={aspect:.3f}, Density={dens:.4f}"

            height_thresh = stats["median_height"] * 0.75  # percentage-based threshold

            # threshold=2
            # if area <= stats["median_area"] and black_pix_perc >= 50 and  h < stats["median_height"]+ threshold:
            #     log_message(msg_header + f" → ✅ Condition 1 met (small area & high black pixel density)")
            #     return True
            # if area <= stats["median_area"] and black_pix_perc < 50 and h < stats["median_height"]:
            #     log_message(msg_header + f" → ✅ Condition 2 met (small area, low black %, low height)")
            #     return True
            # if area > stats["median_area"] and black_pix_perc >= 50 and h < stats["median_height"] :
            #     log_message(msg_header + f" → ✅ Condition new met (large area, low black %, low height)")
            #     return True
            # if area > stats["median_area"] and black_pix_perc < 50 and h < (stats["median_height"] *0.75)  and ( stats["aspect_p5"] < aspect < stats["aspect_p95"]) and( f["compactness"] < stats["median_compact"]):
            
            #     log_message(
            #     msg_header
            #     + f" → ✅ Condition 3 met (large area, low black %, low height) and aspect ratio within diacritic range {stats['aspect_p5']} and {stats['aspect_p95']}"
            # )  
            #     return True
            # if area > stats["median_area"] and black_pix_perc < 50:
            #     log_message(msg_header + f" → ❌ Condition 4 met (large area, low black %, likely main body)")
            #     return False
            if h<= stats["median_height"]:
                if area <= stats["median_area"] and black_pix_perc >= 50 :
                    log_message(msg_header + f" → ✅ Condition 1 met (small area & high black pixel density)")
                    return True
                if area <= stats["median_area"] and black_pix_perc < 50 :
                    log_message(msg_header + f" → ✅ Condition 2 met (small area, low black %, low height)")
                    return True
                if area > stats["median_area"] and black_pix_perc >= 50  :
                    log_message(msg_header + f" → ✅ Condition new met (large area, low black %, low height)")
                    return True
                if area > stats["median_area"] and black_pix_perc < 50 and h < (stats["median_height"] *0.75)  and ( stats["aspect_p5"] < aspect < stats["aspect_p95"]) and( f["compactness"] < stats["median_compact"]):
                
                    log_message(
                msg_header
                + f" → ✅ Condition 3 met (large area, low black %, low height) and aspect ratio within diacritic range {stats['aspect_p5']} and {stats['aspect_p95']}"
    )       
                    return True
                if area > stats["median_area"] and black_pix_perc < 50:
                    log_message(msg_header + f" → ❌ Condition 4 met (large area, low black %, likely main body)")
                    return False
                return True

           

            log_message(msg_header + f" → ⚪ No condition met, default False")
            return False
            

        # =============================================================
        # MAIN SEPARATION EXECUTION
        # =============================================================
        all_feats, map_file_feats = [], {}
        for fname in os.listdir(output_dir):
            if not fname.lower().endswith(".jpg"):
                continue
            fpath = os.path.join(output_dir, fname)
            feats = extract_cc_features(fpath)
            if not feats:
                continue
            for f in feats:
                f["filename"] = fname
            map_file_feats[fname] = feats
            all_feats.extend(feats)

        log_message(f"\nExtracted total {len(all_feats)} components.")
        if not all_feats:
            raise SystemExit("❌ No components found. Check input folder.")

        stats = compute_global_stats(all_feats)

        rows = []
        n_mb = n_dia = 0
        for fname, feats in map_file_feats.items():
            votes = sum(is_diacritic_by_rules(f, stats, fname) for f in feats)
            total = len(feats)
            classification = "D" if votes / total > 0.5 else "MB"
            target = diacritics_dir if classification == "D" else main_body_dir
            if classification == "D":
                n_dia += 1
            else:
                n_mb += 1

            shutil.copy(os.path.join(output_dir, fname), os.path.join(target, fname))
            log_message(f"[{fname}] → Classified as: {classification}")

            for f in feats:
                rows.append({**f, "filename": fname, "classification": classification})

        df = pd.DataFrame(rows)
        df.to_excel(excel_output, index=False)

        log_message("\n" + "=" * 60)
        log_message(f"✅ Excel saved: {excel_output}")
        log_message(f"📦 {n_mb} → main_body | {n_dia} → diacritics")
        log_message("🎯 Classification completed successfully.")
        log_message("=" * 60)
