from typing import Dict, Any

NOTIFICATION_TEMPLATES = {
    'document_uploaded': {
        'title': 'Document Uploaded',
        'message': 'Your document {document_name} has been successfully uploaded.',
        'email_subject': 'Document Upload Confirmation',
        'email_body': '''
            Dear {user_name},
            
            Your document {document_name} has been successfully uploaded to SmartProBono.
            You can view it in your documents section.
            
            Best regards,
            SmartProBono Team
        '''
    },
    'document_reviewed': {
        'title': 'Document Review Complete',
        'message': 'Your document {document_name} has been reviewed.',
        'email_subject': 'Document Review Complete',
        'email_body': '''
            Dear {user_name},
            
            Your document {document_name} has been reviewed by our team.
            Please log in to view the feedback and next steps.
            
            Best regards,
            SmartProBono Team
        '''
    },
    'case_update': {
        'title': 'Case Update',
        'message': 'There is a new update in your case {case_id}.',
        'email_subject': 'Case Update Available',
        'email_body': '''
            Dear {user_name},
            
            There has been an update in your case {case_id}.
            Please log in to view the details.
            
            Best regards,
            SmartProBono Team
        '''
    },
    'appointment_reminder': {
        'title': 'Appointment Reminder',
        'message': 'You have an upcoming appointment on {appointment_date}.',
        'email_subject': 'Appointment Reminder',
        'email_body': '''
            Dear {user_name},
            
            This is a reminder about your upcoming appointment:
            Date: {appointment_date}
            Time: {appointment_time}
            
            Please make sure to be available at the scheduled time.
            
            Best regards,
            SmartProBono Team
        '''
    }
}

def get_notification_template(template_type: str, params: Dict[str, Any]) -> Dict[str, str]:
    """
    Get a notification template and format it with the provided parameters.
    
    Args:
        template_type: The type of notification template to use
        params: Dictionary of parameters to format the template with
        
    Returns:
        Dictionary containing formatted notification content
    """
    if template_type not in NOTIFICATION_TEMPLATES:
        raise ValueError(f"Unknown notification template type: {template_type}")
        
    template = NOTIFICATION_TEMPLATES[template_type]
    return {
        'title': template['title'].format(**params),
        'message': template['message'].format(**params),
        'email_subject': template['email_subject'].format(**params),
        'email_body': template['email_body'].format(**params)
    } 