/**
 * SmartProBono Contract Template Service
 * Provides actual contract templates with real content
 */

class ContractTemplateService {
  constructor() {
    this.templates = this.initializeTemplates();
  }

  initializeTemplates() {
    return {
      employment: {
        id: 'employment',
        title: 'Employment Agreement',
        description: 'Standard employment contract template with customizable terms',
        category: 'Employment',
        features: ['Salary Terms', 'Benefits Package', 'Non-compete Clause', 'Termination Terms'],
        price: 'Free',
        popular: true,
        content: this.getEmploymentTemplate(),
      },
      nda: {
        id: 'nda',
        title: 'Non-Disclosure Agreement (NDA)',
        description: 'Confidentiality agreement for protecting sensitive information',
        category: 'Business',
        features: ['Confidentiality Terms', 'Duration', 'Scope of Information', 'Remedies'],
        price: 'Free',
        popular: true,
        content: this.getNDATemplate(),
      },
      service: {
        id: 'service',
        title: 'Service Agreement',
        description: 'Professional service contract for freelancers and consultants',
        category: 'Business',
        features: ['Service Scope', 'Payment Terms', 'Timeline', 'Deliverables'],
        price: 'Free',
        popular: false,
        content: this.getServiceTemplate(),
      },
      partnership: {
        id: 'partnership',
        title: 'Partnership Agreement',
        description: 'Business partnership contract with profit sharing terms',
        category: 'Business',
        features: ['Partnership Terms', 'Profit Sharing', 'Decision Making', 'Exit Strategy'],
        price: 'Free',
        popular: false,
        content: this.getPartnershipTemplate(),
      },
      lease: {
        id: 'lease',
        title: 'Lease Agreement',
        description: 'Property rental agreement for residential or commercial use',
        category: 'Real Estate',
        features: ['Rent Terms', 'Security Deposit', 'Maintenance', 'Termination'],
        price: 'Free',
        popular: false,
        content: this.getLeaseTemplate(),
      },
      consulting: {
        id: 'consulting',
        title: 'Consulting Agreement',
        description: 'Independent contractor agreement for consulting services',
        category: 'Business',
        features: ['Project Scope', 'Payment Schedule', 'Intellectual Property', 'Confidentiality'],
        price: 'Free',
        popular: true,
        content: this.getConsultingTemplate(),
      },
    };
  }

  getEmploymentTemplate() {
    return {
      sections: [
        {
          title: 'EMPLOYMENT AGREEMENT',
          content: `This Employment Agreement ("Agreement") is entered into on [DATE] between [COMPANY NAME], a [STATE] corporation ("Company"), and [EMPLOYEE NAME] ("Employee").

1. POSITION AND DUTIES
Employee shall serve as [POSITION TITLE] and shall perform such duties as may be assigned by the Company. Employee agrees to devote their full business time and attention to the performance of their duties.

2. COMPENSATION
Employee shall receive a base salary of $[AMOUNT] per [PERIOD], payable in accordance with the Company's regular payroll practices. Employee may also be eligible for bonuses and benefits as determined by the Company.

3. BENEFITS
Employee shall be entitled to participate in the Company's benefit programs, including but not limited to health insurance, retirement plans, and paid time off, subject to the terms and conditions of such programs.

4. CONFIDENTIALITY
Employee agrees to maintain the confidentiality of all proprietary and confidential information of the Company and shall not disclose such information to any third party without prior written consent.

5. NON-COMPETE
During employment and for a period of [DURATION] following termination, Employee agrees not to engage in any business that competes with the Company within [GEOGRAPHIC AREA].

6. TERMINATION
Either party may terminate this Agreement with [NOTICE PERIOD] written notice. The Company may terminate immediately for cause, including but not limited to breach of this Agreement or misconduct.

7. GOVERNING LAW
This Agreement shall be governed by the laws of [STATE].

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[COMPANY REPRESENTATIVE]                    [EMPLOYEE NAME]
Date: _______________                      Date: _______________`
        }
      ],
      variables: [
        { key: 'DATE', label: 'Agreement Date', type: 'date', required: true },
        { key: 'COMPANY NAME', label: 'Company Name', type: 'text', required: true },
        { key: 'STATE', label: 'State of Incorporation', type: 'text', required: true },
        { key: 'EMPLOYEE NAME', label: 'Employee Name', type: 'text', required: true },
        { key: 'POSITION TITLE', label: 'Position Title', type: 'text', required: true },
        { key: 'AMOUNT', label: 'Salary Amount', type: 'number', required: true },
        { key: 'PERIOD', label: 'Pay Period', type: 'select', options: ['year', 'month', 'week'], required: true },
        { key: 'DURATION', label: 'Non-compete Duration', type: 'text', required: true },
        { key: 'GEOGRAPHIC AREA', label: 'Geographic Area', type: 'text', required: true },
        { key: 'NOTICE PERIOD', label: 'Notice Period', type: 'text', required: true },
      ]
    };
  }

