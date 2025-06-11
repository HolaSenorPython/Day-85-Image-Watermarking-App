from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFont, ImageDraw
#-------------------CONSTANTS--------------------#
FONT_NAME = "Comic Sans MS"
DARK_BLUE = "#00809D"
APRICOT = "#FCECDD"
ORANGE = "#FF7601"
LIGHT_ORANGE = "#F3A26D"
LIME_GREEN = "#32CD32"
#----------------NON-BUTTON FUNCTIONS THAT ARE REALLY USEFUL LOL--------------#
def clear_home(): # Clears the home screen widgets
    frame.grid_forget()
    canvas.grid_forget()
    title_label.grid_forget()
    desc_label.grid_forget()
    upl_img_btn.grid_forget()
    how_to_use_btn.grid_forget()

def return_home(): # Reveals all the home widgets again
    frame.grid(row=3, column=1, columnspan=2)
    canvas.grid(row=1, column=1)
    title_label.grid(row=0, column=1)
    desc_label.grid(row=2, column=1)
    upl_img_btn.grid(row=3, column=1, padx=10)
    how_to_use_btn.grid(row=3, column=2, padx=10)

def create_image(image_path): # Process and understand the opened image from the user
    users_pil_img = Image.open(image_path)
    return users_pil_img

# Literally deletes a widget when called
def delete_widget(widget):
    widget.destroy()

def clear(*args):
    # Destroys every widget on the page
    for arg in args:
        delete_widget(arg)

# Show the UI for the add watermark page
def show_add_wtrmark_ui(pil_image, name_of_file):
    # If the file name is really long shorten it, else leave it
    if len(name_of_file) > 20:
        selected_file_lbl = Label(text=f"Selected {name_of_file[:20]}...", font=(FONT_NAME, 32, "bold"),
                                  bg=APRICOT, fg=ORANGE)
    else:
        selected_file_lbl = Label(text=f"Selected {name_of_file}", font=(FONT_NAME, 32, "bold"),
                                  bg=APRICOT, fg=ORANGE)
    selected_file_lbl.grid(row=0, column=1, columnspan=2)
    # If the image is too big resize it
    if pil_image.width >= 1000 or pil_image.height >= 1000:
        new_width = pil_image.width / 2
        new_height = pil_image.height / 2
        canvas_for_img = Canvas(screen, width=new_width, height=new_height, bg=APRICOT)
        print("Your image was resized for previewing purposes.")
    else:
        canvas_for_img = Canvas(screen, width=pil_image.width, height=pil_image.height, bg=APRICOT)

    tk_img = ImageTk.PhotoImage(pil_image)
    canvas_for_img.image_ref = tk_img  # Save a reference to the tk image in the canvas to remember it
    canvas_for_img.create_image(0, 0, image=canvas_for_img.image_ref, anchor="nw")
    canvas_for_img.grid(row=1, column=1)
    frame2 = ttk.Frame(screen, padding=10)
    frame2.grid(row=1, column=2, rowspan=6)
    # Add the labels and buttons for the watermark stuff
    wtrmrk_lbl = Label(frame2, text="Insert Watermark Text here.\n(Text is 28 pixels tall)", bg=APRICOT, fg=ORANGE, font=(FONT_NAME, 14))
    wtrmrk_lbl.grid(row=1, column=2, pady=10)
    watermark_entry = Entry(frame2)
    watermark_entry.grid(row=2, column=2, pady=10)
    add_coords_lbl = Label(frame2, text=f"Specify watermark coordinates (x first, then y)\n"
                                        f"(your image is {pil_image.width}x{pil_image.height})\n(0,0) is"
                                        f" the top left. No decimals please!", bg=APRICOT, fg=ORANGE, font=(FONT_NAME, 14))
    add_coords_lbl.grid(row=3, column=2, pady=10)
    x_entry = Entry(frame2)
    x_entry.grid(row=4, column=2, pady=10)
    y_entry = Entry(frame2)
    y_entry.grid(row=5, column=2, pady=10)
    add_wtrmrk_btn = Button(frame2, text="Add Watermark!", font=(FONT_NAME, 14), bg=DARK_BLUE, fg="white",
                            relief="flat", highlightthickness=0,
                            command=lambda: [place_watermark(watermark_entry.get(), int(x_entry.get()),
                                                             int(y_entry.get()), pil_image), clear(selected_file_lbl, canvas_for_img, frame2),])
    add_wtrmrk_btn.grid(row=6, column=2, pady=10)

