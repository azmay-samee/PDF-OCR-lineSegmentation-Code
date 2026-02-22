import cv2
from skimage import img_as_ubyte
from skimage.filters import threshold_sauvola
import numpy as np
import os
from image_processor import ImageProcessor
LOG_FILE = r"D:\FYP\Handwritten\Sample_Page_1\line_visualization\dia_distance.txt"
def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:  
        f.write(str(msg) + "\n")

import cv2
import numpy as np
from skimage import img_as_ubyte

def calculate_bottom(line, dia):
    dia_center=(dia.top+dia.bottom)/2
    distance_offset=0
    dia_distance=0

    if dia_center>line.main_bottom:
        dia_distance=dia_center- dia.top
        distance_offset=dia.top - line.main_bottom
        start=(line.main_bottom-line.main_top+1) 
        return ((distance_offset),start, "between")
    if dia_center<=line.main_bottom:
        dia_distance=dia_center- dia.top
        distance_offset=0
        start=dia.top-line.main_top
        return ((distance_offset), (start), ("overlap"))
    
    return 0


   

def calculate_top(line, dia):
    dia_center=(dia.top+dia.bottom)/2
    distance_offset=0
    dia_distance=0

    if dia_center<line.main_top:
        dia_distance= dia.bottom - dia_center
        distance_offset=line.main_top-dia.bottom
        start=(0) 
        return ((distance_offset),start, "between")
   
    if dia_center>=line.main_top:
        dia_distance=dia.bottom-dia_center
        distance_offset=0
        start=dia.bottom-line.main_top
        return ((distance_offset), (start), "overlap")
    

    return 0

# def calculate_bottom(dia,line):
#     if dia.top>line.main_bottom:
#         return line.main_bottom-dia.top
#     return 0

# def calculate_top(dia,line):
#     if dia.bottom<line.main_top:
#         return line.main_top-dia.bottom
#     return 0
    

    
def visualize_dia_distance(page_img, dia, column_starts, color=(0, 0, 255)):
    """
    Draws vertical lines from detected black pixel positions up to dia.top for each column.

    Args:
        page_img: np.ndarray (grayscale or BGR)
        dia: object with .top, .bottom, .left, .right attributes
        column_starts: dict {x_column: y_start} for each detected start pixel
        color: BGR color (default red)
    """

    # --- 1) Ensure page image is color ---
    if page_img.dtype.kind == 'f':
        page_uint8 = img_as_ubyte(page_img)
    else:
        page_uint8 = page_img.copy().astype(np.uint8)

    if len(page_uint8.shape) == 2:
        page_bgr = cv2.cvtColor(page_uint8, cv2.COLOR_GRAY2BGR)
    else:
        page_bgr = page_uint8.copy()

    # --- 2) Draw one vertical line per column ---
    for x, y_start in column_starts.items():
        cv2.line(page_bgr, (x, y_start), (x, dia.top), color, thickness=1, lineType=cv2.LINE_AA)
        # Optional: mark the start pixel (where black found)
        cv2.circle(page_bgr, (x, y_start), 2, (0, 255, 0), -1)

    # # --- 3) Draw bounding box for reference ---
    # cv2.rectangle(page_bgr, (dia.left, dia.top), (dia.right, dia.bottom), (255, 255, 0), 1)

    # # --- 4) Resize for display ---
    # scale_percent = 40
    # width = int(page_bgr.shape[1] * scale_percent / 100)
    # height = int(page_bgr.shape[0] * scale_percent / 100)
    # resized = cv2.resize(page_bgr, (width, height), interpolation=cv2.INTER_AREA)

    # # --- 5) Show the image ---
    # cv2.imshow("Diacritic Column Distances", resized)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



# def attach_diacritics_to_lines(lines, diacritics, margin, debug_dir):
#     """
#     Attach each diacritic bounding box to the most likely line.
#     Priority:
#       1. Containment (fully inside line)
#       2. Overlap + pixel distance analysis
#       2.5. Between two lines — pseudo-overlap handling
#       3. Nearest line fallback
#     """
#     # page_img=r"D:\FYP\OCR_Data\1209\1209_Page_12.jpg"
#     # imgHandler = ImageProcessor()
#     # page_img = cv2.imread(page_img, cv2.IMREAD_GRAYSCALE)

#     # imgHandler.gray=page_img

#     # page_iimg = imgHandler.sauvola_binarize()

#     # --- Stable ordering ---
#     diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
#     lines = sorted(lines, key=lambda l: l.ID)

#     log(f"\n===== START DIACRITIC ATTACHMENT =====")
#     log(f"Total diacritics: {len(diacritics)} | Total lines: {len(lines)}")

#     for dia in diacritics:
#         dia_cy = (dia.top + dia.bottom) / 2.0
#         overlaps = []
#         assigned = False
#         only_vertical=[]

#         log(f"\n--- Processing diacritic: {dia.name} ---")
#         log(f"Bounding Box: L={dia.left}, R={dia.right}, T={dia.top}, B={dia.bottom}")

#         # --- Step 1: Containment / Overlap detection ---
#         for line in lines:
#             L, R, T, B = line.main_left, line.main_right, line.main_top, line.main_bottom

