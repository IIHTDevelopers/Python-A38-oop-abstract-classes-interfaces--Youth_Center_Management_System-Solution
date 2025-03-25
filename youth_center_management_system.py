"""
Youth Center Management System

This module implements a management system for BrightFuture Foundation's youth center
to demonstrate abstract classes and interfaces through object-oriented programming.
"""

import random
from abc import ABC, abstractmethod


class PersonNotFoundException(Exception):
    """Exception raised when a person is not found in the youth center."""
    pass


class ScheduleConflictException(Exception):
    """Exception raised when there is a scheduling conflict."""
    pass


class CertificationException(Exception):
    """Exception raised when certification verification fails."""
    pass


class Person(ABC):
    """Abstract base class representing any person at the youth center."""
    
    person_count = 0
    
    def __init__(self, id, name, role):
        """Initialize a Person with required attributes."""
        self._id = id
        self._name = name
        self._role = role
        
        # Increment person count
        Person.person_count += 1
    
    def __del__(self):
        """Clean up resources when the object is destroyed."""
        Person.person_count -= 1
    
    @property
    def id(self): return self._id
    
    @property
    def name(self): return self._name
    
    @property
    def role(self): return self._role
    
    @abstractmethod
    def display_info(self):
        """Display person information."""
        pass
    
    @abstractmethod
    def perform_duty(self):
        """Perform the person's primary duty."""
        pass


class ISchedulable:
    """Interface for objects that can be scheduled."""
    
    @abstractmethod
    def schedule(self, date, time):
        """Schedule an activity at a specific date and time."""
        pass
    
    @abstractmethod
    def is_available(self, date, time):
        """Check if available at a specific date and time."""
        pass


class ICertified:
    """Interface for objects that require certification."""
    
    @abstractmethod
    def verify_certification(self):
        """Verify that certification is valid."""
        pass
    
    @abstractmethod
    def get_certification_details(self):
        """Get details about the certification."""
        pass


class Counselor(Person, ISchedulable, ICertified):
    """Class representing counselors at the youth center."""
    
    def __init__(self, id, name, specialization, case_load=0, certification_expiry="2025-12-31"):
        """Initialize a Counselor with required attributes."""
        super().__init__(id, name, "Counselor")
        self._specialization = specialization
        self._case_load = case_load
        self._certification_expiry = certification_expiry
        self._schedule = {}
    
    @property
    def specialization(self): return self._specialization
    
    @property
    def case_load(self): return self._case_load
    
    @case_load.setter
    def case_load(self, value):
        if 0 <= value <= 20:
            self._case_load = value
    
    def perform_duty(self):
        """Perform counseling duties."""
        return f"{self._name} is providing {self._specialization} counseling to youth."
    
    def display_info(self):
        """Display counselor-specific information."""
        return f"ID: {self._id} | Name: {self._name} | Role: {self._role} | " \
               f"Specialization: {self._specialization} | Case Load: {self._case_load}"
    
    def schedule(self, date, time):
        """Schedule a counseling session."""
        if self.is_available(date, time):
            if date not in self._schedule:
                self._schedule[date] = []
            self._schedule[date].append(time)
            return True
        else:
            raise ScheduleConflictException(f"{self._name} already has a session at {date} {time}")
    
    def is_available(self, date, time):
        """Check if available for a session."""
        return date not in self._schedule or time not in self._schedule[date]
    
    def verify_certification(self):
        """Verify counseling certification."""
        # Simple validation - in a real system, this would check against a database
        return True if self._certification_expiry > "2023-01-01" else False
    
    def get_certification_details(self):
        """Get certification details."""
        return f"Certification in {self._specialization} counseling, expires: {self._certification_expiry}"


