# # # import os
# # # import json

# # # # === Paths ===
# # # full_json_path = r"D:\FYP\Data\line_segmentation\connected_components2\1209_Page_10\lines_info.json"
# # # correct_json_path = r"D:\FYP\Data\line_segmentation\connected_components2\1209_Page_10\correctLines_GT.json"
# # # output_report = r"D:\FYP\Data\line_segmentation\connected_components2\1209_Page_10\incorrect_lines_report.json"

# # # # === Step 1: Load both JSONs ===
# # # with open(full_json_path, "r", encoding="utf-8") as f:
# # #     full_gt = json.load(f)

# # # with open(correct_json_path, "r", encoding="utf-8") as f:
# # #     correct_gt = json.load(f)

# # # # === Step 2: Extract page key ===
# # # page_key = list(full_gt.keys())[0]
# # # full_page = full_gt[page_key]
# # # correct_page = correct_gt.get(page_key, {})

# # # # === Step 3: Comparison ===
# # # correct_lines = []
# # # incorrect_lines = []

# # # for line_key, full_line_data in full_page.items():
# # #     correct_line_data = correct_page.get(line_key)

# # #     if not correct_line_data:
# # #         incorrect_lines.append({
# # #             "line_id": line_key,
# # #             "reason": "Missing in correctLines_GT.json"
# # #         })
# # #         continue

# # #     # ✅ Condition 1: same CC labels
# # #     full_labels = set(full_line_data.keys())
# # #     correct_labels = set(correct_line_data.keys())

# # #     if full_labels != correct_labels:
# # #         incorrect_lines.append({
# # #             "line_id": line_key,
# # #             "reason": f"Different CC labels (full={sorted(full_labels)}, correct={sorted(correct_labels)})"
# # #         })
# # #         continue

# # #     # ✅ Condition 2: Compare TBLR for each CC
# # #     label_mismatch = False
# # #     for cc_label in full_labels:
# # #         full_cc = full_line_data[cc_label]
# # #         correct_cc = correct_line_data[cc_label]

# # #         for key in ["top", "bottom", "left", "right"]:
# # #             if full_cc[key] != correct_cc[key]:
# # #                 label_mismatch = True
# # #                 break

# # #         if label_mismatch:
# # #             break

# # #     if label_mismatch:
# # #         incorrect_lines.append({
# # #             "line_id": line_key,
# # #             "reason": "TBLR mismatch in one or more CCs"
# # #         })
# # #     else:
# # #         correct_lines.append(line_key)

# # # # === Step 4: Summary ===
# # # print("✅ Comparison complete.")
# # # print(f"✔️ Correct lines: {len(correct_lines)}")
# # # print(f"❌ Incorrect lines: {len(incorrect_lines)}")

# # # if incorrect_lines:
# # #     print("\nIncorrect Line Details:")
# # #     for entry in incorrect_lines:
# # #         print(f" - {entry['line_id']}: {entry['reason']}")

# # # # === Step 5: Save report ===
# # # report = {
# # #     "total_lines": len(full_page),
# # #     "correct_lines": correct_lines,
# # #     "incorrect_lines": incorrect_lines,
# # #     "accuracy_percent": round((len(correct_lines) / len(full_page)) * 100, 2)
# # # }

# # # with open(output_report, "w", encoding="utf-8") as f:
# # #     json.dump(report, f, ensure_ascii=False, indent=4)

# # # print(f"\n🧾 Detailed report saved at: {output_report}")

# # import os
# # import json
# # import pandas as pd

# # # === PATHS ===
# # book_root = r"D:\FYP\Data\Books_Data\1209_book"
# # lines_info2_path = os.path.join(book_root, "lines_info2.json")  # Reference GT
# # correct_json_path = os.path.join(book_root, "correctlines_GT2", "correctLines_GT2.json")  # Predicted GT
# # line_output_root = os.path.join(book_root, "line_output")  # For counting total JPGs
# # report_path = os.path.join(book_root, "report2.xlsx")

# # # === Load JSON files ===
# # print("📖 Loading lines_info.json ...")
# # with open(lines_info2_path, "r", encoding="utf-8") as f:
# #     lines_info2 = json.load(f)

# # print("📖 Loading correctLines_GT.json ...")
# # with open(correct_json_path, "r", encoding="utf-8") as f:
# #     correct_lines_json = json.load(f)