#             is_inside = (
#                 dia.left >= L - margin and dia.right <= R + margin and
#                 dia.top >= T - margin and dia.bottom <= B + margin
#             )
#             partial_inside=dia.top >= T - margin and dia.bottom <= B + margin
            
#             horiz_intersect = not (dia.right < L - margin or dia.left > R + margin)
#             vert_intersect  = not (dia.bottom < T - margin or dia.top > B + margin)

#             if is_inside:
#                 log(f"✅ Contained in line ID {line.ID} — attaching directly.")
#                 line.AddDiacritic(dia)
#                 assigned = True
#                 break
#             elif horiz_intersect and vert_intersect:
#                 log(f"⚠️ Overlaps line ID {line.ID} (no full containment).")
#                 overlaps.append(line)
#                 break
#             elif partial_inside:
#                 line.AddDiacritic(dia)
#                 assigned = True
#                 break

#         if assigned:
#             continue

#         # --- Step 2: Overlap classification ---
#         over_lines = {}

#         for line in overlaps:
#             log(f"Processing overlap candidate — Line ID {line.ID}")
#             idx = lines.index(line)
#             prev_line = lines[idx - 1] if idx > 0 else None
#             next_line = lines[idx + 1] if idx + 1 < len(lines) else None

#             if dia.top < line.main_top:
#                 lines_array = [line]
#                 if prev_line:
#                     lines_array.append(prev_line)
#                 over_lines[line.ID] = (lines_array, "above")
#                 log(f"  ↳ Classified as ABOVE line {line.ID}")

#             elif dia.bottom > line.main_bottom:
                
#                 lines_array = [line]
#                 if next_line:
#                     lines_array.append(next_line)
#                 over_lines[line.ID] = (lines_array, "below")
#                 log(f"  ↳ Classified as BELOW line {line.ID}")

#             else:
#                 log(f"  ✅ Vertically overlaps line {line.ID}, attaching immediately.")
#                 line.AddDiacritic(dia)
#                 assigned = True
#                 break

#         if assigned:
#             continue

#         # --- Step 2.5: Handle diacritics between two lines (no overlap) ---
#         if not overlaps:
#             above_line, below_line = None, None
#             min_above_gap, min_below_gap = float("inf"), float("inf")
#             #keep array of lines_bottom and lines_top
           
#             for line in lines:
               
#                 # If line is completely above the diacritic
#                 if line.main_bottom < dia.top:
#                     gap = dia.top - line.main_bottom
#                     if gap < min_above_gap:
#                         above_line = line
#                         min_above_gap = gap

#                 # If line is completely below the diacritic
#                 elif line.main_top > dia.bottom:
#                     gap = line.main_top - dia.bottom
#                     if gap < min_below_gap:
#                         below_line = line
#                         min_below_gap = gap
            

#             if above_line and below_line:
#                 log(f"⚖️ Diacritic {dia.name} lies between line {above_line.ID} and line {below_line.ID}")
#                 over_lines[above_line.ID] = ([above_line, below_line], "between")
#             elif above_line:
#                 log(f"⬆️ Diacritic {dia.name} is just below line {above_line.ID}")
#                 over_lines[above_line.ID] = ([above_line], "below")
#             elif below_line:
#                 log(f"⬇️ Diacritic {dia.name} is just above line {below_line.ID}")
#                 over_lines[below_line.ID] = ([below_line], "above")


#         # --- Step 3: Distance-based best-line selection ---
#         UD_distance, DD_distance = 9999, 9999
#         id_above, id_below = -1, -1

#         if over_lines:
#             log(f"🔍 Evaluating pixel distance for overlap/between region(s):")
#         else:
#             log(f"🔍 No overlaps or neighboring lines detected, skipping pixel-based analysis.")

#         for key, (lines_array, status) in over_lines.items():
#             log(f"  ↳ Processing candidate region — Line ID {key}")
#             log(f"    Classified as {status.upper()} region (len={len(lines_array)})")

#             for i, current_line in enumerate(lines_array):
#                 img = current_line.main_image
#                 line_height = current_line.main_bottom - current_line.main_top + 1
#                 dia_left = max(dia.left, current_line.main_left) - current_line.main_left + 1
#                 dia_right = min(dia.right, current_line.main_right) - current_line.main_left + 1

#                 if dia_left >= img.shape[1] or dia_right < 0:
#                     log(f"    ⚠️ Skipping line {current_line.ID}: diacritic outside image bounds")
#                     continue

                
                
#                 # Setup scan ranges depending on relation
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
#                 elif status == "between":
#                     # For "between", process both lines:
#                     log(f"&&&&&&&&&&&&&&&&&&&between case&&&&&&&&&&&&&&&&&&&")
#                     if i == 0:  # Top line
#                         start = calculate_bottom(current_line, dia)
#                         distance_offset = start
#                         kk_range = range(line_height - 1, -1, -1)
#                     elif i == 1:  # Bottom line
#                         start = calculate_top(current_line, dia)
#                         distance_offset = start
#                         kk_range = range(0, line_height)
#                     else:
#                         continue
#                 else:
#                     continue


