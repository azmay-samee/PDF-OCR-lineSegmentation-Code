# import os
# import numpy as np

# class Line:
#     def __init__(self, imgProcessor):
#         self.imgProcessorClass = imgProcessor
#         self.line_cc = []
#         self.top = 0
#         self.bottom = 0
#         self.left = 0
#         self.right = 0
#         self.ID = 0
#         self.image = []
#         self.height = 0
#         self.width = 0

#     def update_bounds(self, CC):
#         if len(self.line_cc) == 1:
#             self.top = CC.top
#             self.bottom = CC.bottom
#             self.left = CC.left
#             self.right = CC.right
#         else:
#             self.top = min(self.top, CC.top)
#             self.bottom = max(self.bottom, CC.bottom)
#             self.left = min(self.left, CC.left)
#             self.right = max(self.right, CC.right)

#     def check_Component(self, CC):
#         if len(self.line_cc) == 0:
#             return False
#         self.height = self.bottom - self.top + 1
#         overlap_top = max(self.top, CC.top)
#         overlap_bottom = min(self.bottom, CC.bottom)
#         overlap_height = max(0, overlap_bottom - overlap_top + 1)
#         CC_height = CC.bottom - CC.top + 1
#         overlap_percentage = (overlap_height / CC_height) * 100
#         return overlap_percentage >= 45
#     def Add(self, CC):
#         self.line_cc.append(CC)
#         self.update_bounds(CC)



# class Line:
#     def __init__(self, imgProcessor):
#         self.imgProcessorClass = imgProcessor
#         self.line_cc = []        # all CCs (main + diacritics)
#         self.main_cc = []   
#         self.diacritics=[]     # only main-body CCs

#         # Main body bounding box
#         self.main_top = float("inf")
#         self.main_bottom = -float("inf")
#         self.main_left = float("inf")
#         self.main_right = -float("inf")
#         self.diacritics_top = float("inf")
#         self.diacritics_bottom = -float("inf")
#         self.diacritics_left = float("inf")
#         self.diacritics_right = -float("inf")

#         # Full bounding box (includes diacritics)
#         self.full_top = float("inf")
#         self.full_bottom = -float("inf")
#         self.full_left = float("inf")
#         self.full_right = -float("inf")
#         self.baseline=0
#         self.ID = 0
#         self.image = None
#         self.main_height = 0
#         self.main_width = 0
#         self.full_height = 0
#         self.full_width = 0
#         self.diacritics_height = 0
#         self.diacritics_width = 0
#     # -------------------------------
#     # Update bounding boxes
#     # -------------------------------
#     def update_main_bounds(self, CC):
#         """Update main-body box only."""
#         self.main_top = min(self.main_top, CC.top)
#         self.main_bottom = max(self.main_bottom, CC.bottom)
#         self.main_left = min(self.main_left, CC.left)
#         self.main_right = max(self.main_right, CC.right)

#     def update_full_bounds(self, CC):
#         """Update full box (letters + diacritics)."""
#         self.full_top = min(self.full_top, CC.top)
#         self.full_bottom = max(self.full_bottom, CC.bottom)
#         self.full_left = min(self.full_left, CC.left)
#         self.full_right = max(self.full_right, CC.right)
#     def update_diacritics_bounds(self, CC):
#         """Update diacritics box only."""
#         self.diacritics_top = min(self.diacritics_top, CC.top)
#         self.diacritics_bottom = max(self.diacritics_bottom, CC.bottom)
#         self.diacritics_left = min(self.diacritics_left, CC.left)
#         self.diacritics_right = max(self.diacritics_right, CC.right)

#     # -------------------------------
#     # Add components
#     # -------------------------------
#     def AddMain(self, CC):
#         """Add a main-body CC to the line."""
#         self.main_cc.append(CC)
#         self.line_cc.append(CC)
#         self.update_main_bounds(CC)
#         self.update_full_bounds(CC)

#     def AddDiacritic(self, CC):
#         """Add a diacritic CC to the line (does not touch main bounds)."""
#         self.diacritics.append(CC)
#         self.update_diacritics_bounds(CC)
#         self.line_cc.append(CC)
#         self.update_full_bounds(CC)

#     # -------------------------------
#     # Component check for line grouping
#     # -------------------------------
#     def check_Component(self, CC):
#         """
#         Decide if CC belongs to this line based on overlap with main box.
#         Uses % overlap relative to CC height.
#         """
#         if len(self.main_cc) == 0:
#             return False

#         overlap_top = max(self.main_top, CC.top)
#         overlap_bottom = min(self.main_bottom, CC.bottom)
#         overlap_height = max(0, overlap_bottom - overlap_top + 1)

#         CC_height = CC.bottom - CC.top + 1
#         overlap_percentage = (overlap_height / CC_height) * 100

#         return overlap_percentage >=  45# threshold (can tune)
# #    -----------------    # Helpers
#     # -------------------------------
#     def get_main_box(self):
#         return (self.main_top, self.main_bottom, self.main_left, self.main_right)

#     def get_full_box(self):
#         return (self.full_top, self.full_bottom, self.full_left, self.full_right)




