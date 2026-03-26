import pandas as pd
import random
from datetime import datetime, timedelta

# Налаштування для солідного об'єму даних
num_employees = 1000
num_events = 60000  # Достатньо для серйозної аналітики

# Налаштування періоду
start_date = datetime(2025, 9, 1)
end_date = datetime(2026, 3, 31, 23, 59, 59)
total_seconds = int((end_date - start_date).total_seconds())

locations = ['Isle of Wight', 'London', 'Southampton', 'Portsmouth', 'Remote']
departments = ['IT', 'Sales', 'Finance', 'Legal', 'HR', 'Operations', 'Marketing']
event_types = ['Failed Login', 'Malware Blocked', 'Unauthorized IP Access', 'Phishing Link Clicked']
severities = ['Low', 'Medium', 'High', 'Critical']

print(f"Починаю генерацію {num_events} записів для {num_employees} працівників за період з {start_date.date()} по {end_date.date()}...")

# Списки для реалістичних імен
first_names = ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth', 
               'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Christopher', 'Karen', 
               'Charles', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 
               'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 
              'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 
              'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 
              'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts']

# 1. Employees
employees = []
used_names = set()
for i in range(1, num_employees + 1):
    while True:
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        short_name = f"{fn}_{ln[:3]}"
        if short_name not in used_names:
            used_names.add(short_name)
            break
        else:
            short_name = f"{fn}_{ln[:3]}_{i}"
            used_names.add(short_name)
            break

    employees.append({
        'EmployeeID': i,
        'FullName': short_name,
        'Department': random.choice(departments),
        'Location': random.choice(locations),
        'IsRemote': random.choice([True, False])
    })
df_employees = pd.DataFrame(employees)

# 2. Devices
devices = []
device_id_counter = 1001
for i in range(1, num_employees + 1):
    num_devs = random.choices([1, 2], weights=[80, 20])[0]
    for _ in range(num_devs):
        os_ver = random.choices(['Windows 11', 'Windows 10', 'macOS Sonoma', 'Linux'], weights=[50, 35, 10, 5])[0]
        devices.append({
            'DeviceID': device_id_counter,
            'EmployeeID': i,
            'DeviceType': random.choice(['Laptop', 'Desktop', 'Workstation']),
            'OS_Version': os_ver,
            'LastPatchDate': (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
            'AntivirusStatus': random.choices(['Active', 'Outdated', 'Disabled'], weights=[90, 7, 3])[0]
        })
        device_id_counter += 1
df_devices = pd.DataFrame(devices)

# 3. Security Events
events = []
device_ids = df_devices['DeviceID'].tolist()
for i in range(1, num_events + 1):
    d_id = random.choice(device_ids)
    e_type = random.choice(event_types)
    emp_id = df_devices.loc[df_devices['DeviceID'] == d_id, 'EmployeeID'].values[0]
    emp_dept = df_employees.loc[df_employees['EmployeeID'] == emp_id, 'Department'].values[0]
    
    if emp_dept in ['Sales', 'Marketing'] and random.random() > 0.4:
        e_type = 'Phishing Link Clicked'
    
    # Рівномірний розподіл у періоді
    random_seconds = random.randint(0, total_seconds)
    timestamp = start_date + timedelta(seconds=random_seconds)
    
    severity = random.choices(severities, weights=[60, 25, 10, 5])[0]
    blocked_weights = [95, 5]
    if severity == 'Critical': blocked_weights = [70, 30]
    elif severity == 'High': blocked_weights = [85, 15]

    events.append({
        'EventID': 100000 + i,
        'DeviceID': d_id,
        'EventType': e_type,
        'EventSeverity': severity,
        'EventTimestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'IsBlocked': random.choices([True, False], weights=blocked_weights)[0]
    })
    
    if i % 10000 == 0: print(f"Згенеровано {i} подій...")

df_events = pd.DataFrame(events)

# 4. MFA Status
mfa = []
services = ['Email', 'Island Cloud', 'VPN', 'Internal HR Portal']
for i in range(1, num_employees + 1):
    dept = df_employees.loc[df_employees['EmployeeID'] == i, 'Department'].values[0]
    for service in services:
        mfa_enabled = random.choices([True, False], weights=[98, 2])[0] if dept in ['IT', 'Finance'] else random.choices([True, False], weights=[75, 25])[0]
        mfa.append({'EmployeeID': i, 'Service': service, 'MFA_Enabled': mfa_enabled})
df_mfa = pd.DataFrame(mfa)

# 5. Training Logs
training = []
for i in range(1, num_employees + 1):
    status = random.choices(['Completed', 'In Progress', 'Overdue'], weights=[75, 15, 10])[0]
    training.append({
        'LogID': 900000 + i,
        'EmployeeID': i,
        'CourseName': 'Cyber Security Essentials 2024',
        'Status': status,
        'CompletionDate': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') if status == 'Completed' else None
    })
df_training = pd.DataFrame(training)

# Збереження
print("Зберігаю файли...")
df_employees.to_csv('employees.csv', index=False)
df_devices.to_csv('devices.csv', index=False)
df_events.to_csv('security_events.csv', index=False)
df_mfa.to_csv('mfa_status.csv', index=False)
df_training.to_csv('training_logs.csv', index=False)
print("Успіх!")
