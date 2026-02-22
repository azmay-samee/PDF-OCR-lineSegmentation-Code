# import cv2
# import numpy as np
# import os

# # folder_path = r"D:\FYP\Data\Books_Data\1209_book\output\1209_Page_11\diacritics"
# # output_dir  = r"D:\FYP\Data\Books_Data\1209_book\output\1209_Page_11\iterative_merged"

# # os.makedirs(output_dir, exist_ok=True)

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
# def parse_box(filename):
#     """Extract bounding box from filename"""
#     name = os.path.splitext(filename)[0].split('_')
#     label  = int(name[3].replace('CC', ''))
#     top    = int(name[4].replace('Top', ''))
#     bottom = int(name[5].replace('Bottom', ''))
#     left   = int(name[6].replace('Left', ''))
#     right  = int(name[7].replace('Right', ''))
#     return name, label, top, left, bottom, right, filename


# # def merge(files,min_dist):   
# #     merged=[]
    
# #     for i in range(len(files)):
# #         name, label, top, left, bottom, right, file1 = parse_box(files[i])
# #         width = right - left + 1
# #         central_point = left + width // 2
# #         if file1=='1209_Page_10_CC321_Top445_Bottom452_Left1150_Right1165.jpg':

# #             print(central_point)
# #         j=i+1
# #         while j < len(files):
# #             name2, label2, top2, left2, bottom2, right2, file2 = parse_box(files[j])
# #             width2 = right2 - left2 + 1
# #             central_point2 = left2 + width2 // 2
# #             if file1=='1209_Page_10_CC321_Top445_Bottom452_Left1150_Right1165.jpg':

# #                 print(central_point)
                
# #             # Check horizontal alignment (with tolerance)
# #             if abs(central_point - central_point2) <= 2:
# #                 vertical_gap = top2 - bottom
# #                 if file1=='1209_Page_10_CC321_Top445_Bottom452_Left1150_Right1165.jpg':

# #                     print(vertical_gap)
# #                     break
# #                 if vertical_gap <= min_dist:
# #                     # Merge into bigger box
# #                     new_top    = min(top, top2)
# #                     new_left   = min(left, left2)
# #                     new_bottom = max(bottom, bottom2)
# #                     new_right  = max(right, right2)
# #                     #merged_name=f"1209_Page_10_CC{label}_Top{new_top}_Bottom{new_bottom}_Left{new_left}_Right{new_right}.jpg"
# #                     # Keep list of member files

# #                     merged.append((name, label, new_top, new_left, new_bottom, new_right, [file1, file2]))
# #                     files.remove(file1)
# #                     files.remove(file2)
# #                     j+=1
# #     return merged

# def merge(files, min_dist):
#     merged = []
#     used = set()

#     for i in range(len(files)):
#         if files[i] in used:
#             continue
#         name, label, top, left, bottom, right, file1 = parse_box(files[i])
#         width = right - left + 1
#         height=bottom-top+1
#         central_point = left + width // 2

#         j = i + 1
#         while j < len(files):
#             if files[j] in used:
#                 j += 1
#                 continue
#             name2, label2, top2, left2, bottom2, right2, file2 = parse_box(files[j])
#             width2 = right2 - left2 + 1
#             central_point2 = left2 + width2 // 2
#             height2= bottom2- left2 +1


#             # Check horizontal alignment
#             if abs(central_point - central_point2) <= 2 and abs(height2-height)<=2:
#                 vertical_gap = top2 - bottom
#                 if vertical_gap <= min_dist:
#                     # Merge
#                     new_top    = min(top, top2)
#                     new_left   = min(left, left2)
#                     new_bottom = max(bottom, bottom2)
#                     new_right  = max(right, right2)

#                     merged.append((name, label, new_top, new_left, new_bottom, new_right, [file1, file2]))
#                     used.add(files[i])
#                     used.add(files[j])
#                     break  # stop looking further for this base box
#             j += 1
#     return merged,used

# def _save_component(name, img_label, top, left, bottom, right, members, folder_path, output_dir, page_name):
#     """Save merged diacritics"""
#     width = right - left + 1
#     height = bottom - top + 1
#     cc_matrix = np.full((height, width), 255, dtype=np.uint8)

#     for file in members:
#         path = os.path.join(folder_path, file)
#         small_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#         if small_img is None:
#             continue
#         _, _, t, l, b, r, _ = parse_box(file)
#         y_offset = t - top
#         x_offset = l - left
#         h, w = small_img.shape
#         cc_matrix[y_offset:y_offset+h, x_offset:x_offset+w] = cv2.bitwise_and(
#             cc_matrix[y_offset:y_offset+h, x_offset:x_offset+w],
#             small_img
#         )

