import base64

import requests


def download():
    url = 'https://cdn.prod.website-files.com/6600c65ea72e48aee6a742fe/6609b080d3a32bb0fd1a0381_token.png'
    response = requests.get(url)
    with open('image.png', 'wb') as f:
        f.write(response.content)


def encode():
    with open('image.png', 'rb') as f:
        print(base64.b64encode(f.read()))


encode()
