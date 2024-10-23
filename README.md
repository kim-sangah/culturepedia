## Project name
Culturepedia

## Introduction
It is a platform that allows you to conveniently explore cultural content containing performances of various genres, provides personalized recommendations by analyzing user tastes, and helps you make better choices through in-depth reviews.

## Development Period
- Planning and Documentation: 2024.09.23 ~ 2024.09.27
- Development: 2024.09.27 ~ 2024.10.23
## Team Roles and Responsibilities

<table>
        <tr>
            <th scope="col">API</th>
            <th scope="col">FEATURES</th>
            <th scope="col">FRONTEND</th>
            <th scope="col">BACKEND</th>
        </tr>
        <tr>
            <td rowspan="6">ACCOUNTS</td>
            <td>Sign up</td>
            <td>김상아</td>
            <td>김채림</td>
        </tr>
        <tr>
            <td>Log in</td>
            <td>김상아, 김채림</td>
            <td>김채림</td>
        </tr>
        <tr>
            <td>Log out</td>
            <td>김상아</td>
            <td>김상아</td>
        </tr>
        <tr>
            <td>Profile view</td>
            <td>김채림</td>
            <td>김상아</td>
        </tr>
        <tr>
            <td>Profile Edit</td>
            <td>김상아</td>
            <td>김상아</td>
        </tr>
        <tr>
            <td>Account Deletion</td>
            <td>김채림</td>
            <td>김채림</td>
        </tr>
        <tr>
            <td rowspan="11">PERFORMANCES</td>
            <td>Data Pipeline Construction</td>
            <td>-</td>
            <td>이광욱, 김상아</td>
        </tr>
        <tr>
            <td>KOPIS API Crawling</td>
            <td>이광욱</td>
            <td>김채림</td>
        </tr>
        <tr>
            <td>Search</td>
            <td>이광욱</td>
            <td>김상아</td>
        </tr>
        <tr>
            <td>Detail Page</td>
            <td>이광욱</td>
            <td>김상아</td>
        </tr>
        <tr>
            <td>Favorites</td>
            <td>김채림</td>
            <td>김상아</td>
        </tr>
        <tr>
            <td>Reviews</td>
            <td>김채림</td>
            <td>김상아</td>
        </tr>
        <tr>
            <td>Category-Based Recommendations</td>
            <td>김채림</td>
            <td>김채림</td>
        </tr>
        <tr>
            <td>Cookie and Session Storage</td>
            <td>김채림, 이광욱</td>
            <td>김채림</td>
        </tr>
        <tr>
            <td>AI Hashtaging</td>
            <td align="center">-</td>
            <td>이광욱</td>
        </tr>
        <tr>
            <td>Scheduling</td>
            <td align="center">-</td>
            <td>이광욱</td>
        </tr>
        <tr>
            <td>Image Resizing</td>
            <td align="center">-</td>
            <td>이광욱</td>
        </tr>
        <tr>
            <td rowspan="1">Deployment</td>
            <td>Deployment</td>
            <td colspan="2" align="center">김상아</td>
        </tr>
        <tr>
            <td rowspan="1">Debugging</td>
            <td>Debugging, Improvements Based on UT (Unit Testing)</td>
            <td colspan="2" align="center">공통</td>
        </tr>
</table>


## Full Technology Stack Overview
- Backend: Python, Django REST Framework (DRF), LLM
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite
- Version Control: Github, AWS
- IDE: VSCode
- APIs Used: KOPIS API (Korea Performance Information System), OpenAI API
- Other Tools and Libraries:
  - APScheduler==3.10.4
  - asgiref==3.8.1
  - certifi==2024.8.30
  - charset-normalizer==3.3.2
  - Django==4.2
  - django-apscheduler==0.7.0
  - django-seed==0.3.1
  - djangorestframework==3.15.2
  - djangorestframework-simplejwt==5.3.1
  - ElementTreeFactory==1.0
  - Faker==30.1.0
  - idna==3.10
  - pillow==10.4.0
  - psycopg2==2.9.9
  - PyJWT==2.9.0
  - python-dateutil==2.9.0.post0
  - pytz==2024.2
  - requests==2.32.3
  - six==1.16.0
  - sqlparse==0.5.1
  - toposort==1.10
  - typing_extensions==4.12.2
  - tzdata==2024.2
  - tzlocal==5.2
  - urllib3==2.2.3
  - xmltodict==0.13.0


