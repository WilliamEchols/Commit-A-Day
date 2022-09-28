#include <vector>
#include <iostream>
  
using namespace std;
  
int factorial(int n) {
  if(n > 1)
    return n * factorial(n - 1);
  else
    return 1;
}

void logNestedVector(vector<vector<string>> nestedVector)
{
    for(vector<string> x : nestedVector)
    {
        for(string y : x) {
            cout << y;
        }
        cout << endl;
    }
}

void logVector(vector<string> vector)
{
    for(string point : vector) {
        cout << point;
        cout << endl;
    }
}

vector<string> genSeedVector(int n)
{

    

    string seedString("");
    for (int i = 1; i <= n; i++)
        seedString += to_string(i);

    vector<string> seedVector;

    do
    {
        seedVector.push_back(seedString);
    }
    while ( next_permutation(seedString.begin(), seedString.end()) );

    seedVector.resize(factorial(n - 1));
    for(int i = 0; i < factorial(n - 1); i++)
    {
        seedVector[i] += seedVector[i].substr(0, seedVector[i].size() - 1);
    }

    //logVector(seedVector);

    return seedVector;    
    
}

int determineOverlap(string string1, string string2)
{
    int charsToCheck = string1.length() < string2.length() ? string1.length() : string2.length();

    int overlapNum = 0;
    for (int i = 0; i <= charsToCheck; i++)
        if(string1.substr(string1.size() - i) == string2.substr(0, i))
            overlapNum = i;

    return overlapNum;
}

void genSuperVector(vector<string> semiPermutations)
{
    // determine starting vector
    vector<string> allSuperPermutations;

    do {
        string currentSuperPermutation("");
        for(string semi : semiPermutations)
            // combine
            int overlapNum = determineOverlap(currentSuperPermutation, semi);
            //semi.erase(0, overlapNum);
            //currentSuperPermutation += semi;

        allSuperPermutations.push_back(currentSuperPermutation);
    } while (std::next_permutation(semiPermutations.begin(), semiPermutations.end()));

    //logVector(allSuperPermutations);
}

int main()
{
    int n = 4;
    vector<string> seedVector = genSeedVector(n); // vector of semi-permutations

    genSuperVector(seedVector);

    return 0;
}