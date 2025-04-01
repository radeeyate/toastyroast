# ToastyRoast

ToastyRoast is a website powered by Google Gemini 2.0 Flash that rates/roasts you on several factors.

![Screenshot of ToastyRoast](./media/Screenshot%202024-11-23%20at%2014-37-52%20ToastyRoast%20-%20Get%20roasted%20by%20AI!.png)

To host your own version, get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and put it in a `.env` file.
This is how it should look:

```env
GEMINI_KEY="YOUR_KEY_HERE"
CONNECTION_STRING="YOUR_MONGODB_CONNECTING_STRING_HERE"
```

After you make that, run `pip install -r requirements.txt` to install essential requirements.
Now, you can run `uvicorn main:app` to start up the web server.
