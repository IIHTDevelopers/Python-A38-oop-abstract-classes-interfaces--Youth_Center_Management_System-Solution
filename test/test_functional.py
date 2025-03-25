import pytest
import random
from test.TestUtils import TestUtils
from youth_center_management_system import Person, Counselor, Educator, Volunteer, YouthCenter, PersonNotFoundException, ScheduleConflictException, CertificationException

class TestFunctional:
    """Test cases for functional requirements of the youth center management system."""
    
    def test_person_constructor_destructor(self):
        """Test Person abstract class and derived class constructor/destructor functionality."""
        try:
            # Cannot test Person directly since it's abstract
            # Test through concrete implementations
            initial_count = Person.person_count
            
            # Create different types of personnel
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            assert Person.person_count == initial_count + 1
            
            educator = Educator("E001", "John Davis", "mathematics")
            assert Person.person_count == initial_count + 2
            
            volunteer = Volunteer("V001", "Sara Johnson", "weekends")
            assert Person.person_count == initial_count + 3
            
            # Test property access - inherits from Person
            assert counselor.id == "C001"
            assert counselor.name == "Emma Smith"
            assert counselor.role == "Counselor"
            
            # Force destructor call and test count decrement
            del volunteer
            # Note: Count won't immediately update due to garbage collection timing
            
            TestUtils.yakshaAssert("test_person_constructor_destructor", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_person_constructor_destructor", False, "functional")
            raise e
    
    def test_abstract_class_implementation(self):
        """Test proper implementation of abstract methods."""
        try:
            # Create instances of concrete classes
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            educator = Educator("E001", "John Davis", "mathematics")
            volunteer = Volunteer("V001", "Sara Johnson", "weekends")
            
            # Test display_info abstract method implementation
            counselor_info = counselor.display_info()
            assert "Emma Smith" in counselor_info
            assert "Counselor" in counselor_info
            assert "behavioral" in counselor_info
            
            educator_info = educator.display_info()
            assert "John Davis" in educator_info
            assert "Educator" in educator_info
            assert "mathematics" in educator_info
            
            volunteer_info = volunteer.display_info()
            assert "Sara Johnson" in volunteer_info
            assert "Volunteer" in volunteer_info
            assert "weekends" in volunteer_info
            
            # Test perform_duty abstract method implementation
            counselor_duty = counselor.perform_duty()
            assert "Emma" in counselor_duty
            assert "counseling" in counselor_duty.lower()
            
            educator_duty = educator.perform_duty()
            assert "John" in educator_duty
            assert "teaching" in educator_duty.lower()
            
            volunteer_duty = volunteer.perform_duty()
            assert "Sara" in volunteer_duty or "volunteering" in volunteer_duty.lower()
            
            TestUtils.yakshaAssert("test_abstract_class_implementation", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_abstract_class_implementation", False, "functional")
            raise e
    
    def test_interface_implementation(self):
        """Test proper implementation of interface methods."""
        try:
            # Create instances of classes implementing interfaces
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            educator = Educator("E001", "John Davis", "mathematics")
            volunteer = Volunteer("V001", "Sara Johnson", "weekends")
            
            # Test ISchedulable interface implementation
            # All should implement schedule and is_available
            
            # Counselor (implements ISchedulable, ICertified)
            assert counselor.schedule("2024-03-15", "10:00") is True
            assert counselor.is_available("2024-03-15", "10:00") is False
            assert counselor.is_available("2024-03-16", "10:00") is True
            
            # Test ICertified interface implementation
            assert counselor.verify_certification() is True
            cert_details = counselor.get_certification_details()
            assert "behavioral" in cert_details
            assert "expires" in cert_details
            
            # Educator (implements ISchedulable, ICertified)
            assert educator.schedule("2024-03-15", "14:00") is True
            assert educator.is_available("2024-03-15", "14:00") is False
            assert educator.is_available("2024-03-15", "15:00") is True
            
            assert educator.verify_certification() is True
            cert_details = educator.get_certification_details()
            assert "mathematics" in cert_details
            assert "expires" in cert_details
            
            # Volunteer (implements only ISchedulable)
            # Weekend volunteer should be available on weekends
            assert volunteer.is_available("2024-03-16Sat", "10:00") is True
            assert volunteer.schedule("2024-03-16Sat", "10:00") is True
            assert volunteer.is_available("2024-03-16Sat", "10:00") is False
            
            # Test volunteer-specific method
            assert volunteer.log_hours(5) is True
            assert volunteer.hours_completed == 5
            
            TestUtils.yakshaAssert("test_interface_implementation", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_interface_implementation", False, "functional")
            raise e
    
    def test_youth_center_functionality(self):
        """Test YouthCenter class and management functionality."""
        try:
            # Create youth center
            center = YouthCenter("BrightFuture Youth Center")
            assert center.name == "BrightFuture Youth Center"
            
            # Add various personnel
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            educator = Educator("E001", "John Davis", "mathematics")
            volunteer = Volunteer("V001", "Sara Johnson", "weekends")
            
            center.add_person(counselor)
            center.add_person(educator)
            center.add_person(volunteer)
            
            # Test personnel management
            assert len(center.personnel) == 3
            
            # Test get_personnel_by_type
            counselors = center.get_personnel_by_type(Counselor)
            educators = center.get_personnel_by_type(Educator)
            volunteers = center.get_personnel_by_type(Volunteer)
            
            assert len(counselors) == 1 and counselors[0].id == "C001"
            assert len(educators) == 1 and educators[0].id == "E001"
            assert len(volunteers) == 1 and volunteers[0].id == "V001"
            
            # Test personnel count
            counts = center.get_personnel_count()
            assert counts["Counselor"] == 1
            assert counts["Educator"] == 1
            assert counts["Volunteer"] == 1
            
            # Test find_person_by_id
            found_counselor = center.find_person_by_id("C001")
            assert found_counselor.id == "C001" and found_counselor.name == "Emma Smith"
            
            # Test activity scheduling
            result = center.create_activity("Math Tutoring", "2024-03-15", "14:00", "E001")
            assert result is True
            
            # Verify the activity was created in activities
            assert "Math Tutoring" in center.activities
            
            # Test scheduling conflict
            result = center.create_activity("Another Math Session", "2024-03-15", "14:00", "E001")
            assert result is False
            
            # Test certification verification
            verification_results = center.verify_all_certifications()
            assert len(verification_results) == 2  # Both counselor and educator should have certifications
            
            # Count valid certifications
            valid_certs = sum(1 for result in verification_results if result["certification_valid"])
            assert valid_certs == 2
            
            # Test removal of personnel
            assert center.remove_person("C001") is True
            counts = center.get_personnel_count()
            assert counts["Counselor"] == 0
            
            # Try finding deleted person
            try:
                center.find_person_by_id("C001")
                assert False, "Should raise PersonNotFoundException"
            except PersonNotFoundException:
                pass  # Expected behavior
            
            TestUtils.yakshaAssert("test_youth_center_functionality", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_youth_center_functionality", False, "functional")
            raise e
    
    def test_property_implementation(self):
        """Test proper implementation of properties across classes."""
        try:
            # Test Counselor properties
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            assert counselor.id == "C001"  # From Person
            assert counselor.name == "Emma Smith"  # From Person
            assert counselor.role == "Counselor"  # From Person
            assert counselor.specialization == "behavioral"  # Counselor-specific
            assert counselor.case_load == 5  # Counselor-specific with setter
            
            # Test case_load setter with validation
            counselor.case_load = 15
            assert counselor.case_load == 15
            
            counselor.case_load = 25  # Should be rejected or capped
            assert counselor.case_load <= 20
            
            counselor.case_load = -5  # Should be rejected or capped
            assert counselor.case_load >= 0
            
            # Test Educator properties
            educator = Educator("E001", "John Davis", "mathematics", "PhD")
            assert educator.id == "E001"  # From Person
            assert educator.name == "John Davis"  # From Person
            assert educator.role == "Educator"  # From Person
            assert educator.subject == "mathematics"  # Educator-specific
            assert educator.education_level == "PhD"  # Educator-specific
            
            # Test Volunteer properties
            volunteer = Volunteer("V001", "Sara Johnson", "weekends")
            assert volunteer.id == "V001"  # From Person
            assert volunteer.name == "Sara Johnson"  # From Person
            assert volunteer.role == "Volunteer"  # From Person
            assert volunteer.availability == "weekends"  # Volunteer-specific
            assert volunteer.hours_completed == 0  # Volunteer-specific with setter
            
            # Test hours_completed setter with validation
            volunteer.hours_completed = 10
            assert volunteer.hours_completed == 10
            
            volunteer.hours_completed = -5  # Should be rejected
            assert volunteer.hours_completed == 10  # Unchanged
            
            # Test YouthCenter properties
            center = YouthCenter("Test Center")
            assert center.name == "Test Center"
            
            # Test personnel list immutability
            personnel_list = center.personnel
            center.add_person(counselor)
            
            # Original list should be a copy and not affected by subsequent additions
            assert len(personnel_list) == 0
            assert len(center.personnel) == 1
            
            # Test activities dictionary immutability
            activities_dict = center.activities
            center.create_activity("Test Activity", "2024-03-15", "10:00", "C001")
            
            # Original dict should be a copy and not affected by subsequent additions
            assert len(activities_dict) == 0
            assert len(center.activities) == 1
            
            TestUtils.yakshaAssert("test_property_implementation", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_property_implementation", False, "functional")
            raise e
    
    def test_encapsulation(self):
        """Test proper encapsulation of attributes."""
        try:
            # Create objects for testing
            counselor = Counselor("C001", "Emma Smith", "behavioral", 5)
            center = YouthCenter("Test Center")
            
            # Test protected attributes (_prefix) access
            # Direct access should be avoided, we test through properties
            assert counselor.id == "C001"  # Access through property
            
            # For YouthCenter, attributes should be private (__prefix)
            # Direct access would raise AttributeError, so we test through properties
            assert center.name == "Test Center"  # Access through property
            
            # Add a counselor and test operations that use private attributes
            center.add_person(counselor)
            
            # Test operations that would use private attributes internally
            found_person = center.find_person_by_id("C001")
            assert found_person.id == "C001"
            
            center.create_activity("Counseling Session", "2024-03-15", "10:00", "C001")
            
            # Test get_next_id functionality (uses private counter)
            id1 = center.get_next_id("C")
            id2 = center.get_next_id("C")
            assert id1 != id2  # Should be different
            
            TestUtils.yakshaAssert("test_encapsulation", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_encapsulation", False, "functional")
            raise e