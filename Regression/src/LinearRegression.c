/*
 * Machine Learning by Progyan1997
 * MIT License
 * Linear Regression - Fitting observation points to a straight line
 */

#ifndef __LinearRegression
#define __LinearRegression

#ifndef __math_h
#include <math.h>
#endif
#ifndef __stdio_h
#include <stdio.h>
#endif

typedef struct {
	double m, c;			// Slope and y-intercept
} EquationSpec;

typedef struct {
	EquationSpec RegEq;		// Equation of Regression Line
	double R2, StdErr;		// R2 and Standard Error of Estimation
} RegressionObj;

// Prototype for Linear Regression method
RegressionObj LinearRegression(int, double[], double[]);

// Main method
int main(void) {
	int n;
	printf("Enter the number of observation: ");
	scanf("%d", &n);
	double x[n], y[n];
	for (int i = 0; i < n; i++) {
		printf("Enter x[%d]: ", i + 1);
		scanf("%lf", x + i);
		printf("Enter y[%d]: ", i + 1);
		scanf("%lf", y + i);
	}
	RegressionObj regobj = LinearRegression(n, x, y);
	printf("Equation of the Regression Line: y = %g x + %g\n", regobj.RegEq.m, regobj.RegEq.c);
	printf("Value of R2 = %g\n", regobj.R2);
	printf("Standard Error of Estimation: %g\n", regobj.StdErr);
	return 0;
}

// Definition of Linear Regression
RegressionObj LinearRegression(int n, double x[], double y[]) {
	// House-keeping
	if (n < 2)
		return (RegressionObj) { (EquationSpec) { 0.0, 0.0}, 0.0, 0.0 };
	
	// Calculating Mean
	double _x = 0.0, _y = 0.0;
	for (int i = 0; i < n; i++)
		_x += x[i], _y += y[i];
	_x = _x / n, _y = _y / n;
	
	// Calculating Slope and y-intercept
	double m, c, dx[n], dx2 = 0.0, dy[n], dxdy = 0.0;
	for (int i = 0; i < n; i++) {
		dx[i] = (x[i] - _x), dy[i] = (y[i] - _y);
		dx2 += dx[i] * dx[i], dxdy += dx[i] * dy[i];
	}
	m = dxdy / dx2;
	c = _y - m * _x;
	
	// Calculating Estimation and R2
	double Y[n], R2, dy2 = 0.0, dY = 0.0;
	for (int i = 0; i < n; i++) {
		Y[i] = m * x[i] + c;
		dy2 += dy[i] * dy[i], dY += (Y[i] - _y) * (Y[i] - _y);
	}
	R2 = dY / dy2;
	
	// Calculating Standard Error of Estimation
	double StdErr, var;
	dY = 0.0;
	for (int i = 0; i < n; i++)
		dY += (Y[i] - y[i]) * (Y[i] - y[i]);
	var = dY / (n - 2);
	StdErr = sqrt(var);
	
	// Return the results
	return (RegressionObj) { (EquationSpec) { m, c}, R2, StdErr };
}

#endif
