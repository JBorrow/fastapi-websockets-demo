# Simple FastAPI Websockets Demo

This simple demo contains four parts:

- A very simple FastAPI (actually Starlette, as FastAPI just provides
  passthroughs when it comes to websockets) server that provides an
  endpoint where you can request squares of fixed colours. It also
  provides a HTTP endpoint, too!
- A webpage with a form with R, G, B entries where you can request
  squares of the colour you specify. This is primarily used to
  demonstrate error handling.
- A webpage with a single button that requests a thousand images
  from the server, to demonstrate the speed of websockets. There
  are two alternatives: one that uses a single websocket connection,
  and another that uses the more traditional approach of opening
  a HTTP request per image.

To really understand the benefits of websockets, you should
either run this on a remote server, or run it on a local server
with throttling enabled.

License: MIT

To run the demo, simply run `uvicorn app:app --port=12345`, and open
the webpages in your browser.
