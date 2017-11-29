#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <windows.h>
#include <psapi.h>
#include <ctime>

using namespace std;
using namespace std::chrono;

int N;

template <class Prec>
void fill_array_A(Prec **A){
    int m = 4, k = 4;
    for(int i = 0; i<N; i++){
        for(int j = 0; j<N; j++){
            if(i == j)
                A[i][j] = (-1) * m * (i+1) - k;
            else {
                if(j == i+1)
                    A[i][j] = i;
                else {
                    if(j == i-1)
                        A[i][j] = m / i;
                    else
                        A[i][j] = 0;
                }
            }
        }
    }
    //cout << "Finish A"<<endl;
}

void fill_array_X(int *X){
    srand(time(NULL));
    for(int i = 0; i < N; i++){
        int a = rand();
        if(a % 2 == 0)
            X[i] = -1;
        else X[i] = 1;
    }
}

template <class Prec>
void fill_array_B(Prec **A, int *X, Prec *B){
    for(int i = 0; i < N; i++){
        B[i] = 0;
        for(int j = 0; j < N; j++){
            B[i] += A[i][j] * X[j];
        }
    }
    //cout << "Finish B"<<endl;
}

template <class Prec>
void solve(Prec **A, Prec *result){
        for (int i=0; i<N; i++) {
        // Search for maximum in this column
        Prec maxEl = abs(A[i][i]);
        int maxRow = i;
        for (int k=i+1; k<N; k++) {
            if (abs(A[k][i]) > maxEl) {
                maxEl = abs(A[k][i]);
                maxRow = k;
            }
        }

        // Swap maximum row with current row (column by column)
        for (int k=i; k<N+1;k++) {
            Prec tmp = A[maxRow][k];
            A[maxRow][k] = A[i][k];
            A[i][k] = tmp;
        }

        // Make all rows below this one 0 in current column
        for (int k=i+1; k<N; k++) {
            Prec c = -A[k][i]/A[i][i];
            for (int j=i; j<N+1; j++) {
                if (i==j) {
                    A[k][j] = 0;
                } else {
                    A[k][j] += c * A[i][j];
                }
            }
        }
    }

    // Solve equation Ax=b for an upper triangular matrix A
    for (int i=N-1; i>=0; i--) {
        result[i] = A[i][N]/A[i][i];
        for (int k=i-1;k>=0; k--) {
            A[k][N] -= A[k][i] * result[i];
        }
    }
}

template <class Prec>
void test(Prec **A, int *X){
    Prec *result = new Prec[N];
    Prec *B = new Prec[N];

    fill_array_A(A);
    fill_array_B(A, X, B);

    Prec **A_to_solve = new Prec*[N];
    for(int i=0; i<N; i++)
        A_to_solve[i] = new Prec[N+1];

    for(int i=0; i<N; i++){
        for(int j=0; j<N; j++)
            A_to_solve[i][j] = A[i][j];
        A_to_solve[i][N] = B[i];
    }

    high_resolution_clock::time_point t1 = high_resolution_clock::now();
    solve(A_to_solve, result);
    high_resolution_clock::time_point t2 = high_resolution_clock::now();

    PROCESS_MEMORY_COUNTERS pmc;
    GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
    cout << "Memory used: " << pmc.WorkingSetSize/1024 << "KB" << endl;

    if (N <= 15){
        cout << endl << "Wektor zadany" << endl;
        for(int i = 0; i<N; i++)
            cout << X[i] << endl;

        cout << endl << "Wektor otrzymany" << endl;
        for(int i = 0; i<N; i++)
            cout << result[i] << endl;
    }

    Prec *err = new Prec[N];

    for(int i = 0; i<N; i++)
        err[i] = abs(result[i] - X[i]);

    Prec d = 0.0;
    for(int i = 0; i<N; i++)
        d += err[i] * err[i];
    cout << "Metryka euklidesowa: " << sqrt(d) << endl;

    auto duration = duration_cast<microseconds>( t2 - t1 ).count();
    cout << "Elapsed time: " << duration << endl;

    for(int i=0; i<N; i++){
        delete [] A_to_solve[i];
    }
    delete [] A_to_solve;
    delete [] err;
    delete [] result;
    delete [] B;
}

