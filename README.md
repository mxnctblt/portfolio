<div align="center">
  <img src="./static/apple-touch-icon.png" alt="interlude-logo">
</div>
<h1 align="center">Interlude</h1>
<h4 align="center">A web social media app focusing on music.</h4>

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

<div class="bg-image mb-5">
    <img src="./static/readmeimg.png" class="img-fluid" alt="about image" />
    </div>
</div>

## Introduction
To finalize our first year at [Holberton School](https://www.holbertonschool.fr/), we created Interlude !

> Interlude (definition) :
>>(music) a short piece of music played between the parts of a longer composition.

We played with the words and used it as a metaphore. Meaning, as everyone has already listened to music and will listen again, the short pieces are the moments in-between those listenings and the longer composition is life.

Interlude is a web social media app focusing on music, providing with a new way to pass the time. It is a place where anyone can discuss, discover & also introduce music to anyone. It's aimed at anyone who loves music - in other words, everyone!

## Key Features
<div align="center">
    <a href="https://www.youtube.com/watch?v=TfX71LlmUH4"></a>
</div>

## Installation

Our team has decided to not deployed this project but here is how to install it locally.

#### Required:
- [Git](https://git-scm.com/)
- [Django](https://www.djangoproject.com/) 4.2
- [Python](https://www.python.org/) 3.8+

#### Clone this repo:
If the requierements are met you can now clone this repository:
```
$ git clone https://github.com/mxnctblt/portfolio.git
```

#### Final step:
Once the repo is cloned, go in it:
```
$ cd portfolio
```

And do this 2 commands:
```
$ pip install django-cors-headers
```
```
$ python -m pip install Pillow
```

Note that depending on the Python's version you have downloaded the commands can change.

## Usage
Now that everything is installed you are ready to go and try Interlude !

Start by running the Server with:
```
$ pyhton manage.py runserver
```

`manage.py`: This is the command-line utility for interacting with our Django project. We can use it to run development servers, perform database migrations, run tests, and execute other management commands.

This message must have appeared:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 05, 2023 - 09:59:08
Django version 4.2.1, using settings 'portfolio.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Now that the server is running go to our website url that you just installed locally.

URL: http://127.0.0.1:8000/

Landing Page: http://127.0.0.1:8000/about

## Contributing

This web application uses the following open source packages:

- [Django](https://www.djangoproject.com/)
- [Python](https://www.python.org/)
- [MDB5](https://mdbootstrap.com/)

## Related
> Author's Github links :
>> Antoine Jacob [@AntoineJacob](https://github.com/AntoineJacob)
>> 
>> Maxence Thibault [@mxnctblt](https://github.com/mxnctblt)

## License
© 2023 Interlude, All Rights Reserved.
