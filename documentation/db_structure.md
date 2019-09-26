## CREATE TABLE statements for the database

### Account

```
CREATE TABLE account (
	id INTEGER NOT NULL, 
	name VARCHAR(144) NOT NULL, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	employee BOOLEAN NOT NULL, 
	PRIMARY KEY (id)
)
```

### Appointment

```
CREATE TABLE appointment (
	id INTEGER NOT NULL, 
	start_time DATETIME, 
	reserved BOOLEAN NOT NULL, 
	PRIMARY KEY (id)
)
```

### Service

```
CREATE TABLE service (
	id INTEGER NOT NULL, 
	service VARCHAR(144) NOT NULL, 
	price INTEGER NOT NULL, 
	PRIMARY KEY (id)
)
```

### Accountappointment

```
CREATE TABLE accountappointment (
	account_id INTEGER, 
	appointment_id INTEGER, 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(appointment_id) REFERENCES appointment (id)
)
```

### Serviceappointment

```
CREATE TABLE serviceappointment (
	service_id INTEGER, 
	appointment_id INTEGER, 
	FOREIGN KEY(service_id) REFERENCES service (id), 
	FOREIGN KEY(appointment_id) REFERENCES appointment (id)
)
```