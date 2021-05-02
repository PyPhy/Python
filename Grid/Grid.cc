#include <iostream>
#include <math.h>
#include <fstream>

using namespace std;

void linspace(double a, double b, int n, double *x)
{
    double h = (b - a)/ n;

    for (int i = 0; i < n; i++)
    {
        x[i] = a + h* i;
    }
}

double Psi(double x, double xm, double y, double ym, double A, double k)
{
    return A* sin( k* sqrt( pow(x - xm, 2) + pow(y - ym, 2) ) );
}

void JmpingPt(int Ny, double *y, int Nym, double *ym)
{
    int Start = Ny/2 - Nym/2;

    for (int i = 0; i < Nym; i++)
    {
        ym[i] = y[Start + i];
    }
}

int main()
{
	string dmy;
    double Lx , Ly;
    int Nx, Ny;

	fstream file("input.txt", ios_base::in);
	file >> dmy >> dmy >> Lx
         >> dmy >> dmy >> Ly
         >> dmy >> dmy >> Nx
         >> dmy >> dmy >> Ny;
	file.close();
	
    double A = 1, k = 1;

    double GDx[Nx], GDy[Ny];
    linspace(-Lx/2, Lx/2, Nx, GDx);
    linspace(-Ly/2, Ly/2, Ny, GDy);

    int Nxm = Nx/2 - Nx/4, Nym = Ny/2;

    double xm = GDx[Nxm];

    double ym[Nym];
    JmpingPt(Ny, GDy, Nym, ym);

    double z[Nx][Ny];
    ofstream MyCSVfile("DataZ.csv");

    for (int iy = 0; iy < Ny; iy++){
        for (int ix = 0; ix < Nx; ix++)
        {
            z[ix][iy] = 0;
            for (int jm = 0; jm < Nym; jm++)
            {
                z[ix][iy] += Psi(GDx[ix], xm, GDy[iy], ym[jm], A, k);
            }

            MyCSVfile << z[ix][iy] << ",";
        }
        MyCSVfile << "\n";
        cout << iy << endl;
    }

    MyCSVfile.close();
}
