## Introduction: 
This document describes the architecture of a web application built using Django,
PostgresSQL, and Bulma. The application is designed to provide users with a simple
and efficient way to manage their inventory and stock levels. This document provides
a detailed overview of the system architecture, including its major components, data
and application architecture, deployment, security, and scalability considerations.

## System Components
#### Server:
The server component is responsible for handling incoming requests from clients 
and generating responses. It uses the Django framework to provide the necessary
middleware, routing, and other functionality required to manage client-server interactions.
#### Database:
The database component is responsible for storing and managing the application's data. It uses
PostgresSQL as the database management system to store data related to suppliers, products,
invoices, storehouses, and stock items.
#### Frontend: 
The web application's frontend is built with the Bulma CSS framework, which provides responsive and visually appealing UI elements to users. The framework offers a range of pre-built components, such as navigation bars, buttons, forms, and tables, which can be customized using CSS classes. In addition, the frontend uses Jinja rendering capabilities, which enable the dynamic generation of HTML pages based on data from the backend. Jinja is a templating language that allows for the insertion of variables, loops, conditionals, and other logic into HTML templates, making it easy to create dynamic and reusable page layouts.
.
#### Apps
1) Supplier App - The supplier app component is responsible for managing supplier-related functionality within the 
system. It provides CRUD operations on supplier information, including name, contact information, and other relevant data.

2) Product App - The product app component is responsible for managing product-related functionality within the 
system. It provides CRUD operations on product information, including product name, description, and other
relevant data. It will follow 3NF principles to maintain data integrity.
3) Invoice App - The invoice app component is responsible for managing the creation and management of invoices
within the system. It provides CRUD operations on invoice information and has a foreign key relation to the
supplier app. It also has an InvoiceItem model that holds the information for a product derived from the product
app.
4) Storehouse App - The storehouse app component is responsible for managing storage-related functionality within the 
   system. It provides CRUD operations on storage and bin information and handles various storage operations. It creates a stock item when an InvoiceItem is saved.
5) BPanel App - The bpanel app is responsible for generating reports based on data stored in the database.
It contains views to filter, group, and visualize data in HTML. The app uses Matplotlib and Seaborn to generate graphs, 
which can be embedded into HTML pages. Both are data visualization libraries that provides a range of
chart types, such as line charts, bar charts, scatter plots, and histograms.
The library offers a wide range of customization options, such as color schemes, axis labels, legends,
and annotations, which allow for the creation of professional-looking graphs.
The BPanel app is also responsible for the index.html page, which serves as the main entry point to the web
application. The index page provides a simple message board where users can leave announcements. 

## Data Architecture:
The data architecture of the StockPilePro web application is built around a
relational database management system, PostgreSQL. The system uses a schema-based
approach to organizing data, with each app in the Django project having its own set
of models, and each model corresponding to a table in the database. The data model
is designed to support the following functionalities: 
- supplier management
- product management
- invoice management
- storage management.

The schema consists of these main tables: 
- Abstract Tables:
  - TimeStamp
  - CategoryTempValues
  - BinType
- DTask 
- Supplier
- Product
  - Category
  - SubCategory
  - Material
  - Package
  - Tax
- Invoice and InvoiceItem,
- Storage
- Section
- Spot
- Bin
- Stock
- PlaceStock

The TimeStamp table holds information about the time that an object is created and updated. Most of the models 
inherit from it

The CategoryTempValues exists only to hold information about colours, size and icons used when categories is rendered
in the frontend and is marked for future refactoring (or deletion) since it is a security risk.

The BinType describes the type of Bin which is either Floor or Shelf.

The Dtask table handles the information around the announcement functionality in the index page(user,message, status).

The Supplier table holds information about the company's address, contact and tax information as well as the 2-digit 
identifier used in SKU .

The Product table contains details about the products in the inventory, including name, SKU, packaging,categories, 
tax rate, and description.

The Invoice table represents an invoice issued by a supplier, and it contains a foreign key reference to the 
Supplier table. The InvoiceItem table is a pivot table that represents the line items on an invoice, and it contains foreign key
references to both the Invoice and Product tables.

The Storage, Section, Spot and Bin are tables used to identify places that stocks can be placed. The Bin table is 
being constructed by the other 3 tables with FK relation. 

The Stock table holds information about the InvoiceItem's price and quantity.When a new Stock object to be created
a unique SKU is created based on the suppliers' and product's SKU parts.Contains one-to-one relation with InvoiceItem.

The PlaceStock table hold information about how much of a Stock's quantity is stored and where, giving us the option
to place a product to more than one Bin.It is connected to the Stock with FK relationship 


The system's database is managed using Django's ORM, which provides a high-level abstraction layer over the underlying database.
The ORM allows for the creation, deletion, querying, and updating of data using Python code, without having to write SQL queries
directly. Additionally, the ORM includes a set of tools for managing database migrations, which allows for the easy evolution
of the database schema over time as the application changes.

### SKU
The process of generating a new SKU number in the StockPilePro system is crucial for efficient inventory management.
The SKU number is a unique identifier assigned to each Stock that is added to the system.
The SKU number is composed of two alphanumerical digits unique to each supplier, followed by three alphanumerical 
digits unique to each product, and three alphanumerical digits generated when a new Stock object is created.

To generate a new SKU number, the system first checks if the supplier and product already exist in the database. 
If the supplier does not exist, a new supplier object is created, and a unique two-digit alphanumeric identifier is assigned.
If the product does not exist, a new product object is created, and a unique three-digit alphanumeric identifier is assigned.

Once the supplier and product have been identified, a new Stock object is created with a three-digit alphanumeric identifier.
This identifier is appended to the end of the supplier and product identifiers where the uniqueness of the full 
SKU is being checked. The SKU number is then stored in the Stock object and used to track the product in the system.

The unique nature of the SKU number ensures that each product is easily identifiable and trackable in the system,
making inventory management more efficient and accurate.

## Application Architecture
StockPilePro is a web application built with Django, a high-level Python web framework that promotes rapid development
and clean, pragmatic design. It uses PostgresSQL as its relational database management system to store all the data.
The application also uses Bulma, a free, open-source CSS framework based on Flexbox, to provide a responsive and visually 
appealing user interface to the users.Additionally, the app utilizes various Python libraries, including coverage,
Django-extensions, django-import-export, django-debug-toolbar, factory-boy, Faker, MarkupPy, matplotlib, mixer, numpy, 
packaging, pandas, Pillow, psycopg2-binary, pydotplus, python-dotenv, and seaborn.

The backend of the application is designed using the Model-View-Controller (MVC) architecture, which separates the application
logic into three interconnected components: the data model, the user interface, and the control flow. The data model defines
the structure and relationships of the data stored in the database, while the user interface provides a way for the user to 
interact with the application. The control flow manages the communication between the data model and the user interface.

The application's frontend is designed using the Jinja template engine, which is integrated with Django, to render dynamic
HTML pages based on the data stored in the database. Additionally, the BPanel app component is responsible for generating 
reports based on data stored in the database, and it provides functionality to filter, group, and visualize data in HTML.

The Django Rest Framework can be used to create a well-documented API that can be used by other applications. The application
can also be extended to integrate with third-party APIs, such as payment gateways or shipping providers, to provide additional
functionality to users.





## Conclusion
A summary of the key points covered in the system architecture document and any additional 
recommendations or considerations for the system.
