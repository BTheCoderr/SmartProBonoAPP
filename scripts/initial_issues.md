# Initial Issues Setup Guide

This guide provides a structured approach to creating beginner-friendly issues to help new contributors get started with SmartProBono.

## Setting Up Issue Labels

First, create these essential labels in your GitHub repository:

1. `good first issue` - Beginner-friendly issues for first-time contributors
2. `help wanted` - Issues where we're actively seeking community help
3. `documentation` - Documentation-related issues
4. `bug` - Something isn't working as expected
5. `enhancement` - New feature or improvement
6. `frontend` - Frontend-related issues
7. `backend` - Backend-related issues
8. `legal-content` - Legal content-related issues
9. `ui/ux` - User interface and experience issues
10. `accessibility` - Accessibility-related issues

## Creating Good First Issues

Here are 10 beginner-friendly issues to create, each with detailed descriptions to help new contributors:

### 1. Documentation Improvements

**Title**: Improve installation instructions in README

**Description**:
```
We need to improve the installation instructions in our README to make them clearer for new users and contributors.

### What needs to be done
- Review the current installation instructions
- Add more detailed steps for setting up the development environment
- Include troubleshooting tips for common issues
- Add screenshots where helpful

### Skills needed
- Markdown
- Clear technical writing

### Resources
- Current README: [link]
- Contributing guidelines: [link]

This is a great first issue for someone who wants to help improve our documentation!

Labels: good first issue, documentation, help wanted
```

### 2. Frontend Enhancement

**Title**: Add loading indicators to document generation form

**Description**:
```
Currently, when a user submits the document generation form, there's no visual feedback that the system is processing their request.

### What needs to be done
- Add a loading spinner or progress indicator when the form is submitted
- Disable the submit button during processing
- Show appropriate error states if the request fails

### Skills needed
- React
- Basic CSS

### Where to find the code
- Frontend code is in `/frontend/src/components/DocumentGenerator.jsx`

### Testing
- Verify the loading state appears when the form is submitted
- Verify the form returns to normal state after processing

Labels: good first issue, frontend, enhancement, ui/ux
```

### 3. Bug Fix

**Title**: Fix mobile responsive layout on homepage

**Description**:
```
The homepage layout breaks on mobile devices smaller than 375px width.

### What needs to be done
- Identify the elements causing the layout to break
- Update the CSS to make the layout responsive
- Test on various mobile screen sizes

### Steps to reproduce
1. Open the homepage on a mobile device or using browser dev tools
2. Set the viewport width to 375px or smaller
3. Notice the content overflowing horizontally

### Skills needed
- CSS
- Responsive design
- Basic HTML

### Where to find the code
- Homepage component: `/frontend/src/pages/Home.jsx`
- Styles: `/frontend/src/styles/Home.css`

Labels: good first issue, bug, frontend, ui/ux
```

### 4. Accessibility Improvement

**Title**: Add ARIA labels to form inputs

**Description**:
```
We need to improve the accessibility of our forms by adding proper ARIA labels to all input elements.

### What needs to be done
- Review all form components
- Add appropriate ARIA labels to inputs
- Ensure form elements have proper focus states
- Test with a screen reader

### Skills needed
- HTML
- Basic accessibility knowledge
- React

### Where to find the code
- Form components are in `/frontend/src/components/forms/`

### Resources
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM: Introduction to ARIA](https://webaim.org/techniques/aria/)

Labels: good first issue, accessibility, frontend, enhancement
```

### 5. Backend Test Coverage

**Title**: Add unit tests for user authentication

**Description**:
```
We need to improve our test coverage for the user authentication functionality.

### What needs to be done
- Write unit tests for the user authentication routes
- Test successful login, failed login, and registration
- Ensure tests are properly isolated

### Skills needed
- Python
- pytest
- Basic understanding of authentication flows

### Where to find the code
- Authentication routes: `/backend/routes/auth.py`
- Existing tests: `/backend/tests/`

### Resources
- [pytest documentation](https://docs.pytest.org/)
- Our testing guidelines in CONTRIBUTING.md

Labels: good first issue, backend, help wanted
```

### 6. Documentation Translation

**Title**: Translate README to Spanish

