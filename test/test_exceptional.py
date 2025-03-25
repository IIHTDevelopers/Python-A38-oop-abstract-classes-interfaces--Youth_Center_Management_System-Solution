import pytest
import random
from test.TestUtils import TestUtils
from youth_center_management_system import Person, Counselor, Educator, Volunteer, YouthCenter, PersonNotFoundException, ScheduleConflictException, CertificationException

class TestExceptional:
    """Test cases for exceptional conditions in the youth center management system."""
    
    def test_exception_handling(self):
        """Test all exception handling across the youth center management system."""
        try:
            # We can't test Person directly since it's abstract
            # Testing Counselor exceptions
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            
            # Test scheduling conflicts
            counselor.schedule("2024-03-15", "10:00")  # Schedule first session
            
            try:
                counselor.schedule("2024-03-15", "10:00")  # Same date/time
                assert False, "Should raise ScheduleConflictException"
            except ScheduleConflictException:
                pass  # Expected behavior
            
            # Test expiration date for certification
            valid_counselor = Counselor("C002", "Valid Cert", "family", 3, "2025-12-31")
            expired_counselor = Counselor("C003", "Expired Cert", "crisis", 2, "2022-12-31")
            
            assert valid_counselor.verify_certification() is True
            assert expired_counselor.verify_certification() is False
            
            # Test certification details
            assert "family" in valid_counselor.get_certification_details()
            assert "expires" in valid_counselor.get_certification_details()
            
            # Test Educator exceptions
            educator = Educator("E001", "John Davis", "mathematics")
            
            # Test scheduling conflicts
            educator.schedule("2024-03-15", "10:00")  # Schedule first class
            
            try:
                educator.schedule("2024-03-15", "10:00")  # Same date/time
                assert False, "Should raise ScheduleConflictException"
            except ScheduleConflictException:
                pass  # Expected behavior
            
            # Test expiration date for certification
            valid_educator = Educator("E002", "Valid Cert", "science", "PhD", "2025-12-31")
            expired_educator = Educator("E003", "Expired Cert", "history", "Master's", "2022-12-31")
            
            assert valid_educator.verify_certification() is True
            assert expired_educator.verify_certification() is False
            
            # Test Volunteer exceptions
            volunteer = Volunteer("V001", "Sara Johnson", "weekends")
            
            # Test scheduling for unavailable times
            try:
                # Try to schedule for a weekday when only available on weekends
                result = volunteer.schedule("2024-03-18Mon", "10:00")
                # If implementation doesn't throw exception but returns False, that's also valid
                assert result is False, "Should either raise exception or return False for invalid schedule"
            except ScheduleConflictException:
                pass  # This is also acceptable behavior
            
            # Successful scheduling for available time
            assert volunteer.schedule("2024-03-16Sat", "10:00") is True
            
            # Test duplicate scheduling
            try:
                volunteer.schedule("2024-03-16Sat", "10:00")  # Same date/time
                assert False, "Should raise ScheduleConflictException"
            except ScheduleConflictException:
                pass  # Expected behavior
            
            # Test logging hours
            assert volunteer.log_hours(5) is True
            assert volunteer.log_hours(-5) is False  # Negative hours
            assert volunteer.log_hours(0) is False   # Zero hours
            
            # YouthCenter exceptions
            center = YouthCenter("Test Center")
            
            # Test finding non-existent person
            try:
                center.find_person_by_id("NONEXISTENT")
                assert False, "Should raise PersonNotFoundException for non-existent ID"
            except PersonNotFoundException:
                pass  # Expected behavior
            
            # Test removing non-existent person
            assert center.remove_person("NONEXISTENT") is False
            
            # Test personnel list immutability
            personnel_copy = center.personnel
            
            # Add a test person to the center
            test_person = Counselor("TEST", "Test Person", "test", 1)
            center.add_person(test_person)
            
            # Modify the copy (should not affect original)
            if len(personnel_copy) > 0:
                personnel_copy.pop()
            
            # Verify center's personnel list wasn't affected
            assert len(center.personnel) == 1
            
            # Test duplicate person addition
            assert center.add_person(test_person) is False
            
            # Test activity creation with non-schedulable person
            # This is a bit tricky since all our person types implement ISchedulable
            # For the test, we could use a mock or just test the failure path
            
            # Test with non-existent person
            assert center.create_activity("Math Class", "2024-03-20", "14:00", "NONEXISTENT") is False
            
            # Create a new center for certification tests to avoid counting test_person
            cert_center = YouthCenter("Certification Test Center")
            
            # Test certification verification system
            # Add people with mixed certification status to new center
            cert_center.add_person(valid_counselor)
            cert_center.add_person(expired_counselor)
            cert_center.add_person(valid_educator)
            cert_center.add_person(expired_educator)
            cert_center.add_person(volunteer)  # Not certified
            
            verification_results = cert_center.verify_all_certifications()
            
            # Should have 4 certification results (2 valid, 2 invalid)
            assert len(verification_results) == 4
            
            # Count valid and invalid certifications
            valid_count = sum(1 for result in verification_results if result["certification_valid"])
            invalid_count = sum(1 for result in verification_results if not result["certification_valid"])
            
            assert valid_count == 2
            assert invalid_count == 2
            
            # Test scheduling conflict in activity creation
            # First, create a valid activity
            assert cert_center.create_activity("Math Class", "2024-03-21", "14:00", "E002") is True
            
            # Now try to create another activity at the same time
            assert cert_center.create_activity("Another Class", "2024-03-21", "14:00", "E002") is False
            
            # Test creating activity with volunteer at wrong time
            weekend_volunteer = Volunteer("V002", "Weekend Only", "weekends")
            cert_center.add_person(weekend_volunteer)
            
            # Try to schedule on a weekday
            assert cert_center.create_activity("Weekend Activity", "2024-03-18Mon", "14:00", "V002") is False
            
            # Should work on a weekend
            assert cert_center.create_activity("Weekend Activity", "2024-03-16Sat", "14:00", "V002") is True
            
            # Test scenarios with empty center
            empty_center = YouthCenter("Empty Center")
            
            # Verify empty counts
            counts = empty_center.get_personnel_count()
            assert counts["Counselor"] == 0
            assert counts["Educator"] == 0
            assert counts["Volunteer"] == 0
            
            # Verify empty personnel lists
            assert len(empty_center.get_personnel_by_type(Counselor)) == 0
            assert len(empty_center.get_personnel_by_type(Educator)) == 0
            assert len(empty_center.get_personnel_by_type(Volunteer)) == 0
            
            # Verify empty certification list
            assert len(empty_center.verify_all_certifications()) == 0
            
            # Test activities dictionary immutability (if applicable)
            activities_copy = cert_center.activities
            # Try to modify the copy
            if isinstance(activities_copy, dict) and len(activities_copy) > 0:
                first_key = next(iter(activities_copy))
                activities_copy[first_key] = []
            
            # The original should be unchanged - this depends on your implementation
            # Either the copy is completely separate, or modifications shouldn't affect the original
            
            TestUtils.yakshaAssert("test_exception_handling", True, "exceptional")
        except Exception as e:
            TestUtils.yakshaAssert("test_exception_handling", False, "exceptional")
            raise e