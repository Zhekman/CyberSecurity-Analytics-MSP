import pandas as pd
import random
from datetime import datetime, timedelta

# Налаштування для солідного об'єму даних
num_employees = 1000
num_events = 60000  # Достатньо для серйозної аналітики
days_history = 180  # Півроку історії

locations = ['Isle of Wight', 'London', 'Southampton', 'Portsmouth', 'Remote']
departments = ['IT', 'Sales', 'Finance', 'Legal', 'HR', 'Operations', 'Marketing']
event_types = ['Failed Login', 'Malware Blocked', 'Unauthorized IP Access', 'Phishing Link Clicked']
severities = ['Low', 'Medium', 'High', 'Critical']

print(f"Починаю генерацію {num_events} записів для {num_employees} працівників...")

# 1. Employees
employees = []
for i in range(1, num_employees + 1):
    employees.append({
        'EmployeeID': i,
        'FullName': f'Employee_{i}',
        'Department': random.choice(departments),
        'Location': random.choice(locations),
        'IsRemote': random.choice([True, False])
    })
df_employees = pd.DataFrame(employees)

# 2. Devices (деякі працівники мають 2 пристрої)
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

# 3. Security Events (Масштабна генерація з логікою)
events = []
device_ids = df_devices['DeviceID'].tolist()
for i in range(1, num_events + 1):
    d_id = random.choice(device_ids)
    e_type = random.choice(event_types)
    
    # Специфічна логіка для цікавих інсайтів:
    # Sales та Marketing частіше клікають на фішинг
    emp_id = df_devices.loc[df_devices['DeviceID'] == d_id, 'EmployeeID'].values[0]
    emp_dept = df_employees.loc[df_employees['EmployeeID'] == emp_id, 'Department'].values[0]
    
    if emp_dept in ['Sales', 'Marketing'] and random.random() > 0.4:
        e_type = 'Phishing Link Clicked'
    
    # "Нічні" атаки (Unauthorized IP) частіше трапляються у вихідні
    timestamp = datetime.now() - timedelta(days=random.randint(0, days_history), 
                                           hours=random.randint(0, 23),
                                           minutes=random.randint(0, 59))
    
    # Більш реалістичний розподіл серйозності подій
    severity = random.choices(severities, weights=[60, 25, 10, 5])[0]
    
    # Логіка блокування: критичні події складніше заблокувати автоматично
    blocked_weights = [95, 5] # Default: 95% blocked
    if severity == 'Critical':
        blocked_weights = [70, 30]
    elif severity == 'High':
        blocked_weights = [85, 15]

    events.append({
        'EventID': 100000 + i,
        'DeviceID': d_id,
        'EventType': e_type,
        'EventSeverity': severity,
        'EventTimestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'IsBlocked': random.choices([True, False], weights=blocked_weights)[0]
    })
    
    if i % 10000 == 0:
        print(f"Згенеровано {i} подій...")

df_events = pd.DataFrame(events)

# 4. MFA Status
mfa = []
services = ['Email', 'Island Cloud', 'VPN', 'Internal HR Portal']
for i in range(1, num_employees + 1):
    dept = df_employees.loc[df_employees['EmployeeID'] == i, 'Department'].values[0]
    for service in services:
        # IT та Finance мають вищий рівень MFA
        if dept in ['IT', 'Finance']:
            mfa_enabled = random.choices([True, False], weights=[98, 2])[0]
        else:
            mfa_enabled = random.choices([True, False], weights=[75, 25])[0]
            
        mfa.append({
            'EmployeeID': i,
            'Service': service,
            'MFA_Enabled': mfa_enabled
        })
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

print(f"\nУспіх! Згенеровано:")
print(f"- {len(df_employees)} працівників")
print(f"- {len(df_devices)} пристроїв")
print(f"- {len(df_events)} подій безпеки")
print(f"Файли готові до аналізу в SQL та Power BI.")
