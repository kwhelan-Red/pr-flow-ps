#!/usr/bin/env python3
"""
Jira Cookie-Based Authentication
For Red Hat Jira and other instances that require session-based authentication
"""

import requests
import sys

def test_with_cookie(jira_url: str, jsessionid: str):
    """Test Jira connection using JSESSIONID cookie"""
    url = jira_url.rstrip('/')
    api_url = f"{url}/rest/api/3"
    
    session = requests.Session()
    session.cookies.set('JSESSIONID', jsessionid)
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })
    
    try:
        response = session.get(f"{api_url}/myself")
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Successfully connected to Jira!")
            print(f"   User: {user_data.get('displayName', 'N/A')}")
            print(f"   Email: {user_data.get('emailAddress', 'N/A')}")
            print(f"   Account ID: {user_data.get('accountId', 'N/A')}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 80)
    print("JIRA COOKIE-BASED AUTHENTICATION")
    print("=" * 80)
    print("\nTo get your JSESSIONID cookie:")
    print("1. Log into https://issues.redhat.com in your browser")
    print("2. Open Developer Tools (F12)")
    print("3. Go to Application/Storage → Cookies")
    print("4. Find the JSESSIONID cookie value")
    print("5. Copy the entire value")
    print("\n" + "=" * 80)
    
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  python check_jira_cookie.py <jira_url> <jsessionid>")
        print("\nExample:")
        print("  python check_jira_cookie.py https://issues.redhat.com ABC123DEF456...")
        sys.exit(1)
    
    jira_url = sys.argv[1]
    jsessionid = sys.argv[2]
    
    test_with_cookie(jira_url, jsessionid)




