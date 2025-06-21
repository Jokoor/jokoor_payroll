import frappe

def get_context(context):
    context.title = "Jokoor Payroll - Modern Payroll Solution for The Gambia"
    context.description = "Streamline your payroll processes with our comprehensive system designed specifically for Gambian businesses."
    
    # Hero section
    context.hero = {
        "title": "Payroll made easy for The Gambia",
        "subtitle": "Move beyond manual payroll and build a better workplace for your business with Jokoor Payroll, powerful payroll software from the Jokoor suite.",
        "cta_text": "Get Started",
        "cta_url": "/contact"
    }
    
    # Features section
    context.features = [
        {
            "title": "Automated Calculations",
            "description": "Automatically calculate salaries, taxes, and deductions with precision and compliance to Gambian regulations.",
            "icon": "fa-calculator"
        },
        {
            "title": "Employee Self-Service",
            "description": "Empower employees to access their pay slips, tax forms, and request leaves through a user-friendly portal.",
            "icon": "fa-users"
        },
        {
            "title": "Compliance Management",
            "description": "Stay compliant with Gambian tax regulations and labor laws with built-in compliance checks.",
            "icon": "fa-shield-alt"
        },
        {
            "title": "Comprehensive Reports",
            "description": "Generate detailed reports on payroll expenses, tax contributions, and employee compensation.",
            "icon": "fa-chart-bar"
        }
    ]
    
    # Advanced Features section
    context.advanced_features = [
        {
            "title": "Formula-based earnings",
            "description": "Create and apply custom formulas to salary components and let the system handle all the payroll math for you.",
            "icon": "fa-calculator"
        },
        {
            "title": "Scheduled earnings",
            "description": "Set up bonuses and variable pay in advance, ensuring your team receives their fair share with every pay run.",
            "icon": "fa-calendar-check"
        },
        {
            "title": "Pay schedule",
            "description": "Choose a pay schedule that works best for your team's needs, from task-based pay to monthly cycles.",
            "icon": "fa-clock"
        },
        {
            "title": "Reporting tags",
            "description": "Create custom tags, link them to employees, and get tailored reports that provide deeper insights into your workforce.",
            "icon": "fa-tags"
        }
    ]
    
    # Compliance section
    context.compliance_features = [
        {
            "title": "Social security",
            "description": "Build your team across borders while Jokoor Payroll automatically manages pensions for every employee.",
            "icon": "fa-shield-alt"
        },
        {
            "title": "Gratuity",
            "description": "Reward long-serving employees with gratuity and ensure accurate payouts to departing members.",
            "icon": "fa-gift"
        },
        {
            "title": "WPS",
            "description": "Effortlessly generate Wage files and meet WPS requirements while processing employee salaries.",
            "icon": "fa-file-invoice"
        },
        {
            "title": "Overtime",
            "description": "Auto-sync overtime hours and reward employees who go above and beyond their call of duty.",
            "icon": "fa-business-time"
        }
    ]
    
    # Leave types section
    context.leave_types = [
        {
            "title": "Sick Leave",
            "status": "Active",
            "icon": "fa-thermometer",
            "type": "sick"
        },
        {
            "title": "Casual Leave",
            "status": "Active",
            "icon": "fa-umbrella-beach",
            "type": "casual"
        },
        {
            "title": "Annual Leave",
            "status": "Active",
            "icon": "fa-calendar-alt",
            "type": "annual"
        }
    ]
    
    # Benefits section
    context.benefits = [
        {
            "title": "Save Time and Resources",
            "description": "Reduce the time spent on payroll processing by up to 80% and minimize manual errors.",
            "icon": "fa-clock"
        },
        {
            "title": "Enhanced Security",
            "description": "Protect sensitive employee and financial data with enterprise-grade security measures.",
            "icon": "fa-lock"
        },
        {
            "title": "Local Support",
            "description": "Get dedicated support from our team based in The Gambia who understand local business needs.",
            "icon": "fa-headset"
        },
        {
            "title": "Scalable Solution",
            "description": "Our system grows with your business, from small startups to large enterprises.",
            "icon": "fa-expand-arrows-alt"
        }
    ]
    
    # Testimonials section
    context.testimonials = [
        {
            "quote": "Jokoor Payroll has transformed how we manage employee compensation. The system is intuitive, reliable, and perfectly adapted to Gambian business requirements.",
            "author": "Fatou Ceesay",
            "position": "HR Director, Gambia Tourism Board"
        },
        {
            "quote": "Since implementing Jokoor Payroll, we've reduced our payroll processing time by 75% and eliminated calculation errors. The local support team is exceptional.",
            "author": "Lamin Jatta",
            "position": "Finance Manager, Banjul Breweries"
        },
        {
            "quote": "As a growing business in The Gambia, we needed a payroll solution that could scale with us. Jokoor Payroll has exceeded our expectations in every way.",
            "author": "Isatou Saine",
            "position": "CEO, TechHub Gambia"
        },
        {
            "quote": "The compliance features alone are worth the investment. We no longer worry about keeping up with changing tax regulations in The Gambia.",
            "author": "Omar Touray",
            "position": "Accountant, Gambia Ports Authority"
        }
    ]
    
    # Section content
    context.sections = {
        "advanced_features": {
            "subtitle": "ADVANCED FEATURES",
            "title": "Powerfully engineered to back your unique processes",
            "description": "Our system adapts to your business workflows, not the other way around. Customize every aspect of your payroll process."
        },
        "compliance": {
            "subtitle": "SIMPLIFIED COMPLIANCE",
            "title": "Free yourself from compliance tasks",
            "description": "We handle regionally intricate compliance so you can relax knowing your payroll stays on the right side of the law always."
        },
        "visualization": {
            "title": "Visualize payroll like never before",
            "description": "Get complete visibility on your payroll costs with 10+ auto-generated reports and make data-backed decisions."
        },
        "unified_operations": {
            "subtitle": "STREAMLINED OPERATIONS",
            "title": "Unify payroll, leave, and attendance",
            "description": "Create leave types that suit your business, let employees apply for leave, and keep track of their attendance—all within one payroll software."
        },
        "language": {
            "title": "Make Jokoor Payroll speak your language",
            "description": "Choose English or Arabic and let Jokoor Payroll adapt to the language you're most comfortable with."
        }
    }
    
    # CTA section
    context.cta = {
        "title": "Ready to Streamline Your Payroll Process?",
        "description": "Join hundreds of Gambian businesses that trust Jokoor Payroll for their payroll management needs.",
        "button_text": "Request a Demo",
        "button_url": "/contact"
    }
    
    return context
