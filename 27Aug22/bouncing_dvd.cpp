// Goal: a basic command line simulation of the iconic bouncing dvd logo

#include <iostream>
#include <unistd.h>
using namespace std;

int const w = 16+2; // 16 + border on left and right
int const h = 9+2; // 9 + border on top and bottom

void cout_display(char bg[], char logo [], int logo_pos)
{
    for( int n=0 ; n<w*h ; n++ )
    {
        if(n%w==0) cout << "\n";

        if(n==logo_pos) cout << logo[0];
        else if(n==logo_pos+1) cout << logo[1];
        else cout << bg[n];
        
    }
    cout << endl;
}

int main()
{  
    // generate background
    char bg [w*h];
    for( int n=0 ; n<w*h ; n++ )
    {
        bg[n]=' ';
        if(n<w) bg[n]='-';
        else if(n>=(w*h-w)) bg[n]='-';
        else if(n%w==0||(n+1)%w==0) bg[n]='|';

        if(n==0) bg[n]='/';
        else if(n==w-1) bg[n]='\\';
        else if(n==w*h-w) bg[n]='\\';
        else if(n==w*h-1) bg[n]='/';
    }

    // init bouncing logo
    char logo [2] = { '[', ']' };
    int logo_pos = w+1;
    int x_vel = 1;
    int y_vel = 1;

    // animation loop
    while(true)
    {
        system("clear");
        cout_display(bg, logo, logo_pos);
        usleep(500 * 1000); // update every 500ms
 
        if((y_vel>0 && logo_pos>=w*(h-2)) || (y_vel<0 && logo_pos<(w*2))) y_vel = -y_vel; // bottom/top collision
        if((x_vel>0 && (logo_pos+3)%w==0) || (x_vel<0 && (logo_pos-1)%w==0)) x_vel = -x_vel; // right/left collision

        logo_pos += x_vel + w*y_vel;
    }

    return 0;
}