class Educator(Person, ISchedulable, ICertified):
    """Class representing educators at the youth center."""
    
    def __init__(self, id, name, subject, education_level="Bachelor's", certification_expiry="2025-12-31"):
        """Initialize an Educator with required attributes."""
        super().__init__(id, name, "Educator")
        self._subject = subject
        self._education_level = education_level
        self._certification_expiry = certification_expiry
        self._schedule = {}
    
    @property
    def subject(self): return self._subject
    
    @property
    def education_level(self): return self._education_level
    
    def perform_duty(self):
        """Perform teaching duties."""
        return f"{self._name} is teaching {self._subject} to youth."
    
    def display_info(self):
        """Display educator-specific information."""
        return f"ID: {self._id} | Name: {self._name} | Role: {self._role} | " \
               f"Subject: {self._subject} | Education: {self._education_level}"
    
    def schedule(self, date, time):
        """Schedule a class."""
        if self.is_available(date, time):
            if date not in self._schedule:
                self._schedule[date] = []
            self._schedule[date].append(time)
            return True
        else:
            raise ScheduleConflictException(f"{self._name} already has a class at {date} {time}")
    
    def is_available(self, date, time):
        """Check if available for a class."""
        return date not in self._schedule or time not in self._schedule[date]
    
    def verify_certification(self):
        """Verify teaching certification."""
        return True if self._certification_expiry > "2023-01-01" else False
    
    def get_certification_details(self):
        """Get certification details."""
        return f"Teaching certification in {self._subject}, expires: {self._certification_expiry}"


class Volunteer(Person, ISchedulable):
    """Class representing volunteers at the youth center."""
    
    def __init__(self, id, name, availability):
        """Initialize a Volunteer with required attributes."""
        super().__init__(id, name, "Volunteer")
        self._availability = availability
        self._hours_completed = 0
        self._schedule = {}
    
    @property
    def availability(self): return self._availability
    
    @property
    def hours_completed(self): return self._hours_completed
    
    @hours_completed.setter
    def hours_completed(self, value):
        if value >= 0:
            self._hours_completed = value
    
    def perform_duty(self):
        """Perform volunteer duties."""
        return f"{self._name} is volunteering at the youth center."
    
    def display_info(self):
        """Display volunteer-specific information."""
        return f"ID: {self._id} | Name: {self._name} | Role: {self._role} | " \
               f"Availability: {self._availability} | Hours: {self._hours_completed}"
    
    def schedule(self, date, time):
        """Schedule volunteer time."""
        # Check if already scheduled
        if date in self._schedule and time in self._schedule[date]:
            raise ScheduleConflictException(f"{self._name} already has a session at {date} {time}")
            
        if self.is_available(date, time):
            if date not in self._schedule:
                self._schedule[date] = []
            self._schedule[date].append(time)
            return True
        else:
            raise ScheduleConflictException(f"{self._name} is not available at {date} {time}")
    
    def is_available(self, date, time):
        """Check if available to volunteer."""
        # Check if already scheduled
        if date in self._schedule and time in self._schedule[date]:
            return False
            
        # Simple availability check based on day of week
        if self._availability == "weekends" and date.endswith("Sat") or date.endswith("Sun"):
            return True
        elif self._availability == "weekdays" and not (date.endswith("Sat") or date.endswith("Sun")):
            return True
        elif self._availability == "all":
            return True
        else:
            return False
    
    def log_hours(self, hours):
        """Log completed volunteer hours."""
        if hours > 0:
            self._hours_completed += hours
            return True
        return False


