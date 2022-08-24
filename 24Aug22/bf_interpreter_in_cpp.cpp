// Goal: a relatively compact brainf*** interpreter written in C++
// notes: supports underflowing, 256 memory cells, and up to 256 nested loops

#include <iostream>
using namespace std;

int main()
{
    // example hello world from wikipedia (NOT MY CODE)
    string bf = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.";

    // memory cells and pointer
    int arr [256] = {0};
    int ptr = 0;

    int n=0; // current instruction
    int loop [256] = {0}; // stores position of start of each loop
    int loop_num = 0; // points to closest-nested loop
    while(n<bf.length())
    {
        if(bf[n]=='+') arr[ptr]++;
        else if(bf[n]=='-') { arr[ptr]--; if(arr[ptr]<0) arr[ptr]=255; }
        else if(bf[n]=='>') ptr++;
        else if(bf[n]=='<') ptr--;
        else if(bf[n]=='.') cout << char(arr[ptr]);
        else if(bf[n]==',') { char temp; cin >> temp; bf[n]=int(temp); }
        else if(bf[n]=='[') { loop_num++; loop[loop_num]=n; }
        else if(bf[n]==']') { if(arr[ptr]>0) { n=loop[loop_num]; } else { loop_num--; } }

        n++;
    }
    cout<<endl;    
    

    return 0;
}