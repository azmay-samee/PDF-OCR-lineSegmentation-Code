# import os
# import numpy as np
# import cv2

# from line import Line
# def bubblesort(CC, start, end, index, order):
#         print('Sorting from index', start, 'to', end - 1, 'based on field', index)
#         for i in range(start, end):
#          for j in range(start, end - 1):
#             name_j = os.path.splitext(CC[j])[0].split('_')
#             name_j1 = os.path.splitext(CC[j + 1])[0].split('_')

#             if index == 4:  # Top
#                 val_j = int(name_j[index].replace('Top', ''))
#                 val_j1 = int(name_j1[index].replace('Top', ''))
#             elif index == 7:  # Right
#                 val_j = int(name_j[index].replace('Right', ''))
#                 val_j1 = int(name_j1[index].replace('Right', ''))
#             else:
#                 continue  # Invalid index

#             if (order == 'ascen' and val_j > val_j1) or (order == 'desc' and val_j < val_j1):
#                 CC[j], CC[j + 1] = CC[j + 1], CC[j]
#         return CC
# def visualize_line(line, dia):
#     # Create a white color image (3 channels)
#     line.full_height = line.full_bottom - line.full_top + 1
#     line.full_width = line.full_right - line.full_left + 1
#     line_img = np.full((line.full_height, line.full_width, 3), 255, dtype=np.uint8)

#     # Draw line components (black text)
#     for CC in line.line_cc:
#         for i in range(CC.height):
#             for j in range(CC.width):
#                 if CC.cc_matrix[i][j] == 0:
#                     x = i + CC.top - line.full_top
#                     y = j + CC.left - line.full_left
#                     line_img[x, y] = (0, 0, 0)  # black

#     # Draw diacritic (RED overlay)
#     dia_color = (0, 0, 255)  # Red
#     for i in range(dia.height):
#         for j in range(dia.width):
#             if dia.cc_matrix[i][j] == 0:
#                 x = i + dia.top - line.full_top
#                 y = j + dia.left - line.full_left
#                 if 0 <= x < line.full_height and 0 <= y < line.full_width:
#                     line_img[x, y] = dia_color

#     # Save + show
#     line_name = f'Sample_Page_1_{dia.name}_Overlap_line_{line.ID}_Top{line.full_top}_Bottom{line.full_bottom}_Left{line.full_left}_Right{line.full_right}.jpg'
#     line_output_dir = r"D:\FYP\Handwritten\Sample_Page_1\line_visualization\overlap"
#     cv2.imwrite(os.path.join(line_output_dir, line_name), line_img)
#     # cv2.imshow(f"{dia.name}", line_img)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()



# LOG_FILE = r"D:\FYP\Handwritten\Sample_Page_1\line_visualization\assignments_log.txt"

# def log(msg):
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(str(msg) + "\n")
# # def attach_diacritics_to_lines(lines, diacritics, y_tol=15):
# #     """
# #     Attach diacritics to their best matching text line.
# #     Uses horizontal overlap first, then vertical distance as a tiebreaker.
# #     """
# #     print("Attaching diacritics to lines with y-tolerance:", y_tol)

# #     # Sort for stability
# #     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
# #     lines = sorted(lines, key=lambda l: l.ID)

# #     for dia in diacritics:
# #         best_line = None
# #         best_score = float("inf")

# #         dia_width = dia.right - dia.left + 1
# #         overlap_candidates = []

# #         for line in lines:
# #             # Compute horizontal overlap
# #             overlap_width = max(0, min(dia.right, line.full_right) - max(dia.left, line.full_left) + 1)
# #             overlap_perc = (overlap_width / dia_width) * 100

# #             if overlap_perc >= 90:
# #                 overlap_candidates.append(line)

# #         # Decision
# #         if len(overlap_candidates) == 1:
# #             best_line = overlap_candidates[0]

# #         elif len(overlap_candidates) > 1:
# #             # Tie-break with vertical distance
# #             dia_center_y = (dia.top + dia.bottom) / 2
# #             for line in overlap_candidates:
# #                 line_center_y = (line.main_top + line.main_bottom) / 2
# #                 vertical_distance = abs(dia_center_y - line_center_y)

# #                 if vertical_distance < best_score:
# #                     best_score = vertical_distance
# #                     best_line = line

# #         # Attach if a best line was found
# #         if best_line:
# #             best_line.AddDiacritic(dia)
# #             visualize_line(best_line, dia)

# #     return lines


# # def attach_diacritics_to_lines(lines, diacritics, y_tol=15):
# #     """
# #     Attach diacritics to their best matching text line.
# #     Uses horizontal overlap first, then zone matching, then vertical distance.
# #     """

# #     print("Attaching diacritics to lines with y-tolerance:", y_tol)

# #     # Sort for stability
# #     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
# #     lines = sorted(lines, key=lambda l: l.ID)

# #     for dia in diacritics:
        
# #         best_line = None
# #         best_score = float("inf")

# #         dia_width = dia.right - dia.left + 1
# #         dia_height= dia.bottom - dia.top + 1    
# #         dia_center_y = (dia.top + dia.bottom) / 2
# #         log(f"{dia.name} \n Dia Width {dia_width} , Dia Center_Y {dia_center_y}")
# #         overlap_candidates = []
# #         log(f"**************************************************")
# #         for line in lines:
# #             log(f"Line ID: {line.ID} | Line Top: {line.main_top} | Line Bottom: {line.main_bottom} | Line Left: {line.main_left} | Line Right: {line.main_right}")
            
# #             # Compute overlap %
# #             overlap_width = max(0, min(dia.right, line.full_right) - max(dia.left, line.full_left) + 1)
# #             overlap_perc = (overlap_width / dia_width) * 100
# #             log(f"Overlap Width: {overlap_width}, Overlap Percentage: {overlap_perc}%")
# #             if overlap_perc >= 90:
# #                 # Estimate baseline + zones for line
# #                 line_height = line.main_bottom - line.main_top
# #                 baseline = line.main_bottom - int(0.2 * line_height)
# #                 log(f"Estimated Baseline for Line {line.ID}: {baseline} , {line_height}")
# #                 # Zone classification
# #                 if dia_center_y < baseline:
# #                     log(f"Diacritic {dia.name} classified as upper zone")
# #                     dia_zone = "upper"
# #                 else:
# #                     log(f"Diacritic {dia.name} classified as lower zone")
# #                     dia_zone = "lower"

