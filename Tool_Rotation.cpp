#include "Tool_Rotation.hpp"
#include <math.h>

// Quaternion Operation
namespace TOOL_ROTATION
{
    Quaternion::Quaternion()
    {
        q0 = 1.000;
        q1 = 0.000;
        q2 = 0.000;
        q3 = 0.000;
    }
    Quaternion::Quaternion(double q0_in, double q1_in, double q2_in, double q3_in)
    {
        q0 = q0_in;
        q1 = q1_in;
        q2 = q2_in;
        q3 = q3_in;
    }

    Quaternion operator+(Quaternion A, Quaternion B)
    {
        Quaternion out;
        out.q0 = A.q0 + B.q0;
        out.q1 = A.q1 + B.q1;
        out.q2 = A.q2 + B.q2;
        out.q3 = A.q3 + B.q3;
        return out;
    }
    Quaternion operator-(Quaternion A, Quaternion B)
    {
        Quaternion out;
        out.q0 = A.q0 - B.q0;
        out.q1 = A.q1 - B.q1;
        out.q2 = A.q2 - B.q2;
        out.q3 = A.q3 - B.q3;
        return out;
    }
    // Hamilton Product
    Quaternion operator*(Quaternion A, Quaternion B)
    {
        Quaternion out;
        out.q0 = A.q0 * B.q0 - A.q1 * B.q3 - A.q2 * B.q2 - A.q3 * B.q3;
        out.q1 = A.q0 * B.q1 + A.q1 * B.q0 + A.q2 * B.q3 - A.q3 * B.q2;
        out.q2 = A.q0 * B.q2 - A.q1 * B.q1 + A.q2 * B.q0 + A.q3 * B.q1;
        out.q3 = A.q0 * B.q3 + A.q1 * B.q2 - A.q2 * B.q1 + A.q3 * B.q0;
        return out;
    }
    //Quaternion operator/(Quaternion A, Quaternion B)
    void Quaternion::normalize()
    {
        double norm = 1.000000000 / sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
        if (norm > 0.000000001)
        {
            q0 = q0 / norm;
            q1 = q1 / norm;
            q2 = q2 / norm;
            q3 = q3 / norm;
        }
        else    // Error Exception
        {

        }
    }
    void Quaternion::conjugate()
    {
        //q0 = q0;
        q1 = -q1;
        q2 = -q2;
        q3 = -q3;
    }
    void Quaternion::inverse()
    {
        double Qsqr = q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3;
        if (Qsqr > 0.00000000001)
        {
            q0 = q0 / Qsqr;
            q1 = q1 / Qsqr;
            q2 = q2 / Qsqr;
            q3 = q3 / Qsqr;
        }
        else // Error Exception
        {

        }
    }
    Quaternion Quaternion::normalize_out()
    {
        Quaternion out;
        double Qsqr = q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3;
        if (Qsqr > 0.00000000001)
        {
            out.q0 = q0 / Qsqr;
            out.q1 = q1 / Qsqr;
            out.q2 = q2 / Qsqr;
            out.q3 = q3 / Qsqr;
        }
        else // Error Exception
        {
            out = Quaternion(q0, q1, q2, q3);
        }
        return out;
    }
    Quaternion Quaternion::conjugate_out()
    {
        Quaternion out;
        out.q0 =  q0;
        out.q1 = -q1;
        out.q2 = -q2;
        out.q3 = -q3;
        return out;
    }
    Quaternion Quaternion::inverse_out()
    {
        Quaternion out;
        double Qsqr = q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3;
        if (Qsqr > 0.00000000001)
        {
            out.q0 = q0 / Qsqr;
            out.q1 = -q1 / Qsqr;
            out.q2 = -q2 / Qsqr;
            out.q3 = -q3 / Qsqr;
        }
        else // Error Exception
        {
            out = Quaternion(q0,q1,q2,q3);
        }
        return out;
    }

    double Quaternion::norm()
    {
        double out;
        out = sqrt(q0*q0 + q1 * q1 + q2 * q2 + q3 * q3);
        return out;
    }
}

