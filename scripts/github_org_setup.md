# GitHub Organization Setup Guide

This guide outlines the steps to create a GitHub organization for SmartProBono and set up the team structure that matches our CODEOWNERS file.

## Creating the GitHub Organization

1. Go to [GitHub's organization creation page](https://github.com/organizations/plan)
2. Select the Free plan
3. Name the organization "SmartProBono"
4. Contact email: admin@smartprobono.org (or your preferred contact email)
5. Select "My personal account" for the organization owner
6. Complete the verification process

## Setting Up Teams

Create the following teams in your organization to match the CODEOWNERS structure:

### Core Teams

1. **Core Team** (Maintainers)
   - Permission level: Admin
   - Description: Core maintainers with overall project oversight
   - Members: Add yourself and other core maintainers

2. **Board**
   - Permission level: Admin
   - Description: Board of Directors for strategic decisions
   - Members: Add board members

### Development Teams

3. **Frontend Team**
   - Permission level: Write
   - Description: Frontend developers working on React components and UI
   - Members: Add frontend developers

4. **Backend Team**
   - Permission level: Write
   - Description: Backend developers working on Flask API and services
   - Members: Add backend developers

5. **DevOps Team**
   - Permission level: Write
   - Description: CI/CD, deployment, and infrastructure management
   - Members: Add DevOps engineers

### Specialized Teams

6. **Legal Team**
   - Permission level: Write
   - Description: Legal professionals reviewing content and templates
   - Members: Add legal professionals

7. **Security Team**
   - Permission level: Write
   - Description: Security specialists and reviewers
   - Members: Add security specialists

8. **Docs Team**
   - Permission level: Write
   - Description: Documentation writers and maintainers
   - Members: Add documentation specialists

9. **Community Team**
   - Permission level: Write
   - Description: Community managers and advocates
   - Members: Add community managers

## Repository Transfer

To transfer the repository from your personal account to the organization:

1. Go to your repository settings
2. Scroll down to the "Danger Zone"
3. Click "Transfer ownership"
4. Select the "SmartProBono" organization
5. Confirm the transfer

## Post-Transfer Setup

After transferring the repository:

1. Update repository settings:
   - Enable Discussions
   - Enable Sponsorships
   - Set up branch protection rules for `main`
   - Enable vulnerability alerts

2. Create project boards:
   - Development Roadmap
   - Bug Tracking
   - Feature Requests
   - Community Engagement

3. Set up repository secrets for CI/CD:
   - `OPENAI_API_KEY`
   - Deployment credentials

4. Create initial labels:
   - `good first issue`
   - `help wanted`
   - `bug`
   - `enhancement`
   - `documentation`
   - `legal-review`

## Team Access Configuration

Ensure each team has the appropriate access to repository sections:

1. Core Team: Full repository access
2. Frontend Team: `/frontend` directory focus
3. Backend Team: `/backend` directory focus
4. Legal Team: Legal content files focus
5. DevOps Team: CI/CD configuration focus
6. Docs Team: Documentation files focus
7. Community Team: Community files focus
8. Security Team: Security-related files focus

## GitHub Apps Integration

Enable the following GitHub apps:

1. Welcome Bot
2. Stale Bot
3. CodeCov
4. Dependabot
5. GitHub Actions

This setup will ensure your organization structure matches the CODEOWNERS file and provides a solid foundation for community collaboration. 