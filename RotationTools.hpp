#pragma once

class RotationTools
{
    RotationTools(DJI::OSDK::Telemetry::Vector3f eulerRad_in);
    RotationTools(DJI::OSDK::Telemetry::Vector3d eulerRad_in) ;
    RotationTools(DJI::OSDK::Telemetry::Quaternion quat_in);
    ~RotationTools();

    void ToEulerRad();
    void ToEulerDeg();
    void ToQuaternion();

    DJI::OSDK::Telemetry::Quaternion quaternion;
    DJI::OSDK::Telemetry::Vector3f eulerf;
    DJI::OSDK::Telemetry::Vector3f eulerd;

}

