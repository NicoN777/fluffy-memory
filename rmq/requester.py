import requests

def request(url:str):
    try:
        response = requests.get(url=url)
        if response.ok:
             data = response.json()
        return data
    except Exception:
        message = response.text
        status_code = response.status_code
        print(f'Something went wrong, status code: {status_code}'
              f'\nMessage: {message}')
        raise


def request_comments():
    url = 'https://jsonplaceholder.typicode.com/comments'
    return request(url)

def request_todos():
        url = 'https://jsonplaceholder.typicode.com/todos'
        return request(url)