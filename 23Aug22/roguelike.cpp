// Goal: create a roguelike ASCII game

#include <iostream>
#include <cmath>
using namespace std;

int score=0;
int moves=20;
int p_pos=21;

const int l = 10;

int grid [l*l] = {};

void cout_grid()
{
    for( int n=0 ; n<l*l ; n++ )
    {
        if(n%l==0) cout << "\n";
        
        if(grid[n]==1) cout << "%";
        else if(grid[n]==2) cout << "$";
        else if(grid[n]==3) cout << "@";
        else cout << ".";
    }
    cout << endl;
    cout << "score: " << score << endl;
    cout << "soves left: " << moves << endl;
}
bool chance(int percentage)
{
    int rand_int = rand() % 100;
    return rand_int < percentage;
}
void safe_move_to(int next)
{
    if(grid[next]!=1)
    {
        grid[p_pos]=0;
        p_pos=next;

        if(grid[p_pos]==2) score+=10;
        grid[p_pos]=3;
        moves--;
    }
}

int main()
{
    // init random grid
    for( int n=0 ; n<l*l ; n++ )
    {
        // edge cases (literally)
        if(n%l==0||(n+1)%l==0||n<l||n>(l*l-l)) grid[n]=1;
        else
        {
            // random items
            if(chance(5)) grid[n]=1;
            if(chance(5)) grid[n]=2;
        }
    }

    // player
    grid[p_pos]=3;
    cout_grid();

    // game loop
    bool running = true;
    while(running)
    {
        string move;
        if(moves <= 0)
        {
            // end game loop
            running=false;
            cout << "game over" << endl;
            cout << "final score: " << score << endl;
        }
        else { 
            // input
            cout << "w/a/s/d" << endl;
            cin >> move;
        }

        // movement
        if(move=="w") safe_move_to(p_pos-l);
        if(move=="a") safe_move_to(p_pos-1);
        if(move=="s") safe_move_to(p_pos+l);
        if(move=="d") safe_move_to(p_pos+1);

        // output
        if(running) cout_grid();

    }

    return 0;
}