# # # === Initialize report data ===
# # report_rows = []

# # # === Iterate through each page in lines_info2.json ===
# # for page_name, page_lines in lines_info2.items():
# #     correct_page = correct_lines_json.get(page_name, {})

# #     # Count total jpgs from line_output/<page_name>
# #     page_folder = os.path.join(line_output_root, page_name)
# #     total_lines = len([f for f in os.listdir(page_folder) if f.lower().endswith(".jpg")]) if os.path.exists(page_folder) else len(page_lines)

# #     correct_count = 0
# #     incorrect_count = 0
# #     incorrect_ids = []
# #     reasons = []

# #     for line_key, gt_line_data in page_lines.items():
# #         # Step 1: check if line exists in correctLines_GT
# #         if line_key not in correct_page:
# #             incorrect_count += 1
# #             incorrect_ids.append(line_key)
# #             reasons.append("Missing line in correctLines_GT")
# #             continue

# #         pred_line_data = correct_page[line_key]

# #         # Step 2: check CC label sets
# #         gt_labels = set(gt_line_data.keys())
# #         pred_labels = set(pred_line_data.keys())

# #         if gt_labels != pred_labels:
# #             incorrect_count += 1
# #             incorrect_ids.append(line_key)
# #             reasons.append(f"CC label mismatch: GT={sorted(gt_labels)} vs Pred={sorted(pred_labels)}")
# #             continue

# #         # Step 3: check TBLR values
# #         tblr_mismatch = []
# #         for cc_label in gt_labels:
# #             gt_cc = gt_line_data[cc_label]
# #             pred_cc = pred_line_data[cc_label]
# #             for key in ["top", "bottom", "left", "right"]:
# #                 if gt_cc.get(key) != pred_cc.get(key):
# #                     tblr_mismatch.append(f"{cc_label}.{key}")
# #         if tblr_mismatch:
# #             incorrect_count += 1
# #             incorrect_ids.append(line_key)
# #             reasons.append("TBLR mismatch in: " + ", ".join(tblr_mismatch))
# #         else:
# #             correct_count += 1

# #     # Compute metrics
# #     accuracy = round((correct_count / total_lines) * 100, 2) if total_lines > 0 else 0.0

# #     report_rows.append({
# #         "page_name": page_name,
# #         "total_lines": total_lines,
# #         "correct_lines": correct_count,
# #         "incorrect_lines": incorrect_count,
# #         "incorrect_line_IDs": ", ".join(incorrect_ids) if incorrect_ids else "",
# #         "reason": "; ".join(reasons) if reasons else "",
# #         "accuracy (%)": accuracy
# #     })

# #     print(f"✅ {page_name}: {correct_count}/{total_lines} correct ({accuracy}%)")

# # # === Save to Excel ===
# # df = pd.DataFrame(report_rows)
# # df.to_excel(report_path, index=False)

# # print("\n📊 Comparison report saved successfully!")
# # print(f"📁 File: {report_path}")


# import os
# import json
# import pandas as pd

# # === PATHS ===
# book_root = r"D:\FYP\Data\Books_Data4\1665_book"
# lines_info2_path = os.path.join(book_root, "lines_info.json")       # Reference GT
# correct_json_path = os.path.join(book_root,  "correctLines_GT.json")  # Predicted GT
# line_output_root = os.path.join(book_root, "line_output")            # For counting total JPGs
# report_path = os.path.join(book_root, "report.xlsx")

# # === Load JSON files ===
# print("📖 Loading lines_info2.json ...")
# with open(lines_info2_path, "r", encoding="utf-8") as f:
#     lines_info2 = json.load(f)

# print("📖 Loading correctLines_GT2.json ...")
# with open(correct_json_path, "r", encoding="utf-8") as f:
#     correct_lines_json = json.load(f)

# # === Initialize report data ===
# report_rows = []

# # === Iterate through each page ===
# for page_name, page_lines in lines_info2.items():
#     correct_page = correct_lines_json.get(page_name, {})

#     # Count total jpgs from line_output/<page_name>
#     page_folder = os.path.join(line_output_root, page_name)
#     total_lines = len([f for f in os.listdir(page_folder) if f.lower().endswith(".jpg")]) \
#         if os.path.exists(page_folder) else len(page_lines)

