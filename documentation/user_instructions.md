# User instructions

There are two key roles in the Appointment System, "User" and "Admin". These can be also regarded as "Customer" and "Employee". Within these roles, the visibility of certain functions are restricted. For unregistered user, the site does not offer any functions other than signing up or logging in. After signing up, you will have the rights of an user. As of now, the only way to become an admin is through contacting database administrator. Few accounts with admin rights have been politely added to the project description which you can find [here](https://github.com/tommise/AppointmentSystem/blob/master/README.md).

## As an user:

1. Create an account by clicking the "Sign up" from the top right corner and provide name, username and a chosen password.
2. Log in with your credentials.
3. As an user, you are able to do following functions:

##### From the "My appointments" dropdown menu:
- "Reserve an appointment"
You will be provided a list of free appointment times and a corresponding employee related to it. Pick a desired service from the dropdown menu and press "Reserve".
- "List my appointments"
Once you have reserved an appointment, you can view your appointments from "List my appointments". You will be provided an information about the starting time, employee, service and price related to the appointment. If you have not reserved an appointment, the list will be empty.
- "Cancel an appointment"
You will be provided with a list of your appointments and their details, you can cancel an appointment by clicking "Cancel" at the end of the details.

You are also able to log out from the site by clicking "Log out" from the right top corner.

## As an admin:

1. Log in with your account from the right top corner with pre-assigned credentials.
2. Now you are able to do following functions:

##### From the "My appointments" dropdown menu:
- "Add an appointment"
Provide a free appointment time and click "Add a new appointment". You will be assigned to the created appointment time by default.
- "List all appointments"
From this view, you can see all appointments: their starting time, employee, reserved status and if an appointment is made by customer, the name of the customer, service type and price.
- "Remove an appointment"
You are authorized to remove your own appointment by clicking "Remove".
- "Update an appointment"
You can modify the date and starting time, assign a new employee or unreserve an appointment of your own.
- "List my appointments"
You will be provided a list of your appointments, their status and additional information related to them.

##### From the "Services" dropdown menu:
- "Add an service"
You can add a new service to the site by providing the name and price of desired service.
- "List all services"
You will be provided with a list of all services provided
- "Remove a service"
You have the right to remove a service.
- "Update a service"
You can update a name or the price of the service by providing desired new name or price to their corresponding fields and pressing "Update".

##### From the "Statistics" dropdown menu:
- "List all users without an reservation"
You will be provided a list of users with name and username details who do not currently have an appointment reserved.
- "List most popular services"
You can view a list of the most popular services provided ordered in ascending order by their frequency.
