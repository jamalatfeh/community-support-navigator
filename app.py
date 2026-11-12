import streamlit as st
import pandas as pd

st.set_page_config(page_title="Community Support Navigator", layout="wide")
st.title("🤝 Community Support Navigator")
st.markdown("**Demo: Check your eligibility for UAE social support.**")

st.sidebar.header("Agent Rules")
st.sidebar.info("1. Cited rules only. No guessing.\n2. May be eligible, not guaranteed.\n3. Human review required.")

# Simple UI for the 4 questions
with st.form("profile_form"):
    st.write("### Tell us about your household")
    nationality = st.selectbox("Nationality", ["Emirati", "Non-Citizen"])
    emirate = st.selectbox("Emirate", ["Dubai", "Abu Dhabi", "Sharjah", "Other"])
    income = st.number_input("Monthly Household Income (AED)", min_value=0, value=8000)
    need = st.selectbox("Primary Need", ["Housing", "Basic Living", "Academic", "Emergency"])
    
    submitted = st.form_submit_button("Check Eligibility")

if submitted:
    st.write("### Results")
    
    # Mock Logic (Replace with your actual navigator_logic.py)
    if nationality == "Non-Citizen":
        st.warning("Federal and CDA programs are for citizens. Pointing to Tawasul 171.")
    else:
        st.success("Based on your profile, you may be eligible for the following:")
        
        # This is where you would call your actual Python engine
        st.info("**1. Basic Allowance (FED-SW-001)**")
        st.write("- Source: Decree-Law 23/2024")
        st.write("- Status: May be eligible (Income threshold check)")
        
        if need == "Housing":
            st.info("**2. Housing Allowance (FED-SW-002)**")
            st.write("- Source: Resolution 57/2025 Art. 10-11")
            st.write("- Status: May be eligible")

    st.warning("This is information, not legal advice. Final eligibility is determined by the relevant authority.")
    
    # Approval Queue
    st.write("### Human Review Queue")
    st.write("Draft application generated. Waiting for user approval.")
    if st.button("Approve Draft"):
        st.success("Draft approved by user. Ready to submit to authority.")