#     nameImg = f"{page_name}_CC{img_label}_Top{top}_Bottom{bottom}_Left{left}_Right{right}.jpg"
#     cv2.imwrite(os.path.join(output_dir, nameImg), cc_matrix)
# def save_unmerged(files, used, folder_path, output_dir):
#     """Save diacritics that were not merged"""
#     for file in files:
#         if file not in used:
#             path = os.path.join(folder_path, file)
#             img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#             if img is not None:
#                 cv2.imwrite(os.path.join(output_dir, file), img)
# def merge_iterative(folder_path, output_dir, page_name, min_dist=2):
#     """
#     Complete iterative merging pipeline.
#     - Sort diacritics by Top & Right
#     - Merge vertically close CCs
#     - Save merged and unmerged images
#     """
#     os.makedirs(output_dir, exist_ok=True)
#     CC_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

#     # --- Sort by Top, then by Right descending ---
#     CC_files = bubblesort(CC_files, 0, len(CC_files), 4, 'ascen')
#     i = 0
#     while i < len(CC_files):
#         name_i = os.path.splitext(CC_files[i])[0].split('_')
#         top_val = int(name_i[4].replace('Top', ''))
#         start = i
#         end = i
#         for j in range(i + 1, len(CC_files)):
#             name_j = os.path.splitext(CC_files[j])[0].split('_')
#             top_val_j = int(name_j[4].replace('Top', ''))
#             if top_val_j == top_val:
#                 end = j
#             else:
#                 break
#         if end > start:
#             CC_files = bubblesort(CC_files, start, end + 1, 7, 'desc')
#         i = end + 1

#     print(f"Total CCs: {len(CC_files)}")
#     merge_files, used = merge(CC_files, min_dist)
#     print(f"Merged groups found: {len(merge_files)}")

#     for (name, label, top, left, bottom, right, members) in merge_files:
#         _save_component(name, label, top, left, bottom, right, members, folder_path, output_dir, page_name)

#     save_unmerged(CC_files, used, folder_path, output_dir)
#     print(f"✅ Merging completed. Output saved to: {output_dir}")


import cv2
import numpy as np
import os

# folder_path = r"D:\FYP\Data\Books_Data\1209_book\output\1209_Page_11\diacritics"
# output_dir  = r"D:\FYP\Data\Books_Data\1209_book\output\1209_Page_11\iterative_merged"

# os.makedirs(output_dir, exist_ok=True)

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
def parse_box(filename):
    """Extract bounding box from filename"""
    name = os.path.splitext(filename)[0].split('_')
    label  = int(name[3].replace('CC', ''))
    top    = int(name[4].replace('Top', ''))
    bottom = int(name[5].replace('Bottom', ''))
    left   = int(name[6].replace('Left', ''))
    right  = int(name[7].replace('Right', ''))
    return name, label, top, left, bottom, right, filename


# def merge(files,min_dist):   
#     merged=[]
    
#     for i in range(len(files)):
#         name, label, top, left, bottom, right, file1 = parse_box(files[i])
#         width = right - left + 1
#         central_point = left + width // 2
#         if file1=='1209_Page_10_CC321_Top445_Bottom452_Left1150_Right1165.jpg':

#             print(central_point)
#         j=i+1
#         while j < len(files):
#             name2, label2, top2, left2, bottom2, right2, file2 = parse_box(files[j])
#             width2 = right2 - left2 + 1
#             central_point2 = left2 + width2 // 2
#             if file1=='1209_Page_10_CC321_Top445_Bottom452_Left1150_Right1165.jpg':

#                 print(central_point)
                
#             # Check horizontal alignment (with tolerance)
#             if abs(central_point - central_point2) <= 2:
#                 vertical_gap = top2 - bottom
#                 if file1=='1209_Page_10_CC321_Top445_Bottom452_Left1150_Right1165.jpg':

#                     print(vertical_gap)
#                     break
#                 if vertical_gap <= min_dist:
#                     # Merge into bigger box
#                     new_top    = min(top, top2)
#                     new_left   = min(left, left2)
#                     new_bottom = max(bottom, bottom2)
#                     new_right  = max(right, right2)
#                     #merged_name=f"1209_Page_10_CC{label}_Top{new_top}_Bottom{new_bottom}_Left{new_left}_Right{new_right}.jpg"
#                     # Keep list of member files

