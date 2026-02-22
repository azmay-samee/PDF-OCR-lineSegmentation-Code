import os
from image_processor import ImageProcessor
from connected_components import ConnectedComponentLabeler
from line import Line
from utils import bubblesort

from utils import merge_close_lines
#from diacritics_Attachment import attach_diacritics_to_lines
# from jackel import attach_diacritics_to_lines, estimate_baseline, visualize_baseline
from my_logic import merge_iterative
from create_json import export_lines_to_json
import numpy as np
from annie2 import attach_diacritics_to_lines
import cv2


book_page=r"D:\FYP\OCR_Data\IAP022\copy"
for page in os.listdir(book_page):
    
    import time
    from concurrent.futures import ThreadPoolExecutor

    start_time = time.time()
    img_path = os.path.join(book_page, page)
    print(img_path)
    page_name=os.path.splitext(page)[0]

    print(f"\n🔹 Processing page: {page_name}", flush=True)

    output_dir = os.path.join(r"D:\FYP\OCR_Data\IAP022\copy\output", os.path.splitext(page)[0])
    line_output_dir = os.path.join(r"D:\FYP\OCR_Data\IAP022\copy\line_output", os.path.splitext(page)[0])
    in_dir=os.path.join(r"D:\FYP\OCR_Data\IAP022\copy\input", os.path.splitext(page)[0])
    diacritics_folder =os.path.join(output_dir, "diacritics")
    diacritics_iterative=os.path.join(output_dir, "iterative_merged")
    #diacritics_iterative=r"D:\FYP\Data\Books_Data4\1378_book\output\1378_Page_117\iterative_merged"
    debug_dir = os.path.join(r"D:\FYP\OCR_Data\IAP022\copy\debug", os.path.splitext(page)[0])
    json_path=r"D:\FYP\OCR_Data\IAP022\copy\lines_info.json"
    lineDia_output_dir = os.path.join(r"D:\FYP\OCR_Data\IAP022\copy\line_outputDia2", os.path.splitext(page)[0])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(line_output_dir):
        os.makedirs(line_output_dir)

    if not os.path.exists(lineDia_output_dir):
        os.makedirs(lineDia_output_dir)
    if not os.path.exists(in_dir):
        os.makedirs(in_dir)
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)
    if not os.path.exists(diacritics_iterative):
        os.makedirs(diacritics_iterative)

    Processor = ImageProcessor()
    Processor.__ReadImage__(img_path, grayed=False)
    grayImg = Processor.to_grayscale()
    Processor.writeImg(in_dir, 'gray.jpg', grayImg)
    binary = Processor.sauvola_binarize()

    Processor.writeImg(in_dir, 'binary.jpg', binary)
    CC = ConnectedComponentLabeler(ImageProcessor, page, binary)
    CC.extract_components(output_dir)

    jpg_files = [
        f for f in os.listdir(output_dir)
        if f.lower().endswith(('.jpg', '.jpeg')) and os.path.isfile(os.path.join(output_dir, f))
    ]

    if not jpg_files:
        print("No JPG/JPEG files found.")
        # Add empty page entry to JSON and skip further processing for this page
        export_lines_to_json({page_name: []}, json_path)
        print(f"⚠️ Added empty page entry for {page_name} to JSON.")
        continue
    else:
        print(f"Found {len(jpg_files)} JPG/JPEG files:")
        for f in jpg_files:
            print(" -", f)

# If we reach here, components exist → run separation
    CC.separation(output_dir)

    

    output_dir=os.path.join(output_dir, "main_body")
    print(output_dir)
# Line grouping
    jpgFiles = os.listdir(output_dir)
    if len(jpgFiles) == 0:
        print("No .jpg files found in output directory.")

        continue
    print(len(jpgFiles), " files found in output directory.")
    CC_files = [f for f in os.listdir(output_dir) if f.endswith('.jpg')]
    CC_files = bubblesort(CC_files, 0, len(CC_files), 4, 'ascen')
    for j in CC_files:
        print(j)
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

    # Sort this Top-group by Right descending
        if end > start:
            CC_files = bubblesort(CC_files, start, end + 1, 5, 'desc')
    
        i = end + 1  # Jump to the next segment

    for i in CC_files:
        print(i)
    
    merge_iterative(diacritics_folder, diacritics_iterative, page_name, min_dist=2)
