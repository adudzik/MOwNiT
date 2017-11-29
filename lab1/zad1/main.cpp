#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>

using namespace std;

int N;

template <class Prec>
void fill_array_A(Prec **A){
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            if(i == 0)
                A[i][j] = 1.0;
            else{
                A[i][j] = 1.0 / (i + j + 1);
            }
        }
    }
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

    solve(A_to_solve, result);

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

    cout << endl << "Metryka euklidesowa" << endl;
    Prec d = 0.0;
    for(int i = 0; i<N; i++)
        d += err[i] * err[i];
    cout << sqrt(d) << endl;

    for(int i=0; i<N; i++){
        delete [] A_to_solve[i];
    }
    delete [] A_to_solve;
    delete [] err;
    delete [] result;
    delete [] B;
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

    cout << endl << "Float precision: ";
    test<float>(A_float, X);

    cout << endl << "Double precision: ";
    test<double>(A_double, X);

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
