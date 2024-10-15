## Project name
Culturepedia

## Introduction
It is a platform that allows you to conveniently explore cultural content containing performances of various genres, provides personalized recommendations by analyzing user tastes, and helps you make better choices through in-depth reviews.

## Development Period
- Planning and Documentation: 2024.09.23 ~ 2024.09.27
- Development: 2024.09.27 ~
## Team Roles and Responsibilities
|Team Member|Responsibilities|
|:--|:--|
|김상아|- Implementing user features<br>- reviews, and favorites|
|박현진|- Implementing user features<br>- reviews, and favorites|
|이광욱|- Integrating Kopis API<br>- implementing OpenAI API|
|김채림|- Integrating Kopis API<br>- implementing OpenAI API|


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
- Log in
  - Users can log in using their email and password. Authentication is handled via JWT (JSON Web Token).
- Log Out
  - Users can log out, and their JWT token will be invalidated.
- Profile Edit
  - Users can update their username, password, gender, and birthday.
- Account Deletion
  - Users can delete their account by entering their password. This removes their data from the system.
- Profile View: Users can view their profile details (email, username, gender, birthday) and access their performance viewing history.
  - Viewing History
    - Users can see the performances they have reviewed.
  - Favorites
    - Users can view a list of performances they have marked as favorites.

### Performances
- Browse Performances
  - Users can browse performance rankings by category, sort them by sales or newest, and filter performances by region. Clicking on a performance poster or title takes users to the performance’s detail page.
- Search Performances
  - Users can search performances by keywords (title, actor, venue, production company).
- Performance Details
  - Users can view detailed information about a performance, including the title, start and end dates, venue, cast, crew, runtime, age restrictions, producers, pricing, poster, synopsis, genre, and status.
- Write Reviews
  - Users can write reviews for performances they have attended, including a star rating out of 5.
- Edit Reviews
  - Users can edit reviews they have written.
- Delete Reviews
  - Users can delete reviews they have written.
- Add to Favorites
  - Users can add performances to their favorites list.
- Remove from Favorites
  - Users can remove performances from their favorites list.
- Performance Recommendations
  - Based on the user’s reviews (ratings of 3 stars or higher), favorites, and search tags, the system recommends personalized performances. If there’s insufficient user data, users can manually choose categories, characteristics, moods, and regions for recommendations.



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

### Database (SQLite, MySQL)
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


## Folder Structure
```bash
CULTUREPEDIA
│
├── accounts/              # Handles user authentication and permissions
├── culturepedia/          # Project configuration files (e.g., settings.py)
├── performances/          # Contains features for performance browsing, searching, and recommendations
│   └── bots.py            # Handles interactions with the OpenAI API
│   └── tasks.py           # Scheduler for saving data from the KOPIS API to the local database
├── facility.py            # Stores detailed data about performance venues from the KOPIS API
├── kopis_api_detail.py    # Stores detailed data about specific performances from the KOPIS API
├── kopis_api.py           # Stores performance list data from the KOPIS API
├── db.sqlite3             # SQLite database file
├── .gitignore             # Specifies which files to ignore in version control
├── manage.py              # Django project management script
├── requirements.txt       # List of required Python packages
```

