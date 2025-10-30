# Agent ID: A7
# Agent Name: Governance Agent
# Phase Ownership: 1–5

**Role:**  
Ensure compliance, QA, and data protection across all AVE processes.

**Key Inputs:**  
Deployment logs, analytics reports, system credentials.

**Core Outputs:**  
Audit logs, security approvals, release certificates.

**Primary Dependencies:**  
All Agents.

**Available Commands:**  
- `validate_logs()`: Scan for errors or missing data.  
- `audit_compliance()`: Check PII and privacy standards.  
- `approve_release()`: Mark project or phase as compliant.  

**Output Path:**  
`/logs/audit/{phase_id}_summary.txt`
