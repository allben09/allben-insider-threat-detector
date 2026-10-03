"""
src/data_generator.py
Insider Threat Detector - Behavioural Data Generator

Simulates 90 days of realistic employee activity across multiple users,
including normal behaviour and injected insider-threat scenarios.

Author: Allben Rakgoale
"""

import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_ZA")
Faker.seed(42)
random.seed(42)
np.random.seed(42)


# Departments and their sensitivity levels
DEPARTMENTS = {
    "IT": 1.0,
    "Finance": 1.2,
    "HR": 1.1,
    "Sales": 0.8,
    "Marketing": 0.7,
    "Engineering": 1.0,
    "Customer Support": 0.9,
    "Executive": 1.5,
}

# Suspicious activity profile (used for injected insider threats)
THREAT_PROFILES = [
    "data_exfiltration",
    "privilege_escalation",
    "off_hours_access",
    "usb_abuse",
]


def generate_employee(user_id: int) -> dict:
    """Generate a single employee profile."""
    department = random.choice(list(DEPARTMENTS.keys()))
    return {
        "user_id": f"EMP{user_id:04d}",
        "name": fake.name(),
        "department": department,
        "sensitivity_weight": DEPARTMENTS[department],
        "is_threat": False,
    }


def generate_normal_activity(employee: dict, n_days: int = 90) -> list:
    """Generate 90 days of normal behaviour for an employee."""
    records = []
    today = datetime.now()

    for day_offset in range(n_days):
        date = today - timedelta(days=day_offset)

        # Weekends: much lower activity
        is_weekend = date.weekday() >= 5

        if is_weekend and random.random() > 0.15:
            continue

        # Normal work hours: 8am - 6pm
        login_hour = random.gauss(9.5, 1.0)
        login_hour = max(6, min(19, login_hour))
        logout_hour = login_hour + random.gauss(8, 1.0)

        # Normal data transfer: 50 - 500 MB
        data_transferred_mb = max(10, random.gauss(200, 80))

        # Normal file access: 20 - 100 files
        files_accessed = max(5, int(random.gauss(60, 20)))

        # Failed logins: usually 0-2
        failed_logins = max(0, int(random.gauss(0.5, 0.8)))

        # USB usage: rare (10% of days)
        usb_events = 1 if random.random() < 0.1 else 0

        # Sensitive file access (weighted by department)
        sensitive_access = int(
            files_accessed * 0.05 * employee["sensitivity_weight"]
            + random.gauss(0, 2)
        )
        sensitive_access = max(0, sensitive_access)

        records.append({
            "user_id": employee["user_id"],
            "name": employee["name"],
            "department": employee["department"],
            "date": date.date(),
            "login_hour": round(login_hour, 2),
            "logout_hour": round(logout_hour, 2),
            "session_hours": round(logout_hour - login_hour, 2),
            "data_transferred_mb": round(data_transferred_mb, 2),
            "files_accessed": files_accessed,
            "failed_logins": failed_logins,
            "usb_events": usb_events,
            "sensitive_access": sensitive_access,
            "is_threat": False,
        })

    return records


def inject_threat(employee: dict, activity: list, profile: str) -> list:
    """Modify an employee's activity to simulate a threat profile."""
    employee["is_threat"] = True
    modified = [dict(r) for r in activity]

    # Affect the last 14 days (recent behaviour)
    recent = modified[-14:] if len(modified) >= 14 else modified

    for record in recent:
        if profile == "data_exfiltration":
            # Massive spike in data transfer
            record["data_transferred_mb"] *= random.uniform(5, 15)
            record["sensitive_access"] = int(record["sensitive_access"] * 3 + 20)

        elif profile == "privilege_escalation":
            # Accessing many sensitive files
            record["sensitive_access"] = int(record["sensitive_access"] * 4 + 30)
            record["files_accessed"] = int(record["files_accessed"] * 1.8)

        elif profile == "off_hours_access":
            # Working at 1am - 5am
            record["login_hour"] = random.uniform(1, 5)
            record["logout_hour"] = record["login_hour"] + random.uniform(2, 5)
            record["session_hours"] = round(
                record["logout_hour"] - record["login_hour"], 2
            )

        elif profile == "usb_abuse":
            # Constant USB usage
            record["usb_events"] = random.randint(3, 10)
            record["data_transferred_mb"] *= random.uniform(2, 5)

        record["is_threat"] = True

    return modified


def generate_dataset(n_employees: int = 50, threat_ratio: float = 0.1) -> pd.DataFrame:
    """
    Generate the full dataset.

    Args:
        n_employees: Total number of employees to simulate
        threat_ratio: Proportion of employees who are insider threats

    Returns:
        DataFrame with all activity records
    """
    n_threats = max(1, int(n_employees * threat_ratio))
    all_records = []

    for i in range(1, n_employees + 1):
        employee = generate_employee(i)
        activity = generate_normal_activity(employee)

        # Inject threat for selected employees
        if i <= n_threats:
            profile = random.choice(THREAT_PROFILES)
            activity = inject_threat(employee, activity, profile)

        all_records.extend(activity)

    df = pd.DataFrame(all_records)
    df["date"] = pd.to_datetime(df["date"])
    return df


if __name__ == "__main__":
    print("🔍 Generating insider threat dataset...")
    df = generate_dataset(n_employees=50, threat_ratio=0.1)
    df.to_csv("data/employee_activity.csv", index=False)
    print(f"✅ Generated {len(df):,} records for {df['user_id'].nunique()} employees")
    print(f"🚨 Threat users: {df[df['is_threat']]['user_id'].nunique()}")
