#!/usr/bin/env python3
"""
Supabase Project Activity Script
Keeps your Supabase project active by performing regular health checks
This prevents automatic pausing due to inactivity
"""

import os
import sys
import time
import logging
from datetime import datetime
from supabase import create_client, Client

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('project_activity.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_env():
    """Load environment variables from .env file"""
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")

def get_supabase_client() -> Client:
    """Create Supabase client"""
    load_env()
    
    url = os.environ.get('SUPABASE_URL', 'https://ewtcvsohdgkthuyajyyk.supabase.co')
    key = os.environ.get('SUPABASE_KEY') or os.environ.get('SUPABASE_ANON_KEY')
    
    if not key:
        logger.error("SUPABASE_KEY or SUPABASE_ANON_KEY not found in environment")
        sys.exit(1)
    
    return create_client(url, key)

def perform_health_check(client: Client) -> bool:
    """Perform a health check on the database"""
    try:
        # Query a lightweight table
        response = client.table('lawyer_profiles').select('id').limit(1).execute()
        logger.info(f"✅ Health check passed - Database is responsive")
        return True
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return False

def log_activity(client: Client, activity_type: str = "health_check"):
    """Log activity to prevent project pause"""
    try:
        # Try to query different tables to show activity
        tables = ['lawyer_profiles', 'case_intakes']
        
        for table in tables:
            try:
                response = client.table(table).select('count', count='exact').limit(1).execute()
                count = response.count if hasattr(response, 'count') else 0
                logger.info(f"📊 {table}: {count} records")
            except Exception as e:
                logger.warning(f"⚠️  Could not query {table}: {e}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Activity logging failed: {e}")
        return False

def run_continuous_checks(interval_hours: int = 12):
    """Run continuous health checks at specified interval"""
    logger.info("=" * 60)
    logger.info("🚀 Starting Supabase Project Activity Monitor")
    logger.info("=" * 60)
    logger.info(f"Check Interval: Every {interval_hours} hours")
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    client = get_supabase_client()
    check_count = 0
    
    while True:
        try:
            check_count += 1
            logger.info(f"\n🔍 Health Check #{check_count}")
            logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Perform health check
            if perform_health_check(client):
                log_activity(client)
                logger.info("✅ Activity logged successfully")
            else:
                logger.warning("⚠️  Health check failed, will retry next cycle")
            
            # Wait for next check
            sleep_seconds = interval_hours * 3600
            logger.info(f"😴 Sleeping for {interval_hours} hours until next check...")
            time.sleep(sleep_seconds)
            
        except KeyboardInterrupt:
            logger.info("\n⚠️  Received interrupt signal, shutting down...")
            break
        except Exception as e:
            logger.error(f"❌ Error in health check loop: {e}")
            logger.info("Retrying in 5 minutes...")
            time.sleep(300)  # Wait 5 minutes before retry

def run_single_check():
    """Run a single health check"""
    logger.info("🔍 Running single health check...")
    client = get_supabase_client()
    
    if perform_health_check(client):
        log_activity(client)
        logger.info("✅ Health check completed successfully")
        return 0
    else:
        logger.error("❌ Health check failed")
        return 1

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Keep Supabase project active with regular health checks'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=12,
        help='Health check interval in hours (default: 12)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run a single check and exit'
    )
    
    args = parser.parse_args()
    
    if args.once:
        sys.exit(run_single_check())
    else:
        run_continuous_checks(args.interval)

if __name__ == "__main__":
    main()

