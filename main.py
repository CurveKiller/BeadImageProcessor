from tkinter import *
from tkinter import ttk
from functools import partial
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

        def open_command():
            print('open')

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

        action_button_frame = ttk.Frame(self.main_frame)
        action_button_frame.grid(row=0, column=0, sticky='W')
        button_height = 1
        button_width = 7

        new_button = Button(action_button_frame, text='New', height=button_height, width=button_width, padx=0, pady=0,
                            command=new_command)
        new_button.grid(row=0, column=0)
        new_button['state'] = 'disabled'

        open_button = Button(action_button_frame, text='Open', height=button_height, width=button_width, padx=0, pady=0,
                             command=open_command)
        open_button.grid(row=0, column=1)
        open_button['state'] = 'disabled'

        save_as_button = Button(action_button_frame, text='Save As', height=button_height, width=button_width, padx=0,
                                pady=0, command=save_as_command)
        save_as_button.grid(row=0, column=2)
        save_as_button['state'] = 'disabled'

        save_button = Button(action_button_frame, text='Save', height=button_height, width=button_width, padx=0, pady=0,
                             command=save_command)
        save_button.grid(row=0, column=3)
        save_button['state'] = 'disabled'

        clear_button = Button(action_button_frame, text='Clear', height=button_height, width=button_width, padx=0,
                              pady=0, command=clear_command)
        clear_button.grid(row=0, column=4)
        # clear_button['state'] = 'disabled'

        export_button = Button(action_button_frame, text='Export', height=button_height, width=button_width, padx=0,
                               pady=0, command=export_command)
        export_button.grid(row=0, column=5)
        export_button['state'] = 'disabled'

        grid_button = Button(action_button_frame, text='Grid', height=button_height, width=button_width, padx=0, pady=0,
                             command=grid_command)
        grid_button.grid(row=0, column=6)
        # grid_button['state'] = 'disabled'

        debug_check_box = ttk.Checkbutton(action_button_frame, text='Debug', command=debug_command,
                                          variable=self.debug_on )
        debug_check_box.grid(row=0, column=7)

    def setup_color_buttons(self):
        def set_fill_color(new_fill_color):
            self.primary_color = new_fill_color

        color_button_frame = ttk.Frame(self.main_frame)

        color_button_frame.grid(row=0, column=2, sticky='E')
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
                                  bg=cur_color, command=partial(set_fill_color, cur_color))
            color_button.grid(row=0, column=index)


    def populate_sheet(self):
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
            self.canvas = Canvas(bip.sheet_frame, bg=self.WHITE)
            self.canvas.grid(row=0, column=0, sticky='NSEW')

            scroll_x = ttk.Scrollbar(bip.sheet_frame, orient="horizontal", command=self.canvas.xview)
            scroll_x.grid(row=1, column=0, sticky="ew")

            scroll_y = ttk.Scrollbar(bip.sheet_frame, orient="vertical", command=self.canvas.yview)
            scroll_y.grid(row=0, column=1, sticky="ns")

            self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

            self.canvas.configure(scrollregion=(0, 0, 5015, 858))

            self.mat = []

        def cell_change(self, action, x, y, tag, color):
            # if self.bip.debug_on == 1:
            #     print(f'{action:10} | ({x:4},{y:4}) | tag = {tag:9} | color = {color}')
            print(f'{action:10} | ({x:4},{y:4}) | tag = {tag:9} | color = {color}')

        def get_tag(self, x, y):
            return self.mat[y // self.CELL_HEIGHT][x // self.CELL_WIDTH]

        def left_click_handler(self, event, cur_tag):
            self.cell_change('l-click', event.x, event.y, cur_tag, self.bip.primary_color)
            self.canvas.itemconfigure(cur_tag, fill=self.bip.primary_color)

        def right_click_handler(self, event, cur_tag):
            self.cell_change('r-click', event.x, event.y, cur_tag, self.bip.secondary_color)
            self.canvas.itemconfigure(cur_tag, fill=self.bip.secondary_color)

        def draw(self, action, x, y, fill, outline, tag):
            self.cell_change(action, x, y, tag, fill)
            cell = self.canvas.create_rectangle(x - x % self.CELL_WIDTH + self.CELL_OFFSET,
                                         y - y % self.CELL_HEIGHT + self.CELL_OFFSET,
                                         x - x % self.CELL_WIDTH + self.CELL_WIDTH + self.CELL_OFFSET,
                                         y - y % self.CELL_HEIGHT + self.CELL_HEIGHT + self.CELL_OFFSET,
                                         fill=fill, outline=outline, tags=(tag, self.ALL_TAG))

            self.canvas.tag_bind(tag, '<ButtonPress-1>', partial(self.left_click_handler, cur_tag=tag))
            self.canvas.tag_bind(tag, '<ButtonPress-3>', partial(self.right_click_handler, cur_tag=tag))

        def populate(self):
            # print(f'height = {self.canvas.winfo_reqheight()}')
            # print(f'width  = {self.canvas.winfo_reqwidth()}')
            # print(f'height = {self.canvas.winfo_height()}')
            # print(f'width  = {self.canvas.winfo_width()}')
            # self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
            #                              fill='red', outline='blue')
            # self.bip.
            #int(self.canvas.winfo_height()*1.4)
            # print(f'{self.canvas.winfo_height()} / {self.CELL_HEIGHT}')
            for r in range(0, 1977-380-380-380, self.CELL_HEIGHT):
                new_row = []
                for c in range(0, 4985, self.CELL_WIDTH):
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
