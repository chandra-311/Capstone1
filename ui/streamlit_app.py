import streamlit as st
import httpx
import json
from datetime import datetime
from enum import Enum

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .stMetric { text-align: center; }
    </style>
""", unsafe_allow_html=True)

MICROSERVICE_URL = "http://localhost:8000"

def main():
    st.title("🏦 AI-Agent Loan Approval System")
    st.markdown("*Intelligent loan application analysis using AI-Agent Technology*")

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📝 New Application", "📊 Status Check", "📋 All Applications"])

    with tab1:
        st.header("Submit Loan Application")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Applicant Information")
            applicant_id = st.text_input("Applicant ID", placeholder="APPL-001")
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
            income = st.number_input("Annual Income ($)", min_value=20000, value=75000, step=5000)
            employment_type = st.selectbox(
                "Employment Type",
                ["full_time", "part_time", "self_employed", "unemployed"]
            )
            location = st.text_input("Location/State", placeholder="California")

        with col2:
            st.subheader("Loan Information")
            credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=720)
            loan_amount = st.number_input("Requested Loan Amount ($)", min_value=50000, value=250000, step=10000)
            loan_tenure_months = st.number_input("Loan Tenure (months)", min_value=12, max_value=360, value=60)
            existing_liabilities = st.number_input("Existing Liabilities ($)", min_value=0, value=50000, step=5000)

        st.divider()

        if st.button("🚀 Submit Application", use_container_width=True):
            if not applicant_id:
                st.error("Please enter an Applicant ID")
            else:
                with st.spinner("Processing application..."):
                    try:
                        application_data = {
                            "applicant_id": applicant_id,
                            "age": age,
                            "income": income,
                            "employment_type": employment_type,
                            "credit_score": credit_score,
                            "loan_amount": loan_amount,
                            "loan_tenure_months": loan_tenure_months,
                            "existing_liabilities": existing_liabilities,
                            "location": location,
                            "application_timestamp": datetime.utcnow().isoformat()
                        }

                        response = httpx.post(
                            f"{MICROSERVICE_URL}/api/apply",
                            json=application_data,
                            timeout=30.0
                        )
                        response.raise_for_status()
                        result = response.json()

                        st.success("✅ Application processed successfully!")

                        # Display DECISION STATUS prominently
                        decision = result["decision"]
                        risk_score = result["risk_score"]

                        # Color coding based on decision
                        if decision == "Approved":
                            st.markdown("---")
                            st.markdown(f"<h1 style='text-align: center; color: #28a745;'>✅ APPROVED</h1>", unsafe_allow_html=True)
                            st.balloons()
                        elif decision == "Rejected":
                            st.markdown("---")
                            st.markdown(f"<h1 style='text-align: center; color: #dc3545;'>❌ REJECTED</h1>", unsafe_allow_html=True)
                        else:  # Requires Manual Review
                            st.markdown("---")
                            st.markdown(f"<h1 style='text-align: center; color: #ffc107;'>⏳ REQUIRES MANUAL REVIEW</h1>", unsafe_allow_html=True)

                        st.markdown("---")

                        # Display results
                        st.markdown("### 📋 Decision Summary")

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric(
                                "Decision Status",
                                result["decision"],
                                delta=f"Risk: {result['risk_score']:.2f}"
                            )
                        with col2:
                            st.metric("Confidence", f"{result['confidence_level']:.1%}")
                        with col3:
                            st.metric("Risk Score", f"{result['risk_score']:.2f}")
                        with col4:
                            st.metric("Case ID", result["case_id"])

                        st.markdown("### 📝 Explanation")
                        st.info(result["explanation"])

                        st.markdown("### 🔍 Key Factors")
                        for i, factor in enumerate(result["key_factors"], 1):
                            st.write(f"{i}. {factor}")

                        st.markdown("### 📊 Detailed Analysis")
                        detailed = result.get("detailed_analysis", {})

                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Applicant Profile")
                            app_analysis = detailed.get("applicant_analysis", {})
                            if app_analysis:
                                st.write(f"**Income Stability Score:** {app_analysis.get('income_stability_score', 'N/A'):.2f}")
                                st.write(f"**Employment Risk:** {app_analysis.get('employment_risk', 'N/A')}")
                                st.write(f"**Credit History:** {app_analysis.get('credit_history_summary', 'N/A')}")

                        with col2:
                            st.subheader("Financial Risk")
                            risk_analysis = detailed.get("risk_analysis", {})
                            if risk_analysis:
                                st.write(f"**DTI Ratio:** {risk_analysis.get('debt_to_income_ratio', 'N/A'):.3f}")
                                st.write(f"**Credit Risk:** {risk_analysis.get('credit_score_risk_level', 'N/A')}")
                                st.write(f"**Loan Risk:** {risk_analysis.get('loan_amount_risk', 'N/A')}")
                                st.write(f"**Anomalies Detected:** {risk_analysis.get('anomaly_detected', False)}")

                    except httpx.HTTPError as e:
                        st.error(f"HTTP Error: {str(e)}")
                    except Exception as e:
                        st.error(f"Error processing application: {str(e)}")

    with tab2:
        st.header("Check Application Status")
        applicant_id = st.text_input("Enter Applicant ID to check status", key="status_check")

        if applicant_id and st.button("Search", use_container_width=True):
            with st.spinner("Fetching application status..."):
                try:
                    response = httpx.get(
                        f"{MICROSERVICE_URL}/api/status/{applicant_id}",
                        timeout=10.0
                    )
                    response.raise_for_status()
                    result = response.json()

                    st.success("✅ Application found!")

                    app_response = result.get("response", {})
                    decision = app_response.get("decision", "N/A")

                    # Display decision status prominently
                    st.markdown("---")
                    if decision == "Approved":
                        st.markdown(f"<h2 style='text-align: center; color: #28a745;'>✅ APPROVED</h2>", unsafe_allow_html=True)
                    elif decision == "Rejected":
                        st.markdown(f"<h2 style='text-align: center; color: #dc3545;'>❌ REJECTED</h2>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h2 style='text-align: center; color: #ffc107;'>⏳ REQUIRES MANUAL REVIEW</h2>", unsafe_allow_html=True)
                    st.markdown("---")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Decision Status", decision)
                    with col2:
                        st.metric("Risk Score", f"{app_response.get('risk_score', 0):.2f}")
                    with col3:
                        st.metric("Case ID", app_response.get("case_id", "N/A"))

                    st.write(f"**Submitted:** {result.get('submitted_at', 'N/A')}")
                    st.markdown(f"**Explanation:** {app_response.get('explanation', 'N/A')}")

                except httpx.HTTPStatusError:
                    st.warning("Application not found. Please check the Applicant ID.")
                except Exception as e:
                    st.error(f"Error fetching status: {str(e)}")

    with tab3:
        st.header("All Applications")

        if st.button("Refresh", use_container_width=True):
            st.rerun()

        try:
            response = httpx.get(
                f"{MICROSERVICE_URL}/api/applications",
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Applications", result.get("total", 0))

            if result.get("applications"):
                st.write("**Application IDs:**")
                for app_id in result.get("applications", []):
                    st.write(f"• {app_id}")
            else:
                st.info("No applications processed yet.")

        except Exception as e:
            st.error(f"Error fetching applications: {str(e)}")

    # Footer
    st.divider()
    st.markdown(
        "*Loan Approval System powered by AI-Agent Technology | Built with Streamlit, FastAPI, and Anthropic Claude*"
    )

if __name__ == "__main__":
    main()
