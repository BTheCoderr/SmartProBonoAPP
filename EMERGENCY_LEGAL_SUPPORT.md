# 24/7 Legal Support Telecom Conference System

## Overview

The 24/7 Legal Support Telecom Conference System provides real-time legal assistance to users facing urgent legal situations. This feature enables users to connect with volunteer lawyers and legal advocates through secure audio/video conferencing during critical moments such as police stops, evictions, and other emergency legal scenarios.

## Features

- **Emergency Legal Assistance Button**: Prominently displayed in the navigation for immediate access
- **Smart Triage System**: Prioritizes cases based on urgency and legal domain
- **Open-Source Conferencing**: Uses Jitsi Meet for free, secure, and encrypted video calls
- **AI-Powered Initial Screening**: Routes users to the appropriate legal advocate
- **Evidence Recording**: Records calls with user consent for documentation
- **Location Sharing**: Helps advocates understand the physical context of the situation
- **Case Tracking**: Maintains history of calls for follow-up support

## Technical Implementation

### Frontend

The frontend implementation uses React with Material-UI for the user interface. Key components include:

- `EmergencyLegalSupportPage`: Main page that handles the emergency support workflow
- `EmergencyLegalCallButton`: Button component that initiates the emergency process
- `EmergencyLegalTriage`: Form that collects essential information before connecting
- `EmergencyLegalService`: Service that handles API calls to the backend

### Backend

The backend provides several API endpoints to support the telecom feature:

- `/api/emergency-legal/availability`: Returns current wait times and lawyer availability
- `/api/emergency-legal/triage`: Accepts triage information and returns connection details
- `/api/emergency-legal/call/:id/status`: Gets the status of a call
- `/api/emergency-legal/call/:id/end`: Ends an ongoing call
- `/api/emergency-legal/call/:id/recording`: Toggles recording for a call

### Video Conferencing

We use Jitsi Meet, an open-source video conferencing solution that provides:

1. Free unlimited calling with no time restrictions
2. End-to-end encryption for privacy
3. No account requirements for users
4. Screen sharing capabilities
5. Meeting recording (with consent)
6. Works in browsers without plugins

## Setting Up Locally

1. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

3. **Configure Jitsi** (for production):
   - For testing, the public Jitsi server (meet.jit.si) is used
   - For production, consider setting up your own Jitsi server for privacy and control

## Production Considerations

When deploying to production, consider the following:

1. **Lawyer Portal**: Develop a matching portal for lawyers to accept cases
2. **Self-Hosted Jitsi**: Set up your own Jitsi server for better control and privacy
3. **Database Integration**: Replace mock data with real database storage
4. **Push Notifications**: Implement notifications for lawyers when new cases arrive
5. **Recording Storage**: Secure storage for recorded calls with proper retention policies
6. **Case Management**: Full case management system to track outcomes and follow-up

## Privacy and Legal Considerations

- All calls should be encrypted
- Recording should only happen with explicit consent
- Clear terms of service should explain data handling
- Compliance with legal regulations in various jurisdictions
- Data retention policies should be transparent

## Volunteer Recruitment

For this system to work effectively, you'll need to:

1. Recruit volunteer lawyers across different specialties
2. Create shifts to ensure 24/7 coverage
3. Provide training on using the system effectively
4. Establish clear escalation paths for complex cases

## Future Enhancements

- **AI-Based Legal Triage**: Further develop AI capabilities for initial legal assessment
- **Integration with Court Systems**: Connect with e-filing systems where available
- **Mobile App**: Dedicated mobile application for faster access in emergencies
- **Offline Support**: Limited functionality when internet connection is unreliable
- **Language Support**: Multilingual capabilities with real-time translation 