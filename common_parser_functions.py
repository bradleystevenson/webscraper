def row_has_link(table_row):
    return table_row.find("a") is not None

def is_header_numeric(table_row):
    return table_row.find('th').text.isnumeric()

def first_link_url(object):
    return object.find('a')['href']

def first_td_text(html_object):
    return html_object.find("td").text

def get_first_th_text(html_object):
    return html_object.find("th").text

def get_second_link_url(html_object):
    return html_object.find_all("a")[1]['href']

def first_link_text(object):
    return object.find('a').text

def get_third_td_text(html_object):
    return html_object.find_all('td')[2].text


def get_text_in_parantheses(html_object):
    return html_object.text.split('(')[1].split(')')[0]

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

