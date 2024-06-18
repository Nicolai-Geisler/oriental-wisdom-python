# Oriental Wisdom Python backend

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2560px-Python_logo_and_wordmark.svg.png" alt="Python logo" style="height:150px;"/>

## Flask

Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.
It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. 
However, Flask supports extensions that can add application features as if they were implemented in Flask itself.

## Pillow

Python Imaging Library (Pillow or PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.

## API endpoints

### Get-image

Returns a random image as a jpeg.

**URL: .../api/get-image**

The function will first search the **unsplash images** and only use the few standard images as a fallback.

### Get-quote

**URL: .../api/get-quote**

Returns a random quote in JSON format:

```JSON
{
  "quote": "Some quote",
  "author": "Some Author"
}
```

The function will first search the **ollama quotes** and only use the few standard quotes as a fallback.

### Get-final

**URL: .../api/get-final**

Returns the final sharepic by adding the selected quote onto the selected image using **Pillow**.

### Fetch-quotes

**URL: .../api/fetch-quotes**

Gets a quote from a local **Ollama** Container. The process takes a lot of time without a GPU.

The quote is then stored in a JSON file.