  getNDATemplate() {
    return {
      sections: [
        {
          title: 'NON-DISCLOSURE AGREEMENT',
          content: `This Non-Disclosure Agreement ("Agreement") is entered into on [DATE] between [DISCLOSING PARTY], a [ENTITY TYPE] ("Disclosing Party"), and [RECEIVING PARTY], a [ENTITY TYPE] ("Receiving Party").

1. DEFINITION OF CONFIDENTIAL INFORMATION
Confidential Information means all non-public, proprietary, or confidential information disclosed by the Disclosing Party to the Receiving Party, including but not limited to technical data, business plans, customer lists, financial information, and trade secrets.

2. OBLIGATIONS OF RECEIVING PARTY
The Receiving Party agrees to:
a) Hold all Confidential Information in strict confidence
b) Not disclose Confidential Information to any third party without prior written consent
c) Use Confidential Information solely for the purpose of [PURPOSE]
d) Take reasonable precautions to protect the confidentiality of such information

3. EXCEPTIONS
The obligations of confidentiality shall not apply to information that:
a) Is publicly available or becomes publicly available through no breach of this Agreement
b) Was known to the Receiving Party prior to disclosure
c) Is independently developed by the Receiving Party
d) Is required to be disclosed by law or court order

4. DURATION
This Agreement shall remain in effect for a period of [DURATION] from the date of execution.

5. RETURN OF INFORMATION
Upon termination of this Agreement, the Receiving Party shall return all Confidential Information and any copies thereof to the Disclosing Party.

6. REMEDIES
The parties acknowledge that breach of this Agreement may cause irreparable harm and agree that injunctive relief may be appropriate in addition to monetary damages.

7. GOVERNING LAW
This Agreement shall be governed by the laws of [STATE].

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[DISCLOSING PARTY REPRESENTATIVE]          [RECEIVING PARTY REPRESENTATIVE]
Date: _______________                      Date: _______________`
        }
      ],
      variables: [
        { key: 'DATE', label: 'Agreement Date', type: 'date', required: true },
        { key: 'DISCLOSING PARTY', label: 'Disclosing Party Name', type: 'text', required: true },
        { key: 'RECEIVING PARTY', label: 'Receiving Party Name', type: 'text', required: true },
        { key: 'ENTITY TYPE', label: 'Entity Type', type: 'select', options: ['corporation', 'LLC', 'partnership', 'individual'], required: true },
        { key: 'PURPOSE', label: 'Purpose of Disclosure', type: 'text', required: true },
        { key: 'DURATION', label: 'Agreement Duration', type: 'text', required: true },
        { key: 'STATE', label: 'Governing State', type: 'text', required: true },
      ]
    };
  }