## Key Features
### Accounts
- Sign up
  - Users can create an account by providing mandatory information (Email, Password, Username) and optional details (Gender, Birthday). After signing up, users can access features like favorites, writing reviews, and receiving performance recommendations.
  ![회원가입(필수입력)](https://github.com/user-attachments/assets/8315c37a-c682-4de3-bd1f-da3ef2194f62)
![회원가입(완료)](https://github.com/user-attachments/assets/c6868f81-fc6e-4c92-a725-74973289abfd)
- Log in
  - Users can log in using their email and password. Authentication is handled via JWT (JSON Web Token).
  ![로그인](https://github.com/user-attachments/assets/c3e2c378-2f5e-49f2-bd7a-1cd5b83be8d0)
- Log Out
  - Users can log out, and their JWT token will be invalidated.
- Profile Edit
  - Users can update their username, password, gender, and birthday.
  ![회원정보 수정](https://github.com/user-attachments/assets/f445c70f-8d82-448b-b6f5-326a3d0d5939)
- Account Deletion
  - Users can delete their account by entering their password. This removes their data from the system.
- Profile View: Users can view their profile details (email, username, gender, birthday) and access their performance viewing history.
  - Viewing History
    - Users can see the performances they have reviewed.
  - Favorites
    - Users can view a list of performances they have marked as favorites.

  ![프로필 조회](https://github.com/user-attachments/assets/dad8d482-a866-45e6-a677-6014b0d020a6)

### Performances
- Browse Performances
  - Users can browse performance rankings by category, sort them by sales or newest, and filter performances by region. Clicking on a performance poster or title takes users to the performance’s detail page.
  ![금주 TOP2](https://github.com/user-attachments/assets/1b9efb8a-8c89-431f-8ef2-7a6d788c0510)
  ![카테고리별](https://github.com/user-attachments/assets/96ffac5f-3834-4f55-ad1a-faaa90454e35)
- Search Performances
  - Users can search performances by keywords (title, actor, venue, production company).
  ![검색](https://github.com/user-attachments/assets/c5bfa045-8b3b-4099-8c62-d387b7e58364)
- Performance Details
  - Users can view detailed information about a performance, including the title, start and end dates, venue, cast, crew, runtime, age restrictions, producers, pricing, poster, synopsis, genre, and status.
  ![상세페이지(공연정보)](https://github.com/user-attachments/assets/119ac518-f28f-4d5d-834a-7a42a4705ed6)
- Write Reviews
  - Users can write reviews for performances they have attended, including a star rating out of 5.
  ![상세페이지(리뷰)](https://github.com/user-attachments/assets/4a07648e-c4df-481d-ba1e-da41c8988b38)
- Edit Reviews
  - Users can edit reviews they have written.
- Delete Reviews
  - Users can delete reviews they have written.
  ![리뷰](https://github.com/user-attachments/assets/aab00e62-a5c2-4c4a-bb8a-5fb25ac0f05e)
- Add to Favorites
  - Users can add performances to their favorites list.
- Remove from Favorites
  - Users can remove performances from their favorites list.
  ![찜하기](https://github.com/user-attachments/assets/2f426fe1-c740-4fe0-9fc2-1726fe01bdfd)
- Performance Recommendations
  - Based on the user’s reviews (ratings of 3 stars or higher), favorites, and search tags, the system recommends personalized performances. If there’s insufficient user data, users can manually choose categories, characteristics, moods, and regions for recommendations.
  ![공연추천](https://github.com/user-attachments/assets/016632af-13bb-43a8-90be-b4678f5b52e6)



## Requirements
### Backend Requirements (Python 3.10, Django REST Framework)
- Sign Up (accounts)
  - Allows new users to register.
- Log In (signin)
  - Users can log in using their email and password.
- Log Out (signout)
  - Users can log out and terminate their session.
- Profile Edit (modify)
  - Users can update their profile information.
- Account Deletion (delete)
  - Users can delete their account.
- Profile View (profile)
  - Displays the user's profile.
- Performance List View (performances)
  - All users can view performance data.
- Performance Search (search)
  - Performances can be searched by title, actor, venue, or production company.
- Performance Details View (detail)
  - Displays detailed information about a performance.
- Performance Reviews (create/edit/delete)
  - Users can write, edit, and delete reviews for performances.
- Add/Remove Favorites
  - Users can add performances to or remove them from their favorites list.

### Frontend Requirements (HTML, CSS, Bootstrap)
- UI/UX Design
  - Build the user interface (UI) using Bootstrap.
- Sign Up/Log In/Log Out Pages
  - Pages for managing user accounts.
- Performance Review and Favorites Pages
  - Provide UI for users to write reviews and manage their favorite performances.
- Profile Page
  - Implement a page where users can view and edit their profile information.

### Database (SQLite, PostgreSQL)
- Review Table
  - Stores review data for each performance.
- Favorites Table
  - Stores a list of performances favorited by users.
- User Table
  - Stores user information and profiles.

### API Requirements
- KOPIS API
  - Provides performance lists and detailed performance information.
- OpenAI API
  - Utilizes LLM to offer additional AI-powered features.


## Service Structure
![Architecture](https://github.com/user-attachments/assets/5f605a7b-5db0-461a-ade4-22a0ea263a6f)
![culturepedia process flow drawio](https://github.com/user-attachments/assets/86118ec0-da4a-466a-a4dd-20637ff47f8a)

## WireFrame
https://www.figma.com/design/bc7ezCAoLV0OBzk35nNMSQ/Culturepedia-WireFrame?m=auto&t=M5PEKIqkya6poh6A-1

## API Documentation
https://documenter.getpostman.com/view/38012126/2sAY4rE4t4

## ERD
![Culturepedia ERD](https://github.com/user-attachments/assets/a3d4997c-6316-47a3-bc2e-502e1eea3bfb)

## Folder Structure
```bash
CULTUREPEDIA
│
├── accounts/              # Handles user authentication and permissions
├── culturepedia/          # Project configuration files (e.g., settings.py)
├── performances/          # Contains features for performance browsing, searching, and recommendations
│   └── bots.py            # Handles interactions with the OpenAI API
│   └── tasks.py           # Scheduler for saving data from the KOPIS API to the local database
├── static/                # Static files (CSS, images, JavaScript, HTML) served to the client for faster loading
│   ├── css/               # Stylesheets that define the look and feel of the website
│   ├── img/               # Performance-related images used across the site
│   ├── js/                # Client-side scripts that handle dynamic interactions on the web pages
├── facility.py            # Stores detailed data about performance venues from the KOPIS API
├── kopis_api_detail.py    # Stores detailed data about specific performances from the KOPIS API
├── kopis_api.py           # Stores performance list data from the KOPIS API
├── db.sqlite3             # SQLite database file
├── .gitignore             # Specifies which files to ignore in version control
├── manage.py              # Django project management script
├── requirements.txt       # List of required Python packages
```

## Trouble Shooting
API DB vs Server DB
: Storing large amounts of performance data locally can put a strain on the server, so it is recommended to query the API DB as it updates in real time.

### API DB
|Issue|Cause|Solution|
|------|---|---|
|Missing data during lookup and search, and server load.|Instead of searching for all performances, only a limited number of performances per page are searched.|Increase the number of performances ( rows) retrieved per page and limit the duration of the performance (start_date, end_date). <br>**Caution : If there are many performances and periods, inquiry and search times can be greatly increased.**|

* Due to the complicated code and traffic problems, it has been changed to store it in a local DB to inquire and retrieve it.

### Server DB
|Issue|Cause|Solution|
|------|---|---|
|Missing results due to performance lookup and search failures|Not all performances are stored, only those within a certain period.|It stores data periodically from the beginning of development, excluding past performance. This mitigates traffic problems when querying and retrieving from API DB.|
|The performance API is in XML format, which raises concerns about storing the data in Django.|It was not a json file format learned while using an existing django.|Use the 'xml toict' module to parse and convert XML into JSON format.|
|Performance details in JSON format are not stored in the DB.|The performance venue is linked via a foreign key in the model.|Fix the upload order so that the venue is saved first, followed by the performance details.|
|As time passes, performance information needs to be updated.|The API DB is always up-to-date, so this issue didn’t arise there.|Initially considered using triggers based on the performance period (start_date, end_date) to update the performance state, but realized that other detailed information might also need updates. Decided to compare the local DB and API DB every midnight for updates using a scheduler and subprocess.|
|Subprocess is not being executed.|Subprocess is referencing a different Python environment.|Specify the Python virtual environment path.|
|Scheduler is being executed multiple times.|No code exists to prevent duplicate executions.|Write code to check if the scheduler is already running.|
|Data is not being updated automatically.|The code that saves performances specifies the date and page, preventing automatic updates.|Modify the code to retrieve all pages starting from the current date using a while loop.|

### Deploy
|Issue|Cause|Solution|
|------|---|---|
|Network error (connection timed out) when attempting to connect to the server.|Subnet issue → Network ACL check → Allow/Deny → Marked as (X) Deny, which caused the problem.|Edit Network ACL settings → Inbound rules → Add new rule → Set to Allow.|

### OPENAI API
|Issue|Cause|Solution|
|------|---|---|
|Sending an image URL to OpenAI sometimes results in successful analysis, and sometimes not.|OpenAI does not seem to recognize the URL properly.| Download and resize the image within the project, then analyze the resized image.|
````
def resizing_images(url_list, quality=85):      # quaility: 70 ~ 90, default: 85
    
    img_folder = os.path.join(settings.STATICFILES_DIRS[0], "img")
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    
    for url in url_list:
        try:
            # Download an image from the URL
            response = requests.get(url)
            response.raise_for_status()  # HTTP 요청 에러 체크

            # Image File Name Extract
            filename = os.path.basename(url)

            # Create a folder by performance.
            folder_name = f"{img_folder}/{filename.split('_')[1]}"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # Open the image in memory.
            im = Image.open(BytesIO(response.content))
            
            # Save Image
            im.save(os.path.join(folder_name, filename), quality=quality)
            
        except Exception as e:
            pass
````
|Issue|Cause|Solution|
|------|---|---|
|An AI was created to extract hashtags using given field values, but the hashtag_list contains unnecessary content in addition to the hashtags.|The gpt-4o-mini model outputs unnecessary messages, causing incorrect behavior.|1. Use the gpt-4o model instead of gpt-4o-mini.<br>Result: When entering the same query, no unnecessary messages are output.<br>Drawback: Relatively more expensive.<br>2. Continue using gpt-4o-mini but modify the query (e.g., "Please provide hashtags." ⇒ "Just provide the hashtags.").<br>Result: Only hashtags are output without any unnecessary messages.|
![image](https://github.com/user-attachments/assets/b2513944-34db-4adc-81a1-4889292a6696)

|Issue|Cause|
|------|---|
|The scheduler runs twice, causing the AI to generate hashtags twice (token waste).|When starting the server using subprocess, two processes are executed simultaneously.|
#### Solution
1. Use jobstores to store scheduler logs in the DB and prevent execution if a scheduler with the same ID already exists.<br>⇒ Duplicate execution occurs, with two IDs being created (failed).
````
scheduler.add_jobstore(jobstores.DjangoJobStore(), "default")  # Save to Django DB
````

2. Set a scheduler execution status flag as a global variable to check execution status and prevent duplicate execution.<br>
⇒ Duplicate execution still occurs (failed).
````
scheduler_running = False  # Adding a Global Variable Flag
start_scheduler():
	scheduler_running = True
````

3. When starting the server using subprocess, two processes (1. performance lookup, reviews, recommendations, etc. / 2. API DB storage, etc.) are running simultaneously, which causes the start_scheduler inside ready to be executed twice.

#### conclusion
Add code to the ready method to prevent duplicate execution.
- Before
````
def ready(self):
	start_scheduler()
````
- After
````
def ready(self):
	if os.environ.get('RUN_MAIN', None) is not None:    # Run scheduler if RUN_MAIN is 'true'
		print(' RUN_MAIN :', os.environ.get('RUN_MAIN', None))
		from .tasks import start_scheduler
		start_scheduler()
````

|Issue|Cause|Solution|
|------|---|---|
|The scheduler is not functioning in the deployment environment.|The code in the deployment environment is blocking the scheduler.|Comment out the conditional statement in the deployment environment and execute it.|