#                 log(f"  ▶️ Scanning line ID {current_line.ID} | status={status}, index={i}")
#                 if distance_offset is None:
#                     log(f"    ⚠️ distance_offset is None — setting to 0 for safety (line {current_line.ID})")
#                     distance_offset = 0.0

#                 log(f"     - line_height={line_height}, dia_left={dia_left}, dia_right={dia_right}, offset={distance_offset:.2f}")

#                 for j in range(dia.left, dia.right + 1):
#                     found_pixel = False  # track if we’ve already found one for this column

#                     for kk in kk_range:
                        
#                         if found_pixel:
#                             break  # skip rest of kk loop once pixel found
                        
#                         if 0 <= j < img.shape[1] and img[kk, j] == 0:
                        
#                             # --- Handle "between" case specially ---
#                             if status == "between":
#                                 if i == 0:
#                                     dia_distance = calculate_distance_for_column(dia, j, status="above")
#                                     dist = dia_distance + distance_offset + (line_height - kk - 1)
#                                     visualize_search(
#         line=current_line,
#         dia=dia,
#         line_img=current_line.main_image,
#         column=j - current_line.main_left,   # local column in line image
#         dia_top=dia.top,
#         dia_bottom=kk
#     )                               
#                                     found_pixel = True

#                                 elif i == 1:
#                                     dia_distance = calculate_distance_for_column(dia, j, status="below")
#                                     visualize_search(
#         line=current_line,
#         dia=dia,
#         line_img=current_line.main_image,
#         column=j - current_line.main_left,   # local column in line image
#         dia_top=dia.bottom,
#         dia_bottom=kk
#     )
#                                     found_pixel = True
#                                     dist = dia_distance + distance_offset + kk
#                                 else:
#                                     log(f"[Warning] Unexpected i={i} for status='between'")
#                                     continue
                                
#                             # --- Handle "above" case ---
#                             elif status == "above":
#                                 dia_distance = 0
#                                 if i == 0:
#                                     dia_distance = calculate_distance_for_column(dia, j, status="below")
#                                     visualize_search(
#         line=current_line,
#         dia=dia,
#         line_img=current_line.main_image,
#         column=j - current_line.main_left,   # local column in line image
#         dia_top=dia.bottom,
#         dia_bottom=kk
#     )
#                                     found_pixel = True
#                                 elif i == 1:
#                                     dia_distance = calculate_distance_for_column(dia, j, status="above")
#                                     visualize_search(
#         line=current_line,
#         dia=dia,
#         line_img=current_line.main_image,
#         column=j - current_line.main_left,   # local column in line image
#         dia_top=dia.top,
#         dia_bottom=kk
#     )

#                                 dist = dia_distance + distance_offset + kk
#                                 found_pixel = True

#                             # --- Handle "below" case ---
#                             elif status == "below":
#                                 dia_distance = 0
#                                 if i == 0:
#                                     dia_distance = calculate_distance_for_column(dia, j, "above")
#                                     visualize_search(
#         line=current_line,
#         dia=dia,
#         line_img=current_line.main_image,
#         column=j - current_line.main_left,   # local column in line image
#         dia_top=kk
#         ,
#         dia_bottom=current_line.main_bottom
        
#     )
#                                     found_pixel = True
#                                 elif i == 1:
#                                     dia_distance = calculate_distance_for_column(dia, j, "below")
#                                     visualize_search(
#         line=current_line,
#         dia=dia,
#         line_img=current_line.main_image,
#         column=j - current_line.main_left,   # local column in line image
#         dia_top=current_line.main_top,
#         dia_bottom=kk
#     )

#                                 dist = dia_distance + distance_offset + (line_height - kk - 1)
#                                 found_pixel = True

#                             else:
#                                 log(f"[Warning] Unsupported status '{status}'")
#                                 continue
                            
#                             # --- Visualization ---
                   

#                             log(f"[{status}] Col {j} | kk={kk} | dia_dist={dia_distance} | offset={distance_offset} | dist={dist}")

#                             # ✅ stop scanning this column once first black pixel is processed
#                           # exit kk loop

                           


#                             if status == "above":
#                                 if i == 0 and dist < UD_distance:
#                                     UD_distance, id_above = dist, current_line.ID
#                                 elif i == 1 and dist < DD_distance:
#                                     DD_distance, id_below = dist, current_line.ID
#                             elif status == "below":
#                                 if i == 0 and dist < UD_distance:
#                                     UD_distance, id_above = dist, current_line.ID
#                                 elif i == 1 and dist < DD_distance:
#                                     DD_distance, id_below = dist, current_line.ID
#                             elif status == "between":
#                                 if i == 0 and dist < UD_distance:
#                                     UD_distance, id_above = dist, current_line.ID
#                                 elif i == 1 and dist < DD_distance:
#                                     DD_distance, id_below = dist, current_line.ID

#                 log(f"  🔸 After scan: UD_distance={UD_distance:.2f}, DD_distance={DD_distance:.2f}")
#         cv2.imwrite(r"D:\FYP\Handwritten\Sample_Page_1\debug_visualization.png", page_img)

