import os, shutil

from datetime import date
from jinja2 import FileSystemLoader, Environment

from messages import UserCorespondence


class TemplateHTML(UserCorespondence):

    def __init__(self, template_path):
        super().__init__("vk_coresnpondence")

        file_loader = FileSystemLoader(template_path)
        self.env = Environment(loader=file_loader)

        self.main_dir = f"VK_{date.today().strftime('%d_%m_%Y')}"
        

    def get_template(self):
        if self.main_dir in os.listdir("."):
            shutil.rmtree(self.main_dir)
        
        print("Файлов в папке: ", len(self.files), "\n")
        x = 1
        for txt_file in self.files:
            self._get_messages(txt_file)
            self.__create_folder()
            for user in self:
                self.__get_dialog(user)
            self.__get_index()

            print(f"{x} / {len(self.files)} |",self.suspect_name["name"], "готово.", f"Всего чатов: {len(self)}.")
            x+=1
        
            
    def __create_folder(self):
        self.user_dir = f'{self.suspect_name["name"]} {" ".join(map(lambda x: x.split()[0],self.suspect_period))}'
        shutil.copytree("vk_dependence/vk_relation", f"{self.main_dir}/{self.user_dir}")
        
    def __get_index(self):
        tm = self.env.get_template('index.html')

        with open(f"{self.main_dir}\\{self.user_dir}\\index.html", "w", encoding="utf-8") as file:
            file.write(tm.render(messages=self))

    def __get_dialog(self, user):
        tm = self.env.get_template('dialogs.html')
        with open(f"{self.main_dir}\\{self.user_dir}\\dialogs\\{user[0].file_path}", "w", encoding="utf-8") as file:
            file.write(tm.render(messages=user))