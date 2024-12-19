# ZEROIN

**MODERN APPLICATION DEVELOPMENT-1: SPONSOR-INFLUENCER FLASK APP**

### INFLUENCER ENGAGEMENT AND SPONSORSHIP COORDINATION PLATFORM
A platform to connect Sponsors and Influencers, enabling sponsors to advertise their products/services while influencers gain monetary benefits.

- The project is built using Flask as the backend framework.
- The platform handles different roles (admin, sponsor, influencer) using role-based access control.
- CRUD operations are implemented for managing users, campaigns, and other entities.
- The frontend is designed to be responsive and user-friendly using Bootstrap.
- Additional functionalities include flagging users, searching/filtering options, and stats charts.

### Frameworks and Libraries Used
1. **Flask Framework**
   - `Flask`: The main web framework used to create the application.
   - `flask_login`: Provides user session management.
   - `flask_sqlalchemy`: Used for database management, providing an ORM for interacting with the database.
   - `flask_wtf`: Simplifies form creation and handling in Flask using the WTForms library.

2. **WTForms**
   - `WTForms`: Used to create and validate forms, making it easy to handle form data.
   - `flask_wtf`: Integrates WTForms with Flask, providing additional features for form handling.

3. **SQLAlchemy**
   - `SQLAlchemy`: An ORM that allows for the creation and management of database models in Python.
   - `flask_sqlalchemy`: A Flask extension that adds SQLAlchemy support to the application.

4. **Bcrypt**
   - `bcrypt`: Used to hash passwords before storing them in the database, ensuring user data security.

5. **Datetime**
   - `datetime`: A Python module used to manage date and time-related data, such as timestamps for user creation, etc.

6. **SQLite**
   - A lightweight, file-based database system used as the backend database for the project. It's simple to set up and doesn't require a separate server process.

7. **Collections**
   - Used for organizing and managing collections of data within the application.

8. **Chart.js**
   - Used to create interactive and visually appealing charts for displaying data on the frontend.

9. **Bootstrap**
   - Used for responsive design and styling of the frontend.

### API Resource Endpoints
1. **Home and About**
   - `GET /` or `GET /home`: Renders the home page.
   - `GET /about`: Renders the about page.

2. **User Registration and Authentication**
   - `GET /register`: Renders the general registration page.
   - `GET/POST /register/sponsor`: Registers a sponsor.
   - `GET/POST /register/influencer`: Registers an influencer.
   - `GET/POST /login`: Authenticates a user and logs them in.
   - `GET /logout`: Logs the user out.

3. **Profile Management**
   - `GET/POST /profile`: Displays and updates the profile information for the current user.

4. **Dashboard Redirection**
   - `GET /dashboard`: Redirects the user to their respective dashboard based on their role.

5. **Admin Dashboard and Management**
   - `GET /admin`: Admin dashboard showing campaigns.
   - `GET /admin/info`: Provides detailed information about the platform statistics.
   - `GET /admin/search`: Allows admin to search for influencers, sponsors, or campaigns.
   - `POST /flag_entry/<int:entry_id>`: Flags an entry (influencer, sponsor, or campaign).
   - `GET /flagged_users`: Lists all flagged users (influencers, sponsors, campaigns).
   - `GET /remove_flag/<int:entry_id>/<string:filter>`: Removes the flag from a specific entry.
   - `GET /admin/chart`: Showcasing Sponsor and Influencer registration per day.

6. **Sponsor Functionality**
   - `GET /sponsor`: Sponsor dashboard.
   - `GET/POST /sponsor/campaign/new`: Creates a new campaign for the sponsor.
   - `GET/POST /sponsor/campaign/manage`: Manages the sponsor's campaigns.
   - `GET/POST /sponsor/campaign/<int:campaign_id>/update`: Updates an existing campaign.
   - `POST /sponsor/campaign/<int:campaign_id>/delete`: Deletes a campaign.
   - `GET/POST /sponsor/ad_request/new`: Creates a new ad request.
   - `GET /sponsor/ad_requests`: Displays the sponsor's ad requests.
   - `GET/POST /sponsor/ad_request/<int:ad_request_id>/update`: Updates an existing ad request.
   - `POST /sponsor/ad_request/<int:ad_request_id>/delete`: Deletes an ad request.
   - `GET/POST /sponsor/ad_request/<int:ad_request_id>/negotiate`: Negotiates the payment amount for an ad request.
   - `GET/POST /sponsor/search_influencers`: Searches for influencers.

7. **Influencer Functionality**
   - `GET /influencer`: Influencer dashboard.
   - `GET/POST /influencer/search_campaigns`: Searches for campaigns.
   - `GET /influencer/ad_requests`: Displays pending ad requests for the influencer.
   - `GET /influencer/ad_request/<int:ad_request_id>/accept`: Accepts an ad request.
   - `GET /influencer/ad_request/<int:ad_request_id>/reject`: Rejects an ad request.
   - `GET/POST /influencer/ad_request/<int:ad_request_id>/negotiate`: Negotiates the payment amount for an ad request.
   - `GET /influencer/accepted_ad_requests`: Displays accepted ad requests for the influencer.
