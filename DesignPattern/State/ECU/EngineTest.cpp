#include "Engine.hpp"
#include <stdio.h>
int main(){
    Engine* Engine1 = Engine::getInstance();
    Engine::EngineOut output;

    Engine1->init();
    for(int i = 0; i < 1000; i++){
        if(i < 500)
            Engine1->update(1);
        else
            Engine1->update(0);
        output = Engine1->getOutput();
        printf("%4i : RPM %8.1f\n", i, output.RPM);
    }
}