  getServiceTemplate() {
    return {
      sections: [
        {
          title: 'SERVICE AGREEMENT',
          content: `This Service Agreement ("Agreement") is entered into on [DATE] between [CLIENT NAME], a [ENTITY TYPE] ("Client"), and [SERVICE PROVIDER NAME], a [ENTITY TYPE] ("Service Provider").

1. SERVICES
Service Provider agrees to provide the following services: [SERVICE DESCRIPTION]

2. SCOPE OF WORK
The specific scope of work includes:
- [DELIVERABLE 1]
- [DELIVERABLE 2]
- [DELIVERABLE 3]

3. TIMELINE
Services shall be completed by [COMPLETION DATE]. Milestones are as follows:
- [MILESTONE 1]: [DATE]
- [MILESTONE 2]: [DATE]
- [MILESTONE 3]: [DATE]

4. COMPENSATION
Client agrees to pay Service Provider [PAYMENT AMOUNT] for the services rendered. Payment terms are [PAYMENT TERMS].

5. INTELLECTUAL PROPERTY
All work product created under this Agreement shall be owned by [OWNERSHIP CLAUSE].

6. CONFIDENTIALITY
Both parties agree to maintain the confidentiality of any proprietary information disclosed during the course of this Agreement.

7. TERMINATION
Either party may terminate this Agreement with [NOTICE PERIOD] written notice. Upon termination, Client shall pay for all services completed to date.

8. GOVERNING LAW
This Agreement shall be governed by the laws of [STATE].

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[CLIENT REPRESENTATIVE]                    [SERVICE PROVIDER REPRESENTATIVE]
Date: _______________                      Date: _______________`
        }
      ],
      variables: [
        { key: 'DATE', label: 'Agreement Date', type: 'date', required: true },
        { key: 'CLIENT NAME', label: 'Client Name', type: 'text', required: true },
        { key: 'SERVICE PROVIDER NAME', label: 'Service Provider Name', type: 'text', required: true },
        { key: 'ENTITY TYPE', label: 'Entity Type', type: 'select', options: ['corporation', 'LLC', 'partnership', 'individual'], required: true },
        { key: 'SERVICE DESCRIPTION', label: 'Service Description', type: 'textarea', required: true },
        { key: 'DELIVERABLE 1', label: 'Deliverable 1', type: 'text', required: true },
        { key: 'DELIVERABLE 2', label: 'Deliverable 2', type: 'text', required: true },
        { key: 'DELIVERABLE 3', label: 'Deliverable 3', type: 'text', required: true },
        { key: 'COMPLETION DATE', label: 'Completion Date', type: 'date', required: true },
        { key: 'MILESTONE 1', label: 'Milestone 1', type: 'text', required: true },
        { key: 'MILESTONE 2', label: 'Milestone 2', type: 'text', required: true },
        { key: 'MILESTONE 3', label: 'Milestone 3', type: 'text', required: true },
        { key: 'PAYMENT AMOUNT', label: 'Payment Amount', type: 'text', required: true },
        { key: 'PAYMENT TERMS', label: 'Payment Terms', type: 'text', required: true },
        { key: 'OWNERSHIP CLAUSE', label: 'IP Ownership', type: 'text', required: true },
        { key: 'NOTICE PERIOD', label: 'Notice Period', type: 'text', required: true },
        { key: 'STATE', label: 'Governing State', type: 'text', required: true },
      ]
    };
  }

  getPartnershipTemplate() {
    return {
      sections: [
        {
          title: 'PARTNERSHIP AGREEMENT',
          content: `This Partnership Agreement ("Agreement") is entered into on [DATE] between [PARTNER 1 NAME] and [PARTNER 2 NAME] (collectively, "Partners").

1. PARTNERSHIP FORMATION
The Partners hereby form a [PARTNERSHIP TYPE] partnership under the laws of [STATE] for the purpose of [BUSINESS PURPOSE].

2. PARTNERSHIP INTERESTS
The partnership interests shall be divided as follows:
- [PARTNER 1 NAME]: [PERCENTAGE]%
- [PARTNER 2 NAME]: [PERCENTAGE]%

3. CAPITAL CONTRIBUTIONS
Each Partner shall contribute the following capital:
- [PARTNER 1 NAME]: $[AMOUNT 1]
- [PARTNER 2 NAME]: $[AMOUNT 2]

4. PROFIT AND LOSS SHARING
Profits and losses shall be shared in proportion to partnership interests.

5. MANAGEMENT
Management decisions shall be made by [DECISION MAKING PROCESS].

6. WITHDRAWAL AND DISSOLUTION
A Partner may withdraw from the partnership with [NOTICE PERIOD] written notice. The partnership may be dissolved by mutual agreement or upon the occurrence of certain events.

7. GOVERNING LAW
This Agreement shall be governed by the laws of [STATE].

IN WITNESS WHEREOF, the Partners have executed this Agreement as of the date first written above.

[PARTNER 1 NAME]                           [PARTNER 2 NAME]
Date: _______________                      Date: _______________`
        }
      ],
      variables: [
        { key: 'DATE', label: 'Agreement Date', type: 'date', required: true },
        { key: 'PARTNER 1 NAME', label: 'Partner 1 Name', type: 'text', required: true },
        { key: 'PARTNER 2 NAME', label: 'Partner 2 Name', type: 'text', required: true },
        { key: 'PARTNERSHIP TYPE', label: 'Partnership Type', type: 'select', options: ['general', 'limited', 'LLP'], required: true },
        { key: 'STATE', label: 'Governing State', type: 'text', required: true },
        { key: 'BUSINESS PURPOSE', label: 'Business Purpose', type: 'text', required: true },
        { key: 'PERCENTAGE', label: 'Partnership Percentage', type: 'number', required: true },
        { key: 'AMOUNT 1', label: 'Partner 1 Capital Contribution', type: 'number', required: true },
        { key: 'AMOUNT 2', label: 'Partner 2 Capital Contribution', type: 'number', required: true },
        { key: 'DECISION MAKING PROCESS', label: 'Decision Making Process', type: 'text', required: true },
        { key: 'NOTICE PERIOD', label: 'Withdrawal Notice Period', type: 'text', required: true },
      ]
    };
  }

