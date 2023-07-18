#include <stdio.h>

class cRestaurant{
    public:
        cRestaurant(){};
        ~cRestaurant(){};

    protected:
        char* mName = nullptr;
        double mExpense = 0.0;
        int mNumber = 0;

    public:
        // 
        void setBussinessName(char* BrandName){
            mName = BrandName;
        }
        // Start-Up Expense
        void setStartUpExpense(double Expense){
            mExpense = Expense;
        }
        void setBussinessNumber(int number){
            mNumber = (number > 0) ? number : -1;
        }
        void BussinessInfo(){
            printf("[%8s.%d] Price : %10.1f\n", mName, mNumber, mExpense);
        }
};

class cRestaurantIncubator{
    public:
        int mNumber=0;
        cRestaurantIncubator(){};
        ~cRestaurantIncubator(){};

    public:
        virtual cRestaurant* incubateBussiness() = 0;

    public:
        cRestaurant* NewBussiness(){
            cRestaurant* pRestaurant = incubateBussiness();
            return pRestaurant;
        }
};

class cKorean : public cRestaurantIncubator{
    private:
        static int mNumberOfFamily;
    public:
        cKorean(){}
        ~cKorean(){};
    public:
        virtual cRestaurant* incubateBussiness(){
            cRestaurant* mRestaurant = new cRestaurant;
            mNumberOfFamily++;
            mRestaurant->setBussinessName("Korean");
            mRestaurant->setStartUpExpense(5000);
            mRestaurant->setBussinessNumber(mNumberOfFamily);
            return mRestaurant;
        }
};
int cKorean::mNumberOfFamily = 0;
class cSushi : public cRestaurantIncubator{
    private:
        static int mNumberOfFamily;
    public:
        cSushi(){}
        ~cSushi(){};
    public:
        virtual cRestaurant* incubateBussiness(){
            cRestaurant* mRestaurant = new cRestaurant;
            mNumberOfFamily++;
            mRestaurant->setBussinessName("Sushi");
            mRestaurant->setStartUpExpense(7000);
            mRestaurant->setBussinessNumber(mNumberOfFamily);
            return mRestaurant;
        }
};
int cSushi::mNumberOfFamily = 0;
class cChinese : public cRestaurantIncubator{
    private:
        static int mNumberOfFamily;
    public:
        cChinese(){}
        ~cChinese(){};
    public:
        virtual cRestaurant* incubateBussiness(){
            cRestaurant* mRestaurant = new cRestaurant;
            mNumberOfFamily++;
            mRestaurant->setBussinessName("Chinese");
            mRestaurant->setStartUpExpense(4000);
            mRestaurant->setBussinessNumber(mNumberOfFamily);
            return mRestaurant;
        }
};
int cChinese::mNumberOfFamily = 0;