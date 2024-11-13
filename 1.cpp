#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <fstream>

using namespace std;

struct Expense {
    string date;
    double amount;
    string category;
};

int main() {
    vector<Expense> expenses;
    map<string, double> category_totals;

    // ... (same input and storage logic as before)

    // Write data to a file for gnuplot
    ofstream dataFile("expenses.dat");
    for (auto& [category, amount] : category_totals) {
        dataFile << category << " " << amount << endl;
    }
    dataFile.close();

    // Create a gnuplot script
    ofstream scriptFile("plot.gp");
    scriptFile << "set terminal png\n";
    scriptFile << "set output 'expense_plot.png'\n";
    scriptFile << "set xlabel 'Category'\n";
    scriptFile << "set ylabel 'Amount Spent'\n";
    scriptFile << "set title 'Expense Breakdown'\n";
    scriptFile << "plot 'expenses.dat' using 2:x1 with boxes\n";
    scriptFile.close();

    // Execute the gnuplot script
    system("gnuplot plot.gp");

    return 0;
}