#         # Choose best based on computed distances
#         best_lineID = -1
#         if UD_distance < DD_distance and UD_distance != 9999:
#             best_lineID = id_above
#             log(f"✅ Closest match ABOVE line ID {best_lineID} (UD_distance={UD_distance:.2f})")
#         elif DD_distance != 9999:
#             best_lineID = id_below
#             log(f"✅ Closest match BELOW line ID {best_lineID} (DD_distance={DD_distance:.2f})")
#         else:
#             log("⚠️ No valid distance found; will use fallback.")

#         if best_lineID != -1:
#             best_line = next((l for l in lines if l.ID == best_lineID), None)
#             if best_line:
#                 best_line.AddDiacritic(dia)
#             continue

#         # --- Step 4: Fallback — nearest line ---
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
#             log(f"  Fallback distance — Line {line.ID}: norm_dist={norm_dist:.3f}")
#             if norm_dist < best_score:
#                 best_score, best_line = norm_dist, line

#         if best_line:
#             log(f"✅ Fallback chosen line ID {best_line.ID} with normalized distance={best_score:.3f}")
#             best_line.AddDiacritic(dia)

#     log(f"\n===== END DIACRITIC ATTACHMENT =====\n")
#     return lines

def attach_diacritics_to_lines(lines, diacritics, margin, debug_dir):
    """
    Attach each diacritic bounding box to the most likely line.
    Priority:
      1. Containment (fully inside line)
      2. Overlap + pixel distance analysis
      2.5. Between two lines — pseudo-overlap handling
      3. Nearest line fallback
    """
    diacritics = sorted(diacritics, key=lambda d: ((d.top + d.bottom) / 2, d.left))
    lines = sorted(lines, key=lambda l: l.ID)

    log(f"\n===== START DIACRITIC ATTACHMENT =====")
    log(f"Total diacritics: {len(diacritics)} | Total lines: {len(lines)}")

    for dia in diacritics:
        dia_cy = (dia.top + dia.bottom) / 2.0
        overlaps = []
        assigned = False

        log(f"\n--- Processing diacritic: {dia.name} ---")
        log(f"Bounding Box: L={dia.left}, R={dia.right}, T={dia.top}, B={dia.bottom}")

        # --- Step 1: Containment / Overlap detection ---
        for line in lines:
            L, R, T, B = line.main_left, line.main_right, line.main_top, line.main_bottom

            is_inside = (
                dia.left >= L - margin and dia.right <= R + margin and
                dia.top >= T - margin and dia.bottom <= B + margin
            )
            partial_inside = dia.top >= T - margin and dia.bottom <= B + margin

            horiz_intersect = not (dia.right < L - margin or dia.left > R + margin)
            vert_intersect  = not (dia.bottom < T - margin or dia.top > B + margin)

            if is_inside:
                log(f"✅ Contained in line ID {line.ID} — attaching directly.")
                line.AddDiacritic(dia)
                assigned = True
                break
            elif horiz_intersect and vert_intersect:
                log(f"⚠️ Overlaps line ID {line.ID} (no full containment).")
                overlaps.append(line)
                break
            elif partial_inside:
                line.AddDiacritic(dia)
                assigned = True
                break

        if assigned:
            continue

        # --- Step 2: Overlap classification ---
        over_lines = {}

        for line in overlaps:
            log(f"Processing overlap candidate — Line ID {line.ID}")
            idx = lines.index(line)
            prev_line = lines[idx - 1] if idx > 0 else None
            next_line = lines[idx + 1] if idx + 1 < len(lines) else None

            if dia.top < line.main_top:
                lines_array = [line]
                if prev_line:
                    lines_array.append(prev_line)
                over_lines[line.ID] = (lines_array, "above")
                log(f"  ↳ Classified as ABOVE line {line.ID}")

            elif dia.bottom > line.main_bottom:
                lines_array = [line]
                if next_line:
                    lines_array.append(next_line)
                over_lines[line.ID] = (lines_array, "below")
                log(f"  ↳ Classified as BELOW line {line.ID}")

            else:

                log(f"  ✅ Vertically overlaps line {line.ID}, attaching immediately.")
                line.AddDiacritic(dia)
                assigned = True
                break

        if assigned:
            continue

        # --- Step 2.5: Handle diacritics between two lines (no overlap) ---
        if not overlaps:
            above_line, below_line = None, None
            min_above_gap, min_below_gap = float("inf"), float("inf")



            for line in lines:
                if line.main_bottom < dia.top:
                    gap = dia.top - line.main_bottom
                    if gap < min_above_gap:
                        above_line = line
                        min_above_gap = gap
                elif line.main_top > dia.bottom:
                    gap = line.main_top - dia.bottom
                    if gap < min_below_gap:
                        below_line = line
                        min_below_gap = gap

            if above_line and below_line:
                log(f"⚖️ Diacritic {dia.name} lies between line {above_line.ID} and line {below_line.ID}")
                over_lines[above_line.ID] = ([above_line, below_line], "between")
            elif above_line:
                log(f"⬆️ Diacritic {dia.name} is just below line {above_line.ID}")
                over_lines[above_line.ID] = ([above_line], "below")
            elif below_line:
                log(f"⬇️ Diacritic {dia.name} is just above line {below_line.ID}")
                over_lines[below_line.ID] = ([below_line], "above")

        # --- Step 3: Distance-based best-line selection ---
        UD_distance, DD_distance = float("inf"), float("inf")
        id_above, id_below = -1, -1

        if over_lines:
            log(f"🔍 Evaluating pixel distance for overlap/between region(s):")
        else:
            log(f"🔍 No overlaps or neighboring lines detected, skipping pixel-based analysis.")

        for key, (lines_array, status) in over_lines.items():
            log(f"  ↳ Processing candidate region — Line ID {key}")
            log(f"    Classified as {status.upper()} region (len={len(lines_array)})")

            for i, current_line in enumerate(lines_array):
                img = current_line.main_image  # expected to be binary/uint8 where 0=black
                line_height = current_line.main_bottom - current_line.main_top + 1

                # Clip diacritic columns to the current line image coordinates
                col_start_global = max(dia.left, current_line.main_left)
                col_end_global   = min(dia.right, current_line.main_right)
                if col_end_global < col_start_global:
                    log(f"    ⚠️ No overlapping columns between diacritic and line {current_line.ID}; skipping")
                    continue
                new_height=0
                # Convert to local (line image) column indices
                local_start = col_start_global - current_line.main_left
                local_end   = col_end_global - current_line.main_left

                # Decide scanning direction and distance offset depending on relation
                if status == "above" and i == 0:
                    # diacritic is above the line => we scan from top->bottom of line image
                    distance_offset,start, within_Status = calculate_top(current_line, dia)

                    kk_range = range(start, line_height)  # from top (0) downward
                    scan_mode = "above_topline"
                    new_height=line_height-start+1
                    log(f"^^^^^^^^^^^^^^^^^^^{distance_offset} {kk_range}  {start}")
                elif status == "above" and i == 1:
                    distance_offset ,start, within_Status= calculate_bottom(current_line, dia)
                    kk_range = range( start,0 ,-1)  # bottom->up
                    scan_mode = "above_prevline"
                    new_height=start+1
                    log(f"^^^^^^^^^^^^^^^^^^^{distance_offset} {kk_range}  {start}")
                elif status == "below" and i == 0:
                    distance_offset ,start, within_Status =calculate_bottom(current_line, dia)
                    kk_range = range(start,0,-1)  # bottom->up
                    scan_mode = "below_bottomline"
                    new_height=start+1
                    log(f"^^^^^^^^^^^^^^^^^^^{distance_offset} {kk_range}  {start} new_height{new_height}")
                elif status == "below" and i == 1:
                    distance_offset ,start, within_Status= calculate_top(current_line, dia)
                    kk_range = range(start, line_height)  # top->down
                    scan_mode = "below_nextline"
                    new_height=line_height-start+1
                    log(f"^^^^^^^^^^^^^^^^^^^{distance_offset} {kk_range}  {start}")
                elif status == "between":
                    # For "between", first entry is the upper line (scan bottom->up),
                    # second entry is the lower line (scan top->down)
                    if i == 0:
                        distance_offset , start,within_Status= calculate_bottom(current_line, dia)
                        kk_range = range(start ,0 ,-1)
                        scan_mode = "between_top"
                        log(f"^^^^^^^^^^^^^^^^^^^{distance_offset} {kk_range}  {start}")
                        new_height=start+1
                    elif i == 1:
                        distance_offset, start,within_Status = calculate_top(current_line, dia)
                        kk_range = range(start,line_height )
                        scan_mode = "between_bottom"
                        log(f"^^^^^^^^^^^^^^^^^^^{distance_offset} {kk_range}  {start}")
                        new_height=line_height-start+1
                    else:
                        continue
                else:
                    log(f"    ⚠️ Unsupported status/index combination: status={status}, i={i}")
                    continue

                log(f"  ▶️ Scanning line ID {current_line.ID} | status={status}, index={i}, local_cols={local_start}-{local_end}, scan_mode={scan_mode}")
                log(f"     - line_height={line_height}, distance_offset={distance_offset}")
                
                # For each column (local coordinates), scan until first black pixel is found
                for local_x in range(local_start, local_end + 1):
                    found_pixel = False
                    # convert back to global column coordinate for distance calculation and viz
                    global_x = local_x + current_line.main_left
 
                    for kk in kk_range:
                        # if kk_range[0]>kk_range[1]:
                        #     new_height=kk_range[0]-kk_range[1]
                        #     log(f"{kk_range[0] }   {kk_range[1]}")
                        # else:
                        #     new_height=kk_range[1]-kk_range[0]
                        # safety bounds check
                        if kk < 0 or kk >= img.shape[0] or local_x < 0 or local_x >= img.shape[1]:
                            
                            continue

                        if img[kk, local_x] == 0:  # black pixel found
                            # compute per-column dia_distance depending on relation
                            if status == "between":
                                if i == 0:
                                    # top line: diacritic is between, we treat as "above" wrt top line
                                    dia_distance = calculate_distance_for_column(dia, global_x, status="above")
                                    # distance: dia_distance + distance_offset + vertical distance from kk to bottom of line
                                    dist = dia_distance + distance_offset + (new_height - kk - 1)
                                   # visualize: top line found pixel at kk in local coords
                                    log(f"{dia_distance} {distance_offset} {(new_height - kk - 1)}")
                                    # visualize_search(
                                    #     line=current_line,
                                    #     dia=dia,
                                    #     line_img=current_line.main_image,
                                    #     column=local_x,
                                    #     dia_top=new_height-1,
                                    #     dia_bottom=kk
                                    # )
                                else:
                                    # bottom line: treat as "below" wrt bottom line
                                    dia_distance = calculate_distance_for_column(dia, global_x, status="below")
                                    dist = dia_distance+distance_offset+ kk
                                    log(f"{dia_distance} {distance_offset} {kk}")
                                    # visualize_search(
                                    #     line=current_line,
                                    #     dia=dia,
                                    #     line_img=current_line.main_image,
                                    #     column=local_x,
                                    #     dia_top=0,
                                    #     dia_bottom=kk
                                    # )
                            elif status == "above":
                                # two cases depending on which of the two lines in lines_array we are processing
                                if i == 0:
                                    # diacritic is above this primary line -> compute distance from dia.bottom to found pixel
                                    dia_distance = calculate_distance_for_column(dia, global_x, status="below")
                                    dist=0
                                    if within_Status=="overlap":
                                        dist = dia_distance +distance_offset + ((kk+current_line.main_top)-(dia.bottom))
                                        log(f"{dia_distance} {distance_offset} kk {((kk+current_line.main_top)-(dia.bottom) )}  dist {dist}")
                                    elif within_Status=="between":
                                        dist=dia_distance+distance_offset+kk
                                        log(f"{dia_distance} {distance_offset} kk {(kk)}  dist {dist}")
                                    
                                    # visualize_search(
                                    #     line=current_line,
                                    #     dia=dia,
                                    #     line_img=current_line.main_image,
                                    #     column=local_x,
                                    #     dia_top=(dia.bottom-current_line.main_top)+1,
                                    #     dia_bottom=kk
                                    # )
                                else:
                                    # second line (previous line) scenario
                                    dia_distance = calculate_distance_for_column(dia, global_x, status="above")
                                    dist=0
                                    if within_Status=="overlap":
                                        dist = dia_distance +distance_offset + ((new_height - kk - 1))
                                        log(f"{dia_distance} {distance_offset} {( new_height - kk - 1 )}  ")
                                    elif within_Status=="between":
                                        dist=dia_distance+distance_offset+(line_height - kk - 1)
                                        log(f"{dia_distance} {distance_offset} {( line_height - kk - 1 )}  ")
                                    
                                    
                                    # visualize_search(
                                    #     line=current_line,
                                    #     dia=dia,
                                    #     line_img=current_line.main_image,
                                    #     column=local_x,
                                    #     dia_top=(dia.top-current_line.main_top)+1,
                                    #     dia_bottom=kk
                                    # )
                            elif status == "below":
                                if i == 0:
                                    dia_distance = calculate_distance_for_column(dia, global_x, "above")
                                    
                                    dist=0
                                    if within_Status=="overlap":
                                        dist = dia_distance +distance_offset + ((new_height - kk - 1))
                                        log(f"{dia_distance} {distance_offset}ooo kk{kk} new_height{new_height}{( new_height - kk - 1 )}  ")
                                    elif within_Status=="between":
                                        dist=dia_distance+distance_offset+(line_height - kk - 1)
                                        log(f"{dia_distance} {distance_offset} {( line_height - kk - 1 )}  ")
                                    
                                    
                                    # visualize_search(
                                    #     line=current_line,
                                    #     dia=dia,
                                    #     line_img=current_line.main_image,
                                    #     column=local_x,
                                    #     dia_top=(dia.top-current_line.main_top)+1,
                                    #     dia_bottom=kk
                                    # )
                                else:
                                    dia_distance = calculate_distance_for_column(dia, global_x, "below")
                                    dist=0
                                    if within_Status=="overlap":
                                        dist = dia_distance +distance_offset + ((kk+current_line.main_top)-(dia.bottom))
                                        log(f"{dia_distance} {distance_offset} kk {((kk+current_line.main_top)-(dia.bottom) )}  dist {dist}")
                                    elif within_Status=="between":
                                        dist=dia_distance+distance_offset+kk
                                        log(f"{dia_distance} {distance_offset} kk {(kk)}  dist {dist}")
                                    
                                    # visualize_search(
                                    #     line=current_line,
                                    #     dia=dia,
                                    #     line_img=current_line.main_image,
                                    #     column=local_x,
                                        
                                    #     dia_top=(dia.bottom-current_line.main_top)+1,
                                    #     dia_bottom=kk
                                    # )
                            else:
                                # fallback
                                dia_distance = 0
                                dist = 0 + distance_offset + kk

                            # update minima depending on whether this black pixel corresponds to "above" side or "below" side
                            # We interpret: i==0 -> candidate for UD (above) distance; i==1 -> candidate for DD (below) distance
                            if i == 0:
                                if dist < UD_distance:
                                    UD_distance, id_above = dist, current_line.ID
                            elif i == 1:
                                if dist < DD_distance:
                                    DD_distance, id_below = dist, current_line.ID

                            log(f"    [col {global_x}] kk={kk} -> dia_dist={dia_distance} dist={dist:.2f} (UD={UD_distance:.2f}, DD={DD_distance:.2f})")
                            found_pixel = True
                            break  # stop scanning this column (we found the first black pixel)

                    # end kk loop for this column
                    # proceed to next column (we purposely do NOT continue scanning same column after first black pixel)

                # finished scanning all columns for this current_line candidate
                log(f"  🔸 After scanning line {current_line.ID}: UD_distance={UD_distance:.2f}, DD_distance={DD_distance:.2f}")

        # Optionally write debug image (you were saving page_img earlier; keep your own debug flow)
        try:
            cv2.imwrite(r"D:\FYP\Handwritten\Sample_Page_1\debug_visualization.png", page_img)
        except Exception as e:
            log(f"Could not write debug image: {e}")

        # Choose best based on computed distances
        best_lineID = -1
        if UD_distance < DD_distance and UD_distance != float("inf"):
            best_lineID = id_above
            log(f"✅ Closest match ABOVE line ID {best_lineID} (UD_distance={UD_distance:.2f})")
        elif DD_distance != float("inf"):
            best_lineID = id_below
            log(f"✅ Closest match BELOW line ID {best_lineID} (DD_distance={DD_distance:.2f})")
        else:
            log("⚠️ No valid distance found; will use fallback.")

        if best_lineID != -1:
            best_line = next((l for l in lines if l.ID == best_lineID), None)
            if best_line:
                best_line.AddDiacritic(dia)
            continue

        # --- Step 4: Fallback — nearest line ---
        best_line, best_score = None, float("inf")
        for line in lines:
            T, B = line.main_top, line.main_bottom
            line_height = max(1, B - T)

            if dia_cy < T:
                dist = T - dia.bottom
            elif dia_cy > B:
                dist = dia.top - B
            else:
                dist = 0

            norm_dist = dist / line_height
            log(f"  Fallback distance — Line {line.ID}: norm_dist={norm_dist:.3f}")
            if norm_dist < best_score:
                best_score, best_line = norm_dist, line

        if best_line:
            log(f"✅ Fallback chosen line ID {best_line.ID} with normalized distance={best_score:.3f}")
            best_line.AddDiacritic(dia)

    log(f"\n===== END DIACRITIC ATTACHMENT =====\n")
    return lines