# #                 # overlap_candidates.append((line, dia_zone, baseline))
# #                 overlap_candidates.append(line)

# #         # If only one candidate → take it
# #         if len(overlap_candidates) == 1:
# #             best_line = overlap_candidates[0][0]

# #         elif len(overlap_candidates) > 1:
# #             # First try to match by zone
# #             # zone_matched = [c for c in overlap_candidates if (c[1] == "upper" and (dia.top < c[2])) or
# #             #                 (c[1] == "lower" and (dia.bottom > c[2]))]

# #             # if len(zone_matched) == 1:
# #             #     best_line = zone_matched[0][0]

# #             # elif len(zone_matched) > 1:
# #             #     # Tie-break by vertical distance
# #             #     for line, dia_zone, baseline in zone_matched:
# #             #         line_center_y = (line.full_top + line.full_bottom) / 2
# #             #         vertical_distance = abs(dia_center_y - line_center_y)
# #             #         if vertical_distance < best_score:
# #             #             best_score = vertical_distance
# #             #             best_line = line
# #             # else:
# #             #     # fallback: no zone match → use distance among all
# #             #     for line, dia_zone, baseline in overlap_candidates:
# #             #         line_center_y = (line.full_top + line.full_bottom) / 2
# #             #         vertical_distance = abs(dia_center_y - line_center_y)
# #             #         if vertical_distance < best_score:
# #             #             best_score = vertical_distance
# #             #             best_line = line
# #             for line in overlap_candidates:
# #                  overlap_height = max(0, min(dia.top, line.main_bottom) - max(dia.bottom, line.main_top) + 1)
# #                  overlap_perc = (overlap_height / dia_height) * 100
                 

# #                  overlap_candidates.append(line)
            
# #         # Attach diacritic to best line
# #         if best_line:

# #             best_line.AddDiacritic(dia)
# #             visualize_line(best_line, dia)

# #     return lines

# # def attach_diacritics_to_lines(lines, diacritics, y_tol=15):
# #     """
# #     Attach diacritics to their best matching text line.
# #     Uses horizontal overlap first (≥90%), then vertical overlap %, then vertical distance.
# #     """

# #     print("Attaching diacritics to lines with y-tolerance:", y_tol)

# #     # Sort for stability
# #     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
# #     lines = sorted(lines, key=lambda l: l.ID)

# #     for dia in diacritics:
# #         best_line = None
# #         best_score = -1  # use overlap % as score (higher is better)

# #         dia_width = dia.right - dia.left + 1
# #         dia_height = dia.bottom - dia.top + 1
# #         dia_center_y = (dia.top + dia.bottom) / 2
# #         log(f"{dia.name} \n Dia Width {dia_width} , Dia Center_Y {dia_center_y}")
# #         overlap_candidates = []
# #         log(f"**************************************************")

# #         # Step 1: find horizontal overlap ≥ 90%
# #         for line in lines:
# #             log(f"Line ID: {line.ID} | Top: {line.main_top} | Bottom: {line.main_bottom} | Left: {line.main_left} | Right: {line.main_right}")

# #             # Horizontal overlap
# #             overlap_width = max(0, min(dia.right, line.full_right) - max(dia.left, line.full_left) + 1)
# #             overlap_perc = (overlap_width / dia_width) * 100
# #             log(f"Overlap Width: {overlap_width}, Overlap Percentage: {overlap_perc:.2f}%")

# #             if overlap_perc >= 90:
# #                 overlap_candidates.append(line)

# #         # Step 2: If only one candidate → assign directly
# #         if len(overlap_candidates) == 1:
# #             best_line = overlap_candidates[0]

# #         # Step 3: If multiple candidates → check vertical overlap %
# #         elif len(overlap_candidates) > 1:
# #             for line in overlap_candidates:
# #                 overlap_height = max(0, min(dia.bottom, line.main_bottom) - max(dia.top, line.main_top) + 1)
# #                 overlap_perc = (overlap_height / dia_height) * 100
# #                 log(f"Vertical Overlap with Line {line.ID}: {overlap_perc:.2f}%")

# #                 if overlap_perc > best_score:
# #                     best_score = overlap_perc
# #                     best_line = line

# #             # Step 4: If still tied (same %), break tie with vertical distance
# #             if best_line is None and overlap_candidates:
# #                 min_dist = float("inf")
# #                 for line in overlap_candidates:
# #                     line_center_y = (line.full_top + line.full_bottom) / 2
# #                     vertical_distance = abs(dia_center_y - line_center_y)
# #                     if vertical_distance < min_dist:
# #                         min_dist = vertical_distance
# #                         best_line = line

# #         # Step 5: Attach diacritic
# #         if best_line:
# #             best_line.AddDiacritic(dia)
# #             visualize_line(best_line, dia)
# #             log(f"✅ Diacritic {dia.name} → Line {best_line.ID} (score={best_score:.2f})")

# #     return lines



# # def attach_diacritics_to_lines(lines, diacritics, y_tol=15):
# #     """
# #     Attach diacritics to their best matching text line.
# #     Uses horizontal overlap first (≥90%), then vertical overlap %, then vertical distance.
# #     """

# #     print("Attaching diacritics to lines with y-tolerance:", y_tol)

# #     # Sort for stability
# #     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
# #     lines = sorted(lines, key=lambda l: l.ID)

# #     for dia in diacritics:
# #         best_line = None
# #         best_score = -1  # use overlap % as score (higher is better)

# #         dia_width = dia.right - dia.left + 1
# #         dia_height = dia.bottom - dia.top + 1
# #         dia_center_y = (dia.top + dia.bottom) / 2
# #         log(f"{dia.name} \n Dia Width {dia_width} , Dia Center_Y {dia_center_y}")
# #         overlap_candidates = []
# #         log(f"**************************************************")

# #         # Step 1: find horizontal overlap ≥ 90%
# #         for line in lines:
# #             log(f"Line ID: {line.ID} | Top: {line.main_top} | Bottom: {line.main_bottom} | Left: {line.main_left} | Right: {line.main_right}")

# #             # Horizontal overlap
# #             overlap_width = max(0, min(dia.right, line.full_right) - max(dia.left, line.full_left) + 1)
# #             overlap_perc = (overlap_width / dia_width) * 100
# #             log(f"Overlap Width: {overlap_width}, Overlap Percentage: {overlap_perc:.2f}%")

