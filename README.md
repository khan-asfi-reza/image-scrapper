<div align="center">
    <div style="display: flex; gap: 10px; justify-content: center; align-items: center">
        <img height="50" width="50" alt="Logo" src="https://github.com/khan-asfi-reza/image-scrapper/blob/master/.github/python.png"/>
        <img height="50" width="50" alt="Logo" src="https://github.com/khan-asfi-reza/image-scrapper/blob/master/.github/api.png"/>
    </div>
    <h1>Image Scrapper API</h1>
    <img alt="Logo" src="https://github.com/khan-asfi-reza/image-scrapper/actions/workflows/ci.yaml/badge.svg"/>
    <p>Image Scrapper scraps a given link and gets images and stores them in the database, later can be queried, not only the image is saved but also meta data [image format, height, width, size etc] are stored</p>
</div>


## Libraries 🌩️

- `Django`: To create backend along with ORM
- `Django Rest Framework`: To create restful API 
- `Beautifulsoup`: For web scrapping and collecting images
- `requests`: To handle external URL handling
- `Pillow`: Image processing
- `Celery`: Background async task handling
- `drf_yasg`: Swagger API Docs 

## How To Get Started 🎇

###1. Clone this repo 👮
```shell
git clone 
```

###2. Activate virtualenv 🅰️
```shell
virtualenv venv
```
For `windows`:
```
E:/image-scrapper/venv/scripts/activate
```

For `MacOS/Linux`
```
source venv/bin/activate
```

###3. Install Requirements 🔨️
```
pip install -r requirements.txt
```

###4. Test Application 🧪
```
python manage.py test
```

###5. Run server
```
python manage.py runserver
```
## Dev Docs 📑

### Important!

After running the server, you can visit `/api-docs` to get a swagger interface,
you can interfere with the api from `api-docs/`, it will automatically provide a beautiful UI and interface
to test the API

## API Docs 📑

<div>
<h3>⭐ /api/url</h3>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #248FB2; padding: 5px 10px; color: white">POST</p>
    <h4>/api/url/</h4>
</div>
</div>

#### Payload
```json
{
  "url": "https://example.com"
}
```

#### Response Sample

`Status Code: 200`

```json
[
  {
    "id": 0,
    "image_url": "https://example.com/api/image/0",
    "image_name": "string",
    "parent_url": {
      "id": 0,
      "link": "https://example.com"
    },
    "original_url": "https://example.com",
    "height": 0,
    "width": 0,
    "mode": "string",
    "format": "string",
    "created": "2019-08-24T14:15:22Z",
    "updated": "2019-08-24T14:15:22Z"
  }
]
```

<div>
<h3>⭐ /api/image/&lt;id:int&gt;</h3>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #2d24b2; padding: 5px 10px; color: white">GET</p>
    <h4>/api/image/&lt;id:int&gt;</h4>
</div>
</div>

#### Query Parameters

|Parameter|Type|Default|Options|
|---|---|---|---|
|width|integer/string|Image default width|`small`, `medium`, `large`|
|height|integer|Image default height|

Note:
If height and width both are given, only width will work to maintain aspect ratio

#### Example

```
api/image/2?width=small
```
or
```
api/image/2?width=678
```


### External

- `Workflow`

There are 2 main endpoints, one scraps through the link to get images and store them,
the second one sends image queried by id.

1. How the scraping and saving works?

- When the api is called, request library uses the link the get HTTP Response content, then bs4 module parses the HTTP 
response and gets `<img/>` tag from it and get the image sources/links. Then these links are passed to Pillow Image module to 
parse the image and get metadata, then the image is saved in the storage and metadata are stored in the database. The image is given an id.
Later the image can be queried through ID

The model schema of Image
```yaml
id: Integer
image: String | Image location in the file system
parent_url: String | The URL that was scrapped to get the image
original_url: String | Original URL of the image
height: Integer | Image height
width: Integer | Image width
mode: String | Image color mode
format: String | Image format
```
