#include <iostream>
#include <string>
#include "formatter_ex.h"
#include "solver.h"

int main()
{
    float a, b, c, x1, x2;
    
    std::cout << "Enter coefficients a, b, c: ";
    std::cin >> a >> b >> c;
    
    solve(a, b, c, x1, x2);
    
    std::string output = "Equation: " + std::to_string(a) + "x^2 + " + std::to_string(b) + "x + " + std::to_string(c) + " = 0\n";
    output += "Roots: x1 = " + std::to_string(x1) + ", x2 = " + std::to_string(x2) + "\n";
    
    formatter(std::cout, output);
    
    return 0;
}
