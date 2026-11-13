"""Community Support Navigator demo.

Rule-based eligibility check. Every rule carries its legal citation exactly as
supplied. Outputs are "May be eligible", never a decision. The thresholds
(10,000 / 15,000 AED) are demo values pending sign-off by the rule owner.
Nothing is submitted anywhere; "Approve" only writes to the audit log.
"""
from datetime import datetime

import pandas as pd
import streamlit as st

# Rules dictionary: one entry per programme. Citations are verbatim.
RULES = {
    "FED-SW-001": {
        "name": "Basic Allowance",
        "source": "Decree-Law 23/2024",
        "applies": lambda p: p["income"] < 10000,
        "why": "Monthly household income is below AED 10,000.",
    },
    "FED-SW-002": {
        "name": "Housing Allowance",
        "source": "Resolution 57/2025 Art. 10-11",
        "applies": lambda p: p["need"] == "Housing" and p["income"] < 15000,
        "why": "Primary need is Housing and monthly household income is below AED 15,000.",
    },
}
DISCLAIMER = "This is information, not legal advice. Final eligibility is determined by the relevant authority."


def check_eligibility(profile: dict) -> dict:
    """Return {'outcome': 'matches'|'redirect'|'more_info', 'matches': [...], 'message': str}."""
    if profile["nationality"] != "Emirati":
        return {"outcome": "redirect", "matches": [],
                "message": "Federal and CDA programs are for citizens. Please contact Tawasul 171."}
    matches = [{"id": rid, "name": r["name"], "source": r["source"], "why": r["why"],
                "status": f"{r['name']} ({rid}) - May be eligible"}
               for rid, r in RULES.items() if r["applies"](profile)]
    if not matches:
        return {"outcome": "more_info", "matches": [], "message": "Needs more information"}
    return {"outcome": "matches", "matches": matches, "message": ""}


def log(event, detail=""):
    st.session_state.audit.append({"Time": datetime.utcnow().strftime("%H:%M:%S") + " UTC",
                                   "Event": event, "Detail": detail})


def main():
    st.set_page_config(page_title="Community Support Navigator", layout="wide")
    for k, v in (("audit", []), ("result", None), ("profile", None)):
        if k not in st.session_state:
            st.session_state[k] = v
    st.title("🤝 Community Support Navigator")
    st.markdown("**Demo: Check your eligibility for UAE social support.**")
    st.sidebar.header("Agent Rules")
    st.sidebar.info("1. Cited rules only. No guessing.\n2. May be eligible, not guaranteed.\n"
                    "3. Human review required.\n4. Every check is written to the audit log.")
    st.sidebar.caption("Thresholds in this demo are prototype values pending rule-owner sign-off.")
    with st.sidebar.expander("Rules loaded"):
        for rid, r in RULES.items():
            st.write(f"**{rid}** {r['name']}  \n{r['source']}")

    with st.form("profile_form"):
        st.write("### Tell us about your household")
        nationality = st.selectbox("Nationality", ["Emirati", "Non-Citizen"])
        emirate = st.selectbox("Emirate", ["Dubai", "Abu Dhabi", "Sharjah", "Other"])
        income = st.number_input("Monthly Household Income (AED)", min_value=0, value=8000)
        need = st.selectbox("Primary Need", ["Housing", "Basic Living", "Academic", "Emergency"])
        submitted = st.form_submit_button("Check Eligibility")

    if submitted:
        profile = {"nationality": nationality, "emirate": emirate, "income": int(income), "need": need}
        res = check_eligibility(profile)
        st.session_state.profile, st.session_state.result = profile, res
        summary = ", ".join(m["id"] for m in res["matches"]) or res["message"]
        log("Eligibility check",
            f"{nationality} | {emirate} | AED {int(income):,} | {need} -> {res['outcome']}: {summary}")

    res = st.session_state.result
    if res:
        st.write("### Results")
        if res["outcome"] == "redirect":
            st.warning(res["message"])
        elif res["outcome"] == "more_info":
            st.info(res["message"])
        else:
            st.success("Based on your profile, you may be eligible for the following:")
            for i, m in enumerate(res["matches"], 1):
                st.info(f"**{i}. {m['status']}**")
                st.write(f"- Source: {m['source']}")
                st.write(f"- Why: {m['why']}")
        st.warning(DISCLAIMER)
        if res["matches"]:
            st.write("### Human Review Queue")
            st.write("Draft application prepared. Waiting for your approval. Nothing is submitted by this demo.")
            if st.button("Approve Draft"):
                log("Draft approved by user", ", ".join(m["id"] for m in res["matches"]) + " (not submitted)")
                st.success("Draft approved and logged. This demo does not submit anything to an authority.")

    st.write("---")
    st.write("### Audit log")
    if st.session_state.audit:
        st.dataframe(pd.DataFrame(st.session_state.audit), use_container_width=True, hide_index=True)
    else:
        st.info("No checks yet.")


if __name__ == "__main__":
    main()