# #             if overlap_perc >= 90:
# #                 overlap_candidates.append(line)

# #         # Step 2: If only one candidate → assign directly
# #         if len(overlap_candidates) == 1:
# #             best_line = overlap_candidates[0]

# #         # Step 3: If multiple candidates → check vertical overlap %
# #         elif len(overlap_candidates) > 1:
# #             for line in overlap_candidates:
# #                 overlap_height = max(0, min(dia.bottom, line.main_bottom) - max(dia.top, line.main_top) + 1)
# #                 overlap_perc = (overlap_height / dia_height) * 100
# #                 log(f"Vertical Overlap with Line {line.ID}: {overlap_perc:.2f}%")

# #                 if overlap_perc > best_score:
# #                     best_score = overlap_perc
# #                     best_line = line

# #             # Step 4: If still tied (same %), break tie with vertical distance
# #             if best_line is None and overlap_candidates:
# #                 min_dist = float("inf")
# #                 for line in overlap_candidates:
# #                     line_center_y = (line.full_top + line.full_bottom) / 2
# #                     vertical_distance = abs(dia_center_y - line_center_y)
# #                     if vertical_distance < min_dist:
# #                         min_dist = vertical_distance
# #                         best_line = line

# #         # Step 5: Attach diacritic
# #         if best_line:
# #             best_line.AddDiacritic(dia)
# #             visualize_line(best_line, dia)
# #             log(f"✅ Diacritic {dia.name} → Line {best_line.ID} (score={best_score:.2f})")

# #     return lines

# # def get_adaptive_vert_thresh(dia_height):
# #     """
# #     Adaptive vertical threshold based on diacritic size.
# #     Small diacritics = lower threshold, larger ones = higher.
# #     """
# #     if dia_height <= 5:     # very tiny dot
# #         return 30
# #     elif dia_height <= 12:  # medium (zer/zabar/pesh)
# #         return 40
# #     else:                   # larger marks (hamza, madda, tashdid)
# #         return 60


# # def attach_diacritics_to_lines(lines, diacritics, horiz_thresh=90):
# #     """
# #     Attach diacritics to their best matching text line.
# #     Conditions:
# #       1. Horizontal overlap >= horiz_thresh
# #       2. Vertical overlap >= adaptive threshold
# #       3. If multiple lines qualify → pick line with min vertical distance
# #     """

# #     # Sort for consistency
# #     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
# #     lines = sorted(lines, key=lambda l: l.ID)

# #     for dia in diacritics:
# #         best_line = None
# #         best_score = -1
# #         best_distance = float("inf")

# #         dia_width = dia.right - dia.left + 1
# #         dia_height = dia.bottom - dia.top + 1
# #         dia_center_y = (dia.top + dia.bottom) / 2

# #         # Adaptive vertical threshold
# #         vert_thresh = get_adaptive_vert_thresh(dia_height)

# #         for line in lines:
# #             # Horizontal overlap
# #             horiz_overlap = max(0, min(dia.right, line.full_right) - max(dia.left, line.full_left) + 1)
# #             horiz_perc = (horiz_overlap / dia_width) * 100

# #             if horiz_perc < horiz_thresh:
# #                 continue

# #             # Vertical overlap
# #             vert_overlap = max(0, min(dia.bottom, line.main_bottom) - max(dia.top, line.main_top) + 1)
# #             vert_perc = (vert_overlap / dia_height) * 100

# #             if vert_perc < vert_thresh:
# #                 continue

# #             # Vertical distance (for tie-breaking)
# #             line_center_y = (line.full_top + line.full_bottom) / 2
# #             vert_distance = abs(dia_center_y - line_center_y)

# #             # Scoring: prefer higher overlap, then closer distance
# #             score = horiz_perc + vert_perc
# #             if score > best_score or (score == best_score and vert_distance < best_distance):
# #                 best_score = score
# #                 best_distance = vert_distance
# #                 best_line = line

# #         # Attach diacritic to chosen line
# #         if best_line:
# #             best_line.AddDiacritic(dia)
# #             visualize_line(best_line, dia)

# #     return lines



# def get_adaptive_vert_thresh(dia_height):
#     """
#     Adaptive vertical threshold based on diacritic size.
#     Small diacritics = lower threshold, larger ones = higher.
#     """
#     if dia_height <= 5:     # very tiny dot
#         return 30
#     elif dia_height <= 12:  # medium (zer/zabar/pesh)
#         return 40
#     else:                   # larger marks (hamza, madda, tashdid)
#         return 60

# def get_adaptive_vert_thresh(dia_height: int) -> float:
#     """
#     Adaptive vertical-overlap threshold (% of diacritic height that must overlap the line).
#     Tune these cutoffs to your data.
#     """
#     if dia_height <= 5:      # tiny single dots
#         return 30.0
#     elif dia_height <= 12:   # small marks (zer/zabar/pesh)
#         return 40.0
#     else:                    # larger marks (hamza, madda, tashdid, etc.)
#         return 60.0


# def attach_diacritics_to_lines(lines, diacritics, horiz_thresh=90.0):
#     """
#     Attach each diacritic to the best line.

#     Rules:
#       1) Prefer lines that FULLY CONTAIN the diacritic bbox (both axes). If >1, pick the one
#          with minimum vertical distance to the line center.
#       2) Otherwise, consider lines that INTERSECT the diacritic bbox (both axes).
#          Keep only those that satisfy BOTH:
#             - horizontal overlap % >= horiz_thresh
#             - vertical overlap %   >= adaptive threshold (based on dia height)
#          If multiple qualify, pick the one with:
#             (a) larger horizontal overlap %, then
#             (b) larger vertical overlap %, then
#             (c) smaller vertical distance to line center.
#       3) Fallbacks if none qualifies:
#             - If any intersect: pick the one with max (horizontal% + vertical%), tiebreak by min distance.
#             - Else: pick global nearest line by vertical distance (rare).
#     """

#     # Stable ordering
#     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
#     lines = sorted(lines, key=lambda l: l.ID)

#     for dia in diacritics:
#         dia_width  = dia.right - dia.left + 1
#         dia_height = dia.bottom - dia.top + 1
#         dia_center_y = (dia.top + dia.bottom) / 2.0

