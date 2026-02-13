import streamlit as st
import pandas as pd
import re
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Team Event Voting Dashboard", layout="wide")
st.title("📊 Team Event Voting Dashboard")

EMP_FILE = "Emp and Training Details.xlsx"

# -----------------------------
# Name Cleaning Function
# -----------------------------
def extract_first_last(name):
    name = str(name).lower().strip()
    name = re.sub(r"\(.*?\)", "", name)
    parts = name.split()

    if len(parts) >= 2:
        return parts[0] + " " + parts[-1]
    elif len(parts) == 1:
        return parts[0]
    return ""

# -----------------------------
# Load Employee Master (Permanent)
# -----------------------------
if not os.path.exists(EMP_FILE):
    st.error("❌ Employee master file not found in project folder.")
    st.stop()

df2 = pd.read_excel(EMP_FILE)
df2.columns = df2.columns.str.strip()

if "Employee Name" not in df2.columns:
    st.error("❌ 'Employee Name' column not found in Employee master file.")
    st.stop()

df2["Emp_key"] = df2["Employee Name"].apply(extract_first_last)

# -----------------------------
# Upload Voting File (CSV or Excel)
# -----------------------------
st.sidebar.header("Upload Voting File")
voted_file = st.sidebar.file_uploader(
    "Upload Voting File (CSV or Excel)",
    type=["csv", "xlsx"]
)

if voted_file:

    # Detect file type
    if voted_file.name.endswith(".csv"):
        df = pd.read_csv(voted_file)
    else:
        df = pd.read_excel(voted_file)

    df.columns = df.columns.str.strip()

    # Validate required column
    if "Name" not in df.columns:
        st.error("❌ 'Name' column not found in uploaded file.")
        st.stop()

    # Auto-detect availability column
    response_col = [col for col in df.columns if "availability" in col.lower()]

    if not response_col:
        st.error("❌ Availability column not found in uploaded file.")
        st.stop()

    response_col = response_col[0]

    # Clean data
    df["Name_key"] = df["Name"].apply(extract_first_last)

    df[response_col] = (
        df[response_col]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # YES / NO split
    yes_voters = df[df[response_col] == "YES"]
    no_voters = df[df[response_col] == "NO"]

    # Not voted
    voted_mask = df2["Emp_key"].isin(df["Name_key"])
    not_voted = df2[~voted_mask]

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    st.subheader("📌 Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", len(df2))
    col2.metric("Total YES", len(yes_voters))
    col3.metric("Total NO", len(no_voters))
    col4.metric("Not Voted", len(not_voted))

    st.divider()

    # -----------------------------
    # Pie Chart
    # -----------------------------
    chart_data = pd.DataFrame({
        "Response": ["YES", "NO", "Not Voted"],
        "Count": [len(yes_voters), len(no_voters), len(not_voted)]
    })

    st.subheader("📊 Voting Distribution")
    st.bar_chart(chart_data.set_index("Response"))

    # -----------------------------
    # Tabs
    # -----------------------------
    tab1, tab2, tab3 = st.tabs([f"✅ YES Voters ({len(yes_voters)})", f"❌ NO Voters ({len(no_voters)})", f"⏳ Not Voted ({len(not_voted)})"])

    with tab1:
        st.dataframe(yes_voters[["Name"]], use_container_width=True)

    with tab2:
        st.dataframe(no_voters[["Name"]], use_container_width=True)

    with tab3:
        st.dataframe(not_voted[["Employee Name"]], use_container_width=True)

else:
    st.info("👆 Please upload the Voting file to continue.")
