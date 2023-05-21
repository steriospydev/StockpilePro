# StockPilePro


## Brief Summary
StockPilePro is a web application built with Django and PostgreSQL that enables
users to manage their suppliers, invoices, stocks, and products. 
By automating the creation of Stock Keeping Units (SKUs) when new invoices are
generated, the app streamlines inventory management and simplifies the tracking 
of stock levels. Additionally, the app performs various storage operations,
providing users with the ability to move products between different storage
facilities and track their location in real-time. However, it is worth noting that not all functional requirements have yet been met, and there is still room for improvement in terms of performance and scalability.
 
# Installation

To install StockPilePro, follow these steps:

- Clone the repository:
  - git clone https://github.com/steriospydev/StockPilePro.git
- Install PostgreSQL:

  - You can download and install PostgreSQL from the official website or by using a package manager on your operating system.

- Create a PostgreSQL user and database:

  - Open a terminal or command prompt and type <code>sudo -u postgres psql </code>to log in to the PostgreSQL shell.
  - Create a user with a password and a database
    -  <code>psql</code>
    -  <code>CREATE DATABASE myproject;</code>
    -  <code>CREATE USER myprojectuser WITH PASSWORD 'password';</code>
    -  <code>ALTER ROLE myprojectuser SET client_encoding TO 'utf8';</code>
    -  <code>ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';</code>
    -  <code>ALTER ROLE myprojectuser SET timezone TO 'UTC';</code>
    - <code> GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;</code>
   
- Create a .env file with your PostgreSQL database credentials(refer to .env.example)
- Create a virtual environment: <code>python3 -m venv env</code>
- Activate the virtual environment: <code>source env/bin/activate</code>
- Install the required packages: <code>pip install -r requirements.txt</code>
- Run: <code>python manage.py makemigrations</code>
- Run: <code>python manage.py mymigrations</code>
- Run migrations:<code> python manage.py migrate</code>
- Load sample data:<code> python manage.py loaddata start_data/data.json</code>
- Create a superuser:<code> python manage.py createsuperuser</code>
- Start the development server:<code> python manage.py runserver</code>

## See also
- [System Architecture](/docs/System-Architecture.md)
- [Requirements Specification](/docs/Requirements-Specification.md)
- [Model Dependency](/docs/model_dependency.png)

## Why is this app created?
StockpilePro, an impressive Django, PostgreSQL, and Bulma application, originated from a local businessman's challenge. As his business expanded rapidly, he lacked an efficient system to handle invoices, stocks, and orders. Although I referred him to a seasoned professional for guidance, I was inspired by our conversations to create an app for my portfolio. Thus, StockpilePro was born. This comprehensive application enables users to store information about products, manage suppliers, handle invoices, and seamlessly organize stock items within multiple storage facilities. With StockpilePro, businesses can efficiently track inventory and streamline their operations.

The whole process was a valuable experience for me as a developer. It gave me the opportunity to work on a real-world 
project and 
gain practical skills that I could apply in future endeavors. Overall, I learned the importance of listening to the needs of the business and creating solutions that could address their specific challenges.

# Structure
The project consists of 6 apps with their own model-view-template structure:
- accounts
    - responsible for register/login contains the login form and template for now
- bpanel
    - responsible  for creating aggregate results and reports...eventually. 
    - A subpackage called graphs 
     that contains the functions that the views use to return graphs using matplotlib and seaborn
     
- invoice
    - Handles the creation and managing of invoices
- product
  - responsible for managing all info related to a product
- storehouse
  - The primary focus of the app is the management of storage, bins, and related operations 
- supplier
  - Manage suppliers

# Next steps in the project
Moving forward with the project, there are several key steps that need to be taken to improve
the app's functionality and user experience. First and foremost, the codebase needs to be
refactored and any existing bugs need to be fixed. This will not only improve the app's 
performance and stability but also make it easier to maintain and update in the future.

Another crucial step is to decouple the backend and create a well-documented API using Django
REST Framework (DRF). This will allow other developers to easily integrate the app's 
functionality into their own projects and ensure that the app can be scaled up in the future.
By breaking down the app's architecture into smaller, more manageable components,
it will also be easier to test and debug any issues that may arise.

When it comes to the frontend, a different technology will be used instead of Bulma(../).
React, Angular, or Vue are all potential options to consider, depending on the app's specific
needs. This will provide a more modern and flexible user interface that can be easily 
customized and updated over time.


Overall, by taking these next steps in the project, the app will be well-positioned to meet 
the growing needs of a small to medium establishments and potentially attract other businesses in 
need of inventory management solutions. The well-documented API and modern frontend will make
the app more accessible and easier to use, while the decoupled architecture will allow for 
greater scalability and flexibility.
