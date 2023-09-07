def row_has_link(table_row):
    return table_row.find("a") is not None

def is_header_numeric(table_row):
    return table_row.find('th').text.isnumeric()

def first_link_url(object):
    return object.find('a')['href']


def first_link_text(object):
    return object.find('a').text

def one(html_object):
    return 1

def zero(html_object):
    return 0