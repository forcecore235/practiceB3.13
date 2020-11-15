class Tag():
    """Объекты класса Tag могут быть непарные или быть парные и содержать текст внутри себя."""
    def __init__(self, tag="div", is_single = False, *args, **kwargs):
        self.tag = tag
        self.attributes = {}
        self.inner_code = []
        self.text = ""
        self.is_single = is_single

    def __str__(self):
        # Преобразование словаря с атрибутами в строку
        attrs = []
        for attribute, value in self.attributes.items():
            for val in value:
                if len(val) > 1:
                    value = " ".join(self.attributes[attribute])
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        # Открывающий и закрывающий теги
        if self.attributes != {}:
            first_line = f"<{self.tag} {attrs}>"
        else:
            first_line = f"<{self.tag}>"
        second_line = f"</{self.tag}>"
        single_line = f"<{self.tag} {attrs}/>"

        # Преобразование списка с вложенным кодом в строку для последующего вывода/записи 
        str_inner_code = "".join(str(x) for x in self.inner_code)

        if self.is_single is False:
            result = str("\n" + first_line + str(self.text) + str_inner_code + second_line)
        else:
            result = str("\n" + single_line + "\n")

        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self

    def __iadd__(self, other):
        self.inner_code.append(other)
        return self

class TopLevelTag(Tag):
    """Объекты класса TopLevelTag скорее всего не содержат внутреннего текста и всегда парные."""
    def __init__(self, tag="div"):
        super().__init__()
        self.tag = tag
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        return self
    
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        # Открывающий и закрывающий теги
        if self.attributes != {}:

            first_line = f"<{self.tag} {attrs}>"
        else:
            first_line = f"<{self.tag}>"
        second_line = f"</{self.tag}>"

        # Преобразование списка с вложенным кодом в строку для последующего вывода/записи 
        str_inner_code = "".join(str(x) for x in self.inner_code)

        result = str("\n" + first_line + str_inner_code + "\n" + second_line)

        return result

    def __iadd__(self, other):
        self.inner_code.append(other)
        return self

class HTML(TopLevelTag):
    """Класс HTML определяет, куда сохранять вывод: на экран через print или в файл."""
    def __init__(self, tag="html", output=None):
        super().__init__()
        self.tag = tag
        self.output = output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        # Преобразование словаря с атрибутами в строку
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        # Открывающий и закрывающий теги
        if self.attributes != {}:
            first_line = f"<{self.tag} {attrs}>"
        else:
            first_line = f"<{self.tag}>"
        second_line = f"</{self.tag}>"
        
        # Преобразование списка с вложенным кодом в строку для последующего вывода/записи 
        str_inner_code = "".join(str(x) for x in self.inner_code)
        result_string = str(first_line + str_inner_code + "\n" + second_line)
        # Вывод в консоль либо в файл в зависимости от значения output 
        if self.output is None:
            print(result_string)
        else:
            with open(self.output, "w") as opfile:
                opfile.write(result_string)

    def __iadd__(self, other):
        self.inner_code.append(other)
        return self

# Функция проверки. Переделал момент с указанием атрибутов(указание атрибутов как здесь ИМХО более понятно для человека кто не видит что под капотом). В связи с этим можно использовать зарезервированное слово class.
def main(output=None):
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1") as h1:
                h1.attributes["class"] = "main-text"
                h1.text = "Test"
                body += h1

            with Tag("div") as div:
                div.attributes["class"] = ("container", "container-fluid")
                div.attributes["id"] = "lead"
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True) as img:
                    img.attributes["src"] = "/icon.png"
                    img.attributes["data_image"] = "responsive"
                    div += img

                body += div

            doc += body

if __name__ == "__main__":
    main()
    