  getLeaseTemplate() {
    return {
      sections: [
        {
          title: 'LEASE AGREEMENT',
          content: `This Lease Agreement ("Agreement") is entered into on [DATE] between [LANDLORD NAME] ("Landlord") and [TENANT NAME] ("Tenant").

1. PROPERTY
Landlord agrees to lease to Tenant the property located at [PROPERTY ADDRESS] (the "Property").

2. TERM
The lease term shall commence on [START DATE] and end on [END DATE].

3. RENT
Tenant agrees to pay rent in the amount of $[RENT AMOUNT] per [PAYMENT PERIOD], due on the [DUE DATE] of each month.

4. SECURITY DEPOSIT
Tenant shall pay a security deposit of $[SECURITY DEPOSIT] upon execution of this Agreement.

5. USE OF PROPERTY
Tenant shall use the Property solely for [USE PURPOSE] and in compliance with all applicable laws and regulations.

6. MAINTENANCE
Landlord shall be responsible for [LANDLORD MAINTENANCE]. Tenant shall be responsible for [TENANT MAINTENANCE].

7. TERMINATION
Either party may terminate this Agreement with [NOTICE PERIOD] written notice.

8. GOVERNING LAW
This Agreement shall be governed by the laws of [STATE].

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[LANDLORD NAME]                            [TENANT NAME]
Date: _______________                      Date: _______________`
        }
      ],
      variables: [
        { key: 'DATE', label: 'Agreement Date', type: 'date', required: true },
        { key: 'LANDLORD NAME', label: 'Landlord Name', type: 'text', required: true },
        { key: 'TENANT NAME', label: 'Tenant Name', type: 'text', required: true },
        { key: 'PROPERTY ADDRESS', label: 'Property Address', type: 'text', required: true },
        { key: 'START DATE', label: 'Lease Start Date', type: 'date', required: true },
        { key: 'END DATE', label: 'Lease End Date', type: 'date', required: true },
        { key: 'RENT AMOUNT', label: 'Monthly Rent Amount', type: 'number', required: true },
        { key: 'PAYMENT PERIOD', label: 'Payment Period', type: 'select', options: ['month', 'week'], required: true },
        { key: 'DUE DATE', label: 'Rent Due Date', type: 'number', required: true },
        { key: 'SECURITY DEPOSIT', label: 'Security Deposit Amount', type: 'number', required: true },
        { key: 'USE PURPOSE', label: 'Property Use Purpose', type: 'text', required: true },
        { key: 'LANDLORD MAINTENANCE', label: 'Landlord Maintenance Responsibilities', type: 'text', required: true },
        { key: 'TENANT MAINTENANCE', label: 'Tenant Maintenance Responsibilities', type: 'text', required: true },
        { key: 'NOTICE PERIOD', label: 'Termination Notice Period', type: 'text', required: true },
        { key: 'STATE', label: 'Governing State', type: 'text', required: true },
      ]
    };
  }