# Line formation
    lines_array = []
    print("complete sorting")
    k=0
    for cc_img in CC_files:
    #print("index ",k)
        path = os.path.join(output_dir, cc_img)
        if not cc_img.endswith('.jpg'):
            continue

        imgHandler = ImageProcessor()
        imgHandler.__ReadImage__(path, grayed=True)
        img = imgHandler.sauvola_binarize()

        name = os.path.splitext(cc_img)[0].split('_')
        #print("Name", name)
        labelID=int(name[3].replace('CC', ''))
        top = int(name[4].replace('Top', ''))
        bottom = int(name[5].replace('Bottom', ''))
        left = int(name[6].replace('Left', ''))
        right = int(name[7].replace('Right', ''))

        height = bottom - top + 1
        width = right - left + 1

        matrix = np.full((height, width), 255, dtype=np.uint16)

        for h in range(height):
            for w in range(width):
                #print(h,' ',w)
                matrix[h][w] = img[h][w]

        # mock ConnectedComponent
        class CCObj:
            pass
        CC = CCObj()
        CC.top, CC.bottom, CC.left, CC.right = top, bottom, left, right
        CC.height, CC.width = height, width
        CC.name = os.path.splitext(cc_img)[0]

        CC.labels=labelID

    
        CC.cc_matrix = matrix
        mainImg = imgHandler.gray

        if mainImg is None:
            raise ValueError(f"{CC.name}: imgHandler.original is None")

    # Convert to numpy if needed
        if not isinstance(mainImg, np.ndarray):
            mainImg = np.array(mainImg)

    # Convert to grayscale if RGB
        if mainImg.ndim == 3:
            mainImg = cv2.cvtColor(mainImg, cv2.COLOR_BGR2GRAY)

    # Ensure dtype is uint8
        if mainImg.dtype != np.uint8:
            mainImg = mainImg.astype(np.uint8)

    # Assign the safe image
        CC.mainImg = mainImg

        added = False
        for line in lines_array:
            if line.check_Component(CC):
                line.AddMain(CC)
                added = True
                break

        if not added:
            new_line = Line(ImageProcessor)
            new_line.AddMain(CC)
            new_line.ID = len(lines_array)
            # if len(lines_array) > 8:
            #      break
            lines_array.append(new_line)
        k+=1
    print(f"{len(lines_array)} lines found before merging.")
    lines_array=merge_close_lines(lines_array, gap_threshold=0, overlap_threshold=0.2)
    print(f"{len(lines_array)} lines formed.")
#     for i in range(len(lines_array)):
#         print(f"Line {lines_array[i].ID}: {len(lines_array[i].main_cc)} components.")
    
# # # list of line objects where {top, bottom, left, right , ccs}

# # #lines_array=
   
    diacritics=[]

    for cc_img in os.listdir(diacritics_iterative):
        path = os.path.join(diacritics_iterative   , cc_img)
        if not cc_img.endswith('.jpg'):
                continue

        imgHandler = ImageProcessor()
        imgHandler.__ReadImage__(path, grayed=True)

        img = imgHandler.sauvola_binarize()
    

        name = os.path.splitext(cc_img)[0].split('_')
        #print("Name",name)
        labell= int(name[3].replace('CC', ''))
        top = int(name[4].replace('Top', ''))
        bottom = int(name[5].replace('Bottom', ''))
        left = int(name[6].replace('Left', ''))
        right = int(name[7].replace('Right', ''))
        height = bottom - top + 1
        width = right - left + 1

        matrix = np.full((height, width), 255, dtype=np.uint16)
        print(height,' ',width)
        for h in range(height):
            for w in range(width):
              #  if cc_img=='dua_Page_5_CC1026_Top1073_Bottom1083_Left329_Right337.jpg':
                #  print(h,w, ' ', img[h][w])
                matrix[h][w] = img[h][w]

        class CCObj:
            pass
        CC = CCObj()
        CC.top, CC.bottom, CC.left, CC.right = top, bottom, left, right
        CC.img = cc_img
        CC.labels= labell
        CC.name= os.path.splitext(cc_img)[0]
        CC.height, CC.width = height, width
        CC.cc_matrix = matrix
        diacritics.append(CC)
       
    print(len(diacritics))

# #     Save line images
    for     idx, line in enumerate(lines_array):
        line.main_height = line.main_bottom - line.main_top + 1
        line.main_width = line.main_right - line.main_left + 1
        line.main_image = np.full((line.main_height, line.main_width), 255, dtype=np.uint8)

        for CC in line.main_cc:
            for i in range(CC.height):
                for j in range(CC.width):

                    if CC.cc_matrix[i][j] == 0:


                        x = i + CC.top - line.main_top
                        y = j + CC.left - line.main_left

                        line.main_image[x][y] = 0

        line_name = f'line_{idx }_Top{line.main_top}_Bottom{line.main_bottom}_Left{line.main_left}_Right{line.main_right}.jpg'

        ImageProcessor().writeImg(line_output_dir, line_name, line.main_image)

    print("Line segmentation complete.")
  
    # for line in lines_array:
    #     line.baseline,line.pts = estimate_baseline(line, method="poly")  
    #     visualize_baseline( line, line.baseline, line.pts, save_path=r"D:\FYP\Data\line_segmentation\connected_components\IAP022_Page_3\show") 
    # visualize_baseline( line, line.baseline, line.pts, save_path=r"D:\FYP\Handwritten\Sample_Page_1\show") 
    
    lines_array=attach_diacritics_to_lines(lines_array, diacritics, margin=0, debug_dir=debug_dir)
    
    export_lines_to_json(
    {f"{page_name}": lines_array},
    json_path
)



# # Save line images
    for idx, line in enumerate(lines_array):
        line.full_height = line.full_bottom - line.full_top + 1
        line.full_width = line.full_right - line.full_left + 1
        line.line_img = np.full((line.full_height, line.full_width), 255, dtype=np.uint8)

        for CC in line.line_cc:
            for i in range(CC.height):
                for j in range(CC.width):
                    if CC.cc_matrix[i][j] == 0:
                        x = i + CC.top - line.full_top
                        y = j + CC.left - line.full_left
                        line.line_img[x][y] = 0

        line_name = f'line_{idx }_Top{line.full_top}_Bottom{line.full_bottom}_Left{line.full_left}_Right{line.full_right}.jpg'
        ImageProcessor().writeImg(lineDia_output_dir, line_name, line.line_img)

    print("Line segmentation complete.")

    elapsed = time.time() - start_time
    print(f"⏱️ Finished processing {page_name} in {elapsed:.2f} seconds.", flush=True)