#         # --- Collect containment and overlap candidates ---
#         containers = []   # lines that fully contain the diacritic bbox (both axes)
#         overlaps  = []   # lines whose bbox intersects the diacritic bbox (both axes)
    

#         for line in lines:
#             # Line bbox
#             L, R = line.full_left,  line.full_right
#             T, B = line.full_top,   line.full_bottom

#             # Full containment (both axes)
#             is_inside = (dia.left >= L and dia.right <= R and
#                          dia.top  >= T and dia.bottom <= B)
#             if is_inside:
#                 containers.append(line)
#                 continue

#             # Intersection (both axes)
#             horiz_intersect = not (dia.right < L or dia.left > R)
#             vert_intersect  = not (dia.bottom < T or dia.top > B)
#             if horiz_intersect and vert_intersect:
#                 overlaps.append(line)
          

#         # --- Case 1: Containment winners ---
#         if containers:
#             # Choose the container with min vertical distance to line center
#             best_line = min(
#                 containers,
#                 key=lambda ln: abs(dia_center_y - ((ln.full_top + ln.full_bottom) / 2.0))
#             )
#             best_line.AddDiacritic(dia)
#             continue

#         # --- Case 2: No containers → evaluate overlaps with thresholds ---
#         qualified = []
#         vert_thresh = get_adaptive_vert_thresh(dia_height)

#         for line in overlaps:
#             # Line bbox
#             L, R = line.full_left,  line.full_right
#             T, B = line.full_top,   line.full_bottom

#             # Horizontal overlap %
#             overlap_w = max(0, min(dia.right, R) - max(dia.left, L) + 1)
#             horiz_perc = (overlap_w / dia_width) * 100.0

#             # Vertical overlap %
#             overlap_h = max(0, min(dia.bottom, B) - max(dia.top, T) + 1)
#             vert_perc = (overlap_h / dia_height) * 100.0

#             if horiz_perc >= horiz_thresh and vert_perc >= vert_thresh:
#                 line_center_y = (T + B) / 2.0
#                 vert_dist = abs(dia_center_y - line_center_y)
#                 qualified.append((line, horiz_perc, vert_perc, vert_dist))

#         if qualified:
#             # Pick by: max horiz%, then max vert%, then min distance
#             best_line, _, _, _ = max(
#                 qualified,
#                 key=lambda t: (t[1], t[2], -t[3])
#             )
#             best_line.AddDiacritic(dia)
#             continue

#         # --- Case 3: Fallbacks ---
#         if overlaps:
#             # Soft-score the overlaps (even if thresholds failed)
#             scored = []
#             for line in overlaps:
#                 L, R = line.full_left,  line.full_right
#                 T, B = line.full_top,   line.full_bottom

#                 overlap_w = max(0, min(dia.right, R) - max(dia.left, L) + 1)
#                 horiz_perc = (overlap_w / dia_width) * 100.0

#                 overlap_h = max(0, min(dia.bottom, B) - max(dia.top, T) + 1)
#                 vert_perc = (overlap_h / dia_height) * 100.0

#                 line_center_y = (T + B) / 2.0
#                 vert_dist = abs(dia_center_y - line_center_y)

#                 scored.append((line, horiz_perc, vert_perc, vert_dist))

#             best_line, _, _, _ = max(scored, key=lambda t: (t[1] + t[2], -t[3]))
#             best_line.AddDiacritic(dia)
#             continue
#         # --- Case 4: Partial Overlaps
#         # if partial_overlap:
#         #     score_partial=[]
#         #     horizontal_score=5
#         #     for line in partial_overlap:
#         #         L, R = line.full_left,  line.full_right
#         #         T, B = line.full_top,   line.full_bottom
#         #         line_center_y = (T + B) / 2.0
#         #         vert_dist = abs(dia_center_y - line_center_y)
                
#         #         score_partial.append((line, horizontal_score, vert_dist))
#         #     if score_partial:
#         #         best_line, _, _ = max(score_partial, key=lambda t: (t[1], -t[2]))
#         #         best_line.AddDiacritic(dia)
#         #         continue
            



        

#         # Last-resort: pick the globally nearest line by vertical distance
#         best_line = min(
#             lines,
#             key=lambda ln: abs(dia_center_y - ((ln.full_top + ln.full_bottom) / 2.0))
#         )
#         best_line.AddDiacritic(dia)

#     return lines
import os
from tracemalloc import start
import numpy as np
import cv2

from line import Line
def bubblesort(CC, start, end, index, order):
        print('Sorting from index', start, 'to', end - 1, 'based on field', index)
        for i in range(start, end):
         for j in range(start, end - 1):
            name_j = os.path.splitext(CC[j])[0].split('_')
            name_j1 = os.path.splitext(CC[j + 1])[0].split('_')

            if index == 4:  # Top
                val_j = int(name_j[index].replace('Top', ''))
                val_j1 = int(name_j1[index].replace('Top', ''))
            elif index == 7:  # Right
                val_j = int(name_j[index].replace('Right', ''))
                val_j1 = int(name_j1[index].replace('Right', ''))
            else:
                continue  # Invalid index

            if (order == 'ascen' and val_j > val_j1) or (order == 'desc' and val_j < val_j1):
                CC[j], CC[j + 1] = CC[j + 1], CC[j]
        return CC
def visualize_line(line, dia, line_output_dir):

    line.full_height = line.full_bottom - line.full_top + 1
    line.full_width = line.full_right - line.full_left + 1
    line_img = np.full((line.full_height, line.full_width, 3), 255, dtype=np.uint8)

    # Draw line components (black text)
    for CC in line.line_cc:
        for i in range(CC.height):
            for j in range(CC.width):
                if CC.cc_matrix[i][j] == 0:
                    x = i + CC.top - line.full_top
                    y = j + CC.left - line.full_left
                    line_img[x, y] = (0, 0, 0)  # black

    # Draw diacritic (RED overlay)
    dia_color = (0, 0, 255)  # Red
    for i in range(dia.height):
        for j in range(dia.width):
            if dia.cc_matrix[i][j] == 0:
                x = i + dia.top - line.full_top
                y = j + dia.left - line.full_left
                if 0 <= x < line.full_height and 0 <= y < line.full_width:
                    line_img[x, y] = dia_color

    # Save + show
    line_name = f'1209_Page_3_line_{line.ID}_Top{line.full_top}_Bottom{line.full_bottom}_Left{line.full_left}_Right{line.full_right}_dia.jpg'
    #line_output_dir = r"D:\FYP\Handwritten\Sample_Page_1\line_visualization\overlap"
   # print("******************************",dia.name)
    filename_without_ext, _ = os.path.splitext(dia.name)
    line_output = os.path.join(line_output_dir,str(line.ID), filename_without_ext)
    os.makedirs(line_output, exist_ok=True)
    cv2.imwrite(os.path.join(line_output, line_name), line_img)
    cv2.imwrite(os.path.join(line_output, f'1209_Page_3_line_{line.ID}_Top{line.main_top}_Bottom{line.main_bottom}_Left{line.main_left}_Right{line.main_right}.jpg'), line.main_image)   
  
  
    # cv2.imshow(f"{dia.name}", line_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



