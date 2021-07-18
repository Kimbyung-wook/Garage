#pragma once

// Vector Operations
namespace TOOL_3D 
{
    // Euler angle(radians) : phi theta psi
    typedef struct Euler
    {
        double phi;     // Roll
        double theta;   // Pitch
        double psi;     // Yaw
    }Euler;

	class Vector3
	{
    public:
		double dX;
		double dY;
		double dZ;

        Vector3();
        Vector3(double x, double y, double z);
        Vector3(Euler euler);
        //Vector3(Euler euler);
        //~Vector3();

		// Vector Norm
		double norm();
		// Vector Normalization
		void normalize();
        // Generate Zero Vector
        void Zero();
	};

    Vector3 operator+(Vector3 A);
    Vector3 operator-(Vector3 A);
    Vector3 operator+(Vector3 A, Vector3 B);
    Vector3 operator-(Vector3 A, Vector3 B);
	double  operator*(Vector3 A, Vector3 B);
	double  operator*(Vector3 A, Vector3 B);
	Vector3 operator*(double  A, Vector3 B);
	Vector3 operator*(Vector3 A, double  B);
	Vector3 operator/(double  A, Vector3 B);
	Vector3 operator/(Vector3 A, double  B);
}

// Matrix Operation
namespace TOOL_3D 
{
    class Matrix3
    {
    public:
        double m11, m12, m13;
        double m21, m22, m23;
        double m31, m32, m33;

        void Zero();
        void Ones();
        void Transpose();
    };
}

// Matrix - Vector Operation
namespace TOOL_3D
{
    Vector3 operator*(Matrix3 A, Vector3 B);
}