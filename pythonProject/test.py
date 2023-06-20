import math
import tkinter
from tkinter import filedialog, messagebox
from tkinter import Entry

from PIL import ImageTk, Image, ImageFont, ImageDraw


def get_file():
    global filename
    filename = filedialog.askopenfilename()
    if filename:

        canvas = tkinter.Canvas(win, height=500, width=500, bg='gray')
        canvas.place(x=15, y=15)
        image = Image.open(filename)
        image = image.resize((500, 500))
        photo = ImageTk.PhotoImage(image)
        canvas.image = photo
        image = canvas.create_image(250, 250, image=photo)

        win.update()
    else:
        messagebox.showinfo('Фото', 'Выберите фото, которое хотите закодировать!')


def post_env():
    global scalefac, charwidth, charheight
    if 18 >= int(charheight_var.get()) >= 0:
        charheight = charheight_var.get()
    else:
        messagebox.showerror('EnvErrorCharHeight!', 'Введите в пределах 18')
    if 10 >= int(charwidth_var.get()) >= 0:
        charwidth = charwidth_var.get()
    else:
        messagebox.showerror('EnvErrorCharWidth!', 'Введите в пределах 10')
    if 0.9 >= (scalefac_var.get() / 100) >= 0:
        scalefac = scalefac_var.get() / 100
    else:
        messagebox.showerror('EnvErrorScaleFac!', 'Вводить в процентах и до 90%')


def coding():
    try:
        filename

        def coder(scalefac_func, charwidth_func, charheight_func):

            image = Image.open(filename)
            w, h = image.size
            image = image.resize((int(scalefac * w), int(scalefac * h * (charwidth / charheight))), Image.NEAREST)
            w, h = image.size
            pixels = image.load()

            font = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', 15)
            output_image = Image.new('RGB', (charwidth * w, charheight * h), color=(0, 0, 0))
            draw = ImageDraw.Draw(output_image)

            def get_some_char(h):
                chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
                charArr = list(chars)
                l = len(charArr)
                mul = l / 256
                return charArr[math.floor(h * mul)]

            for i in range(h):
                for j in range(w):
                    r, g, b = pixels[j, i]
                    grey = int((r / 3 + g / 3 + b / 3))
                    pixels[j, i] = (grey, grey, grey)
                    draw.text((j * charwidth, i * charheight), get_some_char(grey),
                              font=font, fill=(r, g, b))

            output_image.save(
                f"image_ascii_{str(scalefac).replace('.', '_')}_{charwidth}_{charheight}.png")

        coder(scalefac, charwidth, charheight)
        messagebox.showinfo('Успешно!',
                            f'''Фотография была сохранена в файл 
                            "image_ascii_{str(scalefac).replace(".", "_")}_{charwidth}_{charheight}.png"''')
        win.destroy()

    except NameError:
        messagebox.showerror('Фото', 'Выберите фото!')


# win customize
win = tkinter.Tk()
win.title('Image_ascii_coder')
win.geometry('800x600')
win.config(bg='#333')
win.resizable(width=False, height=False)

scalefac_var = tkinter.IntVar()
charwidth_var = tkinter.IntVar()
charheight_var = tkinter.IntVar()

# entry
entry_scalefac = Entry(win, width=11, bg='gray', textvariable=scalefac_var).place(x=535, y=430)
entry_charwidth = Entry(win, width=11, bg='gray', textvariable=charwidth_var).place(x=535, y=405)
entry_charheight = Entry(win, width=11, bg='gray', textvariable=charheight_var).place(x=535, y=380)

# label
label_scalefac = tkinter.Label(win, text='ScaleFac (до 90%)', fg='gray', bg='#333', font='Lobster').place(x=610, y=430)
label_charwidth = tkinter.Label(win, text='CharWidth (до 10)', fg='gray', bg='#333', font='Lobster').place(x=610, y=405)
label_charheight = tkinter.Label(win, text='CharHeight (до 18)', fg='gray', bg='#333', font='Lobster').place(x=610,
                                                                                                             y=380)

# welcome_text
text = 'Данная программа предназначена для "кодировки" фотографий в ascii, что по-моему мнению выглядит круто,' \
       ' и может быть ещё кому-то понадобится'
welcome_text = tkinter.Text(win, wrap=tkinter.WORD, font='Lobster', fg='gray', bg='#333', height=20, width=28,
                            borderwidth=0)
welcome_text.insert(tkinter.INSERT, text)
welcome_text.configure(state=tkinter.DISABLED)
welcome_text.place(x=535, y=15)

# button
continue_btn = tkinter.Button(win, text='Run!', command=coding, borderwidth=0, highlightcolor='#555', bg='gray',
                              font='Lobster').place(x=735, y=550)

open_photo_btn = tkinter.Button(win, borderwidth=0, text='Open photo', command=get_file, highlightcolor='#555',
                                bg='gray',
                                font='Lobster').place(x=15, y=550)

get_env_btn = tkinter.Button(win, borderwidth=0, text='Post env', command=post_env, highlightcolor='#555',
                             bg='gray', width=7,
                             font='Lobster').place(x=535, y=470)

# mainloop
win.mainloop()
