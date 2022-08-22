// Goal: simulate Conway's game of life with a grid of ASCII characters

#include <iostream>

using namespace std;

int num_neighbors(int index, int width, int grid[])
{
    int num = 0;
    // checks for non-wrapping grid
    bool left_check = (index%width != 0);
    bool right_check = ((index+1)%width != 0);
    bool up_check = (index>=width);
    bool down_check = (index<=(width*width-width));

    if(left_check) if(grid[index-1]) num++; // left
    if(right_check) if(grid[index+1]) num++; // right
    if(up_check) if(grid[index-width]) num++; // up
    if(down_check) if(grid[index+width]) num++; // down

    if(left_check&&up_check) if(grid[index-width-1]) num++; // left-up
    if(right_check&&up_check) if(grid[index-width+1]) num++; // right-up
    if(left_check&&down_check) if(grid[index+width-1]) num++; // left-down
    if(right_check&&down_check) if(grid[index+width+1]) num++; // right-down
    

    return num;
}
void cout_grid(int width, int grid[])
{
    for( int n=0 ; n<width*width ; n++ )
    {
        if(n%width==0) cout << "\n";
        
        if(grid[n]) cout << "o";
        else cout << "-";
    }
    cout << endl;
}

int main()
{
    // starting conditions are set with w and grid[]
    const int w = 10;
    int grid[w*w] = { 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    };

    cout_grid(w, grid);

    bool cont = true;
    while (cont)
    {
        string step;
        cout << "step (y/n)" << endl;
        cin >> step;
        if(step=="n"||step=="no") cont=false;

        // game update
        int current_grid [100];
        for( int n=0 ; n<w*w ; n++ ) current_grid[n] = grid[n];
        for( int n=0 ; n<w*w ; n++ )
        {
            int mut = num_neighbors(n, w, grid);
            int cur = grid[n];

            if(cur==0&&mut==3) current_grid[n]=1;
            if(cur==1)
            {
                if(mut<2||mut>3) current_grid[n]=0;
            }
        }
        for( int n=0 ; n<w*w ; n++ ) grid[n] = current_grid[n];

        cout_grid(w, grid);
    }



    return 0;
}