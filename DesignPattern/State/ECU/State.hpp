#ifndef __STATE_HPP__
#define __STATE_HPP__

class State{
    public:
        State();
        ~State();

    public:
        void init();
        void update();
        void terminate();

    public:
        char stateName[20];
    
};

#endif // __STATE_EPP__