# Show the New UI/Final UI in the process after the image is watermarked and ready
def final_ui(le_tk_img, pil_img):
    # Place the label with 'Your final image:'
    ur_final_img_lbl = Label(text="Your final image:", bg=APRICOT, fg=ORANGE, font=(FONT_NAME, 36, "bold"))
    ur_final_img_lbl.grid(row=0, column=1)
    # Get the canvas and get our new image/final image
    final_canvas_for_img = Canvas(screen, width=pil_img.width, height=pil_img.height, bg=APRICOT)
    final_canvas_for_img.image_ref = le_tk_img
    final_canvas_for_img.create_image(0, 0, image=final_canvas_for_img.image_ref, anchor="nw")
    final_canvas_for_img.grid(row=1, column=1)
    # Make the frame that will contain the 'download' button, and 'return home' button
    frame3 = ttk.Frame(screen, padding=10)
    frame3.grid(row=1, column=2, rowspan=3)
    download_img_btn = Button(frame3, text="Download Image!", font=(FONT_NAME, 16), bg=DARK_BLUE, fg="white", relief="flat",
                              highlightthickness=0, command=lambda: download_file_dialog(pillow_image=pil_img, tk_frame=frame3))
    download_img_btn.grid(row=1, column=2, pady=10)
    return_home_btn = Button(frame3, text="Watermark another image!", font=(FONT_NAME, 16), bg=DARK_BLUE, fg="white",
                             relief="flat", highlightthickness=0, command=lambda: [clear(ur_final_img_lbl,
                                                                                         final_canvas_for_img, frame3), return_home()])
    return_home_btn.grid(row=2, column=2, pady=10)
#-------------------BUTTON COMMANDS----------------#
def how_to_use(): # How the screen looks after pressing how to use button
    # Hide all the home widgets
    clear_home()

    # Add new widgets
    how_to_use_title = Label(text="How to use, and what this is for", bg=APRICOT,
                             fg=ORANGE, font=(FONT_NAME, 32, "bold"))
    how_to_use_title.grid(row=0, column=1)

    desc_2 = Label(text="This is a desktop app made made in Tkinter by Elisha N.\n"
                        "(HolaSenorPython) on Github. The purpose of this is for\n"
                        "images to be watermarked easily. This was also made as\n"
                        "part of Angela Yu's bootcamp. However, I didn't get her\n"
                        "help for this one! :D Hope you enjoy!", bg=APRICOT, fg=ORANGE,
                   font=(FONT_NAME, 16))
    desc_2.grid(row=1,column=1, pady=10)

    im_done = Button(text="I'm done reading", bg=DARK_BLUE, fg="white", font=(FONT_NAME, 20),
                     relief="flat", highlightthickness=0)
    im_done.grid(row=2, column=1, columnspan=2, pady=10)
    im_done.config(command=lambda: [clear(how_to_use_title, desc_2, im_done), return_home()])

