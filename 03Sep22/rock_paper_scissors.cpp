// Goal: rock paper scissors

#include <iostream>
#include <unistd.h>

using namespace std;

int main()
{
    // points
    int u_score = 0;
    int r_score = 0;

    while(u_score<3&&r_score<3)
    {
        // user input
        string action [4] = { "rock     (r)", "paper    (p)", "scissors (s)", "shoot!" };
        for ( int i=0 ; i<4 ; i++ )
        {
            usleep(1000 * 1000);
            cout << action[i] << endl;
        }
        char input;
        cin >> input;

        // cpu option
        int r = rand() % 3;

        for ( int i=0 ; i<4 ; i++ )
            if (action[i][0]==input&&action[i]!=action[3]) // if this is user's input
            {
                cout << "User: " << action[i] << " vs Computer: " << action[r] << " -> ";

                if((i<3&&i==r+1)||(i==2&&r==0)) 
                {
                    cout << "user's point!" << endl;
                    u_score++;
                }
                else if((r<3&&r==i+1)||(r==2&&i==0))
                {
                    cout << "computer's point..." << endl;
                    r_score++;
                }
                else 
                {
                    cout << "tie" << endl;
                }

            }
    }

    string winner = u_score > r_score ? "you" : "the computer";
    cout << winner << " won the game!";

    return 0;
}