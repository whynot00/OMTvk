import shutil

from datetime import date
from jinja2 import FileSystemLoader, Environment

from messages import UserCorespondence


class TemplateHTML(UserCorespondence):

    def __init__(self, template_path, filenames):
        super().__init__(filenames)
        
        file_loader = FileSystemLoader(template_path)
        self.env = Environment(loader=file_loader)

        self.main_dir = f"VK_{date.today().strftime('%d_%m_%Y')}"
    
    def get_file_info(self):
        errors_lst = []
        lst_file_info = []
        for txt_file in self.files:
            try:
                lst_file_info.append(self._files_info(txt_file))
            except:
                errors_lst.append((txt_file, 2))
                continue
        
        for errors in errors_lst:
            self.files = errors[0]
            
        return lst_file_info, errors_lst

    def get_template(self, save_path):
        self.save_path = save_path
        
        errors_lst = []

        for txt_file in self.files:
            self._get_messages(txt_file)
            try:
                self.__create_folder()
                for user in self:
                    self.__get_dialog(user)
                self.__get_index()
            except FileExistsError:
                errors_lst.append((txt_file, 1))
                continue

        return errors_lst
            
    def __create_folder(self):
        self.user_dir = f'{self.suspect_name["name"]} {" ".join(map(lambda x: x.split()[0],self.suspect_period))}'
        shutil.copytree("vk_dependence/vk_relation", f"{self.save_path}/{self.main_dir}/{self.user_dir}")
        
    def __get_index(self):
        tm = self.env.get_template('index.html')

        with open(f"{self.save_path}\\{self.main_dir}\\{self.user_dir}\\index.html", "w", encoding="utf-8") as file:
            file.write(tm.render(messages=self))

    def __get_dialog(self, user):
        tm = self.env.get_template('dialogs.html')
        with open(f"{self.save_path}\\{self.main_dir}\\{self.user_dir}\\dialogs\\{user[0].file_path}", "w", encoding="utf-8") as file:
            file.write(tm.render(messages=user))