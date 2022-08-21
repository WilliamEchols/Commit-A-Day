// Goal: find an even number that cannot be represented as the sum of two primes
// i.e. attempt to disprove Goldbach's conjecture or run out of RAM doing it ;)

#include <iostream>

using namespace std;

bool is_prime(int n)
{
    for( int i=2 ; i<n ; i++ ) if (n%i == 0) return false; 
    return true;
}
bool even_is_sum(int even, int len, int arr[])
{
    for( int x=0 ; x<len ; x++ )
        for( int y=0 ; y<len ; y++ )
            if(arr[x] + arr[y] == even)
                return true;
    return false;
}

int main()
{
    // maximum test limit
    int max_limit;
    cout << "maximum test integer: " << endl;
    cin >> max_limit;

    // generate primes_arr
    int primes_num = 0;
    for( int n=2 ; n<max_limit ; n++ ) if (is_prime(n)) primes_num++;
    int primes_arr [primes_num];
    int temp = 0;
    for( int n=2 ; n<max_limit ; n++ ) 
        if (is_prime(n)) 
        {
            primes_arr[temp] = n;
            temp++;
        }

    // test to see if every even integer until max_limit can be the sum of two primes
    int discrepancies = 0;
    for( int n=2 ; n<max_limit/2 ; n++ )
    {
        if(!even_is_sum(n*2, primes_num, primes_arr)) 
        {
            cout << "miraculously, it appears that " << n*2 << " fails Goldbach's conjecture" << endl;
            discrepancies++;
        }

    }

    if(!discrepancies) cout << "It appears that no even number less than " << max_limit << " fails Goldbach's conjecture" << endl;


    return 0;
}