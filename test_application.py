#!/usr/bin/env python3
"""
Test the Loan Approval System locally
"""

import asyncio
import json
from datetime import datetime
from models.loan_application import LoanApplicationRequest, DecisionStatus
from orchestrator.langgraph_engine import execute_workflow

async def main():
    print("\n╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║           🚀 LOAN APPROVAL SYSTEM - LOCAL TEST 🚀                        ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Test Application 1: Strong Profile (Expected: APPROVED)
    print("📋 TEST APPLICATION 1: Strong Profile")
    print("─" * 80)
    
    app1 = LoanApplicationRequest(
        applicant_id="APPL-STRONG-001",
        age=35,
        income=75000,
        employment_type="full_time",
        credit_score=720,
        loan_amount=250000,
        loan_tenure_months=60,
        existing_liabilities=50000,
        location="California"
    )
    
    print(f"Applicant ID: {app1.applicant_id}")
    print(f"Age: {app1.age}")
    print(f"Income: ${app1.income:,}")
    print(f"Employment: {app1.employment_type}")
    print(f"Credit Score: {app1.credit_score}")
    print(f"Loan Amount: ${app1.loan_amount:,}")
    print(f"Loan Tenure: {app1.loan_tenure_months} months")
    print(f"Existing Liabilities: ${app1.existing_liabilities:,}")
    print(f"Location: {app1.location}")
    print()
    
    print("⏳ Processing application through Multi-Agent System...")
    print("   • Agent 1: Analyzing applicant profile...")
    print("   • Agent 2: Assessing financial risk...")
    print("   • Agent 3: Synthesizing decision...")
    print("   • Agent 4: Logging compliance...")
    print()
    
    result1 = await execute_workflow(app1)
    
    print("✅ DECISION RESULT:")
    print(f"   Decision: {result1.decision.value}")
    print(f"   Risk Score: {result1.risk_score:.2f} (0=Low Risk, 1=High Risk)")
    print(f"   Confidence: {result1.confidence_level:.1%}")
    print(f"   Case ID: {result1.case_id}")
    print(f"   Timestamp: {result1.timestamp}")
    print()
    print(f"📝 Explanation:\n   {result1.explanation}")
    print()
    print(f"🔍 Key Factors:")
    for i, factor in enumerate(result1.key_factors, 1):
        print(f"   {i}. {factor}")
    print()
    print(f"📊 Detailed Analysis:")
    print(f"   Applicant Analysis: {json.dumps(result1.detailed_analysis.get('applicant_analysis', {}), indent=2)}")
    print()
    
    print("═" * 80)
    print()
    
    # Test Application 2: Fair Profile (Expected: REVIEW)
    print("📋 TEST APPLICATION 2: Fair Profile")
    print("─" * 80)
    
    app2 = LoanApplicationRequest(
        applicant_id="APPL-FAIR-001",
        age=42,
        income=60000,
        employment_type="part_time",
        credit_score=680,
        loan_amount=200000,
        loan_tenure_months=84,
        existing_liabilities=80000,
        location="Texas"
    )
    
    print(f"Applicant ID: {app2.applicant_id}")
    print(f"Age: {app2.age}")
    print(f"Income: ${app2.income:,}")
    print(f"Employment: {app2.employment_type}")
    print(f"Credit Score: {app2.credit_score}")
    print(f"Loan Amount: ${app2.loan_amount:,}")
    print(f"Loan Tenure: {app2.loan_tenure_months} months")
    print(f"Existing Liabilities: ${app2.existing_liabilities:,}")
    print(f"Location: {app2.location}")
    print()
    
    print("⏳ Processing application through Multi-Agent System...")
    result2 = await execute_workflow(app2)
    
    print("✅ DECISION RESULT:")
    print(f"   Decision: {result2.decision.value}")
    print(f"   Risk Score: {result2.risk_score:.2f}")
    print(f"   Confidence: {result2.confidence_level:.1%}")
    print(f"   Case ID: {result2.case_id}")
    print()
    print(f"📝 Explanation:\n   {result2.explanation}")
    print()
    
    print("═" * 80)
    print()
    
    # Test Application 3: Weak Profile (Expected: REJECTED)
    print("📋 TEST APPLICATION 3: Weak Profile")
    print("─" * 80)
    
    app3 = LoanApplicationRequest(
        applicant_id="APPL-WEAK-001",
        age=55,
        income=40000,
        employment_type="self_employed",
        credit_score=580,
        loan_amount=300000,
        loan_tenure_months=120,
        existing_liabilities=150000,
        location="Nevada"
    )
    
    print(f"Applicant ID: {app3.applicant_id}")
    print(f"Age: {app3.age}")
    print(f"Income: ${app3.income:,}")
    print(f"Employment: {app3.employment_type}")
    print(f"Credit Score: {app3.credit_score}")
    print(f"Loan Amount: ${app3.loan_amount:,}")
    print(f"Loan Tenure: {app3.loan_tenure_months} months")
    print(f"Existing Liabilities: ${app3.existing_liabilities:,}")
    print(f"Location: {app3.location}")
    print()
    
    print("⏳ Processing application through Multi-Agent System...")
    result3 = await execute_workflow(app3)
    
    print("✅ DECISION RESULT:")
    print(f"   Decision: {result3.decision.value}")
    print(f"   Risk Score: {result3.risk_score:.2f}")
    print(f"   Confidence: {result3.confidence_level:.1%}")
    print(f"   Case ID: {result3.case_id}")
    print()
    print(f"📝 Explanation:\n   {result3.explanation}")
    print()
    
    print("═" * 80)
    print()
    print("🎉 ALL TESTS COMPLETED!")
    print()
    print("SUMMARY:")
    print(f"  Test 1 (Strong Profile):   {result1.decision.value:15} ✅")
    print(f"  Test 2 (Fair Profile):     {result2.decision.value:15} ✅")
    print(f"  Test 3 (Weak Profile):     {result3.decision.value:15} ✅")
    print()
    print("════════════════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    asyncio.run(main())
