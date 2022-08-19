// geometric pi estimator using random points

// Goal: estimate pi using a geometric process (if you have a circle inside of a square then the ratio between the amount
//                                              of random points inside each should be a ratio that can estimate pi)
//                                              #in-circle / #in-square * 4

#include <iostream>
#include <cmath>

using namespace std;

int rand_int(int min, int max)
{
    return rand() % (max - min) + min;
}

bool in_circle(int pos_x, int pos_y, int radius) // !in_circle is in_square
{
    return pow(pos_x, 2) + pow(pos_y, 2) <= pow(radius, 2);
}

int main()
{
    int radius = 100;

    int point_num;
    cout << "number of points to estimate pi: " << endl;
    cin >> point_num;

    // generate and categorize random points
    int in_circle_num = 0;
    for( int n=0; n<point_num ; n++ )
    {
        int rand_x = rand_int(0, radius); 
        int rand_y = rand_int(0, radius); 

        in_circle_num += in_circle(rand_x, rand_y, radius);
    }

    // calculate estimation
    float estimation = 4*(float)in_circle_num / (float)point_num;
    cout << "pi estimation: " << estimation << endl;
    cout << "points in circle: " << in_circle_num << endl;
    cout << "total points: " << point_num << endl;

    return 0;
}