LOG_FILE = r"D:\FYP\Handwritten\Sample_Page_1\line_visualization\assignment00.txt"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")



def get_slope_direction_with_visual(binary_img, color=(255, 0, 0), thickness=1):
    """
    Estimate slope of the main body in a binary image and draw the fitted line.

    Args:
        binary_img (np.ndarray): Binary image (0 = text, 255 = background).
        color (tuple): Line color in BGR (default blue).
        thickness (int): Line thickness.

    Returns:
        slope (float): slope of the best-fit line (dy/dx) with corrected sign.
        direction (str): 'rising_right', 'falling_right', or 'horizontal'.
        vis_img (np.ndarray): Visualization image with line drawn.
    """
    # Get coordinates of black pixels
    ys, xs = np.where(binary_img == 0)
    if len(xs) < 2:
        return 0, "undefined", cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

    # Fit line
    [vx, vy, x0, y0] = cv2.fitLine(np.column_stack((xs, ys)).astype(np.float32),
                                   cv2.DIST_L2, 0, 0.01, 0.01)
    slope = vy / vx

    # --- Correct sign because y increases downward in images ---
    slope = -slope  

    # Decide direction
    if slope > 0.1:
        direction = "right"
    elif slope < -0.1:
        direction = "left"
    else:
        direction = "horizontal"

    # Convert to color for drawing
    vis_img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

    # Draw the line across image width
    h, w = binary_img.shape
    left_y  = int(y0 - (x0 * vy / vx))
    right_y = int(y0 + ((w - x0) * vy / vx))
    cv2.line(vis_img, (0, left_y), (w-1, right_y), color, thickness)

    return float(slope), direction, vis_img


def calculate_bottom(line, dia):
    dia_center=(dia.top+dia.bottom)/2
    if dia_center > line.main_bottom:
        return dia_center - line.main_bottom

    return 0

def calculate_top(line, dia):
    dia_center=(dia.top+dia.bottom)/2
    if dia_center < line.main_top:
        return line.main_top - dia_center
    
    return  0
def mainBody(line, dia, margin=3):
    def horizontal_overlap(dia, cc):
        """Compute horizontal overlap percentage between dia and cc"""
        overlap_left = max(dia.left, cc.left)
        overlap_right = min(dia.right, cc.right)
        overlap_width = max(0, overlap_right - overlap_left)
        dia_width = dia.right - dia.left
        return (overlap_width / dia_width) * 100 if dia_width > 0 else 0

    for idx, CCs in enumerate(line.main_cc):
        log(f"Checking CC {CCs.name} for diacritic {dia.name}")
        log(f"{dia.name}")
        log(f"{CCs.left} {CCs.right} {CCs.top} {CCs.bottom}")
        log(f"Dia bbox: Left {dia.left}, Right {dia.right}, Top {dia.top}, Bottom {dia.bottom}")
        # Case 1: fully contained with margin
        if dia.left >= CCs.left - margin and dia.right <= CCs.right + margin:
            log(f"fulfilled")
            log(f"{dia.name}")
            log(f"{CCs.left} {CCs.right} {CCs.top} {CCs.bottom}")
            overlap_perc=horizontal_overlap(dia, CCs)
            return CCs

        # Case 2: partially overlapping → check neighbors
        if dia.left >= CCs.left or dia.right <= CCs.right:
            candidates = []
            
            # current CC
            candidates.append((horizontal_overlap(dia, CCs), CCs))
            
            # left neighbor
            if idx > 0:
                prevCC = line.main_cc[idx - 1]
                candidates.append((horizontal_overlap(dia, prevCC), prevCC))
            
            # right neighbor
            if idx < len(line.main_cc) - 1:
                nextCC = line.main_cc[idx + 1]
                candidates.append((horizontal_overlap(dia, nextCC), nextCC))
            
            # pick the one with the highest horizontal overlap
            best_overlap, bestCC = max(candidates, key=lambda x: x[0])
            
            if best_overlap > 0:  # only return if there's some overlap
                log(f"Best match is {bestCC.name} with overlap {best_overlap:.2f}%")
                return bestCC

    return None     


# def attach_diacritics_to_lines(lines, diacritics, margin=0, debug_dir=None):
#     """
#     Attach diacritic components to their most likely text line.
#     Strategy:
#       1. Containment → safest
#       2. Strong inside preference (horizontal overlap + vertical center inside band)
#       3. Overlap + baseline/topline + neighbor validation → robust
#       4. Fallback → nearest vertical line using normalized distance
#     """

#     # Sort for deterministic behavior
#     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
#     lines = sorted(lines, key=lambda l: l.ID)

#     # average line height for tolerance in inside-preference
#     avg_height = np.mean([max(1, l.main_bottom - l.main_top) for l in lines])

#     for dia in diacritics:
#         dia_cy = (dia.top + dia.bottom) / 2.0
#         dia_cx = (dia.left + dia.right) / 2.0
#         best_line = None

#         containers, overlaps = [], []

#         # --- Pass 1: containment & overlap ---
#         for line in lines:
#             L, R, T, B = line.main_left, line.main_right, line.main_top, line.main_bottom

#             is_inside = (
#                 dia.left >= L - margin and dia.right <= R + margin and
#                 dia.top >= T - margin and dia.bottom <= B + margin
#             )
#             horiz_intersect = not (dia.right < L - margin or dia.left > R + margin)
#             vert_intersect = not (dia.bottom < T - margin or dia.top > B + margin)

#             if is_inside:
#                 containers.append(line)
#             elif horiz_intersect and vert_intersect:
#                 overlaps.append(line)

