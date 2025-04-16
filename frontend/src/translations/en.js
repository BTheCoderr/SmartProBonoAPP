export const en = {
  navigation: {
    home: 'Home',
    services: 'Services',
    resources: 'Resources',
    contact: 'Contact',
    legalChat: 'Legal Assistant',
    rights: 'Know Your Rights',
  },
  immigration: {
    title: 'Immigration Services',
    services: {
      visas: {
        title: 'Visa Applications',
        description:
          'Assistance with various visa types including work, student, and family visas.',
      },
      greenCard: {
        title: 'Green Card Processing',
        description: 'Support for permanent residency applications and renewals.',
      },
      citizenship: {
        title: 'Citizenship',
        description: 'Guidance through the naturalization process and citizenship applications.',
      },
      legal: {
        title: 'Legal Consultation',
        description: 'Expert legal advice on immigration matters and documentation.',
      },
    },
  },
  expungement: {
    steps: {
      eligibility: 'Check Eligibility',
      stateRules: 'State Rules',
      caseDetails: 'Case Details',
      documents: 'Documents',
      review: 'Review',
    },
    eligibility: {
      title: 'Check Your Eligibility',
      state: 'Select Your State',
      caseType: 'Type of Case',
      description: "Let's check if your case is eligible for expungement under your state's laws.",
    },
    stateRules: {
      title: 'State-Specific Rules',
      description: 'Here are the rules and requirements for expungement in your state.',
      waitingPeriod: 'Waiting Period',
      eligibilityCriteria: 'Eligibility Criteria',
      requiredDocuments: 'Required Documents',
    },
    caseDetails: {
      title: 'Case Information',
      caseNumber: 'Case Number',
      courtName: 'Court Name',
      convictionDate: 'Date of Conviction',
      charges: 'Charges',
      sentence: 'Sentence',
      completionDate: 'Sentence Completion Date',
    },
    documents: {
      title: 'Required Documents',
      upload: 'Upload Document',
      generate: 'Generate Document',
      preview: 'Preview',
      download: 'Download',
    },
    review: {
      title: 'Review Your Application',
      success: 'Your expungement application is ready for submission!',
      summary: 'Application Summary',
      submit: 'Submit Application',
      save: 'Save for Later',
    },
  },
  legalRights: {
    title: 'Know Your Rights',
    sections: {
      civil: {
        title: 'Civil Rights',
        description: 'Understanding your fundamental civil rights and protections.',
      },
      housing: {
        title: 'Housing Rights',
        description:
          'Learn about tenant rights, fair housing laws, and protections against discrimination.',
      },
      employment: {
        title: 'Employment Rights',
        description:
          'Information about workplace rights, fair labor standards, and anti-discrimination laws.',
      },
    },
  },
  legalChat: {
    title: 'AI Legal Assistant',
    placeholder: 'Ask a legal question...',
    disclaimer:
      'This AI assistant provides general legal information. For specific legal advice, please consult with a qualified attorney.',
    suggestionsTitle: 'Suggested Questions',
    suggestions: [
      'What are my tenant rights?',
      'How do I apply for citizenship?',
      'What should I do after a car accident?',
    ],
  },
  common: {
    loading: 'Loading...',
    error: 'An error occurred. Please try again.',
    submit: 'Submit',
    cancel: 'Cancel',
    back: 'Back',
    next: 'Next',
    save: 'Save',
    delete: 'Delete',
    edit: 'Edit',
    view: 'View',
    finish: 'Finish',
    backToHome: 'Back to Home',
    goBack: 'Go Back',
  },
  documents: {
    title: 'Legal Document Generator',
    selectTemplate: 'Select Document Template',
    steps: {
      selectTemplate: 'Select Template',
      fillDetails: 'Fill Details',
      review: 'Review',
    },
    review: {
      title: 'Review Your Document',
      details: 'Document Details',
    },
    generate: 'Generate Document',
    validation: {
      required: 'This field is required',
      invalid: 'Invalid format',
    },
  },
  accessibility: {
    mode: 'Accessibility Mode',
    fontSize: {
      small: 'Small Text',
      medium: 'Medium Text',
      large: 'Large Text',
    },
    contrast: 'High Contrast',
    screenReader: 'Screen Reader Optimized',
    textToSpeech: {
      enable: 'Enable Text-to-Speech',
      disable: 'Disable Text-to-Speech',
      speed: 'Speech Speed',
      volume: 'Speech Volume',
    },
    voiceInput: {
      start: 'Start Voice Input',
      stop: 'Stop Voice Input',
      listening: 'Listening...',
      error: 'Voice input not available',
    },
  },
  security: {
    title: 'Security & Compliance',
    subtitle:
      'Your privacy and security are our top priorities. We implement industry-leading security measures to protect your data.',
    features: {
      encryption: {
        title: 'End-to-End Encryption',
        description:
          'All data is encrypted in transit and at rest using industry-standard encryption protocols.',
      },
      audits: {
        title: 'Regular Security Audits',
        description:
          'We conduct regular security assessments and penetration testing to ensure your data is protected.',
      },
      dataProtection: {
        title: 'Data Protection',
        description:
          'Your data is protected according to the highest industry standards and compliance requirements.',
      },
      compliance: {
        title: 'Legal Compliance',
        description: 'We comply with GDPR, CCPA, and other relevant data protection regulations.',
      },
    },
    dataProtection: {
      title: 'Data Protection Measures',
      encryption: {
        title: 'Encryption at Rest',
        description: 'All stored data is encrypted using AES-256 encryption',
      },
      transfer: {
        title: 'Secure Data Transfer',
        description: 'All data transfers use TLS 1.3 encryption',
      },
      access: {
        title: 'Access Controls',
        description: 'Role-based access control and multi-factor authentication',
      },
      backups: {
        title: 'Regular Backups',
        description: 'Automated backups with encryption and secure storage',
      },
    },
    certifications: {
      title: 'Compliance Certifications',
      gdpr: {
        title: 'GDPR Compliance',
        description: 'Full compliance with EU data protection regulations',
      },
      ccpa: {
        title: 'CCPA Compliance',
        description: 'California Consumer Privacy Act compliance',
      },
      hipaa: {
        title: 'HIPAA Compliance',
        description: 'Healthcare data protection standards',
      },
    },
    updateMessage:
      'We regularly update our security measures and compliance certifications to ensure the highest level of protection for your data.',
  },
  subscription: {
    title: 'Choose Your Plan',
    subtitle: 'Get access to advanced features and premium support',
    recommended: 'Recommended',
    current: 'Current Plan',
    upgrade: 'Upgrade',
    contact: 'Contact Us',
    monthly: 'month',
    contactSales: 'Contact Sales',
    nonprofit: 'Are you a nonprofit organization? Get special pricing for your team.',
    plans: {
      free: {
        title: 'Basic',
        description: 'Essential legal resources for individuals',
        features: {
          templates: 'Basic document templates',
          chat: 'AI legal assistant (limited)',
          resources: 'Access to knowledge base',
        },
      },
      pro: {
        title: 'Professional',
        description: 'Advanced features for comprehensive legal support',
        features: {
          all: 'All Basic features',
          advanced: 'Advanced document customization',
          priority: 'Priority AI assistant access',
          customization: 'Custom document branding',
        },
      },
      team: {
        title: 'Enterprise',
        description: 'Complete solution for legal teams',
        price: 'Custom pricing',
        features: {
          all: 'All Professional features',
          team: 'Team collaboration tools',
          analytics: 'Usage analytics & reporting',
          support: 'Dedicated support manager',
        },
      },
    },
  },
  progress: {
    title: 'Your Progress',
    overall: 'Overall Progress',
    recentAchievements: 'Recent Achievements',
    premiumFeature: 'Premium Feature',
    lockedBadgeMessage: 'Complete more actions to unlock this badge',
    badges: {
      firstDoc: 'First Document',
      firstDocDesc: 'Created your first legal document',
      expert: 'Legal Expert',
      expertDesc: 'Completed 10 legal documents',
      advocate: 'Community Advocate',
      advocateDesc: 'Helped 5 other users',
      master: 'Legal Master',
      masterDesc: 'Achieved proficiency in all document types',
    },
    milestones: {
      started: 'Journey Started',
      document: 'Document Created',
      profile: 'Profile Completed',
      shared: 'First Share',
    },
  },
  errors: {
    notFound: {
      title: 'Page Not Found',
      message: 'The page you are looking for does not exist or has been moved.',
    },
  },
  feedback: {
    title: 'Share Your Feedback',
    overallRating: 'Overall Rating',
    accuracy: 'How accurate was the legal information provided?',
    accuracyHigh: 'Very accurate',
    accuracyMedium: 'Somewhat accurate',
    accuracyLow: 'Not accurate',
    helpfulness: 'How helpful was this interaction?',
    helpfulnessVery: 'Very helpful',
    helpfulnessSomewhat: 'Somewhat helpful',
    helpfulnessNot: 'Not helpful',
    clarity: 'How clear were the explanations?',
    clarityHigh: 'Very clear',
    clarityMedium: 'Moderately clear',
    clarityLow: 'Not clear',
    suggestions: 'Do you have any suggestions for improvement?',
    submit: 'Submit Feedback',
    submitted: 'Thank you for your feedback!',
    userType: {
      user: 'User',
      lawyer: 'Legal Professional',
    },
  },
};
