import tkinter.filedialog as fd
import tkinter as tk
import tkinterdnd2 as tkdnd
from template_html import TemplateHTML
import re

class WaitingFrame(tk.Frame):

    def __init__(self, master, template, save_path):
        super().__init__(master)
        self.master = master
        self.config(pady=20, padx=30)

        errors_lst = template.get_template(save_path)

        tk.Label(self, text="Готово.").pack(pady=(25,10), padx=100)
        
        if len(errors_lst) != 0:
            tk.Label(self, text=f"Закончено с ошибкой: {len(errors_lst)}", padx=100).pack()
            for index, error in enumerate(errors_lst):

                tk.Label(self, text=f"{index + 1}. {error[0]} {self.__get_errors_code(error[1])}", padx=20).pack(pady=(5,0))

        tk.Button(self, text="Продолжить", command=self.__continue_button).pack(pady=(25, 25))

    def __get_errors_code(self, code):
        if code == 1:
            return "файл уже сковертирован."

    def __continue_button(self):

        self.destroy()
        DnDFrame(self.master).pack()

class FilesFrame(tk.Frame):

    def __init__(self, master, filenames):
        super().__init__(master)

        self.master = master

        self.config(pady=20, padx=30)
        self.temlplate = TemplateHTML("vk_dependence\\vk_template", filenames)
        files_info, errors_lst = self.temlplate.get_file_info()

        
        tk.Label(self, text=f"Всего загружено: {len(files_info)} файла(ов)", pady=15).grid(row=0, column=0, columnspan=3, sticky="n")
        tk.Label(self, text="Название файла", pady=5).grid(row=3, column=0, sticky="nw")
        tk.Label(self, text="Имя", pady=5).grid(row=3, column=1, sticky="nw")
        tk.Label(self, text="Период", pady=5).grid(row=3, column=2, sticky="nw")

        self.path_label = tk.Label(self, text="Путь сохранения: не указан")
        self.path_label.grid(row=1, column=0, columnspan=3, sticky="nw", pady=(5, 0))

        tk.Button(self, text="Указать путь", command=self.__save_path).grid(row=2, column=0, sticky="nw", pady=(5, 15))


        for item in enumerate(files_info):
            tk.Label(self, text=f"{item[1][2]}").grid(row=item[0] + 4, column=0, sticky="nw")
            tk.Label(self, text=f"{item[1][0]}").grid(row=item[0] + 4, column=1, sticky="nw")
            tk.Label(self, text=f"{item[1][1]}").grid(row=item[0] + 4, column=2, sticky="nw")

        if len(errors_lst) != 0:
            for item in errors_lst:
                row = self.grid_size()[1] + 1
                tk.Label(self, text=f"{item[0]}").grid(row=row, column=0, sticky="nw")
                tk.Label(self, text=f"ошибка").grid(row=row, column=1, sticky="nw")

        

        self.__buttons()


    def __buttons(self):
        row = self.grid_size()[1] + 1
        self.start_button = tk.Button(self, text="Начать", width=15, command=self.__start_button, state="disabled")
        self.start_button.grid(row=row, column=0, sticky="nw", pady=10)

        tk.Button(self, text="Отмена",width=15, command=self.__cancel_button).grid(row=row, column=2, sticky="nw", pady=10)

    def __save_path(self):
        self.dirname = fd.askdirectory(title="Указать путь сохранения", initialdir="/")
        if self.dirname:
            self.path_label.config(text=f"Путь сохранения: {self.dirname}")
            self.start_button["state"] = "normal"

    def __cancel_button(self):

        self.destroy()
        DnDFrame(self.master).pack()

    def __start_button(self):
        
        self.destroy()
        WaitingFrame(self.master, self.temlplate, self.dirname).pack()


class DnDFrame(tk.Frame):

    def  __init__(self, master):
        super().__init__(master)
        self.master = master

        self.config(padx=160, pady=200)
        self.dnd_label = tk.Label(self, text="Перенесите в данное окно .txt файл/файлы\nили\nукажите путь к файлам", pady=15)

        self.dnd_button = tk.Button(self, text="Найти...", width=15, pady=3, bg="#f1f0f7", command=self.__choose_files)        

        self.drop_target_register(tkdnd.DND_ALL)
        self.dnd_bind("<<Drop>>", self.__get_path)

        self.dnd_label.grid()
        self.dnd_button.grid()

    def __choose_files(self):
        filetype = (("Текстовый файл", "*.txt"),)
        filenames = fd.askopenfilenames(title="Открыть файл", initialdir="/",filetypes=filetype)
        if filenames:
            self.destroy()

            FilesFrame(self.master, filenames).pack()


    def __get_path(self, event):
        filenames = event.data.replace("{", "").replace("}", "").strip()
        filenames = re.findall("[^\s].+?.txt", filenames)

        self.destroy()
        FilesFrame(self.master, filenames).pack()


class App(tkdnd.TkinterDnD.Tk):

    def __init__(self):
        super().__init__()
        self.title("OMT Tool")

        frame = DnDFrame(self)
        frame.pack()