class YouthCenter:
    """Class representing the youth center."""
    
    def __init__(self, name):
        """Initialize a YouthCenter with required attributes."""
        self.__name = name
        self.__personnel = []
        self.__activities = {}
        self.__next_id = 1
    
    @property
    def name(self): return self.__name
    
    @property
    def personnel(self): return self.__personnel.copy()
    
    @property
    def activities(self): return self.__activities.copy()
    
    def get_next_id(self, role_prefix):
        """Get next available ID for a new person."""
        id_val = self.__next_id
        self.__next_id += 1
        return f"{role_prefix}{id_val:03d}"
    
    def add_person(self, person):
        """Add a person to the youth center."""
        # Check if person already exists
        if any(p.id == person.id for p in self.__personnel):
            return False
        
        self.__personnel.append(person)
        return True
    
    def remove_person(self, person_id):
        """Remove a person from the youth center."""
        for i, person in enumerate(self.__personnel):
            if person.id == person_id:
                self.__personnel.pop(i)
                return True
        
        return False
    
    def find_person_by_id(self, person_id):
        """Find a person by ID."""
        for person in self.__personnel:
            if person.id == person_id:
                return person
        
        raise PersonNotFoundException(f"Person with ID {person_id} not found")
    
    def get_personnel_by_type(self, person_class):
        """Get all personnel of a specific type."""
        return [p for p in self.__personnel if isinstance(p, person_class)]
    
    def get_personnel_count(self):
        """Get personnel counts by type."""
        counts = {
            "Counselor": len(self.get_personnel_by_type(Counselor)),
            "Educator": len(self.get_personnel_by_type(Educator)),
            "Volunteer": len(self.get_personnel_by_type(Volunteer))
        }
        
        return counts
    
    def create_activity(self, name, date, time, responsible_person_id):
        """Create a new activity at the youth center."""
        try:
            person = self.find_person_by_id(responsible_person_id)
            
            # Check if person can be scheduled
            if isinstance(person, ISchedulable):
                if person.schedule(date, time):
                    if name not in self.__activities:
                        self.__activities[name] = []
                    
                    self.__activities[name].append({
                        "date": date,
                        "time": time,
                        "responsible": person.id
                    })
                    return True
            else:
                return False
                
        except (PersonNotFoundException, ScheduleConflictException):
            return False
        
        return False
    
    def verify_all_certifications(self):
        """Verify certifications for all staff who require them."""
        results = []
        
        for person in self.__personnel:
            if isinstance(person, ICertified):
                is_valid = person.verify_certification()
                results.append({
                    "id": person.id,
                    "name": person.name,
                    "certification_valid": is_valid,
                    "details": person.get_certification_details() if is_valid else "Certification invalid or expired"
                })
        
        return results


