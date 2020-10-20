#pragma once
#include "Tool_3D.hpp"

using namespace TOOL_3D;

// Quaternion Operation
namespace TOOL_ROTATION // Quaternion Operation
{
    class Quaternion
    {
    public:
        double q0;
        double q1;
        double q2;
        double q3;

    public:
        Quaternion();
        Quaternion(double q0, double q1, double q2, double q3);
        //~Quaternion();
        void normalize();
        void conjugate();
        void inverse();
        Quaternion normalize_out();
        Quaternion conjugate_out();
        Quaternion inverse_out();

    private:
        double norm();
    };
    Quaternion operator+(Quaternion A, Quaternion B);
    Quaternion operator-(Quaternion A, Quaternion B);
    // Hamilton Product
    Quaternion operator*(Quaternion A, Quaternion B);
    //Quaternion operator/(Quaternion A, Quaternion B);
}

// Rotation Matrix and Rotation Operation
namespace TOOL_ROTATION
{
    // Rotational Core property is quaternion variable
	class RotationTool
	{
	public:
        RotationTool(Matrix3 dcm_in);
        RotationTool(Euler euler_in);
        RotationTool(Quaternion quat_in);
		RotationTool(const double phiRad, const double thetaRad, const double psiRad);
		RotationTool(const double q0, const double q1, const double q2, const double q3);
		//~RotationTool();

    public:

		void ToEulerDeg(double &phiDeg, double &thetaDeg, double &psiDeg);
		void ToEulerRad(double &phiRad, double &thetaRad, double &psiRad);
        void ToQuaternion(double &q0, double &q1, double &q2, double &q3);

        Euler ToEuler_out();
        Matrix3 ToDCM_out();
        Quaternion ToQuaternion_out();
        Vector3 Rotate(Vector3);


	private:
		Quaternion  quat;	// Quaternion
		Euler       euler;	// radians
		Matrix3     dcm;	// Body 2 Nav
        const double pi = 3.14159;
        const double D2R = pi / 180.000;
        const double R2D = 180.000 / pi;
        void DCM();
	};
}