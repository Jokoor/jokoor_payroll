import frappe

def get_context(context):
    context.title = "Jokoor Payroll Features - Comprehensive Payroll Solution for The Gambia"
    context.description = "Explore the complete set of features in Jokoor Payroll designed specifically for Gambian businesses."
    
    # Employee Management Features
    context.employee_features = [
        {
            "title": "Employee Profiles",
            "description": "Create and manage comprehensive employee profiles with all essential information.",
            "icon": "fa-id-card",
            "details": [
                "Personal and professional details",
                "Document management",
                "Employment history tracking",
                "Custom fields for Gambian-specific information"
            ]
        },
        {
            "title": "Attendance Tracking",
            "description": "Monitor employee attendance, leaves, and time-off with accuracy.",
            "icon": "fa-calendar-check",
            "details": [
                "Daily attendance logging",
                "Leave request management",
                "Overtime tracking",
                "Attendance reports"
            ]
        },
        {
            "title": "Onboarding & Offboarding",
            "description": "Streamline employee onboarding and offboarding processes.",
            "icon": "fa-users-cog",
            "details": [
                "Customizable onboarding checklists",
                "Document verification",
                "Exit interviews and clearance",
                "Asset handover management"
            ]
        }
    ]
    
    # Payroll Processing Features
    context.payroll_features = [
        {
            "title": "Salary Structures",
            "description": "Design flexible salary structures tailored to your organization's needs.",
            "icon": "fa-sitemap",
            "details": [
                "Multiple salary components",
                "Customizable earning and deduction types",
                "Salary grade management",
                "Mass salary structure assignment"
            ]
        },
        {
            "title": "Payrun Management",
            "description": "Process payroll runs efficiently with complete control and accuracy.",
            "icon": "fa-money-check-alt",
            "details": [
                "Scheduled or manual payruns",
                "Batch processing capabilities",
                "Review and approval workflows",
                "Payrun summaries and analysis"
            ]
        },
        {
            "title": "Payslip Generation",
            "description": "Generate detailed and compliant payslips for all employees.",
            "icon": "fa-file-invoice-dollar",
            "details": [
                "Customizable payslip templates",
                "Digital distribution options",
                "Historical payslip access",
                "Bulk generation capabilities"
            ]
        }
    ]
    
    # Tax & Compliance Features
    context.compliance_features = [
        {
            "title": "PAYE Tax Management",
            "description": "Automate Pay As You Earn tax calculations and submissions for your Gambian workforce.",
            "icon": "fa-hand-holding-usd",
            "details": [
                "Automated calculation of tax brackets based on Gambian tax law",
                "Monthly PAYE returns for GRA submission",
                "Employee tax certificates and documentation",
                "Historical tax records for auditing purposes"
            ]
        },
        {
            "title": "SSHFC Contribution Management",
            "description": "Track and manage Social Security and Housing Finance Corporation contributions.",
            "icon": "fa-home",
            "details": [
                "Automatic calculation of employer (10%) and employee (5%) contributions",
                "Monthly SSHFC returns generation",
                "Employee contribution statements",
                "Housing fund management and reporting"
            ]
        },
        {
            "title": "Regulatory Compliance",
            "description": "Stay compliant with all Gambian labor and tax regulations.",
            "icon": "fa-balance-scale",
            "details": [
                "Automatic updates to tax rates and regulatory changes",
                "Compliance reporting dashboard",
                "Audit trail for all financial transactions",
                "Configurable compliance settings"
            ]
        }
    ]
    
    # Reporting & Analytics Features
    context.reporting_features = [
        {
            "title": "Salary Overview Reports",
            "description": "Get comprehensive insights into your organization's salary distribution.",
            "icon": "fa-chart-pie",
            "details": [
                "Department and position-based breakdowns",
                "Salary component analysis",
                "Historical salary trend reports",
                "Exportable in multiple formats"
            ]
        },
        {
            "title": "Monthly Salary Reports",
            "description": "Generate detailed monthly reports for payroll analysis and budgeting.",
            "icon": "fa-chart-line",
            "details": [
                "Monthly payroll summaries",
                "Department-wise cost analysis",
                "Variance reports for budget tracking",
                "Tax and contribution summaries"
            ]
        },
        {
            "title": "Custom Analytics",
            "description": "Create custom reports and dashboards for specific business needs.",
            "icon": "fa-analytics",
            "details": [
                "Drag-and-drop report builder",
                "Customizable metrics and KPIs",
                "Scheduled report generation",
                "Interactive dashboards"
            ]
        }
    ]
    
    # System & Administration Features
    context.admin_features = [
        {
            "title": "User Management",
            "description": "Manage user access and permissions with granular control.",
            "icon": "fa-user-shield",
            "details": [
                "Role-based access controls",
                "Department-specific permissions",
                "Audit logs for user actions",
                "Two-factor authentication options"
            ]
        },
        {
            "title": "System Configuration",
            "description": "Configure the system to align with your organization's policies and workflows.",
            "icon": "fa-cogs",
            "details": [
                "Company profile settings",
                "Fiscal year and accounting period setup",
                "Workflow customization",
                "Notification preferences"
            ]
        },
        {
            "title": "Data Management",
            "description": "Manage, import, and export data securely and efficiently.",
            "icon": "fa-database",
            "details": [
                "Bulk data import and export",
                "Data backup and restore",
                "Data archiving options",
                "Data quality assessments"
            ]
        }
    ]
    
    return context
