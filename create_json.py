# import json
# import os

# def export_lines_to_json(pages_lines, output_path):
#     """
#     pages_lines : dict
#         {
#             "page_1": [line1, line2, ...],
#             "page_2": [line3, line4, ...]
#         }
#         Each line must have:
#             line.ID
#             line.line_cc -> list of CC objects with top, bottom, left, right
#     """

#     export_data = {}

#     for page_name, lines in pages_lines.items():
#         page_lines = {}

#         for line in lines:
#             # Each line will have its ID as key (e.g., "line_1")
#             line_key = f"line_{line.ID}"
#             line_dict = {"Total_CCs": len(line.line_cc),
#             "CC_labels":{}}

#             # Enumerate CCs for that line
#             for idx, cc in enumerate(line.line_cc, start=1):
#                 cc_key = f"CC{cc.labels}"
#                 line_dict["CC_labels"][cc_key] = {
#                     "top": cc.top,
#                     "bottom": cc.bottom,
#                     "left": cc.left,
#                     "right": cc.right
#                 }

#             page_lines[line_key] = line_dict

#         export_data[page_name] = page_lines

#     # Write JSON file
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(export_data, f, ensure_ascii=False, indent=4)

#     print(f"✅ JSON file saved at: {output_path}")


import json
import os

def export_lines_to_json(pages_lines, output_path):
    """
    Export line and CC info for each page into a JSON file.
    Handles empty pages gracefully.
    """
    # Load existing JSON if it exists
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            export_data = json.load(f)
    else:
        export_data = {}

    for page_name, lines in pages_lines.items():
        # If the page has no lines, add an empty record
        if not lines or len(lines) == 0:
            export_data[page_name] = {
                "Total_CCs": 0,
                "CC_labels": {}
            }
            continue

        # Otherwise, process lines as usual
        page_lines = {}
        total_ccs = 0

        for line in lines:
            line_key = f"line_{line.ID}"
            line_dict = {
                "Total_CCs": len(line.line_cc),
                "CC_labels": {}
            }

            for cc in line.line_cc:
                cc_key = f"CC{cc.labels}"
                line_dict["CC_labels"][cc_key] = {
                    "top": cc.top,
                    "bottom": cc.bottom,
                    "left": cc.left,
                    "right": cc.right
                }

            page_lines[line_key] = line_dict
            total_ccs += len(line.line_cc)

        export_data[page_name] = {
            "Total_CCs": total_ccs,
            "Lines": page_lines
        }

    # Save JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON file updated at: {output_path}")
