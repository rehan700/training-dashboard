import streamlit as st
import pandas as pd
import re
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Poll Statistics Dashboard", layout="wide")
st.title("📊 Poll Statistics Dashboard")

EMP_FILE = "Emp and Training Details.xlsx"

# -----------------------------
# Name Cleaning Function
# -----------------------------
def clean_name(name):
    name = str(name).lower().strip()
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name

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

df2["Emp_key"] = df2["Employee Name"].apply(clean_name)

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

    # -----------------------------
    # Auto-detect YES/NO column
    # -----------------------------
    response_col = None

    for col in df.columns:
        values = (
            df[col]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

        unique_vals = set(values.unique())

        if unique_vals and unique_vals.issubset({"YES", "NO"}):
            response_col = col
            break

    if not response_col:
        st.error("❌ No YES/NO response column found in uploaded file.")
        st.stop()

    st.success(f"Detected Response Column: {response_col}")

    # -----------------------------
    # Clean Data
    # -----------------------------
    df["Name_key"] = df["Name"].apply(clean_name)

    df[response_col] = (
        df[response_col]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Remove duplicate votes (keep latest)
    df = df.drop_duplicates(subset=["Name_key"], keep="last")

    # Keep only valid YES/NO responses
    valid_votes = df[df[response_col].isin(["YES", "NO"])]

    yes_voters = valid_votes[valid_votes[response_col] == "YES"]
    no_voters = valid_votes[valid_votes[response_col] == "NO"]

    # -----------------------------
    # Not Voted Calculation
    # -----------------------------
    voted_mask = df2["Emp_key"].isin(valid_votes["Name_key"])
    not_voted = df2[~voted_mask]

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    st.subheader("📌 Summary")

    total_emp = len(df2)
    yes_count = len(yes_voters)
    no_count = len(no_voters)
    not_voted_count = len(not_voted)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", total_emp)
    col2.metric("YES", f"{yes_count} ({yes_count/total_emp:.0%})")
    col3.metric("NO", f"{no_count} ({no_count/total_emp:.0%})")
    col4.metric("Not Voted", f"{not_voted_count} ({not_voted_count/total_emp:.0%})")

    st.divider()

    # -----------------------------
    # Voting Distribution Chart
    # -----------------------------
    chart_data = pd.DataFrame({
        "Response": ["YES", "NO", "Not Voted"],
        "Count": [yes_count, no_count, not_voted_count]
    })

    st.subheader("📊 Voting Distribution")
    st.bar_chart(chart_data.set_index("Response"))

    # -----------------------------
    # Tabs
    # -----------------------------
    tab1, tab2, tab3 = st.tabs([
        f"✅ YES Voters ({yes_count})",
        f"❌ NO Voters ({no_count})",
        f"⏳ Not Voted ({not_voted_count})"
    ])

    with tab1:
        st.dataframe(yes_voters[["Name"]], use_container_width=True)

    with tab2:
        st.dataframe(no_voters[["Name"]], use_container_width=True)

    with tab3:
        st.dataframe(not_voted[["Employee Name"]], use_container_width=True)

else:
    st.info("👆 Please upload the Voting file to continue.")
