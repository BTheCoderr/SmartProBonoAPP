import unittest
import os
import subprocess
import json
import sys
from flask import current_app

from backend.app import create_app
from backend.config import ProductionConfig, TestingConfig

class DeploymentSetupTest(unittest.TestCase):
    """Test class for deployment setup."""
    
    def setUp(self):
        """Set up test environment."""
        # Create test app with production config
        self.app = create_app('production')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create test app with testing config for comparison
        self.test_app = create_app('testing')
        
    def tearDown(self):
        """Clean up test environment."""
        self.app_context.pop()
    
    def test_production_config_loaded(self):
        """Test that production config is loaded."""
        self.assertTrue(self.app.config['TESTING'] is False)
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertTrue(isinstance(self.app.config['SERVER_NAME'], str) or self.app.config['SERVER_NAME'] is None)
    
    def test_environment_variables(self):
        """Test that required environment variables are set."""
        required_vars = [
            'SECRET_KEY',
            'JWT_SECRET_KEY',
            'DATABASE_URL',
            'MAIL_SERVER',
            'MAIL_USERNAME',
            'MAIL_PASSWORD'
        ]
        
        for var in required_vars:
            self.assertIn(var, self.app.config)
            self.assertIsNotNone(self.app.config[var])
    
    def test_database_connection_string(self):
        """Test database connection string format."""
        db_url = self.app.config.get('DATABASE_URL')
        self.assertIsNotNone(db_url)
        
        # Check for valid connection string format
        valid_prefixes = ['postgresql://', 'mysql://', 'sqlite://']
        has_valid_prefix = any(db_url.startswith(prefix) for prefix in valid_prefixes)
        self.assertTrue(has_valid_prefix, f"Database URL must start with one of {valid_prefixes}")
    
    def test_static_file_serving(self):
        """Test static file serving configuration."""
        self.assertTrue('STATIC_FOLDER' in self.app.config)
        static_folder = self.app.config['STATIC_FOLDER']
        if static_folder:
            self.assertTrue(os.path.exists(static_folder), f"Static folder {static_folder} does not exist")
    
    def test_log_configuration(self):
        """Test logging configuration."""
        self.assertTrue('LOG_LEVEL' in self.app.config)
        self.assertTrue('LOG_FILE' in self.app.config)
        
        log_file = self.app.config.get('LOG_FILE')
        if log_file and not os.path.exists(os.path.dirname(log_file)):
            self.skipTest(f"Log directory does not exist: {os.path.dirname(log_file)}")
    
    def test_security_configurations(self):
        """Test security-related configurations."""
        # CSRF protection
        self.assertTrue('WTF_CSRF_ENABLED' in self.app.config)
        
        # Cookie security
        self.assertTrue('SESSION_COOKIE_SECURE' in self.app.config)
        self.assertTrue('SESSION_COOKIE_HTTPONLY' in self.app.config)
        
        # CORS settings
        self.assertTrue('CORS_ORIGINS' in self.app.config)
    
    def test_rate_limiting_configuration(self):
        """Test rate limiting configuration."""
        self.assertTrue('RATELIMIT_ENABLED' in self.app.config)
        if self.app.config.get('RATELIMIT_ENABLED'):
            self.assertTrue('RATELIMIT_DEFAULT' in self.app.config)
    
    def test_email_configuration(self):
        """Test email configuration."""
        mail_config_vars = [
            'MAIL_SERVER',
            'MAIL_PORT',
            'MAIL_USE_TLS',
            'MAIL_USERNAME',
            'MAIL_PASSWORD',
            'MAIL_DEFAULT_SENDER'
        ]
        
        for var in mail_config_vars:
            self.assertIn(var, self.app.config)
        
        # Check specific email config for SmartProBono
        self.assertEqual(self.app.config['MAIL_DEFAULT_SENDER'], 'bferrell@smartprobono.org')
    
    def test_production_vs_testing_config(self):
        """Test differences between production and testing configs."""
        # Production should have stricter security settings
        self.assertNotEqual(
            self.app.config['SECRET_KEY'],
            self.test_app.config['SECRET_KEY'],
            "Production and testing should use different secret keys"
        )
        
        # Debug mode should be off in production
        self.assertFalse(self.app.config['DEBUG'])
        self.assertTrue(self.test_app.config['DEBUG'])
        
        # Testing mode should be off in production
        self.assertFalse(self.app.config['TESTING'])
        self.assertTrue(self.test_app.config['TESTING'])
    
    def test_startup_scripts(self):
        """Test that startup scripts exist and are executable."""
        script_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'start.sh'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'install.sh')
        ]
        
        for script_path in script_paths:
            self.assertTrue(os.path.exists(script_path), f"Script {script_path} does not exist")
            self.assertTrue(os.access(script_path, os.X_OK), f"Script {script_path} is not executable")
    
    def test_required_directories(self):
        """Test that required directories exist."""
        required_dirs = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        ]
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    self.assertTrue(True, f"Created directory {directory}")
                except:
                    self.fail(f"Could not create required directory {directory}")
    
    def test_migrations_directory(self):
        """Test that migrations directory exists and is properly configured."""
        migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')
        self.assertTrue(os.path.exists(migrations_dir), f"Migrations directory {migrations_dir} does not exist")
        
        # Check for alembic.ini
        alembic_ini = os.path.join(migrations_dir, 'alembic.ini')
        self.assertTrue(os.path.exists(alembic_ini), f"Alembic config {alembic_ini} does not exist")
    
if __name__ == '__main__':
    unittest.main() 