template <class Prec>
void thomas_method(Prec **A, int *X){
    //Create a,b,c vectors
    Prec *a = new Prec[N];
    Prec *b = new Prec[N];
    Prec *c = new Prec[N];
    Prec *d = new Prec[N];
    Prec *result = new Prec[N];

    fill_array_A(A);
    fill_array_B(A, X, d);
    high_resolution_clock::time_point t1 = high_resolution_clock::now();

    for(int i = 0; i<N; i++){
        if(i == 0){
            a[i] = 0;
            b[i] = A[i][i];
            c[i] = A[i][i-1];
            continue;
        }
        if(i == N-1){
            a[i] = A[i][i-1];
            b[i] = A[i][i];
            c[i] = 0;
            continue;
        }
        a[i] = A[i][i-1];
        b[i] = A[i][i];
        c[i] = A[i][i+1];
    }

    // Create beta and gamma vectors
    Prec *beta = new Prec[N];
    Prec *gamma = new Prec[N];

    beta[0] = (-1) * c[0] / b[0];
    gamma[0] = d[0] / b[0];

    for(int i = 1; i<N; i++){
        beta[i] = (-1) * c[i] / (a[i] * beta[i-1] + b[i]);
        gamma[i] = (d[i] - a[i]*gamma[i-1]) / (a[i] * beta[i-1] + b[i]);
    }

    // Create result vector
    result[N-1] = gamma[N-1];

    for(int i = N-2; i>=0; i--)
        result[i] = beta[i]*result[i+1] + gamma[i];

    high_resolution_clock::time_point t2 = high_resolution_clock::now();

    PROCESS_MEMORY_COUNTERS pmc;
    GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
    cout << "Memory used: " << pmc.WorkingSetSize/1024 << "KB" << endl;

    if (N <= 15){
        cout << endl << "Wektor zadany" << endl;
        for(int i = 0; i<N; i++)
            cout << X[i] << endl;

        cout << endl << "Wektor otrzymany" << endl;
        for(int i = 0; i<N; i++)
            cout << result[i] << endl;
    }

    Prec *err = new Prec[N];

    for(int i = 0; i<N; i++)
        err[i] = abs(result[i] - X[i]);

    Prec dist = 0.0;
    for(int i = 0; i<N; i++)
        dist += err[i] * err[i];

    cout << "Metryka euklidesowa: " << sqrt(dist) << endl;

    auto duration = duration_cast<nanoseconds>( t2 - t1 ).count();
    cout << "Elapsed time: " << duration << endl;

    delete [] a;
    delete [] b;
    delete [] c;
    delete [] d;
    delete [] err;
    delete [] result;
    delete [] beta;
    delete [] gamma;
}

int main()
{
    cout.precision(20);

    cout << "Podaj N: ";
    cin >> N;

    float **A_float = new float*[N];
    double **A_double = new double*[N];

    for(int i=0; i<N; i++){
        A_float[i] = new float[N];
        A_double[i] = new double[N];
    }

    int *X = new int[N];
    fill_array_X(X);

    //cout << endl << "Float precision: " << endl;
    //test<float>(A_float, X);

    //cout << endl << "Double precision: " << endl;
    //test<double>(A_double, X);

    cout << endl << "Thomas - float precision: " << endl;
    thomas_method<float>(A_float, X);

    cout << endl << "Thomas - double precision: " << endl;
    thomas_method<double>(A_double, X);

    for(int i=0; i<N; i++){
        delete [] A_float[i];
        delete [] A_double[i];
    }
    delete [] A_double;
    delete [] A_float;
    delete [] X;

    cout << endl;
    return 0;
}