#         # --- Case 1: Full containment ---
#         if containers:
#             best_line = min(
#                 containers,
#                 key=lambda ln: abs(dia_cy - ((ln.main_top + ln.main_bottom) / 2.0))
#             )
#             best_line.AddDiacritic(dia)
#             continue

#         # --- Case 2: Strong inside preference ---
#         if overlaps:
#             assigned = False
#             for line in overlaps:
#                 if dia.left <= line.main_right and dia.right >= line.main_left:
#                     # horizontally overlaps
#                     tol_top = line.main_top - 0.1 * avg_height
#                     tol_bottom = line.main_bottom + 0.1 * avg_height
#                     if tol_top <= dia_cy <= tol_bottom:
#                         line.AddDiacritic(dia)
#                         assigned = True
#                         if debug_dir:
#                             os.makedirs(debug_dir, exist_ok=True)
#                             with open(os.path.join(debug_dir, f"force_{getattr(dia,'name',id(dia))}.txt"), "w") as f:
#                                 f.write(f"Forced inside preference -> assigned to line {line.ID}\n")
#                         break
#             if assigned:
#                 continue

#         # # --- Case 3: Overlaps with baseline/topline + neighbor validation ---
#         if overlaps:
#             best_line = None
#             best_score = float("-inf")

#             for i, line in enumerate(lines):
#                 if line not in overlaps:
#                     continue

#                 baseline_func, topline_func, _, _ = estimate_line_curves(line, "poly")
#                 baseline_y = baseline_func(dia_cx)
#                 topline_y = topline_func(dia_cx)

#                 # relative position wrt current line
#                 if dia_cy < line.main_top:
#                     pos = "above"
#                     dist_curr = topline_y - dia_cy
#                 elif dia_cy > line.main_bottom:
#                     pos = "below"
#                     dist_curr = dia_cy - baseline_y
#                 else:
#                     pos = "inside"
#                     dist_curr = min(abs(dia_cy - line.main_top), abs(dia_cy - baseline_y))

#                 # overlap %
#                 curr_overlap, _ = mainBody(line, dia)

#                 # normalize distance by line height
#                 line_height = max(1, (line.main_bottom - line.main_top))
#                 norm_dist = dist_curr / line_height

#                 # weighted score: prefer distance (80%) and overlap (20%)
#                 overlap_norm = curr_overlap / 100.0
#                 curr_score = (0.2 * overlap_norm) + (0.8 * (1 - norm_dist))

#                 chosen_line, chosen_score = line, curr_score

#                 # --- Neighbor check ---
#                 if pos == "below" and i + 1 < len(lines):
#                     neighbor = lines[i + 1]
#                     n_base, n_top, _, _ = estimate_line_curves(neighbor, "poly")
#                     dist_next = abs(dia_cy - n_top(dia_cx))
#                     neighbor_perc, _ = mainBody(neighbor, dia)
#                     neighbor_height = max(1, (neighbor.main_bottom - neighbor.main_top))
#                     norm_dist_next = dist_next / neighbor_height
#                     neighbor_overlap_norm = neighbor_perc / 100.0
#                     neighbor_score = (0.2 * neighbor_overlap_norm) + (0.8 * (1 - norm_dist_next))
#                     if neighbor_score > chosen_score:
#                         chosen_line, chosen_score = neighbor, neighbor_score

#                 elif pos == "above" and i - 1 >= 0:
#                     neighbor = lines[i - 1]
#                     n_base, n_top, _, _ = estimate_line_curves(neighbor, "poly")
#                     dist_prev = abs(dia_cy - n_base(dia_cx))
#                     neighbor_perc, _ = mainBody(neighbor, dia)
#                     neighbor_height = max(1, (neighbor.main_bottom - neighbor.main_top))
#                     norm_dist_prev = dist_prev / neighbor_height
#                     neighbor_overlap_norm = neighbor_perc / 100.0
#                     neighbor_score = (0.2 * neighbor_overlap_norm) + (0.8 * (1 - norm_dist_prev))
#                     if neighbor_score > chosen_score:
#                         chosen_line, chosen_score = neighbor, neighbor_score

#                 # --- Update global best ---
#                 if chosen_score > best_score:
#                     best_line, best_score = chosen_line, chosen_score

#             if best_line is not None:
#                 best_line.AddDiacritic(dia)
#                 continue
       
#         # --- Case 4: Fallback to nearest line vertically ---
#         best_line, best_score = None, float("inf")
#         for line in lines:
#             T, B = line.main_top, line.main_bottom
#             line_height = max(1, B - T)

#             if dia_cy < T:
#                 dist = T - dia.bottom
#             elif dia_cy > B:
#                 dist = dia.top - B
#             else:
#                 dist = 0

#             norm_dist = dist / line_height

#             if norm_dist < best_score:
#                 best_score = norm_dist
#                 best_line = line

#         if best_line:
#             best_line.AddDiacritic(dia)

#     return lines


# def attach_diacritics_to_lines(lines, diacritics, margin, debug_dir):
#     # Stable ordering
#     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
#     lines = sorted(lines, key=lambda l: l.ID)

#     for dia in diacritics:
#         dia_cy = (dia.top + dia.bottom) / 2.0

#         # --- Collect containment and overlap candidates ---
#         # lines that fully contain the diacritic bbox (both axes)
#         overlaps  = []    # lines whose bbox intersects the diacritic bbox (both axes)

#         log(f"{dia.name}")
#         margin = 0

#         for line in lines:
#             L, R, T, B = line.main_left, line.main_right, line.main_top, line.main_bottom

#             is_inside = (
#                 dia.left >= L - margin and dia.right <= R + margin and
#                 dia.top >= T - margin and dia.bottom <= B + margin
#             )
#             horiz_intersect = not (dia.right < L - margin or dia.left > R + margin)
#             vert_intersect  = not (dia.bottom < T - margin or dia.top > B + margin)

#             if is_inside:
               
#                 line.AddDiacritic(dia)
#                 break
#             elif horiz_intersect and vert_intersect:
#                 overlaps.append(line)
#                 break

        
#         # --- Case 2: overlaps but not contained ---
#         over_lines = {}
        

#         for line in overlaps:
#             log(f"{dia.name}")
#             log(f"Processing Key line ID: {line.ID}")
            
#             if dia.top < line.main_top:
#                     prev_line = lines[line.ID - 1] if line.ID - 1 >= 0 else None
#                     lines_array = [line]
#                     if prev_line:
#                         lines_array.append(prev_line)
#                     over_lines[line.ID] = (lines_array, "above")

