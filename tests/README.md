# SmartProBono Test Suite

Comprehensive test suite for the SmartProBono legal platform covering backend APIs, frontend components, integration tests, and more.

## 📋 Test Overview

### Test Categories

1. **Backend API Tests** (`test_backend_apis.py`)
   - Immigration CRM API endpoints
   - Voice processing API endpoints
   - Court filing API endpoints
   - Analytics API endpoints
   - Document collaboration API endpoints
   - WebSocket endpoints
   - Error handling and validation

2. **Voice Service Tests** (`test_voice_service.py`)
   - Speech-to-text functionality
   - Text-to-speech synthesis
   - Voice command processing
   - AI voice analysis
   - Voice service initialization
   - Error handling

3. **Court Filing Service Tests** (`test_court_filing_service.py`)
   - Court filing creation and management
   - Document template generation
   - Court rules and compliance
   - Filing validation
   - Fee calculation
   - Deadline management

4. **Integration Tests** (`test_integration.py`)
   - End-to-end workflows
   - API integration testing
   - WebSocket real-time features
   - Performance testing
   - Security testing
   - Concurrent request handling

5. **Frontend Component Tests** (`test_frontend_components.js`)
   - React component rendering
   - User interaction testing
   - State management
   - API integration
   - Error handling
   - Accessibility testing

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- pip and npm

### Installation

```bash
# Install test dependencies
pip install -r tests/requirements-test.txt

# For frontend tests
cd frontend && npm install
```

### Running Tests

#### Quick Test Run
```bash
python run_tests.py --quick
```

#### Full Test Suite
```bash
python run_tests.py --all
```

#### Specific Test Categories
```bash
# Backend tests only
python run_tests.py --backend

# Integration tests only
python run_tests.py --integration

# Security tests only
python run_tests.py --security

# Coverage report
python run_tests.py --coverage
```

#### Individual Test Files
```bash
# Backend API tests
pytest tests/test_backend_apis.py -v

# Voice service tests
pytest tests/test_voice_service.py -v

# Court filing tests
pytest tests/test_court_filing_service.py -v

# Integration tests
pytest tests/test_integration.py -v
```

#### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Test Output

Test results are displayed directly in the console - **NO HTML FILES!**

- ✅ Backend API test results (console only)
- ✅ Integration test results (console only)  
- ✅ Code coverage report (console only)
- ✅ Security scan results (console only)
- ✅ Performance metrics (console only)

**Simple and clean output - no file clutter!**

## 🧪 Test Structure

### Backend Tests

#### Immigration CRM API Tests
```python
class TestImmigrationCRMAPI:
    def test_get_immigration_cases(self, client):
        """Test getting immigration cases"""
        
    def test_create_immigration_case(self, client):
        """Test creating a new immigration case"""
        
    def test_update_immigration_case(self, client):
        """Test updating an immigration case"""
```

#### Voice API Tests
```python
class TestVoiceAPI:
    def test_get_voice_status(self, client):
        """Test getting voice service status"""
        
    def test_speech_to_text(self, client):
        """Test speech-to-text conversion"""
        
    def test_text_to_speech(self, client):
        """Test text-to-speech synthesis"""
```

#### Court Filing API Tests
```python
class TestCourtFilingAPI:
    def test_get_court_rules(self, client):
        """Test getting court rules"""
        
    def test_generate_document(self, client):
        """Test document generation from templates"""
        
    def test_create_filing(self, client):
        """Test creating court filings"""
```

### Integration Tests

#### Platform Integration
```python
class TestPlatformIntegration:
    def test_immigration_crm_workflow(self, base_url):
        """Test complete immigration CRM workflow"""
        
    def test_voice_processing_workflow(self, base_url):
        """Test complete voice processing workflow"""
        
    def test_court_filing_workflow(self, base_url):
        """Test complete court filing workflow"""
```

#### Performance Tests
```python
class TestPerformanceIntegration:
    def test_response_times(self, base_url):
        """Test API response times"""
        
    def test_concurrent_requests(self, base_url):
        """Test platform under concurrent load"""
```

### Frontend Tests

#### Component Tests
```javascript
describe('ImmigrationCRM Component', () => {
  test('renders immigration CRM component', () => {
    
  test('displays cases list', async () => {
    
  test('creates new case', async () => {
```

#### Integration Tests
```javascript
describe('Component Integration Tests', () => {
  test('navigation between components', () => {
    
  test('shared state management', () => {
```

## 🔧 Test Configuration

### Fixtures

The test suite includes comprehensive fixtures in `conftest.py`:

- `test_config` - Test configuration settings
- `sample_immigration_case` - Sample case data
- `sample_court_filing` - Sample filing data
- `sample_voice_command` - Sample voice command data
- `mock_ai_response` - Mock AI analysis response
- `mock_websocket_message` - Mock WebSocket message

### Mock Services

Tests use mocks for external services:

- Email service mocking
- Slack service mocking
- WebSocket service mocking
- AI service mocking

## 📈 Coverage Goals

- **Backend APIs**: 90%+ coverage
- **Services**: 85%+ coverage
- **Frontend Components**: 80%+ coverage
- **Integration Tests**: All major workflows

## 🚨 Test Markers

Tests are organized with markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.websocket` - WebSocket tests
- `@pytest.mark.external` - External service tests
- `@pytest.mark.slow` - Slow running tests

## 🔒 Security Testing

Security tests include:

- Input validation testing
- SQL injection prevention
- XSS protection
- CORS configuration
- Rate limiting
- Authentication/authorization

## ⚡ Performance Testing

Performance benchmarks:

- API response time < 2 seconds
- Concurrent request handling
- Memory usage monitoring
- Database query optimization

## 🐛 Debugging Tests

### Running Tests in Debug Mode
```bash
pytest tests/test_backend_apis.py -v -s --pdb
```

### Verbose Output
```bash
pytest tests/ -v --tb=long
```

### Specific Test
```bash
pytest tests/test_backend_apis.py::TestImmigrationCRMAPI::test_create_immigration_case -v
```

## 📝 Writing New Tests

### Backend Test Template
```python
def test_new_endpoint(self, client):
    """Test description"""
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = client.post('/api/endpoint', json=test_data)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
```

### Frontend Test Template
```javascript
test('component behavior', async () => {
  // Arrange
  render(<Component />);
  
  // Act
  fireEvent.click(screen.getByText('Button'));
  
  // Assert
  await waitFor(() => {
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

## 🔄 CI/CD Integration

Tests are automatically run on:

- Pull requests
- Pushes to main/develop branches
- Daily scheduled runs
- Manual triggers

### GitHub Actions Workflow

The `.github/workflows/tests.yml` file includes:

- Backend tests (Python 3.8-3.11)
- Integration tests
- Security scans
- Frontend tests
- Performance tests
- Code quality checks
- Coverage reporting

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Testing Library Documentation](https://testing-library.com/)
- [Jest Documentation](https://jestjs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

## 🤝 Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Update this documentation
5. Add integration tests for new workflows

## 📞 Support

For test-related issues:

1. Check the console output for error details
2. Run tests individually to isolate issues
3. Check the GitHub Actions workflow logs
4. Review the test documentation

---

**Happy Testing! 🧪✨**
