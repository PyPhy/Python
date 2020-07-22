#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void Load(int Np, double *M, double *x, double *y, double *Vx, double *Vy)
{
	FILE * f1 = fopen("Data/x.txt",  "r");	// Load x coordinates
	FILE * f2 = fopen("Data/y.txt",  "r");	// Load y coordinates
	FILE * f3 = fopen("Data/vx.txt", "r");	// Load Vx Velocity
	FILE * f4 = fopen("Data/vy.txt", "r");	// Load Vy Velocity
	FILE * f5 = fopen("Data/M.txt",  "r");  // Load M mass

	for(int i = 0; i < Np; i++){
		fscanf(f1, "%lE\t", &x[i]);
		fscanf(f2, "%lE\t", &y[i]);
		fscanf(f3, "%lE\t", &Vx[i]);
		fscanf(f4, "%lE\t", &Vy[i]);
		fscanf(f5, "%lE\t", &M[i]);
	}

	fclose(f1);
	fclose(f2);
	fclose(f3);
	fclose(f4);
	fclose(f5);
}

void Acc(int Np, double rm, double ep, double *M, double *x, double *y, double *Ax, double *Ay)
{
    float r, C;

    for(int i = 0; i < Np; i++){

        Ax[i] = 0.0;
        Ay[i] = 0.0;

        for(int j = 0; j < Np; j++){
            if(i != j){

                r = sqrt( pow(x[i] - x[j], 2) + pow(y[i] - y[j], 2) );
                C = (12* ep/ pow(rm, 2))* ( pow(rm/ r, 14) - pow(rm/ r, 8) )/ M[i];

                Ax[i] += C* (x[i] - x[j]);
                Ay[i] += C* (y[i] - y[j]);
            }
        }
    }
}

void main()
{
	double Data[5];
	FILE * fImpVar = fopen("Inputs.txt", "r");
	for(int i = 0; i < 5; i++){
		fscanf(fImpVar, "%*s %*s %lf\n", &Data[i]);
		printf("%f\n", Data[i]);
	}
	fclose(fImpVar);

	double tmax = Data[1], dt = Data[2], rm = Data[3], eps = Data[4], t = 0;
	int N = Data[0];
	int count = 1;

	double M[N], x[N], y[N], vx[N], vy[N], aox[N], aoy[N], a1x[N], a1y[N], a2x[N], a2y[N];

	Load(N, M, x, y, vx, vy);

	FILE * fX  = fopen("Data/x.txt",  "w");
	FILE * fY  = fopen("Data/y.txt",  "w");
	FILE * fVx = fopen("Data/vx.txt", "w");
	FILE * fVy = fopen("Data/vy.txt", "w");

	// Euler Cromer method
	Acc(N, rm, eps, M, x, y, aox, aoy);

	for(int i = 0; i < N; i++){
		vx[i] += aox[i]* dt;
		vy[i] += aoy[i]* dt;

		x[i]  += vx[i]* dt;
		y[i]  += vy[i]* dt;
	}

	t += dt;

	Acc(N, rm, eps, M, x, y, a1x, a1y);
	for(int i = 0; i < N; i++){
		fprintf(fX,  "%lE\t", x[i]);
		fprintf(fY,  "%lE\t", y[i]);
		fprintf(fVx, "%lE\t", vx[i]);
		fprintf(fVy, "%lE\t", vy[i]);
	}
	fprintf(fX,  "\n");
	fprintf(fY,  "\n");
	fprintf(fVx, "\n");
	fprintf(fVy, "\n");

	while(t <= tmax){

		for(int i = 0; i < N; i++){
			x[i] += vx[i]* dt + (4* a1x[i] - aox[i])* pow(dt, 2)/ 6;
			y[i] += vy[i]* dt + (4* a1y[i] - aoy[i])* pow(dt, 2)/ 6;
		}

		Acc(N, rm, eps, M, x, y, a2x, a2y);

		for(int i = 0; i < N; i++){
			vx[i] += (5* a2x[i] + 8* a1x[i] - aox[i])* dt/ 12;
			vy[i] += (5* a2y[i] + 8* a1y[i] - aoy[i])* dt/ 12;
		}

		// Save data
		if(count == 10){
			count = 1;

			for(int i = 0; i < N; i++){
				fprintf(fX,  "%lE\t", x[i]);
				fprintf(fY,  "%lE\t", y[i]);
				fprintf(fVx, "%lE\t", vx[i]);
				fprintf(fVy, "%lE\t", vy[i]);
			}
			fprintf(fX,  "\n");
			fprintf(fY,  "\n");
			fprintf(fVx, "\n");
			fprintf(fVy, "\n");
		}

		for(int i = 0; i < N; i++){
			aox[i] = a1x[i];
			aoy[i] = a1y[i];
		}

		for(int i = 0; i < N; i++){
			a1x[i] = a2x[i];
			a1y[i] = a2y[i];
		}

		// time update
		t += dt;
		count += 1;
	}

	fclose(fX);
	fclose(fY);
	fclose(fVx);
	fclose(fVy);

	printf("Hey Divyang!!! Code run completed successfully !!!\n");
	printf("%f\n", t);
}
