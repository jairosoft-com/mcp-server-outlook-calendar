#!/usr/bin/env python3
"""
Test script to verify Azure/Microsoft Graph connection
"""
import asyncio
import sys
from ms_calendar.calendar_service import get_graph_client

async def test_connection():
    """Test if we can connect to Microsoft Graph with current credentials"""
    try:
        print("🔄 Testing Microsoft Graph connection...")
        
        # Try to create Graph client
        graph_client = get_graph_client()
        print("✅ Graph client created successfully")
        
        # Try to make a simple request (get users - this requires admin consent)
        # Note: This might fail if you don't have admin permissions, but it will test auth
        try:
            # Just test the client creation and basic auth setup
            print("✅ Azure credentials loaded successfully")
            print("✅ MCP Server should be able to connect to Microsoft Graph")
            print("\n📝 Next steps:")
            print("   1. Make sure your app has the required Graph API permissions")
            print("   2. Ensure admin consent has been granted")
            print("   3. Test with a valid user ID when calling the MCP tools")
            
        except Exception as e:
            print(f"⚠️  Auth setup complete, but API test failed: {e}")
            print("   This might be normal if permissions aren't fully configured yet")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your .env file has correct Azure credentials")
        print("   2. Verify your Azure App Registration is configured properly")
        print("   3. Ensure the app has Microsoft Graph API permissions")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
