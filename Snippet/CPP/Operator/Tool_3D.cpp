#pragma once
#include "Tool_3D.hpp"
#include <math.h>

// Vector Operation
namespace TOOL_3D 
{
    Vector3::Vector3()
    {
        dX = 0.000;
        dY = 0.000;
        dZ = 0.000;
    }
    Vector3::Vector3(double x, double y, double z)
    {
        dX = x;
        dY = y;
        dZ = z;
    }
    Vector3::Vector3(Euler euler)
    {
        dX = euler.phi;
        dY = euler.theta;
        dZ = euler.psi;
    }
	// Vector Norm
	double Vector3::norm()
	{
		double out = 0.0;
		out = sqrt(dX*dX + dY*dY + dZ*dZ);
		return out;
	}

	// Vector Normalization
	void Vector3::normalize()
	{
		double out = 0.0;
		out = sqrt(dX*dX + dY * dY + dZ * dZ);
		if (out > 0.000000001)
		{
			dX = dX / out;
			dY = dY / out;
			dZ = dZ / out;
		}
		else    // Error Exception
		{

		}

	}
	
    // Generate Zero Vector
    void Vector3::Zero()
    {
        dX = 0.000;
        dY = 0.000;
        dZ = 0.000;
    }

    // Vector Operation
    Vector3 operator+(Vector3 A)
    {
        Vector3 out;
        out.dX = A.dX;
        out.dY = A.dY;
        out.dZ = A.dZ;
        return out;
    }
    Vector3 operator-(Vector3 A)
    {
        Vector3 out;
        out.dX = -A.dX;
        out.dY = -A.dY;
        out.dZ = -A.dZ;
        return out;
    }
	Vector3 operator+(Vector3 A, Vector3 B)
	{
		Vector3 out;
		out.dX = A.dX + B.dX;
		out.dY = A.dY + B.dY;
		out.dZ = A.dZ + B.dZ;
		return out;
	}
	Vector3 operator-(Vector3 A, Vector3 B)
	{
		Vector3 out;
		out.dX = A.dX - B.dX;
		out.dY = A.dY - B.dY;
		out.dZ = A.dZ - B.dZ;
		return out;
	}
	double operator*(Vector3 A, Vector3 B)
	{
		return (A.dX*B.dX + A.dY*B.dY + A.dZ*B.dZ);
	}
	Vector3 operator*(double A, Vector3 B)
	{
		Vector3 out;
		out.dX = A * B.dX;
		out.dY = A * B.dY;
		out.dZ = A * B.dZ;
		return out;
	}
	Vector3 operator*(Vector3 A, double B)
	{
		Vector3 out;
		out.dX = A.dX*B;
		out.dY = A.dY*B;
		out.dZ = A.dZ*B;
		return out;
	}
	Vector3 operator/(double A, Vector3 B)
	{
		Vector3 out;
		out.dX = A / B.dX;
		out.dY = A / B.dY;
		out.dZ = A / B.dZ;
		return out;
	}
	Vector3 operator/(Vector3 A, double B)
	{
		Vector3 out;
		out.dX = A.dX / B;
		out.dY = A.dY / B;
		out.dZ = A.dZ / B;
		return out;
	}
}

// Matrix Operation
namespace TOOL_3D 
{
    // Matrix Operation
    void Matrix3::Zero()
    {
        m11 = 0.000; m12 = 0.000; m13 = 0.000;
        m21 = 0.000; m22 = 0.000; m23 = 0.000;
        m31 = 0.000; m32 = 0.000; m33 = 0.000;
    }
    void Matrix3::Ones()
    {
        m11 = 1.000; m12 = 0.000; m13 = 0.000;
        m21 = 0.000; m22 = 1.000; m23 = 0.000;
        m31 = 0.000; m32 = 0.000; m33 = 1.000;
    }
    void Matrix3::Transpose()
    {
        m12 = m21;  m13 = m31;
        m21 = m12;              m23 = m32;
        m31 = m13;  m32 = m23;
    }
}

// Matrix - Vector Operation
namespace TOOL_3D 
{
    // Operations between vector3 and matrix3
    Vector3 operator*(Matrix3 A, Vector3 B)
    {
        Vector3 out;
        out.dX = A.m11 * B.dX + A.m12 * B.dY + A.m13 * B.dZ;
        out.dY = A.m21 * B.dX + A.m22 * B.dY + A.m23 * B.dZ;
        out.dZ = A.m31 * B.dX + A.m32 * B.dY + A.m33 * B.dZ;

        return out;
    }
}