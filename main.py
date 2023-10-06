from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import filedialog as fd
from PIL import Image
import math

class BIP:
    def __init__(self):
        self.root = Tk()
        self.main_frame = None
        self.sheet_frame = None
        self.sheet = None

        self.primary_color = '#FF0000'
        self.secondary_color = '#FFFFFF'
        self.grid_on = True
        self.debug_on = IntVar()
        self.debug_on.set(1)

    def prep_root(self):
        self.root.title('BeadImagizerProcessor')
        # self.root.resizable(False, False)
        self.root.geometry('1078x313')
        self.root.minsize(854, 85)
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky='NSEW')

    def configure_rows_cols(self):
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.main_frame, 1, weight=1)
        Grid.columnconfigure(self.main_frame, 0, weight=1)
        Grid.columnconfigure(self.main_frame, 1, weight=1)
        Grid.columnconfigure(self.main_frame, 2, weight=1)

    def setup_sheet(self):
        self.sheet_frame = ttk.Frame(self.main_frame)
        Grid.rowconfigure(self.sheet_frame, 0, weight=1)
        Grid.columnconfigure(self.sheet_frame, 0, weight=1)
        self.sheet_frame.grid(row=1, column=0, columnspan=3, sticky='NSEW')
        self.sheet = self.Sheet(self)

    def setup_action_buttons(self):
        def new_command():
            print('new')
            new_window = Toplevel(self.root)
            new_window.resizable(False, False)
            new_window.geometry('180x115')
            new_window.title('Loom Size')
            new_window.grid_rowconfigure(0, weight=1)
            new_window.grid_columnconfigure(0, weight=1)

            new_window_frame = ttk.Frame(new_window, padding=10)
            new_window_frame.grid(row=0, column=0, sticky='')

            new_label = ttk.Label(new_window_frame, text='Please select loom size.')
            new_label.grid(row=0, column=0, columnspan=2)

            height_label = ttk.Label(new_window_frame, text='Height:')
            height_label.grid(row=1, column=0, sticky='E')

            width_label = ttk.Label(new_window_frame, text='Width:')
            width_label.grid(row=2, column=0, sticky='E')

            create_button = ttk.Button(new_window_frame)

            class HeightWidthSemaphore:
                def __init__(self):
                    self.height_check = True
                    self.width_check = True

                def update_height(self, new_height):
                    self.height_check = new_height

                def update_width(self, new_width):
                    self.width_check = new_width

            wh_sema = HeightWidthSemaphore()

            def create_button_enabler(whSema, height_checker=None, width_checker=None):
                if height_checker != None:
                    whSema.update_height(height_checker)
                if width_checker != None:
                    whSema.update_width(width_checker)
                if whSema.height_check and whSema.width_check:
                    create_button.configure(state='normal')
                else:
                    create_button.configure(state='disabled')

            def validate_height(action, index, value_if_allowed,
                         prior_value, text, validation_type, trigger_type, widget_name):
                # https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
                if value_if_allowed:
                    try:
                        int(value_if_allowed)
                        create_button_enabler(wh_sema, height_checker=True)
                        return True
                    except ValueError:
                        return False
                else:
                    create_button_enabler(wh_sema, height_checker=False)
                    return True

            vcmd_height = (new_window.register(validate_height),
                           '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

            def validate_width(action, index, value_if_allowed,
                         prior_value, text, validation_type, trigger_type, widget_name):
                # https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
                if value_if_allowed:
                    try:
                        int(value_if_allowed)
                        create_button_enabler(wh_sema, width_checker=True)
                        return True
                    except ValueError:
                        return False
                else:
                    create_button_enabler(wh_sema, width_checker=False)
                    return True
            vcmd_width = (new_window.register(validate_width),
                          '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

            height_combo = ttk.Spinbox(new_window_frame, from_=1, to=200, width=6, validate='key', validatecommand=vcmd_height)
            height_combo.grid(row=1, column=1)
            height_combo.set(13)

            width_combo = ttk.Spinbox(new_window_frame, from_=1, to=500, width=6, validate='key', validatecommand=vcmd_width)
            width_combo.grid(row=2, column=1)
            width_combo.set(50)

            def create_loom(height_combo, width_combo):
                height_combo.update()
                width_combo.update()
                print('create_loom')
                # print(f'height={height_combo.get()} width={width_combo.get()}')
                self.sheet.reset()
                self.sheet.populate(int(height_combo.get()), int(width_combo.get()))
                new_window.destroy()

            height_combo.update()
            create_button.configure(text='Create')
            create_button.configure(command=partial(create_loom, height_combo, width_combo))
            create_button.grid(row=3, column=0, columnspan=2)

            # new_window.grab_set()

        def open_command():
            print('open')
            filetypes = (
                ('Png files', '*.png'),
                ('All files', '*.*')
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            if filename != "":
                image = Image.open(filename)

                self.sheet.load(image)

        def save_as_command():
            print('save as')

        def save_command():
            print('save')

        def clear_command():
            print('clear')
            self.sheet.clear()

        def export_command():
            print('export')

        def grid_command():
            print('grid')
            self.sheet.gridify()
            self.grid_on = not self.grid_on

        def debug_command():
            print('debug')
            # print(self.debug_on)
            # self.debug_on = not self.debug_on
            # self.debug_on = not self.debug_on

        def size_change_command(row=0, col=0):
            self.sheet.change_size(row, col)

        action_button_frame = ttk.Frame(self.main_frame)
        action_button_frame.grid(row=0, column=0, sticky='W')
        button_height = 1
        button_width = 7

        new_button = Button(action_button_frame, text='New', height=button_height, width=button_width, padx=0, pady=0,
                            command=new_command)
        new_button.grid(row=0, column=0)

        open_button = Button(action_button_frame, text='Open', height=button_height, width=button_width, padx=0, pady=0,
                             command=open_command)
        open_button.grid(row=0, column=1)

        save_as_button = Button(action_button_frame, text='Save As', height=button_height, width=button_width, padx=0,
                                pady=0, command=save_as_command)
        save_as_button.grid(row=0, column=2)

        save_button = Button(action_button_frame, text='Save', height=button_height, width=button_width, padx=0, pady=0,
                             command=save_command)
        save_button.grid(row=0, column=3)

        clear_button = Button(action_button_frame, text='Clear', height=button_height, width=button_width, padx=0,
                              pady=0, command=clear_command)
        clear_button.grid(row=0, column=4)

        export_button = Button(action_button_frame, text='Export', height=button_height, width=button_width, padx=0,
                               pady=0, command=export_command)
        export_button.grid(row=0, column=5)

        grid_button = Button(action_button_frame, text='Grid', height=button_height, width=button_width, padx=0, pady=0,
                             command=grid_command)
        grid_button.grid(row=0, column=6)

        debug_check_box = ttk.Checkbutton(action_button_frame, text='Debug', command=debug_command,
                                          variable=self.debug_on )
        debug_check_box.grid(row=0, column=7)

        row_less_button = Button(action_button_frame, text='row-', height=button_height, width=button_width, padx=0, pady=0,
                             command=partial(size_change_command, row=-1))
        row_less_button.grid(row=1, column=0)

        row_plus_button = Button(action_button_frame, text='row+', height=button_height, width=button_width, padx=0, pady=0,
                            command=partial(size_change_command, row=1))
        row_plus_button.grid(row=1, column=1)

        col_less_button = Button(action_button_frame, text='col-', height=button_height, width=button_width, padx=0, pady=0,
                         command=partial(size_change_command, col=-1))
        col_less_button.grid(row=1, column=2)

        col_plus_button = Button(action_button_frame, text='col+', height=button_height, width=button_width, padx=0, pady=0,
                         command=partial(size_change_command, col=1))
        col_plus_button.grid(row=1, column=3)

    def setup_color_buttons(self):
        def set_fill_color(new_fill_color):
            self.primary_color = new_fill_color

        color_button_frame = ttk.Frame(self.main_frame)

        color_button_frame.grid(row=0, column=2, sticky='SE')
        button_height = 1
        button_width = 3

        color_list = []
        color_list.append('#ff0000')
        color_list.append('#ff6a00')
        color_list.append('#ffD800')
        color_list.append('#32AC51')
        color_list.append('#0094FF')
        color_list.append('#0026FF')
        color_list.append('#B200FF')
        color_list.append('#FF00DC')
        color_list.append('#FF006E')
        color_list.append('#FFFFFF')
        color_list.append('#808080')
        color_list.append('#404040')
        color_list.append('#000000')

        for index in range(len(color_list)):
            cur_color = color_list[index]
            color_button = Button(color_button_frame, height=button_height, width=button_width, padx=0, pady=0,
                                  bg=cur_color, activebackground=cur_color, command=partial(set_fill_color, cur_color))
            color_button.grid(row=0, column=index)

    def populate_sheet(self):
        print('populate_sheet')
        self.sheet.populate()

    def run(self):
        self.prep_root()
        self.configure_rows_cols()
        self.setup_sheet()
        self.setup_action_buttons()
        self.setup_color_buttons()

        self.root.update()
        self.populate_sheet()

        self.root.mainloop()

    class Sheet:
        CELL_HEIGHT = 19
        CELL_WIDTH = math.floor(CELL_HEIGHT*1.47826086957+0.5)
        CELL_OFFSET = 2
        BLACK = '#000000'
        WHITE = '#FFFFFF'
        ALL_TAG = 'ALL'

        def __init__(self, bip):
            self.bip = bip
            self.sheet_height = 45
            self.sheet_width = 179
            self.canvas = Canvas(bip.sheet_frame, bg=self.WHITE)
            self.canvas.grid(row=0, column=0, sticky='NSEW')

            scroll_x = ttk.Scrollbar(bip.sheet_frame, orient="horizontal", command=self.canvas.xview)
            scroll_x.grid(row=1, column=0, sticky="ew")

            scroll_y = ttk.Scrollbar(bip.sheet_frame, orient="vertical", command=self.canvas.yview)
            scroll_y.grid(row=0, column=1, sticky="ns")

            self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

            self.canvas.configure(scrollregion=(0, 0, 5015, 858))

            self.mat = []

        def reset(self):
            print('reset')
            self.canvas.delete(self.ALL_TAG)
            self.mat = []

        def change_size(self, row, col):
            if row != 0:
                if row < 0:
                    if self.sheet_height + row >= 1:
                        for r in range(abs(row)):
                            last_row = self.mat.pop()
                            for cell in last_row:
                                self.canvas.delete(cell)
                            self.sheet_height -= 1
                    else:
                        print('Too little rows left!')
                elif row > 0:
                    for r in range(abs(row)):
                        new_row = []
                        for col_index in range(self.sheet_width):
                            new_tag = f'{self.sheet_height}_{col_index}'
                            new_row.append(new_tag)
                            self.draw('col+', col_index, self.sheet_height, self.WHITE,
                                      outline=self.BLACK if self.bip.grid_on else '', tag=new_tag)
                        self.mat.append(new_row)
                        self.sheet_height += 1
            elif col != 0:
                if col < 0:
                    if self.sheet_width + col >= 1:
                        for c in range(abs(col)):
                            for row in self.mat:
                                last_cell = row.pop()
                                self.canvas.delete(last_cell)
                            self.sheet_width -= 1

                    else:
                        print('Too little cols left!')
                elif col > 0:
                    for c in range(abs(col)):
                        for row_index in range(self.sheet_height):
                            new_tag = f'{row_index}_{self.sheet_width}'
                            self.mat[row_index].append(new_tag)
                            self.draw('col+', self.sheet_width, row_index, self.WHITE,
                                      outline=self.BLACK if self.bip.grid_on else '', tag=new_tag)
                        self.sheet_width += 1
            else:
                print('change_size() called but with no parameters!')

            print(f'sheet_height = {self.sheet_height} sheet_width = {self.sheet_width}')
            print(f'mat = **{self.mat}**')

        def cell_change(self, action, x, y, tag, color):
            # if self.bip.debug_on == 1:
            #     print(f'{action:10} | ({x:4},{y:4}) | tag = {tag:9} | color = {color}')
            print(f'{action:10} | ({x:4},{y:4}) | tag = {tag:9} | color = {color}')

        def get_tag(self, r, c):
            return f'{c}_{r}'

        def get_rgb(self, pixel):
            # print(pixel)
            hex_r = hex(pixel[0])
            hex_g = hex(pixel[1])
            hex_b = hex(pixel[2])

            hex_r = hex_r[2:len(hex_r)].upper()
            hex_g = hex_g[2:len(hex_g)].upper()
            hex_b = hex_b[2:len(hex_b)].upper()
            return f'#{hex_r:02}{hex_g:02}{hex_b:02}'

        def load(self, image):
            image = image.convert('RGB')
            # print(f'image size = **{image.size}**')
            pixels = image.load()
            # print(f'pixels[0][0] = **{pixels[0, 0]}**')
            self.reset()
            self.populate(height=image.size[1], width=image.size[0])
            # print('good')
            print(f'pixels = {pixels}')
            for r in range(image.size[0]):
                for c in range(image.size[1]):
                    cur_tag = self.get_tag(r, c)
                    self.canvas.itemconfigure(cur_tag, fill=self.get_rgb(pixels[r,c]))

        def left_click_handler(self, event, cur_tag):
            self.cell_change('l-click', event.x, event.y, cur_tag, self.bip.primary_color)
            self.canvas.itemconfigure(cur_tag, fill=self.bip.primary_color)

        def middle_click_handler(self, event, cur_tag):
            self.cell_change('m-click', event.x, event.y, cur_tag, self.canvas.itemcget(self.canvas.find_withtag(cur_tag), "fill"))
            self.bip.primary_color = self.canvas.itemcget(self.canvas.find_withtag(cur_tag), "fill")

        def right_click_handler(self, event, cur_tag):
            self.cell_change('r-click', event.x, event.y, cur_tag, self.bip.secondary_color)
            self.canvas.itemconfigure(cur_tag, fill=self.bip.secondary_color)

        def draw(self, action, x, y, fill, outline, tag):
            x = x*self.CELL_WIDTH
            y = y*self.CELL_HEIGHT
            self.cell_change(action, x, y, tag, fill)
            cell = self.canvas.create_rectangle(x - x % self.CELL_WIDTH + self.CELL_OFFSET,
                                                y - y % self.CELL_HEIGHT + self.CELL_OFFSET,
                                                x - x % self.CELL_WIDTH + self.CELL_WIDTH + self.CELL_OFFSET,
                                                y - y % self.CELL_HEIGHT + self.CELL_HEIGHT + self.CELL_OFFSET,
                                                fill=fill, outline=outline, tags=(tag, self.ALL_TAG),
                                                )

            self.canvas.tag_bind(tag, '<ButtonPress-1>', partial(self.left_click_handler, cur_tag=tag))
            self.canvas.tag_bind(tag, '<ButtonPress-2>', partial(self.middle_click_handler, cur_tag=tag))
            self.canvas.tag_bind(tag, '<ButtonPress-3>', partial(self.right_click_handler, cur_tag=tag))

        def populate(self, height=-1, width=-1):
            # print(f'height = {self.canvas.winfo_reqheight()}')
            # print(f'width  = {self.canvas.winfo_reqwidth()}')
            # print(f'height = {self.canvas.winfo_height()}')
            # print(f'width  = {self.canvas.winfo_width()}')
            # self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
            #                              fill='red', outline='blue')
            # self.bip.
            #int(self.canvas.winfo_height()*1.4)
            # print(f'{self.canvas.winfo_height()} / {self.CELL_HEIGHT}')
            print('populate')
            print(f'height={height} width={width}')
            if height == -1 and width == -1:
                for r in range(0, self.sheet_height, 1):
                    new_row = []
                    print(self.CELL_WIDTH)
                    for c in range(0, self.sheet_width, 1):
                        tag = f'{r}_{c}'
                        self.draw('populate', c, r, self.WHITE, self.BLACK, tag=tag)
                        new_row.append(tag)
                    self.mat.append(new_row)
            else:
                self.sheet_height = height
                self.sheet_width = width
                for r in range(0, height, 1):
                    new_row = []
                    # print(self.CELL_WIDTH)
                    for c in range(0, width, 1):
                        tag = f'{r}_{c}'
                        self.draw('populate', c, r, self.WHITE, self.BLACK, tag=tag)
                        new_row.append(tag)
                    self.mat.append(new_row)

        def clear(self):
            # for row in self.mat:
            #     for cell_tag in row:
            #         self.cell_change('clear', '', '', cell_tag, self.WHITE)
            #         self.canvas.itemconfigure(cell_tag, fill=self.WHITE)
            self.canvas.itemconfigure(self.ALL_TAG, fill=self.WHITE)

        def gridify(self):
            # for row in self.mat:
            #     for cell_tag in row:
            #         self.cell_change(f'grid-{not self.bip.grid_on}', '', '', cell_tag, '')
            #         self.canvas.itemconfigure(cell_tag, outline='' if self.bip.grid_on else self.BLACK)
            self.canvas.itemconfigure(self.ALL_TAG, outline='' if self.bip.grid_on else self.BLACK)


def main():
    my_bip = BIP()
    my_bip.run()


if __name__ == '__main__':
    main()