**Description**:
```
To make our project more accessible to Spanish-speaking users and contributors, we'd like to translate our README to Spanish.

### What needs to be done
- Translate the current README.md to Spanish
- Create a new file named README.es.md
- Ensure technical terms are translated accurately
- Add a language switcher link at the top of both READMEs

### Skills needed
- Fluency in Spanish and English
- Markdown
- Familiarity with technical terminology

### Resources
- Current README: [link]
- GitHub's guide on multiple language READMEs: [link]

Labels: good first issue, documentation, help wanted
```

### 7. Legal Content Review

**Title**: Review and improve eviction notice template

**Description**:
```
We need help reviewing and improving our eviction notice response template to ensure it's accurate and helpful.

### What needs to be done
- Review the current eviction notice template
- Check for legal accuracy and completeness
- Suggest improvements to make it more user-friendly
- Ensure it includes appropriate disclaimers

### Skills needed
- Legal knowledge (housing law preferred)
- Clear writing
- Understanding of document templates

### Where to find the template
- `/backend/templates/eviction_notice_response.md`

### Note
This issue is particularly suitable for contributors with legal background or experience with housing law.

Labels: good first issue, legal-content, help wanted
```

### 8. UI Component

**Title**: Create a reusable button component

**Description**:
```
We need a standardized, reusable button component with different variants (primary, secondary, danger).

### What needs to be done
- Create a new Button component in the component library
- Implement primary, secondary, and danger variants
- Add disabled state styling
- Include loading state
- Document usage examples

### Skills needed
- React
- CSS/SCSS
- Component design

### Where to create the component
- `/frontend/src/components/common/Button.jsx`
- `/frontend/src/styles/components/Button.scss`

### Resources
- Our design system guidelines: [link]
- Current button usage examples in the codebase

Labels: good first issue, frontend, enhancement, ui/ux
```

### 9. Performance Optimization

**Title**: Optimize images on the landing page

**Description**:
```
The landing page loads slowly due to unoptimized images. We need to optimize these images to improve page load time.

### What needs to be done
- Identify large images on the landing page
- Compress and resize images appropriately
- Convert to modern formats (WebP) where appropriate
- Update image references in the code

### Skills needed
- Basic image optimization knowledge
- HTML/CSS

### Where to find the images
- `/frontend/public/images/`

### Resources
- [Web.dev guide on image optimization](https://web.dev/fast/#optimize-your-images)
- Image optimization tools: TinyPNG, Squoosh, etc.

Labels: good first issue, frontend, performance, enhancement
```

### 10. DevOps Improvement

**Title**: Add GitHub Actions workflow for linting

**Description**:
```
We need to set up a GitHub Actions workflow to automatically lint our code on pull requests.

### What needs to be done
- Create a GitHub Actions workflow file
- Configure ESLint for JavaScript/React code
- Configure Flake8 for Python code
- Ensure the workflow runs on pull requests
- Add appropriate feedback to PR checks

### Skills needed
- Basic GitHub Actions knowledge
- Understanding of linting tools
- YAML

### Where to add the workflow
- Create `.github/workflows/lint.yml`

### Resources
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [ESLint](https://eslint.org/) and [Flake8](https://flake8.pycqa.org/) documentation

Labels: good first issue, devops, help wanted
```

## Issue Creation Process

1. Create each issue with a clear title and detailed description
2. Add appropriate labels, always including `good first issue` for beginner-friendly tasks
3. Link to relevant documentation or code
4. Mention in the description that the issue is suitable for new contributors
5. Add to the project board if you're using one

## Supporting New Contributors

When new contributors express interest in an issue:

1. Respond promptly and welcomingly
2. Provide additional guidance if needed
3. Offer to pair program or provide mentorship
4. Be patient and constructive in feedback
5. Celebrate their contributions

## Tracking Progress

Create a "New Contributors" project board with the following columns:

1. "Available" - Issues ready for new contributors
2. "Claimed" - Issues someone is working on
3. "In Review" - PRs under review
4. "Completed" - Merged contributions

This will help track progress and showcase opportunities for new contributors.

## Regular Maintenance

Regularly review and replenish good first issues:

1. Aim to always have 5-10 open good first issues
2. Vary the types of issues (frontend, backend, docs, etc.)
3. Adjust difficulty levels based on community feedback
4. Thank and recognize contributors who complete these issues

By maintaining a healthy selection of beginner-friendly issues, you'll create a welcoming environment for new contributors to join the SmartProBono community. 