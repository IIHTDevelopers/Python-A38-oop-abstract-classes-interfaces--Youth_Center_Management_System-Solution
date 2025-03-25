import pytest
import random
from test.TestUtils import TestUtils
from youth_center_management_system import Person, Counselor, Educator, Volunteer, YouthCenter, PersonNotFoundException, ScheduleConflictException, CertificationException

class TestBoundary:
    """Test cases for boundary conditions in the youth center management system."""
    
    def test_system_boundaries(self):
        """Test all boundary conditions for the youth center management system."""
        try:
            # Person boundary tests - not directly testable since it's abstract
            # Instead test through concrete implementations
            
            # Counselor boundary tests
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            assert counselor.id == "C001"
            assert counselor.name == "Emma Smith"
            assert counselor.specialization == "behavioral"
            assert counselor.case_load == 5
            
            # Test case_load setter boundary conditions
            counselor.case_load = 20  # Max value
            assert counselor.case_load == 20
            
            counselor.case_load = 0  # Min value
            assert counselor.case_load == 0
            
            counselor.case_load = 25  # Above max - should not change or be capped
            assert counselor.case_load <= 20
            
            counselor.case_load = -5  # Below min - should not change or be capped
            assert counselor.case_load >= 0
            
            # Educator boundary tests
            educator = Educator("E001", "John Davis", "mathematics", "Master's")
            assert educator.id == "E001"
            assert educator.name == "John Davis"
            assert educator.subject == "mathematics"
            assert educator.education_level == "Master's"
            
            # Volunteer boundary tests
            volunteer = Volunteer("V001", "Sara Johnson", "weekends")
            assert volunteer.id == "V001"
            assert volunteer.name == "Sara Johnson"
            assert volunteer.availability == "weekends"
            assert volunteer.hours_completed == 0
            
            # Test hours_completed setter boundary conditions
            volunteer.hours_completed = 100
            assert volunteer.hours_completed == 100
            
            volunteer.hours_completed = 0
            assert volunteer.hours_completed == 0
            
            volunteer.hours_completed = -10  # Negative hours should not be accepted
            assert volunteer.hours_completed >= 0
            
            # Scheduling boundary tests
            assert counselor.schedule("2024-03-15", "10:00") is True
            
            # Test scheduling conflict
            try:
                counselor.schedule("2024-03-15", "10:00")  # Same date/time
                assert False, "Should raise ScheduleConflictException"
            except ScheduleConflictException:
                pass  # Expected behavior
            
            # Test different time on same date
            assert counselor.schedule("2024-03-15", "11:00") is True
            
            # Test availability
            assert counselor.is_available("2024-03-15", "10:00") is False
            assert counselor.is_available("2024-03-15", "12:00") is True
            assert counselor.is_available("2024-03-16", "10:00") is True
            
            # Test certification verification
            assert counselor.verify_certification() is True
            assert educator.verify_certification() is True
            
            # Test certification details
            assert "behavioral" in counselor.get_certification_details()
            assert "mathematics" in educator.get_certification_details()
            
            # Volunteer availability boundary tests
            weekend_volunteer = Volunteer("V002", "Weekend Person", "weekends")
            weekday_volunteer = Volunteer("V003", "Weekday Person", "weekdays")
            anytime_volunteer = Volunteer("V004", "Anytime Person", "all")
            
            # Test is_available based on availability pattern
            assert weekend_volunteer.is_available("2024-03-16Sat", "10:00") is True
            assert weekend_volunteer.is_available("2024-03-18Mon", "10:00") is False
            
            assert weekday_volunteer.is_available("2024-03-16Sat", "10:00") is False
            assert weekday_volunteer.is_available("2024-03-18Mon", "10:00") is True
            
            assert anytime_volunteer.is_available("2024-03-16Sat", "10:00") is True
            assert anytime_volunteer.is_available("2024-03-18Mon", "10:00") is True
            
            # Log hours boundary test
            assert volunteer.log_hours(5) is True
            assert volunteer.hours_completed == 5
            
            assert volunteer.log_hours(0) is False  # Zero hours should fail
            assert volunteer.hours_completed == 5  # No change
            
            assert volunteer.log_hours(-1) is False  # Negative hours should fail
            assert volunteer.hours_completed == 5  # No change
            
            # YouthCenter boundary tests
            center = YouthCenter("Test Center")
            assert center.name == "Test Center"
            
            # Test ID generation
            id1 = center.get_next_id("C")
            id2 = center.get_next_id("C")
            assert id2 != id1  # Should generate unique IDs
            
            # Test adding personnel
            assert center.add_person(counselor) is True
            assert center.add_person(educator) is True
            assert center.add_person(volunteer) is True
            
            # Test duplicate personnel
            assert center.add_person(counselor) is False
            
            # Test get personnel by type
            counselors = center.get_personnel_by_type(Counselor)
            assert len(counselors) == 1
            assert counselors[0].id == "C001"
            
            educators = center.get_personnel_by_type(Educator)
            assert len(educators) == 1
            assert educators[0].id == "E001"
            
            # Test personnel counts
            counts = center.get_personnel_count()
            assert counts["Counselor"] == 1
            assert counts["Educator"] == 1
            assert counts["Volunteer"] == 1
            
            # Test personnel finding
            found_person = center.find_person_by_id("C001")
            assert found_person.id == "C001"
            
            # Test non-existent person
            try:
                center.find_person_by_id("NONEXISTENT")
                assert False, "Should raise PersonNotFoundException"
            except PersonNotFoundException:
                pass  # Expected behavior
            
            # Test removing person
            assert center.remove_person("C001") is True
            assert center.remove_person("NONEXISTENT") is False
            
            # Verify count after removal
            counts = center.get_personnel_count()
            assert counts["Counselor"] == 0
            
            # Test activity creation
            assert center.create_activity("Math Tutoring", "2024-03-20", "14:00", "E001") is True
            
            # Test conflict with existing activity
            assert center.create_activity("Extra Tutoring", "2024-03-20", "14:00", "E001") is False
            
            # Test activity with unknown person
            assert center.create_activity("Unknown Person Activity", "2024-03-20", "16:00", "NONEXISTENT") is False
            
            # Test certification verification
            verification_results = center.verify_all_certifications()
            assert len(verification_results) == 1  # Only educator should be certified now
            
            # Add another certified person
            new_counselor = Counselor("C002", "New Counselor", "family", 3)
            center.add_person(new_counselor)
            
            verification_results = center.verify_all_certifications()
            assert len(verification_results) == 2  # Now both educator and new counselor
            
            TestUtils.yakshaAssert("test_system_boundaries", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("test_system_boundaries", False, "boundary")
            raise e