  getConsultingTemplate() {
    return {
      sections: [
        {
          title: 'CONSULTING AGREEMENT',
          content: `This Consulting Agreement ("Agreement") is entered into on [DATE] between [CLIENT NAME], a [ENTITY TYPE] ("Client"), and [CONSULTANT NAME], a [ENTITY TYPE] ("Consultant").

1. CONSULTING SERVICES
Consultant agrees to provide consulting services in the area of [CONSULTING AREA] for the following project: [PROJECT DESCRIPTION]

2. SCOPE OF WORK
The specific deliverables include:
- [DELIVERABLE 1]
- [DELIVERABLE 2]
- [DELIVERABLE 3]

3. TIMELINE
The project shall be completed by [COMPLETION DATE] with the following milestones:
- [MILESTONE 1]: [DATE]
- [MILESTONE 2]: [DATE]

4. COMPENSATION
Client agrees to pay Consultant [PAYMENT AMOUNT] for the consulting services. Payment shall be made [PAYMENT SCHEDULE].

5. INTELLECTUAL PROPERTY
All work product created under this Agreement shall be owned by [IP OWNERSHIP].

6. CONFIDENTIALITY
Consultant agrees to maintain the confidentiality of all Client information and not to disclose such information to any third party.

7. INDEPENDENT CONTRACTOR
Consultant is an independent contractor and not an employee of Client.

8. TERMINATION
Either party may terminate this Agreement with [NOTICE PERIOD] written notice.

9. GOVERNING LAW
This Agreement shall be governed by the laws of [STATE].

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[CLIENT REPRESENTATIVE]                    [CONSULTANT REPRESENTATIVE]
Date: _______________                      Date: _______________`
        }
      ],
      variables: [
        { key: 'DATE', label: 'Agreement Date', type: 'date', required: true },
        { key: 'CLIENT NAME', label: 'Client Name', type: 'text', required: true },
        { key: 'CONSULTANT NAME', label: 'Consultant Name', type: 'text', required: true },
        { key: 'ENTITY TYPE', label: 'Entity Type', type: 'select', options: ['corporation', 'LLC', 'partnership', 'individual'], required: true },
        { key: 'CONSULTING AREA', label: 'Consulting Area', type: 'text', required: true },
        { key: 'PROJECT DESCRIPTION', label: 'Project Description', type: 'textarea', required: true },
        { key: 'DELIVERABLE 1', label: 'Deliverable 1', type: 'text', required: true },
        { key: 'DELIVERABLE 2', label: 'Deliverable 2', type: 'text', required: true },
        { key: 'DELIVERABLE 3', label: 'Deliverable 3', type: 'text', required: true },
        { key: 'COMPLETION DATE', label: 'Project Completion Date', type: 'date', required: true },
        { key: 'MILESTONE 1', label: 'Milestone 1', type: 'text', required: true },
        { key: 'MILESTONE 2', label: 'Milestone 2', type: 'text', required: true },
        { key: 'PAYMENT AMOUNT', label: 'Total Payment Amount', type: 'text', required: true },
        { key: 'PAYMENT SCHEDULE', label: 'Payment Schedule', type: 'text', required: true },
        { key: 'IP OWNERSHIP', label: 'IP Ownership', type: 'text', required: true },
        { key: 'NOTICE PERIOD', label: 'Termination Notice Period', type: 'text', required: true },
        { key: 'STATE', label: 'Governing State', type: 'text', required: true },
      ]
    };
  }

  // Get all templates
  getAllTemplates() {
    return Object.values(this.templates);
  }

  // Get template by ID
  getTemplate(templateId) {
    return this.templates[templateId];
  }

  // Generate contract from template with variables
  generateContract(templateId, variables) {
    const template = this.getTemplate(templateId);
    if (!template) {
      throw new Error(`Template ${templateId} not found`);
    }

    let content = template.content.sections[0].content;
    
    // Replace variables with actual values
    template.content.variables.forEach(variable => {
      const value = variables[variable.key] || `[${variable.key}]`;
      content = content.replace(new RegExp(`\\[${variable.key}\\]`, 'g'), value);
    });

    return {
      ...template,
      generatedContent: content,
      variables: variables
    };
  }

  // Save contract to user's contracts
  saveContract(templateId, variables, contractName) {
    const contract = this.generateContract(templateId, variables);
    const savedContract = {
      id: Date.now(),
      name: contractName,
      templateId: templateId,
      templateTitle: contract.title,
      content: contract.generatedContent,
      variables: variables,
      status: 'Draft',
      createdDate: new Date().toISOString().split('T')[0],
      lastModified: new Date().toISOString().split('T')[0],
    };

    // In a real app, this would save to a database
    // For now, we'll store in localStorage
    const existingContracts = JSON.parse(localStorage.getItem('userContracts') || '[]');
    existingContracts.push(savedContract);
    localStorage.setItem('userContracts', JSON.stringify(existingContracts));

    return savedContract;
  }

  // Get user's saved contracts
  getUserContracts() {
    return JSON.parse(localStorage.getItem('userContracts') || '[]');
  }
}

// Create and export singleton instance
const contractTemplateService = new ContractTemplateService();
export default contractTemplateService;
