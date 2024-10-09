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
- Database: SQLite, MySQL
- Version Control: Git, GitHub
- IDE: PyCharm, VSCode
- APIs Used: KOPIS API (Korea Performance Information System), OpenAI API
- Other Tools and Libraries:
  - python3.10
  - django==4.2
  - djangorestframework==3.15.2
  - djangorestframework-simplejwt==5.3.1

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
- Search Performances
- Performance Details
- Write Reviews
- Edit Reviews
- Delete Reviews
- Add to Favorites
- Add to Favorites
- Remove from Favorites
- Performance Recommendations


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