def main():
    """Main function to run the youth center management system."""
    # Create youth center
    center = YouthCenter("BrightFuture Youth Center")
    
    # Add initial personnel
    try:
        # Counselors
        center.add_person(Counselor("C001", "Emma Smith", "behavioral", 5))
        center.add_person(Counselor("C002", "Michael Jones", "family", 3))
        
        # Educators
        center.add_person(Educator("E001", "John Davis", "mathematics"))
        
        # Volunteers
        center.add_person(Volunteer("V001", "Sara Johnson", "weekends"))
    except Exception as e:
        print(f"Error setting up youth center: {e}")
    
    # Menu-based interaction
    while True:
        print("\n===== YOUTH CENTER MANAGEMENT SYSTEM =====")
        print(f"Center: {center.name}")
        
        counts = center.get_personnel_count()
        print("\nPersonnel Breakdown:")
        for role, count in counts.items():
            print(f"  {role}s: {count}")
        
        print("\nMenu:")
        print("1. Add Person")
        print("2. Schedule Activity")
        print("3. Display All Personnel")
        print("4. Verify Certifications")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-4): "))
            
            if choice == 1:
                print("\nSelect person type:")
                print("1. Counselor")
                print("2. Educator")
                print("3. Volunteer")
                
                person_type = int(input("Enter choice (1-3): "))
                
                # Common attributes
                if person_type == 1:
                    id_prefix = "C"
                    type_name = "Counselor"
                elif person_type == 2:
                    id_prefix = "E"
                    type_name = "Educator"
                elif person_type == 3:
                    id_prefix = "V"
                    type_name = "Volunteer"
                else:
                    raise ValueError("Invalid person type")
                
                person_id = center.get_next_id(id_prefix)
                name = input("Enter name: ")
                
                # Create person based on type
                try:
                    if person_type == 1:  # Counselor
                        specializations = ["behavioral", "family", "crisis", "youth", "career"]
                        print("\nSelect specialization:")
                        for i, spec in enumerate(specializations, 1):
                            print(f"{i}. {spec}")
                        
                        spec_choice = int(input("Enter choice (1-5): "))
                        if 1 <= spec_choice <= len(specializations):
                            specialization = specializations[spec_choice-1]
                        else:
                            raise ValueError("Invalid specialization")
                            
                        case_load = int(input("Enter current case load (0-20): "))
                        if not (0 <= case_load <= 20):
                            raise ValueError("Case load must be between 0 and 20")
                            
                        person = Counselor(person_id, name, specialization, case_load)
                    
                    elif person_type == 2:  # Educator
                        subjects = ["mathematics", "science", "language", "arts", "music"]
                        print("\nSelect subject:")
                        for i, subj in enumerate(subjects, 1):
                            print(f"{i}. {subj}")
                        
                        subj_choice = int(input("Enter choice (1-5): "))
                        if 1 <= subj_choice <= len(subjects):
                            subject = subjects[subj_choice-1]
                        else:
                            raise ValueError("Invalid subject")
                            
                        education_levels = ["Bachelor's", "Master's", "PhD"]
                        print("\nSelect education level:")
                        for i, level in enumerate(education_levels, 1):
                            print(f"{i}. {level}")
                        
                        level_choice = int(input("Enter choice (1-3): "))
                        if 1 <= level_choice <= len(education_levels):
                            education_level = education_levels[level_choice-1]
                        else:
                            raise ValueError("Invalid education level")
                            
                        person = Educator(person_id, name, subject, education_level)
                    
                    elif person_type == 3:  # Volunteer
                        availabilities = ["weekends", "weekdays", "evenings", "all"]
                        print("\nSelect availability:")
                        for i, avail in enumerate(availabilities, 1):
                            print(f"{i}. {avail}")
                        
                        avail_choice = int(input("Enter choice (1-4): "))
                        if 1 <= avail_choice <= len(availabilities):
                            availability = availabilities[avail_choice-1]
                        else:
                            raise ValueError("Invalid availability")
                            
                        person = Volunteer(person_id, name, availability)
                    
                    # Add to youth center
                    if center.add_person(person):
                        print(f"{type_name} '{person_id}' added successfully.")
                    else:
                        print(f"Person with ID {person_id} already exists.")
                
                except Exception as e:
                    print(f"Error adding person: {e}")
            
            elif choice == 2:
                try:
                    # Display personnel
                    print("\nAvailable Personnel:")
                    for i, person in enumerate(center.personnel, 1):
                        print(f"{i}. {person.id} - {person.name} ({person.role})")
                    
                    person_index = int(input("\nSelect person (by number): ")) - 1
                    if 0 <= person_index < len(center.personnel):
                        selected_person = center.personnel[person_index]
                        
                        if not isinstance(selected_person, ISchedulable):
                            print(f"Error: {selected_person.name} cannot be scheduled.")
                            continue
                        
                        activity_name = input("Enter activity name: ")
                        activity_date = input("Enter date (e.g., 2023-06-15): ")
                        activity_time = input("Enter time (e.g., 14:00): ")
                        
                        if center.create_activity(activity_name, activity_date, activity_time, selected_person.id):
                            print(f"Activity '{activity_name}' scheduled successfully.")
                        else:
                            print("Failed to schedule activity. Check for schedule conflicts.")
                    else:
                        print("Invalid selection.")
                
                except Exception as e:
                    print(f"Error scheduling activity: {e}")
            
            elif choice == 3:
                print("\nAll Personnel:")
                for person in center.personnel:
                    print(person.display_info())
            
            elif choice == 4:
                results = center.verify_all_certifications()
                
                if results:
                    print("\nCertification Verification Results:")
                    for result in results:
                        status = "VALID" if result["certification_valid"] else "INVALID"
                        print(f"{result['id']} | {result['name']} | Status: {status}")
                        print(f"  Details: {result['details']}")
                else:
                    print("No certifications to verify.")
            
            elif choice == 0:
                print("Thank you for using the Youth Center Management System.")
                break
            
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")
        
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()