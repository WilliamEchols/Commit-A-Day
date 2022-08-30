// Goal: convert text to brainf*** output in a relatively compact format

#include <iostream>
#include <regex>

using namespace std;

int main()
{
    const string text = "I am pretty sure that I can put any string here now :)";
    string bf = ">";

    // text to ascii values
    int ascii_vals [text.length()];
    for( int n=0 ; n<text.length() ; n++) ascii_vals[n] = static_cast<int>(text[n]);
    
    // find minimum characters to represent each ascii value
    int factors [] = { 3, 5, 15, 17, 51, 85 };
    int previous_ascii = 0;
    for( int n=0 ; n<text.length() ; n++ )
    {
        int next_value = abs(ascii_vals[n]-previous_ascii);
        int remainder_num, divider, multiplier;

        int min_index = 0;
        int min_char_count = 1000;
        for( int r=0 ; r<(sizeof(factors)/sizeof(factors[0])); r++ ) 
        {
            remainder_num = next_value%factors[min_index]; // add on at end

            divider = factors[min_index];
            multiplier = next_value/divider;
            int char_count=(255/divider) + multiplier + remainder_num;
            if(char_count<=min_char_count) 
            {
                min_index=r;

            }
        }

        string divider_str;
        for( int i=0 ; i<(255/divider) ; i++ ) divider_str += "-";

        string multiplier_str;
        for( int i=0 ; i<multiplier ; i++ ) if(ascii_vals[n]>=ascii_vals[n-1]) {multiplier_str += "+";} else { multiplier_str += "-"; };

        string remainder_str;
        for( int i=0 ; i<remainder_num ; i++ ) if(ascii_vals[n]>=ascii_vals[n-1]) {remainder_str += "+";} else { remainder_str += "-"; };

        string loop_block = "-[" + divider_str + "<" + multiplier_str + ">]";
        if(multiplier<1) loop_block = "";

        bf += loop_block + "<" + remainder_str + ".>";

        previous_ascii=ascii_vals[n];
    }
    
    // go back and erase itself from memory
    bf += "<[-]";

    // minor formmating
    bf = regex_replace(bf, regex("><"), ""); 

    cout << bf << endl;

    return 0;
}