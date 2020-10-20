#include <RotationTools.hpp>
#include <cmath>
#include <math.h>


RotationTools::RotationTools(DJI::OSDK::Telemetry::Vector3f eulerRad_in)
{
    float phi   = eulerRad_in.x;
    float theta = eulerRad_in.y;
    float psi   = eulerRad_in.z;

}
RotationTools::RotationTools(DJI::OSDK::Telemetry::Vector3d eulerRad_in)
{
    float phi   = eulerRad_in.x;
    float theta = eulerRad_in.y;
    float psi   = eulerRad_in.z;
}
RotationTools::RotationTools(DJI::OSDK::Telemetry::Quaternion quat_in)
{
    DJI::OSDK::Telemetry::Quaternion temp;
    temp = quat_in;
    float quat_norm = sqrt(pow(temp.q0,2)+pow(temp.q1,2)+pow(temp.q2,2)+pow(temp.q3,2));
    
    quaternion = quat_in;

}
RotationTools::~RotationTools()
{

}

void RotationTools::ToEulerRad()
{

}
void RotationTools::ToEulerDeg()
{

}
void RotationTools::ToQuaternion()
{

}