#             elif dia.bottom > line.main_bottom:
#                     next_line = lines[line.ID + 1] if line.ID + 1 < len(lines) else None
#                     lines_array = [line]
#                     if next_line:
#                         lines_array.append(next_line)
#                     over_lines[line.ID] = (lines_array, "below")

#             else:
#                     best_line = line
#                     output_dir = r"D:\FYP\Data\line_segmentation\connected_components\1209_Page_3\v_overlap"
#                     visualize_line(best_line, dia, output_dir)
#                     best_line.AddDiacritic(dia)
#                     continue
            
            
            

#         # pick the best line from overlap candidates
#         min_dist = 9999
#         best_lineID = -1
#         UD_distance=9999
#         DD_distance=9999
        
#         for key, (lines_array, status) in over_lines.items():
#             # ... your scanning logic (unchanged) ...
#             for i in range(len(lines_array)):
#                 current_line = lines_array[i]
#                 img = current_line.main_image
#                 line_height = current_line.main_bottom - current_line.main_top + 1
#                 dia_left = max(dia.left, current_line.main_left) - current_line.main_left + 1
#                 dia_right = min(dia.right, current_line.main_right) - current_line.main_left + 1

#                 if dia_left >= img.shape[1] or dia_right < 0:
#                     continue

#                 # top/bottom calculation depending on status & i
#                 if status == "above" and i == 0:
#                     start = calculate_top(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(0, line_height)
#                 elif status == "above" and i == 1:
#                     start = calculate_bottom(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(line_height - 1, -1, -1)
#                 elif status == "below" and i == 0:
#                     start = calculate_bottom(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(line_height - 1, -1, -1)
#                 elif status == "below" and i == 1:
#                     start = calculate_top(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(0, line_height)
#                 else:
#                     continue

              
#                 dist_above0=9999
#                 dist_above1=9999
#                 dist_below0=9999
#                 dist_below1=9999
#                 id_above=-1
#                 id_below=-1
#                 for kk in kk_range:
#                     x_range = range(dia_left, dia_right + 1)
                    
#                     for j in x_range:
#                         if 0 <= j < img.shape[1] and img[kk, j] == 0:
#                             if status == "above" and i == 0:

#                                 dist = distance_offset + kk
#                                 dist_above0 = min(dist_above0, dist)
#                             elif status == "above" and i == 1:
#                                 dist = distance_offset + (line_height - kk - 1)
#                                 dist_above1 = min(dist_above1, dist)
#                             elif status == "below" and i == 0:
#                                 dist = distance_offset + (line_height - kk - 1)
#                                 dist_below0 = min(dist_below0, dist)
#                             elif status == "below" and i == 1:
#                                 dist = distance_offset + kk
#                                 dist_below1 = min(dist_below1, dist)

#                 if dist_above0!=9999 and dist_above0 < UD_distance:   
#                     UD_distance=dist_above0
#                     id_above=current_line.ID

                    
#                 if dist_above1!=9999 and dist_above1 < UD_distance:
#                     UD_distance=dist_above1
#                     id_above=current_line.ID

#                 if dist_below0!=9999 and dist_below0 < DD_distance:
#                     DD_distance=dist_below0
#                     id_below=current_line.ID
                   
#                 if dist_below1!=9999 and dist_below1 < DD_distance:
#                     DD_distance=dist_below1
#                     id_below=current_line.ID   
#         if UD_distance < DD_distance and UD_distance !=9999:
#             best_lineID=id_above 
#         elif DD_distance !=9999:
#             best_lineID=id_below

                
#         # only add once after best line is found
#         if best_lineID != -1:
#             best_line = lines[best_lineID]
#             best_line.AddDiacritic(dia)
#             continue

#         # --- Case 3: fallback (no overlap/containment) ---
#         best_line, best_score = None, float("inf")
#         for line in lines:
#             T, B = line.main_top, line.main_bottom
#             line_height = max(1, B - T)

#             if dia_cy < T:
#                 dist = T - dia.bottom
#             elif dia_cy > B:
#                 dist = dia.top - B
#             else:
#                 dist = 0

#             norm_dist = dist / line_height
#             if norm_dist < best_score:
#                 best_score = norm_dist
#                 best_line = line

#         if best_line:
#             best_line.AddDiacritic(dia)

#     return lines      
# def attach_diacritics_to_lines(lines, diacritics, margin, debug_dir):
#     # Stable ordering
#     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
#     lines = sorted(lines, key=lambda l: l.ID)

#     for dia in diacritics:
#         dia_width  = dia.right - dia.left + 1
#         dia_height = dia.bottom - dia.top + 1
#         dia_cy = (dia.top + dia.bottom) / 2.0

#         # --- Collect containment and overlap candidates ---
#         containers = []   # lines that fully contain the diacritic bbox (both axes)
#         overlaps  = []    # lines whose bbox intersects the diacritic bbox (both axes)

#         log(f"{dia.name}")
#         margin = 0

#         for line in lines:
#             L, R, T, B = line.main_left, line.main_right, line.main_top, line.main_bottom

#             is_inside = (
#                 dia.left >= L - margin and dia.right <= R + margin and
#                 dia.top >= T - margin and dia.bottom <= B + margin
#             )
#             horiz_intersect = not (dia.right < L - margin or dia.left > R + margin)
#             vert_intersect  = not (dia.bottom < T - margin or dia.top > B + margin)

#             if is_inside:
#                 containers.append(line)
#             elif horiz_intersect and vert_intersect:
#                 overlaps.append(line)

#         # --- Case 1: fully contained ---
#         if containers:
#             best_line = min(
#                 containers,
#                 key=lambda ln: abs(dia_cy - ((ln.main_top + ln.main_bottom) / 2.0))
#             )
#             best_line.AddDiacritic(dia)
#             continue

#         # --- Case 2: overlaps but not contained ---
#         over_lines = {}
#         for line in overlaps:
#             log(f"{dia.name}")
#             log(f"Processing Key line ID: {line.ID}")

#             if dia.top < line.main_top:
#                 prev_line = lines[line.ID - 1] if line.ID - 1 >= 0 else None
#                 lines_array = [line]
#                 if prev_line:
#                     lines_array.append(prev_line)
#                 over_lines[line.ID] = (lines_array, "above")

