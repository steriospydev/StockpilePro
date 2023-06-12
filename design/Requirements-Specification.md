## Requirements Specifications:
### Introduction
The Requirements Specifications document outlines the functional and non-functional
requirements of the StockPilePro web application. It serves as a guide for developers,
stakeholders, and testers to ensure that the system meets the specified needs of its users.
This document for our case is an ongoing process.

### User Requirements
- The system shall allow users to create and manage supplier information.
- The system shall allow users to create and manage product information.
- The system shall allow users to create and manage invoice information.
- The system shall provide users with the ability to search and filter supplier
and product information.
- The system shall provide users with the ability to view and print reports based
on supplier, product, and invoice data.
- The system shall provide users with the ability to create and manage storage
and bin information.
- The system shall allow users to create and manage stock information.
- The system shall provide users with the ability to track stock movements and
stock levels in real-time.
- The system shall allow users to perform stock-taking and inventory management
operations.
- The system shall provide users with the ability to set up and receive alerts
when stock levels reach a certain threshold.
    
### Functional Requirements
- User authentication:
> The system shall allow users to create an account, log in, and log out of the system. The 
system shall ensure that user credentials are stored securely and that access to the system is restricted to authorized users only.
- Supplier Management: 
> The system shall allow users to manage suppliers by creating, updating, and deleting supplier information. The 
> system shall ensure that the supplier information is accurate and up-to-date.
- Product Management:
>The system shall allow users to manage products by creating, updating, and deleting product information. The system 
> shall ensure that the product information is accurate and up-to-date.
- Invoice Management: 
> The system shall allow users to create and manage invoices by associating them with suppliers 
  and products. The system shall ensure that invoices are accurate and up-to-date.
- Storage Management:
>The system shall allow users to manage storages and bins by creating, updating, and deleting storage and bin
> information.  The system shall ensure that the storage information is accurate and up-to-date.
- Stock Management: 
> The system shall allow users to manage the stock of products by tracking stock levels and changes.
The system shall ensure that the stock information is accurate and up-to-date.
- Reporting:
>The system shall provide users with the ability to generate reports based on the data stored in the system. The 
> system shall ensure that the reports are accurate, timely, and presented in a clear and understandable manner.

- User Roles and Permissions: 
> The system shall allow administrators to define user roles and permissions. The system 
shall ensure that users are only able to access the features and data that they are authorized to use.
(Not yet implemented)
### Non-functional Requirements
1. Performance - The system should be able to handle a high volume of traffic and respond to user requests quickly and 
efficiently.
2. Scalability - The system should be designed to scale horizontally as the number of users and data stored in the 
   system grows.
3. Security - The system should be secure and protect user data from unauthorized access or breaches.
4. Usability - The system should be easy to use and navigate, with a clear and intuitive interface for users.
5. Availability - The system should have high availability and be accessible to users at all times, with minimal 
   downtime for maintenance or upgrades.
6. Compatibility - The system should be compatible with various devices, operating systems, and web browsers used by 
   its users.
7. Reliability - The system should be reliable and perform consistently under normal and peak usage conditions.
8. Maintainability - The system should be designed and coded in a way that makes it easy to maintain, update, and 
   enhance over time.
9. Compliance - The system should comply with relevant laws and regulations, including data privacy and security laws.
10. Integration - The system should be able to integrate with other systems and services used by its users or 
   stakeholders.

### Use Cases
### Acceptance Criteria

### System Constraints:

- Hardware Requirements:
> The StockPilePro web application requires a minimum of 2 GB RAM and 2 CPU cores to operate effectively. 
> Additionally, the system must have a minimum of 10 GB of available storage space for storing application data, user files, and system logs.

- Software Requirements:
>The system is built using Django web framework and requires Python version 3.9 or higher. Other software 
 requirements include PostgreSQL 13 or higher, matplotlib 3.7.1, and NumPy 1.24.2.
 The application is designed to run on a Linux operating system.

- Network Requirements:
> The system requires a stable internet connection with a minimum bandwidth of 10 Mbps. The application uses 
> HTTP/HTTPS protocols to communicate with clients and third-party services, and requires access to ports 80 and 443.

- Security Requirements:
> The system must comply with the OWASP Top Ten security guidelines and ensure the confidentiality, integrity, and 
> availability of user data. All communication between the application and clients must be encrypted using SSL/TLS protocols, and the system must implement strong authentication and access control mechanisms.

- Regulatory Requirements:
> The system must comply with all applicable data protection regulations, including GDPR and CCPA. The application 
> must provide users with the ability to control their personal data, including the right to access, rectify, and erase their data.

- Constraints and Assumptions:
 - The StockPilePro web application assumes that users have a basic understanding of web browsing and data management. 
 - The system assumes that users will access the application through modern web browsers such as Chrome, Firefox, or 
   Safari .
 - The system constraints include a minimum of two hours of scheduled maintenance per month, during which the 
   application may be unavailable.
 - The maximum number of suppliers that can be stored in the database is 1296 (36^2).
 - The maximum number of products that can be stored is 46,656 (36^3).
 - The maximum number of stock items that can be stored for each product-supplier pair is 46,656 (36^3).
