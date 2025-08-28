# 🔐 Supabase Setup Instructions for SmartProBono

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - Name: `smartprobono`
   - Database Password: (generate a strong password)
   - Region: Choose closest to your users
6. Click "Create new project"

## 2. Get Your Credentials

1. Go to Settings > API
2. Copy your:
   - Project URL
   - Anon public key
   - Service role key (keep this secret!)

## 3. Set Up Environment Variables

1. Copy `.env.example` to `.env`
2. Fill in your Supabase credentials:
   ```
   REACT_APP_SUPABASE_URL=https://your-project.supabase.co
   REACT_APP_SUPABASE_ANON_KEY=your_anon_key
   REACT_APP_SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   ```

## 4. Set Up Database Schema

1. Go to SQL Editor in Supabase
2. Run the SQL from `supabase_policies.sql`
3. This will create all tables and security policies

## 5. Set Up Storage (for documents)

1. Go to Storage in Supabase
2. Create a new bucket called `documents`
3. Set it to public if you want public access
4. Or keep it private and use RLS policies

## 6. Test the Setup

1. Start your app: `./start_mvp.sh`
2. Try signing up a new user
3. Check the Supabase dashboard to see the data

## 7. Security Features

✅ **Row Level Security (RLS)**: Users can only see their own data
✅ **Authentication**: Secure user signup and login
✅ **API Security**: Protected endpoints with JWT tokens
✅ **Data Validation**: Input validation and sanitization
✅ **Rate Limiting**: Built-in Supabase rate limiting

## 8. Multi-Agent AI System

The new AI system includes:
- **Greeting Agent**: Handles simple greetings (no more overwhelming responses!)
- **Compliance Agent**: GDPR, SOC 2, privacy policies
- **Business Agent**: Entity formation, fundraising, contracts
- **Document Agent**: Document analysis and generation
- **Expert Agent**: Complex questions and expert referrals

## 9. Migration from Current Backend

The current Flask backend will be replaced with:
- Supabase for database and auth
- Supabase Edge Functions for API endpoints
- Supabase Storage for file uploads
- Supabase Realtime for live updates

## 10. Next Steps

1. Set up your Supabase project
2. Configure environment variables
3. Test the new system
4. Migrate existing data (if any)
5. Deploy to production

Your SmartProBono platform will now have:
- ✅ Proper security with RLS
- ✅ Scalable database
- ✅ Real-time capabilities
- ✅ Better AI responses
- ✅ Professional authentication
- ✅ File storage and management
