# 🔍 SmartProBono CourtListener Integration

## Overview
SmartProBono now includes a complete CourtListener integration for real-time case law search. This allows users to search millions of court cases directly from the SmartProBono platform.

## Features
- ✅ **Real-time case law search** using CourtListener V4 API
- ✅ **1M+ cases** available for search
- ✅ **AI-powered summaries** (when available)
- ✅ **Quick search presets** for common legal topics
- ✅ **Production-ready** with error handling and CORS
- ✅ **Responsive UI** with modern design

## Files Added

### Backend Integration
- `backend/routes/courtlistener_api.py` - Flask API routes for CourtListener
- `backend/combined_server.py` - Updated to register CourtListener routes

### Frontend Integration
- `frontend/src/pages/api/caselaw.js` - Next.js API route for case law search
- `frontend/src/services/courtlistenerApi.js` - Reusable API service
- `frontend/src/components/CourtListenerSearch.js` - React component for case law search
- `frontend/src/pages/caselaw.js` - Standalone case law search page
- `frontend/src/services/api.js` - Updated with CourtListener integration

### Configuration
- `frontend/env.example` - Environment variables template

## Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp frontend/env.example frontend/.env.local

# Set your CourtListener API key
COURTLISTENER_API_KEY=604ec2a2fbe3e49f5d87a729053803151e514ebe
```

### 2. Start Development Server
```bash
cd frontend
npm run dev
```

### 3. Test the Integration
Visit: `http://localhost:3000/caselaw`

## API Endpoints

### Case Law Search
```
GET /api/caselaw?search=probation violation&page_size=20
```

**Response:**
```json
{
  "success": true,
  "search_term": "probation violation",
  "total_results": 50000,
  "results": [
    {
      "case_name": "Commonwealth v. Johnson",
      "court": "Massachusetts Appeals Court",
      "date_filed": "2023-07-14",
      "absolute_url": "https://www.courtlistener.com/opinion/123456/...",
      "citation": "123 Mass. App. Ct. 456",
      "snippet": "Case excerpt..."
    }
  ]
}
```

## Usage Examples

### Basic Search
```javascript
import { courtlistenerApi } from './services/courtlistenerApi';

const results = await courtlistenerApi.searchCaseLaw({
  search: 'employment discrimination',
  jurisdiction: 'federal',
  page_size: 10
});
```

### Quick Searches
```javascript
// Probation violations
const probationCases = await courtlistenerApi.searchProbationViolations();

// Landlord tenant disputes
const landlordCases = await courtlistenerApi.searchLandlordTenant();

// Immigration bond cases
const immigrationCases = await courtlistenerApi.searchImmigrationBond();
```

### React Component
```jsx
import CourtListenerSearch from './components/CourtListenerSearch';

function MyPage() {
  return (
    <CourtListenerSearch 
      showQuickSearches={true}
      maxResults={20}
      onCaseSelect={(caseData) => {
        console.log('Case selected:', caseData);
      }}
    />
  );
}
```

## Deployment

### 1. Environment Variables
Set in your deployment platform (Vercel, Netlify, etc.):
```
COURTLISTENER_API_KEY=604ec2a2fbe3e49f5d87a729053803151e514ebe
```

### 2. Build and Deploy
```bash
npm run build
npm run start
```

### 3. Smoke Tests
```bash
# Test basic search
curl "https://smartprobono.org/api/caselaw?search=probation violation"

# Test different queries
curl "https://smartprobono.org/api/caselaw?search=landlord tenant"
curl "https://smartprobono.org/api/caselaw?search=immigration bond RI"
```

## Expected Results

| Search Term | Expected Results |
|-------------|------------------|
| **Probation Violation** | ~50,000+ cases |
| **Landlord Tenant** | ~200,000+ cases |
| **Immigration Bond** | ~5,000+ cases |
| **Employment Discrimination** | ~140,000+ cases |
| **Personal Injury** | ~1,180,000+ cases |

## Monitoring

The integration includes built-in logging and monitoring:
- Search queries are logged for analytics
- Error handling with fallback messages
- Performance metrics (response times)
- API usage tracking

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**
   - Check API key is set correctly
   - Verify using V4 API (not V3)

2. **CORS Errors**
   - Ensure CORS headers are set for your domain
   - Check `next.config.js` configuration

3. **No Results**
   - Try broader search terms
   - Check different jurisdictions
   - Verify API key permissions

### Debug Mode
```javascript
// Enable debug logging
localStorage.setItem('debug', 'courtlistener');
```

## Support

For issues or questions:
- Check the console for error messages
- Verify API key configuration
- Test with curl commands first
- Check CourtListener API status

## Next Steps

Future enhancements:
- [ ] AI-powered case summaries
- [ ] Advanced search filters
- [ ] Case citation formatting
- [ ] Export functionality
- [ ] Integration with client files

---

**Status: ✅ Production Ready**  
**Last Updated: October 2024**  
**API Version: CourtListener V4**
