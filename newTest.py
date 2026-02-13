import pandas as pd
import re

file_path = "VotedList4.csv"
emp = "Emp and Training Details.xlsx"

# Read files
df = pd.read_csv(file_path)
df2 = pd.read_excel(emp)

df.columns = df.columns.str.strip()
df2.columns = df2.columns.str.strip()

# -----------------------------
# Clean & Extract First + Last
# -----------------------------
def extract_first_last(name):
    name = str(name).lower().strip()
    name = re.sub(r"\(.*?\)", "", name)  # remove brackets
    parts = name.split()

    if len(parts) >= 2:
        return parts[0] + " " + parts[-1]
    elif len(parts) == 1:
        return parts[0]
    return ""

df["Name_key"] = df["Name"].apply(extract_first_last)
df2["Emp_key"] = df2["Employee Name"].apply(extract_first_last)

# Normalize response column
df["Please confirm your availability for the Team Event on 27th and 28th March"] = df["Please confirm your availability for the Team Event on 27th and 28th March"].astype(str).str.strip().str.upper()

# -----------------------------
# YES and NO voters
# -----------------------------
yes_voters = df[df["Please confirm your availability for the Team Event on 27th and 28th March"] == "YES"]
no_voters = df[df["Please confirm your availability for the Team Event on 27th and 28th March"] == "NO"]

# -----------------------------
# Match with Employee master
# -----------------------------
voted_mask = df2["Emp_key"].isin(df["Name_key"])
not_voted = df2[~voted_mask]

# -----------------------------
# Output
# -----------------------------
print("\nPeople who voted YES:\n")
for name in yes_voters["Name"]:
    print(name)

print("\nPeople who voted NO:\n")
for name in no_voters["Name"]:
    print(name)

print("\nPeople who have NOT voted:\n")
for name in not_voted["Employee Name"]:
    print(name)

print("\n-----------------------------")
print("Total Employees :", len(df2))
print("Total YES       :", len(yes_voters))
print("Total NO        :", len(no_voters))
print("Total Not Voted :", len(not_voted))