#                     merged.append((name, label, new_top, new_left, new_bottom, new_right, [file1, file2]))
#                     files.remove(file1)
#                     files.remove(file2)
#                     j+=1
#     return merged
def merge(files, min_dist):
    merged = []
    used = set()

    for i in range(len(files)):
        if files[i] in used:
            continue

        # Parse the base component
        name, label, top, left, bottom, right, file1 = parse_box(files[i])
        height = bottom - top + 1
        width = right - left + 1
        central_point = left + width // 2

        group_members = [file1]
        group_changed = True

        while group_changed:
            group_changed = False
            for j in range(len(files)):
                if files[j] in used or files[j] in group_members:
                    continue

                name2, label2, top2, left2, bottom2, right2, file2 = parse_box(files[j])
                height2 = bottom2 - top2 + 1
                width2 = right2 - left2 + 1
                central_point2 = left2 + width2 // 2

                # ✅ Same height or very close (±2 pixels)
                if abs(height2 - height) <= 2:
                    # ✅ Reasonable horizontal alignment (avoid side merging)
                    if abs(central_point - central_point2) <= width:
                        # ✅ Close vertically (stacked)
                        vertical_gap = top2 - bottom
                        if -1 <= vertical_gap <= min_dist:
                            # Merge into one bounding box
                            new_top = min(top, top2)
                            new_left = min(left, left2)
                            new_bottom = max(bottom, bottom2)
                            new_right = max(right, right2)

                            # Update group bounding box
                            top, left, bottom, right = new_top, new_left, new_bottom, new_right
                            group_members.append(file2)
                            used.add(file2)
                            group_changed = True

        merged.append((name, label, top, left, bottom, right, group_members))
        for f in group_members:
            used.add(f)

    return merged, used


def _save_component(name, img_label, top, left, bottom, right, members, folder_path, output_dir, page_name):
    """Save merged diacritics"""
    width = right - left + 1
    height = bottom - top + 1
    cc_matrix = np.full((height, width), 255, dtype=np.uint8)

    for file in members:
        path = os.path.join(folder_path, file)
        small_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if small_img is None:
            continue
        _, _, t, l, b, r, _ = parse_box(file)
        y_offset = t - top
        x_offset = l - left
        h, w = small_img.shape
        cc_matrix[y_offset:y_offset+h, x_offset:x_offset+w] = cv2.bitwise_and(
            cc_matrix[y_offset:y_offset+h, x_offset:x_offset+w],
            small_img
        )

    nameImg = f"{page_name}_CC{img_label}_Top{top}_Bottom{bottom}_Left{left}_Right{right}.jpg"
    cv2.imwrite(os.path.join(output_dir, nameImg), cc_matrix)
def save_unmerged(files, used, folder_path, output_dir):
    """Save diacritics that were not merged"""
    for file in files:
        if file not in used:
            path = os.path.join(folder_path, file)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                cv2.imwrite(os.path.join(output_dir, file), img)
def merge_iterative(folder_path, output_dir, page_name, min_dist=2):
    """
    Complete iterative merging pipeline.
    - Sort diacritics by Top & Right
    - Merge vertically close CCs
    - Save merged and unmerged images
    """
    os.makedirs(output_dir, exist_ok=True)
    CC_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

    # --- Sort by Top, then by Right descending ---
    CC_files = bubblesort(CC_files, 0, len(CC_files), 4, 'ascen')
    i = 0
    while i < len(CC_files):
        name_i = os.path.splitext(CC_files[i])[0].split('_')
        top_val = int(name_i[4].replace('Top', ''))
        start = i
        end = i
        for j in range(i + 1, len(CC_files)):
            name_j = os.path.splitext(CC_files[j])[0].split('_')
            top_val_j = int(name_j[4].replace('Top', ''))
            if top_val_j == top_val:
                end = j
            else:
                break
        if end > start:
            CC_files = bubblesort(CC_files, start, end + 1, 7, 'desc')
        i = end + 1

    print(f"Total CCs: {len(CC_files)}")
    merge_files, used = merge(CC_files, min_dist)
    print(f"Merged groups found: {len(merge_files)}")

    for (name, label, top, left, bottom, right, members) in merge_files:
        _save_component(name, label, top, left, bottom, right, members, folder_path, output_dir, page_name)

    save_unmerged(CC_files, used, folder_path, output_dir)
    print(f"✅ Merging completed. Output saved to: {output_dir}")