#             elif dia.bottom > line.main_bottom:
#                 next_line = lines[line.ID + 1] if line.ID + 1 < len(lines) else None
#                 lines_array = [line]
#                 if next_line:
#                     lines_array.append(next_line)
#                 over_lines[line.ID] = (lines_array, "below")

#             else:
#                 best_line = line
#                 output_dir = r"D:\FYP\Data\line_segmentation\connected_components\1209_Page_3\v_overlap"
#                 visualize_line(best_line, dia, output_dir)
#                 best_line.AddDiacritic(dia)
#                 continue

#         # pick the best line from overlap candidates
#         min_dist = 9999
#         best_lineID = -1

#         for key, (lines_array, status) in over_lines.items():
#             for i in range(len(lines_array)):
#                 current_line = lines_array[i]
#                 img = current_line.main_image
#                 line_height = current_line.main_bottom - current_line.main_top + 1
#                 dia_left = max(dia.left, current_line.main_left) - current_line.main_left + 1
#                 dia_right = min(dia.right, current_line.main_right) - current_line.main_left + 1

#                 if dia_left >= img.shape[1] or dia_right < 0:
#                     continue

#                 # top/bottom calculation depending on status & i
#                 if status == "above" and i == 0:
#                     start = calculate_top(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(0, line_height)
#                 elif status == "above" and i == 1:
#                     start = calculate_bottom(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(line_height - 1, -1, -1)
#                 elif status == "below" and i == 0:
#                     start = calculate_bottom(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(line_height - 1, -1, -1)
#                 elif status == "below" and i == 1:
#                     start = calculate_top(current_line, dia)
#                     distance_offset = start
#                     kk_range = range(0, line_height)
#                 else:
#                     continue

#                 mar = 0
#                 log(f"processing lineid {current_line.ID} and status {status}")
#                 log(f"start {start}")

#                 # scan vertically
#                 found = False
#                 for kk in kk_range:
#                     diaImg = dia.cc_matrix
#                     _, binary = cv2.threshold(diaImg, 127, 255, cv2.THRESH_BINARY)
#                     slope, direction, _ = get_slope_direction_with_visual(binary)

#                     if direction == "right":
#                         x_range = range(dia_right + mar, dia_left - 1 - mar, -1)
#                     else:
#                         x_range = range(dia_left - mar, dia_right + 1 + mar)

#                     for j in x_range:
#                         if 0 <= j < img.shape[1] and img[kk, j] == 0:
#                             # --- Weighted distance formula ---
#                             start_weight = 0.6   # give 60% priority to start offset
#                             kk_weight = 0.4      # 40% to pixel-level intersection

#                             if status == "above" and i == 0:
#                                 dist = start_weight * distance_offset + kk_weight * kk
#                             elif status == "above" and i == 1:
#                                 dist = start_weight * distance_offset + kk_weight * (line_height - kk - 1)
#                             elif status == "below" and i == 0:
#                                 dist = start_weight * distance_offset + kk_weight * (line_height - kk - 1)
#                             else:
#                                 dist = start_weight * distance_offset + kk_weight * kk

#                             if dist < min_dist:
#                                 min_dist = dist
#                                 best_lineID = current_line.ID
#                                 log(f"Now {best_lineID}")
#                             found = True
#                             break
#                     if found:
#                         break

#         # only add once after best line is found
#         if best_lineID != -1:
#             best_line = lines[best_lineID]
#             best_line.AddDiacritic(dia)
#             log(f"final {best_lineID}")
#             continue

#         # --- Case 3: fallback (no overlap/containment) ---
#         best_line, best_score = None, float("inf")
#         for line in lines:
#             T, B = line.main_top, line.main_bottom
#             line_height = max(1, B - T)

#             if dia_cy < T:
#                 dist = T - dia.bottom
#             elif dia_cy > B:
#                 dist = dia.top - B
#             else:
#                 dist = 0

#             norm_dist = dist / line_height
#             if norm_dist < best_score:
#                 best_score = norm_dist
#                 best_line = line

#         if best_line:
#             best_line.AddDiacritic(dia)

#     return lines
def overlap_ratio(line1, line2):
    """Compute vertical overlap ratio between two lines."""
    overlap_top = max(line1.main_top, line2.main_top)
    overlap_bottom = min(line1.main_bottom, line2.main_bottom)
    overlap_height = max(0, overlap_bottom - overlap_top)

    avg_height = (line1.main_bottom - line1.main_top + line2.main_bottom - line2.main_top) / 2
    return overlap_height / avg_height if avg_height > 0 else 0.0


def merge_close_lines(lines, gap_threshold=10, overlap_threshold=0.25):
    """
    Merge lines that are vertically close or overlapping.

    Args:
        lines (list[Line]): list of Line objects sorted top to bottom
        gap_threshold (int): max allowed vertical gap (in pixels) to merge
        overlap_threshold (float): required vertical overlap ratio to merge

    Returns:
        list[Line]: merged and re-indexed line list
    """
    if not lines:
        return []

    # Sort lines by their top coordinate
    lines.sort(key=lambda L: L.main_top)
    for i in lines:
        print(i.ID)
    merged_lines = []
    current = lines[0]

    for nxt in lines[1:]:
        # Compute vertical gap and overlap
        gap = nxt.main_top - current.main_bottom
        ov_ratio = overlap_ratio(current, nxt)
        print(f"Gap: {gap}, Overlap Ratio: {ov_ratio:.2f}")
        # Merge if overlapping enough or within gap threshold
        if ov_ratio > overlap_threshold :
            # Expand current line bounds
            current.main_top = min(current.main_top, nxt.main_top)
            current.main_bottom = max(current.main_bottom, nxt.main_bottom)
            current.main_left = min(current.main_left, nxt.main_left)
            current.main_right = max(current.main_right, nxt.main_right)

            # Merge CCs
            current.main_cc.extend(nxt.main_cc)
            current.line_cc.extend(nxt.line_cc)
            current.diacritics.extend(nxt.diacritics)

            # Recompute full bounds after merging
            current.recompute_full_bounds()
        else:
            merged_lines.append(current)
            current = nxt

    # Append the last one
    merged_lines.append(current)

    # ✅ Fix: reassign continuous IDs (0, 1, 2, …)
    for idx, line in enumerate(merged_lines):
        line.ID = idx

    return merged_lines