def open_file_dialog():
    # Calls function to open the file selection dialog
    # This will stop EVERYTHING until something is selected, or dialog is cancelled.
    file_path = filedialog.askopenfilename(
        title="Select an Image file",
        filetypes=(
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), # Allow image file selection
            ("All files", "*.*") # Or all files selection
        )
    )
    # Check if there was actually something opened
    if file_path:
        clear_home()
        print(f"User selected the following file: {file_path}")
        # Split the file path by slashes, and get the last part (file name)
        file_name = file_path.split('/')[-1]
        users_img = create_image(file_path)
        show_add_wtrmark_ui(users_img, file_name) # Show the UI for the Add watermark page
    else:
        print("File selection cancelled.")
        cancel_file_lbl = Label(text="File selection failed or cancelled.\nTry again in two seconds...", font=(FONT_NAME, 20, "bold"),
                                bg=APRICOT, fg=DARK_BLUE)
        cancel_file_lbl.grid(row=4, column=1, columnspan=2)
        screen.after(2000, delete_widget, cancel_file_lbl)

def place_watermark(watermark_text, x_coord, y_coord, image):
    draw_obj = ImageDraw.Draw(image)
    # Get font
    font = ImageFont.truetype("fonts/Comic_Sans.ttf", 28)
    # Place the text on the image
    coords = (x_coord, y_coord)
    draw_obj.text(coords, watermark_text, font=font, fill="white", stroke_width=2, stroke_fill="black")
    # Convert the watermarked image into a tk, and reveal it
    new_tk_img = ImageTk.PhotoImage(image)
    final_ui(new_tk_img, image)

def download_file_dialog(pillow_image, tk_frame):
    # Open the save file as dialog and stuff
    file_path2 = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All files", "*.*")
        ],
        title="Save your watermarked image as..."
    )
    # If the user specified something, save the image, else stay on the same screen lol
    if file_path2:
        pillow_image.save(file_path2)
        print(f"Image saved successfully! Path: {file_path2}")
        success_file_save_label = Label(tk_frame, text="Image saved successfully!", bg=APRICOT, fg=LIME_GREEN, font=(FONT_NAME, 14))
        success_file_save_label.grid(row=3, column=2)
    else:
        print("File save cancelled or failed.")
        cancel_save_lbl = Label(tk_frame, text="File save cancelled or failed.", bg=APRICOT, fg=DARK_BLUE, font=(FONT_NAME, 14))
        cancel_save_lbl.grid(row=3, column=2)
#-------------------------------HOME UI SETUP------------------------------#
# Configure the screen
screen = Tk()

style = ttk.Style()
style.configure("TFrame", background=APRICOT)

frame = ttk.Frame(screen, padding=15)
frame.grid(row=3, column=1, columnspan=2)

screen.title("Image Watermarking App")
screen.minsize(width=650, height=700)
screen.config(padx=50, pady=50, bg=APRICOT)

# Get canvas with henry img
canvas = Canvas(width=256, height=256, bg=APRICOT, highlightthickness=0)
titi_path = 'images/henry.png'
titi_img = PhotoImage(file=titi_path)
canvas.create_image((128, 128), image=titi_img)
canvas.grid(row=1, column=1)

# Make title and other text
title_label = Label(text="Image Watermarking App", bg=APRICOT, fg=ORANGE,
                    font=(FONT_NAME, 32, 'bold'))
title_label.grid(row=0, column=1)

desc_label = Label(text="This app is meant to add a watermark to an image\n"
                        "of your choice, solidifying that image as yours.\nDon't"
                        " use maliciously, or else.", bg=APRICOT, fg=ORANGE,
                   font=(FONT_NAME, 16))
desc_label.grid(row=2, column=1)

upl_img_btn = Button(frame, text='Upload Image', font=(FONT_NAME, 20, "bold"), bg=DARK_BLUE,
                     fg='white', relief='flat', highlightthickness=0, command=open_file_dialog)
upl_img_btn.grid(row=3, column=1, padx=10)

how_to_use_btn = Button(frame, text='How to use?', font=(FONT_NAME, 20, "bold"), bg=DARK_BLUE,
                        fg='white', relief='flat', highlightthickness=0, command=how_to_use)
how_to_use_btn.grid(row=3, column=2, padx=10)

screen.mainloop()