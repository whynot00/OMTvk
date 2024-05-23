from template_html import TemplateHTML
from additional_functions import time_of_function


@time_of_function
def main():

    temlplate = TemplateHTML("vk_dependence\\vk_template")
    temlplate.get_template()

if __name__ == "__main__":
    main()

