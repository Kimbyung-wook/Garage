#ifndef __STATE_HPP__
#define __STATE_HPP__
#include "singleton.hpp"

template<class T>
class State : public Singleton{
    public:
        State();
        ~State();

    public:
        T* m_state;
        void init();
        void update();
        void terminate();
};

#endif // __STATE_HPP__