// Rotation Matrix and Rotation Operation
namespace TOOL_ROTATION
{
    RotationTool::RotationTool(Euler euler_in)
    {
        // Euler angle;
        euler = euler_in;

        double cosR2 = cos(euler.phi * 0.500);
        double sinR2 = sin(euler.phi * 0.500);
        double cosP2 = cos(euler.theta * 0.500);
        double sinP2 = sin(euler.theta * 0.500);
        double cosY2 = cos(euler.psi * 0.500);
        double sinY2 = sin(euler.psi * 0.500);

        quat.q0 = cosR2 * cosP2 * cosY2 + sinR2 * sinP2 * sinY2;
        quat.q1 = sinR2 * cosP2 * cosY2 - cosR2 * sinP2 * sinY2;
        quat.q2 = cosR2 * sinP2 * cosY2 + sinR2 * cosP2 * sinY2;
        quat.q3 = cosR2 * cosP2 * sinY2 - sinR2 * sinP2 * cosY2;
        quat.normalize();
    }
    RotationTool::RotationTool(Matrix3 dcm_in)
    {
        dcm = dcm_in;
        quat.q0 = 0.5000 * sqrt(1.000 + dcm.m11 + dcm.m22 + dcm.m33);
        quat.q1 = 0.2500 * (dcm.m31 - dcm.m13) / quat.q0;
        quat.q2 = 0.2500 * (dcm.m23 - dcm.m32) / quat.q0;
        quat.q3 = 0.2500 * (dcm.m12 - dcm.m21) / quat.q0;
        quat.normalize();
    }
    RotationTool::RotationTool(Quaternion quat_in)
    {
        quat = quat_in.normalize_out();
    }
    RotationTool::RotationTool(const double phiRad, const double thetaRad, const double psiRad)
    {
        euler.phi   = phiRad;
        euler.theta = thetaRad;
        euler.psi   = psiRad;

        double cosR2 = cos(euler.phi * 0.500);
        double sinR2 = sin(euler.phi * 0.500);
        double cosP2 = cos(euler.theta * 0.500);
        double sinP2 = sin(euler.theta * 0.500);
        double cosY2 = cos(euler.psi * 0.500);
        double sinY2 = sin(euler.psi * 0.500);

        quat.q0 = cosR2 * cosP2 * cosY2 + sinR2 * sinP2 * sinY2;
        quat.q1 = sinR2 * cosP2 * cosY2 - cosR2 * sinP2 * sinY2;
        quat.q2 = cosR2 * sinP2 * cosY2 + sinR2 * cosP2 * sinY2;
        quat.q3 = cosR2 * cosP2 * sinY2 - sinR2 * sinP2 * cosY2;
        quat.normalize();
    }
    RotationTool::RotationTool(const double q0, const double q1, const double q2, const double q3)
    {
        quat.q0 = q0;
        quat.q1 = q1;
        quat.q2 = q2;
        quat.q3 = q3;
        quat.normalize();
    }

    void RotationTool::DCM()
    {
        double q0 = quat.q0;
        double q1 = quat.q1;
        double q2 = quat.q2;
        double q3 = quat.q3;

        dcm.m11 = q0 * q0 + q1 * q1 - q2 * q2 - q3 * q3;    dcm.m12 = 2.0 * (q1 * q2 - q0 * q3);                dcm.m13 = 2.0 * (q1 * q3 + q0 * q2);
        dcm.m21 = 2.0 * (q1 * q2 + q0 * q3);                dcm.m22 = q0 * q0 - q1 * q1 + q2 * q2 - q3 * q3;    dcm.m23 = 2.0 * (q2 * q3 - q0 * q1);
        dcm.m31 = 2.0 * (q1 * q3 - q0 * q2);                dcm.m32 = 2.0 * (q2 * q3 + q0 * q1);                dcm.m33 = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3;
    }

    void RotationTool::ToEulerDeg(double &phi, double &theta, double &psi)
    {
        phi   = atan2(2 * (quat.q0*quat.q1 + quat.q2*quat.q3), 1 - 2 * (quat.q1*quat.q1 + quat.q2*quat.q2)) * R2D;
        theta =  asin(2 * (quat.q0*quat.q2 - quat.q3*quat.q1)) * R2D;
        psi   = atan2(2 * (quat.q0*quat.q3 + quat.q1*quat.q2), 1 - 2 * (quat.q2*quat.q2 + quat.q3*quat.q3)) * R2D;
    }
    void RotationTool::ToEulerRad(double &phi, double &theta, double &psi)
    {
        phi   = atan2(2 * (quat.q0*quat.q1 + quat.q2*quat.q3), 1 - 2 * (quat.q1*quat.q1 + quat.q2*quat.q2));
        theta =  asin(2 * (quat.q0*quat.q2 - quat.q3*quat.q1));
        psi   = atan2(2 * (quat.q0*quat.q3 + quat.q1*quat.q2), 1 - 2 * (quat.q2*quat.q2 + quat.q3*quat.q3));
    }
    void RotationTool::ToQuaternion(double &q0, double &q1, double &q2, double &q3)
    {
        q0 = quat.q0;
        q1 = quat.q1;
        q2 = quat.q2;
        q3 = quat.q3;
    }

    Euler RotationTool::ToEuler_out()
    {
        euler.phi   = atan2(2 * (quat.q0*quat.q1 + quat.q2*quat.q3), 1 - 2 * (quat.q1*quat.q1 + quat.q2*quat.q2));
        euler.theta =  asin(2 * (quat.q0*quat.q2 - quat.q3*quat.q1));
        euler.psi   = atan2(2 * (quat.q0*quat.q3 + quat.q1*quat.q2), 1 - 2 * (quat.q2*quat.q2 + quat.q3*quat.q3));
        return euler;
    }
    Matrix3 RotationTool::ToDCM_out()
    {
        DCM();
        return dcm;
    }
    Quaternion RotationTool::ToQuaternion_out()
    {
        return quat;
    }
    Vector3 RotationTool::Rotate(Vector3 in)
    {
        Vector3 out;
        DCM();
        out = dcm * in;
        return out;
    }
}