# def calculate_distance_for_column(dia, column, status="above"):
#     """
#     Calculates the vertical distance to the first black pixel (0) in a column of dia.cc_matrix.
    
#     Args:
#         dia: object with top, bottom, left, right, cc_matrix attributes.
#         column: int, absolute column (x-coordinate) in the page.
#         status: "above" (scan from bottom up) or "below" (scan from top down).

#     Returns:
#         int distance (in pixels), or None if no black pixel found.
#     """
#     diaImg = dia.cc_matrix
#     height, width = diaImg.shape
#     dia_distance = 0  # default: not found

#     # ensure column index is valid
#     if not (dia.left<= column <= dia.right):
#         log(f"Column {column}: out of range ({dia.left}-{dia.right})")
#         return 0

#     local_x = column - dia.left  # convert global column to local x

#     if status == "above":
#         # scan upward (from bottom → top)
#         for i in range(dia.bottom, dia.top - 1, -1):
#             local_y = i - dia.top
#             if 0 <= local_y < height and 0 <= local_x < width:
#                 if diaImg[local_y][local_x] == 0:
#                     dia_distance =  i-dia.top +1 # distance from top to first black pixel
#                     log(f"[Above] Column {column}: black pixel at y={i}, distance={dia_distance}")
#                     return dia_distance