#     correct_count = 0
#     incorrect_count = 0
#     incorrect_ids = []
#     reasons = []

#     for line_key, gt_line_data in page_lines.items():
#         # Step 1: check if line exists
#         if line_key not in correct_page:
#             incorrect_count += 1
#             incorrect_ids.append(line_key)
#             reasons.append("❌ Missing line in correctLines_GT")
#             continue

#         pred_line_data = correct_page[line_key]

#         # ✅ Step 2: Compare total CCs
#         gt_total = gt_line_data.get("Total_CCs", len(gt_line_data.get("CC_labels", {})))
#         pred_total = pred_line_data.get("Total_CCs", len(pred_line_data.get("CC_labels", {})))

#         if gt_total != pred_total:
#             incorrect_count += 1
#             incorrect_ids.append(line_key)
#             reasons.append(f"⚠️ Total_CCs mismatch (GT={gt_total}, Pred={pred_total})")
#             continue

#         gt_labels = set(gt_line_data.get("CC_labels", {}).keys())
#         pred_labels = set(pred_line_data.get("CC_labels", {}).keys())

#         # ✅ Step 3: Compare CC labels
#         if gt_labels != pred_labels:
#             incorrect_count += 1
#             incorrect_ids.append(line_key)
#             reasons.append(f"⚠️ CC label mismatch: GT={sorted(gt_labels)} vs Pred={sorted(pred_labels)}")
#             continue

#         # ✅ Step 4: Compare TBLR
#         tblr_mismatch = []
#         for cc_label in gt_labels:
#             gt_cc = gt_line_data["CC_labels"][cc_label]
#             pred_cc = pred_line_data["CC_labels"][cc_label]
#             for key in ["top", "bottom", "left", "right"]:
#                 if gt_cc.get(key) != pred_cc.get(key):
#                     tblr_mismatch.append(f"{cc_label}.{key}")

#         if tblr_mismatch:
#             incorrect_count += 1
#             incorrect_ids.append(line_key)
#             reasons.append("⚠️ TBLR mismatch in: " + ", ".join(tblr_mismatch))
#         else:
#             correct_count += 1

#     # Compute metrics
#     accuracy = round((correct_count / total_lines) * 100, 2) if total_lines > 0 else 0.0

#     report_rows.append({
#         "page_name": page_name,
#         "total_lines": total_lines,
#         "correct_lines": correct_count,
#         "incorrect_lines": incorrect_count,
#         "incorrect_line_IDs": ", ".join(incorrect_ids) if incorrect_ids else "",
#         "reason": "; ".join(reasons) if reasons else "",
#         "accuracy (%)": accuracy
#     })

#     print(f"✅ {page_name}: {correct_count}/{total_lines} correct ({accuracy}%)")

# # === Convert to DataFrame ===
# df = pd.DataFrame(report_rows)

# # === Add Summary Row ===
# total_total = df["total_lines"].sum()
# total_correct = df["correct_lines"].sum()
# total_incorrect = df["incorrect_lines"].sum()
# overall_accuracy = round((total_correct / total_total) * 100, 2) if total_total > 0 else 0.0

# summary_row = {
#     "page_name": "📘 OVERALL TOTAL",
#     "total_lines": total_total,
#     "correct_lines": total_correct,
#     "incorrect_lines": total_incorrect,
#     "incorrect_line_IDs": "",
#     "reason": "",
#     "accuracy (%)": overall_accuracy
# }

# df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

# # === Save to Excel ===
# df.to_excel(report_path, index=False)

# print("\n📊 Comparison report saved successfully!")
# print(f"📁 File: {report_path}")
# print(f"\n📘 Overall Accuracy: {overall_accuracy}% ({total_correct}/{total_total} lines)")


import os
import json
import pandas as pd

# === PATHS ===
book_root = r"D:\FYP\Data\Books_Data7\1209_book"
lines_info_path = r"D:\FYP\Data\Books_Data7\1209_book\lines_info.json"        # Reference GT
correct_json_path =r"D:\FYP\Data\Books_Data7\1209_book\correctLines_GT.json" # Predicted / Filtered GT
line_output_root = os.path.join(book_root, "line_output")            # For counting total JPGs
report_path = os.path.join(book_root, "report1.xlsx")

