# React Twitter Back

<p>This is the backend code of my Twitter clone project, to use the fronted you can find it here https://github.com/lidormaymon/Twitter-Front </p>
<p>The link for the deployed web https://twitter-clone-project-1.netlify.app/</p>
<p>Credentials for admin user are: Username:admin Password:123</p>

## Features:
<ul>
  <li>Create accounts, post tweets, like, comment, follow, and unfollow users.</li>
  <li>Editing and deleting tweets.</li>
  <li>Editing profile(name, photo, and password)</li>
  <li>Viewing who's following the user on their profile and who they are following.</li>
  <li>Generated profiles for users, where you can see their posts, and posts they have liked.</li>
  <li>Sending email through DJANGO backend to users.</li>
  <li>Using toastr react to handle errors.</li>
  <li>Admin premissions:1.Removing tweets 2.Giving verified 3. Taking verified</li>
  <li>Viewing who liked your tweets</li>
  <li>Uploading photos, using emojis.</li>
  <li>A functionality search bar to search for users.</li>
  <li>Full responsive.</li>
  <li>Having functionality chats using web socket that is updated real, and so the conversations list.</li>
</ul>

## Instructions 
You can run it in two ways, either using the docker compose, or installing all the independices manually.

### Docker:

Using the docker compose you'll need to to do these 2 command down in seprate terminals.

	docker-compose up db

 	docker-compose up

And then you'll need to modify the database configuration in settings.py to this

	DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'twitter',        # Replace 'your_database_name' with your actual database name
        'USER': 'root',       # Replace 'your_mysql_username' with your MySQL username
        # 'PASSWORD': '1234',   # Replace 'your_mysql_password' with your MySQL password
        'PASSWORD':'pass',
        # 'HOST': '127.0.0.1',                 # Replace 'localhost' with your MySQL host if different
        'HOST': 'db',
        'PORT': '3306',                      # Replace '3306' with your MySQL port if different
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
	}

 The back-end will be reached by localhost:8001 afterwards.

### Manually:

First, you'll need to download the repository to your computer, you can do it by either clicking download or using in the terminal

    git clone https://github.com/lidormaymon/Twitter-Back

Then you'll have to create a virtual environment folder, by using.

    python -m venv env

Activate the virtual enviorment

    env/scripts/activate

Installing all the requirements

    pip install -r requirements.txt

Run redis using docker

	docker run --rm -p 6379:6379 redis:7 

Once you do all of that you'll have to create a schema on your MySQL, you can call it whatever you want, but you'll have to modify the adjustments you make
on settings.py according to your adjustments.

After you finished it you can go and use 

    python manage.py runserver

And that's all the backend server would run for you!

#
