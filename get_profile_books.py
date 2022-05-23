from bs4 import BeautifulSoup
import requests
import json
from re import sub

GOODREADS_BASE_URL = 'https://www.goodreads.com'
GOODREADS_BOOK_BASE_URL = GOODREADS_BASE_URL + '/book/show/'

SHELVES = ['read', 'currently-reading', 'to-read']

def get_bookshelf(user_id, shelf):
    is_page_valid = True
    page_num = 1

    data = {}
    books = 0
    while is_page_valid:
        page_link = "https://www.goodreads.com/review/list/{user_id}?page={page_num}&shelf={shelf}".format(user_id=user_id,page_num=str(page_num), shelf=shelf)
        page_response = requests.get(page_link, auth=('user', 'pass'),timeout=10)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        table = page_content.find('table', attrs={'class':'table stacked'})
        
        table_body = table.find('tbody')

        # table has no books
        if table_body.contents == []:
            is_page_valid = False
            break
        
        # parse books on the page
        books = table_body.find_all('tr')
        for book in books:
            isbn, book_data = parse_book(book)
            book_data['shelf'] = shelf
            data[isbn] = book_data
        
        # go to next page
        page_num += 1
            
    return data


def parse_book(book):
    book_data = {}
    attributes = book.find_all('td')
    for attribute in attributes:
        key = snake_case(attribute.find('label').contents[0].strip())
        book_data = parse_attribute(attribute, key, book_data)
    
    return book_data['isbn'], book_data

def parse_attribute(attribute_data, key, book_data):
        if key == 'author':
            author_url = get_author_url(attribute_data)
            value = attribute_data.div.get_text().strip()
            value = value.replace("\n*", "")
            author_name = value.split(", ")
            book_data[key] = author_name[1] + " " + author_name[0] if len(author_name) > 1 else author_name[0]
            book_data['author_url'] = author_url
        elif key == 'cover':
            book_url = get_book_url(attribute_data)
            book_data['book_url'] = book_url
        elif key == 'isbn' and attribute_data.div.get_text().strip() == '':
            # hacky solution: isbn won't be used on client-side
            # if no isbn is available then hash the book's title
            book_data[key] = str(hash(book_data['title']) % 2147483647)[:10]
        elif key == 'num_pages':
            value = attribute_data.div.get_text().strip()
            value = value[:value.find('\n')]
            book_data[key] = value
        elif key == 'num_ratings':
            value = attribute_data.div.get_text().strip().replace(",", "")
            book_data[key] = value
        elif key == 'my_rating' or "'s_rating" in key:
            return book_data
        elif key == 'shelves':
            # does not work; need to be logged in
            value = [link.get_text().strip() for link in attribute_data.find_all('a')] 
            book_data[key] = value 
        else:
            value = attribute_data.div.get_text().strip()
            book_data[key] = value

        return book_data

def get_book_url(attribute):
    return GOODREADS_BOOK_BASE_URL + str(attribute.div.div['data-resource-id'])

def get_author_url(attribute):
    return GOODREADS_BASE_URL + str(attribute.div.a['href'])

def snake_case(s):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()

# def main():
#     book_data = {}

#     for shelf in SHELVES:
#         book_data.update(get_bookshelf(USER_ID, shelf))


#     with open('test.txt', 'w') as convert_file:
#      convert_file.write(json.dumps(book_data))


# main()