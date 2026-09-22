"""
shapes.py
----------
Q4: Menu-driven program to calculate the area or volume of several
shapes:
  a. Circle              (area)
  b. Sphere               (volume)
  c. Cone                 (volume)
  d. Pyramid              (volume, square base)
  e. Cylinder              (volume)
  f. Rectangle             (area)
  g. Custom regular polygon (area, for any number of sides n)
"""

import math


def circle_area(radius):
    """Area of a circle = pi * r^2."""
    return math.pi * radius ** 2


def sphere_volume(radius):
    """Volume of a sphere = (4/3) * pi * r^3."""
    return (4 / 3) * math.pi * radius ** 3


def cone_volume(radius, height):
    """Volume of a cone = (1/3) * pi * r^2 * h."""
    return (1 / 3) * math.pi * radius ** 2 * height


def pyramid_volume(base_side, height):
    """
    Volume of a (square-base) pyramid = (1/3) * base_area * h.
    base_area is simply base_side^2 for a square base.
    """
    base_area = base_side ** 2
    return (1 / 3) * base_area * height


def cylinder_volume(radius, height):
    """Volume of a cylinder = pi * r^2 * h."""
    return math.pi * radius ** 2 * height


def rectangle_area(length, width):
    """Area of a rectangle = length * width."""
    return length * width


def regular_polygon_area(n, side_length):
    """
    Area of a REGULAR polygon (all sides and angles equal) with n
    sides, given the side length.

    Formula: Area = (n * s^2) / (4 * tan(pi / n))

    This works for any n >= 3 (triangle, pentagon, hexagon, etc.),
    which is why it's used here for the "custom polygonal shape".
    """
    if n < 3:
        raise ValueError("A polygon needs at least 3 sides.")
    return (n * side_length ** 2) / (4 * math.tan(math.pi / n))


def print_menu():
    print("\n" + "=" * 45)
    print(" Area / Volume Calculator")
    print("=" * 45)
    print("a. Circle (area)")
    print("b. Sphere (volume)")
    print("c. Cone (volume)")
    print("d. Pyramid (volume, square base)")
    print("e. Cylinder (volume)")
    print("f. Rectangle (area)")
    print("g. Custom regular polygon (area, any n sides)")
    print("q. Quit")


def main():
    while True:
        print_menu()
        choice = input("Choose a shape (a-g, q to quit): ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        elif choice == "a":
            r = float(input("Enter radius: "))
            print(f"Circle area = {circle_area(r):.4f}")

        elif choice == "b":
            r = float(input("Enter radius: "))
            print(f"Sphere volume = {sphere_volume(r):.4f}")

        elif choice == "c":
            r = float(input("Enter base radius: "))
            h = float(input("Enter height: "))
            print(f"Cone volume = {cone_volume(r, h):.4f}")

        elif choice == "d":
            s = float(input("Enter base side length: "))
            h = float(input("Enter height: "))
            print(f"Pyramid volume = {pyramid_volume(s, h):.4f}")

        elif choice == "e":
            r = float(input("Enter radius: "))
            h = float(input("Enter height: "))
            print(f"Cylinder volume = {cylinder_volume(r, h):.4f}")

        elif choice == "f":
            length = float(input("Enter length: "))
            width = float(input("Enter width: "))
            print(f"Rectangle area = {rectangle_area(length, width):.4f}")

        elif choice == "g":
            n = int(input("Enter number of sides (e.g. 5, 6, 7 ...): "))
            s = float(input("Enter side length: "))
            print(f"Regular {n}-sided polygon area = {regular_polygon_area(n, s):.4f}")

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()