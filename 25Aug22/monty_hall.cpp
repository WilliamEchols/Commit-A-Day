// Goal: a Monty Hall simulation that demonstrates an increase in probably of "switching" doors in a hypothetical gameshow

#include <iostream>
using namespace std;

int main()
{
    int total;
    cout << "simulation number: " << endl;
    cin >> total;

    int stay_success = 0;
    int swap_success = 0;
    for( int n=0 ; n<total ; n++ )
    {
        int doors [3] = { 0 };
        doors[rand()%3] = 1; // correct door

        int pick = rand()%3; // picked door

        if(doors[pick]==1) stay_success++;
        else swap_success++;
    }

    cout << "stay success: " << stay_success << "/" << total << endl;
    cout << "swap success: " << swap_success << "/" << total << endl;

    return 0;
}