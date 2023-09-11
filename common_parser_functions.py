def row_has_link(table_row):
    return table_row.find("a") is not None


def is_header_numeric(table_row):
    return table_row.find('th').text.isnumeric()


def get_url_of_element_at_index(element, index):
    def get_url_of_element(html_object):
        return html_object.find_all(element)[index]['href']
    return get_url_of_element


def get_text_of_element_at_index(element, index):
    def get_text_of_element(html_object):
        return html_object.find_all(element)[index].text
    return get_text_of_element


def get_text_of_element_with_attributes(attributes):
    def return_function(html_object):
        return get_element_with_attributes(attributes)(html_object).text
    return return_function


def get_element_with_attributes(attributes):
    def return_function(html_object):
        return html_object.find(attrs=attributes)
    return return_function


def get_text_in_parentheses(html_object):
    return html_object.text.split('(')[1].split(')')[0]


def get_text_after_colon(html_object):
    return html_object.text.split(':')[1]

def does_tr_have_thead_class(html_object):
    return html_object.has_attr('class') and 'thead' in html_object['class']

def does_tr_not_have_thead_class(html_object):
    return does_tr_have_thead_class(html_object) == False


def does_element_not_have_strong_and_does_tr_not_have_thead_class(html_object):
    return does_tr_not_have_thead_class(html_object) and html_object.find("strong") is None

def does_html_object_contain_bold(html_object):
    if html_object.find("b") is not None:
        return 1
    return 0

def is_plus_in_html_object_text(html_object):
    if '+' in html_object.text:
        return 1
    return 0


def one(html_object):
    return 1

def zero(html_object):
    return 0

