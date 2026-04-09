#!/usr/bin/env python3
"""
Backend API Testing for CultGig Landing Page
Tests health endpoints and waitlist functionality
"""

import requests
import sys
import json
from datetime import datetime

class CultGigAPITester:
    def __init__(self, base_url="https://artist-hub-3d.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)}")
                    return True, response_data
                except:
                    print(f"   Response: {response.text}")
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text}")
                self.failed_tests.append({
                    "test": name,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "response": response.text
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "error": str(e)
            })
            return False, {}

    def test_health_endpoints(self):
        """Test basic health check endpoints"""
        print("\n" + "="*50)
        print("TESTING HEALTH ENDPOINTS")
        print("="*50)
        
        # Test root endpoint
        self.run_test(
            "Root Health Check",
            "GET",
            "api/",
            200
        )
        
        # Test detailed health endpoint
        self.run_test(
            "Detailed Health Check",
            "GET", 
            "api/health",
            200
        )

    def test_waitlist_endpoints(self):
        """Test waitlist functionality"""
        print("\n" + "="*50)
        print("TESTING WAITLIST ENDPOINTS")
        print("="*50)
        
        # Test getting waitlist count
        self.run_test(
            "Get Waitlist Count",
            "GET",
            "api/waitlist/count",
            200
        )
        
        # Test getting all waitlist entries
        self.run_test(
            "Get All Waitlist Entries",
            "GET",
            "api/waitlist",
            200
        )
        
        # Test adding to waitlist - Artist
        test_timestamp = datetime.now().strftime('%H%M%S')
        artist_data = {
            "name": f"Test Artist {test_timestamp}",
            "email": f"artist{test_timestamp}@test.com",
            "whatsapp": f"+91 9876543{test_timestamp[-3:]}",
            "role": "artist"
        }
        
        success, response = self.run_test(
            "Add Artist to Waitlist",
            "POST",
            "api/waitlist",
            201,
            data=artist_data
        )
        
        if success and isinstance(response, dict) and 'id' in response:
            print(f"   Created waitlist entry with ID: {response['id']}")
        
        # Test adding to waitlist - Business
        business_data = {
            "name": f"Test Business {test_timestamp}",
            "email": f"business{test_timestamp}@test.com",
            "whatsapp": f"+1 555123{test_timestamp[-4:]}",
            "role": "business"
        }
        
        self.run_test(
            "Add Business to Waitlist",
            "POST",
            "api/waitlist",
            201,
            data=business_data
        )

    def test_invalid_requests(self):
        """Test error handling"""
        print("\n" + "="*50)
        print("TESTING ERROR HANDLING")
        print("="*50)
        
        # Test missing fields (should return 400)
        missing_fields_data = {
            "name": "Test User",
            "email": "test@example.com"
            # Missing whatsapp and role
        }
        
        self.run_test(
            "Missing Required Fields",
            "POST",
            "api/waitlist",
            400,
            data=missing_fields_data
        )
        
        # Test duplicate email (should return 409)
        # Using john@cultgig.com which exists in DB according to context
        duplicate_data = {
            "name": "John Duplicate",
            "email": "john@cultgig.com",
            "whatsapp": "+91 9876543210",
            "role": "artist"
        }
        
        self.run_test(
            "Duplicate Email",
            "POST",
            "api/waitlist",
            409,
            data=duplicate_data
        )
        
        # Test invalid email format
        invalid_email_data = {
            "name": "Test User",
            "email": "invalid-email",
            "whatsapp": "+91 9876543210",
            "role": "artist"
        }
        
        self.run_test(
            "Invalid Email Format",
            "POST",
            "api/waitlist",
            400,  # Should validate email format
            data=invalid_email_data
        )

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"📊 Tests passed: {self.tests_passed}/{self.tests_run}")
        
        if self.failed_tests:
            print(f"\n❌ Failed tests:")
            for test in self.failed_tests:
                print(f"   - {test['test']}")
                if 'error' in test:
                    print(f"     Error: {test['error']}")
                else:
                    print(f"     Expected: {test['expected']}, Got: {test['actual']}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\n📈 Success rate: {success_rate:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    print("🚀 Starting CultGig API Tests")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = CultGigAPITester()
    
    # Run all test suites
    tester.test_health_endpoints()
    tester.test_waitlist_endpoints()
    tester.test_invalid_requests()
    
    # Print final summary
    all_passed = tester.print_summary()
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())