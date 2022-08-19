#include <iostream>
using namespace std;

// a notes/todo app
// commands:
// list: logs a list of tasks
// new: opens a prompt to add new task
// new [task name string]: creates a new task named [task name string]
// remove: opens a prompt to remove a task by id (indexing starts at 1)
// remove [index]: removes the task at index
// move: opens a prompt to select the current and new index for a task
// move [current index] [new index]: moves the task at [current index] to [new index]

// issues: move 2 1 duplicates
//              3 2 fails when 4 tasks in list
//              3 1 fails when 5 tasks in list
// fails when two indexes = length??
// 4 3 fails on length 5

void cout_arr_by_len(int len, string arr[])
{
    for( int n=0 ; n<len ; n++ ) cout << n+1 << ") " << arr[n] << endl;
}

int main()
{
    // init
    string *list;
    int list_len = 3;
    list = new string[list_len] { "do homework", "think of project ideas", "work on this project ;)" };


    while (true)
    {
        string command;
        cout << "]";
        cin >> command;

        if(command == "list") cout_arr_by_len(list_len, list);
        else if(command == "new")
        {
            // input
            string item;
            cout << "new task: ";
            cin.ignore();
            getline(cin, item);

            // new string[]
            string temp [list_len+1];
            for ( int n=0 ; n<list_len ; n++ ) temp[n] = list[n];
            temp[list_len] = item;
            list_len++;
            
            // replace list
            delete[]list;
            list = new string[list_len];
            for ( int n=0 ; n<list_len ; n++ ) list[n] = temp[n];

            cout << "appended \"" << item << "\" to list";
        }
        else if(command == "remove")
        {
            // input
            int index;
            cout << "index (>=1) to delete: ";
            cin >> index;

            // check
            if ( index<=list_len && index>0 )
            {
                // new string[]
                string temp [list_len-1];
                int temp_int = 0;
                for( int n=0 ; n<=list_len ; n++ ) 
                {
                    if(n!=index-1)
                    {
                        temp[temp_int] = list[n]; 
                        temp_int++;
                    }
                }
                list_len--;

                // replace list
                delete[]list;
                list = new string[list_len];
                for ( int n=0 ; n<list_len ; n++ ) list[n] = temp[n];

                cout << "removed task with index of " << index << " from list";

            }
            else cout << "failed to remove task from list";
        }
        else if(command == "move")
        {
            // input
            int current_index;
            cout << "current index to move: ";
            cin >> current_index;

            int new_index;
            cout << "new index: ";
            cin >> new_index;
            
            string temp = list[current_index-1];
            for ( int n=list_len ; n>=new_index ; n-- )
            {
                list[n] = list[n-1];
            }
            list[new_index-1] = temp;

            cout << "moved index of " << current_index << " to position of " << new_index << endl;
        }

        cout << "\n" << endl;
    }

    return 0;
}