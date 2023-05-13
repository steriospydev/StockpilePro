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
    - <code>CREATE USER your_username WITH PASSWORD 'your_password';</code>
    - <code>CREATE DATABASE your_db_name OWNER your_username ENCODING 'UTF8';</code>
    - <code>GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_username;</code>

- Modify the .env file with your PostgreSQL database credentials:

  - DB_NAME=your_db_name
  - DB_USER=your_username
  - DB_PASSWORD=your_password
  - DB_HOST=localhost
  - DB_PORT=5432

- Create a virtual environment:
  <code>python3 -m venv env</code>
- Activate the virtual environment:
  <code>source env/bin/activate</code>
- Install the required packages:
  <code>pip install -r requirements.txt</code>
- Run: <code>python manage.py makemigrations</code>
- Run migrations:<code> python manage.py migrate</code>
- Create a superuser:<code> python manage.py createsuperuser</code>
- Start the development server:<code> python manage.py runserver</code>

## See also
- [System Architecture](/docs/System-Architecture.md)
- [Requirements Specification](/docs/Requirements-Specification.md)
- [Model Dependency](/docs/model_dependency.png)

## Why is this app created?
This app was created to address the growing needs of a local establishment that was expanding rapidly.
Within the span of a year, the business had grown from a two-person operation to a team of over 10
people, with multiple storage facilities to manage. However, with growth came new challenges,
and the primary concern was how to efficiently manage and keep track of the stock.

Despite urging and convincing the local establishment to use a proprietary software to manage their 
inventory, I was determined to create an app for my portfolio that could address their needs.
The business was expanding quickly, and they were in dire need of a system that could help them 
efficiently manage their stock levels across multiple storage facilities.

I understood the challenges they faced and recognized the potential benefits of
a custom app tailored to their specific needs. So, I took on the project and developed an app that
would streamline their inventory management process. The app would also allow them to track their
inventory in real-time, keep track of their stock levels and provide valuable insights 
on which items were selling well and which ones needed to be restocked. This would not only save time
and resources but would also ensure that they always had the right products available for their customers.

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
