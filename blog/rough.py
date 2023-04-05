class Uniblog:
    def __init__(self, name, course, department):
        self.name = name
        self.course = course
        self.department = department


class College:
    def __init__(self) -> None:
        self.university = [
            Uniblog("Favour", "Thermodynamics", "Mechanical Engineering"),
            Uniblog("Collins", "Python Programming", "Computer Science"),
            Uniblog("Benji", "3D Simulation", "Machine Design")
        ]

college = College()
for uni in college:
    print(uni)
# for uni in university:
#     print(f"My name is {uni.name}, I am currently studying {uni.course}, a {uni.course} course")
    # print(uni.name, uni.course)