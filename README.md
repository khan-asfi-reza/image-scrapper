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
- `djangorestframework-simplejwt[crypto]` For JWT Authentication

## How To Get Started 🎇

Get started with the project, install dependencies and run the project.
View /api-docs for API Documentation

- #### Clone this repo 👮

```shell
git clone 
```

- #### Activate virtualenv 🅰️
```shell
virtualenv venv
```
- For `windows` 🪟
```
E:/image-scrapper/venv/scripts/activate
```

- For `MacOS/Linux` 🍏
```
source venv/bin/activate
```

- #### Install Requirements 🔨️
```
pip install -r requirements.txt
```

- #### Test Application 🧪
```
python manage.py test
```

#### Run server
```
python manage.py runserver
```

## Docker 🐋

If you have docker and want to use docker

#### Build Docker Image
```
docker build --tag scrapper-api .
```

#### Run Docker Image

```
docker publish scrapper-api 8000:8000 
```

## Dev Docs 📑

### Important!

After running the server, you can visit `/api-docs` to get a swagger interface,
you can interfere with the api from `api-docs/`, it will automatically provide a beautiful UI and interface
to test the API

OR

Use `/redoc` for Redoc Documentation

## API Docs 📑

URL
------

-----------

<div>
<h3>URL API</h3>
<h3>⭐ /api/url</h3>
<p>
Takes URL, and returns List of images scrapped from the URL,
Saves those images along with meta data in the database
</p>
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
-----------

Image
-------

<div>
<h3> ⭐Image Details API</h3>
<p>
Returns Metadata and Image Link, if given a valid image id
</p>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #2D24B2FF; padding: 5px 10px; color: white">GET</p>
    <h4>/api/images/details/{:id}</h4>
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
```
-----------
<div>
<h3> ⭐Image Details API</h3>
<p>
Returns Metadata and Image Link, if given a valid image id
</p>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #b22439; padding: 5px 10px; color: white">DELETE</p>
    <h4>/api/images/details/{:id}</h4>
</div>
</div>

#### Payload
```json
{
  "url": "https://example.com"
}
```

#### Response Sample

`Status Code: 204`

-----------

<div>
<h3> ⭐Image List API</h3>
<p>
Returns List of saved Metadata and Image Link, if given a valid Parent URL(The URL that was used to scrape the images)
</p>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #248FB2FF; padding: 5px 10px; color: white">POST</p>
    <h4>/api/images/list/</h4>
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
```
-----------


<div>
<h3> ⭐Image Query API</h3>
<p>
Returns List of saved Metadata and Image Link, if given a valid Original Image URL
</p>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #248FB2FF; padding: 5px 10px; color: white">POST</p>
    <h4>/api/images/query/</h4>
</div>
</div>

#### Payload
```json5
{
  "url": "https://example.com/image/image.jpeg" // Original Image URL
}
```

#### Response Sample

`Status Code: 200`

```json
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
```
-----------


<div>
<h3> ⭐Image Restore API</h3>
<p>
Deletes all previous images and re-scrape and restore them
</p>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #248FB2FF; padding: 5px 10px; color: white">POST</p>
    <h4>/api/images/query/</h4>
</div>
</div>

#### Payload
```json5
{
  "url": "https://example.com" // Original Image URL
}
```

#### Response Sample

`Status Code: 200`

```json
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
```
-----------

## Routing Docs 🌐

Image View
------

-----------
<div>
<h3>⭐ Image Preview</h3>
<p>Image Preview Route, it will send image content to the client</p>
<div style="display: flex; gap: 10px; align-items: center">
    <p style="background: #2d24b2; padding: 5px 10px; color: white">GET</p>
    <h4>image/&lt;id:int&gt;</h4>
</div>
</div>

#### Query Parameters

|Parameter|Type|Default|Options|
|---|---|---|---|
|width|integer/string|Image default width|`small`, `medium`, `large`|
|height|integer|Image default height|`small`, `medium`, `large`
|quality|integer|100|Any number between 1 to 100|
|format|string|Image Default|"gif", "png", "jpeg", "jpg", "bmp", "webp"|

Note:
If height and width both are given, only width will work to maintain aspect ratio

#### Example

```
/image/2?width=small
```
or
```
/image/2?width=678
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
