#ifndef __SINGLETON_HPP__
#define __SINGLETON_HPP__
 
// templatized Singleton Pattern
// 23.06.09 bw
 
template<class T>
class Singleton {
    public :
        ~Singleton(){
            if(m_pInst == nullptr){
                return;
            }
            delete m_pInst;
            m_pInst = nullptr;
        }
 
        static T* getInstance(){
            if(m_pInst == nullptr){         // Lazy Initialization
                m_pInst = new T;
            }
            return m_pInst;
        }
 
    private :
        static T* m_pInst;
 
    protected:
        Singleton(){};
        Singleton(const T&){};
 
};
 
template<typename T>
T* Singleton<T>::m_pInst = nullptr;
 
#endif //__SINGLETON_HPP__