#     elif status == "below":
#         # scan downward (from top → bottom)
#         for i in range(dia.top, dia.bottom+1, + 1):
#             local_y = i - dia.top
#             if 0 <= local_y < height and 0 <= local_x < width:
#                 if diaImg[local_y][local_x] == 0:
#                     dia_distance = dia.bottom-i +1 # distance from bottom to first black pixel
#                     log(f"[Below] Column {column}: black pixel at y={i}, distance={dia_distance}")
#                     return dia_distance

#     # if not found
#     log(f"Column {column}: no black pixel found in '{status}' search")
#     return 0

import cv2
import numpy as np
from skimage import img_as_ubyte

def visualize_search(line, dia, line_img, column, dia_top, dia_bottom, window_name="Vertical Search Debug"):
    """
    Show a temporary vertical scan line at column 'column' within line_img.
    This lets you visualize the scanning progress when searching up/down a column.
    Does NOT modify the original image.
    """
    debug_img = line_img.copy()

    # Ensure color version for colored overlays
    if len(debug_img.shape) == 2:
        debug_img = cv2.cvtColor(debug_img, cv2.COLOR_GRAY2BGR)

    # Clip bounds to valid coordinates
    column = int(np.clip(column, 0, debug_img.shape[1] - 1))
    dia_top = max(0, dia_top)
    dia_bottom = min(debug_img.shape[0] - 1, dia_bottom)

    # Draw a vertical red line (scan line)
    cv2.line(debug_img, (column, dia_top), (column, dia_bottom), (0, 0, 255), 1)

    # Draw diacritic bounding box in green for reference
    cv2.rectangle(debug_img,
                  (dia.left - line.main_left, dia.top - line.main_top),
                  (dia.right - line.main_left, dia.bottom - line.main_top),
                  (0, 255, 0), 1)

    # Optional line bounding box for clarity
    cv2.rectangle(debug_img,
                  (0, 0),
                  (line.main_width - 1, line.main_height - 1),
                  (255, 255, 0), 1)

    # Show the debug view
    cv2.imshow(window_name, debug_img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()  # adjust delay for scan speed

def calculate_distance_for_column(dia, column, status="above"):
    """
    Calculates the vertical distance from the top or bottom of the diacritic region
    to the *last* black pixel (0) found in a given column of dia.cc_matrix.
    
    Args:
        dia: object with top, bottom, left, right, cc_matrix attributes.
        column: int, absolute column (x-coordinate) in the page.
        status: 
            - "above": measure distance from TOP → to the last black pixel found (scanning upward)
            - "below": measure distance from BOTTOM → to the last black pixel found (scanning downward)
    
    Returns:
        int distance (in pixels) from top or bottom to the last black pixel.
        Returns 0 if no black pixel is found.
    """
    diaImg = dia.cc_matrix
    height, width = diaImg.shape
    dia_distance = 0  # default if no black pixel found

    # Ensure column index is within diacritic bounds
    if not (dia.left <= column <= dia.right):
        log(f"Column {column}: out of range ({dia.left}-{dia.right})")
        return 0

    local_x = column - dia.left  # convert to local x (within cc_matrix)

    if status == "above":
        # scan upward (bottom → top) to find the *last* black pixel
        last_black_y = None
        for i in range(dia.bottom, dia.top - 1, -1):
            local_y = i - dia.top
            if 0 <= local_y < height and 0 <= local_x < width:
                if diaImg[local_y][local_x] == 0:
                    last_black_y = i  # keep updating until we reach the last (topmost) black pixel

        if last_black_y is not None:
            dia_distance = last_black_y - dia.top # distance from top
            log(f"[Above-LAST] Column {column}: last black pixel at y={last_black_y}, distance={dia_distance}")
        else:
            log(f"[Above-LAST] Column {column}: no black pixel found")

    elif status == "below":
        # scan downward (top → bottom) to find the *last* black pixel
        last_black_y = None
        for i in range(dia.top, dia.bottom + 1):
            local_y = i - dia.top
            if 0 <= local_y < height and 0 <= local_x < width:
                if diaImg[local_y][local_x] == 0:
                    last_black_y = i  # keep updating until we reach the last (bottommost) black pixel

        if last_black_y is not None:
            dia_distance = dia.bottom - last_black_y   # distance from bottom
            log(f"[Below-LAST] Column {column}: last black pixel at y={last_black_y}, distance={dia_distance}")
        else:
            log(f"[Below-LAST] Column {column}: no black pixel found")

    else:
        log(f"[Error] Unsupported status '{status}'")
        return 0

    return dia_distance



# diacritics_iterative =r"D:\FYP\Data\Books_Data4\1209_book\output\1209_Page_3\debug"
# page_img=r"D:\FYP\Data\Books_Data4\IAP022_book\output\IAP022_Page_71\iterative_merged\IAP022_Page_71_CC578_Top573_Bottom580_Left542_Right550.jpg"
# imgHandler = ImageProcessor()
# page_img = cv2.imread(page_img, cv2.IMREAD_GRAYSCALE)

# imgHandler.gray=page_img

# page_iimg = imgHandler.sauvola_binarize()
# print(page_iimg)


# for cc_img in os.listdir(diacritics_iterative):
#         path = os.path.join(diacritics_iterative, cc_img)
#         if not cc_img.endswith('.jpg'):
#                 continue

#         imgHandler = ImageProcessor()
#         imgHandler.__ReadImage__(path, grayed=True)

#         img = imgHandler.sauvola_binarize()
#         for i in range(img.shape[0]):
#             array=[]
#             for j in range(img.shape[1]):
#                 array.append(img[i][j])
#             print(array)
        

#         name = os.path.splitext(cc_img)[0].split('_')
#         #print("Name",name)
#         labell= int(name[3].replace('CC', ''))
#         top = int(name[4].replace('Top', ''))
#         bottom = int(name[5].replace('Bottom', ''))
#         left = int(name[6].replace('Left', ''))
#         right = int(name[7].replace('Right', ''))
#         height = bottom - top + 1
#         width = right - left + 1

#         matrix = np.full((height, width), 255, dtype=np.uint16)
#         print(height,' ',width)
#         for h in range(height):
#             for w in range(width):
#               #  if cc_img=='dua_Page_5_CC1026_Top1073_Bottom1083_Left329_Right337.jpg':
#                 #  print(h,w, ' ', img[h][w])
#                 matrix[h][w] = img[h][w]

#         class CCObj:
#             pass
#         CC = CCObj()
#         CC.top, CC.bottom, CC.left, CC.right = top, bottom, left, right
#         CC.img = cc_img
#         CC.labels= labell
#         CC.name= os.path.splitext(cc_img)[0]
#         CC.height, CC.width = height, width
#         CC.cc_matrix = matrix
#         for i in range(CC.left, CC.right,1):
#             calculate_distance_for_column(CC, i, "below")
        
