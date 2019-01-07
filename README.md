# shorten
Minimal link shortener

```
pip3 install -r requirements.txt
sudo PASSWORD=thepassword python3 app.py
```

### Usage
A password is required to access the home page (to edit routes). Specify the password through the above command.

To change a route, just submit the form again and it will overwrite the old one.

### Troubleshooting
If you see `invalid command bdist_wheel` when installing, try `pip3 install wheel`. If it still gives you issues, just get rid of Flask-BasicAuth from the requirements and write some other janky auth method.
