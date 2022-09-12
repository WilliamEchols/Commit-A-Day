// Goal: basic attempt at a semi-3d coin

#include <iostream>
#include <unistd.h>
#include <cmath>

using namespace std;

const int r = 6;
const int l = 20+1;

// distance from rotational center
int distance(int x, int y, int l) 
{
    return sqrt(pow(abs(l/2-x),2)+pow(abs(l/2-y),2));
}
void cout_canvas(int l, char canvas [21][21])
{
    for( int x=0 ; x<l ; x++ )
    {
        for( int y=0 ; y<l; y++ ) cout << canvas[x][y] << " ";
        cout << "\n";
    }
    cout << endl;
}

int main()
{
    // generate circle
    char canvas [l][l] = { ' ' };
    for( int y=0 ; y<l ; y++ )
        for( int x=0 ; x<l ; x++ )
        {
            int dist = distance(x, y, l);
            if(dist==7) canvas[x][y]='%';
            else canvas[x][y]=' ';
        }

    // update loop
    int rot_row = 2; // rotation_row has a funny variable name to pronounce "ruht-row"
    while(true)
    {
        system("clear");

        // rotate
        for( int n=0 ; n<l ; n++ ) 
        {
            // spin in
            if(rot_row<(l/2))
            {
                // left side (rot_row and rot_row+1)
                if(canvas[n][rot_row]=='%') canvas[n][rot_row+1] = canvas[n][rot_row];
                canvas[n][rot_row]=' ';

                // right side (l-rot_row-1 and l-rot_row-2)
                if(canvas[n][l-rot_row-1]=='%') canvas[n][l-rot_row-2] = canvas[n][l-rot_row-1];
                canvas[n][l-rot_row-1]=' ';

            } 

            // spin out
            else
            {
                
            }
        }

        cout_canvas(l, canvas);
        rot_row++;

        usleep(1000 * 1000);
    }

}