class Line:
    def __init__(self, imgProcessor):
        self.imgProcessorClass = imgProcessor
        self.line_cc = []        # all CCs (main + diacritics)
        self.main_cc = []        # only main-body CCs
        self.diacritics = []     # only diacritics

        # Main body bounding box
        self.main_top = float("inf")
        self.main_bottom = -float("inf")
        self.main_left = float("inf")
        self.main_right = -float("inf")

        # Diacritic bounding box
        self.diacritics_top = float("inf")
        self.diacritics_bottom = -float("inf")
        self.diacritics_left = float("inf")
        self.diacritics_right = -float("inf")

        # Full bounding box (includes everything)
        self.full_top = float("inf")
        self.full_bottom = -float("inf")
        self.full_left = float("inf")
        self.full_right = -float("inf")

        self.baseline = 0
        self.pts=[]
        self.ID = 0
        self.main_image = None
        self.line_img = None
        self.image = None

        # Cached sizes
        self.main_height = 0
        self.main_width = 0
        self.full_height = 0
        self.full_width = 0
        self.diacritics_height = 0
        self.diacritics_width = 0

    # -------------------------------
    # Update bounding boxes
    # -------------------------------
    def update_main_bounds(self, CC):
        self.main_top = min(self.main_top, CC.top)
        self.main_bottom = max(self.main_bottom, CC.bottom)
        self.main_left = min(self.main_left, CC.left)
        self.main_right = max(self.main_right, CC.right)

    def update_full_bounds(self, CC):
        self.full_top = min(self.full_top, CC.top)
        self.full_bottom = max(self.full_bottom, CC.bottom)
        self.full_left = min(self.full_left, CC.left)
        self.full_right = max(self.full_right, CC.right)

    def update_diacritics_bounds(self, CC):
        self.diacritics_top = min(self.diacritics_top, CC.top)
        self.diacritics_bottom = max(self.diacritics_bottom, CC.bottom)
        self.diacritics_left = min(self.diacritics_left, CC.left)
        self.diacritics_right = max(self.diacritics_right, CC.right)

    # -------------------------------
    # Recompute bounds (after removals)
    # -------------------------------
    def recompute_full_bounds(self):
        """Recompute bounding boxes from scratch after changes."""
        if not self.line_cc:
            # Reset everything if empty
            self.full_top = self.full_bottom = self.full_left = self.full_right = 0
            self.main_top = self.main_bottom = self.main_left = self.main_right = 0
            self.diacritics_top = self.diacritics_bottom = self.diacritics_left = self.diacritics_right = 0
            return

        # Reset and recompute
        self.full_top = min(cc.top for cc in self.line_cc)
        self.full_bottom = max(cc.bottom for cc in self.line_cc)
        self.full_left = min(cc.left for cc in self.line_cc)
        self.full_right = max(cc.right for cc in self.line_cc)

        if self.main_cc:
            self.main_top = min(cc.top for cc in self.main_cc)
            self.main_bottom = max(cc.bottom for cc in self.main_cc)
            self.main_left = min(cc.left for cc in self.main_cc)
            self.main_right = max(cc.right for cc in self.main_cc)

        if self.diacritics:
            self.diacritics_top = min(cc.top for cc in self.diacritics)
            self.diacritics_bottom = max(cc.bottom for cc in self.diacritics)
            self.diacritics_left = min(cc.left for cc in self.diacritics)
            self.diacritics_right = max(cc.right for cc in self.diacritics)

    # -------------------------------
    # Add components
    # -------------------------------
    def AddMain(self, CC):
        if CC not in self.main_cc:
            self.main_cc.append(CC)
        if CC not in self.line_cc:
            self.line_cc.append(CC)
        self.update_main_bounds(CC)
        self.update_full_bounds(CC)

    def AddDiacritic(self, CC):
        if CC not in self.diacritics:
            self.diacritics.append(CC)
        if CC not in self.line_cc:
            self.line_cc.append(CC)
        self.update_diacritics_bounds(CC)
        self.update_full_bounds(CC)

    # -------------------------------
    # Remove components
    # -------------------------------
    def RemoveDiacritic(self, CC):
        """Remove diacritic CC safely and recompute bounds."""
        removed = False
        if CC in self.diacritics:
            self.diacritics.remove(CC)
            removed = True
        if CC in self.line_cc:
            self.line_cc.remove(CC)
            removed = True

        if removed:
            self.recompute_full_bounds()
        return removed

    # -------------------------------
    # Component check for line grouping
    # -------------------------------
    def check_Component(self, CC):
        if len(self.main_cc) == 0:
            return False

        overlap_top = max(self.main_top, CC.top)
        overlap_bottom = min(self.main_bottom, CC.bottom)
        overlap_height = max(0, overlap_bottom - overlap_top + 1)

        CC_height = CC.bottom - CC.top + 1
        overlap_percentage = (overlap_height / CC_height) * 100

        return overlap_percentage >= 44  # threshold (can tune)

    # -------------------------------
    # Helpers
    # -------------------------------
    def get_main_box(self):
        return (self.main_top, self.main_bottom, self.main_left, self.main_right)

    def get_full_box(self):
        return (self.full_top, self.full_bottom, self.full_left, self.full_right)
    