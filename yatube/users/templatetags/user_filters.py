from django import template
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})


@register.filter 
def uglify(string):
    new_string = ''
    for letter in string:
        if len(new_string) % 2 == 0:
            new_string = new_string + letter.lower()
        else:
            new_string = new_string + letter.upper()   
    return new_string