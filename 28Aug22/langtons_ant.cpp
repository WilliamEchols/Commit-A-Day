// Goal: simulate Langton's Ant
// note: the classical Langton's Ant is not limited by a specific grid size, allowing it to eventually run out of the grid;
//       however, this has not been implemented, meaning once the ant has "left" the grid, results are extraneous

#include <iostream>
#include <unistd.h>
using namespace std;

void cout_grid(int l, char grid [])
{
    for( int n=0 ; n<l*l ; n++ )
    {
        if(n%l==0) cout << "\n";
        cout << grid[n] << " ";         
    }
    cout << endl;
}

int main()
{
    // grid
    const int l = 10;
    char grid [l*l];

    char white_marker = '-';
    char black_marker = 'o';
    for( int n=0 ; n<l*l ; n++ ) grid[n]=white_marker;

    // ant
    int pos = (l*l+l)/2;
    int direction = 0;

    int iteration = 0; 
    while (true)
    {
        system("clear");
        cout << "Langton's Ant" << endl;

        // update grid and direction
        if(grid[pos]==white_marker)
        {
            direction += 90;
            if(direction >= 360) direction-=360;

            grid[pos]=black_marker;
        } else {
            direction -= 90;
            if(direction < 0) direction+=360;

            grid[pos]=white_marker;
        }

        cout << "direction: " << direction << "deg" << endl;
        cout << "iteration: " << iteration << endl;

        // move ant
        if(direction==0) pos-=l;
        else if(direction==90) pos++;
        else if(direction==180) pos+=l;
        else if(direction==270) pos--;

        cout_grid(l, grid);
        iteration++;
        usleep(500 * 1000);
    }


    return 0;
}