# === Step 1: Load JSONs ===
print("📖 Loading lines_info.json ...")
with open(lines_info_path, "r", encoding="utf-8") as f:
    lines_info = json.load(f)

print("📖 Loading correctLines_GT.json ...")
with open(correct_json_path, "r", encoding="utf-8") as f:
    correct_lines_json = json.load(f)

# === Step 2: Prepare for report ===
report_rows = []

# === Step 3: Compare each page ===
for page_name, page_data in lines_info.items():
    correct_page = correct_lines_json.get(page_name, {})
    gt_lines = page_data.get("Lines", {})
    correct_lines = correct_page.get("Lines", {})

    # Count total JPGs from line_output/<page_name> (optional)
    page_folder = os.path.join(line_output_root, page_name)
    total_lines = (
        len([f for f in os.listdir(page_folder) if f.lower().endswith(".jpg")])
        if os.path.exists(page_folder)
        else len(gt_lines)
    )

    correct_count = 0
    incorrect_count = 0
    incorrect_ids = []
    reasons = []

    # === Step 4: Compare each line ===
    for line_key, gt_line_data in gt_lines.items():
        if line_key not in correct_lines:
            incorrect_count += 1
            incorrect_ids.append(line_key)
            reasons.append("❌ Missing line in correctLines_GT")
            continue

        pred_line_data = correct_lines[line_key]

        # Compare total CCs
        gt_total = gt_line_data.get("Total_CCs", len(gt_line_data.get("CC_labels", {})))
        pred_total = pred_line_data.get("Total_CCs", len(pred_line_data.get("CC_labels", {})))

        if gt_total != pred_total:
            incorrect_count += 1
            incorrect_ids.append(line_key)
            reasons.append(f"⚠️ Total_CCs mismatch (GT={gt_total}, Pred={pred_total})")
            continue

        # Compare CC label sets
        gt_labels = set(gt_line_data.get("CC_labels", {}).keys())
        pred_labels = set(pred_line_data.get("CC_labels", {}).keys())

        if gt_labels != pred_labels:
            incorrect_count += 1
            incorrect_ids.append(line_key)
            reasons.append(f"⚠️ CC label mismatch: GT={sorted(gt_labels)} vs Pred={sorted(pred_labels)}")
            continue

        # Compare TBLR values for each CC
        tblr_mismatch = []
        for cc_label in gt_labels:
            gt_cc = gt_line_data["CC_labels"][cc_label]
            pred_cc = pred_line_data["CC_labels"][cc_label]
            for key in ["top", "bottom", "left", "right"]:
                if gt_cc.get(key) != pred_cc.get(key):
                    tblr_mismatch.append(f"{cc_label}.{key}")

        if tblr_mismatch:
            incorrect_count += 1
            incorrect_ids.append(line_key)
            reasons.append("⚠️ TBLR mismatch in: " + ", ".join(tblr_mismatch))
        else:
            correct_count += 1

    # === Step 5: Calculate accuracy ===
    accuracy = round((correct_count / total_lines) * 100, 2) if total_lines > 0 else 0.0

    report_rows.append({
        "page_name": page_name,
        "total_lines": total_lines,
        "correct_lines": correct_count,
        "incorrect_lines": incorrect_count,
        "incorrect_line_IDs": ", ".join(incorrect_ids),
        "reason": "; ".join(reasons),
        "accuracy (%)": accuracy
    })

    print(f"✅ {page_name}: {correct_count}/{total_lines} correct ({accuracy}%)")

# === Step 6: Create summary ===
df = pd.DataFrame(report_rows)

total_total = df["total_lines"].sum()
total_correct = df["correct_lines"].sum()
total_incorrect = df["incorrect_lines"].sum()
overall_accuracy = round((total_correct / total_total) * 100, 2) if total_total > 0 else 0.0

summary_row = {
    "page_name": "📘 OVERALL TOTAL",
    "total_lines": total_total,
    "correct_lines": total_correct,
    "incorrect_lines": total_incorrect,
    "incorrect_line_IDs": "",
    "reason": "",
    "accuracy (%)": overall_accuracy
}

df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

# === Step 7: Save to Excel ===
df.to_excel(report_path, index=False)

print("\n📊 Comparison report saved successfully!")
print(f"📁 File: {report_path}")
print(f"\n📘 Overall Accuracy: {overall_accuracy}% ({total_correct}/{total_total} lines)")
