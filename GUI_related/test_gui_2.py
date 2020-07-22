## PARTIALLY WORKING - Button - with image resizing - all 20 images

#keep for refernce

## to change a button features later on e.g. 
##      button.configure(relief=tk.SUNKEN, state=tk.DISABLED)
##      button.configure(relief=tk.RAISED, state=tk.ACTIVE)    

##  PEDNING:   when Enlarge button is pressed, should show the image in a new larger window
##  CURRENTLY: when Select button is pressed, toggle the relief and the text
##             when Enlarge button is pressed, just prints the image and path of the image that would have been enlarged

# importing required packages
import tkinter as tk
from PIL import ImageTk, Image
import os

img_folder = r'/home/rohit/PyWDUbuntu/thesis/Imgs2Detect_20imgs/'

image_files_list = [os.path.join(img_folder, f) \
                    for f in os.listdir(img_folder) \
                    if os.path.isfile(os.path.join(img_folder, f))]
print(f"num of images = {len(image_files_list)}\narray=\n{image_files_list}")

class c_my_wnd_main_window:
    def __init__(self, _wnd_name):
        self.wnd = tk.Tk()
        self.wnd_name = _wnd_name
        self.frame_arr = None
    
    def build_frames(self, _n_rows, _n_cols, _in_img_arr):
        ## create array holding skeleton form of the objects of required frame types
        self.frame_arr = []
        for r_idx in range(_n_rows):
            self.wnd.columnconfigure(r_idx, weight=1, minsize=50)
            self.wnd.columnconfigure(r_idx, weight=1, minsize=50)
            temp_array = []
            for c_idx in range(_n_cols):
                frame_name_str = ''.join( ['frm_', str(r_idx+1), '_', str(c_idx+1)] )
                if (r_idx % 3) == 0: ## picture frame
                    temp_array.append(my_frm_image(self.wnd, frame_name_str))
                elif (r_idx % 3) == 1: ## enlarge frame
                    temp_array.append(my_frm_enlarge(self.wnd, frame_name_str))
                else: ## select frame
                    temp_array.append(my_frm_select(self.wnd, frame_name_str))
            self.frame_arr.append(temp_array)
        
        ## set the frame arrays objects as required
        img_idx = 0
        for r_idx in range(_n_rows):
            for c_idx in range(_n_cols):
                if (r_idx) % 3 == 0: ## picture frame
                    self.frame_arr[r_idx][c_idx].frm_img.grid(row=r_idx,
                                                              column=c_idx,
                                                              padx=5, pady=5
                                                             )
                    ## populate the image
                    resized_image, file_with_path = opened_imgs_arr[img_idx]
                    self.frame_arr[r_idx][c_idx].add_image(resized_image)
                    img_idx += 1
                    self.frame_arr[r_idx][c_idx].image_with_path = file_with_path
                elif (r_idx % 3) == 1: ## enlarge frame
                    self.frame_arr[r_idx][c_idx].frm_enlarge.grid(row=r_idx,
                                                              column=c_idx,
                                                              padx=5, pady=5
                                                             )
                    self.frame_arr[r_idx][c_idx].btn_enlarge.pack(padx=5, pady=5)
                    self.frame_arr[r_idx][c_idx].enlarge_this_image = self.frame_arr[r_idx - 1][c_idx].image_with_path ## bcoz immediately previous row should reference the image frame
                else: ## select frame
                    self.frame_arr[r_idx][c_idx].frm_select.grid(row=r_idx,
                                                              column=c_idx,
                                                              padx=5, pady=5
                                                             )
                    self.frame_arr[r_idx][c_idx].btn_select.pack(padx=5, pady=5)

class my_frm_image:
    def __init__(self, _wnd, _frame_name):
        self.frm_img = tk.Frame(
            master=_wnd,
            relief=tk.SUNKEN,
            borderwidth=2)
        self.frame_name = _frame_name
        self.image_with_path = None
        self.lbl_img = tk.Label(master=self.frm_img, image=None)
        
    def add_image(self, _in_img):
        #print(f" function add_image called ")
        self.lbl_img.configure(image=_in_img)
        self.lbl_img.pack(padx=1, pady=1)

class my_frm_enlarge:
    def __init__(self, _wnd, _frame_name):
        self.frm_enlarge = tk.Frame(
            master=_wnd,
            relief=tk.RAISED,
            borderwidth=4)
        self.frame_name = _frame_name
        self.enlarge_this_image = None
        self.btn_enlarge = tk.Button(
            master=self.frm_enlarge,
            text=f"Enlarge",
            bg="black", fg="white", 
            command=self.do_enlarge_btn_press_functionality
        )
        self.btn_enlarge.pack(padx=5, pady=5)
    
    def do_enlarge_btn_press_functionality(self):
        print(f"Would have enlarged image: {self.enlarge_this_image}")

class my_frm_select:
    def __init__(self, _wnd, _frame_name):
        self.frm_select = tk.Frame(
            master=_wnd,
            relief=tk.RAISED,
            borderwidth=4)
        self.frame_name = _frame_name
        self.btn_select = tk.Button(
            master=self.frm_select,
            text=f"Select",
            bg="black", fg="white",
            command=self.do_select_btn_press_functionality
        )
        self.btn_select.pack(padx=5, pady=5)
    
    def do_select_btn_press_functionality(self):
        #print(f"Pressed Select button: {self.frame_name}")
        if self.btn_select["text"] == 'Select':
            ## Sink button and change text to Deselect
            self.btn_select.configure(text=f"Deselect", relief=tk.SUNKEN, bg="yellow", fg="black")
        else:
            ## Raise button and change text to Select
           self.btn_select.configure(text=f"Select", relief=tk.RAISED, bg="black", fg="white")
        return


o_main_window = c_my_wnd_main_window('main_window')

opened_imgs_arr = []
for img_idx in range(20):
    img_orig = Image.open(image_files_list[img_idx])
    img_resized = img_orig.resize((100, 80),Image.ANTIALIAS)
    ## append tuple of resized image and file with path
    opened_imgs_arr.append( (ImageTk.PhotoImage(img_resized), image_files_list[img_idx]) )
    del img_orig, img_resized

num_rows_of_images = 4
n_rows = num_rows_of_images * 3
n_cols = int(len(image_files_list) / num_rows_of_images)
print(f"n_rows = {n_rows}\t\tn_cols = {n_cols}")
o_main_window.build_frames(n_rows, n_cols, image_files_list)
o_main_window.wnd.mainloop()

print(f"\n\nNormal exit.")

print(f"\n\nNormal exit.\n\n")