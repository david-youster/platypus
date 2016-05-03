# Platypus Blogging Engine

A simple blogging engine built on [Flask](http://flask.pocoo.org/).

## Installation

### Requirements

The following applications must first be installed:
- python3
- sass
- pip3

### Setup (Linux)

If you have not already done so, clone the repository and navigate to that
directory:
```
git clone https://github.com/xdav/platypus.git
cd platypus
```

Run the install script to install the Python dependencies:
```
./install.sh
```

Run the setup script to initialise the application:
```
python3 setup.py
```

Run the application:
```
python3 webapp.py
```

### Usage

(The following directions assume the application is using the default port
number, 5000.)

Once the application is running locally, the index page can be accessed by
directing your browser to [127.0.0.1:5000](http://127.0.0.1:5000).

You can log in as the default user by navigating to
[127.0.0.1:5000/login](http://127.0.0.1:5000/login) and inputting 'admin' for
both the login name and password.

#### User Roles

##### admin

Users possessing the *admin* role may create and delete user accounts via the
admin control panel, found at
[127.0.0.1:5000/admin](http://127.0.0.1:5000/admin). At
present, it isn't possible to edit a user's roles once the account has been
created.

##### author

Users with the *author* role may create, edit and delete articles. The author
control panel may be accessed by navigating to
[127.0.0.1:5000/author](http://127.0.0.1:5000/author). An *author* may only edit
or delete their own articles, unless they also possess the *editor* role.

Note that the usage of markdown is permitted in the body of an article, though
plain HTML is not.

##### editor

A user with the *editor* role may edit and delete articles authored by any user,
though they may not create articles of their own unless they are also assigned
the *author* role.

At present, there is no editor control panel. An *editor* may edit or delete an
article by selecting the appropriate option on the article's display page.

#### Configuration

The application's settings are stored in the file **config.json**, generated
upon running the setup script. The *dev* flag may be of particular interest
here - when set to *true* (the default value), the application will write and
read to and from a separate development database.

Database setup is handled automatically on running the webapp.py script.